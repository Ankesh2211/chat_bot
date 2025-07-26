FROM python:3.11-bullseye


WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app/ui.py", "--server.port=8000", "--server.enableCORS=false"]