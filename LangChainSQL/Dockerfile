FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install dependencies with retries
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --timeout=300 --retries=5 -r requirements.txt

# Copy application files (not .env - pass API key via environment variable)
COPY app.py .
COPY parking_sessions.csv .

# Environment variable for OpenAI API key (pass at runtime with -e)
ENV OPENAI_API_KEY=""

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
