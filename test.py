from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,

)

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

TELEGRAM_BOT_TOKEN = '5538417603:AAGny-20v6DK2bD77wPr5TJv8o1X48T5HZo'
VIDEO_FILE_PATH = 'video/video.mp4'
AUDIO_FILE_PATH = 'audio/audio.mp3'
CHANNEL_LINK = 'https://t.me/prmngr'
CHANNEL_USERNAME = '@prmngr'


_bots = """
🤖 Bizning Botlar:

    🤖 @thesaver_bot
    🤖 @insta_downder_bot
    🤖 @usellbuybot
    🤖 @musicfindmebot (yengi versiya)
    🤖 @anonyiobot
    🤖 @tiktoknowater_bot (yengi versiya)
    🤖 @music_recognizerBot
    🤖 @tiktokwatermark_removerBot
    
📞 Contact: @abdibrokhim
📞 Contact: @contactdevsbot

📢 Channel: @prmngr

👻 Developer: @abdibrokhim
"""

_ads = """
🗣 Biz bilan bog\'lanish uchun:

    🤖 @contactdevsbot
    👻 @abdibrokhim
    
🗣 Bizning kanal: @prmngr
🗣 Reklama: @prmngr
🗣 Yangiliklar: @prmngr

🗣 Xullas hamma narsa shetda, krurasila 💩: @prmngr
"""

_about = """
🌝 Bu bot orqali siz Instagram, Facebook, YouTube, Shazam, TikTok va boshqalarida video, audio, post, story, reel va boshqalarini yuklab olish imkoniyatiga ega bo'lasiz.

🗣 "Command"lar xaqida to\'liq ma\'lumot olish uchun /cmd buyrug\'ini yuboring

🗣 Taklif, murojat, reklama va xokazo, /ads buyrug\'ini yuboring

🗣 Barcha Botlarimiz haqida to\'liq ma\'lumot olish uchun, /bots buyrug\'ini yuboring

🗣 Kanalimizga a'zo bo'ling: @prmngr
"""

