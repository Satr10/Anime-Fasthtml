# Anime Fasthtml

Proyek ini adalah aplikasi web yang menyediakan informasi tentang anime yang sedang tren, anime musim saat ini, dan film anime. Aplikasi ini juga memungkinkan pengguna untuk mencari anime, melihat informasi detail tentang setiap anime, dan mengunduh episode.

## Fitur

- **Halaman Utama**: Menampilkan anime yang sedang tren, anime musim saat ini, dan film musim ini.
- **Detail Anime**: Informasi detail tentang setiap anime, termasuk judul, rating, episode, musim, genre, dan lainnya.
- **Pencarian**: Mencari anime berdasarkan judul dan melihat hasil pencarian.
- **Unduh**: Menyediakan tautan unduhan untuk episode anime.
- **Navigasi**: Navigasi sederhana dengan tautan ke halaman Beranda, Tentang, Kontak, dan Trending.

## Technologies Used

- **Python**: The primary programming language used for the backend.
- **FastHTML**: A lightweight and fast web framework for building dynamic web pages in Python.
- **Tailwind CSS**: A utility-first CSS framework used for styling the web pages.
- **Theme-Change**: A JavaScript library used for theme switching functionality.
- **[Otakudesu-Scraper](https://github.com/rzkfyn/otakudesu-scraper)**: An UNOFFICIAL rest API for otakudesu. Otakudesu is a web that provides anime with Indonesian subtitle.  

## Instalasi

### Prasyarat

- Python 3.8+
- Pip

### Langkah-Langkah

1. **Kloning repositori**:

   ```bash
   git clone https://github.com/Satr10/Anime-Fasthtml
   cd anime-dashboard
   ```

2. **Buat dan aktifkan virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Di Windows gunakan `venv\Scripts\activate`
   ```

3. **Install dependensi**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi**:

   ```bash
   python main.py
   ```

5. Buka browser Anda dan kunjungi `http://127.0.0.1:5001/` untuk melihat aplikasi.

## Struktur File

- **main.py**: File aplikasi utama yang berisi rute dan logika untuk merender halaman.
- **fasthtml/common.py**: Berisi fungsi dan utilitas umum.
- **fasthtml/components.py**: Berisi komponen seperti `NotStr`.
- **utils.py**: Fungsi utilitas untuk mengambil data anime.
- **get_download.py**: Fungsi untuk mencari dan mengambil tautan unduhan untuk episode anime.
- **components.py**: Komponen khusus yang digunakan dalam proyek.

## Cara Kerja

- Aplikasi ini menggunakan `fast_app` dari `fasthtml` untuk mengatur aplikasi web.
- **Rute**: Aplikasi ini mendefinisikan beberapa rute seperti `/`, `/anime/{id}`, `/trending/{page}`, `/this-season/{page}`, `/season-movies/{page}`, `/search/{query}/{page}`, dan lainnya.
- **Komponen**: Aplikasi ini menggunakan komponen khusus seperti `create_navbar`, `kumpulan_kartu`, `pemisah`, dan `footer` untuk membangun halaman.

## Tautan Navigasi

- **Beranda**: `/` - Halaman utama dengan anime yang sedang tren dan anime musim saat ini.
- **Trending**: `/trending/1` - Daftar anime yang sedang tren dengan paginasi.
- **This Season**: `/this-season/1` - Daftar anime yang tayang musim ini dengan paginasi.
- **Season Movies**: `/season-movies/1` - Daftar film yang tayang musim ini dengan paginasi.
- **Pencarian**: `/search/{query}/1` - Hasil pencarian untuk query tertentu.
- **Tentang**: `/about` - Informasi tentang aplikasi.
- **Kontak**: `/contact` - Informasi kontak.

## TODO

- ~~**Bug Fix**: Perbaiki masalah saat judul anime terlalu panjang pada query pencarian yang menyebabkan error.~~
- ~~**Mempercepat Kode**: Sekarang kecepatan fetch nya lambat sekali.~~
- **UI Improvements**: Tingkatkan antarmuka pengguna agar lebih responsif dan menarik.
- **Streaming Functionality**: Tambahkan fitur untuk streaming anime secara langsung dari aplikasi.
- **Enhance Search Function**: Tambahkan fitur pencarian lanjutan dengan filter berdasarkan genre, tahun, dan studio.
- **User Authentication**: Tambahkan fitur autentikasi pengguna untuk akses ke fitur-fitur khusus seperti daftar tontonan atau riwayat tontonan.
- **Anime Recommendations**: Implementasi sistem rekomendasi anime berdasarkan preferensi pengguna dan riwayat tontonan.

## Kontribusi

Jangan ragu untuk mengirimkan isu atau pull request jika Anda menemukan bug atau ingin berkontribusi pada proyek ini.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk informasi lebih lanjut.
