from functools import wraps

from api.config import Config
from dotenv import load_dotenv
from flask import Flask, abort, current_app, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

# Load environment variables from .env
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


# Models
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_address = db.Column(db.String(42), nullable=False, index=True)
    original_asset = db.Column(db.String(10), nullable=False)
    original_amount = db.Column(db.Numeric, nullable=False)
    usdc_amount = db.Column(db.Numeric, nullable=False)
    lock_duration_weeks = db.Column(db.Integer, nullable=False)
    transaction_hash = db.Column(db.String(66), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_address": self.user_address,
            "original_asset": self.original_asset,
            "original_amount": float(self.original_amount),
            "usdc_amount": float(self.usdc_amount),
            "lock_duration_weeks": self.lock_duration_weeks,
            "transaction_hash": self.transaction_hash,
            "timestamp": self.timestamp.isoformat(),
        }


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid."}), 401

        token = auth_header.split(" ")[1]

        # Check if token is valid
        if token != current_app.config["AUTH_TOKEN"]:
            return jsonify({"error": "Invalid token."}), 403

        return f(*args, **kwargs)

    return decorated_function


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    @app.route("/api/transactions", methods=["POST"])
    @token_required
    def add_transaction():
        """
        Add a new transaction to the database.
        Expected JSON payload:
        {
            "user_address": "0xUserAddress",
            "original_asset": "ETH",
            "original_amount": 1.5,
            "usdc_amount": 3000,
            "lock_duration_weeks": 12,
            "transaction_hash": "0xTransactionHash"
        }
        """
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload."}), 400

        required_fields = [
            "user_address",
            "original_asset",
            "original_amount",
            "usdc_amount",
            "lock_duration_weeks",
            "transaction_hash",
        ]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return (
                jsonify(
                    {"error": f'Missing required fields: {", ".join(missing_fields)}.'}
                ),
                400,
            )

        # Input Validation
        user_address = data.get("user_address")
        original_asset = data.get("original_asset")
        original_amount = data.get("original_amount")
        usdc_amount = data.get("usdc_amount")
        lock_duration_weeks = data.get("lock_duration_weeks")
        transaction_hash = data.get("transaction_hash")

        # Validate user_address format (basic check)
        if (
            not isinstance(user_address, str)
            or not user_address.startswith("0x")
            or len(user_address) != 42
        ):
            return jsonify({"error": "Invalid user_address format."}), 400

        # Validate original_asset
        if not isinstance(original_asset, str) or len(original_asset) > 10:
            return jsonify({"error": "Invalid original_asset format."}), 400

        # Validate amounts
        try:
            original_amount = float(original_amount)
            usdc_amount = float(usdc_amount)
            if original_amount < 0 or usdc_amount < 0:
                raise ValueError
        except (ValueError, TypeError):
            return (
                jsonify(
                    {
                        "error": "original_amount and usdc_amount must be positive numbers."
                    }
                ),
                400,
            )

        # Validate lock_duration_weeks
        try:
            lock_duration_weeks = int(lock_duration_weeks)
            if lock_duration_weeks <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return (
                jsonify({"error": "lock_duration_weeks must be a positive integer."}),
                400,
            )

        # Validate transaction_hash format (basic check)
        if (
            not isinstance(transaction_hash, str)
            or not transaction_hash.startswith("0x")
            or len(transaction_hash) != 66
        ):
            return jsonify({"error": "Invalid transaction_hash format."}), 400

        # Create Transaction object
        transaction = Transaction(
            user_address=user_address,
            original_asset=original_asset,
            original_amount=original_amount,
            usdc_amount=usdc_amount,
            lock_duration_weeks=lock_duration_weeks,
            transaction_hash=transaction_hash,
        )

        try:
            db.session.add(transaction)
            db.session.commit()
            return jsonify(transaction.to_dict()), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Transaction with this hash already exists."}), 409
        except Exception as e:
            db.session.rollback()
            return (
                jsonify({"error": "An error occurred while adding the transaction."}),
                500,
            )

    @app.route("/api/users/<string:user_address>/transactions", methods=["GET"])
    def get_user_transactions(user_address):
        """
        Retrieve all transactions for a specific user.
        Optional query parameters:
        - page: Page number for pagination (default: 1)
        - per_page: Transactions per page (default: 10)
        """
        # Validate user_address format (basic check)
        if not user_address.startswith("0x") or len(user_address) != 42:
            return jsonify({"error": "Invalid user_address format."}), 400

        # Pagination parameters
        try:
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))
            if page <= 0 or per_page <= 0:
                raise ValueError
        except ValueError:
            return (
                jsonify({"error": "page and per_page must be positive integers."}),
                400,
            )

        # Query transactions
        transactions_query = Transaction.query.filter_by(
            user_address=user_address
        ).order_by(desc(Transaction.timestamp))
        pagination = transactions_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        transactions = [tx.to_dict() for tx in pagination.items]

        response = {
            "user_address": user_address,
            "page": page,
            "per_page": per_page,
            "total_transactions": pagination.total,
            "total_pages": pagination.pages,
            "transactions": transactions,
        }

        return jsonify(response), 200

    @app.route("/api/transactions/<string:tx_hash>", methods=["GET"])
    def get_transaction(tx_hash):
        """
        Retrieve a specific transaction by its hash.
        """
        # Validate tx_hash format (basic check)
        if not tx_hash.startswith("0x") or len(tx_hash) != 66:
            return jsonify({"error": "Invalid transaction_hash format."}), 400

        transaction = Transaction.query.filter_by(transaction_hash=tx_hash).first()
        if not transaction:
            return jsonify({"error": "Transaction not found."}), 404

        return jsonify(transaction.to_dict()), 200

    @app.route("/api/transactions", methods=["GET"])
    def get_all_transactions():
        """
        Retrieve all transactions.
        Optional query parameters:
        - page: Page number for pagination (default: 1)
        - per_page: Transactions per page (default: 10)
        """
        # Pagination parameters
        try:
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))
            if page <= 0 or per_page <= 0:
                raise ValueError
        except ValueError:
            return (
                jsonify({"error": "page and per_page must be positive integers."}),
                400,
            )

        transactions_query = Transaction.query.order_by(desc(Transaction.timestamp))
        pagination = transactions_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        transactions = [tx.to_dict() for tx in pagination.items]

        response = {
            "page": page,
            "per_page": per_page,
            "total_transactions": pagination.total,
            "total_pages": pagination.pages,
            "transactions": transactions,
        }

        return jsonify(response), 200

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed."}), 405

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error."}), 500

    with app.app_context():
        db.create_all()

    return app


# Entry Point
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001)
