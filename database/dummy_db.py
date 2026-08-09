# --- Dummy Database ---
# In a real project, these would come from a database (like MySQL/PostgreSQL).
# We are temporarily using dictionaries/lists for learning purposes.

users_db = {
    "admin1": {"password": "password123", "role": "admin"},
    "employee1": {"password": "password123", "role": "employee"}
}

customers_data = [
    {"id": 1, "name": "Rahim", "balance": 5000},
    {"id": 2, "name": "Karim", "balance": 10000}
]

# Stores pending, approved, and rejected workflow tasks
loan_requests_data = []
