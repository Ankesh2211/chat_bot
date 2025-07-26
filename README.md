## RAG Chatbot

### Setup
```bash
git clone <repo>
cd chat_bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### To Ingest Data
```bash
python load_document.py --path <path of pdf or docx file>
```

### To Run (CLI)
```bash
python app/main.py
```

### To Run (UI)
```bash
streamlit run app/docker_main.py
```

### To Run with Docker
```bash
docker-compose up --build
```

### To View GRAFANA metrics:
To Obtain prometheus container name:
```
docker ps -a
```
Get the IP of prometheus in docker container using the below command
```
docker inspect <prometheus container name>
```
Open graphana dashboard which is running on localhost:3000

