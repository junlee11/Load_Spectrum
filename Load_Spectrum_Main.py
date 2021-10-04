#210922 Project 시작

import sys, os, re, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pandas as pd
import ftplib
import tkinter
from tkinter import ttk
from tkinter import messagebox
import shutil
import keyboard
import pyautogui
from dateutil import parser
from time import sleep


#hot key 알아내기
# while True:
#     print(keyboard.read_key())

c_flag = {'c_is_inf' : 0, 'c_access' : 0, 'back' : 0}
e_flag = {'e_is_path' : 0, 'e_path5' : 0, 'back' : 0, 'e_find' : 0, 'overwrite' : {}, 'folder_overwrite' : 0,
          'ask_cnt' : 0, 'all_overwrite' : 0, 'ext' : {}, 'overwrite_u' : {}, 'folder_overwrite_u' : {}}
ftp_dic = {'e_line' : '', 'c_line' : '', 'item_list' : [], 'ext_list' : [], 'item_list_up' : []}

form_class = uic.loadUiType("Load_Main_EQP_Local.ui")[0]
#form_class = uic.loadUiType("Load_Main_Local_EQP.ui")[0]

#class WindowClass(QMainWindow, form_class) :
class WindowClass(QMainWindow):

    def __init__(self) :
        super().__init__()
        global c_flag
        global e_flag
        global ftp
        global ftp_dic
        self.setupUi(self)
        self.c_fow_list = []
        self.e_fow_list = []
        self.list_e_ip1 = ''
        self.list_e_ip2 = ''
        self.list_e_ip3 = ''
        self.list_e_ip4 = ''
        self.list_e_ip5 = ''
        self.e_path5_str = ''
        ftp = None

        #Local
        self.list_c_drive.addItem('C:')
        self.list_c_drive.addItem('D:')
        self.list_c_drive.addItem('E:')
        self.list_c_drive.itemClicked.connect(self.c_drive_clk)
        self.list_c_path.itemDoubleClicked.connect(self.c_path_dbclk)
        self.push_c_back.clicked.connect(self.c_push_back_clk)
        self.push_c_foward.clicked.connect(self.c_push_fow_clk)
        self.push_c_new.clicked.connect(self.c_push_new_clk)
        self.push_c_del.clicked.connect(self.c_push_del_clk)

        ######################################################################
        #########################hokey setting################################
        self.shortcut_open = QShortcut(QKeySequence('backspace'), self)        #단축키 설정
        self.shortcut_open.activated.connect(self.c_push_back_clk)
        self.shortcut_open = QShortcut(QKeySequence('delete'), self)
        self.shortcut_open.activated.connect(self.c_push_del_clk)
        self.shortcut_open = QShortcut(QKeySequence('n'), self)
        self.shortcut_open.activated.connect(self.c_push_new_clk)
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+n'), self)
        self.shortcut_open.activated.connect(self.e_push_new_clk)
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+d'), self)
        self.shortcut_open.activated.connect(self.e_push_del_clk)


##############################################이하 EQP#############################################
        #EQP - ftp 시작

        #Line
        self.df_eqp_info = pd.read_csv('ip_info.txt')           #eqp 소스
        self.lineID= set(self.df_eqp_info['Line'])
        self.lineID = list(self.lineID)
        self.lineID.sort()
        for i in self.lineID:
            self.list_e_line.addItem(i)

        #id_EQP
        self.list_e_line.itemClicked.connect(self.e_mk_eqp)
        self.list_e_eqp.itemClicked.connect(self.e_mk_drive)

        #ext
        self.df_ext = pd.read_csv('ext_info.txt')
        self.extID = set(self.df_ext['ext'])
        self.extID = list(self.extID)
        self.extID.sort()
        for i in self.extID:
            self.list_e_ext.addItem(i)

        self.e_path_list = [self.list_e_path1, self.list_e_path2, self.list_e_path3, self.list_e_path4, self.list_e_path5]
        self.e_path_ip = [self.list_e_ip1, self.list_e_ip2, self.list_e_ip3, self.list_e_ip4, self.list_e_ip5]

        #EQP ftp 파일,복사 리스트 생성 / ftp는 클릭해서 드래그해야 하므로 더블클릭 이벤트로 작성
        self.list_e_eqp.itemClicked.connect(self.e_mk_drive)
        self.list_e_drive.itemClicked.connect(self.e_mk_path1)

        self.list_e_path1.itemDoubleClicked.connect(self.e_mk_path2)
        self.list_e_path2.itemDoubleClicked.connect(self.e_mk_path3)
        self.list_e_path3.itemDoubleClicked.connect(self.e_mk_path4)
        self.list_e_path4.itemDoubleClicked.connect(self.e_mk_path5)
        self.list_e_path5.itemDoubleClicked.connect(self.e_path5_dbclk)

        self.push_e_back.clicked.connect(self.e_push_back_clk)
        self.push_e_foward.clicked.connect(self.e_push_fow_clk)
        self.push_e_new.clicked.connect(self.e_push_new_clk)
        self.push_e_del.clicked.connect(self.e_push_del_clk)

        ########FTP 다운 관련
        self.line_e_cur_path.textChanged.connect(self.e_address)
        self.line_c_cur_path.textChanged.connect(self.c_address)
        self.list_e_ext.itemSelectionChanged.connect(self.mk_ext_list)
        #self.list_e_ext.currentItemChanged.connect(self.mk_ext_list)

        ########보조 push button
        self.push_eqp_info.clicked.connect(self.e_push_open_eqp)
        self.push_ext_info.clicked.connect(self.e_push_open_ext)
        self.push_manual.clicked.connect(self.e_push_open_manual)
        self.push_hotkey.clicked.connect(self.e_push_open_hotkey)
############################################################
##########################ftp 다운 보조 함수##################
    def e_address(self):
        global ftp_dic
        ftp_dic['e_line'] = self.line_e_cur_path.text()

    def c_address(self):
        global ftp_dic
        ftp_dic['c_line'] = self.line_c_cur_path.text()

    def mk_ext_list(self):
        global ftp_dic
        ftp_dic['ext_list'] = [item.text() for item in self.list_e_ext.selectedItems()]
