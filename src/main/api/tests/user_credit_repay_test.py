import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest


@pytest.mark.api
class TestUserRepayCredit:
    def test_user_repay_credit(self,db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, credit_taken_response, user_credit_repay_request_valid):

        response = api_manager.user_steps.credit_repay(create_credit_user_request, user_credit_repay_request_valid)
        assert response.amountDeposited == 5000

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, user_credit_repay_request_valid.creditId)
        transaction_from_db = TransactionCrudDb.get_last_transaction_by_credit_id_and_type(db_session, user_credit_repay_request_valid.creditId, "credit_repayment")

        assert credit_from_db is not None, "Кредит не найден в БД"

        assert transaction_from_db is not None, "Транзакция погашения кредита не найдена в БД"
        assert transaction_from_db.credit_id == user_credit_repay_request_valid.creditId
        assert transaction_from_db.amount == user_credit_repay_request_valid.amount
        assert transaction_from_db.transaction_type == "credit_repayment"

    def test_user_repay_credit_invalid(self,db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, credit_taken_response, user_credit_repay_request_invalid):

        response = api_manager.user_steps.credit_repay_invalid(create_credit_user_request, user_credit_repay_request_invalid)
        assert response.status_code == 422

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, user_credit_repay_request_invalid.creditId)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, user_credit_repay_request_invalid.accountId)

        assert credit_from_db is not None, "Кредит не найден в БД"
        assert credit_from_db.id == user_credit_repay_request_invalid.creditId
        assert credit_from_db.balance == -5000, "Баланс кредита изменился после невалидного погашения"

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.id == user_credit_repay_request_invalid.accountId
        assert account_from_db.balance == 5000, "Баланс аккаунта изменился после невалидного погашения"



