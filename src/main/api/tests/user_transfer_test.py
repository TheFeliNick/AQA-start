import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.api_fixture import api_manager



@pytest.mark.api
class TestUserTransfer:
    def test_transfer(self,db_session: Session, api_manager: ApiManager, transfer_valid):

        response = api_manager.user_steps.transfer_data_prepared(transfer_valid)
        assert response.fromAccountIdBalance == 500

        account_from_db = Account.get_account_by_id(db_session, response.fromAccountId)
        account_to_db = Account.get_account_by_id(db_session, response.toAccountId)
        transaction_from_db = TransactionCrudDb.get_last_transaction_by_to_account_id(db_session, response.toAccountId)

        assert account_from_db is not None, "Счёт списания не найден в БД"
        assert account_to_db is not None, "Счёт зачисления не найден в БД"

        assert account_from_db.balance == 500, "Баланс счёта списания неверный"
        assert account_to_db.balance == 1500, "Баланс счёта зачисления неверный"

        assert transaction_from_db is not None, "Транзакция перевода не найдена в БД"
        assert transaction_from_db.from_account_id == response.fromAccountId
        assert transaction_from_db.to_account_id == response.toAccountId
        assert transaction_from_db.amount == response.fromAccountIdBalance
        assert transaction_from_db.transaction_type == "transfer"


    def test_transfer_invalid(self,db_session: Session,  api_manager:ApiManager, transfer_invalid):

        response = api_manager.user_steps.transfer_data_prepared_invalid(transfer_invalid)
        assert response.status_code == 400

        transfer_request = transfer_invalid["transfer_request"]

        account_from_db = Account.get_account_by_id(db_session, transfer_request.fromAccountId)
        account_to_db = Account.get_account_by_id(db_session, transfer_request.toAccountId)

        assert account_from_db is not None, "Счёт списания не найден в БД"
        assert account_to_db is not None, "Счёт зачисления не найден в БД"

        assert account_from_db.balance == 1000, "Баланс счёта списания изменился после невалидного перевода"
        assert account_to_db.balance == 1000, "Баланс счёта зачисления изменился после невалидного перевода"
