# **SAINTEK OVERFLOW**



## Implementasi FR-02: Ajukan Pertanyaan



##### **1. Deskripsi Proyek**



SAINTEK OVERFLOW merupakan proyek aplikasi forum tanya jawab akademik mahasiswa. Pada praktikum Software Construction \& Good Coding Practices, kelompok mengimplementasikan Functional Requirement (FR-02), yaitu fitur Ajukan Pertanyaan.



Fitur ini memungkinkan mahasiswa mengirimkan pertanyaan dengan mengisi judul, deskripsi, kategori, dan tag. Sistem melakukan validasi terhadap input sebelum menyimpan pertanyaan ke database.



##### **2. Identifikasi Functional Requirement**



**FR-02 — Ajukan Pertanyaan**



\- Aktor: Mahasiswa.

\- Prasyarat pada rancangan: Mahasiswa sudah login.

\- Input: Judul pertanyaan, deskripsi, kategori, dan tag.

\- Proses: Sistem memvalidasi kelengkapan dan format input, kemudian menyimpan data pertanyaan.

\- Output: Pertanyaan berhasil disimpan dan ditampilkan pada daftar pertanyaan.



**Alur utama:**



1\. Mahasiswa membuka fitur Ajukan Pertanyaan.

2\. Sistem menampilkan formulir.

3\. Mahasiswa mengisi judul, deskripsi, kategori, dan tag.

4\. Mahasiswa mengirim formulir.

5\. Sistem memvalidasi data.

6\. Jika valid, sistem menyimpan pertanyaan ke database.

7\. Sistem menampilkan pesan keberhasilan dan pertanyaan pada daftar.



**Alur alternatif:** Jika input wajib tidak lengkap atau tidak valid, sistem menampilkan pesan kesalahan dan meminta mahasiswa memperbaiki input.



##### **3. Keterkaitan dengan Rancangan UTS**



Implementasi FR-02 mengacu pada rancangan SAINTEK OVERFLOW yang dibuat pada UTS.



| Rancangan sebelumnya       | Implementasi                     |

| -------------------------- | -------------------------------- |

| Use Case Ajukan Pertanyaan | Formulir pengajuan pertanyaan    |

| Aktor Mahasiswa            | Simulasi mahasiswa pada aplikasi |

| Entitas User               | Tabel `users`                    |

| Entitas Question           | Tabel `questions`                |

| Entitas Category           | Tabel `categories`               |

| Validasi input             | Fungsi `validate\_question()`     |

| Penyimpanan pertanyaan     | Fungsi `save\_question()`         |



Relasi tabel `questions` dengan `users` dan `categories` mengikuti rancangan ERD. Implementasi ini menambahkan kolom `tags` pada tabel `questions` untuk mendukung input tag yang disebutkan dalam alur Use Case. Kolom tersebut merupakan penambahan pada implementasi praktikum.



**Catatan ruang lingkup:** Program ini dibuat sebagai demonstrasi mandiri FR-02. Login yang tersedia hanya simulasi, bukan implementasi autentikasi FR-01 secara penuh.



##### **4. Teknologi yang Digunakan**



| Teknologi | Kegunaan                       |

| --------- | ------------------------------ |

| Python    | Bahasa pemrograman utama       |

| Flask     | Framework aplikasi web         |

| MySQL     | Penyimpanan data               |

| PyMySQL   | Penghubung Python dengan MySQL |

| HTML      | Struktur halaman               |

| CSS       | Tampilan halaman               |



##### **5. Struktur Proyek**



SAINTEK-OVERFLOW/

├── app.py

├── database.py

├── question.py

├── requirements.txt

├── README.md

├── database/

│   └── saintek\_overflow.sql

├── templates/

│   ├── index.html

│   └── demo\_login.html

└── static/

&#x20;   └── style.css



##### **6. Code Review dan Refactoring**



Berikut tiga contoh perbaikan kode yang digunakan untuk mendokumentasikan penerapan Good Coding Practices. Contoh kode sebelum merupakan ilustrasi kode awal yang disederhanakan, bukan klaim bahwa repository sebelumnya telah memiliki kesalahan tersebut.



###### **Temuan 1 — Penamaan variabel kurang deskriptif**



**Before:**



python

def save(d):

&#x20;   t = d\["title"]

&#x20;   x = d\["description"]

&#x20;   # proses penyimpanan



**After:**



python

def save\_question(question\_data, user\_id):

&#x20;   title = question\_data\["title"]

&#x20;   description = question\_data\["description"]

&#x20;   # proses penyimpanan



