# Malaria App

Aplikasi web untuk membantu proses diagnosa malaria berbasis gejala. Proyek ini terdiri dari backend Flask dan frontend Vue 3. Backend menyediakan API untuk autentikasi, master gejala, penyakit, aturan, pasien, user, dan riwayat diagnosa. Frontend menyediakan halaman untuk pasien, pakar, dan admin.

## Fitur Utama

- Autentikasi login dan register dengan JWT.
- Role pengguna: `admin`, `pakar`, dan `pasien`.
- Manajemen data gejala.
- Manajemen data penyakit, bobot, solusi, dan aturan penyakit.
- Proses diagnosa pasien berdasarkan gejala yang dipilih.
- Riwayat diagnosa pasien.
- Laporan diagnosa untuk admin.
- Manajemen user oleh admin.

## Struktur Proyek

```text
malariaapp/
+-- backend/
|   +-- malariaapp/
|       +-- app.py
|       +-- config.py
|       +-- helper.py
|       +-- models.py
|       +-- requirements.txt
|       +-- core/
|       |   +-- __init__.py
|       |   +-- blueprints/
|       |       +-- auth_routes.py
|       |       +-- gejala_routes.py
|       |       +-- penyakit_routes.py
|       |       +-- aturan_routes.py
|       |       +-- diagnosa_routes.py
|       |       +-- pasien_routes.py
|       |       +-- user_routes.py
|       +-- migrations/
|       +-- seeders/
+-- clientapp/
    +-- package.json
    +-- vite.config.ts
    +-- src/
        +-- App.vue
        +-- main.ts
        +-- router/
        +-- views/
        +-- services/
        +-- stores/
        +-- models/
        +-- components/
```

## Teknologi

Backend:

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- PyJWT
- MySQL dengan `PyMySQL`

Frontend:

- Vue 3
- Vite
- TypeScript
- Pinia
- Vue Router
- Axios
- Tailwind CSS
- Preline UI
- Vitest

## Model Data

Entitas utama di backend berada di `backend/malariaapp/models.py`.

| Model | Fungsi |
| --- | --- |
| `User` | Data akun pengguna, termasuk username, email, password hash, role, dan status aktif. |
| `Pasien` | Profil pasien yang terhubung ke `User`. |
| `Gejala` | Master gejala penyakit. |
| `Penyakit` | Master penyakit, bobot, dan solusi. |
| `Aturan` | Relasi antara penyakit dan gejala. |
| `Diagnosa` | Hasil diagnosa pasien terhadap penyakit tertentu. |
| `DiagnosaGejala` | Gejala yang dipilih pada proses diagnosa. |

Relasi penting:

- Satu `User` dapat memiliki satu atau lebih data `Pasien`.
- Satu `Penyakit` memiliki banyak `Aturan`.
- Satu `Gejala` dapat digunakan oleh banyak `Aturan`.
- Satu `Diagnosa` dimiliki oleh satu `Pasien` dan satu `Penyakit`.
- Satu `Diagnosa` memiliki banyak `DiagnosaGejala`.

## Prasyarat

- Python 3
- MySQL
- Node.js sesuai engine frontend: `^20.19.0` atau `>=22.12.0`
- Bun

## Konfigurasi Environment

### Backend

Buat atau sesuaikan file `backend/malariaapp/.env`.

```env
SECRET_KEY=isi_secret_key
FLASK_ENV=development
FLASK_CONFIG=config.DevelopmentConfig
FLASK_APP=app.py
FLASK_DEBUG=1

DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DB_NAME=malaria_db

SQLALCHEMY_DATABASE_URI=mysql+pymysql://root@localhost:3306/malaria_db
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

Pada mode development, `config.DevelopmentConfig` membangun koneksi database dari `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, dan `DB_NAME`.

### Frontend

Buat atau sesuaikan file `clientapp/.env`.

```env
VITE_API_URL=http://localhost:5000/api
```

Frontend mengambil nilai ini di `src/App.vue` untuk mengatur `axios.defaults.baseURL`.

## Menjalankan Backend

Masuk ke folder backend:

```powershell
cd backend\malariaapp
```

Buat virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependency:

```powershell
pip install -r requirements.txt
```

Pastikan MySQL sudah berjalan dan database sudah dibuat.

Contoh membuat database lewat MySQL CLI:

```sql
CREATE DATABASE malaria_db;
```

Jalankan aplikasi:

```powershell
flask run
```

Atau:

```powershell
python app.py
```

Secara default Flask berjalan di:

```text
http://localhost:5000
```

## Migrasi Database

Proyek sudah memiliki konfigurasi Flask-Migrate/Alembic di `backend/malariaapp/migrations`.

Contoh perintah:

