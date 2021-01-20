from __future__ import unicode_literals

from base import Uploader


class CatboxUploader(Uploader):
    def __init__(self, filename):
        self.filename = filename
        self.file_host_url = "https://catbox.moe/user/api.php"

    def moveAlbum(self,albumNum,alsoFile):
        file = open(self.filename, 'rb')
        try:
            data = {
                'reqtype': 'addtoalbum',
                'userhash': '', #removed hashed
                'short': albumNum,
                'files': alsoFile
            }
            response = self._multipart_post(data)
        finally:
            file.close()

        return response.text
    def add(self,albumNum):
        file = open(self.filename, 'rb')
        try:
            data = {
                'reqtype': 'fileupload',
                'userhash': '', #removed hashed
                'fileToUpload': (file.name, file, self._mimetype())
            }
            response = self._multipart_post(data)
        finally:
            file.close()

        return response.text
    def createNewAlbum(self,titleName):
        try:
            data = {
                'reqtype': 'createalbum',
                'title': titleName,
                'userhash': '', #removed hashed
                'desc' : titleName+" Songs",
                'files':""
            }
            response = self._multipart_post(data)
        finally:
            print("done")
        return response.text
