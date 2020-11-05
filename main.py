# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from design import Ui_Dialog

#TODO: Добавить кнопку настроек; Добавить настройки пользолвателя, Color Picker, Smile Choose

#Creaate App
app = QtWidgets.QApplication(sys.argv)
#init
Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

HOST = 'http://101kinopoisk.com/'

# URL = 'http://101kinopoisk.com/films/drama/28748-ekstaz-2018.html'

WEBHOOK_URL = 'https://discord.com/api/webhooks/772936761256443915/mSrrgtTh-tHS-w7k6UVrPCBRcmKivhJH5YjpqIWLoY4asK2th_dYv4XhsBMgyxPNFjHl'

#Обход защиты от скриптов
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html, url):
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('div', class_='b-post__title').get_text()
    description = soup.find('div', class_='b-post__description_text').get_text(strip=True)
    image = soup.find('div', class_='b-sidecover').find('img').get('src')
    rate_KP = soup.find('span', class_='b-post__info_rates kp').find('span').get_text()
    rate_imdb = soup.find('span', class_='b-post__info_rates imdb').find('span').get_text()

    webhook = DiscordWebhooks(WEBHOOK_URL)
    webhook.set_content(title=f'**{ui.lineEdit_smile1.text()} {title} {ui.lineEdit_smile2.text()}**', url=url, color=0x00AAFF)
    webhook.add_field(name='Информация о фильме', value=f"*{description}*")
    webhook.set_thumbnail(url=image)
    webhook.set_image(url=image)

    webhook.set_author(name='Сергей Алексеевич', url='https://vk.com/havename' ,icon_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.CG4ws6IcT3PCEx0T7Xim5QHaEU%26pid%3DApi&f=1')
    webhook.add_field(inline=True, name=':flag_ru: Рейтинг Кинопоиск: ', value=f'{rate_KP}')
    webhook.add_field(inline=True, name=':flag_us: Рейтинг IMDb: ', value=f'{rate_imdb}')
    webhook.set_footer(text=f'Дата выхода {ui.lineEdit_Year.text()} год  |  \nДлительность фильма {ui.lineEdit_time.text()} мин  |  Возрасное ограничение {ui.lineEdit_Age.text()}+', icon_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.pngpix.com%2Fwp-content%2Fuploads%2F2016%2F07%2FPNGPIX-COM-Popcorn-PNG-Image.png&f=1&nofb=1')

    # #Отправка в Discord
    webhook.send()



def parser():
    url = ui.lineEdit_link.text()
    if url == '':
        print('error')
        ui.lineEdit_link.setText('http://101kinopoisk.com/films/horror/549-sinister-2012.html')
    else:
        html = get_html(url)
        if html.status_code == 200:
            get_content(html.text, url)
            print('Сообщение успешно отправлено!')
        else:
            print('Error')


#code
ui.pushButton.clicked.connect(lambda: parser())

# Main Loop
sys.exit(app.exec_())