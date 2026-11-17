"""2D Driving Environment — five selectable racing circuits.

Place this file beside your existing driving AI script.

    Set_Map(1)   # easiest
    Set_Map(5)   # hardest

Set_Map resets the current race (removes cars) and changes the track; use it
between races or before calling Start_Race. Reset() removes cars but keeps the
selected map. No changes to the original API or reward dictionary are required.

Angles: 0 = UP, 90 = RIGHT, 180 = DOWN, 270 = LEFT.
Raycasts: distance in pixels to the nearest wall.
Install graphical dependency with: python3 -m pip install pygame
Preview: python 2D_Driving_Environment.py [map_number]
"""

import math
import random
import sys
import threading
import time
from dataclasses import dataclass
from typing import Optional, Union


# ---------------------------------------------------------------------------
# World / driving settings (compatible with the original environment)
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 1040, 760
BACKGROUND = "#000000"
ROAD_COLOR = "#ffffff"

CAR_LENGTH = 26.0
CAR_WIDTH = 14.0
CAR_RADIUS = math.hypot(CAR_LENGTH / 2, CAR_WIDTH / 2)
MAX_RAY_DISTANCE = 1400.0
MAX_SPEED = 165.0
ACCELERATION = 165.0
BRAKING = 245.0
MAX_TURN_RATE = 170.0
FPS = 30
DT = 1.0 / FPS

# These rewards are intentionally the same as in your previous environment.
FIRST_LAP_DEADLINE = 30.0
MAX_CAR_TIME = FIRST_LAP_DEADLINE
SPEED_REWARD_WEIGHT = 5000.0
LAP_REWARD = 1000.0
FAST_LAP_REWARD_WEIGHT = 30000.0
TIMEOUT_PENALTY = 10000.0

CAR_COLORS = (
    "#00b7eb", "#e63946", "#f59e0b", "#8844dd", "#0e9e65",
    "#e559aa", "#d97706", "#1664e8", "#a21caf", "#475569",
)
RAY_COLORS = ("#ff5151", "#00a35b", "#2388ff")

# Each track is a CLOSED clockwise centerline, with a road of the given width.
# Wider roads / fewer corners are easier; narrower winding roads are harder.
# Coordinates are screen pixels. No external geometry package is needed.
MAPS = {
    1: {
        "name": "Training Loop",
        "description": "Wide road, four easy corners",
        "width": 132.0,
        "points": (
            (199, 584), (199, 166), (841, 166), (841, 584),
        ),
    },
    2: {
        "name": "Rounded Circuit",
        "description": "Gentle diagonal corners, slightly narrower road",
        "width": 112.0,
        "points": (
            (216, 577), (170, 490), (170, 285), (235, 164),
            (792, 164), (860, 282), (860, 465), (792, 577),
        ),
    },
    3: {
        "name": "Zigzag Circuit",
        "description": "Alternating bends and tighter corners",
        "width": 94.0,
        "points": (
            (210, 575), (193, 465), (252, 390), (187, 307),
            (210, 189), (359, 168), (456, 229), (556, 169),
            (812, 183), (844, 300), (784, 386), (844, 473),
            (803, 568), (632, 572), (543, 518), (453, 577),
        ),
    },
    4: {
        "name": "Technical Hairpins",
        "description": "Sharp direction changes and a narrow road",
        "width": 84.0,
        "points": (
            (199, 592), (200, 468), (313, 399), (198, 329),
            (203, 219), (323, 163), (460, 225), (558, 154),
            (715, 161), (834, 235), (768, 327), (842, 411),
            (775, 497), (831, 590), (677, 572), (590, 486),
            (471, 563), (340, 503),
        ),
    },
    5: {
        "name": "Serpentine Gauntlet",
        "description": "Very narrow track and frequent difficult turns",
        "width": 66.0,
        "points": (
            (203, 590), (175, 517), (245, 462), (173, 392),
            (247, 310), (178, 247), (231, 157), (342, 160),
            (407, 246), (488, 168), (568, 245), (634, 153),
            (743, 158), (850, 234), (780, 308), (855, 380),
            (777, 443), (847, 519), (798, 595), (698, 589),
            (628, 503), (559, 586), (483, 510), (409, 590),
            (337, 516),
        ),
    },
}


