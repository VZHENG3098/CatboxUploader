import re
import csv
import os
import time

import yt_dlp
import os
import sys
import requests
import mimetypes
from os import path
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from moviepy.editor import VideoFileClip
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
    with open('SongsDat2.csv', encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            allGroup[row[9]] = row[22]
    groupId = 0
    with open('SongsDat2.csv', encoding='UTF-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if row[6] == 'main' and allGroup[row[9]] == groupName:
                groupId = row[9]

                if int(row[13]) > 500000 and row[8] != "#NAME" and row[8] != "":
                    if "r" in row[7] or "d" in row[7] or "j" in row[7] or "a" in row[7] or "z" in row[7] or "d" in row[7] or "e" in row[7]  or "c" in row[7]:
                        print(row[7])
                    else:
                        ydl_opts = {'format': 'bestvideo[height<=?1080]+bestaudio/best[filesize<75M]','outtmpl': "KPOP/"+groupName + '/' + row[2] + "^^^^" + row[0] + ".%(ext)s",'forceip':'4'}
                        print(int(row[13]),row[13],"Views")
                        if int(row[13]) < 25000000 and int(row[13]) > 5000000:
                            ydl_opts = {'format': 'bestvideo[height<=?720]+bestaudio/best',
                                        'outtmpl': "KPOP/" + groupName + '/' + row[2] + "^^^^" + row[0] + ".%(ext)s",
                                        'forceip': '4'}
                            print("Lowered Quality")
                        elif(int(row[13]) < 5000000):
                            ydl_opts = {'format': 'bestvideo[height<=?360]+bestaudio/best',
                                        'outtmpl': "KPOP/" + groupName + '/' + row[2] + "^^^^" + row[0] + ".%(ext)s",
                                        'forceip': '4'}
                            print("Lowered Quality2")
                        try:
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                ydl.download(['https://www.youtube.com/watch?v=' + row[8]])
                        except:
                            print("error")
                else:
                    print("Too Low View Count")
    return groupId


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
                clip = VideoFileClip("KPOP/"+groupName + "/" + filename)
                print(clip.duration)
                a_dict = dict()
                a_dict["url"] = "https://files.catbox.moe/" + result.split("moe/")[1]
                a_dict["groupName"] = groupName
                a_dict["songName"] = filename.split("^^^^")[0]
                a_dict["albumUrl"] = "https://catbox.moe/c/" + id
                a_dict["groupId"] = groupId
                a_dict["songId"] = (filename.split("^^^^")[1]).split(".mp4")[0]
                a_dict["SongLength"] = clip.duration
                writer.writerow(
                    [a_dict["songName"], a_dict["url"], a_dict["groupName"], a_dict["albumUrl"], a_dict["groupId"],
                     a_dict["songId"]])
                clip.close()
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


    path, dirs, files = next(os.walk("KPOP/"+groupName + "/"))
    if len(files) > 0:
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

    with open('ArtistCheck.csv', encoding='utf-8') as csvDataFile:
        firstline = 0
        csvReader = csv.reader(csvDataFile)

        for row in csvReader:
            if firstline < 2:
                firstline += 1
            elif len(row) > 0:
                if row[1] in finishedGroups:
                    print(row[2] + " has finished already")
                else:
                    print("Starting " + row[2])
                    startProcess(row[2])
                    print("sleeping")
                    time.sleep(5)
                    print("continue")
main()
#startProcess("Blackpink")


# upload(groupName,"rwp6j5","165")
