########## IMPORTS ##########
import requests  # Requests for requesting and downloading URLs
from bs4 import BeautifulSoup, Comment  # For parsing downloaded URLs
import re  # Regular Expressions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selectorlib import Extractor
import time  # For providing the user with time spent and for testing

# Far tak i alle kommuner fra SNL.no (her kommuner.txt fil)
# url_kommuner = "https://snl.no/kommuner_i_Norge"
# f = open("kommuner.txt",'r', encoding="utf8")
# ft = f.read()
# kommuner = re.findall(r'(?:\d+\t)(\w+-?\w+)', ft)

kommuner = ['Halden', 'Moss', 'Sarpsborg', 'Fredrikstad',
            'Drammen', 'Kongsberg', 'Ringerike', 'Hvaler',
            'Aremark', 'Marker', 'Indre', 'Skiptvet', 'Rakkestad',
            'Rade', 'Valer-of', 'Vestby', 'Nordre', 'as', 'Frogn', 'Nesodden',
            'Baerum', 'Asker', 'Aurskog-Holand', 'Raelingen', 'Enebakk', 'Lorenskog',
            'Lillestrom', 'Nittedal', 'Gjerdrum', 'Ullensaker', 'Nes', 'Eidsvoll',
            'Nannestad', 'Hurdal', 'Hole', 'Fla', 'Nesbyen', 'Gol', 'Hemsedal',
            'al', 'Hol', 'Sigdal', 'Krodsherad', 'Modum', 'ovre', 'Lier',
            'Flesberg', 'Rollag', 'Nore', 'Jevnaker', 'Lunner', 'Oslo',
            'Kongsvinger', 'Hamar', 'Lillehammer', 'Gjovik', 'Ringsaker',
            'Loten', 'Stange', 'Nord-Odal', 'Sor-Odal', 'Eidskog', 'Grue',
            'asnes', 'Valer', 'Elverum', 'Trysil', 'amot', 'Stor-Elvdal',
            'Rendalen', 'Engerdal', 'Tolga', 'Tynset', 'Alvdal', 'Folldal',
            'Os', 'Dovre', 'Lesja', 'Skjak', 'Lom', 'Vaga', 'Nord-Fron', 'Sel',
            'Sor-Fron', 'Ringebu', 'oyer', 'Gausdal', 'ostre', 'Vestre', 'Gran', 'Sondre',
            'Nordre', 'Sor-Aurdal', 'Etnedal', 'Nord-Aurdal', 'Vestre', 'oystre', 'Vang', 'Horten',
            'Holmestrand', 'Tonsberg', 'Sandefjord', 'Larvik', 'Porsgrunn', 'Skien', 'Notodden', 'Faerder',
            'Siljan', 'Bamble', 'Kragero', 'Drangedal', 'Nome', 'Midt-Telemark', 'Tinn', 'Hjartdal', 'Seljord',
            'Kviteseid', 'Nissedal', 'Fyresdal', 'Tokke', 'Vinje', 'Risor', 'Grimstad',
            'Arendal', 'Kristiansand', 'Lindesnes', 'Farsund', 'Flekkefjord', 'Gjerstad',
            'Vegarshei', 'Tvedestrand', 'Froland', 'Lillesand', 'Birkenes', 'amli', 'Iveland',
            'Evje', 'Bygland', 'Valle', 'Bykle', 'Vennesla', 'aseral', 'Lyngdal', 'Haegebostad',
            'Kvinesdal', 'Sirdal', 'Eigersund', 'Stavanger', 'Haugesund', 'Sandnes', 'Sokndal',
            'Lund', 'Bjerkreim', 'Ha', 'Klepp', 'Time', 'Gjesdal', 'Sola', 'Randaberg', 'Strand',
            'Hjelmeland', 'Suldal', 'Sauda', 'Kvitsoy', 'Bokn', 'Tysvaer', 'Karmoy', 'Utsira', 'Vindafjord',
            'Bergen', 'Kinn', 'Etne', 'Sveio', 'Bomlo', 'Stord', 'Fitjar', 'Tysnes', 'Kvinnherad',
            'Ullensvang', 'Eidfjord', 'Ulvik', 'Voss', 'Kvam', 'Samnanger', 'Bjornafjorden',
            'Austevoll', 'oygarden', 'Askoy', 'Vaksdal', 'Modalen', 'Osteroy', 'Alver', 'Austrheim',
            'Fedje', 'Masfjorden', 'Gulen', 'Solund', 'Hyllestad', 'Hoyanger', 'Vik', 'Sogndal',
            'Aurland', 'Laerdal', 'ardal', 'Luster', 'Askvoll', 'Fjaler', 'Sunnfjord', 'Bremanger',
            'Stad', 'Gloppen', 'Stryn', 'Kristiansund', 'Molde', 'alesund', 'Vanylven', 'Sande', 'Heroy',
            'Ulstein', 'Hareid', 'orsta', 'Stranda', 'Sykkylven', 'Sula', 'Giske', 'Vestnes', 'Rauma',
            'Aukra', 'Averoy', 'Gjemnes', 'Tingvoll', 'Sunndal', 'Surnadal', 'Smola', 'Aure', 'Volda',
            'Fjord', 'Hustadvika', 'Trondheim', 'Steinkjer', 'Namsos', 'Froya', 'Osen', 'Oppdal',
            'Rennebu', 'Roros', 'Holtalen', 'Midtre', 'Melhus', 'Skaun', 'Malvik', 'Selbu',
            'Tydal', 'Meraker', 'Stjordal', 'Frosta', 'Levanger', 'Verdal', 'Snaase', 'Lierne',
            'Raarvihke', 'Namsskogan', 'Grong', 'Hoylandet', 'Overhalla', 'Flatanger', 'Leka',
            'Inderoy', 'Indre', 'Heim', 'Hitra', 'orland', 'afjord', 'Orkland', 'Naeroysund',
            'Rindal', 'Bodo', 'Narvik', 'Bindal', 'Somna', 'Bronnoy', 'Vega', 'Vevelstad',
            'Heroy', 'Alstahaug', 'Leirfjord', 'Vefsn', 'Grane', 'Hattfjelldal', 'Donna',
            'Nesna', 'Hemnes', 'Rana', 'Luroy', 'Traena', 'Rodoy', 'Meloy', 'Gildeskal',
            'Beiarn', 'Saltdal', 'Fauske', 'Sorfold', 'Steigen', 'Lodingen', 'Evenes',
            'Rost', 'Vaeroy', 'Flakstad', 'Vestvagoy', 'Vagan', 'Hadsel', 'Bo', 'oksnes',
            'Sortland', 'Andoy', 'Moskenes', 'Hamaroy', 'Tromso', 'Harstad', 'Alta', 'Vardo', 'Vadso',
            'Hammerfest', 'Kvaefjord', 'Tjeldsund', 'Ibestad', 'Gratangen', 'Loabak', 'Bardu', 'Salangen',
            'Malselv', 'Sorreisa', 'Dyroy', 'Senja', 'Balsfjord', 'Karlsoy', 'Lyngen', 'Storfjord', 'Gaivuotna',
            'Skjervoy', 'Nordreisa', 'Kvaenangen', 'Guovdageaidnu', 'Loppa', 'Hasvik', 'Masoy', 'Nordkapp',
            'Porsanger', 'Karasjohka', 'Lebesby', 'Gamvik', 'Berlevag',
            'Deatnu', 'Unjarga', 'Batsfjord', 'Sor-Varanger']

