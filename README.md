# Pop Balon

Mini game interaktif berbasis webcam. Gerakkan marker berwarna merah di depan kamera untuk memecahkan balon dan mendapatkan skor. Hindari bom, karena menyentuh bom akan mengakhiri permainan.

Deteksi marker menggunakan segmentasi warna HSV dari OpenCV.

## Fitur

- Jendela game berukuran 800 × 600.
- Melacak marker merah melalui webcam.
- Menggunakan latar grafis game, sehingga tampilan webcam tidak ditampilkan.
- Menampilkan sprite balon dan bom.
- Menyesuaikan rentang warna marker lewat kalibrasi HSV.
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

1. Pastikan webcam terhubung dan izinkan akses kamera jika diminta. Kamera hanya digunakan untuk melacak marker; gambar kamera tidak ditampilkan sebagai latar game.
2. Jika marker belum terdeteksi dengan baik, klik **Kalibrasi** pada menu.
3. Sesuaikan slider HSV (H1 dan H2 untuk dua rentang merah) sambil melihat pratinjau; area putih pada tampilan mask adalah warna yang akan terdeteksi.
4. Tekan `S` untuk menerapkan hasil kalibrasi, atau `Esc` untuk membatalkan.
5. Klik **Start** dan arahkan marker berwarna merah ke balon untuk memecahkannya.
6. Hindari bom.
7. Klik **Main Lagi** untuk bermain kembali setelah game over.

Tekan `Q` untuk keluar. Tombol menu juga menyediakan pilihan **Exit**.

## Atribusi Asset

Sprite balon (U+1F388) dan bom (U+1F4A3) berasal dari [Twemoji](https://github.com/jdecked/twemoji/tree/main/assets/72x72) dan digunakan tanpa perubahan. Keduanya berlisensi [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); salinan lisensi disertakan di [assets/LICENSE-GRAPHICS.txt](assets/LICENSE-GRAPHICS.txt).

## Identitas

- **Nama:** Hafidz Ulum Ramadhani
- **NRP:** 5024241014
