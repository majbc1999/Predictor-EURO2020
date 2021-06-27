############################################################################################################################################################

#                                                           * * * PREDICTOR EURO 2021 * * *                                                                #
#                                                                Maj Gaberšček,  Bovec                                                                     #
############################################################################################################################################################


# Tabela kvot
kvote = {
    "1:0": 9,
    "2:0": 13,
    "2:1": 11,
    "3:0": 26,
    "3:1": 23,
    "3:2": 34,

    "0:0": 9,
    "1:1": 6.5,
    "2:2": 15,
    "3:3": 51,

    "0:1": 10,
    "0:2": 17,
    "1:2": 12,
    "0:3": 34,
    "1:3": 29,
    "2:3": 41,
}


# Popularni rezulati, ki ne prinašajo dodatnih dveh točk
popularni_rezultati = [
    "3:2",
    "2:1",
    "1:2",
    ""
]


# Prva in druga ekipa (pazi vrstni red glede na kvote)
ekipe = ["Belgija", "Portugalska"]


# Kvote da katerakoli ekipa zmaga po podaljških
kvote_na_podaljske = [
    10,
    12
]

############################################################################################################################################################

#                                                     * * * TUKAJ NAPREJ JE KODA, NE TIKAJ * * *                                                           #

############################################################################################################################################################


### NAJBOLJŠA NAPOVED ###

def simulacija(verjetnosti, popularni, ekipe):
    #print("--------------------------------------------------------------------")
    #print("Slovar verjetnosti")
    #print(verjetnosti)
    print("--------------------------------------------------------------------")
    najboljsa_napoved = "0:0"
    upanje1 = 0
    upanje_trenutno = 0
    for i in range(6):
        for j in range(6):
            rezultat = str(i) + ":" + str(j)
            upanje_trenutno = upanje(rezultat, verjetnosti, popularni)
            if upanje_trenutno >= upanje1:
                upanje1 = upanje_trenutno
                najboljsa_napoved = rezultat

    print("Najboljša napoved je: " + ekipe[0] + " " + najboljsa_napoved + " " + ekipe[1] + ". Pričakovane točke = " + str(round(upanje1, 2)))
    print("--------------------------------------------------------------------")
    


### SLOVAR VERJETNOSTI REZULTATA ###

def verjetnosti(kvote):
    vsota_kvot = 0
    slovar = {}
    for i in range(6):
        for j in range(6):
            niz = str(i) + ":" + str(j)
            if niz not in kvote.keys():
                continue
            if kvote[niz] != 0:
                vsota_kvot += (1 / kvote[niz])
    for i in range(6):
        for j in range(6):
            niz = str(i) + ":" + str(j)
            if (niz not in kvote.keys()): slovar[niz] = 0
            elif kvote[niz] == 0: slovar[niz] = 0
            else:
                slovar[niz] = 1 / (kvote[niz] * vsota_kvot)
    return slovar



### UPANJE REZULTATA ###
def upanje(rezultat, verjetnosti, popularni):
    upanje1 = 0
    for i in range(6):
        for j in range(6):
            napoved = str(i) + ":" + str(j)
            if verjetnosti[napoved] > 0:
                upanje1 += verjetnosti[napoved] * tocke(rezultat, napoved, popularni)
    return upanje1



### TOČKE ZA NAPOVED ###
def tocke(rezultat, napoved, popularni):
    x = int(rezultat[0])
    y = int(rezultat[2])

    a = int(napoved[0])
    b = int(napoved[2])

    score = 0

    # Pravilna napoved rezultata
    if (x > y and a > b) or (x < y and a < b) or (x == y and a == b):
        score += 3

    # Stevilo golov
    if (x == a): score += 1
    if (y == b): score += 1
    if (x - y == a - b): score += 1

    # Underdog
    if (score == 6 and not (napoved in popularni)): score += 2 

    return score


# Za izločilne boje se v Predictorju šteje 120 min, na bet365 pa so kvote za 90 min zato ročno spremenimo
def popravi_verjetnosti(verjetnosti, kvote_na_podaljske):
    if len(kvote_na_podaljske) == 0:
        return verjetnosti
    else:

        vsote_remijev = verjetnosti["0:0"] + verjetnosti["1:1"] + verjetnosti["2:2"]

        # če vemo, da je bil remi, verjetnost posameznega rezulatata
        dist_remijev = {
            "0:0": verjetnosti["0:0"] / vsote_remijev, 
            "1:1": verjetnosti["1:1"] / vsote_remijev, 
            "2:2": verjetnosti["2:2"] / vsote_remijev
        }

        # kaj se lahko zgodi
        slovar_moznih_razpletov = {
            "0:0": ["0:1", "1:0"],
            "1:1": ["1:2","2:1"],
            "2:2": ["2:3", "3:2"]          
        }

        for rezultat in slovar_moznih_razpletov:
            # Zmaga 1. po podaljških
            kvota1 = kvote_na_podaljske[0]
            kvota1 = 1.10 * kvota1
            ver1 = 1 / kvota1 # verjetnost

            sedanja1 = verjetnosti[slovar_moznih_razpletov[rezultat][0]]
            dodano1 = ver1 * dist_remijev[rezultat]

            verjetnosti[slovar_moznih_razpletov[rezultat][0]] = sedanja1 + dodano1

            # Zmaga 2. po podaljških
            kvota2 = kvote_na_podaljske[1]
            kvota2 = 1.10 * kvota2
            ver2 = 1 / kvota2 # verjetnost

            sedanja2 = verjetnosti[slovar_moznih_razpletov[rezultat][1]]
            dodano2 = ver2 * dist_remijev[rezultat]

            verjetnosti[slovar_moznih_razpletov[rezultat][1]] = sedanja2 + dodano2

            verjetnosti[rezultat] = verjetnosti[rezultat] - dodano1 - dodano2

        return verjetnosti

            





simulacija(popravi_verjetnosti(verjetnosti(kvote), kvote_na_podaljske), popularni_rezultati, ekipe)


### Prazne kvote ###

kvoteprazne = {
    "0:0": 0,
    "0:1": 0,
    "0:2": 0,
    "0:3": 0,

    "1:0": 0,
    "1:1": 0,
    "1:2": 0,
    "1:3": 0,

    "2:0": 0,
    "2:1": 0,
    "2:2": 0,
    "2:3": 0,

    "3:0": 0,
    "3:1": 0,
    "3:2": 0,
    "3:3": 0,
}

