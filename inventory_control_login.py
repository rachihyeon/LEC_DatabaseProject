import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5 import uic
from resources import resource
import MySQLdb

# MySQL 데이터베이스 연결 함수
def connect_to_database():
    try:
        conn = MySQLdb.connect(
            host='localhost',
            user='root',      
            passwd='1234',   
            db='inventory_control'
        )
        return conn
    except MySQLdb.Error as err:
        print(f"Error: {err}")
        return None


#최초화면 Login화면 출력
class WindowClass(QMainWindow):
    def __init__(self) :
        super().__init__()
        # path = os.path.join(os.path.dirname(__file__), 'inventory_control_login.ui')
        if hasattr(sys, '_MEIPASS'):
            path = os.path.join(sys._MEIPASS, 'inventory_control_login.ui')
        else:
            path = os.path.join(os.path.abspath("."), 'inventory_control_login.ui')
        #self.setupUi(self)
        uic.loadUi(path, self)

        self.LoginButton.clicked.connect(self.loginFunction)
        self.IDBox.returnPressed.connect(self.loginFunction)
        self.PasswordBox.returnPressed.connect(self.loginFunction)

    def loginFunction(self):
        id = self.IDBox.text()
        password = self.PasswordBox.text()

        conn = connect_to_database()

        if conn:
            cursor = conn.cursor()

            # user 테이블에서 ID와 비밀번호 확인
            query = "SELECT password FROM user WHERE UserID = %s"
            cursor.execute(query, (id,))  # 사용자 ID로 비밀번호 확인
            result = cursor.fetchone()

            if result:
                db_password = result[0]  # DB에서 가져온 비밀번호
                if password == db_password:
                    # 성공 시 메인 창 열기
                    from inventory_control_main import MainWindow
                    self.main_window = MainWindow(id)
                    self.main_window.load_inventory_data()
                    self.main_window.show()
                    self.close()  # 로그인 창 닫기
                else:
                    QMessageBox.warning(self, "로그인 실패", "잘못된 비밀번호입니다.")
            else:
                QMessageBox.warning(self, "로그인 실패", "잘못된 ID입니다.")

            cursor.close()
            conn.close()
        else:
            QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")
 
 