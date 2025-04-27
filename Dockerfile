FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project (including main.py)
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app (THIS is the key part you were missing)
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
