from faststream import Context
from faststream.kafka import KafkaRouter
from aiogram import Bot, F, Router
from aiogram import types
from aiogram.filters import Command
from src.logging_config import logger
from src.model import ExchangeRateMessage, ExchangeRequest

router = Router()
kafka_router = KafkaRouter()

sender_request = kafka_router.publisher(
    "exchange-rate-request",
    headers={"content-type": "application/json"},
    schema=ExchangeRequest,
)


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await logger.ainfo("User %s started bot", message.from_user.username)  #  type: ignore
    await message.answer("Привет! Назови свое имя и я отправлю тебе курс доллара!")


@router.message(F.text)
async def get_name(message: types.Message):
    try:
        chat_id = message.chat.id
        await logger.ainfo("User %s send name: %s", chat_id, message.text)
        if not message.text:
            raise ValueError
        request = ExchangeRequest(
            chat_id=chat_id, user_name=message.text, value_name="USD"
        )
        await sender_request.publish(request)
    except ValueError:
        await message.answer(
            "Кажется ты отправил что-то странное вместо имени. Попробуй ещё раз."
        )
        await logger.ainfo("User send message in group chat")
    except Exception:
        logger.exception("Unexpected error: %s")


@kafka_router.subscriber("exchange-rate-output")
async def get_exchange_rate(exchange_rate: ExchangeRateMessage, bot: Bot = Context()):
    await logger.ainfo(
        "Get exchange rate message from kafka", message=exchange_rate.model_dump()
    )
    await bot.send_message(
        exchange_rate.chat_id,
        f"{exchange_rate.user_name}, курс {exchange_rate.value_name}: {exchange_rate.exchange_rate}",
    )
