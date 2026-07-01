# Laporan Praktikum Web Scraping

Repositori ini berisi kumpulan program web scraping untuk memenuhi tugas mata kuliah Pengantar Data Mining A. Program dirancang menggunakan Python, BeautifulSoup4, dan Pandas dengan mengutamakan efisiensi koneksi, ketahanan error, serta struktur data yang terorganisasi.

---

## Struktur Proyek

```text
Web Scrapping/
│
├── scrapping-web/
│   ├── latihan_mandiri.py     # Program scraping quotes.toscrape.com
│   └── mini_project.py        # Program scraping scrapethissite.com
│
├── output/
│   ├── latihan-mandiri/       # Output data dari latihan_mandiri.py
│   │   ├── quotes.csv         # File data quote (jika openpyxl absen)
│   │   └── kategori.csv       # File data kategori (jika openpyxl absen)
│   │
│   └── mini-project/          # Output data dari mini_project.py
│       ├── countries.csv      # Data negara
│       ├── hockey_teams.csv   # Data tim hoki
│       └── oscar_films.csv    # Data pemenang Oscar
│
├── web-scrapping.txt          # Panduan modul praktikum dari dosen
└── README.md                  # Dokumentasi laporan proyek
```

---

## Kebutuhan Sistem & Instalasi

Program ini berjalan di lingkungan Python 3.x dan memerlukan pustaka tambahan untuk request HTTP, parsing dokumen HTML, serta pengolahan data tabular.

### 1. Instalasi Pustaka Utama
Jalankan perintah berikut pada terminal Anda untuk memasang pustaka yang diperlukan:

```bash
pip install requests beautifulsoup4 pandas
```

### 2. Instalasi Opsional (Ekspor Excel)
Untuk mendukung penyimpanan format Excel (.xlsx) pada latihan mandiri, Anda dapat menambahkan pustaka openpyxl:

```bash
pip install openpyxl
```
*Catatan: Jika openpyxl tidak terinstal, program latihan mandiri akan mengalihkan output ke format CSV secara otomatis tanpa memicu kegagalan.*

---

## Cara Menjalankan Program

Pastikan Anda berada di direktori utama proyek (`Web Scrapping`) sebelum mengeksekusi perintah di bawah ini.

### 1. Menjalankan Latihan Mandiri
Program ini melakukan scraping pada situs `quotes.toscrape.com` untuk mengambil data kutipan dari 3 halaman pertama serta kategori unik yang tersedia.

```bash
python scrapping-web/latihan_mandiri.py
```

### 2. Menjalankan Mini Project
Program ini melakukan scraping tiga skenario halaman pada `scrapethissite.com` (data statis negara, data paginasi tim hoki, dan data AJAX JSON pemenang film Oscar).

```bash
python scrapping-web/mini_project.py
```

---

## Rincian Teknis Program

Setiap program mengimplementasikan arsitektur berorientasi objek (OOP) dan didesain menggunakan kaidah-kaidah pemrograman profesional:

### 1. Latihan Mandiri (latihan_mandiri.py)
* **Target Web**: https://quotes.toscrape.com
* **Data yang Diambil**:
  - Quote teks, nama penulis, kategori tag, serta nomor halaman.
  - Daftar kategori unik (diambil secara dinamis dari kombinasi sidebar "Top Ten tags" dan seluruh kutipan yang berhasil ter-scrape).
* **Fitur Utama**:
  - `QuotesScraper` class untuk manajemen modul.
  - Auto-fallback format ekspor: Menyimpan file dalam bentuk Excel `.xlsx` multi-sheet (Sheet 1: Quotes, Sheet 2: Categories) jika pustaka `openpyxl` tersedia, dan otomatis beralih ke dua file CSV terpisah jika pustaka tersebut tidak ditemukan.

### 2. Mini Project (mini_project.py)
* **Target Web**: https://www.scrapethissite.com/pages/
* **Skema Scraping**:
  1. **Countries of the World (Simple Example)**: Mengekstrak nama negara, ibu kota, jumlah populasi, dan luas wilayah.
  2. **Hockey Teams (Forms & Pagination)**: Melakukan iterasi dinamis pada formulir tabel tim hoki dari halaman 1 hingga selesai (atau batas maksimum 30 halaman) untuk mendata nama tim, tahun, rekor menang/kalah, selisih gol, dan persentase kemenangan.
  3. **Oscar Winning Films (AJAX & Javascript)**: Melakukan request langsung pada endpoint API AJAX JSON internal website untuk mengunduh film pemenang Oscar dari tahun 2010 hingga 2015.
* **Fitur Utama**:
  - `ScrapeThisSiteScraper` class.
  - Memisahkan fungsi pengambilan data HTML (`_get_soup`) dan JSON (`_get_json`).

---

## Fitur Kinerja dan Ketahanan Jaringan

Kedua skrip di atas dilengkapi dengan optimasi tingkat lanjut untuk menjamin efisiensi dan menghindari blokir IP:

* **Connection Pooling**: Menggunakan `requests.Session()` untuk mempertahankan koneksi TCP yang sama sepanjang aktivitas scraping, mengurangi latensi waktu jabat tangan (handshake) jaringan.
* **Mekanisme Retry Otomatis**: Dilengkapi dengan adapter `urllib3.util.Retry` yang akan mengulangi request secara otomatis dengan peningkatan jeda waktu (*exponential backoff*) jika server merespons dengan kode kesalahan status sementara (500, 502, 503, 504).
* **Defensive Parsing**: Penempatan metode pencari CSS selector dibungkus oleh fungsi penanganan kesalahan. Jika elemen web target hilang, program mengembalikan string kosong `""` tanpa menghentikan paksa aplikasi (*crash-free*).
* **Etika Scraping**: Menambahkan parameter jeda waktu (*delay*) selama 2.0 detik pada setiap request HTTP untuk menghormati kapasitas server dan mencegah pemblokiran alamat IP.
* **Logging System**: Menggunakan pustaka standard `logging` Python untuk mencetak kronologi dan status proses scraping pada terminal secara sistematis.
