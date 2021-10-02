from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from src.db import db_session
from src.db.models.timetable import Timetable
from src.db.models.user import User
from src.utils import answer, auth_required


def show_timetable_menu(_, context):
    markup = InlineKeyboardMarkup([[InlineKeyboardButton('Понедельник', callback_data='Понедельник')],
                                   [InlineKeyboardButton('Вторник', callback_data='Вторник')],
                                   [InlineKeyboardButton('Среда', callback_data='Среда')],
                                   [InlineKeyboardButton('Четверг', callback_data='Четверг')],
                                   [InlineKeyboardButton('Пятница', callback_data='Пятница')],
                                   [InlineKeyboardButton('Показать полностью', callback_data='full_timetable')],
                                   [InlineKeyboardButton('Вернуться назад', callback_data='menu')]])
    if context.user_data.get('bot_message'):
        context.user_data['bot_message'].edit_text('Расписание', reply_markup=markup)
    else:
        context.user_data['message'].reply_text('Расписание', reply_markup=markup)
    return 'menu'


@auth_required
def choose_timetable(_, context, user, session):
    if user.chosen_timetable:
        return show_timetable_menu(_, context)
    timetables = session.query(Timetable).all()
    if not timetables:
        buttons = [[InlineKeyboardButton('Вернуться назад', callback_data='menu')]]
        if user.role == 'admin':
            buttons.append([InlineKeyboardButton('Добавить расписание', callback_data='add_timetable')])
        markup = InlineKeyboardMarkup(buttons)
        answer('На данный момент нет никаких расписаний', markup, context)
        return 'timetable_choice'
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(timetable.name) for timetable in timetables]])
    answer('Выберите расписание', markup, context)
    return 'timetable_choice'


def show_full_timetable():
    pass


def add_timetable(_, context, user, session):
    context.user_data['message'].reply_text('Введите название расписания')
    context.user_data['new_timetable'] = {'user_id': user.id}
    return ''


def set_timetable_name(_, context):
    pass