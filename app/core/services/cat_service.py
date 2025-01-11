import requests
from core.models import Cat

CAT_API_URL = "https://api.thecatapi.com/v1/breeds"

def fetch_valid_breeds():
    response = requests.get(CAT_API_URL)
    response.raise_for_status()
    breeds = response.json()
    return [breed["name"] for breed in breeds]


def validate_breed(breed: str):
       if breed not in fetch_valid_breeds():
           raise ValueError(f"Invalid breed: {breed}. Choose from: {', '.join(fetch_valid_breeds())}")

def create_spy_cat(self, name: str, years_of_experience: int, breed: str, salary: float):
    """Create a new spy cat with validation."""
    self.validate_breed(breed)
    new_cat = Cat(
        name=name,
        years_of_experience=years_of_experience,
        breed=breed,
        salary=salary,
    )
    # Add the new cat to the database (e.g., using a session)
    return new_cat