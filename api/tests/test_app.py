# ./api/tests/test_app.py

import pytest
from api.app import create_app, db
from api.config import TestConfig
from api.app import Transaction


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_add_transaction_no_token(client):
    transaction_data = {
        "user_address": "0x1234567890abcdef1234567890abcdef12345678",
        "original_asset": "ETH",
        "original_amount": 1.5,
        "usdc_amount": 3000,
        "lock_duration_weeks": 12,
        "transaction_hash": "0x" + "g" * 64,
    }
    response = client.post("/api/transactions", json=transaction_data)
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Authorization header missing or invalid."


def test_add_transaction_invalid_token(client):
    transaction_data = {
        "user_address": "0x1234567890abcdef1234567890abcdef12345678",
        "original_asset": "ETH",
        "original_amount": 1.5,
        "usdc_amount": 3000,
        "lock_duration_weeks": 12,
        "transaction_hash": "0x" + "h" * 64,
    }
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 403
    data = response.get_json()
    assert data["error"] == "Invalid token."


def test_add_transaction(client):
    transaction_data = {
        "user_address": "0x1234567890abcdef1234567890abcdef12345678",
        "original_asset": "ETH",
        "original_amount": 1.5,
        "usdc_amount": 3000,
        "lock_duration_weeks": 12,
        "transaction_hash": "0x" + "a" * 64,  # 64 hex characters
    }
    headers = {"Authorization": "Bearer testsecrettoken"}
    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data["user_address"] == transaction_data["user_address"]
    assert data["original_asset"] == transaction_data["original_asset"]
    assert data["original_amount"] == transaction_data["original_amount"]
    assert data["usdc_amount"] == transaction_data["usdc_amount"]
    assert data["lock_duration_weeks"] == transaction_data["lock_duration_weeks"]
    assert data["transaction_hash"] == transaction_data["transaction_hash"]


