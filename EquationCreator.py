def fixedPlaceEquation(rowNum):
    rowPlus1 = str(rowNum + 1)
    return '=IF(INT(H' + rowPlus1 + ')<10,CONCATENATE("00",H' + rowPlus1 + '),IF(INT(H' + rowPlus1 + ')<100,CONCATENATE("0",H' + rowPlus1 + '),H' + rowPlus1 + '))'


def fixedSeasonAndEpisodeNumberEquation(rowNum, letter):
    rowPlus1 = str(rowNum + 1)
    return '=IF(INT(' + letter + rowPlus1 + ')<10,CONCATENATE("0",' + letter + rowPlus1 + '),' + letter + rowPlus1 + ')'


def nameStickerEquation(rowNum):
    rowPlus1 = str(rowNum + 1)
    return '=CONCATENATE(I' + rowPlus1 + ',". ",A' + rowPlus1 + '," S",I' + rowPlus1 + ',"E",J' + rowPlus1 + ', " - ",D' + rowPlus1 + ')'