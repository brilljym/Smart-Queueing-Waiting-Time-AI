# Smart Queue Management System

A comprehensive AI-powered queue management system inspired by Waitwhile, focusing on turnaround time optimization and customer experience enhancement.

## 🌟 Key Features Inspired by Waitwhile

### 1. **Multi-Channel Registration**
- Web-based queue joining
- Customer type prioritization (Walk-in, Appointment, VIP, Returning)
- Service type categorization
- Customer information capture

### 2. **AI-Powered Wait Time Predictions**
- Dynamic wait time calculations based on:
  - Current queue length
  - Service counter utilization
  - Customer type priorities
  - Historical service times
  - Time-of-day patterns (rush hours)
- Real-time turnaround time estimates

### 3. **Real-Time Queue Management**
- Live position updates
- Automatic queue reorganization
- Service counter management
- Customer status tracking (Waiting → In Service → Completed)

### 4. **Customer Experience Features**
- Accurate wait time estimates
- Position tracking
- Service type optimization
- No-show reduction through engagement

### 5. **Analytics & Insights**
- Queue performance metrics
- Average wait times
- Service counter utilization
- No-show rate tracking
- Customer flow analysis

### 6. **Staff Management Tools**
- Next customer alerts
- Service counter configuration
- Customer status management
- Real-time dashboard

## 🚀 API Endpoints

### Queue Management
- `POST /queue/join` - Add customer to queue
- `GET /queue` - Get all queue entries
- `GET /queue/waiting` - Get waiting customers only
- `GET /queue/{customer_id}` - Get specific customer status
- `PUT /queue/{customer_id}/status` - Update customer status
- `DELETE /queue/{customer_id}` - Remove customer from queue

### Analytics & Insights
- `GET /analytics/summary` - Comprehensive queue analytics
- `GET /next-customer` - Get next customer to serve

### Configuration
- `POST /settings/counters` - Update service counter count
- `GET /health` - System health check

### Legacy Support
- `GET /estimate` - Basic wait time estimation

## 📊 Smart Features

### Dynamic Wait Time Calculation
```python
# Factors considered:
- Customer type priority (VIP, Appointment, Returning, Walk-in)
- Service type duration (General, Consultation, Premium, Technical)
- Current queue load and service counter availability
- Time-of-day multipliers (rush hours, lunch time)
- Historical service time learning
```

### Customer Prioritization
- **VIP**: 20% faster service, priority positioning
- **Appointment**: 10% faster service, scheduled optimization
- **Returning**: 15% faster service, familiar process
- **Walk-in**: Standard service timing

### Service Types with AI Learning
- **General Service**: 15 minutes average
- **Consultation**: 30 minutes average
- **Premium Service**: 20 minutes average
- **Technical Support**: 45 minutes average

*System learns and adjusts these times based on actual service completions*

## 🎯 Waitwhile-Inspired Benefits

### For Customers
- **Reduced Wait Times**: AI-powered predictions and virtual queuing
- **Transparency**: Real-time position and wait time updates
- **Flexibility**: Join queue remotely, get accurate estimates
- **Personalization**: Service type and customer type optimization

### For Businesses
- **Increased Efficiency**: Optimized staff allocation and queue flow
- **Better Analytics**: Comprehensive insights into queue performance
- **Reduced No-Shows**: Engaged customers with real-time updates
- **Improved Satisfaction**: Transparent and predictable service experience

### For Staff
- **Easy Management**: Intuitive dashboard for queue oversight
- **Smart Alerts**: Next customer notifications and status updates
- **Resource Optimization**: Service counter utilization tracking
- **Data-Driven Decisions**: Analytics for operational improvements

## 🛠️ Technical Stack

- **Backend**: FastAPI with Python
- **Frontend**: Modern HTML5/CSS3/JavaScript
- **Deployment**: Vercel (serverless)
- **AI/ML**: Custom algorithms for wait time prediction
- **Real-time**: Auto-refresh and live updates

## 📱 Usage

1. **Join Queue**: Customers enter details and get position/wait time
2. **Monitor Status**: Real-time updates on queue position
3. **Staff Management**: Call next customer, update statuses
4. **Analytics**: Track performance and optimize operations

## 🔧 Local Development

```bash
# Install dependencies
pip install -r api/requirements.txt

# Run locally
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Access at http://localhost:8000
```

## 🌐 Deployment

Deploy to Vercel with the included `vercel.json` configuration:

```bash
vercel deploy
```

## 📈 Future Enhancements

- SMS/Email notifications
- Mobile app integration
- Advanced ML prediction models
- Multi-language support
- Calendar integration
- Customer feedback system
- Advanced reporting and forecasting

---

*Transform waiting into a positive experience with AI-powered queue management!*