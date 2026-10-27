import cv2
import numpy as np
import pygame
import random
import sys
from pathlib import Path

lower_merah_1 = np.array([0, 100, 100])
upper_merah_1 = np.array([10, 255, 255])
lower_merah_2 = np.array([170, 100, 100])
upper_merah_2 = np.array([179, 255, 255])

cam_index = 0

lebar = 800
tinggi = 600
fps = 30

radius_balon = 30
speed_balon = 1.5

radius_bom = 28
peluang_bom = 0.25

pygame.init()
layar = pygame.display.set_mode((lebar, tinggi))
pygame.display.set_caption("Pop Balon - Deteksi Warna")
clock = pygame.time.Clock()
font_judul = pygame.font.SysFont(None, 64)
font = pygame.font.SysFont(None, 40)
font_kecil = pygame.font.SysFont(None, 26)

folder_assets = Path(__file__).resolve().parent / "assets"
sprite_balon = pygame.transform.smoothscale(
    pygame.image.load(str(folder_assets / "balloon.png")).convert_alpha(),
    (64, 80),
)
sprite_bom = pygame.transform.smoothscale(
    pygame.image.load(str(folder_assets / "bomb.png")).convert_alpha(),
    (60, 60),
)

cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("kamera ga kebuka, cek cam_index nya")
    sys.exit()

tombol_start = pygame.Rect(lebar / 2 - 100, 250, 200, 60)
tombol_kalibrasi = pygame.Rect(lebar / 2 - 100, 330, 200, 60)
tombol_exit_menu = pygame.Rect(lebar / 2 - 100, 410, 200, 60)
tombol_main_lagi = pygame.Rect(lebar / 2 - 110, 325, 220, 60)
tombol_exit_gameover = pygame.Rect(lebar / 2 - 110, 405, 220, 60)


def kalibrasi_marker(lower_awal_1, upper_awal_1, lower_awal_2, upper_awal_2):
    nama_window = "Kalibrasi Marker"
    nilai_awal = [
        int(lower_awal_1[0]), int(upper_awal_1[0]),
        int(lower_awal_2[0]), int(upper_awal_2[0]),
        int(lower_awal_1[1]), int(lower_awal_1[2]),
        int(upper_awal_1[1]), int(upper_awal_1[2]),
    ]
    trackbar = ["H1 min", "H1 max", "H2 min", "H2 max", "S min", "V min", "S max", "V max"]

    cv2.namedWindow(nama_window)
    for nama, nilai in zip(trackbar, nilai_awal):
        batas = 179 if nama.startswith("H") else 255
        cv2.createTrackbar(nama, nama_window, nilai, batas, lambda _: None)

    hasil = None
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("gagal baca frame saat kalibrasi")
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (lebar, tinggi))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            nilai = [cv2.getTrackbarPos(nama, nama_window) for nama in trackbar]
            h1_min, h1_max = sorted((nilai[0], nilai[1]))
            h2_min, h2_max = sorted((nilai[2], nilai[3]))
            s_min, s_max = sorted((nilai[4], nilai[6]))
            v_min, v_max = sorted((nilai[5], nilai[7]))
            lower_1 = np.array([h1_min, s_min, v_min])
            upper_1 = np.array([h1_max, s_max, v_max])
            lower_2 = np.array([h2_min, s_min, v_min])
            upper_2 = np.array([h2_max, s_max, v_max])
            mask_1 = cv2.inRange(hsv, lower_1, upper_1)
            mask_2 = cv2.inRange(hsv, lower_2, upper_2)
            mask = cv2.bitwise_or(mask_1, mask_2)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            preview = frame.copy()
            cv2.putText(preview, "S: simpan  |  ESC: batal", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            tampilan = np.hstack((preview, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)))
            cv2.imshow(nama_window, tampilan)

            tombol = cv2.waitKey(1) & 0xFF
            if tombol == ord("s"):
                hasil = (lower_1, upper_1, lower_2, upper_2)
                break
            if tombol == 27:
                break
    finally:
        cv2.destroyWindow(nama_window)

    return hasil


