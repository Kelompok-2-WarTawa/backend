# Model
---
this directory containing template for data, intended to make the data explicit so it easier to see the data flows.

why i making this, because i used to using some languages like rust, c++, etc which the data were explicit, so let say it was my behavior.

i think it will making the serial/deserialize data easier (from my views).

---
## Data Table

im not the one who manages the database, but i guess the base on note in [the term](https://kuliah.mhabibalgifari.site/pengembangan-aplikasi-web/uas.html "PEMWEB UAS TERM")
it would be look like this.


---

# ##  Users Table

| Field    | Type       | Description            | Notes                         |
| -------- | ---------- | ---------------------- | ----------------------------- |
| id       | int        | Primary key            | Auto-increment                |
| name     | str        | User full name         |                               |
| email    | str        | Unique user email      | Uniqueness required           |
| password | str        | Hashed password        |                               |
| role     | Role(enum) | User role (admin/user) | Stored as string or int in DB |

---

# ##  Events Table

| Field        | Type     | Description            | Notes                 |
| ------------ | -------- | ---------------------- | --------------------- |
| id           | int      | Primary key            | Auto-increment        |
| organizer_id | int      | Reference to Users(id) | FK                    |
| name         | str      | Event title            |                       |
| description  | str      | Event description      | Multiline OK          |
| date         | datetime | Event date/time        | Use ISO 8601 for JSON |
| venue        | str      | Event location         |                       |
| capacity     | int      | Max attendees          |                       |
| ticket_price | Decimal  | Price per ticket       | Currency-safe         |

---

# ##  Bookings Table

| Field        | Type     | Description               | Notes                    |
| ------------ | -------- | ------------------------- | ------------------------ |
| id           | int      | Primary key               | Auto-increment           |
| event_id     | int      | Reference to Events(id)   | FK                       |
| attendee_id  | int      | Reference to Users(id)    | FK                       |
| quantity     | int      | Number of tickets booked  |                          |
| total_price  | Decimal  | Total calculated price    | Service-layer computed   |
| booking_code | str      | Unique booking identifier | e.g. "EVT-2025-000123"   |
| booking_date | datetime | When booking was created  | ISO 8601 format for JSON |

---
