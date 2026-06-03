# DyslexiaLens GenAI: Generator Kalimat Kotak A4

Aplikasi ini adalah alat generatif khusus yang dirancang untuk membuat kalimat dengan batasan struktural dan mekanis yang dimasukkan ke dalam **layout kotak karakter 8x5** pada kertas A4 fisik.

---

## Fitur Utama

* Menghasilkan kalimat yang terdiri dari **tepat 5 kata**, di mana setiap kata memiliki panjang maksimal **8 huruf**.
* Mendukung pembuatan teks dalam **Bahasa Inggris** dan **Bahasa Indonesia**.
* Menganalisis jumlah karakter dari teks yang dihasilkan secara otomatis untuk menjamin keselarasan struktur layout yang sempurna.
* Menampilkan pratinjau di layar yang meniru bagaimana huruf-huruf akan mengisi lembar pelacakan kotak fisik.

---

## Cara Kerja

Aplikasi ini menggunakan **Google GenAI SDK** yang didukung oleh model berkecepatan tinggi `gemini-2.5-flash`. Dengan memberikan batasan instruksi yang jelas langsung ke model, aplikasi ini langsung mengembalikan data bersih yang dipetakan ke layout Anda.

### Contoh Tampilan Layout
Jika generator memproses sebuah topik, teks akan dipetakan baris-demi-baris ke dalam sistem 8-kolom seperti ini:

```text
[B] [E] [L] [A] [J] [A] [R] [ ] -> Kata 1 (7 karakter)
[B] [A] [H] [A] [S] [A] [ ] [ ] -> Kata 2 (6 karakter)
[S] [A] [N] [G] [A] [T] [ ] [ ] -> Kata 3 (6 karakter)
[M] [U] [D] [A] [H] [ ] [ ] [ ] -> Kata 4 (5 karakter)
[S] [E] [K] [A] [L] [I] [ ] [ ] -> Kata 5 (6 karakter)

```



## Setup & Instalasi Lokal

Untuk menjalankan proyek ini secara lokal di komputer Anda, ikuti langkah-langkah berikut:

### 1. Clone Repositori

```bash
git clone [https://github.com/username-kamu/DyslexiaLens_GenAI.git](https://github.com/username-kamu/DyslexiaLens_GenAI.git)
cd DyslexiaLens_GenAI

```

### 2. Install Dependensi

Pastikan Anda telah menginstal Python 3.9 atau versi di atasnya, lalu jalankan:

```bash
pip install -r requirements.txt

```

### 3. Atur API Key Anda

Dapatkan API key gratis melalui **Google AI Studio**. Anda dapat memasukkannya langsung ke dalam antarmuka aplikasi saat dijalankan atau mengekspornya sebagai environment variable di terminal Anda:

```bash
export GEMINI_API_KEY="isi_api_key_kamu_di_sini"

```

### 4. Jalankan Aplikasi Streamlit

```bash
streamlit run app.py

```
