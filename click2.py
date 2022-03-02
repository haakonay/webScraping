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
import urllib.request
import os



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
hardkodet = ['gjovik','moss']

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": r'C:\Users\haako\PycharmProjects\kbn\pdfer', #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver = webdriver.Chrome(options=options)
count = 0
ant_kommuner = 0

def tiny_file_rename(newname, folder_of_download):
    filename = max([f for f in os.listdir(folder_of_download)], key=lambda xa :   os.path.getctime(os.path.join(folder_of_download,xa)))
    if '.part' in filename:
        time.sleep(1)
        os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))
    else:
        os.rename(os.path.join(folder_of_download, filename),os.path.join(folder_of_download,newname))

def download_pdf(pdf):
        try:
            page = requests.get(pdf)
        except Exception:
            return 1
        # Downloading PDF

        response = urllib.request.urlopen(pdf)

        file = open(i + "-Møteprotokoll-Kommunestyret-2021" + ".pdf", "wb")
        file.write(response.read())
        file.close()

def finn_protokoll():
    try:
        button = driver.find_element(By.LINK_TEXT, "Kommunestyret")
    except Exception:
        return 0
    driver.execute_script("arguments[0].click();", button)
    page = requests.get(driver.current_url)
    soup = BeautifulSoup(page.text, features="html.parser")
    pdf = soup.find("a", {'title': re.compile(r'Protokoll - Kommunestyret - \d+.12.2021')})
    if pdf:
        title = str(pdf.get('title'))
        button = driver.find_element(By.XPATH, "//a[@title='" + title + "']")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
        tiny_file_rename(i +".pdf", r'C:\Users\haako\PycharmProjects\kbn\pdfer')
        return 1
    else:
        return 2

def fjorårets_møteplan(i,url):
    if not url.startswith("http"):
        url = "https://www."+i+".kommune.no"+url
    try:
        driver.get(url)
    except Exception:
        return 0

    driver.maximize_window()
    try:
        button = driver.find_element(By.LINK_TEXT, "Vis forrige år")
        driver.execute_script("arguments[0].click();", button)
        return 1
    except Exception:
        pass
    try:
        button = driver.find_element(By.LINK_TEXT, "Vis Forrige År")
        driver.execute_script("arguments[0].click();", button)
        return 1
    except Exception:
        return 0



# Går gjennom en og en kommune
start = time.time()
for i in kommuner_utenGov:
    godkjent = False
    new_url = "https://www." + i + ".kommune.no" # Noen få kommuner følger ikke dette standard oppsettet
    try:
        page = requests.get(new_url)
    except Exception: # Hvis nettsiden ikke er nedlastbar - neste kommune
        continue
    soup_page = BeautifulSoup(page.text, features="html.parser")
    for moteplan_url in soup_page.find_all('a', href=re.compile("Møteplan|Moteplan|moteplan|møteplan"
                                                                 "|Møtekalender|Motekalender|møtekalender|motekalender")):
        print(moteplan_url)
        href = str(moteplan_url.get('href'))
        if not href.startswith("http"):
            href = "https://www." + i + ".kommune.no" + href
        try:
            page = requests.get(href)
        except Exception:  # Hvis nettsiden ikke er nedlastbar - neste kommune
            continue
        soup_politikk = BeautifulSoup(page.text, features="html.parser")
        count_mote_2 = 0
        for moter in soup_politikk('a', href= re.compile("mote")):
            count_mote_2 += 1
            moter = str(moter.get('href'))
            if fjorårets_møteplan(i, moter):
                count += 1
                status = finn_protokoll()
                if status == 1:
                    godkjent = True
                    # Laster ned pdf funksjon
                    break
                elif status == 2:
                    continue
            elif count_mote_2 == 10:
                break
        if godkjent:
            break

stop = time.time()

print(stop-start)
print(count)


"""
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
            
# Far tak i alle kommuner fra SNL.no (her kommuner.txt fil)
# url_kommuner = "https://snl.no/kommuner_i_Norge"
# f = open("kommuner.txt",'r', encoding="utf8")
# ft = f.read()
# kommuner = re.findall(r'(?:\d+\t)(\w+-?\w+)', ft)

"""

