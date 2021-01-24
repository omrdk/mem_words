# This Python file uses the following encoding: utf-8
import os
import sys
import time
import random
import subprocess
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5 import QtTest
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QApplication, QLabel, QMainWindow, QShortcut, QAction, qApp, QMessageBox

file   = open('words.txt', 'r')         # *.txt file reading mode
lines   = file.readlines()              # readlines
file.close()                            # no longer need *.txt so close

class mainwindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainwindow, self).__init__(*args, **kwargs)

        uic.loadUi("mainwindow.ui", self)   # ui import
        global true_word
        global tr_word
        global cnt_t
        global cnt_f
        global selected_indexes
        cnt_t = 0
        cnt_f = 3
        selected_indexes = []                                 # indexes of selected lines
        self.main_view()                                          # First screen

        # Toolbar configuration
        self.toolBar = self.findChild(QToolBar, "toolbar")
        self.actionDictionary.triggered.connect(self.open_txt)
        self.actionDictionary.setIcon(QIcon("notebook--plus.png"))
        # Window configuration
        self.setWindowTitle("Memmorize")
        self.setFixedSize(400, 480)
        # Label definitions
        self.lbl_1  = self.findChild(QLabel,     "lbl_1"    )
        self.lbl_word  = self.findChild(QLabel,  "lbl_word" )
        self.lbl_count  = self.findChild(QLabel, "lbl_count")
        # Button definitions
        self.btn_skip  = self.findChild(QPushButton, "btn_skip" )
        self.btn_start = self.findChild(QPushButton, "btn_start")
        self.btn_end   = self.findChild(QPushButton, "btn_exit" )
        self.btn_rst   = self.findChild(QPushButton, "btn_rst")
        self.btn_A   = self.findChild(QPushButton, "btn_A")
        self.btn_B   = self.findChild(QPushButton, "btn_B")
        self.btn_C   = self.findChild(QPushButton, "btn_C")
        self.btn_D   = self.findChild(QPushButton, "btn_D")
        # Shortcuts for buttons
        self.btn_A.setShortcut( QKeySequence("1") )
        self.btn_B.setShortcut( QKeySequence("2") )
        self.btn_C.setShortcut( QKeySequence("3") )
        self.btn_D.setShortcut( QKeySequence("4") )


        self.btn_start.clicked.connect(self.back_count)                         # if btn_start is pressed then call fill_word function
        self.btn_skip.clicked.connect(self.fill_word)                           # if btn_slip is pressed then call fill_word function
        self.btn_exit.clicked.connect(self.main_view)                           # if btn_start is pressed then call main_page function
        self.btn_rst.clicked.connect(self.rst_words)
        self.btn_A.clicked.connect(lambda: self.check_word(self.btn_A.text()))  # btn_A'nın text'ini check_word fonksiyonuna gönderir
        self.btn_B.clicked.connect(lambda: self.check_word(self.btn_B.text()))  # if btn_start is pressed then call main_page function
        self.btn_C.clicked.connect(lambda: self.check_word(self.btn_C.text()))  # if btn_start is pressed then call main_page function
        self.btn_D.clicked.connect(lambda: self.check_word(self.btn_D.text()))  # if btn_start is pressed then call main_page function

        self.show()
    # open words.txt
    def open_txt(self):
        #os.system("kate words.txt")
        subprocess.call(('xdg-open', 'words.txt'))                              # opens a file default OS app

    # closeEvent
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close', 'Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def main_view(self):
        # Start-up content and states
        self.lbl_word.setText("Press START")                                    # print en_word to lbl_word label
        self.lbl_count.setText(str(cnt_t))
        self.lbl_1.setText(str(cnt_f))
        self.btn_skip.setEnabled(False)
        self.btn_rst.setEnabled(False)
        self.btn_start.setEnabled(True)
        self.btn_A.setEnabled(False)
        self.btn_B.setEnabled(False)
        self.btn_C.setEnabled(False)
        self.btn_D.setEnabled(False)

    # Count back
    def back_count(self):
        for i in range(3,0,-1):
            if i > 0:
                self.lbl_word.setText(str(i))
                QtTest.QTest.qWait(100)                                        #  time.sleep() is freezing the GUI!!
        self.fill_word()
        # Init states for buttons
        self.btn_skip.setEnabled(True)                                          # skip button is checkable now
        self.btn_start.setEnabled(False)                                        # start button is uncheckable now
        self.btn_A.setEnabled(True)
        self.btn_B.setEnabled(True)
        self.btn_C.setEnabled(True)
        self.btn_D.setEnabled(True)
        # Init_Vars
        global cnt_t
        global cnt_f
        cnt_t = 0
        cnt_f = 3
        self.lbl_count.setText(str(cnt_t))
        self.lbl_1.setText(str(cnt_f))

    # Insert to 'r' a random line number from words.txt and assign the name one of our buttons then do this for every index
    def fill_word(self):
        global selected_indexes
        if (len(lines) - len(selected_indexes) < 4):
            self.lbl_word.setText("Add words to your dictionary or reset the words")
            self.btn_rst.setEnabled(True)
            self.btn_A.setEnabled(False)
            self.btn_B.setEnabled(False)
            self.btn_C.setEnabled(False)
            self.btn_D.setEnabled(False)
            return

        choice_list = [0,1,2,3]
        btn_lst = [self.btn_A, self.btn_B, self.btn_C, self.btn_D]
        random_nums = []                                                                           # şıkların satır sayıları
        words = []
        for i in range(0,4,1):
            random_num = random.randint(0,len(lines) - 1)                                          # sonuncuyu alıyor mu??
            while ((random_num in random_nums) or (random_num in selected_indexes)):               # eğer olusturdugumuz random sayı random listte varsa veya onceden secılmısse tekrar random al
                random_num = random.randint(0,len(lines) - 1)
            random_nums.append(random_num)
            random_word = lines[random_num]
            words = random_word.split("=")
            en_word = words[0].strip()
            tr_word = words[1].strip()
            if i == 0:
                self.lbl_word.setText(en_word)
                global true_word
                true_word = tr_word
                selected_indexes.append(random_num)
            j = random.choice(choice_list)
            btn_lst[j].setText(tr_word)
            choice_list.remove(j)                                                                  # boş şık kalmasın
        #print(*random_nums)


    # Check the words, if they match than plus 1 true counter(cnt_t), else minus 1 false counter(cnt_f)
    def check_word(self, btn_word):
        global true_word
        if btn_word == true_word:
            global cnt_t
            cnt_t+=1
            self.lbl_count.setText(str(cnt_t))
            self.fill_word()
        else:
            global cnt_f
            cnt_f-=1
            self.lbl_1.setText(str(cnt_f))
            if cnt_f == 0:
                self.main_view()
                return
            self.fill_word()

    def rst_words(self):
        global selected_indexes
        selected_indexes = []                       # btn_rst basıldığında tekrarlanan sayıları tekrar listeye ekler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainwindow()
#    window.show()
    sys.exit(app.exec_())
