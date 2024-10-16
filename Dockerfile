FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

RUN python3 -m pip install poetry

RUN poetry install

ENTRYPOINT ["poetry", "run", "streamlit", "run", "ipf_examples/Examples_Home.py", "--server.port=80", "--server.address=0.0.0.0", "--theme.primaryColor=#8C989B", "--theme.backgroundColor=#264183", "--theme.secondaryBackgroundColor=#222D32", "--theme.textColor=#F6F6F6", "--theme.font=monospace"]
