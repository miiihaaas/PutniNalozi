# while True:
#     a=int(input('unesi neki broj: '))
#     print(a)
#     # print(f'broj cifara je {len(a)}')

def number_to_text(a):
    jedinice = ["", "jedan", "dva", "tri", "četiri", "pet", "šest", "sedam", "osam", "devet"]
    druga_dekada = ["", "deset", "jedanaest", "dvanaest", "trinaest", "četrdeset", "petnaest", "šesnaest", "sedamnaest", "osamnaest", "devetnaest"]
    desetice = ["", "deset", "dvadeset", "trideset", "četrdeset", "pedeset", "šezdeset", "sedamdeset", "osamdeset", "devedeset"]
    stotine = ["", "sto", "dvesta", "trista", "četiristo", "petsto", "šesto", "sedamsto", "osamsto", "devetsto"]
    hiljade_10 = ["", "hiljadu", "dvehiljade", "trihiljiade", "četirihiljade", "pethiljada", "šesthiljada", "sedamhiljada", "osamhiljada", "devethiljada"]
    
    def under_100(number):
        if number < 10:
            slovima = jedinice[number]
        elif number < 20:
            slovima = druga_dekada[number-9]
            print(slovima)
        else:
            last_digit = int(str(number)[1])
            last_1_digit = int(str(number)[0])
            print(f'prva cifra broja {number} je {last_1_digit}')
            print(f'poslednja cifra broja {number} je {last_digit}')
            slovima = desetice[last_1_digit] + jedinice[last_digit]
            print(slovima)
        return slovima

    def under_1000(number):
        if number < 100:
            slovima = under_100(number)
        else:
            last_2_digit = int(str(number)[0])
            slovima = stotine[last_2_digit]
            print(slovima)
            l2d = number - last_2_digit * 100 #! poslednje dve cifre
            print(f'poslednje dve cifre {l2d}')
            slovima_l2d = under_100(l2d)
            print(slovima_l2d)
            slovima = slovima + slovima_l2d
            print(slovima)
        return slovima
    
    def under_10000(number):
        last_3_digit = int(str(number)[0])
        slovima = hiljade_10[last_3_digit]
        print(slovima)
        l3d = number - last_3_digit * 1000 #! poslednje tri cifre
        slovima_l3d = under_1000(l3d)
        print(slovima_l3d)
        slovima = slovima + slovima_l3d
        print(slovima)
        return slovima
    
    def under_100000(number):
        f2d = int(str(number)[:2]) #! prve dve cifre
        _2d = int(str(number)[1:2]) #! druga cifra
        print(f'prve dve cifre su: {f2d}')
        if _2d in [2, 3, 4]:
            slovima = under_100(f2d) + 'hiljade' #? ovo važi za hiljade od 5 do 10 - treba if kod koji će da piše "hiljade" za 2-4
        else:
            slovima = under_100(f2d) + 'hiljada' #? ovo važi za hiljade od 5 do 10 - treba if kod koji će da piše "hiljade" za 2-4
        print(slovima)
        l3d = number - f2d * 1000 #! poslednje tri cifre
        slovima_l3d = under_1000(l3d)
        print(slovima_l3d)
        slovima = slovima + slovima_l3d
        print(slovima)
        return slovima

    if a < 10:
        slovima = jedinice[a]
        print(slovima)
    elif a < 20:
        slovima = druga_dekada[a-9]
        print(slovima)
    elif a < 100:
        slovima = under_100(a)
        print(f'iz if bloka <100: {slovima}')
    elif a < 1000:
        slovima = under_1000(a)
        print(f'iz if bloka <1 000: {slovima}')
    elif a < 10000:
        slovima = under_10000(a)
        print(f'iz if bloka <10 000: {slovima}')
    elif a < 100000:
        slovima = under_100000(a)
        print(f'iz if bloka <100 000: {slovima}')
    return slovima

