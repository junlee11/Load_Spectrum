#210922 Project 시작

import sys, os, re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pandas as pd
import ftplib

#210927 Local 탐색기 구현하기
c_flag = {'c_is_inf' : 0, 'c_access' : 0, 'back' : 0}

form_class = uic.loadUiType("Load_Main.ui")[0]

class WindowClass(QMainWindow, form_class) :

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        global c_flag
        self.c_fow_list = []
        self.list_e_ip1 = ''
        self.list_e_ip2 = ''
        self.list_e_ip3 = ''
        self.list_e_ip4 = ''
        self.list_e_ip5 = ''

        #Local
        self.list_c_drive.addItem('C:')
        self.list_c_drive.addItem('D:')
        self.list_c_drive.addItem('E:')
        self.list_c_drive.itemClicked.connect(self.c_drive_clk)
        self.push_c_back.clicked.connect(self.c_push_back_clk)
        self.push_c_foward.clicked.connect(self.c_push_fow_clk)
        self.list_c_path.itemDoubleClicked.connect(self.c_path_dbclk)

        self.shortcut_open = QShortcut(QKeySequence('backspace'), self)        #단축키 설정
        self.shortcut_open.activated.connect(self.c_push_back_clk)

##############################################이하 EQP
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

        #EQP ftp 파일,복사 리스트 생성
        self.list_e_eqp.itemClicked.connect(self.e_mk_drive)
        self.list_e_drive.itemClicked.connect(self.e_mk_path1)
        self.list_e_path1.itemClicked.connect(self.e_mk_path2)
        self.list_e_path2.itemClicked.connect(self.e_mk_path3)
        self.list_e_path3.itemClicked.connect(self.e_mk_path4)
        self.list_e_path4.itemClicked.connect(self.e_mk_path5)

        self.push_eqp_info.clicked.connect(self.e_push_open_eqp)
        self.push_ext_info.clicked.connect(self.e_push_open_ext)
        self.push_manual.clicked.connect(self.e_push_open_manual)

    #EQP 파일 열기
    def e_push_open_eqp(self):
        os.startfile('ip_info.txt')

    #확장자 파일 열기
    def e_push_open_ext(self):
        os.startfile('ext_info.txt')

    #매뉴얼 파일 열기
    def e_push_open_manual(self):
        os.startfile('manual.xlsx')

    #EQP List 만들기
    def e_mk_eqp(self):
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
        self.list_e_drive.clear()
        self.list_e_drive.addItem('D:')
        self.list_e_drive.addItem('E:')

    #본격적으로 eqp path 만들기
    def e_mk_path1(self):
        ftp_id = ''
        ftp_pw = ''

        for i in self.e_path_list:
            i.clear()

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
            QMessageBox.warning(self, 'IP Interlock', '해당 설비로 접근할 수 없습니다. / IP 확인 필요')
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
        self.e_mk_path_all(1)

    def e_mk_path3(self):
        self.e_mk_path_all(2)

    def e_mk_path4(self):
        self.e_mk_path_all(3)

    def e_mk_path5(self):
        self.e_mk_path_all(4)

    def e_mk_path_all(self, k):
        temp = ''
        for i in range(k, len(self.e_path_list)):
            self.e_path_list[i].clear()
        self.e_path_ip[k] = self.e_path_ip[k - 1] + self.e_path_list[k - 1].currentItem().text() + '/'
        arr_e_path, arr_e_path_mlsd = self.e_arr(self.e_path_ip[k])
        temp = self.line_e_cur_path.text()[:-1] + self.e_path_ip[k]
        self.line_e_cur_path.clear()                                #여기부터 210928
        self.line_e_cur_path.setText(temp)
        self.e_list_to_target(arr_e_path, arr_e_path_mlsd, k)

    def e_arr(self, f_path):
        f_path_list = []
        f_exe_list = []
        #ftp 경로 지정
        self.ftp.cwd(f_path)
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

        #print(f_path_list_mlsd)
        #print(f_path_list)
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
            



    #210928
    #path5 더블클릭 path 만들어야 함
    #line 경로 제대로 수정







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


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()