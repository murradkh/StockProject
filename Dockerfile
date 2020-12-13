FROM python:3.8
RUN mkdir -p /home/StockProject
WORKDIR /home/StockProject/
COPY . .
RUN pip install -r requirements.txt