**Perbaikan:** Nama fungsi dan variabel dibuat lebih deskriptif sehingga tujuan kode lebih mudah dipahami dan dipelihara.



###### **Temuan 2 — Validasi input belum dilakukan**



**Before:**



python

title = request.form\["title"]

description = request.form\["description"]



\# Data langsung diproses



**After:**



python

question\_data = {

&#x20;   "title": request.form.get("title", "").strip(),

&#x20;   "description": request.form.get("description", "").strip(),

&#x20;   "category\_id": request.form.get("category\_id", "").strip(),

&#x20;   "tags": request.form.get("tags", "").strip(),

}



errors = validate\_question(question\_data)



if errors:

&#x20;   for error in errors:

&#x20;       flash(error, "error")

&#x20;   return redirect(url\_for("index"))



**Perbaikan:** Input diperiksa terlebih dahulu sebelum diteruskan ke proses penyimpanan. Sistem dapat menolak judul atau deskripsi kosong dan input yang tidak memenuhi batas yang ditentukan.



###### **Temuan 3 — Query SQL tidak menggunakan parameter**



**Before:**



python

sql = f"INSERT INTO questions (title) VALUES ('{title}')"

cursor.execute(sql)



**After:**



python

sql = "INSERT INTO questions (title) VALUES (%s)"

cursor.execute(sql, (title,))



**Perbaikan:** Parameterized query memisahkan perintah SQL dari nilai input pengguna sehingga membantu mencegah SQL Injection.



##### **7. Tabel Pengujian**



Pengujian dilakukan untuk memastikan FR-02 berjalan sesuai kebutuhan.



|FR|Steps / Langkah pengujian|Sesuai?|
|-|-|-|
|FR-02|Mengisi judul, deskripsi, kategori, dan tag dengan data valid, kemudian mengirim formulir.|\[✓]|
|FR-02|Mengosongkan judul, kemudian mengirim formulir. Sistem diharapkan menampilkan pesan kesalahan.|\[✓]|
|FR-02|Memasukkan karakter khusus seperti `<script>alert('xss')</script>` pada judul atau deskripsi. Sistem diharapkan menampilkan karakter sebagai teks, bukan menjalankannya.|\[✓]|
|FR-02|Memasukkan teks `' OR 1=1 --` sebagai input. Sistem diharapkan memperlakukannya sebagai data biasa, bukan perintah SQL.|\[✓]|



Keterangan:



\- \[✓] Sesuai: hanya dicentang setelah pengujian benar-benar berhasil.

\- \[x] Belum diuji atau belum sesuai.



##### **8. Kontribusi Anggota Kelompok**



Nama anggota kelompok:

|No|Nama Anggota|Kontribusi|
|-|-|-|
|1|Ulil Amrizach Ahmad|Implementasi keseluruhan FR-02, pengembangan backend Python Flask, pembuatan database MySQL, pengembangan frontend, integrasi sistem, pengujian program, refactoring, dan dokumentasi proyek.|
|2|Zahratunnida Ayudi||
|3|Nafisyatul Nur Azahra||
|4|Muhammad Hanif Ihsanullah||



##### **9. Instalasi dan Menjalankan Program**



**Persyaratan:**



\- Python 3.10 atau lebih baru.

\- MySQL.

\- pip.



**Langkah instalasi:**



1\. Unduh atau clone repository.

2\. Buka terminal pada folder proyek.

3\. Buat virtual environment:



bash

python -m venv venv



4\. Aktifkan virtual environment pada Windows:



bash

venv\\Scripts\\activate



5\. Instal library:



bash

pip install -r requirements.txt



6\. Jalankan MySQL melalui XAMPP.

7\. Buka phpMyAdmin dan import file `database/saintek\_overflow.sql`.

8\. Jalankan aplikasi:



bash

python app.py



9\. Buka alamat berikut pada browser:



http://127.0.0.1:5000



10\. Masuk menggunakan halaman simulasi login, kemudian coba fitur Ajukan Pertanyaan.



##### **10. Catatan**



Aplikasi ini merupakan implementasi mandiri FR-02 untuk kebutuhan praktikum. Fitur login masih berupa simulasi. Untuk penggunaan aplikasi sebenarnya, diperlukan integrasi autentikasi dan pengamanan konfigurasi aplikasi lebih lanjut.



##### **11. Repository**



Link GitHub/GitLab:



https://github.com/ulilzach38-code/saintek-overflow-fr02.git](https://github.com/ulilzach38-code/saintek-overflow-fr02.git