############################################################
############################################################

    #EQP 파일 열기
    def e_push_open_eqp(self):
        os.startfile('ip_info.txt')

    #확장자 파일 열기
    def e_push_open_ext(self):
        os.startfile('ext_info.txt')

    #매뉴얼 파일 열기
    def e_push_open_manual(self):
        os.startfile('manual.xlsx')

    #단축키 파일 열기
    def e_push_open_hotkey(self):
        os.startfile('hotkey_list.txt')

    #EQP List 만들기
    def e_mk_eqp(self):
        e_flag['e_path5'] = 0
        for i in self.e_path_list:
            i.clear()
        self.line_e_cur_path.clear()

        self.df_result = None
        self.list_e_eqp.clear()
        self.list_e_drive.clear()
        self.df_eqp = self.df_eqp_info[self.df_eqp_info['Line'] == self.list_e_line.currentItem().text()]
        self.df_result = self.df_eqp
        self.eqpID = set(self.df_eqp['EQP'])
        self.eqpID = list(self.eqpID)
        self.eqpID.sort()
        for i in self.eqpID:
            self.list_e_eqp.addItem(i)

    #EQP 드라이브 List 만들기
    def e_mk_drive(self):
        e_flag['e_path5'] = 0
        for i in self.e_path_list:
            i.clear()
        self.line_e_cur_path.clear()

        self.list_e_drive.clear()
        self.list_e_drive.addItem('D:')
        self.list_e_drive.addItem('E:')
        self.list_e_drive.addItem('C:')

    #본격적으로 eqp path 만들기
    def e_mk_path1(self):
        global ftp
        e_flag['e_find'] = 0
        ftp_id = ''
        ftp_pw = ''
        e_flag['e_path5'] = 0
        for i in self.e_path_list:
            i.clear()
        self.line_e_cur_path.clear()

        self.df_index = self.df_result.index[self.df_result['EQP'] == self.list_e_eqp.currentItem().text()].tolist()        #데이터프레임 조건에 맞는 인덱스 찾기
        self.ftp_ip = self.df_result['IP'][self.df_index[0]]
        self.ftp_drive = self.list_e_drive.currentItem().text()
        if self.ftp_drive[0] == 'D':
            ftp_id = 'LS_D'
            ftp_pw = 'LS_D'
        if self.ftp_drive[0] == 'E':
            ftp_id = 'LS_E'
            ftp_pw = 'LS_E'
        if self.ftp_drive[0] == 'C':
            ftp_id = 'LS_C'
            ftp_pw = 'LS_C'

        ftp = ftplib.FTP()
        try:
            ftp.connect(self.ftp_ip, 21)
        except:
            QMessageBox.warning(self, 'IP Interlock', '접속할 수 없습니다. / IP 주소 및 접속 상태 확인')
            return

        try:
            ftp.login(ftp_id, ftp_pw)
        except ftplib.error_perm:
            QMessageBox.warning(self, 'FTP Login Interlock', 'FTP 계정정보가 올바르지 않습니다')
            return

        #self.ftp.cwd('/test/')
        #self.ftp.cwd('/test/a/')
        #self.ftp.cwd('/test/')

        self.line_e_cur_path.setText('ftp://' + self.ftp_ip + '/' + self.list_e_drive.currentItem().text()[:-1] + ftp.pwd())
        arr_e_path, arr_e_path_mlsd = self.e_arr(self.line_e_cur_path.text()[self.line_e_cur_path.text().rfind('/') : ])
        self.e_list_to_target(arr_e_path, arr_e_path_mlsd, 0)
        self.ftp_ip_idx = len(self.line_e_cur_path.text())
        self.e_path_ip[0] = self.line_e_cur_path.text()[self.ftp_ip_idx - 1:]

    def e_mk_path2(self):
        e_flag['e_find'] = 1
        self.e_mk_path_all(1)

    def e_mk_path3(self):
        e_flag['e_find'] = 2
        self.e_mk_path_all(2)

    def e_mk_path4(self):
        e_flag['e_find'] = 3
        self.e_mk_path_all(3)

    def e_mk_path5(self):
        e_flag['e_find'] = 4
        self.e_mk_path_all(4)

    def e_mk_path_all(self, k):
        global ftp
        e_flag['e_path5'] = 0
        for i in range(k, len(self.e_path_list)):
            self.e_path_list[i].clear()
        self.e_path_ip[k] = self.e_path_ip[k - 1] + self.e_path_list[k - 1].currentItem().text() + '/'
        try:
            arr_e_path, arr_e_path_mlsd = self.e_arr(self.e_path_ip[k])
        except:
            arr_e_path = ''
            arr_e_path_mlsd = ''
            if e_flag['e_is_path'] == 1:
                t_path = self.line_e_cur_path.text()[:self.ftp_ip_idx-1] + self.e_path_ip[k]
                self.line_e_cur_path.setText(t_path[:t_path[:-1].rfind('/')] + '/')
                return
        temp = self.line_e_cur_path.text()[:self.ftp_ip_idx-1] + self.e_path_ip[k]
        self.line_e_cur_path.clear()
        self.line_e_cur_path.setText(temp)
        self.e_list_to_target(arr_e_path, arr_e_path_mlsd, k)

    def e_arr(self, f_path):
        global ftp
        e_flag['e_is_path'] = 0
        f_path_list = []
        f_exe_list = []
        #ftp 경로 지정
        try:
            ftp.cwd(f_path)
        except ftplib.error_perm:
            QMessageBox.warning(self, 'Path Interlock', '다음 경로를 보려면 폴더를 선택하세요.')
            e_flag['e_is_path'] = 1
            return

        try:
            f_path_list_mlsd = [f for f in list(ftp.mlsd()) if not (f[0].startswith('.') or (f[0].startswith('$')))]
            for f in f_path_list_mlsd:
                f_path_list.append(f[0])
                if f[1]['type'] == 'dir' : f_exe_list.append('')
                else : f_exe_list.append(f[0][f[0].rfind('.'):len(f[0])])

        except:
            QMessageBox.warning(self, 'Access Interlock', '경로에 오류가 있습니다.')
            return

        f_exe_set = set(f_exe_list)
        f_exe_list = list(f_exe_set)
        f_exe_list.sort()

        f_arr_dic = {}
        for i in range(len(f_exe_list)):
            f_arr_dic[f_exe_list[i]] = []

        #확장자별로 구분
        for i in range(len(f_path_list_mlsd)):

            if f_path_list_mlsd[i][1]['type'] == 'dir':
                ext = ''
                f_arr_dic[ext].append(f_path_list[i])
            else:
                ext = f_path_list_mlsd[i][0][f_path_list_mlsd[i][0].rfind('.'):len(f_path_list_mlsd[i][0])]
                f_arr_dic[ext].append(f_path_list[i])

        # 확장자 각각을 정렬
        for i in f_exe_list:
            f_arr_dic[i].sort()
            f_arr_dic[i] = sorted(f_arr_dic[i], key=self.replace_special)

        # 전체 리스트 반환
        f_result_list = []
        for i in f_exe_list:
            f_result_list += f_arr_dic[i]

        return f_result_list, f_path_list_mlsd


    def e_list_to_target(self, f_path, f_path_mlsd, n):
        global ftp

        for i in f_path:

            if self.ftp_isdir(i, f_path_mlsd) : icon = QIcon('Icon_folder.png')
            elif 'xls' in i[-6:] : icon = QIcon('Icon_excel.png')
            elif 'txt' in i[-6:] : icon = QIcon('Icon_text.png')
            elif 'py' in i[-6:] : icon = QIcon('Icon_python.png')
            elif 'ppt' in i[-6:] : icon = QIcon('Icon_ppt.png')
            else : icon = QIcon('Icon_apeach.png')
            #else : icon = QIcon('Icon_lion.png')

            icon_item = QListWidgetItem(icon, i)
            self.e_path_list[n].addItem(icon_item)

    
    #ftp폴더 내 파일의 타입 반환
    def ftp_isdir(self, s, f_mlsd):
        global ftp
        for i in f_mlsd:
            if s == i[0] : return 'dir' == i[1]['type']

    #path5 더블클릭용 ftp에서 1개의 경로만 받아 폴더 유무 판단
    def ftp_isdir2(self,s):
        global ftp
        t_flag = 0
        origin_ip = self.line_e_cur_path.text()[self.ftp_ip_idx-1:]
        #chg_ip = origin_ip + s
        ftp_mlsd = list(ftp.mlsd())
        for f in ftp_mlsd:
            #파일명과 확장자 모두 일치해야 함
            if s == f[0] and f[1]['type'] == 'dir' :
                t_flag = 1
            else :
                pass
        if t_flag == 1 : return True
        else : return False

    #path5 더블클릭 제어 self.e_path5_dbclk
    def e_path5_dbclk(self):
        self.e_path5_str = ''
        global ftp
        e_flag['e_path5'] += 1
        if e_flag['e_path5'] == 1 : self.e_path5_idx = len(self.line_e_cur_path.text())
        #파일 열기 불가, 폴더 경로만 제어
        if self.ftp_isdir2(self.list_e_path5.currentItem().text()) :
            self.e_path5_str = self.e_path5_str + self.list_e_path5.currentItem().text() + '/'
            path = self.line_e_cur_path.text()[self.ftp_ip_idx - 1:] + self.list_e_path5.currentItem().text()
            arr_e_path, arr_e_path_mlsd = self.e_arr(path)
            self.e_path_list[4].clear()
            self.e_list_to_target(arr_e_path, arr_e_path_mlsd, 4)
            self.line_e_cur_path.setText(self.line_e_cur_path.text()[:self.e_path5_idx] + self.e_path5_str)

        else:
            QMessageBox.warning(self, 'Path Interlock', '다음 경로를 보려면 폴더를 선택하세요.')
            pass

    def e_push_back_clk(self):
        global ftp
        if e_flag['e_path5'] == 0 : self.e_path5_idx = len(self.line_e_cur_path.text())
        t = self.line_e_cur_path.text()
        if self.list_e_path5.item(0) == None and e_flag['e_path5'] == 0:       #path5 사용 안할때는 눌러도 동작안함
            pass
        elif len(t) - len(t[t[:-1].rfind('/') + 1:len(t)]) < self.e_path5_idx :
            pass
        else:
            f_path = self.line_e_cur_path.text()[self.ftp_ip_idx - 1:]
            self.e_cur_path = f_path
            self.e_back_path = f_path[:f_path[:-1].rfind('/') + 1]

            arr_e_path, arr_e_path_mlsd = self.e_arr(self.e_back_path)
            self.e_path_list[4].clear()
            self.e_list_to_target(arr_e_path, arr_e_path_mlsd, 4)
            self.line_e_cur_path.setText(self.line_e_cur_path.text()[:self.ftp_ip_idx - 1] + self.e_back_path)

            self.e_fow_list.append(f_path)
            e_flag['back'] += 1

    def e_push_fow_clk(self):
        global ftp
        if e_flag['back'] != 0:
            arr_e_path, arr_e_path_mlsd = self.e_arr(self.e_fow_list[e_flag['back']-1])
            self.e_path_list[4].clear()
            self.e_list_to_target(arr_e_path, arr_e_path_mlsd, 4)
            self.line_e_cur_path.setText(self.line_e_cur_path.text()[:self.ftp_ip_idx - 1] + self.e_fow_list[e_flag['back']-1])
            e_flag['back'] += -1
            self.e_fow_list.pop()

    def e_push_new_clk(self):
        global ftp
        #현재 기본경로 선택했으면 tkinter 실행
        try:
            print(self.list_e_drive.currentItem().text())
            self.tk_mk()
        except AttributeError:
            QMessageBox.warning(self, 'Path Interlock', '기본 경로가 설정되지 않았습니다.')
            return
        f_path = self.line_e_cur_path.text()[self.ftp_ip_idx -1 :] + self.new_folder + '/'
        if self.new_folder == '' : return
        
        #폴더 생성
        try:
            ftp.mkd(f_path)
            icon = QIcon('Icon_folder.png')
            icon_item = QListWidgetItem(icon, self.new_folder)
            self.e_path_list[e_flag['e_find']].addItem(icon_item)

        except ftplib.error_perm:
            QMessageBox.warning(self, 'Path Interlock', '이미 존재하는 폴더입니다.')
            return

    def e_push_del_clk(self):
        global ftp
        if e_flag['e_find'] == 0 : return

        try:
            print(self.e_path_list[e_flag['e_find']].currentItem().text())

            a = [i.text() for i in self.e_path_list[e_flag['e_find']].selectedItems()]
            b = [i for i in self.e_path_list[e_flag['e_find']].selectedItems()]
        except AttributeError:
            QMessageBox.warning(self, 'Path Interlock', '삭제하려는 대상의 경로가 있는 리스트에서 선택하세요.')
            return

        for i in range(len(a)):
            if i == 0 : str = a[i]
            else : str = str + '\n' + a[i]

        reply = QMessageBox.question(self, '삭제 경고', '정말로 선택한 파일(폴더)를 삭제 하시겠습니까?\n' + str, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for i in range(len(a)):
                f_name = self.line_e_cur_path.text()[self.ftp_ip_idx - 1:] + a[i]
                #f_name = self.line_e_cur_path.text()[self.ftp_ip_idx - 1:] + self.e_path_list[e_flag['e_find']].currentItem().text()
                self.remove_ftp_dir(f_name)
                self.e_path_list[e_flag['e_find']].takeItem(self.e_path_list[e_flag['e_find']].currentRow())
        else:
            pass

    #ftp 경로 내 파일, 폴더 삭제
    def remove_ftp_dir(self, c_path):
        global ftp
        for (name, properties) in ftp.mlsd(path = c_path):
            if name in ['.', '..']:
                continue
            elif properties['type'] == 'file':
                try:
                    print(f"{c_path}/{name}")
                    ftp.delete(f"{c_path}/{name}")
                except ftplib.error_perm:
                    ftp.delete(c_path)
                    return
            elif properties['type'] == 'dir':
                self.remove_ftp_dir(f"{c_path}/{name}")
        ftp.rmd(c_path)


###############################################################################
#####################################이하 Local#################################
###############################################################################
    #Local 드라이브 클릭시 작동, 리스트 표현
    def c_drive_clk(self):
        c_flag['c_is_inf'] = 0
        c_flag['c_fir'] = 1
        self.line_c_cur_path.setText(self.list_c_drive.currentItem().text())
        self.list_c_path.clear()
        self.arr_c_path_list = self.c_arr(self.line_c_cur_path.text() + '\\')  # 경로의 파일, 폴더 정렬하여 리스트로 반환

        if c_flag['c_is_inf'] == 0:
            self.c_list_to_target(self.arr_c_path_list)                                 #리스트 표시
        else:
            self.list_c_path.addItem('파일 없음')
    
    #Local에서 경로를 받아 아이콘과 함께 리스트로 표시
    def c_list_to_target(self, path_list):

        for i in path_list:
            path = self.line_c_cur_path.text() + '/' + i
            if os.path.isdir(path) : icon = QIcon('Icon_folder.png')
            elif 'xls' in os.path.splitext(path)[1] : icon = QIcon('Icon_excel.png')
            elif 'txt' in os.path.splitext(path)[1] : icon = QIcon('Icon_text.png')
            elif 'py' in os.path.splitext(path)[1] : icon = QIcon('Icon_python.png')
            elif 'ppt' in os.path.splitext(path)[1] : icon = QIcon('Icon_ppt.png')
            else : icon = QIcon('Icon_apeach.png')
            #else : icon = QIcon('Icon_lion.png')

            icon_item = QListWidgetItem(icon, i)
            self.list_c_path.addItem(icon_item)

    #특수문자 정렬용 함수
    def replace_special(self, s):
        # add more characters to regex, as required
        return re.sub('[★]', ' ', s)
    
    #Local 경로의 파일, 폴더를 확장자, 오름차순으로 정렬하여 리스트로 반환
    def c_arr(self, path):

        #path_list = os.listdir(path)
        try:
            path_list = [f for f in os.listdir(path) if not (f.startswith('.') or f.startswith('$'))]
            exe_list = []
        except FileNotFoundError:
            #QMessageBox.warning(self, 'Path Interlock', '경로가 존재하지 않습니다.')
            c_flag['c_is_inf'] = 1
            return
        except PermissionError:
            QMessageBox.warning(self, 'Access Interlock', '경로에 접근할 수 없습니다 : 엑세스 거부')
            c_flag['c_access'] = 1
            return

        #확장자 저장
        for i in path_list[:]:
            if os.path.isfile(path +'/' + i):
                name, ext = os.path.splitext(path + '/' + i)
                exe_list.append(ext)
            else:
                ext = ''
                exe_list.append(ext)

        #확장자 중복 제거
        exe_set = set(exe_list)
        exe_list = list(exe_set)
        exe_list.sort()

        arr_dic = {}
        for i in range(len(exe_list)):
            arr_dic[exe_list[i]] = []

        #확장자별로 구분
        for i in path_list[:]:
            if os.path.isfile(path + '/' + i):
                name, ext = os.path.splitext(path + '/' + i)
                arr_dic[ext].append(i)
            else:
                arr_dic[''].append(i)

        #확장자 각각을 정렬
        for i in exe_list:
            arr_dic[i].sort()
            arr_dic[i] = sorted(arr_dic[i], key = self.replace_special)

        #전체 리스트 반환
        result_list = []
        for i in exe_list:
            result_list += arr_dic[i]

        return result_list

    #Local 더블클릭시 파일은 열고 폴더는 다음 경로
    def c_path_dbclk(self):
        if self.line_c_cur_path.text()[-1] != '\\' : path = self.line_c_cur_path.text() + '\\' + self.list_c_path.currentItem().text()
        else : path = self.line_c_cur_path.text() + self.list_c_path.currentItem().text()
        self.c_mk_list(path)

    def c_mk_list(self, path):

        if os.path.isdir(path):
            c_flag['c_is_inf'] = 0
            c_flag['c_access'] = 0

            self.arr_c_path_list = self.c_arr(path)  # 경로의 파일, 폴더 정렬하여 리스트로 반환

            if c_flag['c_is_inf'] == 0 and c_flag['c_access'] == 0:
                self.line_c_cur_path.setText(path.rstrip('\\'))
                self.list_c_path.clear()
                self.c_list_to_target(self.arr_c_path_list)  # 리스트 표시
            elif c_flag['c_access'] == 1:
                return
            elif c_flag['c_is_inf'] == 1:
                self.line_c_cur_path.setText(path.rstrip('\\'))
                self.list_c_path.clear()
                self.list_c_path.addItem('파일 없음')
        elif not os.path.isdir(path):
            os.startfile(path)

    #Local back 버튼 클릭, 경로 뒤로 가게
    def c_push_back_clk(self):

        if len(self.line_c_cur_path.text()) == 2 or len(self.line_c_cur_path.text()) == 0 :
            pass
        else:
            path = self.line_c_cur_path.text()
            self.c_cur_path = path
            self.c_back_path = path[:path.rfind('\\') + 1]
            self.c_mk_list(self.c_back_path)
            self.c_fow_list.append(path)
            c_flag['back'] += 1

    #Local foward 버튼 클릭, 경로 앞으로 가게
    def c_push_fow_clk(self):
        if c_flag['back'] != 0:
            self.c_mk_list(self.c_fow_list[c_flag['back'] - 1])
            c_flag['back'] += -1
            self.c_fow_list.pop()

    #local push 새폴더 만들기
    def c_push_new_clk(self):
        try:
            print(self.list_c_drive.currentItem().text())
            self.tk_mk()
        except AttributeError:
            QMessageBox.warning(self, 'Path Interlock', '기본 경로가 설정되지 않았습니다.')
            return

        if self.new_folder =='' : return

        try:
            if not os.path.exists(self.line_c_cur_path.text() + '/' + self.new_folder):
                os.makedirs(self.line_c_cur_path.text() + '/' + self.new_folder)
                icon = QIcon('Icon_folder.png')
                icon_item = QListWidgetItem(icon, self.new_folder)
                self.list_c_path.addItem(icon_item)

        except OSError:
            QMessageBox.warning(self, 'Path Interlock', '해당 설비로 접근할 수 없습니다. / IP 확인 필요')
            return

    def tk_mk(self):
        #########################tkinter 새 창
        self.new_folder = ''
        self.window = tkinter.Tk()
        self.window.title('Local 새폴더 입력창')
        self.window.geometry('380x70')
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')
        self.window.bind('<Return>', self.tk_buttonClicked_event)
        self.window.bind('<Escape>', self.tk_quit_event)

        self.label = ttk.Label(self.window, text='새폴더 이름을 입력하세요')
        self.label.grid(column=0, row=0)
        self.button = ttk.Button(self.window, text="확인", command=self.tk_buttonClicked)
        self.button.grid(column=1, row=1)
        self.name = tkinter.StringVar()
        self.textbox = ttk.Entry(self.window, width=30, textvariable=self.name)
        self.textbox.grid(column=0, row=1, padx=(10, 10))
        self.textbox.focus()
        self.window.mainloop()
        ########################################


    def tk_buttonClicked(self):
        self.label.configure(foreground='blue')
        self.new_folder = self.name.get()
        self.tk_quit()

    def tk_buttonClicked_event(self, event):
        self.label.configure(foreground='blue')
        self.new_folder = self.name.get()
        self.tk_quit()

    def tk_quit(self):
        self.window.destroy()

    def tk_quit_event(self, event):
        self.window.destroy()
    ###########################################################위까지 새폴더

    #Local 경로 / 파일 삭제하기
    def c_push_del_clk(self):
        if self.line_c_cur_path.text() == '' : return

        try:
            a = [i.text() for i in self.list_c_path.selectedItems()]
            b = [i for i in self.list_c_path.selectedItems()]
        except AttributeError:
            QMessageBox.warning(self, 'Path Interlock', '삭제하려는 대상의 경로가 있는 리스트에서 선택하세요.')
            return

        for i in range(len(a)):
            if i == 0 : str = a[i]
            else : str = str + '\n' + a[i]

        reply = QMessageBox.question(self, '삭제 경고', '정말로 선택한 파일(폴더)를 삭제 하시겠습니까?\n' + str , QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for i in range(len(a)):
                try:
                    shutil.rmtree(self.line_c_cur_path.text() + '/' + a[i])
                    self.list_c_path.takeItem(self.list_c_path.currentRow())
                except NotADirectoryError as e:
                    os.remove(self.line_c_cur_path.text() + '/' + a[i])
                    self.list_c_path.takeItem(self.list_c_path.currentRow())
        else:
            pass

######################################################################################
##############################Form Code Start#########################################
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1252, 823)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_4.addWidget(self.label_10)
        self.line_e_cur_path = QtWidgets.QLineEdit(self.groupBox)
        self.line_e_cur_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line_e_cur_path.setObjectName("line_e_cur_path")
        self.verticalLayout_4.addWidget(self.line_e_cur_path)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setMaximumSize(QtCore.QSize(100, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.list_e_line = QtWidgets.QListWidget(self.groupBox)
        self.list_e_line.setMaximumSize(QtCore.QSize(100, 80))
        self.list_e_line.setObjectName("list_e_line")
        self.verticalLayout.addWidget(self.list_e_line)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setMaximumSize(QtCore.QSize(100, 20))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_12.addWidget(self.label_12)
        self.list_e_eqp = QtWidgets.QListWidget(self.groupBox)
        self.list_e_eqp.setMaximumSize(QtCore.QSize(100, 80))
        self.list_e_eqp.setObjectName("list_e_eqp")
        self.verticalLayout_12.addWidget(self.list_e_eqp)
        self.horizontalLayout.addLayout(self.verticalLayout_12)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setMaximumSize(QtCore.QSize(100, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.list_e_drive = QtWidgets.QListWidget(self.groupBox)
        self.list_e_drive.setMaximumSize(QtCore.QSize(100, 80))
        self.list_e_drive.setObjectName("list_e_drive")
        self.verticalLayout_2.addWidget(self.list_e_drive)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setMaximumSize(QtCore.QSize(100, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.list_e_ext = QtWidgets.QListWidget(self.groupBox)
        self.list_e_ext.setMaximumSize(QtCore.QSize(100, 80))
        self.list_e_ext.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_ext.setObjectName("list_e_ext")
        self.verticalLayout_3.addWidget(self.list_e_ext)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.push_eqp_info = QtWidgets.QPushButton(self.groupBox)
        self.push_eqp_info.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_eqp_info.setObjectName("push_eqp_info")
        self.verticalLayout_13.addWidget(self.push_eqp_info)
        self.push_ext_info = QtWidgets.QPushButton(self.groupBox)
        self.push_ext_info.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_ext_info.setObjectName("push_ext_info")
        self.verticalLayout_13.addWidget(self.push_ext_info)
        self.horizontalLayout.addLayout(self.verticalLayout_13)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.push_e_back = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_e_back.sizePolicy().hasHeightForWidth())
        self.push_e_back.setSizePolicy(sizePolicy)
        self.push_e_back.setMaximumSize(QtCore.QSize(40, 16777215))
        self.push_e_back.setObjectName("push_e_back")
        self.horizontalLayout_5.addWidget(self.push_e_back)
        self.push_e_foward = QtWidgets.QPushButton(self.groupBox)
        self.push_e_foward.setMaximumSize(QtCore.QSize(40, 16777215))
        self.push_e_foward.setObjectName("push_e_foward")
        self.horizontalLayout_5.addWidget(self.push_e_foward)
        self.push_e_new = QtWidgets.QPushButton(self.groupBox)
        self.push_e_new.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_e_new.setObjectName("push_e_new")
        self.horizontalLayout_5.addWidget(self.push_e_new)
        self.push_e_del = QtWidgets.QPushButton(self.groupBox)
        self.push_e_del.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_e_del.setObjectName("push_e_del")
        self.horizontalLayout_5.addWidget(self.push_e_del)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        #self.list_e_path5
        self.list_e_path5 = Lst_e_path5(self.groupBox)
        self.list_e_path5.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path5.setDragEnabled(True)
        self.list_e_path5.setDragDropOverwriteMode(False)
        self.list_e_path5.setDefaultDropAction(Qt.MoveAction)
        self.list_e_path5.setObjectName("list_e_path5")
        self.verticalLayout_9.addWidget(self.list_e_path5)

        self.gridLayout.addLayout(self.verticalLayout_9, 1, 3, 3, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)

        #list_e_path3
        self.list_e_path3 = Lst_e_path3(self.groupBox)
        self.list_e_path3.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path3.setDragEnabled(True)
        self.list_e_path3.setDragDropOverwriteMode(False)
        self.list_e_path3.setDefaultDropAction(Qt.MoveAction)
        self.list_e_path3.setObjectName("list_e_path3")
        self.verticalLayout_7.addWidget(self.list_e_path3)

        self.horizontalLayout_4.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)

        # list_e_path4
        self.list_e_path4 = Lst_e_path4(self.groupBox)
        self.list_e_path4.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path4.setDragEnabled(True)
        self.list_e_path4.setDragDropOverwriteMode(False)
        self.list_e_path4.setDefaultDropAction(Qt.MoveAction)
        self.list_e_path4.setObjectName("list_e_path4")
        self.verticalLayout_8.addWidget(self.list_e_path4)

        self.horizontalLayout_4.addLayout(self.verticalLayout_8)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)

        #list_e_path1
        self.list_e_path1 = Lst_e_path1(self.groupBox)
        self.list_e_path1.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path1.setDragEnabled(True)
        self.list_e_path1.setDragDropOverwriteMode(False)
        self.list_e_path1.setDefaultDropAction(Qt.MoveAction)
        self.list_e_path1.setObjectName("list_e_path1")
        self.verticalLayout_5.addWidget(self.list_e_path1)

        self.horizontalLayout_3.addLayout(self.verticalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)

        #list_e_path2
        self.list_e_path2 = Lst_e_path2(self.groupBox)
        self.list_e_path2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_e_path2.setDragEnabled(True)
        self.list_e_path2.setDragDropOverwriteMode(False)
        self.list_e_path2.setDefaultDropAction(Qt.MoveAction)
        self.list_e_path2.setObjectName("list_e_path2")
        self.verticalLayout_6.addWidget(self.list_e_path2)

        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.push_manual = QtWidgets.QPushButton(self.groupBox)
        self.push_manual.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_manual.setObjectName("push_manual")
        self.verticalLayout_14.addWidget(self.push_manual)
        self.push_hotkey = QtWidgets.QPushButton(self.groupBox)
        self.push_hotkey.setMaximumSize(QtCore.QSize(100, 16777215))
        self.push_hotkey.setObjectName("push_hotkey")
        self.verticalLayout_14.addWidget(self.push_hotkey)
        self.gridLayout.addLayout(self.verticalLayout_14, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 30)
        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 7)
        self.gridLayout.setRowStretch(3, 7)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")

        #self.list_c_path
        self.list_c_path = Lst_c_path(self.groupBox_2)
        #self.list_c_path = QtWidgets.QListWidget(self.groupBox_2)
        #self.list_c_path.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.list_c_path.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_c_path.setDragEnabled(True)
        self.list_c_path.setDragDropOverwriteMode(False)
        self.list_c_path.setDefaultDropAction(Qt.MoveAction)
        self.list_c_path.setObjectName("list_c_path")
        self.gridLayout_2.addWidget(self.list_c_path, 3, 0, 1, 2)


        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_10.addWidget(self.label_4)
        self.list_c_drive = QtWidgets.QListWidget(self.groupBox_2)
        self.list_c_drive.setMaximumSize(QtCore.QSize(100, 16777215))
        self.list_c_drive.setObjectName("list_c_drive")
        self.verticalLayout_10.addWidget(self.list_c_drive)
        self.gridLayout_2.addLayout(self.verticalLayout_10, 0, 0, 1, 2)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_11.setObjectName("label_11")
        self.verticalLayout_11.addWidget(self.label_11)
        self.line_c_cur_path = QtWidgets.QLineEdit(self.groupBox_2)
        self.line_c_cur_path.setFocusPolicy(QtCore.Qt.NoFocus)
        self.line_c_cur_path.setObjectName("line_c_cur_path")
        self.verticalLayout_11.addWidget(self.line_c_cur_path)
        self.gridLayout_2.addLayout(self.verticalLayout_11, 1, 0, 1, 2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.push_c_back = QtWidgets.QPushButton(self.groupBox_2)
        self.push_c_back.setMaximumSize(QtCore.QSize(50, 16777215))
        self.push_c_back.setObjectName("push_c_back")
        self.horizontalLayout_6.addWidget(self.push_c_back)
        self.push_c_foward = QtWidgets.QPushButton(self.groupBox_2)
        self.push_c_foward.setMaximumSize(QtCore.QSize(50, 16777215))
        self.push_c_foward.setObjectName("push_c_foward")
        self.horizontalLayout_6.addWidget(self.push_c_foward)
        self.push_c_new = QtWidgets.QPushButton(self.groupBox_2)
        self.push_c_new.setObjectName("push_c_new")
        self.horizontalLayout_6.addWidget(self.push_c_new)
        self.push_c_del = QtWidgets.QPushButton(self.groupBox_2)
        self.push_c_del.setObjectName("push_c_del")
        self.horizontalLayout_6.addWidget(self.push_c_del)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 0, 1, 2)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 1)
        self.gridLayout_2.setRowStretch(3, 13)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.horizontalLayout_2.setStretch(0, 6)
        self.horizontalLayout_2.setStretch(1, 4)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1252, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "EQP_Local"))
        self.groupBox.setTitle(_translate("mainWindow", "EQP "))
        self.label_10.setText(_translate("mainWindow", "현재 경로"))
        self.label.setText(_translate("mainWindow", "Line"))
        self.label_12.setText(_translate("mainWindow", "EQP"))
        self.label_2.setText(_translate("mainWindow", "Drive"))
        self.label_3.setText(_translate("mainWindow", "확장자"))
        self.push_eqp_info.setText(_translate("mainWindow", "EQP 등록"))
        self.push_ext_info.setText(_translate("mainWindow", "확장자 등록"))
        self.label_9.setText(_translate("mainWindow", "Path5"))
        self.push_e_back.setText(_translate("mainWindow", "◀"))
        self.push_e_foward.setText(_translate("mainWindow", "▶"))
        self.push_e_new.setText(_translate("mainWindow", "새폴더(ctrl+n)"))
        self.push_e_del.setText(_translate("mainWindow", "삭제(ctrl+d)"))
        self.label_7.setText(_translate("mainWindow", "Path3"))
        self.label_8.setText(_translate("mainWindow", "Path4"))
        self.label_5.setText(_translate("mainWindow", "Path1"))
        self.label_6.setText(_translate("mainWindow", "Path2"))
        self.push_manual.setText(_translate("mainWindow", "사용법"))
        self.push_hotkey.setText(_translate("mainWindow", "단축키"))
        self.groupBox_2.setTitle(_translate("mainWindow", "Local"))
        self.label_4.setText(_translate("mainWindow", "Drive"))
        self.label_11.setText(_translate("mainWindow", "현재 경로"))
        self.push_c_back.setText(_translate("mainWindow", "◀"))
        self.push_c_foward.setText(_translate("mainWindow", "▶"))
        self.push_c_new.setText(_translate("mainWindow", "새폴더(n)"))
        self.push_c_del.setText(_translate("mainWindow", "삭제(del.)"))
