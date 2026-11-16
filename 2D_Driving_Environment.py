"""2D Driving Environment — white rectangular circuit on black background.

Drop this file beside your driving AI script and rename it to
    2D_Driving_Environment.py

Public API intentionally matches the original environment:
Spawn_Car, Get_Info, Change_Value, Check_Progress, Get_Rewards,
Update, Reset, Start_GUI, Render and Close_GUI.

Angles: 0 = UP, 90 = RIGHT, 180 = DOWN, 270 = LEFT.
Raycasts report the distance in pixels to the nearest black wall.
Display dependency: python3 -m pip install pygame
Run this file directly for a looping ten-car demonstration.
Import it from your AI to display the cars controlled by that AI.
"""

import math
import threading
import random
import time
from dataclasses import dataclass
from typing import Optional, Union

# ---------------------------------------------------------------------------
# World / road settings
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1040, 760
BACKGROUND = "#000000"
ROAD_COLOR = "#ffffff"

# Two rectangles make an easy, wide, closed square-like road.
# White between OUTER and INNER; everywhere else is black.
OUTER = (128.0, 100.0, 912.0, 650.0)
INNER = (270.0, 232.0, 770.0, 518.0)
CENTER_X = (OUTER[0] + OUTER[2]) / 2
CENTER_Y = (OUTER[1] + OUTER[3]) / 2

CAR_LENGTH = 26.0
CAR_WIDTH = 14.0
CAR_RADIUS = math.hypot(CAR_LENGTH / 2, CAR_WIDTH / 2)
MAX_RAY_DISTANCE = 1400.0
MAX_SPEED = 165.0        # pixels per second
ACCELERATION = 165.0    # pixels per second squared
BRAKING = 245.0         # pixels per second squared
MAX_TURN_RATE = 170.0   # degrees per second
FPS = 30
DT = 1.0 / FPS

# Only cars that fail to complete their first lap have a time limit.
FIRST_LAP_DEADLINE = 30.0
MAX_CAR_TIME = FIRST_LAP_DEADLINE  # compatibility: first-lap deadline only
SPEED_REWARD_WEIGHT = 5000.0
LAP_REWARD = 1000.0
FAST_LAP_REWARD_WEIGHT = 30000.0
TIMEOUT_PENALTY = 10000.0

CAR_COLORS = (
    "#00b7eb", "#e63946", "#f59e0b", "#8844dd", "#0e9e65",
    "#e559aa", "#d97706", "#1664e8", "#a21caf", "#475569",
)
RAY_COLORS = ("#ff5151", "#00a35b", "#2388ff")


def _normalize(angle):
    return float(angle) % 360.0


def _angular_difference(target, current):
    return (target - current + 180.0) % 360.0 - 180.0


def _point_in_rect(x, y, rect):
    return rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]


def _road_contains(x, y, clearance=0.0):
    """White road: within the outer rectangle but outside the inner black wall."""
    ox0, oy0, ox1, oy1 = OUTER
    ix0, iy0, ix1, iy1 = INNER
    in_outer = (ox0 + clearance <= x <= ox1 - clearance and
                oy0 + clearance <= y <= oy1 - clearance)
    in_inner = (ix0 - clearance <= x <= ix1 + clearance and
                iy0 - clearance <= y <= iy1 + clearance)
    return in_outer and not in_inner


def _raycast(x, y, angle):
    """Ray distance to first black wall, using exact rectangle intersections."""
    rad = math.radians(angle)
    dx, dy = math.sin(rad), -math.cos(rad)
    nearest = MAX_RAY_DISTANCE

    for x0, y0, x1, y1 in (OUTER, INNER):
        if abs(dx) > 1e-12:
            for edge_x in (x0, x1):
                t = (edge_x - x) / dx
                if 1e-7 < t < nearest and y0 - 1e-6 <= y + t * dy <= y1 + 1e-6:
                    nearest = t
        if abs(dy) > 1e-12:
            for edge_y in (y0, y1):
                t = (edge_y - y) / dy
                if 1e-7 < t < nearest and x0 - 1e-6 <= x + t * dx <= x1 + 1e-6:
                    nearest = t

    return nearest


