# Dokumentasi Skema Database (Schema)

Proyek ini menggunakan **PostgreSQL** dengan **SQLAlchemy ORM**. Berikut adalah detail struktur tabel, relasi, dan tipe data.

## Entity Relationship Diagram (ERD) Overview

* **Users** (1) ----< (N) **Events** (Organizer)
* **Users** (1) ----< (N) **Bookings** (Customer)
* **Events** (1) ----< (N) **Seats** (Inventory Kursi)
* **Events** (1) ----< (N) **Bookings**
* **Bookings** (1) ---- (1) **Payments**
* **Bookings** (1) ----< (N) **Seats** (Kursi yang dipesan)

---

## Detail Tabel

### 1. Users (`users`)
Menyimpan data pengguna aplikasi (Admin & Customer).
* **Source:**

| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id` | Integer (PK) | ID unik pengguna. |
| `name` | String(100) | Nama lengkap. |
| `email` | String(100) | Email unik (Login credential). |
| `password` | String(255) | Password ter-hash (bcrypt). |
| `role` | Enum | `ADMIN` atau `CUSTOMER`. |

### 2. Events (`events`)
Menyimpan data acara. Saat Event dibuat, kursi otomatis digenerate.
* **Source:**

| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id` | Integer (PK) | ID unik event. |
| `organizer_id`| Integer (FK) | Relasi ke `users.id` (Pembuat acara). |
| `name` | String(255) | Nama acara. |
| `date` | DateTime | Waktu pelaksanaan. |
| `capacity` | Integer | Total kursi tersedia. |
| `ticket_price`| Numeric | Harga per satu kursi. |

### 3. Seats (`seats`) **[BARU]**
Menyimpan inventaris kursi untuk setiap event.
* **Source:**
* **Logic:** Jika `booking_id` NULL, berarti kursi **KOSONG**. Jika terisi, berarti kursi **SUDAH DIBOOKING**.

| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id` | Integer (PK) | ID unik kursi. |
| `event_id` | Integer (FK) | Relasi ke `events.id`. |
| `booking_id` | Integer (FK) | Relasi ke `bookings.id` (Nullable). |
| `seat_label` | String(10) | Label kursi (Cth: "Seat-1", "A5"). |

### 4. Bookings (`bookings`)
Transaksi pemesanan tiket. Satu booking bisa memegang banyak kursi.
* **Source:**

| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id` | Integer (PK) | ID transaksi. |
| `customer_id` | Integer (FK) | Relasi ke `users.id`. |
| `event_id` | Integer (FK) | Relasi ke `events.id`. |
| `booking_code`| String(50) | Kode unik (Cth: `BKG-XY123`). |
| `quantity` | Integer | Jumlah kursi yang dibeli. |
| `status` | Enum | `PENDING`, `CONFIRMED`, `CANCELLED`. |

### 5. Payments (`payments`)
Detail pembayaran untuk booking.
* **Source:**

| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id` | Integer (PK) | ID pembayaran. |
| `booking_id` | Integer (FK) | Relasi One-to-One ke `bookings`. |
| `amount` | Numeric | Nominal yang dibayar. |
| `status` | Enum | `SUCCESS`, `FAILED`, `REFUNDED`. |