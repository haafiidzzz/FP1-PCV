# Pop Balon

Mini game interaktif berbasis webcam. Gerakkan marker berwarna hijau di depan kamera untuk memecahkan balon dan mendapatkan skor. Hindari bom, karena menyentuh bom akan mengakhiri permainan.

Deteksi marker menggunakan segmentasi warna HSV dari OpenCV, tanpa MediaPipe.

## Fitur

- Melacak marker hijau melalui webcam.
- Menggerakkan dan memecahkan balon dengan marker.
- Menambah skor sebesar 10 untuk setiap balon yang dipecahkan.
- Memunculkan bom yang mengakhiri permainan saat tersentuh.
- Meningkatkan kecepatan balon seiring bertambahnya skor.

## Teknologi

- Python
- OpenCV
- NumPy
- Pygame

## Persyaratan

- Python 3
- Webcam yang dapat diakses oleh komputer
- Windows (game menggunakan backend kamera DirectShow)

## Instalasi dan Menjalankan

1. Clone repository:

   ```bash
   git clone https://github.com/haafiidzzz/FP1-PCV.git
   cd FP1-PCV
   ```

2. (Opsional) Buat dan aktifkan virtual environment:

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Pasang dependency:

   ```bash
   python -m pip install opencv-python numpy pygame
   ```

4. Jalankan game:

   ```bash
   python game_balon.py
   ```

## Cara Bermain

1. Pastikan webcam terhubung dan izinkan akses kamera jika diminta.
2. Klik **Start** pada menu.
3. Arahkan marker berwarna hijau ke balon untuk memecahkannya.
4. Hindari bom.
5. Klik **Main Lagi** untuk bermain kembali setelah game over.

Tekan `Q` untuk keluar. Tombol menu juga menyediakan pilihan **Exit**.

## Pemecahan Masalah

- **Kamera tidak terbuka:** pastikan webcam tidak sedang digunakan aplikasi lain. Game menggunakan indeks kamera `0`; jika webcam yang dipakai berbeda, ubah nilai `cam_index` di `game_balon.py`.
- **Marker tidak terdeteksi:** gunakan marker hijau yang terlihat jelas, pastikan pencahayaan cukup, dan jauhkan warna hijau lain dari area kamera.

## Identitas

- **Nama:** Hafidz Ulum Ramadhani
- **NRP:** 5024241014
