# Dit programma leest de ruwe stemdata uit het raw.txt bestand.
# Copiëer de stemmen uit het stem kanaal en dit programma maakt er een grafiek van.

#importeer nodige python libraries
from matplotlib import pyplot as plt
import numpy as np
import random
import datetime


#rr geeft random getal tussen 0 en 1 op 1 decimaal nauwkeurig
def rr():
    return round(random.random(), 1)


#genereert een random kleur set van 3 getallen tussen 0 en 1
def rancol():
    return (rr(), rr(), rr())


#Genereert een nieuwe kleur die licht genoeg is.
def generatecolor():
    color = rancol()
    while (sum(color) < 1.8) or (color in colors):
        color = rancol()
    colors.append(color)
    return color


#filter de datum uit te tekst
def filterdate(line):
    global datefound, day, m
    #filter de datum uit de berichten
    if ("/" + year in line):
        split = line.split("/")
        day = split[1]
        tijdel = split[0][-2:]
        m = int(tijdel)
        datefound = True
    if ('Yesterday' in line):
        day = str(int(day) - 1)
        if (int(day) == 0):
            day = '31'
            m = str(int(m) - 1)
        datefound = True


#filtert de data. Vind datum en vult: stemmers, op, koning, raadsleden, grafstemmers
def filter(raw):
    global grafstemmers, raadsleden, koning, stemmers, op, datefound
    datefound = False
    for line in raw:
        #filter de datum uit de tekst
        if not datefound: filterdate(line)

        #filter grafstemmers
        if (graftekst in line):
            grafstemmers.append(len(stemmers))
            line = line.replace(graftekst, 'stemt op')
        #filter raadsleden
        if (raadstekst in line):
            raadsleden.append(len(stemmers))
            line = line.replace(raadstekst, 'stemt op')
        #filter koning
        if (koningstekst in line):
            koning.append(len(stemmers))
            line = line.replace(koningstekst, 'stemt op')

        #filter de stemmen en stemmers uit de berichten
        if ("stemt" in line):
            split = line.split(" stemt op ")  #splits stemmer van stem op
            stemmer = split[0].split(":")[0]
            stemmers.append(stemmer)
            tijdel = split[1]
            #splits ongewilde tekens af
            for teken in removechars:
                tijdel = tijdel.split(teken)[0]
            op.append(tijdel)


#hernoem een naam met de aliaslijst
def hernoemnaam(naam):
    for persoon in aliassen:
        if naam in persoon:
            naam = persoon[0]
            break
    return naam


#hernoem een lijst van namen met de aliastlijst
def hernoem(lijst):
    for i in range(len(lijst)):
        lijst[i] = hernoemnaam(lijst[i])
    return lijst


#vereenvoudig een naam
def simplify(naam):
    return naam.lower().capitalize()


#vereenvoudig een lijst van namen
def simplifylist(lijst):
    for i in range(len(lijst)):
        lijst[i] = simplify(lijst[i])
    return lijst


#vereenvoudig en hernoem een lijst van lijsten.
def simplifyenhernoem(groep):
    for lijst in groep:
        simplifylist(lijst)
        hernoem(lijst)


#Het maken van de grafiek
def blokkenbouwen(lijst):
    normaal = lijst == stemmers  #noem conditie lijst bevat normale stemmen normaal
    for i in range(len(lijst)):
        for j in range(len(slachtoffers)):
            if (normaal and op[i] == slachtoffers[j]) or (
                    not normaal and lijst[i] == slachtoffers[j]):
                global stemaantal
                global colr
                stemaantal = stemaantal + 1
                #Pas hoogte van blokje aan
                verhoging = np.zeros(len(slachtoffers))
                verhoging[j] = 1
                textcol = 'black'
                style = 'normal'

                if normaal:
                    if i in raadsleden: verhoging[j] = 2 #toneelspeler kracht
                    if i in koning:
                        verhoging[j] = 4 #BM
                        #style = 'bold'
                    if i in grafstemmers: textcol = 'red'
                    if i > 0:  #behoud blok kleur bij meerdere van dezelfde stem achter elkaar
                        if not (lijst[i] == lijst[i - 1]
                                and op[i] == op[i - 1]):
                            colr = generatecolor()

                #Formatting bij speciale gevallen
                if not normaal:
                    colr = 'red'
                    style = 'bold'
                    textcol = 'white'

                if lijst == zelfstem2:
                    verhoging[j] = 3

                if lijst[i] == 'Raaf':
                    colr = 'black'
                    textcol = 'white'
                    style = 'bold'

                if lijst[i] =='Zwarte stem':
                  colr = 'black'
                  textcol = 'white'
                  style = 'bold'

                plt.bar(xas,
                        verhoging,
                        width=bar_width,
                        bottom=totaal,
                        color=colr)
                totaal[j] += verhoging[j]
                plt.text(xas[j],
                         totaal[j] - verhoging[j] / 2,
                         str(stemaantal) + ". " + lijst[i],
                         ha="center",
                         va="center",
                         color=textcol,
                         fontweight=style)


