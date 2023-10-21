import json
from config import faker, users, bot
from telebot import types
from secrets import token_urlsafe
from generator import welcome, messages


@bot.message_handler(commands=['users'])
def users_handler(message):
    users_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    users_markup.add(*users, row_width=2)
    users_markup.add('Back to start')

    reply = bot.send_message(message.chat.id,
                             messages["users_generator"],
                             reply_markup=users_markup)
    bot.register_next_step_handler(reply, users_number)


def users_number(message):
    payload_len = 0
    if (message.text == 'Back to start' or message.text == '/start'):
        welcome(message)
    elif message.text == '1️⃣':
        payload_len = 1
    elif message.text == "3️⃣":
        payload_len = 3
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    elif (message.text.isdigit() and 0 < int(message.text) <= 15):
        payload_len = int(message.text)
    elif message.text.isdigit():
        bot.send_message(message.chat.id, messages["users_generator_error"])
        bot.register_next_step_handler(message, users_number)
    else:
        bot.send_message(message.chat.id, messages["query_error"])
        bot.register_next_step_handler(message, users_number)

    # Generate test data for the selected number of users
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'{faker.msisdn()[4:]}'

        # Use the secrets library to generate a password
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # Serialise the data into a string
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str)

    # Sending the result
    if payload_len != 0:
        bot.send_message(message.chat.id, f"Data of {payload_len} test users:"
                         f"\n\n<code>{payload_str}</code>")
        reply = bot.send_message(message.chat.id,
                                 messages["generator_again"])
        bot.register_next_step_handler(reply, users_number)