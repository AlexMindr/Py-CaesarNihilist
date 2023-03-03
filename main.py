import sys
import numpy as np

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

interface = sg.Window('Criptare si Decriptare Cifrul Caesar+Nihilist ').Layout(
    [[sg.Text('Filepath')], [sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()], [sg.Text('Input file format is:\n1st line criptare/decriptare\n2nd,3rd,4th lines the keys\n5th line the word'
                                                                                            '\nfor examples see example.txt')]])

alfabet0 = 'abcdefghijklmnopqrstuvwxyz'


def toNumber(a):
    for i in range(0, 25):
        if a == alfabet0[i]:
            return i


def toAlphabet(n):
    return alfabet0[n]


def matricezero(x, y, zero):
    return [[zero for i in range(x)] for j in range(y)]


def coordonate(cuvant, matrice):
    vectorcoord = []
    for litera in cuvant:
        for i in range(5):
            for j in range(5):
                if litera.lower() == matrice[i][j]:
                    vectorcoord.append((i + 1) * 10 + j + 1)
                    break

    return vectorcoord


def cripteaza(cuvant, cheie, cheie2):
    cheiecarunic = ""
    for caracter in cheie:
        if caracter not in cheiecarunic:
            cheiecarunic += caracter
    matrice = matricezero(5, 5, 0)
    alfabet = "abcdefghiklmnopqrstuvwxyz"
    for litera in cheiecarunic:
        alfabet = alfabet.replace(litera, '')
    k = 0
    t = 0
    for i in range(5):
        for j in range(5):
            if k < len(cheiecarunic):
                matrice[i][j] = cheiecarunic[k].lower()
                k += 1
            else:
                if t < len(alfabet):
                    matrice[i][j] = alfabet[t]
                    t += 1

    vectorliterecriptate = coordonate(cuvant, matrice)
    vectorcheie = coordonate(cheie2, matrice)

    for i in range(len(vectorliterecriptate) // len(vectorcheie) - 1):
        vectorcheie += vectorcheie
    if len(vectorliterecriptate) % len(vectorcheie) != 0:
        for i in range(len(vectorliterecriptate) % len(vectorcheie)):
            vectorcheie.append(vectorcheie[i])

    vectorliterecriptate = np.array(vectorliterecriptate)
    vectorcheie = np.array(vectorcheie)
    vectorcriptat = vectorliterecriptate + vectorcheie

    return vectorcriptat


def decripteaza(cuvantcriptat, cheie, cheie2):
    cuvantcriptat = cuvantcriptat.split()
    vectorliterecriptate = []
    for cuvant in cuvantcriptat:
        vectorliterecriptate.append(int(cuvant))

    cheiecarunic = ""
    for caracter in cheie:
        if caracter not in cheiecarunic:
            cheiecarunic += caracter

    alfabet = "abcdefghiklmnopqrstuvwxyz"
    matrice = matricezero(5, 5, 0)
    for litera in cheiecarunic:
        alfabet = alfabet.replace(litera, '')
    k = 0
    t = 0
    for i in range(5):
        for j in range(5):
            if (k < len(cheiecarunic)):
                matrice[i][j] = cheiecarunic[k].lower()
                k += 1
            else:
                if (t < len(alfabet)):
                    matrice[i][j] = alfabet[t]
                    t += 1
    vectorcheie = coordonate(cheie2, matrice)

    for i in range(len(vectorliterecriptate) // len(vectorcheie) - 1):
        vectorcheie += vectorcheie
    if len(vectorliterecriptate) % len(vectorcheie) != 0:
        for i in range(len(vectorliterecriptate) % len(vectorcheie)):
            vectorcheie.append(vectorcheie[i])

    vectorliterecriptate = np.array(vectorliterecriptate)
    vectorcheie = np.array(vectorcheie)
    vectordecriptat = vectorliterecriptate - vectorcheie
    solutie = ""
    for literacriptata in vectordecriptat:
        for i in range(5):
            for j in range(5):
                if i == literacriptata // 10 - 1 and j == literacriptata % 10 - 1:
                    solutie += matrice[i][j]
    return solutie


event, values = interface.Read()
# print(event, values)

if event != 'Cancel':
    fin = open(values[0], "r")
    continutFisier = fin.readlines()
    fin.close()
    fout = open("output.txt", "w")
    count = 0
    actiune = ''
    cheieCaesar = ''
    cheieNihilist1 = ''
    cheieNihilist2 = ''

    for line in continutFisier:
        line = line.strip()
        if count == 0:
            #print(line)
            actiune = line
            count += 1
        elif count == 1:
            try:
                cheieCaesar = int(line)
            except:
                fout.write('Cheie incorecta!')
                break
            count += 1
        elif count == 2:
            try:
                cheieNihilist1 = str(line)
            except:
                fout.write('Cheie incorecta!')
                break
            count += 1
        elif count == 3:
            try:
                cheieNihilist2 = str(line)
            except:
                fout.write('Cheie incorecta!')
                break
            count += 1
        else:
            if actiune == 'criptare':
                sir = line.replace(' ', '')
                #print("initial: " + sir)
                sirprimacriptare = ''
                for caracter in sir:
                    sirprimacriptare += toAlphabet((toNumber(caracter.lower()) + cheieCaesar) % 26)
                #print('dupa prima criptare: ' + sirprimacriptare)
                siradouacriptare = cripteaza(sirprimacriptare, cheieNihilist1, cheieNihilist2)
                #print('dupa a doua criptare: ')
                #print(siradouacriptare)
                fout.write("Dupa criptare rezultatul este:\n")
                fout.write(str(siradouacriptare)[2:-1])

            elif actiune == 'decriptare':
                sir = line
                #print("initial: " + sir)
                sirprimadecriptare = decripteaza(sir, cheieNihilist1, cheieNihilist2)
                siradouadecriptare = ''
                #print('dupa prima decriptare: ' + sirprimadecriptare)
                for caracter in sirprimadecriptare:
                    siradouadecriptare += toAlphabet((toNumber(caracter.lower()) - cheieCaesar) % 26)
                #print('dupa a doua decriptare ' + siradouadecriptare)
                fout.write("Dupa decriptare rezultatul este:\n")
                fout.write(siradouadecriptare.upper())

    fout.close()

interface.Close()
