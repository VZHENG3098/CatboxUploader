import re
import csv
import os
import time

import youtube_dl
import sys
import requests
import mimetypes
from os import path
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from catbox import CatboxUploader

import csv

songId = dict()


def downloadMusic(groupName):
    allGroup = dict()
    path = "KPOP/" + groupName
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)
    with open('SongsData.csv', encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            allGroup[row[6]] = row[20]
            print(row[6].row[20])
    groupId = 0

    return groupId
downloadMusic(("Blackpink"))

def _multipart_post(self, data):
    encoder = MultipartEncoder(fields=data)
    monitor = MultipartEncoderMonitor(encoder, callback=self._progress_bar)
    r = requests.post(self.file_host_url,
                      data=monitor,
                      headers={'Content-Type': monitor.content_type})
    return r


def createAlbum(albumName):
    uploader = CatboxUploader(albumName + "/")
    result = uploader.createNewAlbum(albumName)
    print(result)

    if result.find("moe/") != -1:
        print(result.split("moe/c/")[1])
        print("createdAlbum")
        return result.split("moe/c/")[1]
    return "fail"


def upload(groupName, id, groupId):
    print('ha')
    a_file = open("CatBoxData.csv", "a")
    with open("CatBoxData.csv", 'a', encoding='utf-8') as fd:
        writer = csv.writer(fd)
        for filename in os.listdir("KPOP/"+groupName):
            uploader = CatboxUploader("KPOP/"+groupName + "/" + filename)
            result = uploader.add(id)
            print(result)
            if result.find("moe/") != -1:
                a_dict = dict()
                a_dict["url"] = "https://files.catbox.moe/" + result.split("moe/")[1]
                a_dict["groupName"] = groupName
                a_dict["songName"] = filename.split("^^^^")[0]
                a_dict["albumUrl"] = "https://catbox.moe/c/" + id
                a_dict["groupId"] = groupId
                a_dict["songId"] = (filename.split("^^^^")[1]).split(".mp4")[0]
                writer.writerow(
                    [a_dict["songName"], a_dict["url"], a_dict["groupName"], a_dict["albumUrl"], a_dict["groupId"],
                     a_dict["songId"]])
                result = uploader.moveAlbum(id, result.split("moe/")[1])
                print(result)
                os.remove("KPOP/"+groupName + "/" + filename)
            else:
                print(filename + "was not uploaded/moved correctly")
    a_file.close()


def reformatCode(groupName):
    for filename in os.listdir(groupName):
        str = filename
        result = re.sub(r'[^\x00-\x7f]', r'', str)
        os.rename(groupName + "/" + filename, groupName + "/" + result)

def startProcess(name):
    groupName = name
    groupId = downloadMusic(groupName)
    id = createAlbum(groupName)
    # reformatCode(groupName)
    if id != "fail":
        print("Album")
        upload(groupName, id, groupId)
        with open("FinishedGroups.csv", 'a', encoding='utf-8') as fd:
            writer = csv.writer(fd)
            writer.writerow([name])
def main():
    finishedGroups = []
    with open('FinishedGroups.csv', encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if len(row) > 0:
                finishedGroups.append(row[0])

    with open('Artist.csv', encoding='utf-8') as csvDataFile:
        firstline = 0
        csvReader = csv.reader(csvDataFile)

        for row in csvReader:
            if firstline < 2:
                print("skip")
                firstline += 1
            elif len(row) > 0:
                if row[1] in finishedGroups:
                    print(row[1] + " has finished already")
                else:
                    print("Starting " + row[1])
                    startProcess(row[1])
                    print("sleeping")
                    time.sleep(1000)
                    print("continue")
#main()
#startProcess("Blackpink")


# upload(groupName,"rwp6j5","165")
