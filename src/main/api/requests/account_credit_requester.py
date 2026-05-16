from http import HTTPStatus
from requests import Response
from src.main.api.models.account_credit_take_request import AccountCreditTakeRequest
from src.main.api.models.account_credit_take_response import AccountCreditTakeResponse
from src.main.api.requests.requester import Requester
import requests


class AccountCreditRequester(Requester):
    def post(self, account_credit_request: AccountCreditTakeRequest) -> AccountCreditTakeResponse | Response:
        url = f"{self.base_url}/credit/request"

        response = requests.post(
            url = url,
            json= account_credit_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)

        if response.status_code == HTTPStatus.CREATED:
            return AccountCreditTakeResponse(**response.json())
        return response