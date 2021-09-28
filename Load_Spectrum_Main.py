#210922 Project 시작

import sys, os, re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pandas as pd
import ftplib
import tkinter
from tkinter import ttk
import shutil
import keyboard

#hot key 알아내기
# while True:
#     print(keyboard.read_key())

c_flag = {'c_is_inf' : 0, 'c_access' : 0, 'back' : 0}
e_flag = {'e_is_path' : 0, 'e_path5' : 0, 'back' : 0, 'e_find' : 0}

form_class = uic.loadUiType("Load_Main_EQP_Local.ui")[0]
#form_class = uic.loadUiType("Load_Main_Local_EQP.ui")[0]

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        global c_flag
        global e_flag
        self.c_fow_list = []
        self.e_fow_list = []
        self.list_e_ip1 = ''
        self.list_e_ip2 = ''
        self.list_e_ip3 = ''
        self.list_e_ip4 = ''
        self.list_e_ip5 = ''
        self.e_path5_str = ''

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

        ########보조 push button
        self.push_eqp_info.clicked.connect(self.e_push_open_eqp)
        self.push_ext_info.clicked.connect(self.e_push_open_ext)
        self.push_manual.clicked.connect(self.e_push_open_manual)
        self.push_hotkey.clicked.connect(self.e_push_open_hotkey)

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

    #본격적으로 eqp path 만들기
    def e_mk_path1(self):
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

        self.ftp = ftplib.FTP()
        try:
            self.ftp.connect(self.ftp_ip, 21)
        except:
            QMessageBox.warning(self, 'IP Interlock', '접속할 수 없습니다. / IP 주소 및 접속 상태 확인')
            return

        try:
            self.ftp.login(ftp_id, ftp_pw)
        except ftplib.error_perm:
            QMessageBox.warning(self, 'FTP Login Interlock', 'FTP 계정정보가 올바르지 않습니다')
            return

        #self.ftp.cwd('/test/')
        #self.ftp.cwd('/test/a/')
        #self.ftp.cwd('/test/')

        self.line_e_cur_path.setText('ftp://' + self.ftp_ip + '/' + self.list_e_drive.currentItem().text()[:-1] + self.ftp.pwd())
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
        e_flag['e_is_path'] = 0
        f_path_list = []
        f_exe_list = []
        #ftp 경로 지정
        try:
            self.ftp.cwd(f_path)
        except ftplib.error_perm:
            QMessageBox.warning(self, 'Path Interlock', '다음 경로를 보려면 폴더를 선택하세요.')
            e_flag['e_is_path'] = 1
            return

        try:
            f_path_list_mlsd = [f for f in list(self.ftp.mlsd()) if not (f[0].startswith('.') or (f[0].startswith('$')))]
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
        for i in f_mlsd:
            if s == i[0] : return 'dir' == i[1]['type']

    #path5 더블클릭용 ftp에서 1개의 경로만 받아 폴더 유무 판단
    def ftp_isdir2(self,s):
        t_flag = 0
        origin_ip = self.line_e_cur_path.text()[self.ftp_ip_idx-1:]
        #chg_ip = origin_ip + s
        ftp_mlsd = list(self.ftp.mlsd())
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
        if e_flag['back'] != 0:
            arr_e_path, arr_e_path_mlsd = self.e_arr(self.e_fow_list[e_flag['back']-1])
            self.e_path_list[4].clear()
            self.e_list_to_target(arr_e_path, arr_e_path_mlsd, 4)
            self.line_e_cur_path.setText(self.line_e_cur_path.text()[:self.ftp_ip_idx - 1] + self.e_fow_list[e_flag['back']-1])
            e_flag['back'] += -1
            self.e_fow_list.pop()

    def e_push_new_clk(self):
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
            self.ftp.mkd(f_path)
            icon = QIcon('Icon_folder.png')
            icon_item = QListWidgetItem(icon, self.new_folder)
            self.e_path_list[e_flag['e_find']].addItem(icon_item)

        except ftplib.error_perm:
            QMessageBox.warning(self, 'Path Interlock', '이미 존재하는 폴더입니다.')
            return

    def e_push_del_clk(self):

        if e_flag['e_find'] == 0 : return
        try:
            print(self.e_path_list[e_flag['e_find']].currentItem().text())
        except AttributeError:
            QMessageBox.warning(self, 'Path Interlock', '삭제하려는 대상의 경로가 있는 리스트에서 선택하세요.')
            return

        reply = QMessageBox.question(self, '삭제 경고', self.e_path_list[e_flag['e_find']].currentItem().text() + '\n정말로 선택한 파일(폴더)를 삭제 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            f_name = self.line_e_cur_path.text()[self.ftp_ip_idx - 1:] + self.e_path_list[e_flag['e_find']].currentItem().text()
            self.remove_ftp_dir(f_name)
            self.e_path_list[e_flag['e_find']].takeItem(self.e_path_list[e_flag['e_find']].currentRow())
        else:
            pass

    #ftp 경로 내 파일, 폴더 삭제
    def remove_ftp_dir(self, c_path):
        for (name, properties) in self.ftp.mlsd(path = c_path):
            if name in ['.', '..']:
                continue
            elif properties['type'] == 'file':
                try:
                    print(f"{c_path}/{name}")
                    self.ftp.delete(f"{c_path}/{name}")
                except ftplib.error_perm:
                    self.ftp.delete(c_path)
                    return
            elif properties['type'] == 'dir':
                self.remove_ftp_dir(f"{c_path}/{name}")
        self.ftp.rmd(c_path)








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
            name, ext = os.path.splitext(path + '/' + i)
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
            name, ext = os.path.splitext(path + '/' + i)
            arr_dic[ext].append(i)

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
            print(self.list_c_path.currentItem().text())
        except AttributeError:
            QMessageBox.warning(self, 'Path Interlock', '삭제하려는 대상의 경로가 있는 리스트에서 선택하세요.')
            return

        reply = QMessageBox.question(self, '삭제 경고', self.list_c_path.currentItem().text() + '\n정말로 선택한 파일(폴더)를 삭제 하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            shutil.rmtree(self.line_c_cur_path.text() + '/' + self.list_c_path.currentItem().text())
            self.list_c_path.takeItem(self.list_c_path.currentRow())
        else:
            pass





if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()