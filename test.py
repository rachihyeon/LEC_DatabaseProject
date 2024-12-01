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

def connect_to_database():
    try:
        conn = MySQLdb.connect(
            host='localhost',
            user='root',      
            passwd='1234',   
            db='inventory_control'   
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

inventory_id = "6"
quantity_text = "10"
transaction_type = "IN"
warehouse_id = "1"
quantity=int(quantity_text)

conn = connect_to_database()
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO InventoryTransaction (InventoryID, WarehouseID, UserID, TransactionType, Quantity)
                VALUES ("6", "1", "admin", "IN", "4")""", 
               )
conn.commit()


cursor.close()
conn.close()