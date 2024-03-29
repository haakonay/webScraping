import requests
from bs4 import BeautifulSoup, Comment
import re  # Regular Expressions
import urllib.request # Trengs for å laste ned pdf
import os # Sjekker om fil allerede eksisterer


url_gov = "https://opengov.360online.com"
url = "https://opengov.360online.com/Meetings/"

# Municipalities that use opengov
kommuner_medGov = ['LILLESTROMKOM', 'Nittedal', 'Gran',
                   'Skien', 'Siljan', 'Bamble', 'Kragero', 'Drangedal',
                   'Lindesnes', 'Farsund', 'Flekkefjord', 'Vennesla',
                   'aseral', 'Haegebostad', 'Kvinesdal', 'Stavanger',
                   'Sandnes', 'Klepp', 'Gjesdal', 'Randaberg', 'Kvitsoy',
                   'Voss', 'Kristiansund', 'Molde', 'Vestnes', 'Rauma',
                   'Aukra', 'Averoy', 'Gjemnes', 'Tingvoll', 'Sunndal',
                   'Surnadal', 'Smola', 'Aure', 'Heim', 'Orkland', 'Rindal',
                   'Hemnes', 'Vardo', 'Gratangen']

for i in kommuner_medGov:
    new_url = url+i+"/Meetings?month=12&year=2021" # Narrows down month and year
    try:
        page = requests.get(new_url)  # Gathering source code
    except Exception:
        print("Feil med lenken")
        continue
    soup_page = BeautifulSoup(page.text, features="html.parser") # bs4
    for j in soup_page.find_all('span', text=re.compile("Kommunestyre|kommunestyre|KOMMUNESTYRE")): # CSS selector
        a = j.parent.parent # Getting grandparent to grab href
        href = str(a.get('href'))
        lenke_til_protkoll = url_gov + href
        page = requests.get(lenke_til_protkoll)
        soup_page = BeautifulSoup(page.text, features="html.parser")
        for k in soup_page.find_all("li", {'title': re.compile(r'Protokoll|protokoll')}): # Looking for words
            for href in k.find_all('a', href=True): # Confirming that the found href contains href
                pdf_link = str(href.get('href'))
                pdf = url_gov+pdf_link
                response = urllib.request.urlopen(pdf)
                name = i+"-Møteprotokoll-Kommunestyret-2021.pdf"
                if not os.path.isfile(name):    # If name do not exist
                    file = open(name,"wb")      # If there are 2 protocols from december, then only the newest will be
                    file.write(response.read())
                    file.close()

# All municipalities, unfiltered
""""                    
kommuner = ['Halden','Moss', 'Sarpsborg', 'Fredrikstad',
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

# Loop for filtering municipalities that use opengov            
kommuner_med_gov = []
url = "https://opengov.360online.com/Meetings/"
for i in kommuner:
    new_url = url+i
    downloaded_page = requests.get(new_url)
    if downloaded_page.status_code == 200:
        kommuner_med_gov.append(i)
print(kommuner_med_gov)
"""
