from pydantic import BaseModel, Field


class ExchangeRateMessage(BaseModel):
    chat_id: int = Field(examples=[123456788], description="ID of sender")
    user_name: str = Field(examples=["Ortem"], description="Name of sender")
    value_name: str = Field(
        max_length=3, examples=["USD"], description="Value name (ISO 4217)"
    )
    exchange_rate: float = Field(description="Exchange rate", examples=[94.6])


class ExchangeRequest(BaseModel):
    chat_id: int = Field(examples=[123456788], description="ID of sender")
    user_name: str = Field(examples=["Ortem"], description="Name of sender")
    value_name: str = Field(
        max_length=3, examples=["USD"], description="Value name (ISO 4217)"
    )
