from src.main.api.models.base_model import BaseModel


class AccountCreditRepayRequest(BaseModel):
    creditId: int
    accountId: int
    amount: float #Кредит можно погасить только один раз, единовременно и на всю сумму