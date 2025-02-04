from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import List

app = FastAPI(title="Number Classification API", description="API to classify numbers and return their properties along with a fun fact.")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:  # Optimization: 2 is the only even prime
        return True
    if n % 2 == 0:  # Optimization: skip even numbers
        return False
    for i in range(3, int(n**0.5) + 1, 2):  # Check only odd numbers up to sqrt(n)
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number."""
    if n <= 1:
        return False
    divisors_sum = 0
    for i in range(1, int(n**0.5) + 1):  # Only check up to sqrt(n)
        if n % i == 0:
            divisors_sum += i
            if i * i != n:  # Avoid double-counting perfect squares
                divisors_sum += n // i
    return divisors_sum == 2 * n  # Includes the number itself in the sum

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number."""
    num_str = str(n)  # Convert to string once
    num_digits = len(num_str)  # Get length once
    armstrong_sum = sum(int(digit)**num_digits for digit in num_str)
    return armstrong_sum == n

def get_fun_fact(n: int) -> str:
    """Fetch a fun fact about the number from the Numbers API with error handling."""
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=5)  # Add timeout
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching fun fact: {e}")  # Log error for debugging
        return "Could not retrieve fun fact."

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="The number to classify")):
    """Classifies the number and returns its properties."""
    try:
        if number < 0:  # Raise an actual HTTPException for proper handling
            raise HTTPException(status_code=400, detail="Number must be non-negative")

        properties: List[str] = []  # Type hint for properties

        if is_armstrong(number):
            properties.append("armstrong")

        properties.append("odd" if number % 2 else "even")

        return {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(digit) for digit in str(number)),
            "fun_fact": get_fun_fact(number),
        }

    except HTTPException as e:  # Catch HTTPException
        raise e  # FastAPI automatically handles HTTP exceptions
