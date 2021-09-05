
# from imdb import IMDb

# ia = IMDb()
# series = ia.get_movie("2467372")
# print("----------------------------------series 1------------------------------------------")
# print(series)
# print("----------------------------------------------------------------------------")
# ia.update(series, "episodes")
# print("----------------------------------series[episodes]------------------------------------------")
# print(series["episodes"])
# print("----------------------------------------------------------------------------")
# SeasonsArr = sorted(series["episodes"].keys())
# for SeasonNum in SeasonsArr:
#     seasonx = series["episodes"][SeasonNum]
#     EpisodeArr = sorted(seasonx)
#     for episodz in EpisodeArr:
#         episode = series["episodes"][SeasonNum][episodz]
#         print("----------------------------------episode------------------------------------------")
#         print(episode)
#         print("-------------------------------xxxxx---------------------------------------------")
#         for x in episode.keys():
#             print(str(x) + " : " + str(episode[x]))
#         break
#     break


# f = open("first_signal.txt", "r")
# if f.mode == 'r':
#     f1 = f.readlines()
#     print(f1)
#     for x in f1:
#         print(x)
import os

# directory = r'C:\Users\Quickode\Desktop\first_signal.txt'
# output = r'C:\Users\Quickode\Desktop\output.txt'
# f = open(directory, "r")
# fi = open(output, "w+")
# f1 = f.readlines()
# indent = ""
# newString = ""
# for x in f1:
#     vcv = list(x)
#     for y in vcv:
#         newline = ""
#         currentIdent = ""
#         if y == '[':
#             indent += "    "
#             newString +=  y + "\n" + indent
#         elif y == ']':
#             indent = indent[:-4]
#             newString += "\n" + indent + y
#         else:
#             newString += y
# print(newString)
# fi.write(newString)
# fi.close()
# f.close()
directory = r'C:\Users\Quickode\Desktop\first_signal.txt'
output = r'C:\Users\Quickode\Desktop\output.txt'
f = open(directory, "r")
fi = open(output, "w+")
f1 = f.readlines()
level = 0
indent = ""
newString = ""
for x in f1:
    vcv = list(x)
    for y in vcv:
        newline = ""
        currentIdent = ""
        if y == '[':
            level = level + 1
            newString +=  "<Level" + str(level) + ">\n"
        elif y == ']':
            newString += "\n</Level" + str(level) + ">\n"
            level = level - 1
        elif y == ',':
            print(',')
        else:
            newString += y
print(newString)
fi.write(newString)
fi.close()
f.close()