_commands = """
🤖 /start - Botni ishga tushirishh️ 

🤖 /menu - Bosh Menu

🤖 /instagram - Instagram dan qidirish

🤖 /facebook - Facebook dan qidirish

🤖 /youtube - YouTube dan qidirish

🤖 /shazam - Shazam dan qidirish

🤖 /tiktok - TikTok dan qidirish

🤖 /cancel - Botni tuxtatish

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

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('↗️ Kanalga go', url=CHANNEL_LINK)]])

    await update.message.reply_text("Assalomu alaykum, {}!".format(user.first_name))
    await update.message.reply_text(
        "Botga xush kelibsiz\n\nBotdan foydalanish uchun /menu bosing\n\n⬇️ Kanalimizga obuna bo'ling! ⬇️",
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
        "Quyidagi ko'rsatilgan menyudan o'zingizga kerakli bo'limni tanlang\n\nTo\'liq ma\'lumot olish uchun /doc bosing\n\nReklama /ads, Botlar /bots",
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
            KeyboardButton(text="🔙 Orqaga", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Quyidagi ko'rsatilgan menyudan o'zingizga kerakli bo'limni tanlang",
                                    reply_markup=reply_markup)

    return INSTAGRAM


async def facebook_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🔵 Video", ),
        ],
        [
            KeyboardButton(text="🔙 Orqaga", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Quyidagi ko'rsatilgan menyudan o'zingizga kerakli bo'limni tanlang",
                                    reply_markup=reply_markup)

    return FACEBOOK


async def youtube_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🔴 Video", ),
        ],
        [
            KeyboardButton(text="🔙 Orqaga", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Quyidagi ko'rsatilgan menyudan o'zingizga kerakli bo'limni tanlang",
                                    reply_markup=reply_markup)

    return YOUTUBE


async def spotify_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🟢 Ovozli xabar", ),
        ],
        [
            KeyboardButton(text="🟢 Nomi/Ijrochisi", ),
        ],
        [
            KeyboardButton(text="🔙 Orqaga", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Quyidagi ko'rsatilgan menyudan o'zingizga kerakli bo'limni tanlang",
                                    reply_markup=reply_markup)

    return SPOTIFY


async def tiktok_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            KeyboardButton(text="🟡 Video", ),
        ],
        [
            KeyboardButton(text="🔙 Orqaga", ),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text("Quyidagi ko'rsatilgan menyudan o'zingizga kerakli bo'limni tanlang",
                                    reply_markup=reply_markup)

    return TIKTOK


async def instagram_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Instagram post linkini yuboring",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Orqaga"]],
                                        resize_keyboard=True))

    return INSTAGRAM_POST


async def instagram_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Instagram reel linkini yuboring",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Orqaga"]],
                                        resize_keyboard=True))
    return INSTAGRAM_REEL


async def instagram_story_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Instagram story username/linkini yuboring",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Orqaga"]],
                                        resize_keyboard=True))
    return INSTAGRAM_STORY


async def facebook_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Facebook video linkini yuboring",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Orqaga"]],
                                        resize_keyboard=True))
    return FACEBOOK_REEL


async def youtube_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Youtube linkini yuboring",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Orqaga"]],
                                        resize_keyboard=True))
    return YOUTUBE_REEL


async def spotify_voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ovozli xabar yuboring",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Orqaga"]],
                                        resize_keyboard=True))
    return SPOTIFY_MUSIC


async def spotify_args_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Musiqa nomi yoki ijrochisi va maksimal natija yuboring\n\nMasalan: Yurak 5",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Orqaga"]],
                                        resize_keyboard=True))
    return SPOTIFY_ARGS


async def tiktok_reel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tiktok video linkini yuboring",
                                    reply_markup=ReplyKeyboardMarkup([
                                        ["🔙️ Orqaga"]],
                                        resize_keyboard=True))
    return TIKTOK_REEL


async def instagram_post_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Izlanmoqda...')
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
                await update.message.reply_photo(photo=i, caption='\n@thesaver_bot', write_timeout=100)
        except Exception as e:
            print(e)
            await update.message.reply_photo(photo=result['media'], caption='\n@thesaver_bot', write_timeout=100)
    else:
        await update.message.reply_text(text='Linkingizni yuboring')

    return INSTAGRAM


async def instagram_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Izlanmoqda...')
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
                                             caption='\n@thesaver_bot', write_timeout=1000)

            os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            await update.message.reply_text(text='❌ Bu linkda hech narsa yo\'q')
    else:
        await update.message.reply_text(text='Linkingizni yuboring')

    return INSTAGRAM


async def instagram_story_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Izlanmoqda...')
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
                    await update.message.reply_photo(photo=i['media'], caption='\n@thesaver_bot', write_timeout=100)
                if i['type'] == 'Video':
                    response = requests.get(i['media'])
                    with open(VIDEO_FILE_PATH, 'wb') as f:
                        f.write(response.content)

                    await update.message.reply_video(video=open(VIDEO_FILE_PATH, 'rb'),
                                                     caption='\n@thesaver_bot', write_timeout=1000)

                    os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            if result['type'] == 'Image':
                await update.message.reply_photo(photo=result['media'], caption='\n@thesaver_bot', write_timeout=100)
            if result['type'] == 'Video':
                response = requests.get(result['media'])
                with open(VIDEO_FILE_PATH, 'wb') as f:
                    f.write(response.content)

                await update.message.reply_video(video=open(VIDEO_FILE_PATH, 'rb'),
                                                 caption='\n@thesaver_bot', write_timeout=1000)

                os.remove(VIDEO_FILE_PATH)
    else:
        await update.message.reply_text(text='Linkingizni yuboring')

    return INSTAGRAM


async def facebook_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Izlanmoqda...')
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
                                             caption='\n@thesaver_bot', write_timeout=1000)

            os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            await update.message.reply_text(text='❌ Bu linkda hech narsa yo\'q')
    else:
        await update.message.reply_text(text='Linkingizni yuboring')

    return FACEBOOK


async def youtube_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text

    await _post_query(user.id, link)

    await update.message.reply_text(text='❌ Xatolik yuz berdi!')

    return YOUTUBE


async def spotify_voice_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Search and Identify song function"""
    user = update.effective_user

    args = await update.message.voice.get_file()
    file_path = args['file_path']
    response = requests.get(file_path, allow_redirects=True)

    await update.message.reply_text(text='🔎 Izlanmoqda...')

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
                                         title=title, caption='\n@thesaver_bot', write_timeout=100,)

        os.remove(FILE_PATH)
    else:
        txt = '❌ Topa olmadik!'
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

        await update.message.reply_text(text='🔎 Qidirilmoqda...')
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
                await update.message.reply_text(text=txt + '\n@thesaver_bot', write_timeout=100, parse_mode=ParseMode.HTML,)
            except Exception as e:
                print(e)
                await update.message.reply_text(text="❌ Xatolik yuz berdi, Iltimos qayta urinib ko'ring")
    else:
        await update.message.reply_text(text='Musiqa nomi yoki ijrochisini va maksimal natijani yuboring\n\nMasalan: Yurak 5')

    return SPOTIFY


