import os
directory = r'C:\Users\Quickode\Desktop\typeChart.txt'
pokemonTypes = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]

pokeDict = [
    #  Nor | Fir | Wat | Gra | Ele | Ice | Fig | Poi | Gro | Fly | Psy | Bug | Roc | Gho | Dra | Dar | Ste | Fai
    [  1,    1,    1,    1,    1,    1,    2,    1,    1,    1,    1,    1,    1,    0,    1,    1,    1,    1], #Normal
    [  1,  0.5,    2,  0.5,    1,  0.5,    1,    1,    2,    1,    1,  0.5,    2,    1,    1,    1,  0.5,  0.5], #Fire
    [  1,  0.5,  0.5,    2,    2,  0.5,    1,    1,    1,    1,    1,    1,    1,    1,    1,    1,  0.5,    1], #Water
    [  1,    2,  0.5,  0.5,  0.5,    2,    1,    2,  0.5,    2,    1,    2,    1,    1,    1,    1,    1,    1], #Grass
    [  1,    1,    1,    1,  0.5,    1,    1,    1,    2,  0.5,    1,    1,    1,    1,    1,    1,  0.5,    1], #Electric
    [  1,    2,    1,    1,    1,  0.5,    2,    1,    1,    1,    1,    1,    2,    1,    1,    1,    2,    1], #Ice
    [  1,    1,    1,    1,    1,    1,    1,    1,    1,    2,    2,  0.5,  0.5,    1,    1,  0.5,    1,    2], # Fighting
    [  1,    1,    1,  0.5,    1,    1,  0.5,  0.5,    2,    1,    2,  0.5,    1,    1,    1,    1,    1,  0.5], #Poison
    [  1,    1,    2,    2,    0,    2,    1,  0.5,    1,    1,    1,    1,  0.5,    1,    1,    1,    1,    1], #Ground
    [  1,    1,    1,  0.5,    2,    2,  0.5,    1,    0,    1,    1,  0.5,    2,    1,    1,    1,    1,    1], #Flying
    [  1,    1,    1,    1,    1,    1,  0.5,    1,    1,    1,  0.5,    2,    1,    2,    1,    2,    1,    1], #Psychic
    [  1,    2,    1,  0.5,    1,    1,  0.5,    1,  0.5,    2,    1,    1,    2,    1,    1,    1,    1,    1], #Bug
    [0.5,  0.5,    2,    2,    1,    1,    2,  0.5,    2,  0.5,    1,    1,    1,    1,    1,    1,    2,    1], #Rock
    [  0,    1,    1,    1,    1,    1,    0,  0.5,    1,    1,    1,  0.5,    1,    2,    1,    1,    1,    2], #Ghost
    [  1,  0.5,  0.5,  0.5,  0.5,    2,    1,    1,    1,    1,    1,    1,    1,    1,    2,    1,    1,    2], #Dragon
    [  1,    1,    1,    1,    1,    1,    2,    1,    1,    1,    0,    2,    1,  0.5,    1,  0.5,    1,    2], #Dark
    [0.5,    2,    1,  0.5,    1,  0.5,    2,    0,    2,  0.5,  0.5,  0.5,  0.5,    1,  0.5,    1,  0.5,  0.5], #Steel
    [  1,    1,    1,    1,    1,    1,  0.5,    2,    1,    1,    1,  0.5,    1,    1,    0,  0.5,    2,    1]  #Fairy
]

length = len(pokeDict)

print("Length: " + str(length))
f = open(directory, "w+")
for x in range(length):
    for y in range(x, length):
        secoundLength = len(pokeDict[y])
        ressitanceCount = 0
        extraLowCount = 0
        lowCount = 0
        normalCount = 0
        highCount = 0
        extraHighCount = 0
        overallTotal = 0
        if x == y:
            f.write(pokemonTypes[y] + ": \n")
            print(pokemonTypes[y] + ": ")
        else:
            f.write(pokemonTypes[x] + "-" + pokemonTypes[y] + ": \n")
            print(pokemonTypes[x] + "-" + pokemonTypes[y] + ": ")
        for z in range(0, secoundLength):
            if x == y:
                damage = 1 * pokeDict[x][z]
            else:
                damage = 1 * pokeDict[x][z] * pokeDict[y][z]

            if damage == 0:
                ressitanceCount += 1
                overallTotal += 1
            elif damage == 0.25:
                extraLowCount += 1
                overallTotal += 1
            elif damage == 0.5:
                lowCount += 1
                overallTotal += 0.5
            elif damage == 1:
                normalCount += 1
            elif damage == 2:
                highCount += 1
                overallTotal -= 0.5
            elif damage == 4:
                overallTotal -= 1
                extraHighCount += 1
            f.write("Gets Damage from " + pokemonTypes[z] + " that is: " + str(damage) + "\n")
            print("Gets Damage from " + pokemonTypes[z] + " that is: " + str(damage) + "\n")
        f.write("No Effect: " + str(ressitanceCount) + "\n")
        f.write("Double Not Very Effective: " + str(extraLowCount) + "\n")
        f.write("Not Very Effective: " + str(lowCount) + "\n")
        f.write("Normal: " + str(normalCount) + "\n")
        f.write("Super Efective: " + str(highCount) + "\n")
        f.write("Double Super Efective: " + str(extraHighCount) + "\n")
        f.write("Overall Total: " + str(overallTotal) + "\n")
        f.write("-------------------------------------\n")
    print("-------------------------------------")


f.close()

        