```powershell
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

Catatan: kode saat ini juga memanggil `database.create_all()` saat aplikasi dibuat, sehingga tabel dapat dibuat otomatis saat aplikasi start.

## Seeder

Seeder tersedia di folder `backend/malariaapp/seeders`.

Data yang dibuat saat ini:

- User admin dari `user_seeder.py`.
- Master penyakit dari `penyakit_seeder.py`.
- Master gejala dari `gejala_seeder.py`.
- Aturan penyakit-gejala dari `aturan_seeder.py`.

Jalankan:

```powershell
flask seed
```

Default user admin:

```text
username: admin
email: admin@malaria.app
password: Password@123
role: admin
```

Default data penyakit:

| Kode | Nama | Bobot | Solusi |
| --- | --- | --- | --- |
| `P001` | Tropika | 0.1 | Cek darah |
| `P002` | Tersiana | 0.3 | Cek Darah |
| `P003` | Mix Tropika & Tersiana | 0.3 | Cek darah |
| `P004` | Malariae | 1 | Cek Darah |

Default data gejala:

| Kode | Nama | Aktif |
| --- | --- | --- |
| `G01` | Demam | Ya |
| `G02` | Menggigil | Ya |
| `G03` | Keringat berlebihan | Ya |
| `G04` | Mual dan muntah | Ya |
| `G05` | Lidah pahit | Ya |
| `G06` | Nyeri kepala | Ya |
| `G07` | Nafsu makan menurun | Ya |
| `G08` | Lemas | Ya |
| `G09` | Badan sakit-sakit | Ya |

Default data aturan:

| Penyakit | Gejala |
| --- | --- |
| `P001` | `G01`, `G03`, `G04`, `G05`, `G06`, `G07` |
| `P002` | `G01`, `G02`, `G03`, `G04`, `G05`, `G07` |
| `P003` | `G01`, `G02`, `G03`, `G04`, `G05`, `G06`, `G07`, `G08` |
| `P004` | `G01`, `G03`, `G04`, `G05`, `G07`, `G09` |

## Menjalankan Frontend

Masuk ke folder frontend:

```powershell
cd clientapp
```

Install dependency:

```powershell
bun install
```

Jalankan mode development:

```powershell
bun dev
```

Build production:

```powershell
bun run build
```

Menjalankan test unit:

```powershell
bun test:unit
```

Menjalankan lint:

```powershell
bun lint
```

## Role dan Halaman

Routing frontend berada di `clientapp/src/router/index.ts`.

| Role | Prefix Halaman | Fungsi |
| --- | --- | --- |
| `admin` | `/admin` | Dashboard admin, manajemen user, laporan. |
| `pakar` | `/pakar` | Manajemen gejala, penyakit, dan aturan penyakit. |
| `pasien` | `/pasien` | Beranda pasien, diagnosa, dan riwayat diagnosa. |

Route publik:

- `/auth/login`
- `/auth/register`
- `/about`

Route lain membutuhkan token login. Jika user membuka `/`, frontend akan mengarahkan berdasarkan role:

- `admin` ke `/admin`
- `pakar` ke `/pakar`
- selain itu ke `/pasien`

## Alur Diagnosa

1. Pasien login atau register.
2. Pasien membuka halaman diagnosa.
3. Frontend mengirim daftar gejala yang dipilih ke endpoint `POST /api/pasien/diagnosa`.
4. Backend mengambil seluruh penyakit dan aturan aktif.
5. Untuk setiap penyakit, backend menjalankan fungsi `backward_chaining`.
6. Jika semua gejala aturan suatu penyakit terpenuhi, status penyakit menjadi `true`.
7. Frontend dapat menyimpan hasil diagnosa dengan endpoint `POST /api/pasien/savediagnosa`.
8. Riwayat diagnosa dapat dilihat lewat `GET /api/pasien/riwayat`.

Logika diagnosa berada di:

- `backend/malariaapp/core/blueprints/pasien_routes.py`

## Autentikasi

Backend menggunakan JWT. Endpoint yang dilindungi memakai decorator `@auth_required`.

Header yang diharapkan:

```http
Authorization: Bearer <token>
```

Token berisi:

- `id`
- `username`
- `email`
- `role`
- `is_active`
- `iat`
- `exp`

Masa berlaku token saat ini adalah 1 hari.

## Endpoint API

Base URL backend:

```text
/api
```

### Auth

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| `POST` | `/api/auth/login` | Login dengan username/email dan password. |
| `POST` | `/api/auth/register` | Registrasi akun pasien dan profil pasien. |
| `POST` | `/api/auth/refresh_token` | Membuat token baru dari token lama. |
| `GET` | `/api/auth/pasien` | Mengambil profil pasien dari token login. |

Contoh login:

```json
{
  "username": "admin",
  "password": "Password@123"
}
```

### Gejala

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| `GET` | `/api/gejala` | Mengambil semua gejala. |
| `GET` | `/api/gejala/<id>` | Mengambil detail gejala. |
| `POST` | `/api/gejala/` | Membuat gejala. |
| `PUT` | `/api/gejala/<id>` | Mengubah gejala. |
| `DELETE` | `/api/gejala/<id>` | Menghapus gejala. |

Contoh payload:

```json
{
  "kode": "G001",
  "nama": "Demam",
  "is_active": true
}
```

### Penyakit

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| `GET` | `/api/penyakit` | Mengambil semua penyakit. |
| `GET` | `/api/penyakit/<id>` | Mengambil detail penyakit beserta aturan gejalanya. |
| `POST` | `/api/penyakit/` | Membuat penyakit. |
| `PUT` | `/api/penyakit/<id>` | Mengubah penyakit. |
| `DELETE` | `/api/penyakit/<id>` | Menghapus penyakit. |

Contoh payload:

```json
{
  "kode": "P001",
  "nama": "Malaria Tropika",
  "bobot": 0.8,
  "solusi": "Segera lakukan pemeriksaan lanjutan ke fasilitas kesehatan."
}
```

### Aturan

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| `GET` | `/api/aturan` | Mengambil aturan aktif. |
| `GET` | `/api/aturan/<id>` | Mengambil detail aturan. |
| `POST` | `/api/aturan/` | Membuat aturan penyakit-gejala. |
| `PUT` | `/api/aturan/<id>` | Mengubah aturan. |
| `DELETE` | `/api/aturan/<id>` | Menonaktifkan aturan. |
| `GET` | `/api/aturan/penyakit/<penyakit_id>` | Mengambil aturan aktif berdasarkan penyakit. |

Contoh payload:

```json
{
  "penyakit_id": 1,
  "gejala_id": 2,
  "is_active": true
}
```

### Pasien

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| `GET` | `/api/pasien` | Mengambil semua pasien. |
| `GET` | `/api/pasien/<id>` | Mengambil detail pasien. |
| `PUT` | `/api/pasien/<id>` | Mengubah data pasien. |
| `DELETE` | `/api/pasien/<id>` | Menghapus pasien. |
| `POST` | `/api/pasien/diagnosa` | Melakukan pengecekan diagnosa berdasarkan gejala. |
| `POST` | `/api/pasien/savediagnosa` | Menyimpan hasil diagnosa. |
| `GET` | `/api/pasien/riwayat` | Mengambil riwayat diagnosa pasien login. |

Contoh payload diagnosa:

```json
[
  { "kode": "G001", "jawaban": "ya" },
  { "kode": "G002", "jawaban": "ya" }
]
```

Contoh payload simpan diagnosa:

```json
{
  "penyakit_id": 1,
  "gejalas": [1, 2, 3]
}
```

### Diagnosa

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| `GET` | `/api/diagnosa` | Mengambil semua riwayat diagnosa. |
| `GET` | `/api/diagnosa/search?mulai=<tanggal>&hingga=<tanggal>` | Filter diagnosa berdasarkan rentang tanggal. |
| `GET` | `/api/diagnosa/<id>` | Mengambil detail diagnosa. |
| `POST` | `/api/diagnosa/` | Membuat diagnosa. |
| `PUT` | `/api/diagnosa/<id>` | Mengubah diagnosa. |
| `DELETE` | `/api/diagnosa/<id>` | Menghapus diagnosa. |

Contoh query search:

```text
/api/diagnosa/search?mulai=2026-01-01T00:00:00&hingga=2026-01-31T23:59:59
```

### User

| Method | Endpoint | Keterangan |
| --- | --- | --- |
| `GET` | `/api/user` | Mengambil semua user. |
| `POST` | `/api/user/` | Membuat user baru. |
| `DELETE` | `/api/user/<id>` | Menghapus user. |

Contoh payload:

```json
{
  "username": "pakar1",
  "email": "pakar1@example.com",
  "role": "pakar",
  "is_active": true
}
```

Password default user yang dibuat dari endpoint ini adalah:

```text
Password@123
```

## Catatan Pengembangan

- Frontend membutuhkan `VITE_API_URL` yang mengarah ke backend dengan prefix `/api`.
- Header auth standar adalah `Authorization: Bearer <token>`.
- Beberapa route backend memakai slash akhir, misalnya `POST /api/gejala/`, `POST /api/penyakit/`, dan `POST /api/aturan/`.
- Endpoint `POST /api/pasien/diagnosa` hanya menghitung kemungkinan penyakit. Untuk menyimpan hasil, gunakan `POST /api/pasien/savediagnosa`.
- Endpoint `DELETE /api/aturan/<id>` melakukan soft delete dengan mengubah `is_active` menjadi `False`.
- Seeder admin, penyakit, gejala, dan aturan mengecek data yang sudah ada, sehingga `flask seed` aman dijalankan ulang.
- File `backend/books.db`, `backend/db.py`, dan `backend/dbconnection.py` terlihat sebagai artefak lama/eksperimen SQLite dan tidak menjadi jalur utama aplikasi Flask saat ini.

## Troubleshooting

### Frontend tidak bisa mengakses API

Pastikan `clientapp/.env` berisi:

```env
VITE_API_URL=http://localhost:5000/api
```

Restart dev server setelah mengubah `.env`.

### Endpoint mengembalikan 401

Pastikan token dikirim dengan format:

```http
Authorization: Bearer <token>
```

Login ulang jika token sudah kedaluwarsa.

### Database gagal terkoneksi

Periksa variabel:

- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`

Pastikan database MySQL sudah dibuat dan service MySQL berjalan.

### User admin belum ada

Jalankan:

```powershell
cd backend\malariaapp
flask seed
```

Lalu login menggunakan:

```text
admin / Password@123
```
