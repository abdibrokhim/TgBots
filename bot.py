# with Django
# en version

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,

)

from babel.support import Translations

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    filters,
    MessageHandler,

)

from telegram.constants import ParseMode

import os
import requests
import logging
import time

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

# start Django
import sys

sys.dont_write_bytecode = True

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django

django.setup()

from app import models, serializers
from config import settings

from asgiref.sync import sync_to_async

# end Django

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = '5538417603:AAGny-20v6DK2bD77wPr5TJv8o1X48T5HZo'  #test token
VIDEO_FILE_PATH = 'video/video.mp4'
AUDIO_FILE_PATH = 'audio/audio.mp3'
CHANNEL_LINK = 'https://t.me/prmngr'
COMMUNITY_LINK = 'https://t.me/thesaver1chat'
CHANNEL_USERNAME = '@prmngr'
COMMUNITY_USERNAME = '@thesaver1chat'



_bots = """
🤖 Useful Bots:

    🤖 @thesaver_bot (Uzbek version)
    🤖 @insta_downder_bot
    🤖 @usellbuybot
    🤖 @musicfindmebot (new version)
    🤖 @anonyiobot
    🤖 @tiktoknowater_bot (new version)
    🤖 @music_recognizerBot
    🤖 @tiktokwatermark_removerBot
    
📞 Contact: @abdibrokhim
📞 Contact: @contactdevsbot

📢 Channel: @prmngr

👻 Developer: @abdibrokhim
👻 Developer: https://github.com/abdibrokhim

☕️ Buy me Coffee: 

    💳 Visa: 4023 0602 4638 1551
    🪙 Bitcoin: bc1qpylxaqwapk0tgdmpnnljj545z4lk2z9q5us6p6
    
"""

_ads = """
🗣 Contact us:

    🤖 @contactdevsbot
    👻 @abdibrokhim
    
🗣 Join Channel: @prmngr
🗣 Join Community: @thesaver1chat

🗣 Ads: @prmngr
🗣 News/Updates: @prmngr

☕️ Buy me Coffee: 

    💳 Visa: 4023 0602 4638 1551
    🪙 Bitcoin: bc1qpylxaqwapk0tgdmpnnljj545z4lk2z9q5us6p6
    
"""

_about = """
🌝 You can download videos and audios from Instagram, Facebook, YouTube, Shazam and TikTok.

🗣 To get more information about bot, use /doc command.

🗣 To get more information about other useful bots, use /bots command.

🗣 To get more information about ads/news/updates, use /ads command.

🗣 Join our channel: @prmngr
🗣 Join our community: @thesaver1chat

☕️ Buy me Coffee: 

    💳 Visa: 4023 0602 4638 1551
    🪙 Bitcoin: bc1qpylxaqwapk0tgdmpnnljj545z4lk2z9q5us6p6
    
"""

_commands = """
🤖 /start - Start bot

🤖 /menu - Main menu

🤖 /instagram - Browse Instagram

🤖 /facebook - Browse Facebook

🤖 /youtube - Browse YouTube

🤖 /shazam - Browse Shazam

🤖 /tiktok - Browse TikTok

🤖 /doc - Documentation

🤖 /ads - Ads/News/Updates

🤖 /bots - Useful Bots

🤖 /cmd - Commands

🤖 /end - End bot

☕️ Buy me Coffee: 

    💳 Visa: 4023 0602 4638 1551
    🪙 Bitcoin: bc1qpylxaqwapk0tgdmpnnljj545z4lk2z9q5us6p6

"""

(MAIN,
 INSTAGRAM,
 FACEBOOK,
 YOUTUBE,
 SPOTIFY,
 TIKTOK,
 INSTAGRAM_POST,
 INSTAGRAM_REEL,
 INSTAGRAM_STORY,
 FACEBOOK_REEL,
 YOUTUBE_REEL,
 SPOTIFY_MUSIC,
 SPOTIFY_ARGS,
 TIKTOK_REEL) = range(14)


