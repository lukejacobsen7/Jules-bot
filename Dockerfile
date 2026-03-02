FROM node:20-slim

RUN apt-get update && apt-get install -y python3 python3-pip --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g @google/jules

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --break-system-packages
COPY bot.py .

CMD ["python3", "bot.py"]