kommuner_utenGov = ['Halden', 'Moss', 'Fredrikstad', 'Drammen', 'Kongsberg', 'Ringerike',
                    'Hvaler', 'Aremark', 'Marker', 'Indre', 'Skiptvet', 'Rakkestad', 'Rade',
                    'Valer-of', 'Vestby', 'Nordre', 'as', 'Frogn', 'Nesodden', 'Baerum', 'Asker',
                    'Aurskog-Holand', 'Raelingen', 'Enebakk', 'Lorenskog', 'Gjerdrum', 'Ullensaker',
                    'Nes', 'Eidsvoll', 'Nannestad', 'Hurdal', 'Hole', 'Fla', 'Nesbyen', 'Gol', 'Hemsedal',
                    'al', 'Hol', 'Sigdal', 'Krodsherad', 'Modum', 'ovre', 'Lier', 'Flesberg', 'Rollag', 'Nore',
                    'Jevnaker',
                    'Lunner', 'Oslo', 'Kongsvinger', 'Hamar', 'Lillehammer', 'Gjovik', 'Ringsaker', 'Loten', 'Stange',
                    'Nord-Odal',
                    'Sor-Odal', 'Eidskog', 'Grue', 'asnes', 'Valer', 'Elverum', 'Trysil', 'amot', 'Stor-Elvdal',
                    'Rendalen', 'Engerdal', 'Tolga', 'Tynset', 'Alvdal', 'Folldal', 'Os', 'Dovre', 'Lesja',
                    'Skjak', 'Lom', 'Vaga', 'Nord-Fron', 'Sel', 'Sor-Fron', 'Ringebu', 'oyer', 'Gausdal',
                    'ostre', 'Vestre', 'Sondre', 'Nordre', 'Sor-Aurdal', 'Etnedal', 'Nord-Aurdal', 'Vestre',
                    'oystre', 'Vang', 'Horten', 'Holmestrand', 'Tonsberg', 'Sandefjord', 'Larvik', 'Porsgrunn',
                    'Notodden', 'Faerder', 'Nome', 'Midt-Telemark', 'Tinn', 'Hjartdal', 'Seljord', 'Kviteseid',
                    'Nissedal', 'Fyresdal', 'Tokke', 'Vinje', 'Risor', 'Grimstad', 'Arendal', 'Kristiansand',
                    'Gjerstad', 'Vegarshei', 'Tvedestrand', 'Froland', 'Lillesand', 'Birkenes', 'amli', 'Iveland',
                    'Evje', 'Bygland', 'Valle', 'Bykle', 'Lyngdal', 'Haegebostad', 'Sirdal', 'Eigersund',
                    'Haugesund', 'Sokndal', 'Lund', 'Bjerkreim', 'Ha', 'Time', 'Sola', 'Strand', 'Hjelmeland',
                    'Suldal', 'Sauda', 'Bokn', 'Tysvaer', 'Karmoy', 'Utsira', 'Vindafjord', 'Bergen', 'Kinn',
                    'Etne', 'Sveio', 'Bomlo', 'Stord', 'Fitjar', 'Tysnes', 'Kvinnherad', 'Ullensvang', 'Eidfjord',
                    'Ulvik', 'Kvam', 'Samnanger', 'Bjornafjorden', 'Austevoll', 'oygarden', 'Askoy', 'Vaksdal',
                    'Modalen', 'Osteroy', 'Alver', 'Austrheim', 'Fedje', 'Masfjorden',
                    'Gulen', 'Solund', 'Hyllestad', 'Hoyanger', 'Vik', 'Sogndal', 'Aurland',
                    'Laerdal', 'ardal', 'Luster', 'Askvoll', 'Fjaler', 'Sunnfjord', 'Bremanger',
                    'Stad', 'Gloppen', 'Stryn', 'alesund', 'Vanylven', 'Sande', 'Heroy', 'Ulstein',
                    'Hareid', 'orsta', 'Stranda', 'Sykkylven', 'Sula', 'Giske', 'Volda', 'Fjord', 'Hustadvika',
                    'Trondheim', 'Steinkjer', 'Namsos', 'Froya', 'Osen', 'Oppdal', 'Rennebu', 'Roros',
                    'Holtalen', 'Midtre', 'Melhus', 'Skaun', 'Malvik', 'Selbu', 'Tydal', 'Meraker',
                    'Stjordal', 'Frosta', 'Levanger', 'Verdal', 'Snaase', 'Lierne', 'Raarvihke',
                    'Namsskogan', 'Grong', 'Hoylandet', 'Overhalla', 'Flatanger', 'Leka', 'Inderoy',
                    'Indre', 'Hitra', 'orland', 'afjord', 'Naeroysund', 'Bodo', 'Narvik', 'Bindal',
                    'Somna', 'Bronnoy', 'Vega', 'Vevelstad', 'Heroy', 'Alstahaug', 'Leirfjord',
                    'Vefsn', 'Grane', 'Hattfjelldal', 'Donna', 'Nesna', 'Rana', 'Luroy', 'Traena',
                    'Rodoy', 'Meloy', 'Gildeskal', 'Beiarn', 'Saltdal', 'Fauske', 'Sorfold', 'Steigen',
                    'Lodingen', 'Evenes', 'Rost', 'Vaeroy', 'Flakstad', 'Vestvagoy', 'Vagan', 'Hadsel',
                    'Bo', 'oksnes', 'Sortland', 'Andoy', 'Moskenes', 'Hamaroy', 'Tromso', 'Harstad',
                    'Alta', 'Vadso', 'Hammerfest', 'Kvaefjord', 'Tjeldsund', 'Ibestad', 'Loabak',
                    'Bardu', 'Salangen', 'Malselv', 'Sorreisa', 'Dyroy', 'Senja', 'Balsfjord',
                    'Karlsoy', 'Lyngen', 'Storfjord', 'Gaivuotna', 'Skjervoy', 'Nordreisa',
                    'Kvaenangen', 'Guovdageaidnu', 'Loppa', 'Hasvik', 'Masoy', 'Nordkapp',
                    'Porsanger', 'Karasjohka', 'Lebesby', 'Gamvik', 'Berlevag', 'Deatnu',
                    'Unjarga', 'Batsfjord', 'Sor-Varanger']