####################################################################################
##############################Form Code End#########################################

#ftp upload
class Lst_e_path1(QListWidget):
    def __init__(self, parent=None):
        super(Lst_e_path1, self).__init__(parent)
        self.setAcceptDrops(True)
        global ftp

    def dropEvent(self, QDropEvent):
        global ftp
        global ftp_dic

        source_Widget = QDropEvent.source()
        print(source_Widget.objectName())
        if 'list_e_path' in source_Widget.objectName() : return
        ########################################################위 공통

class Lst_e_path2(QListWidget):
    def __init__(self, parent=None):
        super(Lst_e_path2, self).__init__(parent)
        self.setAcceptDrops(True)
        global ftp

    def dropEvent(self, QDropEvent):
        global ftp
        global ftp_dic
        #211002 전체 lineedit 경로 중 path2에 해당하는 경로만 가져오기
        source_Widget = QDropEvent.source()

        e_flag['all_overwrite'] = 0
        e_flag['ask_cnt'] = 0

        if 'list_e_path' in source_Widget.objectName() : return
        ########################################################위 공통
        ftp_dic['item_list_up'] = [item.text() for item in source_Widget.selectedItems()]  # str
        items = source_Widget.selectedItems()
        if ftp_dic['e_line'][-1] == '/' : ftp_dic['e_line'] = find_upload_index(ftp_dic['e_line'], 2)         #몇번째 리스트까지의 경로를 가져올지에 대한 함수
        else : ftp_dic['e_line'] = find_upload_index(ftp_dic['e_line'] + '/', 2)  # 몇번째 리스트까지의 경로를 가져올지에 대한 함수
        upload_to_eqp(ftp_dic)  # upload

        for i in items:
            if e_flag['overwrite_u'][i.text()] == 0:
                icon_item = QListWidgetItem(i.icon(), i.text())
                self.addItem(icon_item)

