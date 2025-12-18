# Panduan Migrasi Database (Alembic)

Folder ini berisi konfigurasi dan riwayat perubahan database (version control for database).

## Cara Menggunakan

Pastikan Virtual Environment (`venv`) sudah aktif sebelum menjalankan perintah.

### 1. Membuat Revisi Baru (Generate Migration)
Jalankan perintah ini setiap kali Anda mengubah kode di `src/models/`.
```bash
# Format: alembic revision --autogenerate -m "Pesan perubahan"
alembic revision --autogenerate -m "Add seats table"
```

### 2. Update Database (Apply Changes)
Perintah ini akan membuat/mengubah tabel di PostgreSQL sesuai revisi terbaru.
```bash
alembic upgrade head
```

### 3. Membatalkan Perubahan (Undo)
Jika ada kesalahan migrasi, mundur satu langkah ke belakang.
```bash
alembic downgrade -1
```

### 4. Reset Database (Fresh Start)
Jika database error parah dan ingin diulang dari nol (Data akan hilang!).
1. Hapus semua tabel di database (bisa pakai pgAdmin atau Docker).
2. Hapus semua file `.py` di dalam folder `alembic/versions/`.
3. Jalankan:
```bash
alembic revision --autogenerate -m "Initial Migration"
alembic upgrade head
```

---

# Business Logic (Services Layer)

Layer ini menangani logika bisnis aplikasi sebelum data disimpan ke database. Controller/View memanggil Service, bukan Model langsung.

## Daftar Service Utama

### 1. Event Service (`event_service.py`)
* **Fungsi:** CRUD Event.
* **Auto-Generate Seats:** Saat event dibuat, sistem otomatis membuat record kursi di tabel `seats` sejumlah `capacity`.
    * *Pola Label:* "Seat-1", "Seat-2", dst.

### 2. Booking Service (`booking_service.py`)
Service paling kompleks yang menangani logika konkurensi pemesanan tiket.

* **Create Booking (Pemesanan):**
    1.  Cek apakah `quantity` > 0.
    2.  Query mencari `Seat` milik event tersebut yang `booking_id`-nya masih `NULL` (Kosong).
    3.  Menggunakan `with_for_update()` untuk mengunci baris database (mencegah *double booking* saat traffic tinggi).
    4.  Jika kursi cukup, sistem mengisi kolom `booking_id` pada kursi-kursi tersebut dengan ID booking baru.
    
* **Cancel Booking (Pembatalan):**
    1.  Mengubah status booking jadi `CANCELLED`.
    2.  **Melepas Kursi:** Mengubah kolom `booking_id` pada tabel `seats` kembali menjadi `NULL` agar bisa dipesan orang lain.

### 3. User Service (`user_service.py`)
* Menangani Hashing Password (bcrypt).
* Validasi email unik.
* Login & Autentikasi.