url = "https://opengov.360online.com/Meetings/"
hardkodet = ['gjovik']
driver = webdriver.Chrome(ChromeDriverManager().install())
count = 0
ant_kommuner = 0

def fjorårets_møteplan(i,url):
    if not url.startswith("https"):
        url = "https://www."+i+".kommune.no"+url
        print(url)
    try:
        driver.get(url)
    except Exception:
        return 0

    driver.maximize_window()
    time.sleep(2)
    try:
        button = driver.find_element(By.LINK_TEXT, "Vis forrige år")
    except Exception:
        return 0
    button.click()
    return 1

# Går gjennom en og en kommune
for i in kommuner_utenGov:
    new_url = "https://www." + i + ".kommune.no" # Noen få kommuner følger ikke dette standard oppsettet
    try:
        downloaded_url = requests.get(new_url)
    except Exception: # Hvis nettsiden ikke er nedlastbar - neste kommune
        continue
    page = requests.get(new_url)
    soup_page = BeautifulSoup(page.text, features="html.parser")
    pretty_soup = soup_page.prettify()
    for moteplan_url in soup_page.find_all('span', text= re.compile("møte")):
        ant_kommuner += 1
        break
        href = str(moteplan_url.get('href'))
        if href=="None":
                href = str(moteplan_url.find_parent('a').get('href'))
                if href =="None":
                    print("Enda en ny løsning") # Hvis man heller ikke fant lenke til møteplan her
                else: # Når man har kommet til møteplan på nyåret (gitt at forige år er fjoråret)
                    print(href)
                    if fjorårets_møteplan(i, href):
                        print(driver)
                        count +=1
                        break


print(count)
print(ant_kommuner)

            # Gå videre fra her og begynne på funksjoner som tar for seg andre caser


