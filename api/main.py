from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.linear_model import LinearRegression
import pandas as pd
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your domain(s) for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample historical data for training the predictive model
data = {
    'queue_length': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'avg_service_time': [5, 5, 5, 5, 5, 6, 6, 6, 6, 6],
    'counters': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
    'actual_wait_time': [5, 10, 15, 20, 25, 18, 21, 24, 27, 30]
}
df = pd.DataFrame(data)
model = LinearRegression()
model.fit(df[['queue_length', 'avg_service_time', 'counters']], df['actual_wait_time'])

@app.get("/estimate")
def estimate_wait_time(queue_length: int, avg_service_time: float, counters: int = 1):
    """
    Estimate wait time using basic formula: (queue_length * avg_service_time) / counters
    """
    wait_time = (queue_length * avg_service_time) / counters
    return {"estimated_wait_time_minutes": round(wait_time, 2)}

@app.get("/predict_release")
def predict_release_date(queue_length: int, avg_service_time: float, counters: int = 1):
    """
    Predictive model to estimate suggested release date for pending documents based on historical data and workload.
    Uses a linear regression model trained on sample historical data.
    """
    predicted_wait = model.predict([[queue_length, avg_service_time, counters]])[0]
    current_time = datetime.now()
    release_date = current_time + timedelta(minutes=predicted_wait)
    return {"suggested_release_date": release_date.isoformat()}