# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
import discord
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from design import Ui_Main
from settings import Ui_Settings

#TODO: Добавить кнопку настроек; Добавить настройки пользователя, Color Picker, Smile Choose

#Creaate App
app = QtWidgets.QApplication(sys.argv)
#init
Dialog = QtWidgets.QDialog()
ui = Ui_Main()
ui.setupUi(Dialog)
Dialog.show()

#Create App Settings
app2 = QtWidgets.QApplication(sys.argv)
Settings = QtWidgets.QDialog()
ui2 = Ui_Settings()
ui2.setupUi(Settings)

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

def get_content(html, url, color):
    soup = BeautifulSoup(html, 'html.parser')

    table = []

    for td in soup.find('table').parent.find_all('td'):
        table.append(td.getText())

    # print(f'Слоган: {table[3]}')
    # print(f'Дата выхода: {table[5]}')
    # print(f'Страна: {table[7]}')
    # print(f'Режисер: {table[9]}')
    # print(f'Возрастное ограничение: {table[17]}')
    # print(f'Длительность: {table[19]}')

    title = soup.find('div', class_='b-post__title').get_text()
    description = soup.find('div', class_='b-post__description_text').get_text(strip=True)
    image = soup.find('div', class_='b-sidecover').find('img').get('src')
    rate_KP = soup.find('span', class_='b-post__info_rates kp').find('span').get_text()
    rate_imdb = soup.find('span', class_='b-post__info_rates imdb').find('span').get_text()

    webhook = DiscordWebhooks(WEBHOOK_URL)

    webhook.set_content(title=f'{ui.smile1.currentText()} **{title}** {ui.smile2.currentText()}', url=url, color=color)
    webhook.add_field(inline=True, name='Слоган', value=table[3])
    webhook.add_field(inline=True, name='Режисер', value=table[9])
    webhook.add_field(name='Информация о фильме', value=f'*{description}*')
    webhook.add_field(name='Смотреть онлайн бесплатно', value=f'{url}')
    webhook.set_thumbnail(url=image)
    webhook.set_image(url=image)

    webhook.set_author(name='Сергей Алексеевич', url='https://vk.com/havename' ,icon_url='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse4.mm.bing.net%2Fth%3Fid%3DOIP.CG4ws6IcT3PCEx0T7Xim5QHaEU%26pid%3DApi&f=1')
    webhook.add_field(inline=True, name=':map: Страна:', value=table[7])
    webhook.add_field(inline=True, name=':flag_ru: Рейтинг Кинопоиск: ', value=f'{rate_KP}')
    webhook.add_field(inline=True, name=':flag_us: Рейтинг IMDb: ', value=f'{rate_imdb}')
    webhook.set_footer(
        text=f'Дата выхода {table[5]}  |  Длительность фильма {table[19]}\nВозрасное ограничение {table[17]}',
        icon_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.pngpix.com%2Fwp-content%2Fuploads%2F2016%2F07%2FPNGPIX-COM-Popcorn-PNG-Image.png&f=1&nofb=1')

    # #Отправка в Discord
    webhook.send()



def parser():
    url = ui.lineEdit_link.text()
    color = ui.lineEdit_color.text()
    print(color)
    print(type(color))

    if url == '':
        print('Поле пустое! Заполняю контентом..')
        ui.lineEdit_link.setText('http://getkinopoisk.com/films/horror/549-sinister-2012.html')
    else:
        try:
            html = get_html(url)
            if html.status_code == 200:
                get_content(html.text, url, color)
                print('Сообщение успешно отправлено!')
            else:
                print('Error')
        except:
            print('Ошибка!\nДанный URL заблокирован или введен не верно!')


#code
# print(type(0xAD16F0)) # Открытие века!

ui.pushButton.clicked.connect(lambda: parser())
ui.toolButton.clicked.connect(lambda: Settings.show())

# Main Loop
sys.exit(app.exec_())
sys.exit(app2.exec_())