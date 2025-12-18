# Views Layer (Controllers)

Folder ini berisi **View Handlers** (Controller) yang bertugas menerima request HTTP, memvalidasi input dasar, memanggil **Service Layer**, dan mengembalikan response JSON.

Views diimplementasikan menggunakan dekorator `@view_config` dari framework **Pyramid**.

---

## Daftar Module Views

### 1. User Views (`user_views.py`)
Menangani endpoint terkait otentikasi dan manajemen pengguna.
* **Source:**

| Method | Endpoint | Fungsi |
| :--- | :--- | :--- |
| `POST` | `/api/users` | Register user baru (Default role: Customer). |
| `POST` | `/api/users/login` | Login & mendapatkan JWT Token. |
| `GET` | `/api/users` | Melihat daftar semua user. |
| `GET` | `/api/users/{id}` | Melihat detail user spesifik. |
| `PUT` | `/api/users/{id}` | Update profil user. |
| `GET` | `/api/users/{id}/events` | Melihat event yang dibuat oleh user (Organizer). |
| `GET` | `/api/users/{id}/bookings` | Melihat riwayat booking user (Customer). |

### 2. Event Views (`event_views.py`)
Menangani manajemen acara stand-up comedy. Hanya **ADMIN** yang bisa membuat/mengubah event.
* **Source:**

| Method | Endpoint | Fungsi |
| :--- | :--- | :--- |
| `GET` | `/api/events` | Melihat daftar semua event. |
| `POST` | `/api/events` | Membuat event baru (Admin only). Otomatis generate kursi. |
| `GET` | `/api/events/{id}` | Detail event. |
| `PUT` | `/api/events/{id}` | Update informasi event. |
| `DELETE`| `/api/events/{id}` | Menghapus event. |
| `GET` | `/api/events/{id}/seats` | **[Fitur Baru]** Melihat ketersediaan kursi (Booked/Available). |

### 3. Booking Views (`booking_views.py`)
Menangani transaksi pemesanan tiket.
* **Source:**

| Method | Endpoint | Fungsi |
| :--- | :--- | :--- |
| `POST` | `/api/bookings` | Booking tiket (Memilih kursi otomatis). |
| `GET` | `/api/bookings/{code}` | Cek status booking berdasarkan Kode Booking. |
| `POST` | `/api/bookings/{code}/pay` | Melakukan pembayaran (Simulasi). |
| `POST` | `/api/bookings/{code}/cancel`| Membatalkan booking & melepas kursi. |

---

## Alur Data (Flow)

1.  **Request** masuk ke `routes.py` dan diarahkan ke fungsi View yang sesuai.
2.  **View** membaca `request.json_body` dan memvalidasi schema menggunakan Pydantic (di `schemas.py`).
3.  **View** memanggil `request.services` (User/Event/Booking Service) untuk memproses logika bisnis.
4.  **Service** mengembalikan objek Model (SQLAlchemy).
5.  **View** merender objek tersebut menjadi JSON dan mengembalikan HTTP Response (misal: 200 OK, 201 Created).