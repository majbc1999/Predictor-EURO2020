############################################################################################################################################################

#                                                           * * * PREDICTOR EURO 2021 * * *                                                                #
#                                                                Maj Gaberšček,  Bovec                                                                     #
############################################################################################################################################################


# Tabela kvot
kvote = {
    "0:0": 9,
    "0:1": 9.5,
    "0:2": 15,
    "0:3": 29,

    "1:0": 9.5,
    "1:1": 6.5,
    "1:2": 12,
    "1:3": 26,

    "2:0": 15,
    "2:1": 12,
    "2:2": 15,
    "2:3": 34,

    "3:0": 29,
    "3:1": 26,
    "3:2": 34,
    "3:3": 51,
}


# Popularni rezulati, ki ne prinašajo dodatnih dveh točk
popularni_rezultati = [
    "2:1",
    "2:2",
    "1:1",
    ""
]


# Prva in druga ekipa (pazi vrstni red glede na kvote)
ekipe = ["Francija", "Nemčija"]



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
    for i in range(4):
        for j in range(4):
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
    for i in range(4):
        for j in range(4):
            niz = str(i) + ":" + str(j)
            if kvote[niz] != 0:
                vsota_kvot += (1 / kvote[niz])
    for i in range(4):
        for j in range(4):
            niz = str(i) + ":" + str(j)
            if kvote[niz] == 0: slovar[niz] = 0
            else:
                slovar[niz] = 1 / (kvote[niz] * vsota_kvot)
    return slovar



### UPANJE REZULTATA ###
def upanje(rezultat, verjetnosti, popularni):
    upanje1 = 0
    for i in range(4):
        for j in range(4):
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

simulacija(verjetnosti(kvote), popularni_rezultati, ekipe)


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