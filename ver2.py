import socket
import csv
from bs4 import BeautifulSoup
import requests
from datetime import date
import os

yes = ['yes', 'y']
no = ['no', 'n']


def material():
    mineral_list = {
        'copper': ['cu', 0.20],
        'manganese': ['mn', 0.15],
        'zinc': ['zn', 0.10]
    }
    mineral = input('Mineral: ').lower()
    dutyPercent = mineral_list[mineral][1]
    grade = input(f'Grade of {mineral}: % ')

    return mineral, dutyPercent, grade


def forex():

    def online():
        src_rate = requests.get(
            'https://www.google.com/search?q=usd+to+zambia+kwacha').text

        rate_soup = BeautifulSoup(src_rate, 'html.parser')

        rate_raw = rate_soup.find('div', class_='BNeawe iBp4i AP7Wnd')
        rate_number = rate_raw.text.split(' ')[0]
        rate = round(float(rate_number), 2)

        return rate

    def offline():
        os.chdir('/Users/hardikpatel/Desktop/test')
        with open('invoice.csv') as invoice:
            for rate_invoice in invoice:
                rate_invoice = rate_invoice.split('\t')
                if rate_invoice:
                    rate = (rate_invoice[3])
        return rate

    try:
        socket.create_connection(("www.google.com", 80))
        rate = float(online())
        # return rate
    except OSError:
        rate = float(offline())
        # return rate
        pass

    ex_currency = input('In Kwacha? (y/n): ')
    if ex_currency in yes:
        ex_kwacha = int(input('Price: K '))
        ex_usd = round((ex_kwacha / rate), 2)
    else:
        ex_usd = int(input('Price: $ '))

    return rate, ex_usd


def hidden():
    transport = 75
    royalty = 1.7
    handling = 32
    misc = 2.5
    hidden_cost = transport + royalty + handling + misc

    return hidden_cost


def printing():

    mineral, dutyPercent, grade = material()
    rate, ex_usd = forex()
    hidden_cost = hidden()

    quantity = int(input('Quantity in MT: '))
    exTotal = round((quantity * ex_usd), 2)
    printExTotal = ('Total Ex = ' + format(exTotal)).center(50, '-')

    duty = ex_usd * dutyPercent
    fob = round((ex_usd + hidden_cost), 2)
    fob_duty = round((fob + duty), 2)

    fobTotal = round((quantity * fob_duty), 2)
    printFobTotal = ('Total FOB = ' + format(fobTotal)).center(50, '-')

    default_date = date.today()
    custom_date = default_date.strftime('%Y-%b-%d')
    today = custom_date.center(50, '_')

    def niceLooks(a, b, c):
        line = ''.ljust(5) + a.ljust(25) + b + format(c)
        return line
    print(today)
    print(niceLooks(mineral, '% ', grade))
    print(niceLooks('Todays Rate', '$ ', rate))
    print(niceLooks('Ex', '$ ', ex_usd))
    print(niceLooks('Quantity', 'T ', quantity))
    print(niceLooks('FOB', '$ ', fob))
    print(niceLooks('FOB & Duty', '$ ', fob_duty))
    print(printExTotal)
    print(printFobTotal)

    def save_db():
        os.chdir('/Users/han/Desktop/test')

        location = input('Ex works location: ').lower()
        note = input('Note: ')
        # h1 = ['Date', 'Mineral', 'Grade','Rate', 'Qnt.','EX', 'ExTotal','FOB','fobTotal', 'place', 'Notes']
        DATA = [custom_date, mineral, grade, rate, quantity,
                ex_usd, exTotal, fob, fobTotal, location, note]
        filename = 'invoice.csv'
        with open(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='\t')
            # csvwriter.writerow(h1)
            csvwriter.writerow(DATA)
    saveCSV = input('Save info: ').lower()
    if saveCSV in yes:
        save_db()


printing()
