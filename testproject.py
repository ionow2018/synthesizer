import sys
import math
import wave
import numpy
import pyaudio
from PyQt5 import uic
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMessageBox,\
     QMainWindow, QInputDialog, QFileDialog


def sine(frequency, length, rate):  # создаём значения синусов на сигнал
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return numpy.sin(numpy.arange(length) * factor)


def play_tone(stream, frequency=440, length=1, rate=44100):
    # воспроизводим сигнал
    chunks = list()
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) * 0.25
    stream.write(chunk.astype(numpy.float32).tostring())


def write_tone(frequency=440, length=1, rate=44100):
    # подготовка данных для записи в wav
    chunks = list()
    chunks.append(sine(frequency, length, rate))
    chunk = numpy.concatenate(chunks) * 0.25
    return chunk.astype(numpy.float32)


class MyWidget(QMainWindow):  # класс с виджетом
    def __init__(self):
        super().__init__()
        uic.loadUi('1o.ui', self)
        self.lbl = ""
        self.oct = "4"
        self.dlit = "2"
        self.note = "A"
        self.radioButton_1.clicked.connect(self.run1)
        self.radioButton_2.clicked.connect(self.run2)
        self.radioButton_4.clicked.connect(self.run4)
        self.radioButton_8.clicked.connect(self.run8)
        self.radioButton_16.clicked.connect(self.run16)
        self.radioButton_83.clicked.connect(self.run83)
        self.radioButton_84.clicked.connect(self.run84)
        self.radioButton_85.clicked.connect(self.run85)
        self.radioButton_86.clicked.connect(self.run86)
        self.pushButton_z.clicked.connect(self.runZ)
        self.pushButton_x.clicked.connect(self.runX)
        self.pushButton_c.clicked.connect(self.runC)
        self.pushButton_v.clicked.connect(self.runV)
        self.pushButton_b.clicked.connect(self.runB)
        self.pushButton_n.clicked.connect(self.runN)
        self.pushButton_m.clicked.connect(self.runM)
        self.pushButton_s.clicked.connect(self.runS)
        self.pushButton_d.clicked.connect(self.runD)
        self.pushButton_g.clicked.connect(self.runG)
        self.pushButton_h.clicked.connect(self.runH)
        self.pushButton_j.clicked.connect(self.runJ)
        self.pushButton_p.clicked.connect(self.runP)
        self.sbut.clicked.connect(self.save)
        self.obut.clicked.connect(self.open)
        self.rbut.clicked.connect(self.rset)
        self.pbut.clicked.connect(self.play)
        self.testB.clicked.connect(self.savewav)
        self.qbut.clicked.connect(QCoreApplication.instance().quit)
        self.notes = {'C': 261.63, 'D': 293.66, 'E': 329.63, 'F': 349.23,
                      'G': 392.00, 'A': 440.00, 'H': 493.88, 'J': 277.19,
                      'K': 311.12, 'L': 370.00, 'M': 415.31, 'N': 466.16,
                      "P": 0}  # Частоты для нот 4-й октавы

    def keyPressEvent(self, event):  # обработка нажатия клавиш
        if event.key() == Qt.Key_Z:
            self.runZ()
        elif event.key() == Qt.Key_X:
            self.runX()
        elif event.key() == Qt.Key_C:
            self.runC()
        elif event.key() == Qt.Key_V:
            self.runV()
        elif event.key() == Qt.Key_B:
            self.runB()
        elif event.key() == Qt.Key_N:
            self.runN()
        elif event.key() == Qt.Key_M:
            self.runM()
        elif event.key() == Qt.Key_S:
            self.runS()
        elif event.key() == Qt.Key_D:
            self.runD()
        elif event.key() == Qt.Key_G:
            self.runG()
        elif event.key() == Qt.Key_H:
            self.runH()
        elif event.key() == Qt.Key_J:
            self.runJ()
        elif event.key() == 16777251 or event.key() == 16777249:
            # Alt или Ctrl - пауза
            self.runP()
        elif event.key() == 59:  # Нажата ;
            if int(self.dlit) > 0:
                self.dlit = str(int(self.dlit)-1)
                if self.dlit == "2":
                    self.radioButton_4.setChecked(True)
                elif self.dlit == "0":
                    self.radioButton_1.setChecked(True)
                elif self.dlit == "1":
                    self.radioButton_2.setChecked(True)
                elif self.dlit == "3":
                    self.radioButton_8.setChecked(True)
                elif self.dlit == "4":
                    self.radioButton_16.setChecked(True)
        elif event.key() == 92:  # Нажата \
            if int(self.dlit) < 4:
                self.dlit = str(int(self.dlit)+1)
                if self.dlit == "2":
                    self.radioButton_4.setChecked(True)
                elif self.dlit == "0":
                    self.radioButton_1.setChecked(True)
                elif self.dlit == "1":
                    self.radioButton_2.setChecked(True)
                elif self.dlit == "3":
                    self.radioButton_8.setChecked(True)
                elif self.dlit == "4":
                    self.radioButton_16.setChecked(True)
        elif event.key() == 91:  # Нажата [
            if int(self.oct) > 3:
                self.oct = str(int(self.oct)-1)
                if self.oct == "3":
                    self.radioButton_83.setChecked(True)
                elif self.oct == "4":
                    self.radioButton_84.setChecked(True)
                elif self.oct == "5":
                    self.radioButton_85.setChecked(True)
        elif event.key() == 39:  # Нажата '
            if int(self.oct) < 6:
                self.oct = str(int(self.oct)+1)
                if self.oct == "6":
                    self.radioButton_86.setChecked(True)
                elif self.oct == "4":
                    self.radioButton_84.setChecked(True)
                elif self.oct == "5":
                    self.radioButton_85.setChecked(True)

    def savewav(self):  # сохранение в файл wav
        st, okBtnPressed = QInputDialog.getText(
            self, "Сохранение файла", "Введите имя файла")
        if okBtnPressed:
            chunks = []
            for i in range(2, len(self.lbl), 3):
                chunks.append(write_tone(self.notes[self.lbl[i-2]] * 2 **
                              (int(self.lbl[i-1]) - 4), 2 / 2 **
                              int(self.lbl[i])))
            wf = wave.open(st + ".wav", 'wb')
            wf.setnchannels(2)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(chunks))
            wf.close()

    def run(self, button):  # записываем и проигрываем ноту
        self.note = button
        self.lbl = self.lbl + button + self.oct + self.dlit
        if len(self.lbl) > 60:
            self.label_2.setText(self.lbl[60:])
        else:
            self.label.setText(self.lbl)
        #                 ▼буква, обозначающая ноту        ▼номер октавы
        play_tone(stream, self.notes[self.note] * 2 ** (int(self.oct) - 4),
                  2 / 2 ** int(self.dlit))
        #                      ▲номер, обозначающий длительность

    def play(self):  # воспроизводим все записанные ноты
        for i in range(2, len(self.lbl), 3):
            play_tone(stream, self.notes[self.lbl[i-2]] * 2 **
                      (int(self.lbl[i-1]) - 4), 2 / 2 ** int(self.lbl[i]))

    def rset(self):  # сброс к начальному состоянию
        self.lbl = ""
        self.label.setText(self.lbl)
        self.label_2.setText(self.lbl)
        self.oct = "4"
        self.radioButton_84.setChecked(True)
        self.dlit = "2"
        self.radioButton_4.setChecked(True)

    def save(self):  # сохраняем в виде текста
        opn = False
        if len(self.lbl) == 0:
            qtn = "Пока сохранять нечего. Все равно записать файл?"
            buttonReply = QMessageBox.question(self, 'Предупреждение', qtn,
                                               QMessageBox.Yes |
                                               QMessageBox.No,
                                               QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                opn = True
        else:
            opn = True
        if opn:
            fname, okBtnPressed = QFileDialog.getSaveFileName(
                self, "Сохранение файла", "", "*.txt")
            if okBtnPressed:
                f = open(fname, 'w')
                f.write(self.lbl)
                f.close()

    def open(self):  # Открытие сохранённую в виде текста мелодию
        opn = False
        if len(self.lbl) != 0:
            qtn = "Есть несохранённая информация. Все равно открыть файл?"
            buttonReply = QMessageBox.question(self, 'Предупреждение', qtn,
                                               QMessageBox.Yes |
                                               QMessageBox.No,
                                               QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                opn = True
        else:
            opn = True
        if opn:
            fname, okBtnPressed = QFileDialog.getOpenFileName(
                self, 'Открываем файл', '', '*.txt')
            if okBtnPressed:
                f = open(fname, 'r')
                self.lbl = f.read()
                self.label.setText(self.lbl)

    def run1(self):     # функции, вызываемые при нажатии клавиш синтезатора
        self.dlit = "0"

    def run2(self):
        self.dlit = "1"

    def run4(self):
        self.dlit = "2"

    def run8(self):
        self.dlit = "3"

    def run16(self):
        self.dlit = "4"

    def run83(self):
        self.oct = "3"

    def run84(self):
        self.oct = "4"

    def run85(self):
        self.oct = "5"

    def run86(self):
        self.oct = "6"

    def runZ(self):
        self.run("C")

    def runX(self):
        self.run("D")

    def runC(self):
        self.run("E")

    def runV(self):
        self.run("F")

    def runB(self):
        self.run("G")

    def runN(self):
        self.run("A")

    def runM(self):
        self.run("H")

    def runS(self):
        self.run("J")

    def runD(self):
        self.run("K")

    def runG(self):
        self.run("L")

    def runH(self):
        self.run("M")

    def runJ(self):
        self.run("N")

    def runP(self):
        self.run("P")

app = QApplication(sys.argv)  # открываем главное окно
ex = MyWidget()
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1, rate=44100, output=1)
ex.show()
sys.exit(app.exec_())