def maakgrafiek():
    global xas
    global titel
    xas = np.arange(len(slachtoffers))
    imgw = len(slachtoffers) * 2.5
    plt.figure(figsize=(imgw, imgh))

    blokkenbouwen(stemmers)
    blokkenbouwen(zelfstem)
    blokkenbouwen(zelfstem2)

    #formatting van de datum
    month = maanden[int(m) - 1]
    datum = day + " " + month


    #labelen van de grafiek
    plt.xticks(xas, slachtoffers)
    if titel == '':
        titel = 'De stemmen van ' + datum
    plt.title(titel, fontweight='bold')

    plt.ylabel("Aantal stemmen", fontweight='bold')
    plt.xlabel("Gestemd op", fontweight='bold')

    #slaat de grafiek op
    plt.savefig('figures/' + month + " " + day, bbox_inches='tight')
    plt.show()


def doehet(zelfstemmers, permanentestemmen, aliaslijst, stopkarakters,
           staafbreedte, ravenveer, titeloverrule, hoog, zwartestem):
    global zelfstem, zelfstem2, aliassen, removechars, bar_width, veer, titel, imgw, imgh
    zelfstem = zelfstemmers
    zelfstem2 = permanentestemmen
    aliassen = aliaslijst
    removechars = stopkarakters
    bar_width = staafbreedte
    veer = ravenveer
    titel = titeloverrule
    imgw = 15
    imgh = hoog
    zwart = zwartestem

    #Initializeren
    global raw
    raw = open("stemmen.txt", "r")  #Open stemmen bestand

    global d, day, m, year, month, maanden
    d = datetime.datetime.now(
    )  #initieer met de dag van vandaag. Vervang later door dag in berichten
    day = d.strftime("%d")
    m = d.strftime("%m")
    year = d.strftime("%Y")
    maanden = [
        "Januari", "Februari", "Maart", "April", "Mei", "Juni", "Juli",
        "Augustus", "September", "Oktober", "November", "December"
    ]

    global stemmers, op, slachtoffers, totaal, stemaantal
    stemmers = []  #De persoon die stemt
    op = []  #Stemt op
    slachtoffers = []  #De mensen waarop gestemd is
    totaal = []  #Hoe veel stemmen iederen op het einde heeft
    stemaantal = 0  #Hoeveel stemmen er zijn

    global colors, colr
    colors = []  #kleuren die gegenereerd worden
    colr = generatecolor()

    global grafstemmers, raadsleden, koning
    grafstemmers = []  #lijst van mensen die vanuit het graf stemmen
    raadsleden = []  #lijst van raadsleden
    koning = []  #lijst van burgemeester(s)

    global graftekst, raadstekst, koningstekst
    graftekst = 'stemt vanuit het graf op'
    raadstekst = 'stemt x2 op'
    koningstekst = 'stemt x4 op'

    #voeg de stem van de raaf toe.
    if veer != '':
        for v in veer:
            stemmers.insert(0, 'Raaf')
            op.insert(0, v)

    if zwart != '':
      for z in zwart:
        stemmers.insert(0, 'Zwarte stem')
        op.insert(0, z)

    filter(raw)  #filter de stemmen en stemmers uit de tekst

    #Maak alle namen kleine letters en starten met een hoofdletter
    for i in range(len(aliassen)):
        aliassen[i] = simplifylist(aliassen[i])
    simplifyenhernoem([stemmers, op, zelfstem, zelfstem2])

    #slachtoffers bepalen
    for s in op + zelfstem + zelfstem2:
        if s not in slachtoffers:
            slachtoffers.append(s)
            totaal.append(0)

    maakgrafiek()

    #sluit het stemmen bestand
    raw.close()
