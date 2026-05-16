from dataclasses import dataclass
from enum import Enum
from typing import Type, Optional

from src.main.api.models.account_credit_repay_request import AccountCreditRepayRequest
from src.main.api.models.account_credit_repay_response import AccountCreditRepayResponse
from src.main.api.models.account_credit_take_request import AccountCreditTakeRequest
from src.main.api.models.account_credit_take_response import AccountCreditTakeResponse
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse
from src.main.api.models.user_deposit_request import UserDepositRequest
from src.main.api.models.user_deposit_response import UserDepositResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url = "/admin/create",
        response_model = CreateUserResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = "/admin/users",
        response_model = None
    )

    LOGIN_USER = EndpointConfiguration(
        request_model = LoginUserRequest,
        url = "/auth/token/login",
        response_model = LoginUserResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model = None,
        url = "/account/create",
        response_model = CreateAccountResponse
    )

    DEPOSIT_ACCOUNT = EndpointConfiguration(
        request_model = UserDepositRequest,
        url = "/account/deposit",
        response_model = UserDepositResponse
    )

    TRANSFER_ACCOUNT = EndpointConfiguration(
        request_model = TransferAccountRequest,
        url = "/account/transfer",
        response_model = TransferAccountResponse
    )

    CREDIT_TAKE = EndpointConfiguration(
        request_model = AccountCreditTakeRequest,
        url = "/credit/request",
        response_model = AccountCreditTakeResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        request_model = AccountCreditRepayRequest,
        url = "/credit/repay",
        response_model = AccountCreditRepayResponse
    )

