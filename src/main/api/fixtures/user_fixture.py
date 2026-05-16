import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.account_credit_repay_request import AccountCreditRepayRequest
from src.main.api.models.account_credit_take_request import AccountCreditTakeRequest
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.user_deposit_request import UserDepositRequest


@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)
    return user_request

@pytest.fixture
def create_account_response(api_manager, create_user_request):
    return api_manager.user_steps.create_account(create_user_request)

@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateCreditUserRequest)
    api_manager.admin_steps.create_credit_user(user_request)
    return user_request

@pytest.fixture
def create_credit_account_response(api_manager, create_credit_user_request):
    return api_manager.user_steps.create_account(create_credit_user_request)


@pytest.fixture
def user_two_accounts(api_manager, create_user_request):
    first_account = api_manager.user_steps.create_account(create_user_request)

    assert first_account.balance == 0

    deposit_request = UserDepositRequest(
        accountId=first_account.id,
        amount=1000
    )

    first_deposit_response = api_manager.user_steps.deposit(
        create_user_request=create_user_request,
        user_deposit_request=deposit_request
    )

    assert first_deposit_response.id == first_account.id
    assert first_deposit_response.balance == 1000

    # Создание второго счета

    second_account = api_manager.user_steps.create_account(create_user_request)
    assert second_account.balance == 0

    deposit_request = UserDepositRequest(
        accountId=second_account.id,
        amount=1000
    )

    second_deposit_response = api_manager.user_steps.deposit(
        create_user_request=create_user_request,
        user_deposit_request=deposit_request
    )

    assert second_deposit_response.id == second_account.id
    assert second_deposit_response.balance == 1000

    return {
        "user": create_user_request,
        "first_account": first_account,
        "second_account": second_account,
        "first_deposit": first_deposit_response,
        "second_deposit": second_deposit_response,
    }

@pytest.fixture
def transfer_valid(api_manager,create_user_request, user_two_accounts):
    user = user_two_accounts["user"]
    first_account = user_two_accounts["first_account"]
    second_account = user_two_accounts["second_account"]

    transfer_request =  TransferAccountRequest(
        fromAccountId=first_account.id,
        toAccountId=second_account.id,
        amount=500
    )

    return {
        "user": user,
        "transfer_request": transfer_request
    }
@pytest.fixture
def transfer_invalid(api_manager,create_user_request, user_two_accounts):
    user = user_two_accounts["user"]
    first_account = user_two_accounts["first_account"]
    second_account = user_two_accounts["second_account"]

    transfer_request =  TransferAccountRequest(
        fromAccountId=first_account.id,
        toAccountId=second_account.id,
        amount=499
    )

    return {
        "user": user,
        "transfer_request": transfer_request
    }


@pytest.fixture
def user_deposit_request_valid(api_manager,create_account_response,create_user_request ):
    return  UserDepositRequest(accountId=create_account_response.id, amount=1000)


@pytest.fixture
def user_deposit_request_invalid(api_manager,create_account_response,create_user_request ):
    return UserDepositRequest(accountId=create_account_response.id, amount=999)


@pytest.fixture
def user_credit_take_request_valid(api_manager,create_credit_account_response,create_credit_user_request ):
        return AccountCreditTakeRequest(accountId=create_credit_account_response.id, amount=5000, termMonths=12)



@pytest.fixture
def user_credit_take_request_invalid(api_manager,create_credit_account_response,create_credit_user_request ):
        return AccountCreditTakeRequest(accountId=create_credit_account_response.id, amount=500000, termMonths=12)

@pytest.fixture
def credit_taken_response(api_manager, create_credit_user_request, user_credit_take_request_valid):
    return api_manager.user_steps.credit_take(
        create_credit_user_request,
        user_credit_take_request_valid
    )

@pytest.fixture
def user_credit_repay_request_valid(api_manager,credit_taken_response, user_credit_take_request_valid,):
    return AccountCreditRepayRequest(creditId=credit_taken_response.creditId,accountId=credit_taken_response.id, amount=5000)


@pytest.fixture
def user_credit_repay_request_invalid(api_manager,credit_taken_response, user_credit_take_request_valid):
    return AccountCreditRepayRequest(creditId=credit_taken_response.creditId,accountId=credit_taken_response.id, amount=4999)