# Post TGClient
@sync_to_async
def _post_client(user):
    models.TGClient(
        tg_id=user.id,
    ).save()


# Get TGClient list
@sync_to_async
def _get_clients():
    return models.TGClient.objects.all().values()


# Check TGClient
@sync_to_async
def _is_client(user):
    client = models.TGClient.objects.select_related().filter(tg_id=user.id)
    if client:
        return True
    else:
        return False


# Post TGClient Query
@sync_to_async
def _post_query(user_id, query):
    models.TGClientQuery(
        tg_id=user_id,
        query=query,
    ).save()


async def doc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_about)


async def cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_commands)


async def ads_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_ads)


async def bots_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=_bots)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not await _is_client(user):
        await _post_client(user)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('↗️ Join Channel', url=CHANNEL_LINK)],
                                         [InlineKeyboardButton('↗️ Join Community', url=COMMUNITY_LINK)]])

    await update.message.reply_text("Welcome, {}!".format(user.first_name))
    await update.message.reply_text(
        "Was-sap!\n\nClick /menu and start Browse\n\n⬇️ Stay in touch! ⬇️",
        reply_markup=reply_markup)


async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # member = await context.bot.getChatMember(chat_id=CHANNEL_USERNAME, user_id=update.effective_user.id)

    buttons = [
        [
            KeyboardButton(text="🟣 Instagram", ),
        ],
        [
            KeyboardButton(text="🔵 Facebook", ),
        ],
        [
            KeyboardButton(text="🔴 YouTube", ),
        ],
        [
            KeyboardButton(text="🟢 Shazam", ),
        ],
        [
            KeyboardButton(text="🟡 TikTok", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(
        "Choose an option\n\nClick /doc to learn more\n\nAds /ads, Useful Bots /bots",
        reply_markup=reply_markup)

    return MAIN


async def instagram_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🟣 Post", ),
        ],
        [
            KeyboardButton(text="🟣 Reel", ),
        ],
        [
            KeyboardButton(text="🟣 Stories", ),
        ],
        [
            KeyboardButton(text="🔙 Back", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Choose an option",
                                    reply_markup=reply_markup)

    return INSTAGRAM


async def facebook_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🔵 Video", ),
        ],
        [
            KeyboardButton(text="🔙 Back", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Choose an option",
                                    reply_markup=reply_markup)

    return FACEBOOK


async def youtube_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🔴 Video", ),
        ],
        [
            KeyboardButton(text="🔙 Back", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Choose an option",
                                    reply_markup=reply_markup)

    return YOUTUBE


async def spotify_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🟢 Voice message", ),
        ],
        [
            KeyboardButton(text="🟢 Song/Singer", ),
        ],
        [
            KeyboardButton(text="🔙 Back", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Choose an option",
                                    reply_markup=reply_markup)

    return SPOTIFY


async def tiktok_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🟡 Video", ),
        ],
        [
            KeyboardButton(text="🔙 Back", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Choose an option",
                                    reply_markup=reply_markup)

    return TIKTOK


async def instagram_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send Instagram Post link",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Back"]],
                                        resize_keyboard=True))

    return INSTAGRAM_POST


async def instagram_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send Instagram Reel link",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Back"]],
                                        resize_keyboard=True))
    return INSTAGRAM_REEL


async def instagram_story_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send Instagram Story link or username",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Back"]],
                                        resize_keyboard=True))
    return INSTAGRAM_STORY


async def facebook_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send Facebook video link",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Back"]],
                                        resize_keyboard=True))
    return FACEBOOK_REEL


async def youtube_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send YouTube video link",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Back"]],
                                        resize_keyboard=True))
    return YOUTUBE_REEL


async def spotify_voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send Voice message",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Back"]],
                                        resize_keyboard=True))
    return SPOTIFY_MUSIC


async def spotify_args_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send name of Song or Singer and limit\n\nExample: Sad 5",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Back"]],
                                        resize_keyboard=True))
    return SPOTIFY_ARGS


