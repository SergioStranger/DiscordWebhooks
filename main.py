# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks

HOST = 'http://101kinopoisk.com/'
URL = input('Адрес страницы: ')
# URL = 'http://101kinopoisk.com/films/drama/28748-ekstaz-2018.html'

WEBHOOK_URL = 'https://discord.com/api/webhooks/772580651038670888/HjWRHdAsuKeSXN5ToZFwOALSGZzh9fNVP_iWV9Wz0yX4ptgx4umqd7xQhec3YuqG5tq1'

#Обход защиты от скриптов
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('div', class_='b-post__title').get_text()
    description = soup.find('div', class_='b-post__description_text').get_text(strip=True)
    image = soup.find('div', class_='b-sidecover').find('img').get('src')
    rate_KP = soup.find('span', class_='b-post__info_rates kp').find('span').get_text()
    rate_imdb = soup.find('span', class_='b-post__info_rates imdb').find('span').get_text()
    age_limit = input('Введите возрастное ограниение: ')
    out_date = input('Год выхода: ')
    film_time = input('Длительность фильма: ')

    webhook = DiscordWebhooks(WEBHOOK_URL)
    webhook.set_content(title=f'**:film_frames: {title} :movie_camera:**', url=URL, color=0x00AAFF)
    webhook.add_field(name='Информация о фильме', value=f"*{description}*")
    webhook.set_thumbnail(url=image)
    webhook.set_image(url=image)

    webhook.set_author(name='Сергей Алексеевич', url='https://vk.com/havename' ,icon_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.CG4ws6IcT3PCEx0T7Xim5QHaEU%26pid%3DApi&f=1')
    webhook.add_field(inline=True, name=':flag_ru: Рейтинг Кинопоиск: ', value=f'{rate_KP}')
    webhook.add_field(inline=True, name=':flag_us: Рейтинг IMDb: ', value=f'{rate_imdb}')
    webhook.set_footer(text=f'Дата выхода {out_date} год  |  \nДлительность фильма {film_time} мин  |  Возрасное ограничение {age_limit}+', icon_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.pngpix.com%2Fwp-content%2Fuploads%2F2016%2F07%2FPNGPIX-COM-Popcorn-PNG-Image.png&f=1&nofb=1')

    # #Отправка в Discord
    webhook.send()


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
        print('Сообщение успешно отправлено!')
    else:
        print('Error')

parser()