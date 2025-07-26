## RAG Chatbot
Note: makesure you have internet connection
Note: python version: 3.11.1
### Setup
```bash
git clone <repo>
cd chat_bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### OpenAI API key setup
Please provide openAI API key in .env file in this directory.
Below is the format of .env
```bash
OPENAI_API_KEY=<api key>
```

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

