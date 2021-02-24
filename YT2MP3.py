"""
Youtube2MP3 程式說明:
本程式使用 Python 3.7 開發，使用模組為 PyQt5 及 youtube-dl ，影片轉MP3使用開源軟體 FFMPEG。
本程式會在 github 開放原始碼提供網友學習參考 程式執行中生成的媒體檔案請於24小時內刪除並勿用於商業用途以免觸法
"""
YT2MP3_VERSION="0001A"
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os,sys,requests,re,time
import yt2mp3_ui as ui
import pathlib,youtube_dl

class Main(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # 在 win10 路徑是 \\ ，在 macos 路徑是 /
        #self.save_dir=str(pathlib.Path().absolute())+"\\output\\"
        self.save_dir=str(pathlib.Path().absolute())+"/output/"
        self.movie_list=set()
        #若資料夾不存在就新增資料夾
        pathlib.Path(self.save_dir).mkdir(parents=True, exist_ok=True)
        self.setupUi(self)
        self.btn_saveMP3.clicked.connect(lambda: self.runDownloadAndSaveMp3())
        self.btn_get_from_playlist.clicked.connect(lambda: self.getLinkFromPlaylist(self.yt_playlist_url.text()))
        self.actionExit.setShortcut('Ctrl+Q')
        self.actionExit.triggered.connect(app.exit)
        self.actionOpen.setShortcut('Ctrl+O')
        self.actionOpen.triggered.connect(lambda: self.openFileNameDialog())
        self.actionSave.setShortcut('Ctrl+S')
        self.actionSave.triggered.connect(lambda: self.saveFileDialog())
        self.actionAbout_Yt2MP3.setShortcut('Ctrl+I')
        self.actionAbout_Yt2MP3.triggered.connect(lambda: self.show_message("關於Youtube2MP3","軟體版本 : "+YT2MP3_VERSION+"\n本軟體沒有任何說明!\n哈哈!"))
        #self.menubar.menuexample("actionExit").connect(lambda: self.menuAction(0))

    def getLinkFromPlaylist(self,playlist_url):
        self.btn_get_from_playlist.setEnabled(False)
        self.movie_list=set()
        if playlist_url!="":
            r=requests.get(playlist_url)
            r.encoding="utf-8"
            movie_links=re.findall(r"\/watch\?v=([^\\]+)",str(r.text))
            for link in movie_links:
                self.movie_list.add(link)
        #print(len(self.movie_list))
        out_str=""
        for i in self.movie_list:
            if out_str!="":
                out_str+="\n"
            out_str+="https://www.youtube.com/watch?v="+i
        # 將結果輸出到待轉出文字區塊
        self.plainTextEdit.setPlainText(out_str)
        self.btn_get_from_playlist.setEnabled(True)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"讀取文字檔", "","Text Files (*.txt)", options=options)
        if fileName:
            if ".txt" not in fileName: fileName+=".txt"
            #print(fileName)
            self.loadTxtFile(fileName)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"儲存文字檔","","Text Files (*.txt)", options=options)
        if fileName:
            if ".txt" not in fileName: fileName+=".txt"
            #print(fileName)
            self.saveTxtFile(fileName)

    def runDownloadAndSaveMp3(self):
        self.btn_get_from_playlist.setEnabled(False)
        self.btn_saveMP3.setEnabled(False)
        time.sleep(2)
        #讀取文字編輯區
        tmp_list=self.plainTextEdit.toPlainText().split("\n")
        tmp_count=0
        for i in tmp_list:
            if i!="" and i.find("watch?v=")>0:
                tmp_count+=1
                try:
                    self.subDownloadAndSaveMp3(i)
                except:
                    print(i+"下載出錯，跳過這個影片")
                    continue
        if tmp_count>0:
            self.show_message("影片轉檔MP3完成!","MP3下載轉檔完成!\n所有的檔案存放於 output 資料夾...")
        else:
            self.show_message("未進行任何影片轉檔!","請確認待轉檔連結內容是否正確，再重新轉檔...")
        self.btn_get_from_playlist.setEnabled(True)
        self.btn_saveMP3.setEnabled(True)

    def subDownloadAndSaveMp3(self,youtube_url):
        temp_filepath=self.save_dir+ '%(title)s-%(id)s.%(ext)s'
        ydl_opts = {
            'nocheckcertificate' : True,
            'format': 'bestaudio/best', # choice of quality
            'extractaudio' : True,      # only keep the audio
            'audioformat' : 'mp3',      # convert to mp3
            'outtmpl': temp_filepath,  # name the location
            'noplaylist' : True,        # only download single song, not playlist
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',

            }],
            #'logger': MyLogger(),
            #'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

    def show_message(self,msg_title,msg_content):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(msg_content)
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle(msg_title)
        #msg.setDetailedText("The details are as follows:")
        msg.exec_()

    def menuAction(self,action):
        if action==0:
            sys.exit(0)
    def addNumber(self, number):
        print(number)
        self.lEquation.insert(str(number))

    def textChanged(self, text, src):
        print(src, '=', text)

    def loadTxtFile(self,txtFileName):
        with open(txtFileName,"r",encoding="utf-8") as f:
            self.plainTextEdit.setPlainText(f.read())

    def saveTxtFile(self,txtFileName):
        #print(self.plainTextEdit.toPlainText())
        with open(txtFileName,"w+",encoding="utf-8") as f:
           f.write(self.plainTextEdit.toPlainText())

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())