
import re
import csv
import os
import youtube_dl
import sys
import requests
import mimetypes
from os import path
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from catbox import CatboxUploader

import csv

with open('CatBoxData.csv',encoding='utf-8') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        if len(row)>0:
            row[1] = '"'+row[1]+'"'
            row[0] = '"' + row[0] + '"'
            row[2] = '"' + row[2] + '"'
            row[3] = '"' + row[3] + '"'
            row[5] = '"' + row[5] + '"'
            print("INSERT INTO Songs SET"+" Song_Id =" +(row[5])+", Song_Name =" +row[0]+", CatBoxUrl =" +row[1]
                  +", CatBoxAlbum =" +row[3]+", Group_Name =" +row[2]+";")