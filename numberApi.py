from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import math
import requests
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()

class Resp(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: List[str]
    digit_sum: int
    fun_fact: str

class ErrorResp(BaseModel):
    number: str
    error: bool

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.isqrt(n))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n <= 1:
        return False
    total = 1
    sqrt_n = math.isqrt(n)
    for i in range(2, sqrt_n + 1):
        if n % i == 0:
            total += i
            if (other := n // i) != i:
                total += other
    return total == n

def digit_sum(n: int) -> int:
    n = abs(n)
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

def is_armstrong(n: int) -> bool:
    original = n
    n = abs(n)
    num_str = str(n)
    length = len(num_str)
    total = 0
    temp = n
    
    while temp > 0:
        digit = temp % 10
        total += digit ** length
        temp //= 10
    
    return total == original

@app.get("/api/classify-number")
async def classify_number(number: str = Query(default="")):
    if not number.strip():
        return JSONResponse(
            content=ErrorResp(number="", error=True).dict(),
            status_code=400
        )

    try:
        n = int(number)
    except ValueError:
        return JSONResponse(
            content=ErrorResp(number=number, error=True).dict(),
            status_code=400
        )

    # Fetch fun fact with error handling
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=5)
        response.raise_for_status()
        fun_fact = response.text
    except requests.exceptions.RequestException:
        fun_fact = "No fun fact available."

    # Determine properties
    properties = ["even" if n % 2 == 0 else "odd"]
    if is_armstrong(n):
        properties.append("armstrong")

    return Resp(
        number=n,
        is_prime=is_prime(n),
        is_perfect=is_perfect(n),
        properties=properties,
        digit_sum=digit_sum(n),
        fun_fact=fun_fact
    )
