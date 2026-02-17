# Parking Sessions Analytics & AI Assistant

A generative AI application that allows users to ask natural language questions about parking session data. Built with Streamlit, LangChain, and OpenAI.

## Purpose

This application provides:

- **Interactive Dashboard**: Visual analytics with KPIs and charts showing parking revenue, session trends, and facility performance across NYC districts
- **AI-Powered Chatbot**: Natural language interface to query parking data using LangChain's Pandas DataFrame Agent powered by OpenAI

## Features

### Dashboard (Left Panel)
- Total Revenue, Total Sessions, Average Duration, Unique Vehicles (KPIs)
- Revenue by District (bar chart)
- Sessions by Hour (trend line)
- Top 10 Facilities by Revenue
- Sessions by License Plate State (pie chart)

### AI Chatbot (Right Panel)
- Ask questions in plain English about the parking data
- Powered by OpenAI GPT model via LangChain
- Sample questions provided for quick start

## Data

The application analyzes `parking_sessions.csv` containing:
- Session details (ID, timestamps, duration)
- Facility information (name, district)
- Pricing (hourly rate, total cost)
- Vehicle information (license plate, state)

## Prerequisites

- Docker (recommended) or Python 3.11+
- OpenAI API key

## Deployment

### Option 1: Docker (Recommended)

1. **Clone/download the project files**

2. **Set your OpenAI API key** in the `.env` file:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

3. **Build the Docker image**:
   ```bash
   docker build -t parking-analytics .
   ```

4. **Run the container**:
   ```bash
   docker run -d --name parking-app -p 8510:8501 --env-file .env parking-analytics
   ```

5. **Access the application**: http://localhost:8510

#### Docker Commands Reference

```bash
# Stop the container
docker stop parking-app

# Start the container
docker start parking-app

# View logs
docker logs parking-app

# Remove container
docker rm -f parking-app

# Rebuild after code changes
docker rm -f parking-app
docker build -t parking-analytics .
docker run -d --name parking-app -p 8510:8501 --env-file .env parking-analytics
```

### Option 2: Local Python Environment

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key** in the `.env` file:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the application**: http://localhost:8501

## Example Questions

- "What is the total revenue?"
- "Which district has the most parking sessions?"
- "What's the average cost per session in Manhattan?"
- "Top 5 facilities by number of sessions?"
- "How many vehicles from NJ parked here?"
- "What's the busiest hour for parking?"

## Project Structure

```
.
├── app.py                 # Main Streamlit application
├── parking_sessions.csv   # Parking session data
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker build exclusions
├── .env                  # Environment variables (API key)
└── README.md             # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

## Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **AI/LLM**: LangChain, OpenAI (gpt-4o-mini)
- **Data**: Pandas
- **Containerization**: Docker
