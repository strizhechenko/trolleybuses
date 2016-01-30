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
    u'шварца-работа': 'http://m.ettu.ru/station/962909',
    u'дом-шварца': 'http://m.ettu.ru/station/962512',
    u'гостиница уктус': 'http://m.ettu.ru/station/962907',
    u'шварца-дом': 'http://m.ettu.ru/station/961948',
}

MARKDOWN = Markdown()

@app.route('/')
def main():
    return render_template('index.html', content=main_content())

def main_content():
    """ главная страница """
    output = []
    for station, url in STATIONS.items():
        tree = etree.parse(urlopen(url))
        output.append("# %s" % (station,))
        root = tree.getroot()
        for bus in root.findall('body/div/p/div'):
            bus_num = bus[0].find('b').text
            bus_time = bus[1].text
            bus_distance = bus[2].text
            output.append("- %s / %s / %s" % (bus_num, bus_time, bus_distance))
    return MARKDOWN.convert(u"\n".join(output))

if __name__ == '__main__':
    app.run()
