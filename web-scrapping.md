# Modul Praktikum: Dasar Web Scraping Menggunakan BeautifulSoup

## 1. Pendahuluan
Web scraping adalah teknik untuk mengambil data dari website secara otomatis menggunakan program. Pada praktikum ini digunakan:
* Bahasa pemrograman Python
* Library `requests`
* Library `BeautifulSoup` untuk parsing HTML

## 2. Tujuan Pembelajaran
Mahasiswa mampu:
1. Memahami konsep dasar web scraping
2. Menggunakan library BeautifulSoup
3. Mengekstrak data dari HTML
4. Menyimpan hasil scraping ke CSV

## 3. Instalasi Library
```bash
pip install requests beautifulsoup4 pandas
```

## 4. Konsep Dasar HTML
Contoh struktur HTML:
```html
<html>
    <body>
        <h1>Judul</h1>
        <p class="deskripsi">Ini paragraf</p>
    </body>
</html>
```

## 5. Alur Web Scraping
```text
Request → Ambil HTML → Parsing → Ekstraksi Data → Simpan
```

---

## 6. Praktikum 1: Mengambil Judul Halaman
Website latihan: https://quotes.toscrape.com

```python
import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.text)
```

## 7. Praktikum 2: Mengambil Data Quotes
```python
import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("div", class_="quote")

for quote in quotes:
    text = quote.find("span", class_="text").text
    author = quote.find("small", class_="author").text
    print(f"Quote : {text}")
    print(f"Author : {author}")
    print("-" * 40)
```

## 8. Praktikum 3: Mengambil Semua Link
```python
links = soup.find_all("a")

for link in links:
    print(link.get("href"))
```

## 9. Praktikum 4: Menyimpan ke CSV
```python
import pandas as pd

data = []

for quote in quotes:
    text = quote.find("span", class_="text").text
    author = quote.find("small", class_="author").text
    data.append([text, author])

df = pd.DataFrame(data, columns=["Quote", "Author"])
df.to_csv("quotes.csv", index=False)

print("Data berhasil disimpan!")
```

## 10. Praktikum 5: Scraping Tabel
```python
table = soup.find("table")
rows = table.find_all("tr")

for row in rows[:5]:
    cols = row.find_all("td")
    data = [col.text.strip() for col in cols]
    print(data)
```

---

## 11. Error yang Sering Terjadi

| Error | Penyebab | Solusi |
| :--- | :--- | :--- |
| **403** | Forbidden (Website memblokir bot) | Tambah User-Agent |
| **NoneType error** | Tag tidak ditemukan | Cek struktur HTML |
| **Timeout** | Koneksi lambat | Tambah parameter timeout |

### Contoh Penggunaan User-Agent:
```python
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
```

## 12. Etika Web Scraping
* Periksa file `robots.txt`
* Jangan melakukan request terlalu cepat
* Gunakan untuk tujuan akademik
* Hindari scraping data sensitif

---

## 13. Latihan Mandiri
1. Ambil semua kategori dari website quotes.toscrape
2. Ambil semua quote dari 3 halaman
3. Simpan hasil ke Excel
4. Tambahkan delay 2 detik tiap request

## 14. Mini Project
Scrape data dari web https://www.scrapethissite.com/pages/, ambil datanya lalu simpan dalam bentuk CSV untuk masing-masing data pada halaman:
* Countries of the World: A Simple Example
* Hockey Teams: Forms, Searching and Pagination
* Oscar Winning Films: AJAX and Javascript

---

## 15. Kesimpulan
Pada modul ini telah dipelajari:
* Konsep dasar web scraping
* Penggunaan `requests`
* Parsing HTML dengan BeautifulSoup
* Ekstraksi data
* Penyimpanan hasil ke CSV
