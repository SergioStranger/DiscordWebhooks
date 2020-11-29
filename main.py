# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
import json
from PyQt5 import QtWidgets
import sys
from design import Ui_Main
from settings import Ui_Settings

#TODO: Добавить Color Picker

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

#Обход защиты от скриптов
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; RMX1941 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/269.0.0.50.127;]'
}

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r

def push_content(html, url):
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

    with open('settings_file.json', 'r') as j:
        json_data = json.load(j)

    webhook = DiscordWebhooks(json_data[0]['DiscordWebhook'])

    webhook.set_content(title=f'{ui.smile1.currentText()} **{title}** {ui.smile2.currentText()}', url=url, color=0x00AAFF)
    webhook.add_field(inline=True, name='Слоган', value=table[3])
    webhook.add_field(inline=True, name='Режисер', value=table[9])
    webhook.add_field(name='Информация о фильме', value=f'*{description}*')
    webhook.add_field(name='Смотреть онлайн бесплатно', value=f'{url}')
    webhook.set_thumbnail(url=image)
    webhook.set_image(url=image)

    webhook.set_author(name=json_data[0]['UserName'], url=json_data[0]['UserLink'],
                       icon_url=json_data[0]['UserImage'])
    webhook.add_field(inline=True, name=':map: Страна:', value=table[7])
    webhook.add_field(inline=True, name=':flag_ru: Рейтинг Кинопоиск: ', value=f'{rate_KP}')
    webhook.add_field(inline=True, name=':flag_us: Рейтинг IMDb: ', value=f'{rate_imdb}')
    webhook.set_footer(
        text=f'Дата выхода {table[5]}  |  Длительность фильма {table[19]}\nВозрасное ограничение {table[17]}',
        icon_url='https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.pngpix.com%2Fwp-content%2Fuploads%2F2016%2F07%2FPNGPIX-COM-Popcorn-PNG-Image.png&f=1&nofb=1')

    # #Отправка в Discord
    webhook.send()

def settings():
    Settings.show()

    try:
        with open('settings_file.json', 'r') as j:
            json_data = json.load(j)

            ui2.lineEdit_UserName.setText(json_data[0]['UserName'])
            ui2.lineEdit_UserLink.setText(json_data[0]['UserLink'])
            ui2.lineEdit_UserImage.setText(json_data[0]['UserImage'])
            ui2.lineEdit_color.setText(json_data[0]['UserColor'])

            ui2.lineEdit_UserWebhook.setText(json_data[0]['DiscordWebhook'])
    except:
        print('Поля не должны быть пустыми!')

    ui2.pushButton.clicked.connect(lambda: settings_send())

    ui2.pushButton_Cancel.clicked.connect(lambda: Settings.close())

def settings_send():
    user = [
        {
            'UserName': ui2.lineEdit_UserName.text(),
            'UserLink': ui2.lineEdit_UserLink.text(),
            'UserImage': ui2.lineEdit_UserImage.text(),
            'UserColor': ui2.lineEdit_color.text(),
            'DiscordWebhook': ui2.lineEdit_UserWebhook.text()
        }
    ]

    with open('settings_file.json', 'w') as file:
        json.dump(user, file)

    Settings.close()

def parser():
    url = ui.lineEdit_link.text()

    if url == '':
        print('Поле с ссылкой пустое! Заполняю контентом по умолчанию')
        ui.lineEdit_link.setText('http://getkinopoisk.com/films/horror/549-sinister-2012.html')
    else:
        try:
            html = get_html(url)
            if html.status_code == 200:
                push_content(html.text, url)
                print('Сообщение успешно отправлено!')
            else:
                print('Error')
        except:
            print('Ошибка!\nДанный URL заблокирован или введен не верно!')


#code
# print(type(0xAD16F0)) # Открытие века!

ui.pushButton.clicked.connect(lambda: parser())
ui.toolButton.clicked.connect(lambda: settings())

# Main Loop
sys.exit(app.exec_())
