"""2D Driving Environment — white rectangular circuit on black background.

Drop this file beside your driving AI script and rename it to
    2D_Driving_Environment.py

Public API intentionally matches the original environment:
Spawn_Car, Get_Info, Change_Value, Check_Progress, Get_Rewards,
Update, Reset, Start_GUI, Render and Close_GUI.

Angles: 0 = UP, 90 = RIGHT, 180 = DOWN, 270 = LEFT.
Raycasts report the distance in pixels to the nearest black wall.
No extra dependencies: uses Python's standard tkinter graphics library.
"""

import math
import threading
import tkinter as tk
from dataclasses import dataclass
from typing import Optional, Union

# ---------------------------------------------------------------------------
# World / road settings
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1040, 760
BACKGROUND = "#080808"
ROAD_COLOR = "#f7f7f7"

# Two rectangles make an easy, wide, closed square-like road.
# White between OUTER and INNER; everywhere else is black.
OUTER = (128.0, 100.0, 912.0, 650.0)
INNER = (270.0, 232.0, 770.0, 518.0)
CENTER_X = (OUTER[0] + OUTER[2]) / 2
CENTER_Y = (OUTER[1] + OUTER[3]) / 2

CAR_RADIUS = 7.0
MAX_RAY_DISTANCE = 1400.0
MAX_SPEED = 165.0        # pixels per second
ACCELERATION = 165.0    # pixels per second squared
BRAKING = 245.0         # pixels per second squared
MAX_TURN_RATE = 170.0   # degrees per second
FPS = 30
DT = 1.0 / FPS

# Prevent one very slow / stationary clone keeping a generation alive forever.
MAX_CAR_TIME = 35.0
STILL_TIME_LIMIT = 7.0
STILL_DISTANCE = 5.0

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


