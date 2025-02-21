import pandas
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime

url = "https://de.investing.com/central-banks/fed-rate-monitor"

page = requests.get(url)
soup = bs(page.text, "html.parser")

array = []
for card in soup.select(".cardWrapper"):
    date = card.select_one(".fedRateDate").text.strip()
    table = card.find("tbody")
    update_time = card.select_one(".fedUpdate").text.strip()
    for zeile in table.findAll("tr"):
        zeile_array = []
        for zelle in zeile.findAll("td"):
            inhalt = zelle.text.strip()
            if inhalt == "—": inhalt = "0"
            zeile_array.append(inhalt)
        zeile_array.append(date)
        zeile_array.append(update_time)
        array.append(zeile_array)

df = pandas.DataFrame(columns=["Zielrate", "Aktuell", "Vorheriger Tag", "Voherige Woche", "Sitzungstermin","UpdatedTime"], data=array)
df.to_csv(" /Master/F/User/Microsoft Excel/Privat/Börse/Investing/Fed-Monitor/fed_" +  datetime.datetime.today().strftime("%d.%m.%Y") + ".csv", sep=";", index = False, encoding="utf-8")