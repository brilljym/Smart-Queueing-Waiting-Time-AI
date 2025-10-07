from fastapi import FastAPI
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

app = FastAPI()

# Dummy training data for AI model
data = {
    'queue_length': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 1, 6, 7, 8, 9],
    'avg_service_time': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 6, 5, 5, 5, 5, 5, 5, 5],
    'counters': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
    'wait_time': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 4, 18, 20, 25, 5, 30, 35, 40, 45]
}

df = pd.DataFrame(data)
X = df[['queue_length', 'avg_service_time', 'counters']]
y = df['wait_time']

# Train the AI model
model = LinearRegression()
model.fit(X, y)

@app.get("/estimate")
def estimate_wait_time(queue_length: int, avg_service_time: float, counters: int = 1):
    # Use AI model to predict wait time
    prediction = model.predict([[queue_length, avg_service_time, counters]])[0]
    return {"estimated_wait_time_minutes": round(max(0, prediction), 2)}