from settings import conf, constants, emojis
# noinspection PyPackageRequirements
from telebot import TeleBot
# noinspection PyPackageRequirements
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import common

bot = TeleBot(conf['telegram_token'])

ADD_COMMAND = 'add'
REMOVE_COMMAND = 'remove'
LIST_COMMAND = 'list'
UPDATE_COMMAND = 'update'

add_date_txt = emojis['plus'] + constants['add_date_btn']
remove_date_txt = emojis['remove'] + constants['remove_date_btn']
view_dates_txt = emojis['list'] + constants['view_dates_btn']
update_date_txt = emojis['update'] + constants['update_date_btn']

start_buttons_markup = InlineKeyboardMarkup(row_width=1)
start_buttons_markup.add(
    InlineKeyboardButton(add_date_txt, callback_data=ADD_COMMAND),
    InlineKeyboardButton(remove_date_txt, callback_data=REMOVE_COMMAND),
    InlineKeyboardButton(view_dates_txt, callback_data=LIST_COMMAND),
    InlineKeyboardButton(update_date_txt, callback_data=UPDATE_COMMAND)
)

keyboard_date_type = ReplyKeyboardMarkup(True, True)
keyboard_date_type.row(constants['date_type_bday'], constants['date_type_anniv'])


@bot.message_handler(commands=['start'])
def start_message(message):
    if not common.verify_user_valid(message.chat.id, bot):
        return
    current_state = common.db_worker('get_state', message.chat.id)
    bot.send_message(message.chat.id, constants['start_instructions'], reply_markup=start_buttons_markup)


@bot.callback_query_handler(func=lambda call: True)
def start_callback(call):
    if not common.verify_user_valid(call.from_user.id, bot):
        return
    if call.data == ADD_COMMAND:
        add_date_first_step(call.from_user.id)
    # elif call.data == REMOVE_COMMAND:
    #     remove_date_first_step()
    # elif call.data == LIST_COMMAND:
    #     list_dates()
    # elif call.data == REMOVE_COMMAND:
    #     remove_date_first_step()


def add_date_first_step(user_id):
    common.db_worker('update_state', 'add_date_first_step', user_id)
    bot.send_message(user_id, constants['input_name'])


@bot.message_handler(content_types=['text'])
def send_text(message):
    if not common.verify_user_valid(message.chat.id, bot):
        return

    current_state = common.db_worker('get_state', message.chat.id)
    if current_state == 'add_date_first_step':
        common.db_worker('insert_name', message.text)
        bot.send_message(message.chat.id, 'done')


bot.polling()
