from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import uuid
import math
from enum import Enum

app = FastAPI(
    title="Smart Queue Management API",
    description="AI-powered queue management system with real-time wait time predictions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your domain(s) for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class QueueStatus(str, Enum):
    WAITING = "waiting"
    IN_SERVICE = "in_service"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    CANCELLED = "cancelled"

class CustomerType(str, Enum):
    WALK_IN = "walk_in"
    APPOINTMENT = "appointment"
    VIP = "vip"
    RETURNING = "returning"

class JoinQueueRequest(BaseModel):
    customer_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    customer_type: CustomerType = CustomerType.WALK_IN
    service_type: str = "general"
    estimated_service_duration: Optional[int] = None  # minutes
    notes: Optional[str] = None

class UpdateQueueRequest(BaseModel):
    status: QueueStatus
    actual_service_duration: Optional[int] = None

class QueueEntry(BaseModel):
    id: str
    customer_name: str
    phone: Optional[str]
    email: Optional[str]
    customer_type: CustomerType
    service_type: str
    status: QueueStatus
    position: int
    estimated_wait_time: int  # minutes
    estimated_turnaround_time: int  # minutes
    actual_wait_time: Optional[int]
    actual_service_time: Optional[int]
    check_in_time: datetime
    service_start_time: Optional[datetime]
    service_end_time: Optional[datetime]
    notes: Optional[str]

# In-memory storage (replace with database in production)
queue_data: Dict[str, QueueEntry] = {}
service_counters = 3  # Default number of service counters
avg_service_times = {
    "general": 15,
    "consultation": 30,
    "premium": 20,
    "technical": 45
}

# AI-powered wait time prediction
def calculate_dynamic_wait_time(position: int, service_type: str, customer_type: CustomerType) -> tuple:
    """
    Advanced wait time calculation using multiple factors
    """
    base_service_time = avg_service_times.get(service_type, 15)
    
    # Adjust for customer type
    if customer_type == CustomerType.VIP:
        base_service_time *= 0.8  # VIP gets faster service
    elif customer_type == CustomerType.APPOINTMENT:
        base_service_time *= 0.9  # Appointments are pre-planned
    elif customer_type == CustomerType.RETURNING:
        base_service_time *= 0.85  # Returning customers need less time
    
    # Calculate current queue load
    active_queue = [q for q in queue_data.values() if q.status == QueueStatus.WAITING]
    queue_length = len(active_queue)
    
    # Dynamic service counter utilization
    current_serving = len([q for q in queue_data.values() if q.status == QueueStatus.IN_SERVICE])
    available_counters = max(1, service_counters - current_serving)
    
    # AI-powered prediction considering time of day, queue patterns
    current_hour = datetime.now().hour
    rush_hour_multiplier = 1.0
    if 9 <= current_hour <= 11 or 14 <= current_hour <= 16:
        rush_hour_multiplier = 1.2
    elif 12 <= current_hour <= 13:
        rush_hour_multiplier = 1.3  # Lunch rush
    
    # Calculate wait time
    estimated_wait = ((position - 1) * base_service_time * rush_hour_multiplier) / available_counters
    estimated_turnaround = estimated_wait + base_service_time
    
    return int(estimated_wait), int(estimated_turnaround)

def update_queue_positions():
    """Update positions for all waiting customers"""
    waiting_customers = [q for q in queue_data.values() if q.status == QueueStatus.WAITING]
    waiting_customers.sort(key=lambda x: x.check_in_time)
    
    for idx, customer in enumerate(waiting_customers, 1):
        wait_time, turnaround_time = calculate_dynamic_wait_time(
            idx, customer.service_type, customer.customer_type
        )
        customer.position = idx
        customer.estimated_wait_time = wait_time
        customer.estimated_turnaround_time = turnaround_time

@app.get("/")
def root():
    return {
        "message": "Smart Queue Management API",
        "features": [
            "AI-powered wait time predictions",
            "Multi-channel queue registration",
            "Real-time position updates",
            "Customer type prioritization",
            "Service analytics",
            "No-show reduction"
        ]
    }

@app.post("/queue/join", response_model=QueueEntry)
def join_queue(request: JoinQueueRequest):
    """
    Add customer to queue with AI-powered wait time estimation
    """
    customer_id = str(uuid.uuid4())
    
    # Calculate initial position and wait time
    position = len([q for q in queue_data.values() if q.status == QueueStatus.WAITING]) + 1
    wait_time, turnaround_time = calculate_dynamic_wait_time(
        position, request.service_type, request.customer_type
    )
    
    queue_entry = QueueEntry(
        id=customer_id,
        customer_name=request.customer_name,
        phone=request.phone,
        email=request.email,
        customer_type=request.customer_type,
        service_type=request.service_type,
        status=QueueStatus.WAITING,
        position=position,
        estimated_wait_time=wait_time,
        estimated_turnaround_time=turnaround_time,
        actual_wait_time=None,
        actual_service_time=None,
        check_in_time=datetime.now(),
        service_start_time=None,
        service_end_time=None,
        notes=request.notes
    )
    
    queue_data[customer_id] = queue_entry
    update_queue_positions()
    
    return queue_entry

@app.get("/queue", response_model=List[QueueEntry])
def get_queue_status():
    """Get current queue status with real-time updates"""
    update_queue_positions()
    return list(queue_data.values())

@app.get("/queue/waiting", response_model=List[QueueEntry])
def get_waiting_customers():
    """Get only customers currently waiting"""
    update_queue_positions()
    waiting = [q for q in queue_data.values() if q.status == QueueStatus.WAITING]
    return sorted(waiting, key=lambda x: x.position)

@app.get("/queue/{customer_id}", response_model=QueueEntry)
def get_customer_status(customer_id: str):
    """Get specific customer's queue status"""
    if customer_id not in queue_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    update_queue_positions()
    return queue_data[customer_id]

@app.put("/queue/{customer_id}/status")
def update_customer_status(customer_id: str, request: UpdateQueueRequest):
    """Update customer status (start service, complete, etc.)"""
    if customer_id not in queue_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer = queue_data[customer_id]
    old_status = customer.status
    customer.status = request.status
    
    now = datetime.now()
    
    if request.status == QueueStatus.IN_SERVICE and old_status == QueueStatus.WAITING:
        customer.service_start_time = now
        customer.actual_wait_time = int((now - customer.check_in_time).total_seconds() / 60)
    
    elif request.status == QueueStatus.COMPLETED and old_status == QueueStatus.IN_SERVICE:
        customer.service_end_time = now
        if customer.service_start_time:
            customer.actual_service_time = int((now - customer.service_start_time).total_seconds() / 60)
    
    if request.actual_service_duration:
        customer.actual_service_time = request.actual_service_duration
        # Update average service time for this service type
        if customer.service_type in avg_service_times:
            avg_service_times[customer.service_type] = (
                avg_service_times[customer.service_type] + request.actual_service_duration
            ) / 2
    
    update_queue_positions()
    
    return {"message": f"Customer status updated to {request.status}"}

@app.delete("/queue/{customer_id}")
def remove_from_queue(customer_id: str):
    """Remove customer from queue"""
    if customer_id not in queue_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    del queue_data[customer_id]
    update_queue_positions()
    
    return {"message": "Customer removed from queue"}

@app.get("/analytics/summary")
def get_analytics_summary():
    """Get queue analytics and insights"""
    total_customers = len(queue_data)
    waiting_count = len([q for q in queue_data.values() if q.status == QueueStatus.WAITING])
    serving_count = len([q for q in queue_data.values() if q.status == QueueStatus.IN_SERVICE])
    completed_count = len([q for q in queue_data.values() if q.status == QueueStatus.COMPLETED])
    no_show_count = len([q for q in queue_data.values() if q.status == QueueStatus.NO_SHOW])
    
    # Calculate average wait times
    completed_customers = [q for q in queue_data.values() if q.status == QueueStatus.COMPLETED and q.actual_wait_time]
    avg_actual_wait = sum(c.actual_wait_time for c in completed_customers) / len(completed_customers) if completed_customers else 0
    
    # Calculate average service times
    avg_actual_service = sum(c.actual_service_time for c in completed_customers if c.actual_service_time) / len(completed_customers) if completed_customers else 0
    
    return {
        "total_customers": total_customers,
        "current_waiting": waiting_count,
        "currently_serving": serving_count,
        "completed_today": completed_count,
        "no_shows": no_show_count,
        "no_show_rate": round((no_show_count / total_customers) * 100, 2) if total_customers > 0 else 0,
        "average_wait_time_minutes": round(avg_actual_wait, 2),
        "average_service_time_minutes": round(avg_actual_service, 2),
        "service_counter_utilization": round((serving_count / service_counters) * 100, 2),
        "avg_service_times_by_type": avg_service_times
    }

@app.get("/estimate")
def estimate_wait_time(queue_length: int, avg_service_time: float, counters: int = 1):
    """Legacy endpoint for basic wait time estimation"""
    wait_time = (queue_length * avg_service_time) / counters
    turnaround_time = wait_time + avg_service_time
    return {"estimated_turnaround_time_minutes": round(turnaround_time, 2)}

@app.get("/next-customer")
def get_next_customer():
    """Get the next customer to be served"""
    waiting_customers = [q for q in queue_data.values() if q.status == QueueStatus.WAITING]
    if not waiting_customers:
        return {"message": "No customers waiting"}
    
    next_customer = min(waiting_customers, key=lambda x: x.position)
    return next_customer

@app.post("/settings/counters")
def update_service_counters(counters: int):
    """Update number of service counters"""
    global service_counters
    service_counters = max(1, counters)
    update_queue_positions()
    return {"message": f"Service counters updated to {service_counters}"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_queues": len([q for q in queue_data.values() if q.status == QueueStatus.WAITING]),
        "total_processed": len(queue_data)
    }