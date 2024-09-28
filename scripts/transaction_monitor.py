import random
from api.app import create_app, db, Transaction

from sqlalchemy.exc import IntegrityError


def simulate_transactions():
    # todo: implement ethscanner to parse all transactions.
    app = create_app()
    with app.app_context():
        # Hardcoded transaction data
        transactions = [
            {
                "user_address": "0xab5801a7d398351b8be11c439e05c5b3259aec9b",
                "original_asset": "ETH",
                "original_amount": 1.5,
                "usdc_amount": 3000,
                "lock_duration_weeks": 12,
                "transaction_hash": "0x"
                + "".join(random.choices("abcdef1234567890", k=64)),
            },
            {
                "user_address": "0x5abfec25f74cd88437631a7731906932776356f9",
                "original_asset": "DAI",
                "original_amount": 200,
                "usdc_amount": 200,
                "lock_duration_weeks": 24,
                "transaction_hash": "0x"
                + "".join(random.choices("abcdef1234567890", k=64)),
            },
        ]

        for txn_data in transactions:
            transaction = Transaction(
                user_address=txn_data["user_address"],
                original_asset=txn_data["original_asset"],
                original_amount=txn_data["original_amount"],
                usdc_amount=txn_data["usdc_amount"],
                lock_duration_weeks=txn_data["lock_duration_weeks"],
                transaction_hash=txn_data["transaction_hash"],
            )
            try:
                db.session.add(transaction)
                db.session.commit()
                print(f"Transaction {transaction.transaction_hash} added.")
            except IntegrityError:
                db.session.rollback()
                print(f"Transaction {transaction.transaction_hash} already exists.")


if __name__ == "__main__":
    simulate_transactions()
