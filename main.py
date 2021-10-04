import os
import logging
import movielinks
import time
from telegram.ext import *
from telegram import *

API_KEY = os.environ.get('API_KEY')
bot = Bot(token=API_KEY)
MLINK = 'https://linkpdisk.com/share-video?videoid='
admin_chat_id1 = 
admin_chat_id2 = 1317474154


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting bot...')

def start_command(update, context):
    text = f'''
    Hello {update.message.chat.username}, ᴀꜱᴋ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ᴡɪᴛʜᴏᴜᴛ ꜱᴘᴇʟʟɪɴɢ ᴍɪꜱᴛᴀᴋᴇꜱ,
    ɪ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴡᴀᴛᴄʜ ᴛʜᴀᴛ ᴍᴏᴠɪᴇ
    ʙᴇꜰᴏʀᴇ ꜱᴇᴀʀᴄʜɪɴɢ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ʀᴇꜰᴇʀ ᴛʜᴇ ɢᴏᴏɢʟᴇ ꜰᴏʀ ᴍᴏᴠɪᴇ ɴᴀᴍᴇꜱ ᴀɴᴅ ɢɪᴠᴇ ᴍᴇ ɴᴀᴍᴇ ᴀꜱ ɪᴛ ɪꜱ.
    1.ꜱᴇᴀʀᴄʜ 🔍
    2.ᴄʟɪᴄᴋ
    3.ᴇɴᴊᴏʏ
    Developed by @king_webseries
    '''
    chat_id = update.message.chat.id

    bot.send_message(chat_id=chat_id, text=text)


def movie(msg, username, chat_id, msg_id):

    movie_name_user_input = msg
    movie_name_user_input = movie_name_user_input.split()
    movie_keys = movielinks.movies_ids.keys()
    try:
        priority_size = 1
        result = {}
        final_result = {}
        for keys in movie_keys:
            movie_name = keys
            keys = keys.split()
            for key in keys:
                for movie_name_user_entered in movie_name_user_input:
                    if movie_name_user_entered == key:
                        priority_size += 1
                    else:
                        pass
            result[movie_name] = priority_size
            priority_size = 1

        priority_range = list(result.values())
        # priority_movie_name = list(result.keys())
        highest_range = max(priority_range)
        if highest_range > 1:
            for key, value in result.items():
                if value not in final_result:
                    final_result[value] = [key]
                else:
                    final_result[value].append(key)

            for name in final_result[highest_range]:
                admin_reply = ''
                for link in movielinks.movies_ids[name]:
                    bot.send_message(chat_id=chat_id, text=MLINK + link, reply_to_message_id=msg_id)
                    if admin_reply != name:
                        bot.send_message(chat_id=admin_chat_id1,')
                        bot.send_message(chat_id=admin_chat_id2,')
                        admin_reply = name
        else:
            keyboard1 = [
                [InlineKeyboardButton('Click Here To Check Spelling', url='https://www.google.com/search?q='+msg+' movie')]
            ]
            keyboard2 = [
                [InlineKeyboardButton('Developed By King_webseries', url='https://telegram.me/king_webseries')]
            ]
            reply_markup1 = InlineKeyboardMarkup(keyboard1)
            reply_markup2 = InlineKeyboardMarkup(keyboard2)
            reply_msg = 'If the \'MOVIE NAME\' is incorrect please check the spelling in google.'
            bot.send_message(chat_id=chat_id, text=reply_msg, reply_markup=reply_markup1, reply_to_message_id=msg_id)
            bot.send_message(chat_id=chat_id, text='Otherwise we will upload your requested movie as soon as possible.', reply_markup=reply_markup2, reply_to_message_id=msg_id)
            bot.send_message(chat_id=admin_chat_id1, text='User : @'+username+' Asked Movie name : '+msg+' #Not_Available Admin. Please upload movie as soon as possible.')
            bot.send_message(chat_id=admin_chat_id2, text='User : @'+username+' Asked Movie name : '+msg+' #Not_Available Admin. Please upload movie as soon as possible.')
    except:
        bot.send_message(chat_id=chat_id, text='Your Movie Not Exists We Will Upload As Soon As Possible. ', reply_to_message_id=msg_id)
        bot.send_message(chat_id=admin_chat_id1, text='User : @'+username+' Asked Movie name : '+msg+' #Not_Available Admin. Please upload movie as soon as possible.')
        bot.send_message(chat_id=admin_chat_id2, text='User : @'+username+' Asked Movie name : '+msg+' #Not_Available Admin. Please upload movie as soon as possible.')

def movie_request(update, context):
    username = update.message.chat.username
    username = str(username)
    msg = update.effective_message.text
    msg = msg.replace('movies', '')
    msg = msg.replace('movie', '')
    msg = msg.replace('links', '')
    msg = msg.replace('link', '')
    msg = msg.replace('files', '')
    msg = msg.replace('file', '')
    # msg = msg.replace(' ', '')
    msg = msg.lower()
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    if msg == '':
        bot.send_message(chat_id=chat_id,text='Please ask the movie name without spelling mistake.', reply_to_message_id = msg_id)
    elif msg == 'hi' or msg == 'hii' or msg == 'hiii' or msg == 'thanks' or msg == 'thank':
        bot.send_message(chat_id=chat_id, text='Please don\'t send like this only ask movie names', reply_to_message_id = msg_id)
    else:
        movie(msg, username, chat_id, msg_id)

def error(update, context):
    logging.error(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    Updater = Updater(API_KEY, use_context=True)

    dp = Updater.dispatcher
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(MessageHandler(Filters.text, movie_request))

    dp.add_error_handler(error)
    Updater.start_polling(5)
    Updater.idle()