class DrivingEnvironment:
    def __init__(self):
        self.cars = {}
        self._next_id = 1
        self.window = None
        self.canvas = None
        self._user_closed = False

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
        start_y = 466.0 - (index % 10) * 13.0
        car = Car(name, lane_x, start_y)
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
        for car in list(self.cars.values()):
            if car.crashed:
                continue
            car.elapsed += dt

            if car.elapsed >= MAX_CAR_TIME:
                car.crashed = True
                car.timed_out = True
                continue

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
            if not _road_contains(nx, ny, CAR_RADIUS):
                car.crashed = True
                continue

            dx, dy = nx - car.x, ny - car.y
            car.x, car.y = nx, ny
            car.distance += math.hypot(dx, dy)

            # If the car has barely travelled for 7 seconds, end its trial.
            if car.distance - car.still_distance >= STILL_DISTANCE:
                car.still_distance = car.distance
                car.still_since = car.elapsed
            elif car.elapsed - car.still_since >= STILL_TIME_LIMIT:
                car.crashed = True
                car.timed_out = True
                continue

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

    def get_rewards(self, car_id):
        car = self.cars[car_id]
        progress_reward = max(-100.0, car.progress)
        crash_penalty = 60.0 if car.crashed and not car.timed_out else 0.0
        stall_penalty = 35.0 if car.timed_out else 0.0
        lap_bonus = 0.0
        if car.best_lap_time is not None:
            lap_bonus = car.laps * 200.0 + 3000.0 / max(1.0, car.best_lap_time)
        time_penalty = car.elapsed * 0.3
        return {
            "distance_reward": round(progress_reward, 2),
            "crash_penalty": round(crash_penalty, 2),
            "lap_bonus": round(lap_bonus, 2),
            "time_penalty": round(time_penalty, 2),
            "total": round(progress_reward - crash_penalty - stall_penalty + lap_bonus - time_penalty, 2),
        }

    def check_progress(self, car_id):
        car = self.cars[car_id]
        return {
            "crashed": car.crashed,
            "distance": round(car.distance, 2),
            "forward_progress": round(car.progress, 2),
            "fastest_lap_time": car.best_lap_time if car.best_lap_time is not None else 1,
            "laps": car.laps,
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

    def start_gui(self):
        if self.window is not None:
            return True
        if threading.current_thread() is not threading.main_thread():
            raise RuntimeError("Start_GUI() must run on the main Python thread.")
        try:
            self.window = tk.Tk()
            self.window.title("2D Driving — White Track / Black Walls")
            self.window.resizable(False, False)
            self.window.configure(bg=BACKGROUND)
            self.canvas = tk.Canvas(
                self.window, width=WIDTH, height=HEIGHT,
                bg=BACKGROUND, highlightthickness=0, bd=0,
            )
            self.canvas.pack(fill="both", expand=True)
            self.window.protocol("WM_DELETE_WINDOW", self._on_user_close)
            self._user_closed = False
            self.render()
            self.window.lift()
            return True
        except Exception as exc:
            self.close_gui()
            raise RuntimeError(
                "Could not open the 2D Driving GUI: {}. "
                "Try running 'python3 -m tkinter' in Terminal.".format(exc)
            ) from exc

    def render(self, caption=""):
        if self.window is None or self.canvas is None:
            return
        c = self.canvas
        c.delete("all")
        # BLACK outside / WHITE ring / BLACK center. A genuine closed rectangle.
        c.create_rectangle(0, 0, WIDTH, HEIGHT, fill=BACKGROUND, outline="")
        c.create_rectangle(*OUTER, fill=ROAD_COLOR, outline=ROAD_COLOR)
        c.create_rectangle(*INNER, fill=BACKGROUND, outline=BACKGROUND)

        # A very subtle guide along the lane center, kept inside the white road.
        lmid = (OUTER[0] + INNER[0]) / 2
        rmid = (OUTER[2] + INNER[2]) / 2
        tmid = (OUTER[1] + INNER[1]) / 2
        bmid = (OUTER[3] + INNER[3]) / 2
        c.create_rectangle(lmid, tmid, rmid, bmid, outline="#c8c8c8", width=1, dash=(9, 13))

        for index, car in enumerate(list(self.cars.values())):
            rad = math.radians(car.angle)
            fx, fy = math.sin(rad), -math.cos(rad)
            sx, sy = math.cos(rad), math.sin(rad)
            points = (
                car.x + fx * 16, car.y + fy * 16,
                car.x - fx * 11 + sx * 9, car.y - fy * 11 + sy * 9,
                car.x - fx * 11 - sx * 9, car.y - fy * 11 - sy * 9,
            )
            color = CAR_COLORS[index % len(CAR_COLORS)] if not car.crashed else "#777777"
            c.create_polygon(points, fill=color, outline="#121212", width=2)
            # Number labels make it clear all 10 clones are present.
            name = str(car.car_id)
            label = name.replace("Clone", "")
            c.create_text(car.x + 16, car.y + 13, text=label,
                          fill="#151515", anchor="nw", font=("Arial", 10, "bold"))

        # Draw three sensor rays for the first still-active car (otherwise cluttered).
        active = next((car for car in self.cars.values() if not car.crashed), None)
        if active is not None:
            readings = (
                _raycast(active.x, active.y, active.angle - 45),
                _raycast(active.x, active.y, active.angle),
                _raycast(active.x, active.y, active.angle + 45),
            )
            for offset, distance, color in zip((-45, 0, 45), readings, RAY_COLORS):
                radians = math.radians(active.angle + offset)
                ex = active.x + math.sin(radians) * distance
                ey = active.y - math.cos(radians) * distance
                c.create_line(active.x, active.y, ex, ey, fill=color, width=2, dash=(7, 5))
                c.create_oval(ex - 3, ey - 3, ex + 3, ey + 3, fill=color, outline="")
            c.create_text(
                WIDTH // 2, HEIGHT - 43,
                text="{}  |  LEFT {:5.0f}px     FRONT {:5.0f}px     RIGHT {:5.0f}px".format(
                    active.car_id, *readings),
                fill="#eeeeee", font=("Arial", 13, "bold"), anchor="center",
            )
        else:
            c.create_text(WIDTH // 2, HEIGHT - 43,
                          text="ALL CARS FINISHED",
                          fill="#eeeeee", font=("Arial", 13, "bold"))

        total = len(self.cars)
        alive = sum(not car.crashed for car in self.cars.values())
        title = caption or "2D DRIVING ENVIRONMENT"
        c.create_text(27, 40, text=title, fill="#ffffff", anchor="w",
                      font=("Arial", 19, "bold"))
        c.create_text(WIDTH - 25, 40, text="CARS: {} / {} ACTIVE".format(alive, total),
                      fill="#eeeeee", anchor="e", font=("Arial", 13, "bold"))
        c.create_text(WIDTH // 2, HEIGHT - 17,
                      text="White = drivable road   |   Black = wall   |   Cars start facing up (0°)",
                      fill="#aaaaaa", font=("Arial", 10))

        try:
            self.window.update_idletasks()
            self.window.update()
        except tk.TclError:
            self._on_user_close()

    def close_gui(self):
        if self.window is not None:
            try:
                self.window.destroy()
            except tk.TclError:
                pass
        self.window = None
        self.canvas = None


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
def Start_GUI(): return _env.start_gui()
def Render(caption=""): return _env.render(caption)
def Close_GUI(): return _env.close_gui()

if __name__ == "__main__":
    import time
    print("Opening the 2D Driving Environment test window...")
    for i in range(1, 11):
        Spawn_Car("Clone{}".format(i))
    Start_GUI()
    try:
        for frame in range(30 * 20):
            if _env.window is None:
                break
            # Simple demonstration: drive upward at moderate speed, then try a turn.
            for car in _env.cars.values():
                if not car.crashed:
                    Change_Value(car.car_id, 0.58, 0 if frame < 110 else 90)
            Update()
            Render()
            time.sleep(DT)
    except KeyboardInterrupt:
        pass
    finally:
        Close_GUI()
