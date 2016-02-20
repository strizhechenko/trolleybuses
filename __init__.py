# coding: utf8

import json
import thread
import time
import xml.etree.ElementTree as etree
from urllib2 import urlopen
from markdown import Markdown
from flask import Flask, render_template

MARKDOWN = Markdown()
APP = Flask(__name__)

STATIONS = {
    u'шварца-работа': {
        'url': 'http://m.ettu.ru/station/962909',
        'numbers': [6, 20],
    },
    u'дом-шварца': {
        'url': 'http://m.ettu.ru/station/962512',
        'numbers': [9],
    },
    u'гостиница уктус': {
        'url': 'http://m.ettu.ru/station/962907',
        'numbers': [6],
    },
    u'шварца-дом': {
        'url': 'http://m.ettu.ru/station/961948',
        'numbers': [9],
    },
    u'от лична': {
        'url': 'http://m.ettu.ru/station/961924',
        'numbers': [9, 15],
    }
}


def fetch_station(station):
    data = STATIONS.get(station)
    tree = etree.parse(urlopen(data['url']))
    output_s = {}
    output_s = {
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
        output_s['buslist'].append(bus_string)

    output_s['header'] = MARKDOWN.convert(output_s['header'])
    output_s['buslist'] = MARKDOWN.convert(u'\n'.join(output_s['buslist']))
    STATIONS[station]['output'] = output_s


@APP.route('/')
def main():
    for station_name, station_data in STATIONS.items():
        if 'output' in station_data:
            del station_data['output']
        thread.start_new_thread(fetch_station, (station_name,))

    timeout = 2
    cur_timeout = 0

    while not all(['output' in t.keys() for t in STATIONS.values()]):
        time.sleep(0.1)
        cur_timeout += 0.1
        if cur_timeout > timeout:
            break

    return render_template('index.html', stations=STATIONS)

if __name__ == '__main__':
    # APP.debug = True
    APP.run()
