# coding: utf-8
"""
Пытаемся получить данные по всем популярным остановкам
"""
from urllib2 import urlopen
import xml.etree.ElementTree as etree
from flask import Flask, render_template
from markdown import Markdown

app = Flask(__name__)

STATIONS = {
    u'шварца-работа': {
        'url': 'http://m.ettu.ru/station/962909',
        'numbers': [6, 20]
    },
    u'дом-шварца': {
        'url': 'http://m.ettu.ru/station/962512',
        'numbers': [9]
    },
    u'гостиница уктус': {
        'url': 'http://m.ettu.ru/station/962907',
        'numbers': [6],
    },
    u'шварца-дом': {
        'url': 'http://m.ettu.ru/station/961948',
        'numbers': [9],
    },
}

MARKDOWN = Markdown()


@app.route('/')
def main():
    return render_template('index.html', content=main_content())


def main_content():
    """ главная страница """
    output = {}
    for station, data in STATIONS.items():
        tree = etree.parse(urlopen(data['url']))
        output[station] = {
            'header': "## %s" % (station,),
            'buslist': [],
        }
        root = tree.getroot()
        for bus in root.findall('body/div/p/div'):
            bus_num = bus[0].find('b').text
            if int(bus_num) not in data['numbers']:
                continue
            bus_time = bus[1].text
            bus_distance = bus[2].text
            bus_string = "%s / %s / %s\n" % (bus_num, bus_time, bus_distance)
            output[station]['buslist'].append(bus_string)

        output[station]['header'] = MARKDOWN.convert(output[station]['header'])
        output[station]['buslist'] = MARKDOWN.convert(u'\n'.join(output[station]['buslist']))
    return output

if __name__ == '__main__':
    app.run()
