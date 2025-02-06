from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math
import aiohttp
from typing import List
import cProfile
import pstats

app = FastAPI()

# CORS settings for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
)

# Response Models
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

# Number checks
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = math.isqrt(n)
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
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

def is_armstrong(n: int) -> bool:
    original = n
    num_str = str(abs(n))
    length = len(num_str)
    total = sum(int(digit) ** length for digit in num_str)
    return total == original

# Asynchronous fun fact retrieval
async def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                return await response.text()
    except Exception:
        return "No fun fact available."

# API Endpoint
@app.get("/api/classify-number")
async def classify_number(number: str = Query(...)):

    if not number.strip():
        return JSONResponse(content=ErrorResp(number="", error=True).dict(), status_code=400)

    try:
        number = int(number)
        if number < 0:
            return JSONResponse(content=ErrorResp(number=str(number), error=True).dict(), status_code=400)
    except ValueError:
        return JSONResponse(content=ErrorResp(number=number, error=True).dict(), status_code=400)

    properties = ["even" if number % 2 == 0 else "odd"]
    if is_armstrong(number):
        properties.append("armstrong")

    fun_fact = await get_fun_fact(number)
    if __name__ == "__main__":
       uvicorn.run(app, port=8080)

    return Resp(
        number=number,
        is_prime=is_prime(number),
        is_perfect=is_perfect(number),
        properties=properties,
        digit_sum=digit_sum(number),
        fun_fact=fun_fact
    )
