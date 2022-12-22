import logging

from telegram import ReplyKeyboardRemove, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

import messages
import telegramcalendar
import utils

TOKEN = "5943689784:AAGP2Yc4z_joomO6CN1RbY4XPsd3u6iPs3Y"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.start_message.format(update.message.from_user.first_name),
        parse_mode=ParseMode.HTML)


def calendar_handler(update, context):
    update.message.reply_text(text=messages.calendar_message,
                              reply_markup=telegramcalendar.create_calendar())


def inline_handler(update, context):
    query = update.callback_query
    (kind, _, _, _, _) = utils.separate_callback_data(query.data)
    if kind == messages.CALENDAR_CALLBACK:
        inline_calendar_handler(update, context)


def inline_calendar_handler(update, context):
    selected, date = telegramcalendar.process_calendar_selection(update, context)
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.calendar_response_message % (date.strftime("%d/%m/%Y")),
                                 reply_markup=ReplyKeyboardRemove())


if TOKEN == "":
    print("Please write TOKEN into file")
else:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", calendar_handler))
    dp.add_handler(CommandHandler("calendar", calendar_handler))
    dp.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()
    updater.idle()
