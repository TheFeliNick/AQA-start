from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.valdate_crud_requester import ValidateCrudRequester
from src.main.api.models.account_credit_repay_request import AccountCreditRepayRequest
from src.main.api.models.account_credit_take_request import AccountCreditTakeRequest
from src.main.api.models.create_credit_user_request import CreateCreditUserRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.user_deposit_request import UserDepositRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def deposit(self, create_user_request : CreateUserRequest ,user_deposit_request: UserDepositRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(user_deposit_request)
        return response


    def deposit_invalid(self, create_user_request : CreateUserRequest ,user_deposit_request: UserDepositRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(user_deposit_request)
        return response


    def transfer_data_prepared(self, transfer_data):
        return self.transfer(
            create_user_request=transfer_data["user"],
            transfer_account_request=transfer_data["transfer_request"],
        )

    def transfer_data_prepared_invalid(self, transfer_data):
        return self.transfer_invalid(
            create_user_request=transfer_data["user"],
            transfer_account_request=transfer_data["transfer_request"],
        )

    def transfer(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_account_request)
        return response


    def transfer_invalid(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_user_request.username,
                password=create_user_request.password
            ),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(transfer_account_request)
        return response

    def credit_take(self, create_credit_user_request: CreateCreditUserRequest,account_credit_take_request: AccountCreditTakeRequest ):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_credit_user_request.username,
                password=create_credit_user_request.password
            ),
            Endpoint.CREDIT_TAKE,
            ResponseSpecs.request_created()
        ).post(account_credit_take_request)
        return response

    def credit_take_invalid(self, create_credit_user_request: CreateCreditUserRequest,account_credit_take_request: AccountCreditTakeRequest ):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_credit_user_request.username,
                password=create_credit_user_request.password
            ),
            Endpoint.CREDIT_TAKE,
            ResponseSpecs.request_bad()
        ).post(account_credit_take_request)
        return response

    def credit_repay(self, create_credit_user_request: CreateCreditUserRequest, account_credit_repay_request: AccountCreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(
                username=create_credit_user_request.username,
                password=create_credit_user_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        ).post(account_credit_repay_request)
        return response

    def credit_repay_invalid(self, create_credit_user_request: CreateCreditUserRequest, account_credit_repay_request: AccountCreditRepayRequest):
        response = CrudRequester(
            RequestSpecs.auth_headers(
                username=create_credit_user_request.username,
                password=create_credit_user_request.password
            ),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_bad_content()
        ).post(account_credit_repay_request)
        return response