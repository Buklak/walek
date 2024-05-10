import unicodedata
import string
import random
import csv

def usun_polskie_znaki(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.replace('ł', 'l')
    
def get_domains():
    domeny = {}
    with open('domeny.csv', encoding='utf-8') as csvfile:
        domenyreader = csv.reader(csvfile, delimiter =';')
        next(domenyreader)
        for domena in domenyreader:
            key = domena[0]
            domain = domena[1]
            domeny[key] = domain
    return domeny

def usun_przed_myslnikiem(nazwisko):
    # Sprawdź czy jest znak "-"
    if "-" in nazwisko:
        # Podziel nazwisko na części przed i po myślniku
        czesci = nazwisko.split("-")
        # Zbuduj nowe nazwisko z pierwszej części oraz reszty nazwiska po myślniku
        nowe_nazwisko = nazwisko[0] + czesci[-1]
        return nowe_nazwisko
    else:
        # Jeżeli nie ma myślnika, zwróć oryginalne nazwisko
        return nazwisko
    
def generuj_email(imie, nazwisko, skrot_spolki):
    domeny = get_domains()
    if skrot_spolki in domeny:
        domena = domeny[skrot_spolki]
        imie = usun_polskie_znaki(imie.lower())
        nazwisko = usun_polskie_znaki(nazwisko.lower())
        return f"{imie}.{nazwisko}@{domena}"
    else:
        return "Nieznany skrót spółki"

def generuj_imie(imie, nazwisko):
    imie = usun_polskie_znaki(imie.lower())
    nazwisko = usun_polskie_znaki(nazwisko.lower())
    return f"{imie}.{nazwisko}"
    
def generuj_haslo(dlugosc=12):
    znaki_specjalne = "!@#$%*()"
    litery = string.ascii_letters
    cyfry = string.digits

    dozwolone_litery = litery.replace("I", "").replace("l", "")
    dozwolone_cyfry = cyfry.replace("1", "").replace("0","")

    pierwsza_czesc = random.choice(dozwolone_litery) + random.choice(dozwolone_cyfry) + random.choice(znaki_specjalne)

    reszta = ''.join(random.choice(dozwolone_litery + dozwolone_cyfry + znaki_specjalne) for _ in range(dlugosc - 3))

    haslo = pierwsza_czesc + reszta
    haslo = ''.join(random.sample(haslo, len(haslo)))

    return haslo
def generuj_domene(imie, nazwisko):
    imie = usun_polskie_znaki(imie.lower())
    nazwisko = usun_polskie_znaki(nazwisko.lower())
    nazwisko = usun_przed_myslnikiem(nazwisko)
    return f"{imie[0]}{nazwisko}"
    
with open('imie.txt', 'r', encoding='utf-8') as file:
    with open('dane do spark.txt', 'w', encoding='utf-8') as output_file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            try:
                imie_nazwisko = lines[i].strip().split()
                if len(imie_nazwisko) >= 2:
                    imie = imie_nazwisko[0]
                    nazwisko = ''.join(imie_nazwisko[1:])
                    spolka = lines[i+1].strip()
                    spark = "Dane do sparka: " + generuj_imie(imie, nazwisko) + "; " + imie + " " + nazwisko + "; " + generuj_email(imie, nazwisko, spolka) + "; " + generuj_haslo()
                    AD = "Dane do AD: " + imie + "; " + nazwisko + "; " + generuj_domene(imie, nazwisko)+ "; " + generuj_haslo() + "\n"
                    output_file.write(spark + '\n' + AD + "\n")
                else:
                    raise ValueError("Błędny wałek danych: " + lines[i])
            except ValueError as e:
                print(e)

print("Adresy e-mail zostały zapisane do pliku 'maile.txt'")