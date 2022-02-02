########## IMPORTS ##########
import requests                          # Requests for requesting and downloading URLs
from bs4 import BeautifulSoup, Comment   # For parsing downloaded URLs
import re                                # Regular Expressions
import urllib.request
from collections import Counter          # For returning most common words in dictionary
import validators                        # Validating URLs provided by user
from validators import ValidationFailure # -
import time                              # For providing the user with time spent and for testing


# Far tak i alle kommuner fra SNL.no (her kommuner.txt fil)
# url_kommuner = "https://snl.no/kommuner_i_Norge"
#f = open("kommuner.txt",'r', encoding="utf8")
#ft = f.read()
#kommuner = re.findall(r'(?:\d+\t)(\w+-?\w+)', ft)

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

kommuner_utenGov = ['Halden', 'Moss', 'Fredrikstad', 'Drammen', 'Kongsberg', 'Ringerike',
                    'Hvaler', 'Aremark', 'Marker', 'Indre', 'Skiptvet', 'Rakkestad', 'Rade',
                    'Valer-of', 'Vestby', 'Nordre', 'as', 'Frogn', 'Nesodden', 'Baerum', 'Asker',
                    'Aurskog-Holand', 'Raelingen', 'Enebakk', 'Lorenskog', 'Gjerdrum', 'Ullensaker',
                    'Nes', 'Eidsvoll', 'Nannestad', 'Hurdal', 'Hole', 'Fla', 'Nesbyen', 'Gol', 'Hemsedal',
                    'al', 'Hol', 'Sigdal', 'Krodsherad', 'Modum', 'ovre', 'Lier', 'Flesberg', 'Rollag', 'Nore', 'Jevnaker',
                    'Lunner', 'Oslo', 'Kongsvinger', 'Hamar', 'Lillehammer', 'Gjovik', 'Ringsaker', 'Loten', 'Stange', 'Nord-Odal',
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
url_innsyn = ".kommune.no/innsyn.aspx?response=moteplan&MId1=435&scripturi=/innsyn.aspx&skin=infolink&fradato=2021-01-01T00:00:00"

count_innsyn = 0
count = 0
fant_moteplan = 0
fant_kommunestyret = 0

# INNSYN
for i in kommuner_utenGov:
    new_url = "https://www." + i + url_innsyn
    try:
        downloaded_url = requests.get(new_url)
    except Exception:
        continue
    for j in range(4, 9,4): # De fleste møteplaner er å finne i de tidlig indekserte sidene
        url = "https://www."+i+".kommune.no/innsyn.aspx?response=moteplan&MId1=" \
              + str(j) + "&scripturi=/innsyn.aspx&skin=infolink&fradato=2021-01-01T00:00:00"
        page = requests.get(url)
        soup_page = BeautifulSoup(page.text, features="html.parser")
        pretty_soup = soup_page.prettify()
        if re.search(r'Siden finnes ikke', pretty_soup): # Hvis siden ikke finnes sjekk neste indeks
            print("Siden finnes ikke")
            continue
        if re.search(r'Møteplan', pretty_soup): # Hvis møteplan ble funnet
            print("Fant møteplan")
            fant_moteplan +=1
            if soup_page.find("a", href=True, text="Kommunestyret"):
                a_1 = soup_page.find("a", href=True, text="Kommunestyret")
                href = str(a_1.get('href'))
                final_url = "https://www."+i+".kommune.no" + href +"PF=PI"
                fant_kommunestyret +=1
                print(final_url)
                try:
                    final_page = requests.get(final_url) # Dersom urlen til møteplan er OK: Last ned
                except Exception:
                    continue
                final_soup_page = BeautifulSoup(final_page.text, features="html.parser")
                pdf = final_soup_page.find("a", {'title': re.compile(r'Protokoll - Kommunestyret - \d+.12.2021')})
                if pdf:
                    pdf = str(pdf.get('href'))
                    # Downloading PDF
                    response = urllib.request.urlopen(pdf)
                    file = open(i+"-Møteprotokoll-Kommunestyret-2021"+ ".pdf", "wb")
                    file.write(response.read())
                    file.close()
                    print(i)
                    count +=1
                    break

print(fant_moteplan)
print(fant_kommunestyret)


# 360 GOV
""""
for i in kommuner:
    new_url = url+i
    downloaded_page = requests.get(new_url)
    if downloaded_page.status_code == 200:
        kommuner_utenGov.remove(i)
print(kommuner_utenGov)
"""








