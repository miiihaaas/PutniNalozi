def proracun_broja_dnevnica(br_casova):
    if br_casova < 8:
        br_dnevnica = 0.0
        print(f'ispod 8h: {br_dnevnica=}')
    elif br_casova < 12:
        br_dnevnica = 0.5
        print(f'od 8h do 12h: {br_dnevnica=}')
    else:
        br_dnevnica = br_casova / 24
        print(f'proračun: {br_dnevnica=}')
        if br_dnevnica % 1 <= (8/24): #zaokruživanje na 0.5 (da li je 0-12h ili 8-12h)
            #zaokruži na x.0
            br_dnevnica = br_dnevnica // 1
            print(f'zaokruživanje na pola dnevnice: {br_dnevnica=}')
        elif br_dnevnica % 1 <= (12/24): #zaokruživanje na 0.5 (da li je 0-12h ili 8-12h)
            #zaokruži na x.5
            br_dnevnica = br_dnevnica // 1 + 0.5
            print(f'zaokruživanje na pola dnevnice: {br_dnevnica=}')
        else:
            #zaokruži na x+1
            br_dnevnica = br_dnevnica // 1 + 1
            print(f'zaokruživanje na celu dnevnicu: {br_dnevnica=}')
    br_dnevnica = br_dnevnica * 1.0
    return br_dnevnica