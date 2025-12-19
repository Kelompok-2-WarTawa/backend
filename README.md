# Backend - Tugas UAS Kelompok 2 WarTawa

Repositori ini berisi kode sumber backend untuk sistem ticketing stand-up comedy "WarTawa". Backend ini dibangun menggunakan framework **Pyramid**, **SQLAlchemy ORM**, dan **PostgreSQL**.

---

## 1. Tim dan Anggota
**Kelompok 2 - WarTawa**
* **Daffa Hakim Matondang** - **123140002** (Database Administrator & Schema)
* **Arrauf Setiawan Muhammad Jabar** - **123140032** (Project Leader)
* **Varasina Farmadani** - **123140107** (Backend Developer & Logic)
* **Fadzilah saputri** - **123140149** (UI/UX Designer)
* **Fadina Mustika Ratnaningsih** - **123140157** (Frontend Developer)



---

## 2. Deskripsi Project dan Fitur Utama
WarTawa adalah platform manajemen tiket acara stand-up comedy yang memungkinkan Admin mengelola acara dan Pengguna (Customer) untuk melakukan reservasi kursi secara real-time.

**Fitur Utama:**
### A. User Authentication (Registrasi & Login)
* **Register:** Pengguna dapat mendaftar sebagai Customer.
* **Login:** Sistem autentikasi menggunakan **JWT (JSON Web Token)** untuk menjaga sesi pengguna.
* **Role Management:** Pembedaan akses antara `ADMIN` (Organizer) dan `CUSTOMER` (Attendee).
* **Security:** Password disimpan dalam bentuk hash menggunakan library `bcrypt`.

### B. Event Management (Organizer/Admin)
* **CRUD Event:** Admin dapat membuat, melihat, memperbarui, dan menghapus data acara.
* **Atribut Lengkap:** Pengaturan nama acara, tanggal, lokasi (venue), kapasitas maksimal, dan harga tiket.
* **Ticket Phases:** Mendukung pengaturan harga berbeda berdasarkan fase (misal: Early Bird, Presale, Normal).

### C. Ticket Booking (Attendee/Customer)
* **Browse Events:** Customer dapat melihat daftar acara yang tersedia.
* **Seat Selection:** Customer dapat memilih nomor kursi secara spesifik pada denah yang tersedia.
* **Race Condition Handling:** Menggunakan sistem *locking* database (`with_for_update`) untuk memastikan satu kursi tidak bisa dipesan oleh dua orang secara bersamaan.

### D. Booking Management
* **Admin Dashboard:** Organizer dapat melihat statistik total pendapatan, jumlah tiket terjual, dan daftar transaksi terbaru.
* **Booking History:** Attendee dapat melihat riwayat pemesanan tiket yang pernah dilakukan pada menu profil.

### E. Ticket Confirmation & Check-in
* **Unique Booking Code:** Setiap transaksi berhasil akan mendapatkan kode unik (format: `BKG-XXXXX`).
* **Validation/Check-in:** Fitur bagi Admin untuk memvalidasi tiket di lokasi acara (mengubah status tiket menjadi *checked-in*) untuk mencegah penggunaan tiket ganda.
---

## 3. Tech Stack
* **Framework:** Pyramid
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** PyJWT (JSON Web Token)
* **Validation:** Pydantic
* **Migration:** Alembic
* **Security:** Bcrypt (Password Hashing)

---

## 4. Cara Instalasi dan Menjalankan (Docker Compose)
### Prasyarat
* **Docker** dan **Docker Compose** terinstal di mesin Anda.
* **PostgreSQL** (sebagai database utama).
### Langkah-langkah
1. **Clone Repositori:**
```bash
git clone <repository-url>
cd kelompok-2-wartawa/backend
```

2. **Konfigurasi Environment:**
Buat file `.env` di direktori utama backend dan lengkapi konfigurasi berikut:
```env
APP_PORT=6543
DB_URL=postgresql://username:password@host.docker.internal:5432/nama_db
JWT_SECRET=rahasia_anda_disini
FRONTEND_URL=http://localhost:5173
```
*(Gunakan `host.docker.internal` jika database PostgreSQL berjalan di sistem host lokal Anda)*.

3. **Build dan Jalankan Kontainer:**
Gunakan Docker Compose untuk membangun image dan menjalankan server API:
```bash
docker-compose up --build
```
Server akan berjalan di `http://localhost:6543**`.

4. **Migrasi Database:**
Setelah kontainer aktif, jalankan perintah migrasi di dalam kontainer untuk membuat struktur tabel:
```bash
docker exec -it wartawa-api alembic upgrade head
```



## 5. Link Deployment

* **Frontend:** https://wartawa.vercel.app/
* **Backend API:** api.wartawa.online

---

## 6. Dokumentasi API (Endpoints)

### User & Authentication

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| `POST` | `/api/users` | Registrasi user(customer) baru. |
| `POST` | `/api/users/login` | Login dan mendapatkan token JWT. |
| `GET` | `/api/users` | Melihat daftar semua user(customer) (Admin Only). |
| `GET` | `/api/users/{id}` | Detail profil user(customer) tertentu. |
| `PUT` | `/api/users/{id}` | Update profil user(customer). |
| `DELETE` | `/api/users/{id}` | Menghapus user(customer) (Admin Only). |
| `POST` | `/api/users/{id}/password` | Ganti password user(customer). |
| `GET` | `/api/users/{id}/events` | Tiket event yang di beli user(customer). |
| `GET` | `/api/users/{id}/bookings` | Riwayat booking user(customer). |

### Event Management

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| `GET` | `/api/events` | Daftar semua event. |
| `POST` | `/api/events` | Membuat event baru (Admin Only). |
| `GET` | `/api/events/{id}` | Detail informasi event. |
| `PUT` | `/api/events/{id}` | Update informasi event (Admin Only). |
| `DELETE` | `/api/events/{id}` | Menghapus event (Admin Only). |
| `GET` | `/api/events/{id}/seats` | Cek ketersediaan kursi event. |

### Booking & Transaction

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| `POST` | `/api/bookings` | Melakukan booking tiket. |
| `GET` | `/api/bookings/{code}` | Cek status booking via kode. |
| `POST` | `/api/bookings/{code}/pay` | Simulasi pembayaran booking. |
| `POST` | `/api/bookings/{code}/cancel` | Membatalkan booking. |
| `POST` | `/api/bookings/{code}/checkin` | Scan tiket/Check-in (Admin Only). |

### Dashboard

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| `GET` | `/api/dashboard` | Statistik admin (revenue, tiket terjual). |

---

## 7. Screenshot Aplikasi
SOON
---

## 8. Link Video Presentasi

https://youtu.be/C2z0OSN27kc

```

```
