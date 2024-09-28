# Project README

## Overview

This project provides the **backend implementation** for a crypto-based website, allowing users to deposit funds and earn boosted liquidity for an upcoming project.

### Key Features:

- **User Deposits**: Users can deposit cryptocurrencies and select a lock period.
- **Asset Swap**: Deposited assets are swapped to USDC via Uniswap.
- **Transaction Monitoring**: Backend monitors transactions and stores them in the database.
- **API Endpoints**: Provides RESTful API endpoints for transactions.
- **Testing**: Includes a comprehensive test suite using `pytest`.

## Table of Contents

- [Project README](#project-readme)
  - [Overview](#overview)
    - [Key Features:](#key-features)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
    - [Clone the Repository](#clone-the-repository)
    - [Set Up Virtual Environment](#set-up-virtual-environment)
    - [Install Dependencies](#install-dependencies)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
    - [Using Docker Compose](#using-docker-compose)
  - [Running Tests](#running-tests)
  - [Testing the API](#testing-the-api)
    - [Using Curl](#using-curl)
      - [Set the Authentication Token](#set-the-authentication-token)
      - [Add a Transaction](#add-a-transaction)
      - [Get All Transactions](#get-all-transactions)
      - [Get a Transaction by Hash](#get-a-transaction-by-hash)
      - [Get Transactions by User Address](#get-transactions-by-user-address)
  - [Project Structure](#project-structure)
  - [License](#license)

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.9 or higher**
- **Docker** and **Docker Compose**
- **Git**

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### Set Up Virtual Environment

It's recommended to use a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root directory with the following content:

```dotenv
FLASK_APP=api.app
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@db:5432/yourdb
TEST_DATABASE_URL=sqlite:///:memory:
ETHERSCAN_API_KEY=your_etherscan_api_key
GNOSIS_SAFE_ADDRESS=your_gnosis_safe_address
INFURA_URL=https://mainnet.infura.io/v3/your_infura_project_id
AUTH_TOKEN=mysecrettoken
```

- **Note**: Replace placeholder values with actual credentials.
- **Important**: Do not commit `.env` to version control.

---

## Running the Application

### Using Docker Compose

The application is containerized using Docker. Follow these steps to run it:

1. **Build and Run the Containers**

   ```bash
   docker-compose up --build
   ```

   This command:

   - Builds the Docker images.
   - Starts the following services:
     - **web**: Flask API server.
     - **db**: PostgreSQL database.
     - **transaction_monitor**: Simulates transaction monitoring.

2. **Check the Services**

   - **API Endpoint**: The API should be running at `http://localhost:5001`.
   - **Database**: PostgreSQL is running inside a Docker container.

3. **Verify Database Initialization**

   - The database tables are automatically created on startup using Flask-Migrate.

---

## Running Tests

To run unit tests using `pytest`:

1. **Activate the Virtual Environment**

   ```bash
   source venv/bin/activate
   ```

2. **Install Test Dependencies**

   Ensure all packages are installed:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Tests**

   ```bash
   pytest
   ```

   - This command discovers and runs all tests in the `api/tests` directory.

---

## Testing the API

### Using Curl

You can test the API endpoints using `curl`.

#### Set the Authentication Token

Export the `AUTH_TOKEN` (must match the one in your `.env` file):

```bash
export AUTH_TOKEN=mysecrettoken
```

#### Add a Transaction

```bash
curl -X POST http://localhost:5001/api/transactions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $AUTH_TOKEN" \
     -d '{
           "user_address": "0x1234567890abcdef1234567890abcdef12345678",
           "original_asset": "ETH",
           "original_amount": 1.5,
           "usdc_amount": 3000,
           "lock_duration_weeks": 12,
           "transaction_hash": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef"
         }'
```

- **Response**: Should return a `201 Created` status with the transaction details.

#### Get All Transactions

```bash
curl http://localhost:5001/api/transactions
```

- **Response**: Returns a list of all transactions.

#### Get a Transaction by Hash

```bash
curl http://localhost:5001/api/transactions/0xabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef
```

- **Response**: Returns the details of the specified transaction.

#### Get Transactions by User Address

```bash
curl http://localhost:5001/api/users/0x1234567890abcdef1234567890abcdef12345678/transactions
```

- **Response**: Returns all transactions for the specified user.

---

## Project Structure

```
yourproject/
├── api/
│   ├── __init__.py
│   ├── app.py                  # Main Flask application
│   ├── config.py               # Configuration settings
│   └── tests/                  # Unit tests
│       ├── __init__.py
│       └── test_app.py
├── scripts/
│   ├── transaction_monitor.py  # Simulates transaction monitoring
│   └── database_setup.py       # Database initialization script
├── .env                        # Environment variables (not in version control)
├── .gitignore                  # Files to ignore in Git
├── Dockerfile                  # Docker image instructions
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
├── run_transaction_monitor.sh  # Script to run transaction monitor
└── README.md                   # Project documentation
```

---

## License

This project is licensed under the **MIT License**.

---

Thank you for using our backend system! If you have any questions or need further assistance, please feel free to reach out.
