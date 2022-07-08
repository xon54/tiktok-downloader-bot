import re
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'BOT_TOKEN_HERE'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

headers = {
    'Accept-language': 'en',
    'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
                  'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10'
}


def fetch_video_id(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find('link', {'rel': 'canonical'}).attrs['href']
    video_id = link.split('/')[-1:][0]
    return video_id


def get_video_link(video_id):
    request_url = f'https://api2.musical.ly/aweme/v1/aweme/detail/?aweme_id={video_id}'
    response = requests.get(request_url, headers=headers)
    uri = response.json()['aweme_detail']['video']['download_addr']['uri']
    video_link = f'https://api2-16-h2.musical.ly/aweme/v1/play/?video_id={uri}&vr_type=0&is_play_url=1&source' \
                 f'=PackSourceEnum_PUBLISH&media_type=4'
    return video_link


def download_video(url):
    video_id = fetch_video_id(url)
    video_link = get_video_link(video_id)
    return video_link


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(f'Добро пожаловать, {message.chat.first_name}!\n\nВы можете скинуть мне ссылку на видео в '
                        f'TikTok и через пару секунд этот видос будет у вас!\n\nНа данный момент, я поддерживаю '
                        f'только видео из TikTok!')


@dp.message_handler()
async def send_video(message: types.Message):
    if re.compile('https://[a-zA-Z]+.tiktok.com/').match(message.text):
        video_link = download_video(message.text)
        await message.reply_video(video_link, caption='Рад был помочь! Ваш, @GetTTVideoBot')
    else:
        await message.answer('⛔️ Вы прислали ссылку, которая не поддерживается ботом!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