def gambar_tombol(rect, teks):
    pygame.draw.rect(layar, (60, 60, 70), rect, border_radius=8)
    pygame.draw.rect(layar, (255, 255, 255), rect, 2, border_radius=8)
    label = font.render(teks, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    layar.blit(label, label_rect)


def buat_latar_game():
    latar = pygame.Surface((lebar, tinggi))
    warna_atas = (22, 42, 92)
    warna_bawah = (89, 169, 205)

    for y in range(tinggi):
        rasio = y / tinggi
        warna = tuple(
            int(atas + (bawah - atas) * rasio)
            for atas, bawah in zip(warna_atas, warna_bawah)
        )
        pygame.draw.line(latar, warna, (0, y), (lebar, y))

    pygame.draw.circle(latar, (255, 224, 135), (lebar - 85, 85), 38)

    for x, y, skala in [(120, 155, 1), (405, 95, 0.75), (645, 220, 0.9)]:
        warna_awam = (190, 224, 235)
        pygame.draw.ellipse(latar, warna_awam, (x, y + 12 * skala, 100 * skala, 28 * skala))
        pygame.draw.circle(latar, warna_awam, (int(x + 25 * skala), int(y + 15 * skala)), int(17 * skala))
        pygame.draw.circle(latar, warna_awam, (int(x + 50 * skala), int(y + 5 * skala)), int(23 * skala))
        pygame.draw.circle(latar, warna_awam, (int(x + 75 * skala), int(y + 16 * skala)), int(16 * skala))

    pygame.draw.ellipse(latar, (64, 151, 145), (-130, tinggi - 85, 480, 150))
    pygame.draw.ellipse(latar, (51, 132, 130), (220, tinggi - 65, 570, 150))
    return latar


latar_game = buat_latar_game()


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
        layar.blit(judul, judul.get_rect(center=(lebar / 2, 150)))

        gambar_tombol(tombol_start, "Start")
        gambar_tombol(tombol_kalibrasi, "Kalibrasi")
        gambar_tombol(tombol_exit_menu, "Exit")

        if klik:
            if tombol_start.collidepoint(mouse_pos):
                reset_game()
                state = "main"
            elif tombol_kalibrasi.collidepoint(mouse_pos):
                hasil_kalibrasi = kalibrasi_marker(
                    lower_merah_1, upper_merah_1, lower_merah_2, upper_merah_2
                )
                if hasil_kalibrasi is not None:
                    lower_merah_1, upper_merah_1, lower_merah_2, upper_merah_2 = hasil_kalibrasi
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

        mask_1 = cv2.inRange(hsv, lower_merah_1, upper_merah_1)
        mask_2 = cv2.inRange(hsv, lower_merah_2, upper_merah_2)
        mask = cv2.bitwise_or(mask_1, mask_2)
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
                list_balon.append([bx, by])
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

        layar.blit(latar_game, (0, 0))

        for b in list_balon:
            rect_balon = sprite_balon.get_rect(center=(int(b[0]), int(b[1])))
            layar.blit(sprite_balon, rect_balon)

        for bm in list_bom:
            rect_bom = sprite_bom.get_rect(center=(int(bm[0]), int(bm[1])))
            layar.blit(sprite_bom, rect_bom)

        if pos_marker is not None:
            titik = (int(pos_marker[0]), int(pos_marker[1]))
            jejak.append(titik)
            if len(jejak) > 10:
                jejak.pop(0)
            pygame.draw.circle(layar, (255, 0, 0), titik, 10, 2)
        else:
            teks_warn = font_kecil.render("marker gak kedeteksi", True, (255, 80, 80))
            layar.blit(teks_warn, (10, tinggi - 30))

        if len(jejak) > 1:
            pygame.draw.lines(layar, (255, 0, 0), False, jejak, 3)

        teks_score = font.render("Score: " + str(score), True, (255, 255, 255))
        layar.blit(teks_score, (10, 10))

    elif state == "gameover":
        layar.fill((20, 20, 30))
        judul = font_judul.render("Game Over", True, (255, 80, 80))
        layar.blit(judul, judul.get_rect(center=(lebar / 2, 190)))

        teks_score = font.render("Score kamu: " + str(score), True, (255, 255, 255))
        layar.blit(teks_score, teks_score.get_rect(center=(lebar / 2, 270)))

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