def test_get_transaction(client):
    # First, add a transaction to the database
    transaction = Transaction(
        user_address="0x1234567890abcdef1234567890abcdef12345678",
        original_asset="ETH",
        original_amount=1.5,
        usdc_amount=3000,
        lock_duration_weeks=12,
        transaction_hash="0x" + "a" * 64,
    )
    with client.application.app_context():
        db.session.add(transaction)
        db.session.commit()
        # Access transaction_hash within the same context
        tx_hash = transaction.transaction_hash

    # Now retrieve the transaction
    response = client.get(f"/api/transactions/{tx_hash}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["user_address"] == transaction.user_address
    assert data["original_asset"] == transaction.original_asset
    assert data["original_amount"] == float(transaction.original_amount)
    assert data["usdc_amount"] == float(transaction.usdc_amount)
    assert data["lock_duration_weeks"] == transaction.lock_duration_weeks
    assert data["transaction_hash"] == transaction.transaction_hash


def test_get_user_transactions(client):
    # Add multiple transactions for the same user
    user_address = "0x1234567890abcdef1234567890abcdef12345678"
    transactions = [
        Transaction(
            user_address=user_address,
            original_asset="ETH",
            original_amount=1.5,
            usdc_amount=3000,
            lock_duration_weeks=12,
            transaction_hash="0x" + "a" * 64,  # 64 hex characters after "0x"
        ),
        Transaction(
            user_address=user_address,
            original_asset="DAI",
            original_amount=200,
            usdc_amount=200,
            lock_duration_weeks=24,
            transaction_hash="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        ),
    ]
    with client.application.app_context():
        for txn in transactions:
            db.session.add(txn)
        db.session.commit()

    # Now retrieve transactions for the user
    response = client.get(f"/api/users/{user_address}/transactions")
    assert response.status_code == 200
    data = response.get_json()
    assert data["user_address"] == user_address
    assert data["total_transactions"] == 2
    assert len(data["transactions"]) == 2


def test_get_all_transactions(client):
    # Add multiple transactions
    transactions = [
        Transaction(
            user_address="0x1234567890abcdef1234567890abcdef12345678",
            original_asset="ETH",
            original_amount=1.5,
            usdc_amount=3000,
            lock_duration_weeks=12,
            transaction_hash="0x" + "a" * 64,  # 64 hex characters after "0x"
        ),
        Transaction(
            user_address="0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef",
            original_asset="DAI",
            original_amount=200,
            usdc_amount=200,
            lock_duration_weeks=24,
            transaction_hash="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        ),
    ]
    with client.application.app_context():
        for txn in transactions:
            db.session.add(txn)
        db.session.commit()

    # Now retrieve all transactions
    response = client.get("/api/transactions")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total_transactions"] == 2
    assert len(data["transactions"]) == 2


# Additional tests can be added to cover edge cases, validation errors, etc.


def test_add_transaction_missing_fields(client):
    # Test adding a transaction with missing required fields
    transaction_data = {
        "user_address": "0x1234567890abcdef1234567890abcdef12345678",
        # "original_asset": "ETH",  # Missing field
        "original_amount": 1.5,
        "usdc_amount": 3000,
        "lock_duration_weeks": 12,
        "transaction_hash": "0x" + "b" * 64,
    }
    headers = {"Authorization": "Bearer testsecrettoken"}
    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required fields" in data["error"]
    assert "original_asset" in data["error"]


def test_add_transaction_invalid_user_address(client):
    # Test invalid user_address format
    transaction_data = {
        "user_address": "InvalidAddress",
        "original_asset": "ETH",
        "original_amount": 1.5,
        "usdc_amount": 3000,
        "lock_duration_weeks": 12,
        "transaction_hash": "0x" + "c" * 64,
    }
    headers = {"Authorization": "Bearer testsecrettoken"}
    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Invalid user_address format."


def test_add_transaction_duplicate_hash(client):
    # Test adding a transaction with a duplicate transaction_hash
    transaction_data = {
        "user_address": "0x1234567890abcdef1234567890abcdef12345678",
        "original_asset": "ETH",
        "original_amount": 1.5,
        "usdc_amount": 3000,
        "lock_duration_weeks": 12,
        "transaction_hash": "0x" + "d" * 64,
    }
    # Add the transaction the first time
    headers = {"Authorization": "Bearer testsecrettoken"}
    response1 = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response1.status_code == 201
    # Try adding the same transaction again
    response2 = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response2.status_code == 409
    data = response2.get_json()
    assert data["error"] == "Transaction with this hash already exists."


def test_get_transaction_not_found(client):
    # Test retrieving a transaction that doesn't exist
    tx_hash = "0x" + "e" * 64
    response = client.get(f"/api/transactions/{tx_hash}")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Transaction not found."


def test_get_transaction_invalid_hash(client):
    # Test invalid transaction_hash format
    tx_hash = "InvalidHash"
    response = client.get(f"/api/transactions/{tx_hash}")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Invalid transaction_hash format."


def test_get_user_transactions_invalid_address(client):
    # Test invalid user_address format
    user_address = "InvalidAddress"
    response = client.get(f"/api/users/{user_address}/transactions")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Invalid user_address format."


def test_get_all_transactions_invalid_pagination(client):
    # Test invalid pagination parameters
    response = client.get("/api/transactions?page=-1&per_page=0")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "page and per_page must be positive integers."


def test_method_not_allowed(client):
    # Test method not allowed (e.g., DELETE on /api/transactions)
    response = client.delete("/api/transactions")
    assert response.status_code == 405
    data = response.get_json()
    assert data["error"] == "Method not allowed."


def test_add_transaction_invalid_amounts(client):
    # Test negative amounts
    transaction_data = {
        "user_address": "0x1234567890abcdef1234567890abcdef12345678",
        "original_asset": "ETH",
        "original_amount": -1.5,  # Negative amount
        "usdc_amount": -3000,  # Negative amount
        "lock_duration_weeks": 12,
        "transaction_hash": "0x" + "f" * 64,
    }
    headers = {"Authorization": "Bearer testsecrettoken"}
    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert "original_amount and usdc_amount must be positive numbers." in data["error"]


def test_add_transaction_invalid_lock_duration(client):
    # Test invalid lock_duration_weeks
    transaction_data = {
        "user_address": "0x1234567890abcdef1234567890abcdef12345678",
        "original_asset": "ETH",
        "original_amount": 1.5,
        "usdc_amount": 3000,
        "lock_duration_weeks": 0,  # Invalid duration
        "transaction_hash": "0x" + "1" * 64,
    }
    headers = {"Authorization": "Bearer testsecrettoken"}
    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "lock_duration_weeks must be a positive integer."


def test_add_transaction_invalid_original_asset(client):
    # Test invalid original_asset (too long)
    transaction_data = {
        "user_address": "0x1234567890abcdef1234567890abcdef12345678",
        "original_asset": "TOO_LONG_ASSET_NAME",
        "original_amount": 1.5,
        "usdc_amount": 3000,
        "lock_duration_weeks": 12,
        "transaction_hash": "0x" + "2" * 64,
    }
    headers = {"Authorization": "Bearer testsecrettoken"}
    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Invalid original_asset format."


def test_post_get_transactions_pagination(client):
    # Add multiple transactions to test pagination
    headers = {"Authorization": "Bearer testsecrettoken"}
    for i in range(25):
        transaction_data = {
            "user_address": f"0x{str(i).zfill(40)}",
            "original_asset": "ETH",
            "original_amount": 1.0 + i,
            "usdc_amount": 1000 + i * 10,
            "lock_duration_weeks": 12,
            "transaction_hash": f"0x{str(i).zfill(64)}",
        }
        response = client.post(
            "/api/transactions", json=transaction_data, headers=headers
        )
        assert response.status_code == 201

    # Test pagination for page 2
    response = client.get("/api/transactions?page=2&per_page=10")
    assert response.status_code == 200
    data = response.get_json()
    assert data["page"] == 2
    assert len(data["transactions"]) == 10


def test_get_user_transactions_pagination(client):
    user_address = "0x" + "3" * 40
    headers = {"Authorization": "Bearer testsecrettoken"}
    # Add multiple transactions for the same user
    for i in range(15):
        transaction_data = {
            "user_address": user_address,
            "original_asset": "ETH",
            "original_amount": 1.0 + i,
            "usdc_amount": 1000 + i * 10,
            "lock_duration_weeks": 12,
            "transaction_hash": f"0x{str(i + 100).zfill(64)}",
        }
        response = client.post(
            "/api/transactions", json=transaction_data, headers=headers
        )
        assert response.status_code == 201

    # Test pagination for user's transactions
    response = client.get(f"/api/users/{user_address}/transactions?page=1&per_page=5")
    assert response.status_code == 200
    data = response.get_json()
    assert data["page"] == 1
    assert data["per_page"] == 5
    assert len(data["transactions"]) == 5
    assert data["total_transactions"] == 15
    assert data["total_pages"] == 3
