import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.fixtures.user_fixture import create_account_response
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest



@pytest.mark.api
class TestUserDeposit:
    def test_deposit_account_valid(self,db_session: Session, api_manager: ApiManager, create_account_response: CreateAccountResponse, user_deposit_request_valid, create_user_request: CreateUserRequest):

        response = api_manager.user_steps.deposit(create_user_request, user_deposit_request_valid)
        assert response.id == create_account_response.id

        account_from_db = Account.get_account_by_id(db_session, response.id)
        transaction_from_db = TransactionCrudDb.get_last_transaction_by_to_account_id(db_session,response.id)

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.id == response.id, "Аккаунт не создан, id аккаунта нет в БД"
        assert account_from_db.balance == response.balance, "Счет не был пополнен"

        assert transaction_from_db.transaction_type == "deposit"


    def test_deposit_account_invalid(self, db_session: Session, api_manager: ApiManager, user_deposit_request_invalid,create_account_response: CreateAccountResponse, create_user_request: CreateUserRequest):

        response = api_manager.user_steps.deposit_invalid(create_user_request, user_deposit_request_invalid)
        assert response.status_code == 400

        account_from_db = Account.get_account_by_id(db_session, create_account_response.id)
        transaction_from_db = TransactionCrudDb.get_last_transaction_by_to_account_id(db_session, create_account_response.id)

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.id == create_account_response.id, "Аккаунт не создан, id аккаунта нет в БД"
        assert account_from_db.balance == 0, "Неисправно пополнение счета"

        assert transaction_from_db is None, "Транзакция создалась после невалидного пополнения"