class Lst_e_path3(QListWidget):
    def __init__(self, parent=None):
        super(Lst_e_path3, self).__init__(parent)
        self.setAcceptDrops(True)
        global ftp

    def dropEvent(self, QDropEvent):
        global ftp
        global ftp_dic

        source_Widget = QDropEvent.source()
        #print(source_Widget.objectName())
        if 'list_e_path' in source_Widget.objectName() : return
        ########################################################위 공통

class Lst_e_path4(QListWidget):
    def __init__(self, parent=None):
        super(Lst_e_path4, self).__init__(parent)
        self.setAcceptDrops(True)
        global ftp

    def dropEvent(self, QDropEvent):
        global ftp
        global ftp_dic

        source_Widget = QDropEvent.source()
        print(source_Widget.objectName())
        if 'list_e_path' in source_Widget.objectName() : return
        ########################################################위 공통

class Lst_e_path5(QListWidget):
    def __init__(self, parent=None):
        super(Lst_e_path5, self).__init__(parent)
        self.setAcceptDrops(True)
        global ftp

    def dropEvent(self, QDropEvent):
        global ftp
        global ftp_dic

        source_Widget = QDropEvent.source()
        print(source_Widget.objectName())
        if 'list_e_path' in source_Widget.objectName() : return
        ########################################################위 공통

