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


class ChangePasswordDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        # path = os.path.join(os.path.dirname(__file__), 'Change_password.ui')
        if hasattr(sys, '_MEIPASS'):
            path = os.path.join(sys._MEIPASS, 'Change_password.ui')
        else:
            path = os.path.join(os.path.abspath("."), 'Change_password.ui')
        uic.loadUi(path, self)
        
        self.user_id = user_id
        self.setWindowTitle("비밀번호 변경")

        # 버튼 클릭 연결
        self.accept.clicked.connect(self.change_password)
        self.reject.clicked.connect(self.close)

    def change_password(self):
        old_pass = self.Old_password.text()
        new_pass = self.New_password.text()
        confirm_pass = self.Confirm_password.text()

        # 비밀번호 일치 여부 확인
        if new_pass != confirm_pass:
            QMessageBox.warning(self, "오류", "새 비밀번호와 확인 비밀번호가 일치하지 않습니다.")
            return

        # 실제 비밀번호 변경 로직 (DB 연결 및 변경)
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            try:
                # 사용자가 입력한 현재 비밀번호와 DB의 비밀번호를 비교
                query = "SELECT Password FROM user WHERE UserID = %s"
                cursor.execute(query, (self.user_id,))
                result = cursor.fetchone()

                if result and result[0] == old_pass:
                    # 비밀번호 변경 쿼리
                    update_query = "UPDATE user SET Password = %s WHERE UserID = %s"
                    cursor.execute(update_query, (new_pass, self.user_id))
                    conn.commit()

                    QMessageBox.information(self, "성공", "비밀번호가 성공적으로 변경되었습니다.")
                    self.close()  # 대화상자 닫기
                else:
                    QMessageBox.warning(self, "오류", "현재 비밀번호가 잘못되었습니다.")

            except Exception as e:
                QMessageBox.warning(self, "오류", f"비밀번호 변경 실패: {str(e)}")
            finally:
                cursor.close()
                conn.close()
        else:
            QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")

            