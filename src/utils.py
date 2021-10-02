from src.constants import TRANSLITERATION_DICT
from src.db import db_session
from src.db.models.user import User


def make_transliteration(text):
    new_text = ''
    for s in text:
        if s.lower() in TRANSLITERATION_DICT:
            new_text += TRANSLITERATION_DICT[s.lower()].upper() if s.isupper() else TRANSLITERATION_DICT[s]
        else:
            new_text += s
    return new_text


def answer(text, markup, context):
    return (context.user_data['bot_message'].edit_text(text, reply_markup=markup)
            if context.user_data.get('bot_message')
            else context.user_data['message'].reply_text(text, reply_markup=markup))


def get_user_entity(user_id):
    session = db_session.create_session()
    return (session.query(User).get(user_id), session) if user_id else (None, None)


def auth_required(func):
    def wrapper(update, context):
        user_id = context.user_data['user_id'] if context.user_data.get('user_id') else update.message.from_user.id
        user, session = get_user_entity(user_id)
        if not user:
            user = User(id=user_id)
            session.add(user)
            session.commit()
        context.user_data['user_id'] = user.id
        output = func(update, context, user, session)
        session.close()
        return output
    return wrapper