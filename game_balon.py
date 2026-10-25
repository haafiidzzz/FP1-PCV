import cv2
import json
import os
import random
import sys
import numpy as np
import pygame

CONFIG_FILE = "color_config.json"
WIDTH, HEIGHT = 640, 480
FPS = 30
MIN_AREA = 300
SMOOTHING = 0.5
MAX_MISSING = 5

BALLOON_RADIUS = 30
SPAWN_INTERVAL = 1000  # ms
BALLOON_SPEED = 1.5
BALLOON_COLORS = [(255, 80, 80), (80, 150, 255), (80, 220, 120), (255, 200, 60)]


def load_color():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        return np.array(cfg["lower"]), np.array(cfg["upper"])
    print("color_config.json tidak ada, pakai default. Jalankan calibrate_color.py dulu.")
    return np.array([25, 100, 100]), np.array([35, 255, 255])


def detect_marker(frame_bgr, lower, upper):
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > MIN_AREA:
            M = cv2.moments(c)
            return (M["m10"] / M["m00"], M["m01"] / M["m00"])
    return None


class Balloon:
    def __init__(self):
        self.x = random.randint(BALLOON_RADIUS, WIDTH - BALLOON_RADIUS)
        self.y = HEIGHT + BALLOON_RADIUS
        self.color = random.choice(BALLOON_COLORS)
        self.alive = True

    def update(self):
        self.y -= BALLOON_SPEED
        if self.y < -BALLOON_RADIUS:
            self.alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALLOON_RADIUS)

    def is_hit(self, px, py):
        dist = ((self.x - px) ** 2 + (self.y - py) ** 2) ** 0.5
        return dist < BALLOON_RADIUS + 10


def frame_to_surface(frame_bgr):
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    frame_rgb = np.rot90(frame_rgb)
    surface = pygame.surfarray.make_surface(frame_rgb)
    surface = pygame.transform.flip(surface, False, True)
    return surface


def main():
    lower, upper = load_color()
    cap = cv2.VideoCapture(0)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Game - Pop Balon pakai Deteksi Warna")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    balloons = []
    score = 0
    last_spawn = pygame.time.get_ticks()

    smooth = None
    missing = 0
    blade_trail = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))

        pos = detect_marker(frame, lower, upper)
        if pos is not None:
            missing = 0
            smooth = pos if smooth is None else (
                SMOOTHING * smooth[0] + (1 - SMOOTHING) * pos[0],
                SMOOTHING * smooth[1] + (1 - SMOOTHING) * pos[1],
            )
        else:
            missing += 1
            if missing > MAX_MISSING:
                smooth = None

        now = pygame.time.get_ticks()
        if now - last_spawn > SPAWN_INTERVAL:
            balloons.append(Balloon())
            last_spawn = now

        for b in balloons:
            b.update()
            if smooth is not None and b.alive and b.is_hit(*smooth):
                b.alive = False
                score += 10

        balloons = [b for b in balloons if b.alive]

        screen.blit(frame_to_surface(frame), (0, 0))

        for b in balloons:
            b.draw(screen)

        if smooth is not None:
            pos_int = (int(smooth[0]), int(smooth[1]))
            blade_trail.append(pos_int)
            if len(blade_trail) > 10:
                blade_trail.pop(0)
            pygame.draw.circle(screen, (255, 255, 255), pos_int, 10, 2)

        if len(blade_trail) > 1:
            pygame.draw.lines(screen, (255, 255, 255), False, blade_trail, 3)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    cap.release()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()