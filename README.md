# Tugas Praktikum Web Scraping - Pengantar Data Mining

Repositori ini dibuat untuk memenuhi tugas praktikum Web Scraping pada mata kuliah Pengantar Data Mining (Kelas A). Program ini ditulis menggunakan Python dengan memanfaatkan library BeautifulSoup4 untuk parsing HTML, requests untuk HTTP request, dan pandas untuk pengolahan serta penyimpanan data.

---

## Struktur Folder

```text
Web Scrapping/
├── scrapping-web/
│   ├── latihan_mandiri.py     # Script scraping untuk quotes.toscrape.com
│   └── mini_project.py        # Script scraping untuk scrapethissite.com
├── output/
│   ├── latihan-mandiri/       # Folder hasil output latihan mandiri
│   │   ├── quotes.csv         # Hasil quote (jika openpyxl tidak ada)
│   │   └── kategori.csv       # Kategori tag unik (jika openpyxl tidak ada)
│   └── mini-project/          # Folder hasil output mini project
│       ├── countries.csv      # Data negara
│       ├── hockey_teams.csv   # Data tim hoki (seluruh halaman)
│       └── oscar_films.csv    # Data film pemenang Oscar (AJAX)
├── web-scrapping.md           # Modul praktikum format Markdown
├── .gitignore                 # Konfigurasi ignore file Git
└── README.md                  # Dokumentasi tugas
```

---

## Kebutuhan Library

Sebelum menjalankan program, pastikan modul-modul berikut sudah terinstal di lingkungan Python Anda:

```bash
pip install requests beautifulsoup4 pandas
```

Jika ingin hasil latihan mandiri langsung disimpan dalam format Excel (.xlsx), instal juga library berikut:

```bash
pip install openpyxl
```

---

## Cara Menjalankan Program

Jalankan perintah berikut melalui terminal atau command prompt di direktori utama proyek:

1. **Menjalankan Latihan Mandiri**:
   ```bash
   python scrapping-web/latihan_mandiri.py
   ```

2. **Menjalankan Mini Project**:
   ```bash
   python scrapping-web/mini_project.py
   ```

---

## Penjelasan Singkat Implementasi Program

Kedua script telah dirapikan agar lebih modular dengan pendekatan Class-based di Python untuk mempermudah pembacaan kode dan debugging.

### 1. Latihan Mandiri (latihan_mandiri.py)
* **Sumber Data**: https://quotes.toscrape.com
* **Alur Kerja**:
  - Mengambil daftar kategori/tag dari sidebar halaman utama.
  - Melakukan looping untuk mengambil data quote, penulis, dan tag dari halaman 1 sampai 3.
  - Menggabungkan seluruh tag unik dari halaman utama dan hasil quotes untuk dijadikan daftar kategori final.
  - **Penyimpanan**: Data quotes dan kategori disimpan ke dalam satu file Excel (`quotes_data.xlsx`) dengan dua sheet berbeda jika `openpyxl` tersedia. Jika tidak tersedia, program otomatis menyimpannya ke dalam dua file CSV terpisah (`quotes.csv` dan `kategori.csv`) di folder `output/latihan-mandiri/`.

### 2. Mini Project (mini_project.py)
* **Sumber Data**: https://www.scrapethissite.com/pages/
* **Alur Kerja**:
  - **Countries of the World**: Mengambil data nama negara, ibu kota, populasi, dan luas wilayah dalam sekali request.
  - **Hockey Teams**: Melakukan pagination secara otomatis dengan mengirimkan parameter halaman (`page_num`) untuk mengumpulkan seluruh data tim hoki dari halaman 1 sampai selesai (berhenti jika halaman berikutnya kosong).
  - **Oscar Winning Films**: Melakukan request parameter query AJAX (`ajax=true&year=tahun`) langsung ke backend website untuk mengambil data film dalam bentuk JSON dari tahun 2010 hingga 2015.
  - **Penyimpanan**: Masing-masing data disimpan ke dalam file `.csv` terpisah di folder `output/mini-project/`.

---

## Penanganan Masalah & Optimasi Kode

Untuk meningkatkan performa dan keandalan scraping, beberapa modifikasi teknis berikut diterapkan:

* **Session Connection**: Menggunakan `requests.Session()` untuk menjaga koneksi TCP tetap terbuka selama proses request berulang. Hal ini mempercepat proses request halaman secara signifikan.
* **Auto-Retry & Timeout**: Menggunakan adapter `Retry` untuk otomatis mencoba ulang request maksimal 3 kali jika terjadi gangguan jaringan (seperti server lambat atau error 5xx), serta menambahkan batas timeout 10 detik agar program tidak menggantung.
* **Jeda Waktu (Delay)**: Menambahkan delay `time.sleep(2)` setiap kali program melakukan request ke server untuk mematuhi etika web scraping.
* **Penanganan Tag Kosong (Error Handling)**: Menggunakan selector CSS (`select` / `select_one`) yang dibungkus dengan pengecekan kondisi. Jika ada data atau tag HTML yang kosong/berubah di website target, program akan mengisi nilai default (string kosong) daripada berhenti karena error.

---

## Identitas Penulis

Chandra Andaya — H071241044 — Sistem Informasi UNHAS — Mata Kuliah Pengantar Data Mining

