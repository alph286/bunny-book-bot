import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import Forbidden
from telegram.ext import ContextTypes

from . import catalog, config, persona

logger = logging.getLogger(__name__)


def _is_allowed_context(message) -> bool:
    if message.chat.type == "private":
        return True
    return message.chat_id == config.GROUP_CHAT_ID and message.message_thread_id == config.MANUALI_TOPIC_ID


def _render_list(chat_data: dict, cmd_message_id: int) -> tuple[str, InlineKeyboardMarkup | None]:
    flavor = persona.pick_lista_flavor(chat_data)
    documents = catalog.list_documents()

    if not documents:
        return f"{flavor}\n\nAl momento non ho nessun manuale sugli scaffali. Che tristezza.", None

    buttons = [
        [InlineKeyboardButton(f"\U0001F4C4 {doc.title}", callback_data=f"send|{doc.id}|{cmd_message_id}")]
        for doc in documents
    ]
    return f"{flavor}\n\nEcco i manuali disponibili, te li mando in privato:", InlineKeyboardMarkup(buttons)


async def lista(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not _is_allowed_context(message):
        return

    text, markup = _render_list(context.chat_data, message.message_id)
    await message.reply_text(
        text,
        reply_markup=markup,
        message_thread_id=message.message_thread_id,
    )


async def on_pdf_uploaded(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message.message_thread_id != config.MANUALI_TOPIC_ID:
        return

    document = message.document

    caption = (message.caption or "").strip()
    title = caption.splitlines()[0].strip() if caption else None
    if not title:
        title = document.file_name.rsplit(".", 1)[0].replace("_", " ").strip()

    catalog.upsert_document(title=title, file_id=document.file_id, file_unique_id=document.file_unique_id)

    flavor = persona.pick_archive_flavor(context.chat_data)
    await message.reply_text(
        f"{flavor}\n\n«{title}» è ora disponibile con /lista.",
        message_thread_id=message.message_thread_id,
    )


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    list_message = query.message

    parts = query.data.split("|")
    doc_id_raw = parts[1] if len(parts) > 1 else ""
    cmd_message_id = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None
    doc = catalog.get_document(int(doc_id_raw)) if doc_id_raw.isdigit() else None

    if doc is None:
        await query.answer("Questo tomo non si trova più sullo scaffale, strano.", show_alert=True)
        return

    requester_id = query.from_user.id
    flavor = persona.pick_send_flavor(context.chat_data)

    try:
        await context.bot.send_document(chat_id=requester_id, document=doc.file_id, caption=flavor)
    except Forbidden:
        await query.answer(
            "Devi prima scrivermi in privato (aprimi la chat e premi /start): solo allora posso mandarti i tomi lì.",
            show_alert=True,
        )
        return

    await query.answer("Te l'ho mandato in privato!")

    if list_message.chat_id == config.GROUP_CHAT_ID and list_message.message_thread_id == config.MANUALI_TOPIC_ID:
        try:
            await context.bot.delete_message(chat_id=list_message.chat_id, message_id=list_message.message_id)
        except Exception:
            logger.warning("Impossibile cancellare il messaggio della lista, mancano i permessi?")
        if cmd_message_id is not None:
            try:
                await context.bot.delete_message(chat_id=list_message.chat_id, message_id=cmd_message_id)
            except Exception:
                logger.warning("Impossibile cancellare il messaggio /lista, mancano i permessi?")
