from src.main.api.requests.requester import Requester
import requests
from http import HTTPStatus
from requests import Response
from src.main.api.models.account_credit_repay_request import AccountCreditRepayRequest
from src.main.api.models.account_credit_repay_response import AccountCreditRepayResponse



class AccountCreditRepayRequester(Requester):
    def post(self, account_credit_repay_request: AccountCreditRepayRequest) -> AccountCreditRepayResponse | Response:
        url = f"{self.base_url}/credit/repay"

        response = requests.post(
            url=url,
            json=account_credit_repay_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return AccountCreditRepayResponse(**response.json())
        return response