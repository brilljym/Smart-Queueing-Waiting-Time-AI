from fastapi import FastAPI

app = FastAPI()

@app.get("/estimate")
def estimate_wait_time(queue_length: int, avg_service_time: float, counters: int = 1):
    wait_time = (queue_length * avg_service_time) / counters
    return {"estimated_wait_time_minutes": round(wait_time, 2)}