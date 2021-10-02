import os
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, CallbackQueryHandler, CallbackContext
from telegram import Update
from dotenv import load_dotenv

from src.interactions.timetable import *


def start(update, context):
    return show_menu(update, context)


@auth_required
def show_menu(update: Update, context: CallbackContext, _, __):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('Расписание', callback_data='choose_timetable')]])
    if context.user_data.get('bot_message'):
        context.user_data['bot_message'].edit_text('Меню', reply_markup=markup)
        return 'menu'
    if hasattr(update.message, 'reply_text'):
        context.user_data['bot_message'] = update.message.reply_text('Меню', reply_markup=markup)
        context.user_data['message'] = update.message
    else:
        context.user_data['bot_message'] = context.user_data['message'].reply_text('Меню', reply_markup=markup)
    return 'menu'


def main():
    updater = Updater(os.getenv('token'))
    updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={'menu': [CallbackQueryHandler(choose_timetable, pattern='choose_timetable'),
                         CallbackQueryHandler(show_full_timetable, pattern='full_timetable'),
                         CallbackQueryHandler(show_menu, pattern='menu')],
                'timetable_choice': [CallbackQueryHandler(show_menu, pattern='menu'),
                                     [CallbackQueryHandler(add_timetable, pattern='add_timetable')],
                                     CallbackQueryHandler(show_timetable_menu)],
                'timetable_name': [MessageHandler()]},
        fallbacks=[CommandHandler('start', start)]
    ))
    updater.start_polling()
    updater.idle()


def pre_start():
    with db_session.create_session() as session:
        session.add(User(id=738699147, role='admin'))
        session.commit()


if __name__ == '__main__':
    load_dotenv()
    db_session.global_init('sqlite:///%s?check_same_thread=False' % os.path.join('src', 'db', 'binary', 'data.db'))
    # pre_start()
    main()
