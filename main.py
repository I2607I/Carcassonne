import sys
import os
import copy
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QLabel, QVBoxLayout, QStackedLayout
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIcon, QCursor, QPainter, QFont, QPolygonF, QTransform
from PyQt6 import QtCore
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import Qt
from random import choice

N = 7
M = 11

class Feature():

    turn = 0
    image = 0

    def __init__(self, left=0, up=0, right=0, down=0):
        self.left = left
        self.up = up
        self.right = right
        self.down = down

    def printf(self):
        print(self.left, self.up, self.right, self.down, self.turn)
    
    def turnl(self):
        self.turn +=1
        if self.turn == 4:
            self.turn = 0

    def get(self):
        pass

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        # self.setFixedWidth(1500)
        # self.setFixedHeight(750)

        self.feature = False
        self.cur = QCursor()
        self.first_feature_river = [1]
        self.list_features_river = [2, 3, 4, 5, 6, 7, 8, 8, 9, 10]
        self.last_feature_river = [1]
        self.list_features = [11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 18, 18, 19, 19, 19, 20, 20, 21, 22, 23, 23, 23, 23, 24, 24, 24, 25, 26, 26, 27, 27, 27, 28, 28, 28, 29, 30, 31, 31, 32, 33, 34, 35, 35, 35, 35]
        self.index = -1
        self.list_features_on_map = []
        self.first_feature = True
        self.features_config = {
            1: Feature(0, 0, 0, 'river'),
            2: Feature('river', 'river', 'road', 'road'),
            3: Feature('road', 'river', 'road', 'river'),
            4: Feature('river', 'river', 'city', 'city'),
            5: Feature('city', 'river', 'city', 'river'),
            6: Feature('road', 'river', 'city', 'river'),
            7: Feature('road', 'river', 0, 'river'),
            8: Feature(0, 'river', 0, 'river'),
            9: Feature(0, 0, 'river', 'river'),
            10: Feature('river', 'river', 0, 0),
            11: Feature(0, 'road', 0, 'road'),
            12: Feature(0, 0, 'road', 'road'),
            13: Feature('road', 0, 'road', 'road'),
            14: Feature('road', 'road', 'road', 'road'),
            15: Feature('city', 'road', 'city', 'city'),
            16: Feature('city', 'road', 'road', 0),
            17: Feature('city', 0, 'road', 'road'),
            18: Feature('road', 'road', 'city', 'city'),
            19: Feature('city', 'road', 'road', 'road'),
            20: Feature(0, 0, 'road', 0),
            21: Feature('road', 'road', 0, 0),
            22: Feature('road', 0, 'road', 0),
            23: Feature(0, 0, 'city', 0),
            24: Feature(0, 0, 'city', 'city'),
            25: Feature('city', 0, 0, 'city'),
            26: Feature('city', 0, 'city', 0),
            27: Feature('city', 0, 'city', 0),
            28: Feature('city', 0, 'city', 'city'),
            29: Feature('city', 'city', 'city', 'city'),
            30: Feature('city', 0, 0, 0),
            31: Feature(0, 0, 'city', 'city'),
            32: Feature('city', 0, 0, 'city'),
            33: Feature('city', 0, 'city', 0),
            34: Feature('city', 0, 'city', 'city'),
            35: Feature(0, 0, 0 ,0),
        }

        layout = QGridLayout()
        layout_left = QGridLayout()
        layout_right = QGridLayout()
        layout_up = QGridLayout()
        layout_down = QGridLayout()
        layout_central = QHBoxLayout()
        layout_central.addLayout(layout_left)
        layout_central.addLayout(layout)
        layout_central.addLayout(layout_right)
        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_up)
        layout_main.addLayout(layout_central)
        layout_main.addLayout(layout_down)
        for i in range(N):
            button = QPushButton()
            button.setStyleSheet("QPushButton {background-color: rgb(32,154,22); color: White; border-radius: 600px;}")
            button.setMinimumSize(QtCore.QSize(100, 100))
            button.setMaximumSize(QtCore.QSize(100, 100))
            layout_left.addWidget(button, i, 0)
        for i in range(N):
            button = QPushButton()
            button.setStyleSheet("QPushButton {background-color: rgb(32,154,22); color: White; border-radius: 600px;}")
            button.setMinimumSize(QtCore.QSize(100, 100))
            button.setMaximumSize(QtCore.QSize(100, 100))
            layout_right.addWidget(button, i, 0)
        for i in range(M+2):
            button = QPushButton()
            button.setStyleSheet("QPushButton {background-color: rgb(32,154,22); color: White; border-radius: 600px;}")
            button.setMinimumSize(QtCore.QSize(100, 100))
            button.setMaximumSize(QtCore.QSize(100, 100))
            layout_up.addWidget(button, 0, i)
        for i in range(M+2):
            button = QPushButton()
            button.setStyleSheet("QPushButton {background-color: rgb(32,154,22); color: White; border-radius: 600px;}")
            button.setMinimumSize(QtCore.QSize(100, 100))
            button.setMaximumSize(QtCore.QSize(100, 100))
            layout_down.addWidget(button, 0, i)
        
        self.buttons = [[0 for i in range(M)] for j in range(N)]
        self.map = [[0 for i in range(M+20)] for j in range(N+20)]
        self.shifti=9
        self.shiftj=9
        # print(self.map)
        for i in range(N):
            for j in range(M):
                self.buttons[i][j] = QPushButton()
                #self.buttons[i][j].setCheckable(True)
                self.buttons[i][j].setStyleSheet("QPushButton {background-color: rgb(37,60,32); color: White; border-radius: 600px;}")
                #self.buttons[i][j].clicked.connect(self.set_color_button)
                self.buttons[i][j].setMinimumSize(QtCore.QSize(100, 100))
                self.buttons[i][j].setMaximumSize(QtCore.QSize(100, 100))
                # self.buttons[i][j].clicked.connect(lambda: self.click_button(i, j))
                # a.append(self.buttons[i][j])
                layout.addWidget(self.buttons[i][j], i, j)
        ggg = QPixmap(f'images/logo.png')

        button = layout_up.itemAt(0).widget()
        button.setIcon(QIcon(f'images/logo.png'))
        button.setIconSize(QtCore.QSize(100, 100))
        button.setObjectName('logo')
        button.clicked.connect(self.click_button)

        button = layout_up.itemAt(M+1).widget()
        button.setIcon(QIcon(f'images/turn.png'))
        button.setIconSize(QtCore.QSize(100, 100))
        button.setObjectName('turn')
        button.clicked.connect(self.click_button)

        button = layout_up.itemAt((M+2)//2).widget()
        button.setIcon(QIcon(f'images/up.png'))
        button.setIconSize(QtCore.QSize(100, 100))
        button.setObjectName('up')
        button.clicked.connect(self.click_button)

        button = layout_down.itemAt((M+2)//2).widget()
        button.setIcon(QIcon(f'images/down.png'))
        button.setIconSize(QtCore.QSize(100, 100))
        button.setObjectName('down')
        button.clicked.connect(self.click_button)

        button = layout_left.itemAt(N//2).widget()
        button.setIcon(QIcon(f'images/left.png'))
        button.setIconSize(QtCore.QSize(100, 100))
        button.setObjectName('left')
        button.clicked.connect(self.click_button)

        button = layout_right.itemAt(N//2).widget()
        button.setIcon(QIcon(f'images/right.png'))
        button.setIconSize(QtCore.QSize(100, 100))
        button.setObjectName('right')
        button.clicked.connect(self.click_button)


        for i, item in enumerate(self.buttons):
            for j, button in enumerate(item):
                button.clicked.connect(lambda i, j = [i, j]: self.click_button(i, j))   # передаю i и j

        layout.setSpacing(0)
        layout_left.setSpacing(0)
        layout_right.setSpacing(0)
        layout_up.setSpacing(0)
        layout_down.setSpacing(0)
        layout_central.setSpacing(0)
        layout_main.setSpacing(0)

        main_widget = QWidget()
        main_widget.setLayout(layout_main)

        # menu = QLabel()
        # menu.setPixmap(QPixmap("images/castle1.jpg").scaled((M+2)*100, (N+2)*100))
        # menu.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        menu2 = QVBoxLayout()
        menu2_widget = QWidget()
        menu2_widget.setLayout(menu2)
        menu2_widget.setStyleSheet("border-image: url(images/castle1.jpg);")
        up_b = QPushButton()
        up_b.setMinimumSize(QtCore.QSize((M+2)*100, int((N+2)*100*0.6)))
        up_b.setMaximumSize(QtCore.QSize((M+2)*100, int((N+2)*100*0.6)))
        up_b.setStyleSheet("QPushButton {background-color: rgb(32,154,22); border-image: url(image/s); color: White; border-radius: 600px;}")
        middle_b = QWidget()
        middle_layout = QHBoxLayout()

        left_b = QPushButton()
        left_b.setMinimumSize(QtCore.QSize(int((M+2)*100*0.1), int((N+2)*100*0.1)))
        left_b.setMaximumSize(QtCore.QSize(int((M+2)*100*0.1), int((N+2)*100*0.1)))
        left_b.setStyleSheet("QPushButton {background-color: rgb(32,154,22); border-image: url(image/s); color: White; border-radius: 600px;}")
        main_b = QPushButton()
        main_b.setMinimumSize(QtCore.QSize(int((M+2)*100*0.2), int((N+2)*100*0.1)))
        main_b.setMaximumSize(QtCore.QSize(int((M+2)*100*0.2), int((N+2)*100*0.1)))
        right_b = QPushButton()
        right_b.setMinimumSize(QtCore.QSize(int((M+2)*100*0.7), int((N+2)*100*0.1)))
        right_b.setMaximumSize(QtCore.QSize(int((M+2)*100*0.7), int((N+2)*100*0.1)))
        right_b.setStyleSheet("QPushButton {background-color: rgb(32,154,22); border-image: url(image/s); color: White; border-radius: 600px;}")

        middle_layout.addWidget(left_b)
        middle_layout.addWidget(main_b)
        middle_layout.addWidget(right_b)
        middle_layout.setSpacing(0)

        middle_b.setLayout(middle_layout)
        middle_b.setStyleSheet(" border-image: url(image/s); color: White; border-radius: 600px;")

        down_b = QPushButton()
        down_b.setMinimumSize(QtCore.QSize((M+2)*100, int((N+2)*100*0.3)))
        down_b.setMaximumSize(QtCore.QSize((M+2)*100, int((N+2)*100*0.3)))
        down_b.setStyleSheet("QPushButton {background-color: rgb(32,154,22); border-image: url(image/s); color: White; border-radius: 600px;}")


        menu2.addWidget(up_b)
        menu2.addWidget(middle_b)
        menu2.addWidget(down_b)
        menu2.setSpacing(0)
        
        stack_layout = QStackedLayout()
        stack_layout.addWidget(main_widget)
        stack_layout.addWidget(menu2_widget)
        stack_layout.setCurrentIndex(1)

        widget = QWidget()
        widget.setLayout(stack_layout)
        self.setCentralWidget(widget)


        #sounds
        self.sound_set = QSoundEffect()
        self.sound_set.setSource(QtCore.QUrl.fromLocalFile('sounds/set.wav'))
        self.sound_fail = QSoundEffect()
        self.sound_fail.setSource(QtCore.QUrl.fromLocalFile('sounds/fail.wav'))


    def click_button(self, i, j=(0,0)):
        # print('i', i)
        # print('j', j)
        i, j = j
        button = self.sender()
        if button.objectName() == 'logo' and self.feature == False:
            print('logo')
            if len(self.first_feature_river) > 0:
                self.index = choice(self.first_feature_river)
                self.first_feature_river.remove(self.index)
            elif len(self.list_features_river) > 0:
                self.index = choice(self.list_features_river)
                self.list_features_river.remove(self.index)
            elif len(self.last_feature_river) > 0:
                self.index = choice(self.last_feature_river)
                self.last_feature_river.remove(self.index)
            else:
                self.index = choice(self.list_features)
                self.list_features.remove(self.index)
            self.object = copy.deepcopy(self.features_config[self.index])
            self.object.image = f'images/{self.index}.png'
            self.cur = QCursor(QPixmap(self.object.image))
            QApplication.setOverrideCursor(self.cur)
            self.feature = True

        elif button.objectName() == 'up':
            self.shifti +=1
            for ii in range(N):
                for jj in range(M):
                    if self.map[ii+self.shifti][jj+self.shiftj]!=0:
                        t = QTransform().rotate(90*self.map[ii+self.shifti][jj+self.shiftj].turn)
                        pix = QPixmap(self.map[ii+self.shifti][jj+self.shiftj].image).transformed(t)
                        self.buttons[ii][jj].setIcon(QIcon(pix))
                        self.buttons[ii][jj].setIconSize(QtCore.QSize(100, 100))
                    else:
                        self.buttons[ii][jj].setIcon(QIcon())
        elif button.objectName() == 'down':
            self.shifti -=1
            for ii in range(N):
                for jj in range(M):
                    if self.map[ii+self.shifti][jj+self.shiftj]!=0:
                        t = QTransform().rotate(90*self.map[ii+self.shifti][jj+self.shiftj].turn)
                        pix = QPixmap(self.map[ii+self.shifti][jj+self.shiftj].image).transformed(t)
                        self.buttons[ii][jj].setIcon(QIcon(pix))
                        self.buttons[ii][jj].setIconSize(QtCore.QSize(100, 100))
                    else:
                        self.buttons[ii][jj].setIcon(QIcon())
        elif button.objectName() == 'left':
            self.shiftj +=1
            for ii in range(N):
                for jj in range(M):
                    if self.map[ii+self.shifti][jj+self.shiftj]!=0:
                        t = QTransform().rotate(90*self.map[ii+self.shifti][jj+self.shiftj].turn)
                        pix = QPixmap(self.map[ii+self.shifti][jj+self.shiftj].image).transformed(t)
                        self.buttons[ii][jj].setIcon(QIcon(pix))
                        self.buttons[ii][jj].setIconSize(QtCore.QSize(100, 100))
                    else:
                        self.buttons[ii][jj].setIcon(QIcon())
        elif button.objectName() == 'right':
            self.shiftj -=1
            for ii in range(N):
                for jj in range(M):
                    if self.map[ii+self.shifti][jj+self.shiftj]!=0:
                        t = QTransform().rotate(90*self.map[ii+self.shifti][jj+self.shiftj].turn)
                        pix = QPixmap(self.map[ii+self.shifti][jj+self.shiftj].image).transformed(t)
                        self.buttons[ii][jj].setIcon(QIcon(pix))
                        self.buttons[ii][jj].setIconSize(QtCore.QSize(100, 100))
                    else:
                        self.buttons[ii][jj].setIcon(QIcon())      
        elif button.objectName() == 'turn' and self.feature == True:
            self.object.turnl()
            t = QTransform().rotate(90*self.object.turn)
            pix = QPixmap(self.object.image).transformed(t)
            self.cur = QCursor(pix)
            QApplication.restoreOverrideCursor()
            QApplication.setOverrideCursor(self.cur)
            print('first',self.object.left, self.object.up, self.object.right, self.object.down)
            print([self.object.left, self.object.up, self.object.right, self.object.down][3:]+
                [self.object.left, self.object.up, self.object.right, self.object.down][:3])
            new_lurd = ([self.object.left, self.object.up, self.object.right, self.object.down][3:]+
                [self.object.left, self.object.up, self.object.right, self.object.down][:3])
            self.object.left, self.object.up, self.object.right, self.object.down = new_lurd[0], new_lurd[1], new_lurd[2], new_lurd[3]
        elif button.objectName() == '' and self.feature == True and (i+self.shifti, j+self.shiftj) not in self.list_features_on_map:
            print('f', button.objectName())
            print('not logo')
            i+=self.shifti
            j+=self.shiftj
            print(i, j)
            flag = True
            print('!!!!!!!!!!!!!!!!',self.object.left, self.object.up, self.object.right, self.object.down)
            if self.map[i][j+1] != 0 or self.map[i][j-1] != 0 or self.map[i - 1][j] != 0 or self.map[i + 1][j] != 0 or self.first_feature == True:
                print('check')
                # self.object.printf()
                if self.map[i][j+1] !=0:
                    print('left', self.map[i][j+1].left)
                    if self.map[i][j+1].left != self.object.right:
                        flag = False
                if self.map[i][j-1] !=0:
                    print('right',self.map[i][j-1].right)
                    if self.map[i][j-1].right != self.object.left:
                        flag = False
                if self.map[i+1][j] !=0:
                    print('up',self.map[i+1][j].up)
                    if self.map[i+1][j].up != self.object.down:
                        flag = False
                if self.map[i-1][j] !=0:
                    print('down', self.map[i-1][j].down)
                    if self.map[i-1][j].down != self.object.up:
                        flag = False
                count_river = 0
                if self.first_feature == False:
                    if self.object.left == 'river':
                        if self.map[i][j-1] == 0:
                            count_river +=1
                        elif self.map[i][j-1].right != 'river':
                            count_river +=1
                    if self.object.right == 'river':
                        if self.map[i][j+1] == 0:
                            count_river +=1
                        elif self.map[i][j+1].left != 'river':
                            count_river +=1
                    if self.object.up == 'river':
                        if self.map[i-1][j] == 0:
                            count_river +=1
                        elif self.map[i-1][j].down != 'river':
                            count_river +=1  
                    if self.object.down == 'river':
                        print(123)
                        if self.map[i+1][j] == 0:
                            count_river +=1
                        elif self.map[i+1][j].up != 'river':
                            count_river +=1
                if count_river > 1:
                    flag = False
                if flag == True:
                    t = QTransform().rotate(90*self.object.turn)
                    pix = QPixmap(self.object.image).transformed(t)
                    button.setIcon(QIcon(pix))
                    button.setIconSize(QtCore.QSize(100, 100))
                    self.sound_set.play()
                    QApplication.restoreOverrideCursor()
                    # self.map[i][j] = button
                    self.list_features_on_map.append((i, j))
                    self.map[i][j] = self.object
                    self.feature = False
                    self.first_feature = False
                else:
                    self.sound_fail.play()
            else:
                self.sound_fail.play()







    def paintEvent(self, paintEvent):
        paint = QPainter(self)
        sky_image = QPixmap(f'images/sky.png').scaled(1750, 225)
        paint.drawPixmap(self.rect(), sky_image)










app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

a = Feature(0, 'road', 0, 'road')
b = copy.deepcopy(a)
b.turnl()


a.printf()
b.printf()