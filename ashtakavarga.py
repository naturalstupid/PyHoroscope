from collections import Counter
panchanga = __import__('panchanga')

ashtaka_varga_dict={
    "0":[[1,2,4,7,8,9,10,11],[3,6,10,11],[1,2,4,7,8,9,10,11],[3,5,6,9,10,11,12],[5,6,9,11],[6,7,12],[1,2,4,7,8,9,10,11],[3,4,6,10,11,12]],
    "1":[[3,6,7,8,10,11 ],[1,3,6,7,10,11],[2,3,5,6,10,11],[1,3,4,5,7,8,10,11],[1,2,4,7,8,10,11],[3,4,5,7,9,10,11],[3,5,6,11],[3,6,10,11]],
    "2":[[3,5,6,10,11],[3,6,11],[1,2,4,7,8,10,11],[3,5,6,11],[6,10,11,12],[6,8,11,12],[1,4,7,8,9,10,11],[1,3,5,10,11]],
    "3":[[5,6,9,11,12],[2,4,6,8,10,11],[1,2,4,7,8,9,10,11],[1,3,5,6,9,10,11,12],[6,8,11,12],[1,2,3,4,5,8,9,11],[1,2,4,7,8,9,10,11],[1,2,4,6,8,10,11]],
    "4":[[1,2,3,4,7,8,9,10,11],[2,5,7,9,11],[1,2,4,7,8,10,11],[1,2,4,5,6,9,10,11],[1,2,3,4,7,8,10,11],[2,5,6,9,10,11],[3,5,6,12],[1,2,4,5,6,7,9,10,11]],
    "5":[[8,11,12],[1,2,3,4,5,8,9,11,12],[3,4,6,9,11,12],[3,5,6,9,11],[5,8,9,10,11],[1,2,3,4,5,8,9,10,11],[3,4,5,8,9,10,11],[1,2,3,4,5,8,9,11]],
    "6":[[1,2,4,7,8,10,11],[3,6,11],[3,5,6,10,11,12],[6,8,9,10,11,12],[5,6,11,12],[6,11,12],[3,5,6,11],[1,3,4,6,10,11]],
    "7":[[3,4,6,10,11,12],[3,6,10,11,12],[1,3,6,10,11],[1,2,4,6,8,10,11],[1,2,4,5,6,7,9,10,11],[1,2,3,4,5,8,9],[1,3,4,6,10,11],[3,6,10,11]]
    }
planet_list = ['sun','moon','mars','mercury','jupiter','venus','saturn','lagnam']
raasi_list=['Mesham','Rishabam','Mithunam','Katakam','Simmam','Kanni','Thulaam','Vrichigam','Dhanusu','Makaram','Kumbam','Meenam']
raasi_index = lambda planet,planet_positions_in_chart: [i for i,raasi in enumerate(planet_positions_in_chart) if planet.lower() in raasi.lower() ][0]
def ashtaka_varga_chart(planet_positions_in_chart):
    raasi_ashtaka = [[0 for r in range(12)] for p in range(9)]
    prastara_ashtaka_varga  = [[[0 for r in range(12)] for p1 in range(9)] for p2 in range(9)]
    for key in ashtaka_varga_dict.keys():
        p = int(key)
        planet = planet_list[p]
        planet_raasi_list = ashtaka_varga_dict[key]
        for op,other_planet in enumerate(planet_raasi_list):
            pr = raasi_index(planet_list[op],planet_positions_in_chart)
            for raasi in other_planet:
                r = (raasi-1+pr) % 12
                raasi_ashtaka[p][r] +=1
                prastara_ashtaka_varga[p][op][r] = 1
    planet_ashtaka_chart = [ [] for i in range(8) ]
    for planet in range(8):
        for raasi in range(12):
            planet_ashtaka_chart[planet].append(raasi_ashtaka[planet][raasi])
    samudhaya_ashtaka_varga = [0 for i in range(12)]
    for raasi in range(12):
        for planet in range(7): # Exclude Lagnam
            samudhaya_ashtaka_varga[raasi] += planet_ashtaka_chart[planet][raasi]
    return planet_ashtaka_chart, samudhaya_ashtaka_varga,prastara_ashtaka_varga
if __name__ == "__main__":
    planet_positions_in_chart = ['','','','','Mars','Rahu','Moon/Venus','Sun','Mercury/Jupiter','Lagnam','','Saturn/Ketu']
    planet_ashtaka,samudhaya_ashtaka_varga,prastara_ashtaka_varga = ashtaka_varga_chart(planet_positions_in_chart)
    for planet in range(8):
        print(planet_list[planet],planet_ashtaka[planet])
    print('samidhaya ashtaka varga',samudhaya_ashtaka_varga)