def _track_angle(x, y):
    """Continuous clockwise progress around the rectangular loop."""
    # Angle is normalized for the rectangle's unequal dimensions.
    # Radii of the centerline's approximate ellipse (used only for reward progress).
    rx = CENTER_X - (INNER[0] + OUTER[0]) / 2
    ry = CENTER_Y - (INNER[1] + OUTER[1]) / 2
    return math.atan2((y - CENTER_Y) / ry, (x - CENTER_X) / rx)


def _car_corners(x, y, angle):
    a = math.radians(angle)
    fx, fy = math.sin(a), -math.cos(a)
    sx, sy = math.cos(a), math.sin(a)
    return [(x+fx*f+sx*s, y+fy*f+sy*s)
            for f, s in ((13, 7), (13, -7), (-13, -7), (-13, 7))]


def _car_on_road(x, y, angle):
    # Edges cannot cross the central wall: test polygon/rectangle separation.
    corners = _car_corners(x, y, angle)
    if not all(_point_in_rect(px, py, OUTER) for px, py in corners):
        return False
    ix0, iy0, ix1, iy1 = INNER
    wall = ((ix0, iy0), (ix1, iy0), (ix1, iy1), (ix0, iy1))
    a = math.radians(angle)
    for ax, ay in ((1, 0), (0, 1), (math.sin(a), -math.cos(a)),
                   (math.cos(a), math.sin(a))):
        car_proj = [px*ax+py*ay for px, py in corners]
        wall_proj = [px*ax+py*ay for px, py in wall]
        if max(car_proj) < min(wall_proj) or max(wall_proj) < min(car_proj):
            return True
    return False


@dataclass
class Car:
    car_id: Union[int, str]
    x: float
    y: float
    angle: float = 0.0
    speed: float = 32.0
    target_speed: float = 32.0
    target_angle: float = 0.0
    elapsed: float = 0.0
    distance: float = 0.0
    progress: float = 0.0
    laps: int = 0
    crashed: bool = False
    timed_out: bool = False
    last_track_angle: float = math.pi
    lap_started: float = 0.0
    best_lap_time: Optional[float] = None
    still_since: float = 0.0
    still_distance: float = 0.0
    color: str = "#00b7eb"


