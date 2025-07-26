## RAG Chatbot
Note: makesure you have internet connection
Note: python version: 3.11.1
### Setup
```bash
git clone <repo>
cd chat_bot
python -m venv venv
source venv/bin/activate
pip install -r local_requirements.txt
```
### OpenAI API key setup
Please provide openAI API key in .env file in this directory.
Below is the format of .env
```bash
OPENAI_API_KEY=<api key>
```
Note: You need to ingest data into chromaDB before running UI on local PC or using Docker.
### To Ingest Data
```bash
python load_document.py --path <path of pdf or docx file>
```

### To Run (UI)
```bash
streamlit run app/main.py
```

### To Run with Docker
Makesure docker engine is running using the below command
```bash
docker version
```

If it is not running, just open docker desktop in your PC, so that docker engine will starts.

Next build and run the docker container using below command:
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
username: admin
password: admin

1. Go to Data Sources.
2. Click on Add Data Source .
3. Click on prometheus.
4. Enter Prometheus Server Url as: http://<prometheus_ip>:9090

Now Visualize Dashboards using following steps:
1. Click on DashBoards.
2. Click on create dashboard.
3. Click on add Visualization.
4. Select prometheus.
5. Query the required metric.

