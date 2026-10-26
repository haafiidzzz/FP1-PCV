import cv2
import numpy as np
import pygame
import random
import sys

lower_hijau = np.array([40, 100, 100])
upper_hijau = np.array([85, 255, 255])

cam_index = 0

lebar = 640
tinggi = 480
fps = 30

radius_balon = 30
speed_balon = 1.5
warna_balon = [(255, 80, 80), (80, 150, 255), (80, 220, 120), (255, 200, 60)]

radius_bom = 28
peluang_bom = 0.25

pygame.init()
layar = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption("Pop Balon - Deteksi Warna")
clock = pygame.time.Clock()
font_judul = pygame.font.SysFont(None, 56)
font = pygame.font.SysFont(None, 36)
font_kecil = pygame.font.SysFont(None, 22)

cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("kamera ga kebuka, cek cam_index nya")
    sys.exit()

tombol_start = pygame.Rect(lebar / 2 - 80, 220, 160, 50)
tombol_exit_menu = pygame.Rect(lebar / 2 - 80, 290, 160, 50)
tombol_main_lagi = pygame.Rect(lebar / 2 - 90, 260, 180, 50)
tombol_exit_gameover = pygame.Rect(lebar / 2 - 90, 330, 180, 50)


def gambar_tombol(rect, teks):
    pygame.draw.rect(layar, (60, 60, 70), rect, border_radius=8)
    pygame.draw.rect(layar, (255, 255, 255), rect, 2, border_radius=8)
    label = font.render(teks, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    layar.blit(label, label_rect)


def reset_game():
    global list_balon, list_bom, score, waktu_spawn_terakhir, pos_marker, frame_hilang, jejak, speed_sekarang
    list_balon = []
    list_bom = []
    score = 0
    waktu_spawn_terakhir = pygame.time.get_ticks()
    pos_marker = None
    frame_hilang = 0
    jejak = []
    speed_sekarang = speed_balon


reset_game()

state = "menu"
main_loop = True

while main_loop:
    mouse_pos = pygame.mouse.get_pos()
    klik = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_loop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                main_loop = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            klik = True

    if state == "menu":
        layar.fill((20, 20, 30))
        judul = font_judul.render("Pop Balon", True, (255, 255, 255))
        layar.blit(judul, judul.get_rect(center=(lebar / 2, 120)))

        gambar_tombol(tombol_start, "Start")
        gambar_tombol(tombol_exit_menu, "Exit")

        if klik:
            if tombol_start.collidepoint(mouse_pos):
                reset_game()
                state = "main"
            elif tombol_exit_menu.collidepoint(mouse_pos):
                main_loop = False

    elif state == "main":
        ret, frame = cap.read()
        if not ret:
            print("gagal baca frame")
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (lebar, tinggi))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_hijau, upper_hijau)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        kontur, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        marker_ketemu = False
        if len(kontur) > 0:
            c = max(kontur, key=cv2.contourArea)
            if cv2.contourArea(c) > 300:
                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                if pos_marker is None:
                    pos_marker = (cx, cy)
                else:
                    sx = pos_marker[0] * 0.5 + cx * 0.5
                    sy = pos_marker[1] * 0.5 + cy * 0.5
                    pos_marker = (sx, sy)

                marker_ketemu = True
                frame_hilang = 0

        if not marker_ketemu:
            frame_hilang += 1
            if frame_hilang > 5:
                pos_marker = None

        sekarang = pygame.time.get_ticks()
        if sekarang - waktu_spawn_terakhir > 1000:
            bx = random.randint(radius_balon, lebar - radius_balon)
            by = tinggi + radius_balon
            if random.random() < peluang_bom:
                list_bom.append([bx, by])
            else:
                warna = random.choice(warna_balon)
                list_balon.append([bx, by, warna])
            waktu_spawn_terakhir = sekarang

        speed_sekarang = speed_balon + score * 0.02
        if speed_sekarang > speed_balon * 4:
            speed_sekarang = speed_balon * 4

        balon_baru = []
        for b in list_balon:
            b[1] -= speed_sekarang

            kena = False
            if pos_marker is not None:
                jarak = ((b[0] - pos_marker[0]) ** 2 + (b[1] - pos_marker[1]) ** 2) ** 0.5
                if jarak < radius_balon + 10:
                    kena = True
                    score += 10

            if b[1] > -radius_balon and not kena:
                balon_baru.append(b)
        list_balon = balon_baru

        bom_baru = []
        kena_bom = False
        for bm in list_bom:
            bm[1] -= speed_sekarang

            if pos_marker is not None:
                jarak = ((bm[0] - pos_marker[0]) ** 2 + (bm[1] - pos_marker[1]) ** 2) ** 0.5
                if jarak < radius_bom + 10:
                    kena_bom = True

            if bm[1] > -radius_bom and not kena_bom:
                bom_baru.append(bm)
        list_bom = bom_baru

        if kena_bom:
            state = "gameover"

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = np.transpose(frame_rgb, (1, 0, 2))
        surface_cam = pygame.surfarray.make_surface(frame_rgb)
        layar.blit(surface_cam, (0, 0))

        for b in list_balon:
            pygame.draw.circle(layar, b[2], (int(b[0]), int(b[1])), radius_balon)

        for bm in list_bom:
            pygame.draw.circle(layar, (30, 30, 30), (int(bm[0]), int(bm[1])), radius_bom)
            pygame.draw.circle(layar, (255, 255, 255), (int(bm[0]), int(bm[1])), radius_bom, 2)
            pygame.draw.line(layar, (255, 150, 0), (bm[0], bm[1] - radius_bom),
                              (bm[0] + 8, bm[1] - radius_bom - 10), 3)

        if pos_marker is not None:
            titik = (int(pos_marker[0]), int(pos_marker[1]))
            jejak.append(titik)
            if len(jejak) > 10:
                jejak.pop(0)
            pygame.draw.circle(layar, (255, 255, 255), titik, 10, 2)
        else:
            teks_warn = font_kecil.render("marker gak kedeteksi", True, (255, 80, 80))
            layar.blit(teks_warn, (10, tinggi - 30))

        if len(jejak) > 1:
            pygame.draw.lines(layar, (255, 255, 255), False, jejak, 3)

        teks_score = font.render("Score: " + str(score), True, (255, 255, 255))
        layar.blit(teks_score, (10, 10))

    elif state == "gameover":
        layar.fill((20, 20, 30))
        judul = font_judul.render("Game Over", True, (255, 80, 80))
        layar.blit(judul, judul.get_rect(center=(lebar / 2, 150)))

        teks_score = font.render("Score kamu: " + str(score), True, (255, 255, 255))
        layar.blit(teks_score, teks_score.get_rect(center=(lebar / 2, 210)))

        gambar_tombol(tombol_main_lagi, "Main Lagi")
        gambar_tombol(tombol_exit_gameover, "Exit")

        if klik:
            if tombol_main_lagi.collidepoint(mouse_pos):
                reset_game()
                state = "main"
            elif tombol_exit_gameover.collidepoint(mouse_pos):
                main_loop = False

    pygame.display.flip()
    clock.tick(fps)

cap.release()
pygame.quit()