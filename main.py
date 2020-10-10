import os
import urllib
import uuid
from datetime import datetime
# noinspection PyPackageRequirements
from string import Template

from telebot import TeleBot
# noinspection PyPackageRequirements
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

import common
from settings import conf, messages, emojis

bot = TeleBot(conf['telegram_token'])

ADD_COMMAND = 'add'
REMOVE_COMMAND = 'remove'
LIST_COMMAND = 'list'
UPDATE_COMMAND = 'update'

add_date_txt = emojis['plus'] + messages['add_date_btn']
remove_date_txt = emojis['remove'] + messages['remove_date_btn']
view_dates_txt = emojis['list'] + messages['view_dates_btn']
update_date_txt = emojis['update'] + messages['update_date_btn']

main_commands_markup = InlineKeyboardMarkup(row_width=1)
main_commands_markup.add(
    InlineKeyboardButton(add_date_txt, callback_data=ADD_COMMAND),
    InlineKeyboardButton(remove_date_txt, callback_data=REMOVE_COMMAND),
    InlineKeyboardButton(view_dates_txt, callback_data=LIST_COMMAND),
    InlineKeyboardButton(update_date_txt, callback_data=UPDATE_COMMAND)
)

keyboard_date_type = ReplyKeyboardMarkup(True, True)
keyboard_date_type.row(messages['date_type_bday'], messages['date_type_anniv'])


@bot.message_handler(commands=['start'])
def start_message(message):
    if not common.verify_user_valid(message.chat.id, bot):
        return
    current_state = common.db_worker('get_state', message.chat.id)
    bot.send_message(message.chat.id, messages['start_instructions'], reply_markup=main_commands_markup)


@bot.callback_query_handler(func=lambda call: True)
def start_callback(call):
    if not common.verify_user_valid(call.from_user.id, bot):
        return
    if call.data == ADD_COMMAND:
        common.db_worker('update_state', 'add_date_name_step', call.from_user.id)
        add_date_name_step(call.from_user.id)
    # elif call.data == REMOVE_COMMAND:
    #     remove_date_first_step()
    # elif call.data == LIST_COMMAND:
    #     list_dates()
    # elif call.data == REMOVE_COMMAND:
    #     remove_date_first_step()


def add_date_name_step(user_id):
    bot.send_message(user_id, messages['input_name'])


def add_date_type_step(user_id):
    reply_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    reply_markup.row(messages['birthday_type'], messages['anniv_type'])
    bot.send_message(user_id, messages['input_type'], reply_markup=reply_markup)


def add_date_date_step(user_id):
    bot.send_message(user_id, messages['input_date'])


def add_date_photo_step(user_id):
    bot.send_message(user_id, messages['input_photo'])


def generate_unique_file_name():
    name = uuid.uuid4().hex[:12].lower()
    img_folder = 'photos'
    if os.path.isfile(f'{img_folder}/{name}.jpg'):
        generate_unique_file_name()
    return f'{img_folder}/{name}.jpg'


@bot.message_handler(content_types=['text', 'photo'])
def send_text(message):
    if not common.verify_user_valid(message.chat.id, bot):
        return

    current_state = common.db_worker('get_state', message.chat.id)
    if current_state == 'add_date_name_step':
        new_date_id = common.db_worker('insert_name', message.text)
        common.db_worker('update_state_date_id', 'add_date_type_step', new_date_id, message.chat.id)
        add_date_type_step(message.chat.id)
    elif current_state == 'add_date_type_step':
        date_id = common.db_worker('get_current_date_id', message.chat.id)
        common.db_worker('set_type', message.text, date_id)
        common.db_worker('update_state', 'add_date_date_step', message.chat.id)
        add_date_date_step(message.chat.id)
    elif current_state == 'add_date_date_step':
        date_str = message.text
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        except ValueError:
            bot.send_message(message.chat.id, messages['input_date_invalid'])
            return
        date_id = common.db_worker('get_current_date_id', message.chat.id)
        date_obj.strftime('%Y-%m-%d %H:%M:%S')
        common.db_worker('set_date', date_obj, date_id)
        common.db_worker('update_state', 'add_date_photo_step', message.chat.id)
        add_date_photo_step(message.chat.id)
    elif current_state == 'add_date_photo_step':
        date_id = common.db_worker('get_current_date_id', message.chat.id)
        img_file = bot.get_file(message.photo[-1].file_id)
        img_url = f'https://api.telegram.org/file/bot{conf["telegram_token"]}/{img_file.file_path}'
        img_path = generate_unique_file_name()
        urllib.request.urlretrieve(img_url, img_path)
        common.db_worker('set_photo_path', img_path, date_id)
        added_date_row = common.db_worker('get_one_date', date_id)
        caption_obj = Template(messages['new_added_date'])
        caption_text = caption_obj.substitute(
            name=added_date_row[0],
            date_type=added_date_row[1],
            date=added_date_row[2],
        )
        bot.send_photo(
            message.chat.id,
            photo=open(added_date_row[3], 'rb'),
            caption=str(caption_text),
            reply_markup=main_commands_markup,
        )
        common.db_worker('update_state_date_id', 'new', None, message.chat.id)


bot.polling()
