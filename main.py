from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title=" CineStar Booking API")

movies = [
    {"id": 1, "title": "KGF", "genre": "Action", "language": "Kannada", "duration_mins": 148, "ticket_price": 300, "seats_available": 50},
    {"id": 2, "title": "Inception", "genre": "Sci-Fi", "language": "English", "duration_mins": 155, "ticket_price": 250, "seats_available": 40},
    {"id": 3, "title": "Interstellar", "genre": "Sci-Fi", "language": "English", "duration_mins": 169, "ticket_price": 350, "seats_available": 30},
    {"id": 4, "title": "The Prestige", "genre": "Action", "language": "Hindi", "duration_mins": 170, "ticket_price": 200, "seats_available": 60},
    {"id": 5, "title": "Avengers", "genre": "Action", "language": "English", "duration_mins": 143, "ticket_price": 400, "seats_available": 25},
    {"id": 6, "title": "Kantara", "genre": "Drama", "language": "Kannada", "duration_mins": 150, "ticket_price": 220, "seats_available": 35},
]

bookings = []
booking_counter = 1

holds = []
hold_counter = 1

class BookingRequest(BaseModel):
    customer_name: str = Field(min_length=2)
    movie_id: int
    seats: int = Field(gt=0, le=10)
    phone: str = Field(min_length=10)
    seat_type: str = "standard"
    promo_code: str = ""

class NewMovie(BaseModel):
    title: str = Field(min_length=2)
    genre: str = Field(min_length=2)
    language: str = Field(min_length=2)
    duration_mins: int = Field(gt=0)
    ticket_price: int = Field(gt=0)
    seats_available: int = Field(gt=0)

def find_movie(movie_id):
    return next((m for m in movies if m["id"] == movie_id), None)

def calculate_ticket_cost(base_price, seats, seat_type, promo_code=""):
    multiplier = 1
    if seat_type == "premium":
        multiplier = 1.5
    elif seat_type == "recliner":
        multiplier = 2

    total = base_price * seats * multiplier

    discount = 0
    if promo_code == "SAVE10":
        discount = total * 0.1
    elif promo_code == "SAVE20":
        discount = total * 0.2

    return {
        "original": total,
        "discounted": int(total - discount)
    }

@app.get("/")
def home():
    return {"message": "Welcome to CineStar Booking 🎬🍿"}

@app.get("/movies")
def get_movies():
    return {
        "movies": movies,
        "total": len(movies),
        "total_seats_available": sum(m["seats_available"] for m in movies)
    }

@app.get("/movies/summary")
def get_summary():
    return {
        "total_movies": len(movies),
        "most_expensive": max(movies, key=lambda m: m["ticket_price"]),
        "cheapest": min(movies, key=lambda m: m["ticket_price"]),
        "total_seats": sum(m["seats_available"] for m in movies),
        "genre_count": {
            g: sum(1 for m in movies if m["genre"] == g)
            for g in set(m["genre"] for m in movies)
        }
    }

@app.get("/movies/filter")
def filter_movies(
    genre: Optional[str] = None,
    language: Optional[str] = None,
    max_price: Optional[int] = None,
    min_seats: Optional[int] = None
):
    result = movies

    if genre:
        result = [m for m in result if m["genre"].lower() == genre.lower()]
    if language:
        result = [m for m in result if m["language"].lower() == language.lower()]
    if max_price:
        result = [m for m in result if m["ticket_price"] <= max_price]
    if min_seats:
        result = [m for m in result if m["seats_available"] >= min_seats]

    return {"movies": result}

@app.get("/movies/search")
def search_movies(keyword: str):
    result = [
        m for m in movies
        if keyword.lower() in m["title"].lower()
        or keyword.lower() in m["genre"].lower()
        or keyword.lower() in m["language"].lower()
    ]
    return {"total_found": len(result), "movies": result}

@app.get("/movies/sort")
def sort_movies(sort_by: str = "ticket_price", order: str = "asc"):
    if sort_by not in ["ticket_price", "title", "duration_mins", "seats_available"]:
        raise HTTPException(400, "Invalid sort_by")

    return {"movies": sorted(movies, key=lambda m: m[sort_by], reverse=(order == "desc"))}

