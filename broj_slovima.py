a=input('unesi neki broj: ')
print(a)
print(f'broj cifara je {len(a)}')


jedinice = ["", "jedan", "dva", "tri", "četiri", "pet", "šest", "sedam", "osam", "devet"]
desetice = ["", "deset", "dvadeset", "trideset", "četrdeset", "pedeset", "šezdeset", "sedamdeset", "osamdeset", "devedeset"]

for i in reversed(a):
    print(a[int(i)])
