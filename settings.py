from dotenv import load_dotenv
import os

load_dotenv()

conf = {
    'telegram_token': os.getenv('BOT_TOKEN'),
    'mysql': {
        'user': os.getenv('MYSQL_USER'),
        'password': os.getenv('MYSQL_PASSWORD'),
        'host': os.getenv('MYSQLL_HOST'),
        'database': os.getenv('MYSQL_DB'),
        'port': 3306,
        'raise_on_warnings': True
    },
    'user_id': os.getenv('ALLOWED_USER_ID')
}
constants = {
    'add_date_btn': 'Добавить дату',
    'remove_date_btn': 'Удалить дату',
    'view_dates_btn': 'Список дат',
    'update_date_btn': 'Изменить дату',
    'start_instructions': 'Здесь будут инструкции',
    'start_text': 'Здравствуйте! Выберите одну из опций',
    'date_type': 'Выберите тип даты. Если опции не подходят для вас, пришлите свой тип даты текстом',
    'remove_date': 'Выберите дату, которую хотите удалить:',
    'date_type_bday': 'День рождения',
    'date_type_anniv': 'Годовщина свадьбы',
    'not_valid_user': 'Неавторизованный пользователь',
    'error_occurred': 'Произошла ошибка, свяжитесь с админом бота - @nodirosaka',

    'input_name': 'Как зовут человека?'
}
emojis = {
    'plus': u'\U00002795',
    'remove': u'\U0000274C',
    'list': u'\U0001F4CB',
    'update': u'\U0001F504'
}