def _normalize(angle):
    return float(angle) % 360.0


def _angular_difference(target, current):
    return (target - current + 180.0) % 360.0 - 180.0


def _cross(ax, ay, bx, by):
    return ax * by - ay * bx


def _offset_polygon(points, offset):
    """Miter-offset a non-self-intersecting closed centerline polygon."""
    output = []
    count = len(points)
    for i, (x, y) in enumerate(points):
        previous = points[i - 1]
        following = points[(i + 1) % count]
        ax, ay = x - previous[0], y - previous[1]
        bx, by = following[0] - x, following[1] - y
        la, lb = math.hypot(ax, ay), math.hypot(bx, by)
        ax, ay, bx, by = ax / la, ay / la, bx / lb, by / lb
        # A right-hand normal points inside these clockwise screen-space loops.
        n1x, n1y = -ay, ax
        n2x, n2y = -by, bx
        mx, my = n1x + n2x, n1y + n2y
        divisor = mx * n2x + my * n2y
        if abs(divisor) < 1e-8:
            raise ValueError("Track has an excessively sharp reversal")
        output.append((x + offset * mx / divisor,
                       y + offset * my / divisor))
    return tuple(output)


def _edges(points):
    return tuple((x, y, points[(i + 1) % len(points)][0] - x,
                  points[(i + 1) % len(points)][1] - y)
                 for i, (x, y) in enumerate(points))


def _point_in_polygon(x, y, points):
    """Even/odd containment; exact on-wall positions are treated as collisions."""
    inside = False
    j = len(points) - 1
    for i in range(len(points)):
        x1, y1 = points[j]
        x2, y2 = points[i]
        if (y1 > y) != (y2 > y):
            at_x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < at_x:
                inside = not inside
        j = i
    return inside


def _segments_intersect(ax, ay, bx, by, cx, cy, dx, dy):
    """Proper and touching segment intersections; endpoints count as walls."""
    abx, aby = bx - ax, by - ay
    cdx, cdy = dx - cx, dy - cy
    denom = _cross(abx, aby, cdx, cdy)
    qx, qy = cx - ax, cy - ay
    if abs(denom) < 1e-10:
        if abs(_cross(qx, qy, abx, aby)) > 1e-8:
            return False
        # Collinear segments: test bounding boxes for overlap.
        return (max(min(ax, bx), min(cx, dx)) <= min(max(ax, bx), max(cx, dx))
                and max(min(ay, by), min(cy, dy)) <= min(max(ay, by), max(cy, dy)))
    t = _cross(qx, qy, cdx, cdy) / denom
    u = _cross(qx, qy, abx, aby) / denom
    return -1e-9 <= t <= 1 + 1e-9 and -1e-9 <= u <= 1 + 1e-9


def _car_corners(x, y, angle):
    a = math.radians(angle)
    fx, fy = math.sin(a), -math.cos(a)
    sx, sy = math.cos(a), math.sin(a)
    return tuple((x + fx * f + sx * s, y + fy * f + sy * s)
                 for f, s in ((13, 7), (13, -7), (-13, -7), (-13, 7)))


