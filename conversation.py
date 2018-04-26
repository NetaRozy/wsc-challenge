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

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE, TEAM, GAME, GAME_ACTIONS, PLAYER, GAME_PLAYER, PLAYER_ACTIONS, HIGHLIGHTS = range(10)

reply_keyboard = [['Summaries', 'Team'],
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
        "hey! what do you want to see?",
        reply_markup=markup)

    return CHOOSING



def team(bot, update, user_data):
    reply_keyboard = [['Slovenia', 'Serbia'],
                      ['Spain'],
                      ['Russia']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['choice'] = update.message.text
    update.message.reply_text(
        "So.. you want to hear about a {}. Which one?".format(update.message.text),
        reply_markup=markup)

    return GAME

def game(bot, update, user_data):
    team = update.message.text

    # Query Team's latest games with XX api.
    teams = ["Israel", "Germany", "Poland", "France", "Austria"]
    reply_keyboard = [["{} vs {}".format(team, random.choice(teams))],
                       ["{} vs {}".format(team, random.choice(teams))],
                       ["{} vs {}".format(team, random.choice(teams))],
                       ["{} vs {}".format(team, random.choice(teams))]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['team'] = update.message.text
    update.message.reply_text(
        "Oh! You're a fan of {}? Here are the latest games.".format(update.message.text),
        reply_markup=markup)

    return GAME_ACTIONS

def game_actions(bot, update, user_data):
    reply_keyboard = [['3 Points', '2 Points'],
                      ['Dunks'], ['Blocks'],
                      ['Assists'], ['Alley Oops'],
                      ['General']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['game'] = update.message.text
    update.message.reply_text(
        "I can show you some videos of {}. Just pick one.".format(update.message.text),
        reply_markup=markup)


    return TYPING_REPLY

def player(bot, update, user_data):
    reply_keyboard = [['Gabriel Olaseni', 'Aleksei Shaved'],
                      ['Jonas Valanciunas'],
                      ['Kristaps Porzingis']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['choice'] = update.message.text
    update.message.reply_text(
        "So.. you want to hear about a {}. Which one?".format(update.message.text),
        reply_markup=markup)

    return GAME_PLAYER

def gameplayer(bot, update, user_data):
    reply_keyboard = [['recents', 'olds']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['team'] = update.message.text
    update.message.reply_text(
        "Oh! You're a fan of {}? want to see his new highlights or travel to his past a little bit?".format(update.message.text),
        reply_markup=markup)

    return PLAYER_ACTIONS

def player_actions(bot, update, user_data):
    reply_keyboard = [['3 Points', '2 Points'],
                      ['Dunks'], ['Blocks'],
                      ['Assists'], ['Alley Oops'],
                      ['General']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    user_data['game'] = update.message.text
    update.message.reply_text(
        "I can show you some videos of {}. Just pick one.".format(update.message.text),
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

    update.message.reply_text("We send you your highlight, want more?".format(
                                  facts_to_str(user_data)), reply_markup=markup)

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
    updater = Updater("563416873:AAEalULoCiYMwS88M1_l9D5knfJj3qrTl_Q")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

            states={
            CHOOSING: [RegexHandler('^(Team)$',
                                    team,
                                    pass_user_data=True),
                       RegexHandler('^(Player)$',
                                    player,
                                    pass_user_data=True),
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
            GAME_PLAYER: [MessageHandler(Filters.text,
                                  gameplayer,
                                  pass_user_data=True),
                   ],
            PLAYER_ACTIONS: [MessageHandler(Filters.text,
                                          player_actions,
                                          pass_user_data=True),
                           ],
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
