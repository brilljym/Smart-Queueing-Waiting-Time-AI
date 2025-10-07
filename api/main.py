from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your domain(s) for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/estimate")
def estimate_wait_time(queue_length: int, avg_service_time: float, counters: int = 1):
    wait_time = (queue_length * avg_service_time) / counters
    turnaround_time = wait_time + avg_service_time
    return {"estimated_turnaround_time_minutes": round(turnaround_time, 2)}