from time import time
from fastapi import Request

async def log_middleware(request: Request, call_next):
    print("Before route")
    start_time = time()
    response = await call_next(request)
    end_time = time()
    process_time = end_time - start_time
    print(f"Request {request.url} processed in {process_time} seconds")
    return response