class Track:
    def __init__(self, map_number):
        config = MAPS[map_number]
        self.number = map_number
        self.name = config["name"]
        self.description = config["description"]
        self.road_width = config["width"]
        self.center = tuple(config["points"])
        self.outer = _offset_polygon(self.center, -self.road_width / 2)
        self.inner = _offset_polygon(self.center, self.road_width / 2)
        self.boundary_edges = _edges(self.outer) + _edges(self.inner)
        # Cache wall bounding boxes expanded by one car radius. Most cars are
        # far enough from the walls to skip polygon/corner collision checks.
        self.nearby_walls = tuple(
            (px, py, dx, dy,
             min(px, px + dx) - CAR_RADIUS, min(py, py + dy) - CAR_RADIUS,
             max(px, px + dx) + CAR_RADIUS, max(py, py + dy) + CAR_RADIUS)
            for px, py, dx, dy in self.boundary_edges
        )
        self.path_edges = _edges(self.center)
        self.path_lengths = tuple(math.hypot(dx, dy)
                                  for _, _, dx, dy in self.path_edges)
        self.path_starts = []
        length = 0.0
        for segment_length in self.path_lengths:
            self.path_starts.append(length)
            length += segment_length
        self.length = length
        self.bounds = (
            min(x for x, _ in self.outer), min(y for _, y in self.outer),
            max(x for x, _ in self.outer), max(y for _, y in self.outer),
        )

    def contains(self, x, y):
        x0, y0, x1, y1 = self.bounds
        return (x0 < x < x1 and y0 < y < y1
                and _point_in_polygon(x, y, self.outer)
                and not _point_in_polygon(x, y, self.inner))

    def car_on_road(self, x, y, angle):
        if not self.contains(x, y):
            return False
        nearby = [(px, py, dx, dy)
                  for px, py, dx, dy, x0, y0, x1, y1 in self.nearby_walls
                  if x0 <= x <= x1 and y0 <= y <= y1]
        if not nearby:
            # If no boundary is within a whole-car radius, the full car fits.
            return True
        corners = _car_corners(x, y, angle)
        if not all(self.contains(px, py) for px, py in corners):
            return False
        # Corners alone are not sufficient for concave walls: check car edges.
        for i in range(4):
            ax, ay = corners[i]
            bx, by = corners[(i + 1) % 4]
            for cx, cy, dx, dy in nearby:
                if _segments_intersect(ax, ay, bx, by,
                                       cx, cy, cx + dx, cy + dy):
                    return False
        return True

    def raycast(self, x, y, angle):
        radians = math.radians(angle)
        rx, ry = math.sin(radians), -math.cos(radians)
        nearest = MAX_RAY_DISTANCE
        for px, py, dx, dy in self.boundary_edges:
            denominator = _cross(rx, ry, dx, dy)
            if abs(denominator) < 1e-10:
                continue
            qx, qy = px - x, py - y
            distance = _cross(qx, qy, dx, dy) / denominator
            along = _cross(qx, qy, rx, ry) / denominator
            if 1e-7 < distance < nearest and 0 <= along <= 1:
                nearest = distance
        return nearest

    def position_along_track(self, x, y):
        """Return nearest arc-distance along the centerline, modulo one lap."""
        best_distance_sq = float("inf")
        best_s = 0.0
        for i, (sx, sy, dx, dy) in enumerate(self.path_edges):
            segment_length_sq = dx * dx + dy * dy
            t = max(0.0, min(1.0,
                             ((x - sx) * dx + (y - sy) * dy) / segment_length_sq))
            delta_x = x - (sx + t * dx)
            delta_y = y - (sy + t * dy)
            distance_sq = delta_x * delta_x + delta_y * delta_y
            if distance_sq < best_distance_sq:
                best_distance_sq = distance_sq
                best_s = self.path_starts[i] + t * self.path_lengths[i]
        return best_s % self.length

    def point_at(self, distance):
        s = distance % self.length
        for i, segment_length in enumerate(self.path_lengths):
            if s <= self.path_starts[i] + segment_length:
                t = (s - self.path_starts[i]) / segment_length
                x, y, dx, dy = self.path_edges[i]
                return x + dx * t, y + dy * t
        return self.center[0]

    def starting_position(self, index):
        # Place cars safely on the first straight, without cars hitting each other.
        s = min(34.0 + (index % 4) * 7.0, self.path_lengths[0] * 0.48)
        x, y = self.point_at(s)
        _, _, dx, dy = self.path_edges[0]
        angle = _normalize(math.degrees(math.atan2(dx, -dy)))
        return x, y, angle


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
    last_track_position: float = 0.0
    lap_started: float = 0.0
    best_lap_time: Optional[float] = None
    still_since: float = 0.0
    still_distance: float = 0.0
    color: str = "#00b7eb"