async def tiktok_reel_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    link = update.message.text
    print(link)

    if link != '':
        await _post_query(user.id, link)

        await update.message.reply_text(text='🔎 Izlanmoqda...')
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
                                             caption='\n@thesaver_bot', write_timeout=1000)

            os.remove(VIDEO_FILE_PATH)
        except Exception as e:
            print(e)
            await update.message.reply_text(text='❌ Bu linkda hech narsa yo\'q')
    else:
        await update.message.reply_text(text='Linkingizni yuboring')

    return TIKTOK


async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi")
    await update.message.reply_text("Qaytadan boshlash uchun\n/start ni bosing", reply_markup=ReplyKeyboardRemove())
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
                MessageHandler(filters.Regex(".*Orqaga$"), menu_handler),
            ],
            FACEBOOK: [
                MessageHandler(filters.Regex(".*Video$"), facebook_reel_handler),
                MessageHandler(filters.Regex(".*Orqaga$"), menu_handler),
            ],
            YOUTUBE: [
                MessageHandler(filters.Regex(".*Video$"), youtube_reel_handler),
                MessageHandler(filters.Regex(".*Orqaga$"), menu_handler),
            ],
            SPOTIFY: [
                MessageHandler(filters.Regex(".*Ovozli xabar$"), spotify_voice_handler),
                MessageHandler(filters.Regex(".*Nomi/Ijrochisi$"), spotify_args_handler),
                MessageHandler(filters.Regex(".*Orqaga$"), menu_handler),
            ],
            TIKTOK: [
                MessageHandler(filters.Regex(".*Video$"), tiktok_reel_handler),
                MessageHandler(filters.Regex(".*Orqaga$"), menu_handler),
            ],
            INSTAGRAM_POST: [
                MessageHandler(filters.Regex(".*Orqaga$"), instagram_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), instagram_post_link_handler)
            ],
            INSTAGRAM_REEL: [
                MessageHandler(filters.Regex(".*Orqaga$"), instagram_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), instagram_reel_link_handler)
            ],
            INSTAGRAM_STORY: [
                MessageHandler(filters.Regex(".*Orqaga$"), instagram_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), instagram_story_link_handler)
            ],
            FACEBOOK_REEL: [
                MessageHandler(filters.Regex(".*Orqaga$"), facebook_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), facebook_reel_link_handler)
            ],
            YOUTUBE_REEL: [
                MessageHandler(filters.Regex(".*Orqaga$"), youtube_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), youtube_reel_link_handler)
            ],
            SPOTIFY_MUSIC: [
                MessageHandler(filters.Regex(".*Orqaga$"),  spotify_handler),
                MessageHandler(filters.VOICE & (~filters.COMMAND), spotify_voice_msg_handler)
            ],
            SPOTIFY_ARGS: [
                MessageHandler(filters.Regex(".*Orqaga$"), spotify_handler),
                MessageHandler(filters.TEXT & (~filters.COMMAND), spotify_args_msg_handler)
            ],
            TIKTOK_REEL: [
                MessageHandler(filters.Regex(".*Orqaga$"), tiktok_handler),
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
