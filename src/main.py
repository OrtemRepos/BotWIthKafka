import asyncio

from faststream import FastStream, ContextRepo
from faststream.asgi import make_asyncapi_asgi, make_ping_asgi
from faststream.kafka import KafkaBroker
from faststream.asyncapi.schema import Contact, License

from aiogram import Bot, Dispatcher

from src.handler import router, kafka_router
from src.config import settings
from src.logging_config import logger


async def main():
    bot = Bot(token=settings.token, logger=logger)
    dp = Dispatcher()
    dp.include_router(router)

    broker = KafkaBroker("localhost:9094", graceful_timeout=5)
    broker.include_router(kafka_router)

    app = FastStream(
        broker,
        logger=logger,
        title="Exchange Rate Telegram Bot",
        version="0.1.0",
        description="Telegram bot for exchange rate",
        license=License(name="MIT", url="https://opensource.org/licenses/MIT"),  #  type: ignore
        contact=Contact(name="Sadykov Artem", url="https://github.com/OrtemRepo"),  # type: ignore
    ).as_asgi(asgi_routes=[("/health", make_ping_asgi(broker))])

    app.mount("/docs", make_asyncapi_asgi(app))

    @app.after_startup
    async def startup(context: ContextRepo):
        context.set_global("logger", logger)
        context.set_global("bot", bot)
        await logger.ainfo("Set bot in context")

    @app.on_shutdown
    async def shutdown():
        await dp.stop_polling()
        await logger.ainfo("DP shutdown...")
        await broker.close()

    app_task = asyncio.create_task(
        app.run(run_extra_options={"host": "0.0.0.0", "port": 8002})
    )
    bot_task = asyncio.create_task(dp.start_polling(bot, handle_signals=False))

    await asyncio.gather(app_task, bot_task)


if __name__ == "__main__":
    asyncio.run(main())