@app.get("/movies/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return {
        "page": page,
        "total_pages": -(-len(movies) // limit),
        "movies": movies[start:start + limit]
    }

@app.get("/movies/browse")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "ticket_price",
    order: str = "asc",
    page: int = 1,
    limit: int = 3,
    genre: Optional[str] = None,
    language: Optional[str] = None
):
    result = movies

    if keyword:
        result = [m for m in result if keyword.lower() in m["title"].lower()]
    if genre:
        result = [m for m in result if m["genre"].lower() == genre.lower()]
    if language:
        result = [m for m in result if m["language"].lower() == language.lower()]
    allowed_fields = ["ticket_price", "title", "duration_mins", "seats_available"]

    if sort_by not in allowed_fields:
        raise HTTPException(400, detail="Invalid sort field")

    if order not in ["asc", "desc"]:
        raise HTTPException(400, detail="Invalid order")

    result = sorted(result, key=lambda m: m[sort_by], reverse=(order == "desc"))

    total = len(result)

    start = (page - 1) * limit
    end = start + limit

    paginated = result[start:end]

    return {
        "total_found": total,
        "page": page,
        "limit": limit,
        "total_pages": -(-total // limit),
        "movies": paginated
    }

# CRUD
@app.post("/movies", status_code=201)
def add_movie(movie: NewMovie):
    if any(m["title"].lower() == movie.title.lower() for m in movies):
        raise HTTPException(400, "Duplicate movie")

    new_movie = movie.dict()
    new_movie["id"] = len(movies) + 1
    movies.append(new_movie)

    return new_movie

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, ticket_price: Optional[int] = None, seats_available: Optional[int] = None):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if ticket_price is not None:
        movie["ticket_price"] = ticket_price
    if seats_available is not None:
        movie["seats_available"] = seats_available

    return movie

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)

    if not movie:
        raise HTTPException(404, "Movie not found")

    if any(b["movie"] == movie["title"] for b in bookings):
        raise HTTPException(400, "Cannot delete movie with bookings")

    movies.remove(movie)

    return {"message": f"{movie['title']} deleted"}

# BOOKINGS
@app.post("/bookings")
def create_booking(data: BookingRequest):
    global booking_counter

    movie = find_movie(data.movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")

    if movie["seats_available"] < data.seats:
        raise HTTPException(400, "Not enough seats")

    cost = calculate_ticket_cost(movie["ticket_price"], data.seats, data.seat_type, data.promo_code)

    movie["seats_available"] -= data.seats

    booking = {
        "booking_id": booking_counter,
        "customer_name": data.customer_name,
        "movie": movie["title"],
        "seats": data.seats,
        "total_cost": cost["discounted"]
    }

    bookings.append(booking)
    booking_counter += 1

    return booking

@app.get("/bookings")
def get_bookings():
    return {"bookings": bookings}

# HOLDING 

@app.post("/seat-hold")
def hold_seats(customer_name: str, movie_id: int, seats: int):
    global hold_counter

    movie = find_movie(movie_id)
    if not movie or movie["seats_available"] < seats:
        raise HTTPException(400, "Not enough seats")

    movie["seats_available"] -= seats

    hold = {
        "hold_id": hold_counter,
        "customer_name": customer_name,
        "movie_id": movie_id,
        "seats": seats
    }

    holds.append(hold)
    hold_counter += 1

    return hold

@app.get("/seat-hold")
def get_holds():
    return holds

@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id: int):
    global booking_counter

    hold = next((h for h in holds if h["hold_id"] == hold_id), None)
    if not hold:
        raise HTTPException(404, "Hold not found")

    movie = find_movie(hold["movie_id"])

    booking = {
        "booking_id": booking_counter,
        "customer_name": hold["customer_name"],
        "movie": movie["title"],
        "seats": hold["seats"]
    }

    bookings.append(booking)
    holds.remove(hold)
    booking_counter += 1

    return {
        "message": "Booking confirmed",
        "booking": booking
    }

@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id: int):
    hold = next((h for h in holds if h["hold_id"] == hold_id), None)
    if not hold:
        raise HTTPException(404, "Hold not found")

    movie = find_movie(hold["movie_id"])
    movie["seats_available"] += hold["seats"]

    holds.remove(hold)

    return {"message": "Hold released"}

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(404, "Movie not found")
    return movie
