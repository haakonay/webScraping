# Imports
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
import time  # For providing the user with time spent and for testing
import os


# Webdriver for chrome (Must have chrome downloaded on the desktop)
# REMEMBER TO CHANGE DEFAULT DIRECTORY
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": r'C:\Users\haako\PycharmProjects\kbn\webScraping\pdf',
    # Change default directory for downloads
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
})

# Path to downlaoded chromedriver
driver = webdriver.Chrome(executable_path=r'C:\Users\haako\PycharmProjects\kbn\webScraping\chromedriver.exe',
                          options=options)
driver.maximize_window()

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
test_kommune = ['ringerike']

# Changing name of newly downloaded .pdf file
def tiny_file_rename(newname, folder_of_download, time_to_wait=60):
    time_counter = 0
    filename = max([f for f in os.listdir(folder_of_download)],
                   key=lambda xa: os.path.getctime(os.path.join(folder_of_download, xa)))
    while '.part' in filename:
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise Exception('Waited too long for file to download')
    filename = max([f for f in os.listdir(folder_of_download)],
                   key=lambda xa: os.path.getctime(os.path.join(folder_of_download, xa)))
    os.rename(os.path.join(folder_of_download, filename), os.path.join(folder_of_download, newname))


# Finding buttons with corresponding text and clicking them
def klikk(text1, text2):
    try:
        button = driver.find_element(By.LINK_TEXT, text1)
        driver.execute_script("arguments[0].click();", button)
        return 1
    except Exception:
        pass
    try:
        button = driver.find_element(By.LINK_TEXT, text2)
        driver.execute_script("arguments[0].click();", button)
        return 2
    except Exception:
        return 0

# Finding, clicking, and downloading pdf
def klikk_pdf(text):
    try:
        button = driver.find_element(By.XPATH, "//a[@title='" + text + "']")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
        tiny_file_rename(i + "-Møteprotokoll-Kommunestyret-2021" + ".pdf",
                         r'C:\Users\haako\PycharmProjects\kbn\webScraping\pdf')
    except Exception:
        return 0


def finn_motekalender(page):
    soup_page = BeautifulSoup(page.text, features="html.parser")
    motekalender = soup_page.find('a', href=re.compile("Møteplan|Moteplan|moteplan|møteplan"
                                                       "|Møtekalender|Motekalender|møtekalender|motekalender"))
    if not motekalender:
        mote = soup_page.find('a', href=re.compile("Møte|Mote|mote|møte"))
        if mote:
            href = str(mote.get('href'))
            if not href.startswith("http"):
                href = new_url + href
            try:
                page = requests.get(href)
                soup_mote = BeautifulSoup(page.text, features="html.parser")
                motekalender = soup_mote.find('a', href=re.compile("Møteplan|Moteplan|moteplan|møteplan"
                                                                   "|Møtekalender|Motekalender|møtekalender|motekalender"))
            except Exception:
                pass
    if not motekalender:
        motekalender = soup_page.find('a', text=re.compile("Møteplan|Moteplan|moteplan|møteplan"
                                                           "|Møtekalender|Motekalender|møtekalender|motekalender"))
        if motekalender:
            href = str(motekalender.get('href'))
            if not href.startswith("http"):
                href = new_url + href
            try:
                page = requests.get(href)
                soup_mote = BeautifulSoup(page.text, features="html.parser")
                motekalender = soup_mote.find('a', href=re.compile("Møteplan|Moteplan|moteplan|møteplan"
                                                                   "|Møtekalender|Motekalender|møtekalender|motekalender"))
            except Exception:
                pass
    return motekalender


# def finn_motekalender_recursive():  Bruke rekursjon for å loope litt til

for i in kommuner_utenGov:
    new_url = "https://www." + i + ".kommune.no"
    try:
        page = requests.get(new_url)
    except Exception:
        continue
    motekalender = finn_motekalender(page)
    if motekalender:
        href = str(motekalender.get('href'))
        if not href.startswith("http"):
            href = new_url + href
        try:
            page = requests.get(href)
        except Exception:
            continue
        soup_page = BeautifulSoup(page.text, features="html.parser")
        forige_år = soup_page.find('a', text=re.compile("Vis Forrige År|Vis forrige år"))
        if forige_år:
            try:
                driver.get(href)
                klikk("Vis forrige år", "Vis Forrige År")
                klikk("Kommunestyret", "KOMMUNESTYRET")
                page = driver.current_url
            except Exception:
                continue
            page = requests.get(page)
            soup_page = BeautifulSoup(page.text, features="html.parser")
            pdf = soup_page.find("a", {'title': re.compile(r'(Protokoll|protokoll|PROTOKOLL).*\d+.12.2021')})
            try:
                title = str(pdf.get('title'))
                klikk_pdf(title)
            except Exception:
                continue
        else:
            print("fant ikke forrige år", i)
    else:
        print("fant ikke møtekalender", i)
        continue


"""
        for moteplan in soup_page.find_all('a', href=re.compile("Møteplan|Moteplan|moteplan|møteplan"
                                                                 "|Møtekalender|Motekalender|møtekalender|motekalender")):
        print(i)
        moteplan_link = str(moteplan.get('href'))
        print(moteplan_link)

"""
