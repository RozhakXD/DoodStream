# Dood-NG: Downloader & Streamer untuk DoodStream

![Dood-NG](https://github.com/user-attachments/assets/6759b4e2-d5ff-4fe9-b482-57782589e8c5)

**Dood-NG** adalah sebuah aplikasi web full-stack yang dirancang untuk memberikan pengalaman terbaik dalam menonton dan mengunduh video dari DoodStream. Ucapkan selamat tinggal pada iklan yang mengganggu, pop-up yang tidak jelas, dan potensi malware. Fokus kami adalah menyediakan antarmuka yang bersih, cepat, dan fungsional.

**Tampilan Antarmuka (UI/UX)**
Kami merancang antarmuka yang modern, responsif, dan intuitif dengan tema gelap yang nyaman di mata.

**Tampilan Desktop:**
![Desktop](https://github.com/user-attachments/assets/c2d5cb3a-06f1-4a8d-b4ae-0a3ea83c922e)

## 📖 Tentang Proyek

Proyek ini lahir dari kebutuhan akan sebuah alat yang efisien dan aman untuk mengakses konten dari DoodStream. Situs aslinya sering kali dipenuhi dengan iklan agresif yang merusak pengalaman menonton dan menimbulkan risiko keamanan. Dood-NG hadir sebagai solusi, dengan memprioritaskan:

* Keamanan Pengguna: Tidak ada iklan, tidak ada pelacak, tidak ada skrip berbahaya.
* Pengalaman Pengguna (UX): Antarmuka yang bersih, cepat, dan mudah digunakan di semua perangkat.
* Fungsionalitas: Tidak hanya mengunduh, tetapi juga menyediakan fitur streaming langsung.

Proyek ini bersifat open source dengan harapan dapat dikembangkan lebih lanjut oleh komunitas dan bermanfaat bagi banyak orang.

## ✨ Fitur Utama

* **Streaming Langsung:** Tonton video secara langsung di browser tanpa perlu mengunduhnya terlebih dahulu.
* **Unduhan Video Tunggal:** Tempel URL video (`/e/` atau `/d/`) untuk memproses dan mengunduhnya.
* **Dukungan Unduhan Folder:** Masukkan URL folder (`/f/`) untuk menampilkan semua video di dalamnya, lalu pilih video mana yang ingin Anda proses.
* **Pembersihan Otomatis:** File video yang diproses di server akan dihapus secara otomatis setelah 1 jam untuk menghemat ruang penyimpanan.
* **Backend Asinkron:** Dibangun dengan Django dan Celery untuk menangani proses unduhan di latar belakang tanpa memblokir antarmuka pengguna.
* **Antarmuka Responsif:** Desain yang optimal untuk perangkat desktop, tablet, maupun mobile.

## 🛠️ Teknologi yang Digunakan

* Backend:
  * [Python](https://www.python.org/)
  * [Django](https://www.djangoproject.com/) & [Django REST Framework](https://www.django-rest-framework.org/)
  * [Celery](https://docs.celeryq.dev/en/stable/) (untuk tugas latar belakang)
  * [Redis](https://redis.io/) (sebagai message broker untuk Celery)
  * [Aiohttp](https://docs.aiohttp.org/en/stable/) (untuk permintaan HTTP asinkron)
* Frontend:
  * HTML5
  * [Tailwind CSS](https://tailwindcss.com/)
  * JavaScript (vanilla)

## 🚀 Instalasi & Konfigurasi

Untuk menjalankan proyek ini di lingkungan lokal Anda, ikuti langkah-langkah berikut.

#### 1. Prasyarat

Pastikan Anda telah menginstal perangkat lunak berikut:

* **Python** (versi 3.10 atau lebih tinggi)
* **Redis Server**. Anda bisa mengunduhnya dari [situs resmi Redis](https://redis.io/download).

#### 2. Kloning Repositori

```bash
git clone https://github.com/RozhakXD/Dood-NG.git
cd Dood-NG
```

#### 3. Siapkan Lingkungan Virtual & Dependensi

Sangat disarankan untuk menggunakan lingkungan virtual (venv) untuk mengisolasi dependensi proyek.

```bash
# Buat dan aktifkan venv
python -m venv venv
source venv/bin/activate  # Di Windows, gunakan: venv\Scripts\activate

# Instal semua dependensi yang dibutuhkan
pip install -r requirements.txt
```

#### 4. Migrasi Database

Jalankan migrasi awal untuk menyiapkan database Django.

```bash
python manage.py migrate
```

#### 5. Menjalankan Server

Anda perlu menjalankan **tiga proses server** secara terpisah, masing-masing di terminalnya sendiri.

* **Terminal 1: Jalankan Redis Server**
  
  ```bash
  redis-server
  ```
* **Terminal 2: Jalankan Celery Worker** (Pastikan venv Anda aktif di terminal ini)
  
  ```bash
  celery -A dood_downloader worker -l info
  ```
* **Terminal 3: Jalankan Celery Beat (Scheduler)** (Pastikan venv Anda aktif di terminal ini)
  
  ```bash
  celery -A dood_downloader beat -l info
  ```
* **Terminal 4: Jalankan Server Django** (Pastikan venv Anda aktif di terminal ini)
  
  ```bash
  python manage.py runserver
  ```

Setelah semua server berjalan, aplikasi akan dapat diakses di `http://127.0.0.1:8000/`.

## ⚙️ Cara Penggunaan

1. Buka browser dan akses `http://127.0.0.1:8000/`.
2. Masukkan URL video atau folder DoodStream ke kolom input.
3. Klik tombol "Proses" untuk memulai.
4. Jika URL video, tunggu sampai pemutar muncul; jika folder, klik "Proses" pada video yang diinginkan lalu tunggu hingga pemutar muncul.

## 🤝 Kontribusi

Kami sangat terbuka untuk kontribusi! Jika Anda memiliki ide untuk fitur baru, perbaikan bug, atau peningkatan lainnya, silakan:

1. Fork repositori ini.
2. Buat branch baru untuk fitur Anda (`git checkout -b fitur/FiturKeren`).
3. Lakukan perubahan dan commit (`git commit -m 'Menambahkan FiturKeren'`).
4. Push ke branch Anda (`git push origin fitur/FiturKeren`).
5. Buka sebuah _Pull Request_.

## ☕ Dukung Pengembangan

Jika Anda ingin mendukung pengembangan proyek ini, Anda dapat memberikan donasi melalui:

- [Trakteer](https://trakteer.id/rozhak_official/tip?)
- [PayPal](https://paypal.me/rozhak9)

Setiap dukungan sangat berarti dan membantu proyek ini terus berkembang!

## 📜 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.