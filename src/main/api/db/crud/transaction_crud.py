from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_last_transaction_by_to_account_id(db: Session, account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=account_id).order_by(Transaction.id.desc()).first()

    @staticmethod
    def get_last_transaction_by_credit_id_and_type(db: Session, credit_id: int, transaction_type: str) -> Transaction | None:
        return db.query(Transaction).filter_by(credit_id=credit_id, transaction_type=transaction_type).order_by(Transaction.id.desc()).first()