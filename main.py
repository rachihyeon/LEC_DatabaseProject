import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5 import uic
from resources import resource
import MySQLdb
from Change_password import *
from inventory_control_login import *
from inventory_control_main import *


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


if __name__ == "__main__" :
    app = QApplication(sys.argv) 
    myWindow = WindowClass() 
    myWindow.show()
    app.exec_()

