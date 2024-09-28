FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the transaction monitor script is executable
RUN chmod +x run_transaction_monitor.sh

EXPOSE 5000

CMD ["python", "api/app.py"]
