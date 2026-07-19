import logging

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from . import config, handlers

logging.basicConfig(
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    level=logging.INFO,
)


def main() -> None:
    app = Application.builder().token(config.BOT_TOKEN).build()

    group_filter = filters.Chat(chat_id=config.GROUP_CHAT_ID)

    app.add_handler(CommandHandler("lista", handlers.lista))
    app.add_handler(MessageHandler(group_filter & filters.Document.PDF, handlers.on_pdf_uploaded))
    app.add_handler(CallbackQueryHandler(handlers.on_button))

    logging.getLogger(__name__).info("Vecchia Bunny è pronta tra i suoi scaffali. Avvio polling...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
