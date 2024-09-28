#!/bin/bash

# Set the working directory to /app
cd /app

# Infinite loop to run the transaction monitor every 5 seconds
while true; do
    python scripts/transaction_monitor.py
    sleep 5
done