class DrivingEnvironment:
    def __init__(self):
        self.cars = {}
        self._next_id = 1
        self.max_car_time = MAX_CAR_TIME
        self.window = None
        self.canvas = None
        self._user_closed = False
        self._pygame = None
        self._last_frame = 0.0
        self._caption = ""
        self._colors = random.SystemRandom()

    def create_car(self, name=None):
        if name is None:
            while self._next_id in self.cars:
                self._next_id += 1
            name = self._next_id
            self._next_id += 1
        if name in self.cars:
            raise ValueError("Car already exists: {!r}".format(name))

        # Place up to 10 cars separately along the left straight, all at 0°.
        index = len(self.cars)
        lane_x = (OUTER[0] + INNER[0]) / 2
        start_y = 550.0 - (index % 10) * 28.0
        car = Car(name, lane_x, start_y)
        car.color = self._colors.choice(CAR_COLORS)
        car.last_track_angle = _track_angle(car.x, car.y)
        self.cars[name] = car
        return name

    def get_info(self, car_id):
        car = self.cars[car_id]
        return {
            "raycast1": _raycast(car.x, car.y, car.angle - 45),
            "raycast2": _raycast(car.x, car.y, car.angle),
            "raycast3": _raycast(car.x, car.y, car.angle + 45),
            "speed": car.speed / MAX_SPEED,
            "angle": _normalize(car.angle),
            "crashed": car.crashed,
            "lap": car.laps,
            "elapsed": car.elapsed,
            "progress": car.progress,
            "best_lap_time": car.best_lap_time if car.best_lap_time is not None else 1,
        }

    def send_info(self, car_id, speed, angle):
        car = self.cars[car_id]
        if not car.crashed:
            car.target_speed = max(0.0, min(1.0, float(speed))) * MAX_SPEED
            car.target_angle = _normalize(angle)

    def update(self, dt=DT):
        dt = max(0.0, min(float(dt), 0.1))
        if self.window is not None:
            self._pump_events()
        for car in list(self.cars.values()):
            if car.crashed:
                continue
            car.elapsed += dt

            desired_change = car.target_speed - car.speed
            max_change = (ACCELERATION if desired_change > 0 else BRAKING) * dt
            car.speed += max(-max_change, min(max_change, desired_change))
            car.speed = max(0.0, min(MAX_SPEED, car.speed))

            turn_limit = MAX_TURN_RATE * (0.25 + 0.75 * car.speed / MAX_SPEED) * dt
            error = _angular_difference(car.target_angle, car.angle)
            car.angle = _normalize(car.angle + max(-turn_limit, min(turn_limit, error)))

            rad = math.radians(car.angle)
            nx = car.x + math.sin(rad) * car.speed * dt
            ny = car.y - math.cos(rad) * car.speed * dt
            if not _car_on_road(nx, ny, car.angle):
                car.crashed = True
                continue

            dx, dy = nx - car.x, ny - car.y
            car.x, car.y = nx, ny
            car.distance += math.hypot(dx, dy)

            new_angle = _track_angle(car.x, car.y)
            delta = (new_angle - car.last_track_angle + math.pi) % (2 * math.pi) - math.pi
            # Unwrapped angle avoids jumping at the top/left crossing.
            car.progress += delta / (2 * math.pi) * 2080.0
            car.last_track_angle = new_angle
            new_laps = max(0, int(car.progress / 2080.0))
            if new_laps > car.laps:
                lap_time = car.elapsed - car.lap_started
                car.best_lap_time = lap_time if car.best_lap_time is None else min(car.best_lap_time, lap_time)
                car.lap_started = car.elapsed
                car.laps = new_laps

            # Evaluate after movement so a lap finished at the deadline counts.
            if (self.max_car_time is not None and car.laps == 0
                    and car.elapsed >= self.max_car_time):
                car.crashed = True  # existing AI loops use this as "trial ended"
                car.timed_out = True

    def get_rewards(self, car_id):
        """Cumulative fitness; inspect it, do not add it again every frame.

        Speed earns up to 5000 points, scaled by first-lap progress so
        driving in tiny circles or crashing immediately cannot win on speed.
        After the first lap, the full speed bonus applies. Each completed lap
        earns 1000; a smaller fastest-lap time earns a larger extra bonus.
        Wall collisions stop scoring but deduct nothing. Failure to finish
        the first lap within 30 seconds deducts 10000 points.
        """
        car = self.cars[car_id]
        average_speed = car.distance / car.elapsed if car.elapsed > 0 else 0.0
        progress_reward = max(-100.0, car.progress)
        progress_factor = min(1.0, max(0.0, car.progress) / 2080.0)
        speed_ratio = min(1.0, max(0.0, average_speed / MAX_SPEED))
        speed_bonus = SPEED_REWARD_WEIGHT * speed_ratio ** 2 * progress_factor
        lap_bonus = car.laps * LAP_REWARD
        fastest_lap_bonus = (FAST_LAP_REWARD_WEIGHT / max(1.0, car.best_lap_time)
                            if car.best_lap_time is not None else 0.0)
        timeout_penalty = TIMEOUT_PENALTY if car.timed_out else 0.0
        total = progress_reward + speed_bonus + lap_bonus + fastest_lap_bonus - timeout_penalty
        return {
            "distance_reward": round(progress_reward, 2),
            "average_speed": average_speed,
            "speed_bonus": round(speed_bonus, 2),
            "crash_penalty": 0.0,
            "timeout_penalty": round(timeout_penalty, 2),
            "lap_bonus": round(lap_bonus, 2),
            "fastest_lap_bonus": round(fastest_lap_bonus, 2),
            "time_penalty": 0.0,
            "total": round(total, 2),
        }

    def check_progress(self, car_id):
        """Average speed is distance / elapsed simulation time, in pixels/second."""
        car = self.cars[car_id]
        return {
            "crashed": car.crashed,
            "distance": round(car.distance, 2),
            "forward_progress": round(car.progress, 2),
            "fastest_lap_time": car.best_lap_time if car.best_lap_time is not None else 1,
            "laps": car.laps,
            "average_speed": car.distance / car.elapsed if car.elapsed > 0 else 0.0,
            "elapsed": round(car.elapsed, 2),
            "reward": self.get_rewards(car_id)["total"],
            "timed_out": car.timed_out,
        }

    def get_results(self, car_id):
        car = self.cars[car_id]
        return {
            "car_id": car_id,
            "crashed": car.crashed,
            "distance_travelled": round(car.distance, 2),
            "forward_progress": round(car.progress, 2),
            "lap_count": car.laps,
            "best_lap_time": car.best_lap_time,
            "average_speed": car.distance / car.elapsed if car.elapsed > 0 else 0.0,
            "elapsed": round(car.elapsed, 2),
            "reward": self.get_rewards(car_id),
            "timed_out": car.timed_out,
        }

    def reset(self):
        self.cars.clear()
        self._next_id = 1

    def _on_user_close(self):
        self._user_closed = True
        # Tell the AI race loop its session is over so it doesn't run invisibly.
        for car in self.cars.values():
            car.crashed = True
        self.close_gui()

    def _pump_events(self):
        if self.window is None:
            return
        if threading.current_thread() is not threading.main_thread():
            raise RuntimeError("GUI calls must run on the main Python thread.")
        for event in self._pygame.event.get():
            if event.type == self._pygame.QUIT or (
                event.type == self._pygame.KEYDOWN and event.key == self._pygame.K_ESCAPE
            ):
                self._on_user_close()
                break

    def start_gui(self):
        if self.window is not None:
            return True
        if threading.current_thread() is not threading.main_thread():
            raise RuntimeError("Start_GUI() must run on the main Python thread.")
        try:
            import pygame
        except ImportError as exc:
            raise RuntimeError(
                "Install the display dependency in your Python environment: "
                "python3 -m pip install pygame"
            ) from exc
        self._pygame = pygame
        try:
            pygame.display.init()
            pygame.font.init()
            surface = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("2D Driving - White Track / Black Walls")
            self.canvas = surface
            self.window = _WindowHandle(self)
            self._font = pygame.font.Font(None, 23)
            self._small_font = pygame.font.Font(None, 19)
            self._user_closed = False
            self._last_frame = 0.0
            self.render()
            return True
        except Exception:
            self.close_gui()
            raise

    def render(self, caption=""):
        if self.window is None:
            return
        self._pump_events()
        if self.window is None:
            return
        # Pace a visible simulation even when its caller is a tight training loop.
        remaining = DT - (time.perf_counter() - self._last_frame)
        if remaining > 0:
            time.sleep(remaining)
        self._last_frame = time.perf_counter()
        if caption:
            self._caption = str(caption)
        pg, screen = self._pygame, self.canvas
        screen.fill(BACKGROUND)
        def rect(bounds, color):
            x0, y0, x1, y1 = bounds
            pg.draw.rect(screen, color, (int(x0), int(y0), int(x1-x0), int(y1-y0)))
        rect(OUTER, ROAD_COLOR)
        rect(INNER, BACKGROUND)
        def text(message, position, color="#eeeeee", small=False):
            font = self._small_font if small else self._font
            screen.blit(font.render(message, True, color), position)
        for active in self.cars.values():
            readings = []
            for offset, color in zip((-45, 0, 45), RAY_COLORS):
                angle = active.angle + offset
                distance = _raycast(active.x, active.y, angle)
                readings.append(distance)
                rad = math.radians(angle)
                end = (active.x + math.sin(rad)*distance,
                       active.y - math.cos(rad)*distance)
                pg.draw.line(screen, color, (active.x, active.y), end, 2)
                pg.draw.circle(screen, color, (round(end[0]), round(end[1])), 3)

        for car in self.cars.values():
            pg.draw.polygon(screen, car.color if not car.crashed else "#777777",
                            _car_corners(car.x, car.y, car.angle))
            pg.draw.polygon(screen, "#202020", _car_corners(car.x, car.y, car.angle), 1)
            # A windshield marks the front, while the body stays rectangular.
            a = math.radians(car.angle)
            fx, fy, sx, sy = math.sin(a), -math.cos(a), math.cos(a), math.sin(a)
            pg.draw.line(screen, "#173247",
                         (car.x+fx*6-sx*4, car.y+fy*6-sy*4),
                         (car.x+fx*6+sx*4, car.y+fy*6+sy*4), 3)
            text(str(car.car_id), (car.x+17, car.y+6), "#777777", True)
        alive = sum(not c.crashed for c in self.cars.values())
        text(self._caption or "2D DRIVING ENVIRONMENT", (26, 30))
        text("CARS: {} / {} ACTIVE".format(alive, len(self.cars)), (790, 30))
        text("White = road | Black = wall | 0 degrees = up | Esc = close",
             (290, HEIGHT-24), small=True)
        pg.display.flip()

    def close_gui(self):
        if self._pygame is not None:
            self._pygame.display.quit()
        self.window = self.canvas = None
        if globals().get("_env") is self:
            globals()["window"] = None