async def tiktok_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send TikTok video link",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Back"]],
                                        resize_keyboard=True))
    return TIKTOK_REEL


async def instagram_post_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Searching...')
        url = "https://instagram-story-downloader-media-downloader.p.rapidapi.com/index"

        querystring = {"url": link}

        headers = {
            "X-RapidAPI-Key": "abdcae06e1msh6684906bfdbf574p134a43jsne849763a8cb4",
            "X-RapidAPI-Host": "instagram-story-downloader-media-downloader.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)

        result = response.json()

        try:
            for i in result['media']:
                await update.message.reply_photo(photo=i, caption='\n@thesaver1_bot', write_timeout=100)
        except Exception as e:
            print(e)
            await update.message.reply_photo(photo=result['media'], caption='\n@thesaver1_bot', write_timeout=100)
    else:
        await update.message.reply_text(text='Send link again')

    return INSTAGRAM


async def instagram_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Searching...')
        url = "https://instagram-story-downloader-media-downloader.p.rapidapi.com/index"

        querystring = {"url": link}

        headers = {
            "X-RapidAPI-Key": "abdcae06e1msh6684906bfdbf574p134a43jsne849763a8cb4",
            "X-RapidAPI-Host": "instagram-story-downloader-media-downloader.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)

        result = response.json()

        try:
            response = requests.get(result['media'])
            with open(VIDEO_FILE_PATH, 'wb') as f:
                f.write(response.content)

            await update.message.reply_video(video=open(VIDEO_FILE_PATH, 'rb'),
                                             caption='\n@thesaver1_bot', write_timeout=1000)

            os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            await update.message.reply_text(text='❌ Link is not valid')
    else:
        await update.message.reply_text(text='Send link again')

    return INSTAGRAM


async def instagram_story_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Searching...')
        url = "https://instagram-story-downloader-media-downloader.p.rapidapi.com/story/index"

        querystring = {"url": link}

        headers = {
            "X-RapidAPI-Key": "abdcae06e1msh6684906bfdbf574p134a43jsne849763a8cb4",
            "X-RapidAPI-Host": "instagram-story-downloader-media-downloader.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)

        result = response.json()
        try:
            for i in result['stories']:
                if i['type'] == 'Image':
                    await update.message.reply_photo(photo=i['media'], caption='\n@thesaver1_bot', write_timeout=100)
                if i['type'] == 'Video':
                    response = requests.get(i['media'])
                    with open(VIDEO_FILE_PATH, 'wb') as f:
                        f.write(response.content)

                    await update.message.reply_video(video=open(VIDEO_FILE_PATH, 'rb'),
                                                     caption='\n@thesaver1_bot', write_timeout=1000)

                    os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            if result['type'] == 'Image':
                await update.message.reply_photo(photo=result['media'], caption='\n@thesaver1_bot', write_timeout=100)
            if result['type'] == 'Video':
                response = requests.get(result['media'])
                with open(VIDEO_FILE_PATH, 'wb') as f:
                    f.write(response.content)

                await update.message.reply_video(video=open(VIDEO_FILE_PATH, 'rb'),
                                                 caption='\n@thesaver1_bot', write_timeout=1000)

                os.remove(VIDEO_FILE_PATH)
    else:
        await update.message.reply_text(text='Send link again')

    return INSTAGRAM


async def facebook_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Searching...')
        url = "https://facebook-reel-and-video-downloader.p.rapidapi.com/app/main.php"

        querystring = {"url": link}

        headers = {
            "X-RapidAPI-Key": "6a90d6d4efmsh32f9758380f3589p11e571jsn642878f330b1",
            "X-RapidAPI-Host": "facebook-reel-and-video-downloader.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

        result = response.json()

        try:
            response = requests.get(result['links']['Download High Quality'])
            with open(VIDEO_FILE_PATH, 'wb') as f:
                f.write(response.content)

            await update.message.reply_video(video=open(VIDEO_FILE_PATH, 'rb'),
                                             caption='\n@thesaver1_bot', write_timeout=1000)

            os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            await update.message.reply_text(text='❌ Link is not valid')
    else:
        await update.message.reply_text(text='Send link again')

    return FACEBOOK


async def youtube_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text

    await _post_query(user.id, link)

    await update.message.reply_text(text='❌ An error has occurred')

    return YOUTUBE


async def spotify_voice_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Search and Identify song function"""
    user = update.effective_user

    args = await update.message.voice.get_file()
    file_path = args['file_path']
    response = requests.get(file_path, allow_redirects=True)

    await update.message.reply_text(text='🔎 Searching...')

    open(AUDIO_FILE_PATH, 'wb').write(response.content)

    url = "http://38.242.138.39/recognize-track/"
    response = requests.request("POST", url, headers={'accept': 'application/json'},
                                files={'audio': open(AUDIO_FILE_PATH, 'rb')}, )
    result = response.json()

    if len(result['link']['matches']) != 0:
        title = result['link']['track']['share']['subject']
        preview = result['link']['track']['hub']['actions'][1]['uri']

        await _post_query(user.id, title)

        os.remove(AUDIO_FILE_PATH)
        FILE_PATH = f'audio/{title}.mp3'

        open(FILE_PATH, 'wb').write(requests.get(preview, allow_redirects=True).content)
        await update.message.reply_audio(audio=open(FILE_PATH, 'rb'),
                                         title=title, caption='\n@thesaver1_bot', write_timeout=100,)

        os.remove(FILE_PATH)
    else:
        txt = '❌ Nothing to show!'
        await update.message.reply_text(text=txt)

        os.remove(AUDIO_FILE_PATH)

    return SPOTIFY


async def spotify_args_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = update.message.text
    args = args.split(' ')
    query = ' '.join(args[:-1])
    limit = args[-1]

    print(args)

    if args != '':
        await _post_query(user.id, args)
        # array = ""

        await update.message.reply_text(text='🔎 Searching...')
        url = "http://38.242.138.39/search_track/"

        response = requests.request("POST", url, headers={'accept': 'application/json'}, json={'query': query, 'limit': limit})
        result = response.json()

        result_length = len(result['data']['tracks']['hits'])

        for i in range(0, result_length):
            subject = result['data']['tracks']['hits'][i]['share']['subject']
            previewurl = result['data']['tracks']['hits'][i]['stores']['apple']['previewurl']

            print(subject)
            print(previewurl)

            txt = f"""<b><a href="{previewurl}">{subject}</a></b>"""

            # array += f"{txt}" + "\n\n"

            try:
                await update.message.reply_text(text=txt + '\n@thesaver1_bot', write_timeout=100, parse_mode=ParseMode.HTML,)
            except Exception as e:
                print(e)
                await update.message.reply_text(text="❌ An error has occurred!", write_timeout=100,)
    else:
        await update.message.reply_text(text='Send name of Song or Singer and limit\n\nExample: Sad 5')

    return SPOTIFY


async def tiktok_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Searching...')
        url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

        querystring = {"url": link, 'hd': '0'}

        headers = {
            "X-RapidAPI-Key": "6a90d6d4efmsh32f9758380f3589p11e571jsn642878f330b1",
            "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        link = response.json()
        # print(link)
        link = link['data']['play']
        print(link)

        try:
            response = requests.get(link)
            with open(VIDEO_FILE_PATH, 'wb') as f:
                f.write(response.content)

            await update.message.reply_video(video=open(VIDEO_FILE_PATH, 'rb'),
                                             caption='\n@thesaver1_bot', write_timeout=1000)

            os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            await update.message.reply_text(text='❌ Link is not valid')
    else:
        await update.message.reply_text(text='Send link again')

    return TIKTOK


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Canceled")
    await update.message.reply_text("Click /start to start again", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


async def report_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _cls = ""

    cls = await _get_clients()

    if cls:
        for i in cls:
            _cls += 'ID: ' + i['tg_id'] + '\nClient since: ' + str(i['created_at']) + '\n\n'

        await update.message.reply_text(text=_cls)
        await update.message.reply_text(text='Total: ' + str(len(cls)))

    else:
        await update.message.reply_text(text='Error')


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).read_timeout(100).get_updates_read_timeout(100).build()
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
            CommandHandler('menu', menu_handler),
            CommandHandler('doc', doc_handler),
        ],
        states={
            MAIN: [
                MessageHandler(filters.Regex(".*Instagram$"), instagram_handler),
                MessageHandler(filters.Regex(".*Facebook$"), facebook_handler),
                MessageHandler(filters.Regex(".*YouTube$"), youtube_handler),
                MessageHandler(filters.Regex(".*Shazam$"), spotify_handler),
                MessageHandler(filters.Regex(".*TikTok$"), tiktok_handler),
            ],
            INSTAGRAM: [
                MessageHandler(filters.Regex(".*Post$"), instagram_post_handler),
                MessageHandler(filters.Regex(".*Reel$"), instagram_reel_handler),
                MessageHandler(filters.Regex(".*Stories$"), instagram_story_handler),
                MessageHandler(filters.Regex(".*Back$"), menu_handler),
            ],
            FACEBOOK: [
                MessageHandler(filters.Regex(".*Video$"), facebook_reel_handler),
                MessageHandler(filters.Regex(".*Back$"), menu_handler),
            ],
            YOUTUBE: [
                MessageHandler(filters.Regex(".*Video$"), youtube_reel_handler),
                MessageHandler(filters.Regex(".*Back$"), menu_handler),
            ],
            SPOTIFY: [
                MessageHandler(filters.Regex(".*Voice message$"), spotify_voice_handler),
                MessageHandler(filters.Regex(".*Song/Singer$"), spotify_args_handler),
                MessageHandler(filters.Regex(".*Back$"), menu_handler),
            ],
            TIKTOK: [
                MessageHandler(filters.Regex(".*Video$"), tiktok_reel_handler),
                MessageHandler(filters.Regex(".*Back$"), menu_handler),
            ],
            INSTAGRAM_POST: [
                MessageHandler(filters.Regex(".*Back$"), instagram_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), instagram_post_link_handler)
            ],
            INSTAGRAM_REEL: [
                MessageHandler(filters.Regex(".*Back$"), instagram_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), instagram_reel_link_handler)
            ],
            INSTAGRAM_STORY: [
                MessageHandler(filters.Regex(".*Back$"), instagram_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), instagram_story_link_handler)
            ],
            FACEBOOK_REEL: [
                MessageHandler(filters.Regex(".*Back$"), facebook_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), facebook_reel_link_handler)
            ],
            YOUTUBE_REEL: [
                MessageHandler(filters.Regex(".*Back$"), youtube_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), youtube_reel_link_handler)
            ],
            SPOTIFY_MUSIC: [
                MessageHandler(filters.Regex(".*Back$"),  spotify_handler),
                MessageHandler(filters.VOICE & (~filters.COMMAND), spotify_voice_msg_handler)
            ],
            SPOTIFY_ARGS: [
                MessageHandler(filters.Regex(".*Back$"), spotify_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), spotify_args_msg_handler)
            ],
            TIKTOK_REEL: [
                MessageHandler(filters.Regex(".*Back$"), tiktok_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), tiktok_reel_link_handler)
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
            CommandHandler('start', start_handler),
            CommandHandler('menu', menu_handler),
            CommandHandler('instagram', instagram_handler),
            CommandHandler('facebook', facebook_handler),
            CommandHandler('youtube', youtube_handler),
            CommandHandler('shazam', spotify_handler),
            CommandHandler('tiktok', tiktok_handler),
            CommandHandler('doc', doc_handler),
            CommandHandler('ads', ads_handler),
            CommandHandler('cmd', cmd_handler),
            CommandHandler('bots', bots_handler),
            CommandHandler('r', report_handler),
        ],
    )

    app.add_handler(conv_handler)

    app.add_error_handler(error_handler)


    print("updated...")
    app.run_polling()
