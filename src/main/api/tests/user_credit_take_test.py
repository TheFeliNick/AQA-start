import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest


@pytest.mark.api
class TestUserTakeCredit:
    def test_user_take_credit(self,db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, user_credit_take_request_valid):

        response = api_manager.user_steps.credit_take(create_credit_user_request, user_credit_take_request_valid)
        assert response.amount == 5000

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, response.creditId)

        assert credit_from_db is not None, "Кредит не найден в БД"
        assert credit_from_db.id == response.creditId
        assert credit_from_db.account_id == user_credit_take_request_valid.accountId
        assert credit_from_db.amount == response.amount
        assert credit_from_db.term_months == response.termMonths
        assert credit_from_db.balance == -response.amount


    def test_user_take_credit_invalid(self,db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, user_credit_take_request_invalid):

        response = api_manager.user_steps.credit_take_invalid(create_credit_user_request, user_credit_take_request_invalid)
        assert response.status_code == 400

        assert response.status_code == 400

        account_from_db = AccountCrudDb.get_account_by_id(db_session, user_credit_take_request_invalid.accountId)
        credit_from_db = CreditCrudDb.get_last_credit_by_account_id(db_session, user_credit_take_request_invalid.accountId)

        assert account_from_db is not None, "Аккаунт не найден в БД"
        assert account_from_db.id == user_credit_take_request_invalid.accountId
        assert account_from_db.balance == 0, "Баланс аккаунта изменился после невалидного кредита"

        assert credit_from_db is None, "Кредит создался после невалидного запроса"

