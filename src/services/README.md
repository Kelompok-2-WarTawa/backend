# Services Layer (Business Logic)

Folder ini berisi inti dari logika bisnis aplikasi WarTawa. Layer ini bertugas memproses data, melakukan validasi kompleks, dan menjaga integritas database sebelum data dikirim ke Controller (Views).

## Prinsip Desain
* **Dependency Injection:** Setiap service menerima `db_session` saat inisialisasi untuk melakukan query database.
* **Separation of Concerns:** Service tidak mengetahui tentang HTTP Request/Response. Mereka hanya menerima data (dict/args), memprosesnya, dan mengembalikan objek Model atau melempar Error.

---

## Daftar Service

### 1. Event Service (`event_service.py`)
Bertanggung jawab atas manajemen acara dan inventaris kursi.
* **Source:**

**Fitur Utama:**
* **CRUD Event:** Membuat, membaca, mengupdate, dan menghapus event.
* **Automatic Seat Generation:** Setiap kali Event baru dibuat, service ini secara otomatis melakukan *looping* sebanyak kapasitas event dan membuat record kursi di tabel `seats`.
  * *Format Label:* "Seat-1", "Seat-2", ..., "Seat-N".
* **Validasi Tanggal:** Memastikan format tanggal input sesuai standar ISO 8601.

### 2. Booking Service (`booking_service.py`)
Service paling kompleks yang menangani transaksi pemesanan tiket dengan keamanan tinggi (Thread-safe).
* **Source:**

**Logika Transaksi (Create Booking):**
1. **Validasi Input:** Memastikan jumlah tiket (`quantity`) > 0.
2. **Race Condition Handling:** Menggunakan query `with_for_update()` saat mengambil data kursi. Ini mengunci baris database agar tidak ada dua orang yang membooking kursi yang sama di waktu yang bersamaan.
3. **Seat Assignment:** Sistem otomatis mencari kursi dengan `event_id` yang sesuai dan `booking_id` yang masih `NULL` (Kosong).
4. **Booking Code:** Menghasilkan kode unik acak (misal: `BKG-7F3A2C1B`).
5. **Update Kursi:** Mengisi kolom `booking_id` pada kursi yang terpilih dengan ID booking baru.

**Logika Pembatalan (Cancel Booking):**
* Membatalkan status booking menjadi `CANCELLED`.
* **Release Seats:** Secara otomatis melepas kursi yang sebelumnya dipesan (mengubah `booking_id` kembali menjadi `NULL`) sehingga kursi tersebut bisa dipesan ulang oleh user lain.

**Logika Pembayaran (Pay Booking):**
* Memverifikasi jumlah pembayaran.
* Mengubah status booking menjadi `CONFIRMED`.
* Mencatat riwayat pembayaran di tabel `payments`.

### 3. User Service (`user_service.py`)
Menangani manajemen pengguna dan keamanan akun.
* **Source:**

**Fitur Utama:**
* **Password Hashing:** Menggunakan `bcrypt` untuk mengenkripsi password sebelum disimpan ke database.
* **Autentikasi:** Memverifikasi email dan password saat login.
* **Validasi Email:** Mencegah pendaftaran ganda dengan email yang sama.
* **Role Management:** Menetapkan peran user sebagai `ADMIN` atau `CUSTOMER`.
