#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import random
import logging
import json
import mainMethods

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, TEAM, GAME, GAME_ACTIONS = range(6)

reply_keyboard = [['Highlights', 'Team'],
                  ['Player'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    update.message.reply_text(
        "Hi! we can make special highlights for you, just choose your topic:",
        reply_markup=markup)

    return CHOOSING


def regular_choice(bot, update, user_data):
    reply_keyboard = [['Slovenia', 'Serbia'],
                      ['Spain'],
                      ['Russia']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['choice'] = update.message.text
    update.message.reply_text(
        "So.. you want to hear about a {}. Which one?".format(update.message.text),
        reply_markup=markup)

    return TYPING_REPLY


def team(bot, update, user_data):
    # We present the top 4 teams, with an option to enter one by your own.
    reply_keyboard = [['Slovenia', 'Serbia'],
                      ['Spain'],
                      ['Russia'], ['Other']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['choice'] = update.message.text
    update.message.reply_text(
        "So.. you want to hear about a {}. Which one?".format(update.message.text),
        reply_markup=markup)

    return GAME


def game(bot, update, user_data):
    team = update.message.text

    games = []
    with open('eurobasket_games.json') as euro:
        euro = json.loads(euro.read())
        for day in euro.keys():
            for game in euro[day]:
                if team.lower() in game.keys():
                    keys = list(game.keys())
                    games.append(["{} vs {} - {}".format(keys[0], keys[1], day.lower())])

    print(games)
    # Query Team's latest games with XX api.
    reply_keyboard = games
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['team'] = update.message.text
    update.message.reply_text(
        "Great choise! here are all of the games for {}. choose the game you want?".format(update.message.text),
        reply_markup=markup)

    return GAME_ACTIONS


def game_actions(bot, update, user_data):
    reply_keyboard = [['3 PTS', '2 PTS'],
                      ['Dunks'], ['Blocks'],
                      ['Assists'],
                      ['General']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['game'] = update.message.text
    update.message.reply_text(
        "Good chooise, what kind of events do you prefer?".format(update.message.text),
        reply_markup=markup)

    return TYPING_REPLY


def custom_choice(bot, update):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    data = user_data['game'].split()
    print(data[0])
    print(data[2])
    print(text)
    vid = mainMethods.get_my_video(data[0] + data[2] + text)
    url = vid['videoUrl']
    thumbnail = vid['thumbnail']['mediumThumbnailUrl']
    input = data[0] + data[1] + text
    update.message.reply_text("excelent, we made a special highlights video just for you, ENJOY!"" "
                              "{} {}"
        .format(
        thumbnail, url), reply_markup=markup)

    return CHOOSING


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.

    # f = open('token', 'r')
    # token = f.read().strip()
    # f.close()
    
    updater = Updater('512075931:AAFhxD7f5gBwVYcM7MadnR2-jRPbt0iFxhU')


    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(

        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^(Team)$',
                                    team,
                                    pass_user_data=True),
                       RegexHandler('^Something else...$',
                                    custom_choice),
                       ],
            GAME: [MessageHandler(Filters.text,
                                  game,
                                  pass_user_data=True),
                   ],
            GAME_ACTIONS: [MessageHandler(Filters.text,
                                          game_actions,
                                          pass_user_data=True),
                           ],
            # TYPING_CHOICE: [MessageHandler(Filters.text,
            #                                regular_choice,
            #                                pass_user_data=True),
            #                 ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    