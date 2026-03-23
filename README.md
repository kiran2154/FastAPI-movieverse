# FastAPI-movieverse
# CineStar Booking API (FastAPI Project)

A complete **Movie Ticket Booking System** built using **FastAPI**, covering all core backend concepts including CRUD operations, validation, booking logic, filtering, searching, sorting, pagination, and seat management.

## Features

###  Movie Management

* Add new movies
* Update movie details (price, seats)
* Delete movies (with booking restriction)
* View all movies
* View single movie by ID
* Movie summary (stats + analytics)


###  Booking System

* Create bookings with validation
* Seat availability check
* Cost calculation (with seat types & promo codes)
* View all bookings
* Total revenue calculation

### Seat Hold System

* Hold seats temporarily
* Confirm hold → convert to booking
* Release hold → restore seats

### Search & Filtering

* Search movies by:

  * Title
  * Genre
  * Language
* Filter by:

  * Genre
  * Language
  * Price
  * Available seats

### Sorting

* Sort movies by:

  * Ticket price
  * Title
  * Duration
  * Seats available
* Ascending / Descending order

### Pagination

* Page-based movie listing
* Custom page & limit
* Total pages calculation

### Combined Browse

* Search + Filter + Sort + Pagination in one endpoint

## Tech Stack

* **Backend:** FastAPI
* **Language:** Python
* **Validation:** Pydantic
* **Server:** Uvicorn

## How to Run

### 1. Install dependencies

```bash
pip install fastapi uvicorn
```

### 2. Run server

```bash
uvicorn main:app --reload
```

### 3. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

## 📌 Important Endpoints

### 🎬 Movies

* `GET /movies`
* `GET /movies/{movie_id}`
* `POST /movies`
* `PUT /movies/{movie_id}`
* `DELETE /movies/{movie_id}`
* `GET /movies/summary`

---

### 🎟️ Bookings

* `POST /bookings`
* `GET /bookings`

---

### 🪑 Seat Hold

* `POST /seat-hold`
* `POST /seat-confirm/{hold_id}`
* `DELETE /seat-release/{hold_id}`

---

### 🔍 Advanced Features

* `GET /movies/search`
* `GET /movies/filter`
* `GET /movies/sort`
* `GET /movies/page`
* `GET /movies/browse`

---

## 🧠 Key Concepts Covered

* REST API design
* Data validation (Pydantic)
* Query & path parameters
* Error handling (HTTPException)
* Business logic (booking system)
* List operations (filter, sort, slice)
* Pagination logic
* Real-world workflow simulation

---

## Sample Booking Input
{
  "customer_name": "AbcD",
  "movie_id": 1,
  "seats": 2,
  "phone": "9876543210",
  "seat_type": "premium"
}
## ⚠️ Notes
* Duplicate movies are not allowed
* Cannot delete movies with existing bookings
* Seat hold is temporary until confirmed
* Validation prevents invalid inputs
## 🎯 Conclusion
This project demonstrates a **complete backend system** with real-world features like booking workflows, data validation, and API design — suitable for **learning, assignments, and backend portfolio projects**.