#211002 여기부터
def find_upload_index(f_path,n):
    sum = 0
    temp = 0
    temp_path = f_path
    for i in range(0, n + 3):
        if i == 0: f_path = f_path[temp:]
        else: f_path = f_path[temp+1:]
        temp = f_path.find('/')
        sum += (temp+1)
    print(temp_path[:sum-1])
    return temp_path[:sum-1]


#ftp upload
def upload_to_eqp(f_dic):       #전체 다운
    global ftp
    print(f_dic)
    idx = f_dic['e_line'].find('/',7) + 2
    #f_dic['e_line'] = f_dic['e_line'][idx:] #여기서 변함
    ftp_path = f_dic['e_line'][idx:]
    origin = ftp.pwd()

    #ftp.cwd("받아올  파일 위치")
    for filename in f_dic['item_list_up']:
        try:
            upload_local_Files(f_dic['c_line'] + '\\' + filename, ftp_path)
            ftp.cwd(origin)
        except PermissionError as e:
            pyautogui.alert('다운받을 수 없는 경로입니다.', 'FTP Upload Interlock')

def ftp_is_in(str):
    global ftp

    f_dic = dict(list(ftp.mlsd()))
    try:
        print(f_dic[str])
        return True
    except KeyError:
        return False


def upload_local_Files(local, ftp_path):      #1개 path 다운
    global ftp
    global ftp_dic
    m_list = []
    m_dic = {}
    sleep(1)

    if os.path.isdir(local):
        #폴더 업로드
        try:
            t = local.replace('\\', '/')
            p = ftp_path + t[t.rfind('/'):]
            ftp.mkd(p)
        except: #중복될때
            #e_flag['folder_overwrite_u'] = 0
            folder = t[t.rfind('/') + 1:]
            if e_flag['ask_cnt'] < 4:
                a = pyautogui.confirm(folder + '\n이미 존재하는 폴더입니다. 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
            else:
                if e_flag['all_overwrite'] == 0:
                    b = pyautogui.confirm('모든 폴더(파일)에 대해 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
                    if b == 'Yes':
                        e_flag['all_overwrite'] = 2
                    else:
                        e_flag['all_overwrite'] = 3

            e_flag['overwrite_u'][folder] = 1
            e_flag['ask_cnt'] += 1

    else:
        #파일 업로드
        a=''
        t = local.replace('\\', '/')
        #print(t[t.rfind('/') : ])
        if ftp_is_in(t[t.rfind('/') +1 : ]):
            if e_flag['ask_cnt'] < 4 : a = pyautogui.confirm(t[t.rfind('/') +1 : ] + '\n이미 존재하는 파일입니다. 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
            else:
                if e_flag['all_overwrite'] == 0 :
                    b = pyautogui.confirm('모든 폴더(파일)에 대해 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
                    if b == 'Yes' : e_flag['all_overwrite'] = 2
                    else : e_flag['all_overwrite'] = 3
            if a == 'Yes' or e_flag['all_overwrite'] == 2:
                e_flag['overwrite_u'][t[t.rfind('/') +1 : ]] = 1
                fd = open(local, 'rb')  # download local path
                ftp.storbinary("STOR " + local[local.rfind('\\') + 1:], fd)
                fd.close()
                e_flag['ask_cnt'] += 1
                return
            else:
                e_flag['overwrite_u'][ftp_path[ftp_path.rfind('/') + 1:]] = 1
                e_flag['ask_cnt'] += 1
                return

        else:
            #print(local[local.rfind('/') + 1:])
            fd = open(local, 'rb')
            ftp.storbinary("STOR " + local[local.rfind('\\') + 1:], fd)
            fd.close()
            e_flag['ask_cnt'] += 1
            return



    #아래부터 폴더 내 파일 있는 경우
    file_list = os.listdir(local)
    if file_list == [] : return     #없으면 종료

    #폴더 내 파일이 있다면 : 재귀
    for file in file_list:
        t = local.replace('\\', '/')
        #print(t[t.rfind('/'):])
        #print(ftp_path + t[t.rfind('/'):] + '/' + file)
        #print(local+ '\\' + file)

        if os.path.isdir(local + '\\' + file):     #폴더일때
            #ftp.mkd(ftp_path + '/' + file)
            ftp.cwd(ftp_path + t[t.rfind('/'):])
            upload_local_Files(local + '\\' + file, ftp_path + t[t.rfind('/'):])

        else :                       #파일일때
            ftp.cwd(ftp_path + t[t.rfind('/'):])
            if ftp_is_in(file):
                if e_flag['ask_cnt'] < 4:
                    a = pyautogui.confirm(file + '\n이미 존재하는 파일입니다. 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
                else:
                    if e_flag['all_overwrite'] == 0:
                        b = pyautogui.confirm('모든 폴더(파일)에 대해 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
                        if b == 'Yes':
                            e_flag['all_overwrite'] = 2
                        else:
                            e_flag['all_overwrite'] = 3
                if a == 'Yes' or e_flag['all_overwrite'] == 2:
                    e_flag['overwrite_u'][file] = 1
                    fd = open(local + '\\' + file, 'rb')  # download local path
                    ftp.storbinary("STOR " + file, fd)
                    fd.close()
                    e_flag['ask_cnt'] += 1
                    return
                else:
                    e_flag['overwrite'][ftp_path[ftp_path.rfind('/') + 1:]] = 1
                    e_flag['ask_cnt'] += 1
                    return

            else:
                fd = open(local + '\\' + file, 'rb')  # download local path
                ftp.storbinary("STOR " + file, fd)
                fd.close()
                e_flag['ask_cnt'] += 1
                return


###########################################################################################
#ftp download
class Lst_c_path(QListWidget):
    def __init__(self, parent=None):
        super(Lst_c_path, self).__init__(parent)
        self.setAcceptDrops(True)
        global ftp

    def dropEvent(self, QDropEvent):
        global ftp
        global ftp_dic
        e_flag['all_overwrite'] = 0
        e_flag['ask_cnt'] = 0
        source_Widget = QDropEvent.source()
        if 'list_c_path' in source_Widget.objectName(): return
        ftp_dic['item_list'] = [item.text() for item in source_Widget.selectedItems()]      #str
        items = source_Widget.selectedItems()

        download_to_local(ftp_dic)      #download

        for i in items:
            #source_Widget.takeItem(source_Widget.indexFromItem(i).row())
            if e_flag['overwrite'][i.text()] == 0 and e_flag['ext'][i.text()] == 0:
                icon_item = QListWidgetItem(i.icon(), i.text())
                self.addItem(icon_item)

        # print(source_Widget.objectName())


def download_to_local(f_dic):       #전체 다운
    global ftp
    idx = f_dic['e_line'].find('/',7) + 2
    #f_dic['e_line'] = f_dic['e_line'][idx:] #여기서 변함
    ftp_path = f_dic['e_line'][idx:]

    #ftp.cwd("받아올  파일 위치")
    for filename in f_dic['item_list']:
        try:
            download_FTP_Files(ftp_path + filename, f_dic['c_line'])
        except PermissionError as e:
            pyautogui.alert('다운받을 수 없는 경로입니다.', 'FTP Down Interlock')

def download_FTP_Files(path, destination):      #1개 path 다운
    global ftp
    global ftp_dic
    ext_flag = 0
    m_list = []
    m_dic = {}
    sleep(1)

    a=''

    e_flag['overwrite'][path[path.rfind('/') + 1:]] = 0
    e_flag['ext'][path[path.rfind('/') + 1:]] = 0

    try:            #폴더 다운
        ftp.cwd(path)
        mkdir_p(destination.replace('\\','/') + path[path.rfind('/'):])
        if e_flag['folder_overwrite'] == 1 : return

    except ftplib.error_perm:       #파일 다운로드
        ftp.cwd(path[:path.rfind('/')])
        timestamp = ''
        f = path[path.rfind('/') + 1:]

######################################ftp mlsd를 dic로 변환
######################################timestamp, 확장자 확정
        m_list = list(ftp.mlsd())
        m_dic = dict(m_list)

        timestamp = m_dic[f]['modify']
        if ftp_dic['ext_list'] == []:
            ext_flag = 1
        else:
            for i in ftp_dic['ext_list']:
                if i == all : ext_flag = 1
                if i in f : ext_flag = 1

        if ext_flag == 0 :
            e_flag['ext'][f] = 1
            return

        mtime = parser.parse(timestamp)
        #파일 존재하면 인터락
        if os.path.isfile(destination + '\\' + path[path.rfind('/') + 1 :]):
            if e_flag['ask_cnt'] < 4 : a = pyautogui.confirm(path[path.rfind('/') + 1 :] + '\n이미 존재하는 파일입니다. 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
            else:
                if e_flag['all_overwrite'] == 0 :
                    b = pyautogui.confirm('모든 폴더(파일)에 대해 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
                    if b == 'Yes' : e_flag['all_overwrite'] = 2
                    else : e_flag['all_overwrite'] = 3
            if a == 'Yes' or e_flag['all_overwrite'] == 2:
                e_flag['overwrite'][path[path.rfind('/') + 1:]] = 1
                fd = open(destination + '\\' + path[path.rfind('/') + 1:], 'wb')  # download local path
                ftp.retrbinary("RETR " + path[path.rfind('/') + 1:], fd.write)
                fd.close()
                os.utime(destination + '\\' + path[path.rfind('/') + 1:], (mtime.timestamp(), mtime.timestamp()))
                e_flag['ask_cnt'] += 1
                return
            else:
                e_flag['overwrite'][path[path.rfind('/') + 1 :]] = 1
                e_flag['ask_cnt'] += 1
                return
        else:

            fd = open(destination + '\\' + path[path.rfind('/') + 1 :], 'wb')                #download local path
            ftp.retrbinary("RETR " + path[path.rfind('/') + 1 :], fd.write)
            fd.close()
            os.utime(destination + '\\' + path[path.rfind('/') + 1 :], (mtime.timestamp(), mtime.timestamp()))
            return

    filelist = ftp.nlst()

    if filelist == [] : return      #path가 폴더이고 폴더 내 파일이나 폴더 1개 이상 있을 때

    for file in filelist:
        ext_flag = 0
        e_flag['overwrite'][file] = 0
        time.sleep(0.05)
        try:        #폴더
            ftp.cwd(path + '/' + file)
            download_FTP_Files(path + '/' + file, destination + '/' + path[path.rfind('/') + 1 :])
        except ftplib.error_perm:       #파일
            f_name = destination + '\\' + path[path.rfind('/') + 1:] + '\\' + file
            timestamp = ''

            ######################################ftp mlsd를 dic로 변환
            ######################################timestamp, 확장자 확정
            m_list = list(ftp.mlsd())
            m_dic = dict(m_list)

            timestamp = m_dic[file]['modify']
            if ftp_dic['ext_list'] == []:
                ext_flag = 1
            else:
                for i in ftp_dic['ext_list']:
                    if i == all: ext_flag = 1
                    if i in file: ext_flag = 1

            if ext_flag == 0:
                e_flag['ext'][file] = 1
                continue
#

            mtime = parser.parse(timestamp)
            if os.path.isfile(f_name):
                if e_flag['ask_cnt'] < 4 : a = pyautogui.confirm(file + '\n이미 존재하는 파일입니다. 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
                else:
                    if e_flag['all_overwrite'] == 0 :
                        b = pyautogui.confirm('모든 폴더(파일)에 대해 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
                        if b == 'Yes' : e_flag['all_overwrite'] = 2
                        else : e_flag['all_overwrite'] = 3

                if a == 'Yes' or e_flag['all_overwrite'] == 2:
                    e_flag['overwrite'][file] = 1
                    fd = open(f_name, 'wb')  # download local path
                    ftp.retrbinary("RETR " + file, fd.write)
                    fd.close()
                    os.utime(f_name, (mtime.timestamp(), mtime.timestamp()))
                    e_flag['ask_cnt'] += 1

                else:
                    e_flag['overwrite'][file] = 1
                    e_flag['ask_cnt'] += 1
            else:
                fd = open(f_name, 'wb')  # download local path
                ftp.retrbinary("RETR " + file, fd.write)
                fd.close()
                os.utime(f_name, (mtime.timestamp(), mtime.timestamp()))

def mkdir_p(path):
    global ftp
    a = ''
    try:
        os.makedirs(path)
    except OSError as exc:
        e_flag['folder_overwrite'] = 0
        folder = path[path.rfind('/') + 1:]
        if e_flag['ask_cnt'] < 4 : a = pyautogui.confirm(folder + '\n이미 존재하는 폴더입니다. 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
        else :
            if e_flag['all_overwrite'] == 0 :
                b = pyautogui.confirm('모든 폴더(파일)에 대해 덮어 씌우겠습니까?', title='FTP Down Interlock', buttons=['Yes', 'No'])
                if b == 'Yes' : e_flag['all_overwrite'] = 2
                else : e_flag['all_overwrite'] = 3
        if a == 'Yes' or e_flag['all_overwrite'] == 2:
            e_flag['overwrite'][folder] = 1
            e_flag['folder_overwrite'] = 0
            e_flag['ask_cnt'] += 1
            return

        else:
            e_flag['overwrite'][folder] = 1
            e_flag['folder_overwrite'] = 1
            e_flag['ask_cnt'] += 1
            return




#############################################################################
#################################pgb#########################################

class Thread_pgb(QThread):
    def __init__(self, parent):
        self.parent = parent

    def run(self):
        dlg = Load_pgb_dialog()
        dlg.exe_()


form_class_pgb = uic.loadUiType("Load_pgb.ui")[0]
class Load_pgb_dialog(QDialog, form_class_pgb):
    def __init__(self):
        super().__init__()  # 기반 클래스의 생성자 실행 : QMainWindow의 생성자 호출
        self.setupUi(self)

##############################################################################

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