class _WindowHandle:
    """Compatibility for older drivers that end with Env.window.mainloop()."""
    def __init__(self, environment):
        self.environment = environment

    def mainloop(self):
        while self.environment.window is self:
            self.environment.render()

    def destroy(self):
        self.environment._on_user_close()


# Public wrapper functions — keep compatibility with the existing AI file.
_env = DrivingEnvironment()

def Create_Car(Name=None): return _env.create_car(Name)
def Spawn_Car(Name=None): return _env.create_car(Name)
def Get_Info(CarID): return _env.get_info(CarID)
def Send_Info(CarID, Speed, Angle): return _env.send_info(CarID, Speed, Angle)
def Change_Value(CarID, Speed, Angle): return _env.send_info(CarID, Speed, Angle)
def Update(dt=DT): return _env.update(dt)
def Get_Rewards(CarID): return _env.get_rewards(CarID)
def Check_Progress(CarID): return _env.check_progress(CarID)
def Get_Results(CarID): return _env.get_results(CarID)
def Reset(): return _env.reset()
def Start_GUI():
    result = _env.start_gui()
    globals()["window"] = _env.window
    return result
def Render(caption=""): return _env.render(caption)
def Close_GUI():
    _env.close_gui()
    globals()["window"] = None

window = None

def _demo_control(environment, car):
    # Preview controller only: never applied to cars driven by an imported AI.
    left, right, top, bottom = 199.0, 841.0, 166.0, 584.0
    targets = ((left, top), (right, top), (right, bottom), (left, bottom))
    index = getattr(car, "demo_target", 0)
    tx, ty = targets[index]
    if math.hypot(tx-car.x, ty-car.y) < 36:
        index = (index+1) % len(targets)
        car.demo_target = index
        tx, ty = targets[index]
    angle = math.degrees(math.atan2(tx-car.x, -(ty-car.y))) % 360
    environment.send_info(car.car_id, 0.55, angle)


def Demo():
    """Live preview until closed."""
    for i in range(10):
        Spawn_Car("Car{}".format(i+1))
    _env.max_car_time = None
    Start_GUI()
    try:
        while _env.window is not None:
            for car in _env.cars.values():
                _demo_control(_env, car)
            Update()
            Render("LIVE DEMO - ten rectangular cars")
    except KeyboardInterrupt:
        pass
    finally:
        Close_GUI()
        _env.max_car_time = MAX_CAR_TIME


if __name__ == "__main__":
    Demo()