class DrivingEnvironment:
    def __init__(self):
        self.cars = {}
        self._next_id = 1
        self.track = Track(1)
        self.max_car_time = MAX_CAR_TIME
        self.window = None
        self.canvas = None
        self._user_closed = False
        self._pygame = None
        self._last_frame = 0.0
        self._caption = ""
        self._colors = random.SystemRandom()

    def set_map(self, map_number):
        """Change level 1..5. Existing cars are reset for a fresh race."""
        if isinstance(map_number, bool) or not isinstance(map_number, int) or map_number not in MAPS:
            raise ValueError("Map_Number must be an integer from 1 to 5")
        self.track = Track(map_number)
        self.reset()
        self._caption = ""
        if self.window is not None:
            self._pygame.display.set_caption(
                "2D Driving - Level {}: {}".format(map_number, self.track.name))
        return map_number

    def create_car(self, name=None):
        if name is None:
            while self._next_id in self.cars:
                self._next_id += 1
            name = self._next_id
            self._next_id += 1
        if name in self.cars:
            raise ValueError("Car already exists: {!r}".format(name))
        x, y, angle = self.track.starting_position(len(self.cars))
        car = Car(name, x, y, angle=angle, target_angle=angle)
        car.color = self._colors.choice(CAR_COLORS)
        car.last_track_position = self.track.position_along_track(x, y)
        if not self.track.car_on_road(x, y, angle):
            raise RuntimeError("The selected map has an invalid starting position")
        self.cars[name] = car
        return name

    def get_info(self, car_id):
        car = self.cars[car_id]
        return {
            "raycast1": self.track.raycast(car.x, car.y, car.angle - 45),
            "raycast2": self.track.raycast(car.x, car.y, car.angle),
            "raycast3": self.track.raycast(car.x, car.y, car.angle + 45),
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

            radians = math.radians(car.angle)
            nx = car.x + math.sin(radians) * car.speed * dt
            ny = car.y - math.cos(radians) * car.speed * dt
            if not self.track.car_on_road(nx, ny, car.angle):
                car.crashed = True
                continue

            dx, dy = nx - car.x, ny - car.y
            car.x, car.y = nx, ny
            car.distance += math.hypot(dx, dy)

            new_position = self.track.position_along_track(car.x, car.y)
            perimeter = self.track.length
            # Unwrap distance so moving BACKWARDS produces negative progress.
            # One lap is the current map's actual perimeter, not a fixed 2080.
            step = (new_position - car.last_track_position + perimeter / 2) % perimeter - perimeter / 2
            car.progress += step
            car.last_track_position = new_position
            new_laps = max(0, int((car.progress + 1e-7) // perimeter))
            if new_laps > car.laps:
                lap_time = car.elapsed - car.lap_started
                car.best_lap_time = (lap_time if car.best_lap_time is None
                                     else min(car.best_lap_time, lap_time))
                car.lap_started = car.elapsed
                car.laps = new_laps

            # As in the original: only the first lap has a deadline.
            if (self.max_car_time is not None and car.laps == 0
                    and car.elapsed >= self.max_car_time):
                car.crashed = True
                car.timed_out = True

    def get_rewards(self, car_id):
        """Cumulative fitness; do not add this value again every frame.

        Preserves the original scoring formula. Speed rewards depend on
        average speed AND forward progress; driving backwards loses progress.
        Collision = no direct penalty; missing the first-lap deadline = -10000.
        """
        car = self.cars[car_id]
        average_speed = car.distance / car.elapsed if car.elapsed > 0 else 0.0
        progress_reward = max(-100.0, car.progress)
        progress_factor = min(1.0, max(0.0, car.progress) / self.track.length)
        speed_ratio = min(1.0, max(0.0, average_speed / MAX_SPEED))
        speed_bonus = SPEED_REWARD_WEIGHT * speed_ratio ** 2 * progress_factor
        lap_bonus = car.laps * LAP_REWARD
        fastest_lap_bonus = (FAST_LAP_REWARD_WEIGHT / max(1.0, car.best_lap_time)
                            if car.best_lap_time is not None else 0.0)
        timeout_penalty = TIMEOUT_PENALTY if car.timed_out else 0.0
        total = (progress_reward * 3 + speed_bonus * 3 + car.laps * 5000
                 + fastest_lap_bonus * 3 - timeout_penalty)
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
                    event.type == self._pygame.KEYDOWN and event.key == self._pygame.K_ESCAPE):
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
                "Install the display dependency: python3 -m pip install pygame"
            ) from exc
        self._pygame = pygame
        try:
            pygame.display.init()
            pygame.font.init()
            self.canvas = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption(
                "2D Driving - Level {}: {}".format(self.track.number, self.track.name))
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
        remaining = DT - (time.perf_counter() - self._last_frame)
        if remaining > 0:
            time.sleep(remaining)
        self._last_frame = time.perf_counter()
        if caption:
            self._caption = str(caption)
        pg, screen = self._pygame, self.canvas
        screen.fill(BACKGROUND)

        # Draw concave/convex circuits from the actual collision polygons.
        pg.draw.polygon(screen, ROAD_COLOR, self.track.outer)
        pg.draw.polygon(screen, BACKGROUND, self.track.inner)

        def draw_text(message, position, color="#eeeeee", small=False):
            font = self._small_font if small else self._font
            screen.blit(font.render(str(message), True, color), position)

        # Showing 1500 rays for 500 clones would hide the whole map.
        cars = list(self.cars.values())
        ray_cars = cars if len(cars) <= 10 else cars[:10]
        for car in ray_cars:
            if car.crashed:
                continue
            for offset, color in zip((-45, 0, 45), RAY_COLORS):
                ray_angle = car.angle + offset
                distance = self.track.raycast(car.x, car.y, ray_angle)
                a = math.radians(ray_angle)
                endpoint = (car.x + math.sin(a) * distance,
                            car.y - math.cos(a) * distance)
                pg.draw.line(screen, color, (car.x, car.y), endpoint, 2)
                pg.draw.circle(screen, color,
                               (round(endpoint[0]), round(endpoint[1])), 3)

        for car in cars:
            corners = _car_corners(car.x, car.y, car.angle)
            pg.draw.polygon(screen, car.color if not car.crashed else "#777777", corners)
            pg.draw.polygon(screen, "#202020", corners, 1)
            a = math.radians(car.angle)
            fx, fy, sx, sy = math.sin(a), -math.cos(a), math.cos(a), math.sin(a)
            pg.draw.line(screen, "#173247",
                         (car.x + fx * 6 - sx * 4, car.y + fy * 6 - sy * 4),
                         (car.x + fx * 6 + sx * 4, car.y + fy * 6 + sy * 4), 3)
            if len(cars) <= 35:
                draw_text(car.car_id, (car.x + 17, car.y + 6), "#777777", True)

        alive = sum(not c.crashed for c in cars)
        draw_text(self._caption or "2D DRIVING ENVIRONMENT", (26, 24))
        draw_text("LEVEL {} / 5 - {}".format(self.track.number, self.track.name),
                  (26, 48), "#ffcc66")
        draw_text("CARS: {} / {} ACTIVE".format(alive, len(cars)), (790, 28))
        draw_text("White = road | Black = wall | 0 degrees = up | Esc = close",
                  (290, HEIGHT - 24), small=True)
        pg.display.flip()

    def close_gui(self):
        if self._pygame is not None:
            self._pygame.display.quit()
        self.window = self.canvas = None
        if globals().get("_env") is self:
            globals()["window"] = None


class _WindowHandle:
    """Compatibility with older scripts using Env.window.mainloop()."""
    def __init__(self, environment):
        self.environment = environment

    def mainloop(self):
        while self.environment.window is self:
            self.environment.render()

    def destroy(self):
        self.environment._on_user_close()


# ---------------------------------------------------------------------------
# Public wrapper API — compatible with the user's existing AI program.
# ---------------------------------------------------------------------------
_env = DrivingEnvironment()

def Set_Map(Map_Number): return _env.set_map(Map_Number)
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
    """Slow preview autopilot, only used when the environment file runs alone."""
    track = environment.track
    current_s = track.position_along_track(car.x, car.y)
    tx, ty = track.point_at(current_s + 33.0)
    desired_angle = math.degrees(math.atan2(tx - car.x, -(ty - car.y))) % 360
    environment.send_info(car.car_id, 0.19, desired_angle)


def Demo(map_number=1):
    """Visual preview of the specified map. Press Esc to close."""
    Set_Map(map_number)
    for i in range(10):
        Spawn_Car("Car{}".format(i + 1))
    _env.max_car_time = None
    Start_GUI()
    try:
        while _env.window is not None:
            for car in list(_env.cars.values()):
                if not car.crashed:
                    _demo_control(_env, car)
            Update()
            Render("LIVE PREVIEW - {}".format(_env.track.name))
    except KeyboardInterrupt:
        pass
    finally:
        Close_GUI()
        _env.max_car_time = MAX_CAR_TIME


if __name__ == "__main__":
    Demo(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
