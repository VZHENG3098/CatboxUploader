import csv

songDict = dict()
with open('SongsDat2.csv', encoding='utf-8') as csvDataFile:
    firstline = 0
    csvReader = csv.reader(csvDataFile)

    for row in csvReader:
        if firstline < 1:
            firstline += 1
        elif len(row) > 0:
            songDict[int(row[0])] = row

tb = ["song_id","id_parent","kpop_name","kname","original_name","name_aka","vtype","tags","vlink","id_artist","id_original_artist","releasedate","publishedon","views","likes","dislikes","lastupdate","recentviews","recentlikes","awards","regionlocked","id","is_collab","name","fname","alias","id_company","id_artist1","id_artist2","id_artist3","id_artist4","members","issolo","id_parentgroup","id_currentgroup","formation","disband","social","id_debut","debut_date","date_birth","fanclub","miak","miak_level","sales","gaondigital_times","gaondigital_firsts","yawards","yawards_total","yt_followers"]
stringToTable = {}
for stuff in enumerate(tb):
    stringToTable[stuff[1]] = stuff[0]

listOfCurrentInformation = ["SongName","CatBoxLink","GroupName","AlbumName","ArtistId","SongId","Duration","releasedate","issolo","Gender"]
finalList = []
with open('CatBoxData.csv', encoding='utf-8') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        if len(row) > 0:
            row[5] = int(row[5].split(".")[0])
            songId = row[5]
            listofInformtionWanted = []
            for info in row:
               listofInformtionWanted.append(info)
            extraInformation = songDict[songId]
            listofInformtionWanted.append(extraInformation[stringToTable["releasedate"]])
            listofInformtionWanted.append(extraInformation[stringToTable["issolo"]])
            listofInformtionWanted.append(extraInformation[stringToTable["members"]])
            finalList.append(listofInformtionWanted)
with open("SongInformations.csv", 'a', encoding='utf-8') as fd:
    writer = csv.writer(fd)
    writer.writerow(["SongName","CatBoxLink","GroupName","AlbumName","ArtistId","SongId","Duration","releasedate","issolo","Gender"])
    for fileIn in finalList:
        writer.writerow(fileIn)