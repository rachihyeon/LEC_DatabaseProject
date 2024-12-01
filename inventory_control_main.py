import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5 import uic
from resources import resource
import MySQLdb
from Change_password import ChangePasswordDialog
from inventory_control_login import WindowClass

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


#Main 화면
class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        # path = os.path.join(os.path.dirname(__file__), 'inventory_control_main.ui')
        if hasattr(sys, '_MEIPASS'):
            path = os.path.join(sys._MEIPASS, 'inventory_control_main.ui')
        else:
            path = os.path.join(os.path.abspath("."), 'inventory_control_main.ui')
        uic.loadUi(path, self)
        self.user_id = user_id
        self.user_name = ''
        self.user_role = ''
        self.user_authority = ['']

        self.load_user_info()   # 사용자 정보 로드
        self.initialize_tabs()
        self.load_transaction_data()


        self.LogOutButton.clicked.connect(self.logout)                  # 로그아웃 버튼 반응
        self.SearchButton.clicked.connect(self.search_inventory)        # 검색 버튼 클릭 연결
        self.SearchKeyword.installEventFilter(self) 
        self.SearchedDataField.setSortingEnabled(True)               # 열 클릭 시 정렬 활성화
        self.ChangePasswordButton.clicked.connect(self.open_change_password_window)
        self.SearchedDataField.setEditTriggers(QAbstractItemView.NoEditTriggers)
        

        # ----------------------------------------------------------
        self.Registration.clicked.connect(self.register_transaction)
        self.Clear.clicked.connect(self.clear_inputs)
        self.InventoryID.setTabChangesFocus(True)
        self.Quantity.setTabChangesFocus(True)
        self.WarehouseID.setTabChangesFocus(True)
        self.TransactionList.setSortingEnabled(True)
        self.TransactionList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        

        # ----------------------------------------------------------
        self.ProductRegistration.clicked.connect(self.register_product)
        self.ProductDelete.clicked.connect(self.delete_product)
        self.load_product_data()
        self.ProductName.setTabChangesFocus(True)
        self.ProductDescription.setTabChangesFocus(True)
        self.Unitprice.setTabChangesFocus(True)
        self.ProductTable.setSortingEnabled(True)
        self.ProductTable.setEditTriggers(QAbstractItemView.NoEditTriggers)



        # ----------------------------------------------------------

    def open_change_password_window(self):
        # Change_password.ui 창을 띄울 때 user_id를 넘겨줌
        self.change_password_window = ChangePasswordDialog(self.user_id)
        self.change_password_window.exec_()  # exec_() 메서드 사용

    def eventFilter(self, source, event):
        if source is self.SearchKeyword and event.type() == QKeyEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.search_inventory()  # Enter 키 입력 시 검색 실행
                return True  # 이벤트를 처리했다고 알려줌
        return super().eventFilter(source, event)

    def logout(self):
        # 로그아웃 재확인 
        reply = QMessageBox.question(
            self,
            "로그아웃",
            "로그아웃 하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No 
        )

        if reply == QMessageBox.Yes:
            self.login_window = WindowClass()
            self.login_window.show()
            self.close() 
        else:
            pass

    def load_user_info(self):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            try:
                # UserInfoView에서 사용자 정보 가져오기
                query = """
                    SELECT Name, RoleName, AuthorityName 
                    FROM UserInfoView 
                    WHERE UserID = %s
                """
                cursor.execute(query, (self.user_id,))
                results = cursor.fetchall()

                if results:
                    self.user_name, self.user_role = results[0][:2]
                    for result in results:
                        self.user_authority.append(result[2])
                    self.NameField.setText(self.user_name)
                    self.NameField.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.RoleField.setText(self.user_role)

                    # # 권한 목록 표시
                    # self.AuthorityList.clear()
                    # for _, _, authority in results:
                    #     self.AuthorityList.addItem(authority)
                else:
                    QMessageBox.warning(self, "오류", "사용자 정보를 불러올 수 없습니다.")

            except MySQLdb.Error as err:
                QMessageBox.critical(self, "DB 오류", f"데이터베이스 오류: {err}")

            finally:
                cursor.close()
                conn.close()
        else:
            QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")

    def load_inventory_data(self):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            try:
                # Inventory 테이블에서 Product ID, 이름, 재고 수량 가져오기
                query = """
                    SELECT p.ProductID, p.ProductName, w.WarehouseID, w.WarehouseName, i.TotalQuantity 
                    FROM Inventory i
                    JOIN Product p ON i.ProductID = p.ProductID
                    JOIN WareHouse w ON i.WarehouseID = w.WarehouseID;
                """
                cursor.execute(query)
                results = cursor.fetchall()

                # SearchedDataField 초기화 (테이블을 비움)
                self.SearchedDataField.setRowCount(0)

                # 결과 출력
                for product_id, product_name, warehouse_id, warehouse_name, total_quantity in results:
                    # 새로운 행 추가
                    row_position = self.SearchedDataField.rowCount()
                    self.SearchedDataField.insertRow(row_position)

                    # 각 셀에 데이터 삽입
                    self.SearchedDataField.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
                    self.SearchedDataField.setItem(row_position, 1, QTableWidgetItem(product_name))
                    self.SearchedDataField.setItem(row_position, 2, QTableWidgetItem(str(warehouse_id)))
                    self.SearchedDataField.setItem(row_position, 3, QTableWidgetItem(warehouse_name))
                    self.SearchedDataField.setItem(row_position, 4, QTableWidgetItem(str(total_quantity)))

            except Exception as e:
                QMessageBox.warning(self, "오류", f"데이터 로드 실패: {str(e)}")
            finally:
                cursor.close()
                conn.close()
        else:
            QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")

    def search_inventory(self):
        category = self.SearchCategory.currentText()  # 선택된 카테고리
        keyword = self.SearchKeyword.toPlainText().strip()  # 입력된 키워드 (toPlainText 사용)

        if not keyword:
            # 키워드가 비어있으면 전체 재고 목록을 로드
            self.load_inventory_data()
            return

        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            try:
                # 테이블 초기화 (검색 전마다 테이블을 비움)
                self.SearchedDataField.setRowCount(0)

                if category == "상품이름":  # Product에서 검색
                    query = """
                        SELECT p.ProductID, p.ProductName, w.WarehouseID, w.WarehouseName, i.TotalQuantity
                        FROM Product p
                        JOIN Inventory i ON p.ProductID = i.ProductID
                        JOIN WareHouse w ON i.WarehouseID = w.WarehouseID
                        WHERE p.ProductName LIKE %s
                    """
                    cursor.execute(query, (f"%{keyword}%",))
                    results = cursor.fetchall()

                    if results:
                        for row in results:
                            product_id, product_name, warehouse_id, warehouse_name, total_quantity = row
                            # 새로운 행 추가
                            row_position = self.SearchedDataField.rowCount()
                            self.SearchedDataField.insertRow(row_position)

                            # 각 셀에 데이터 삽입
                            self.SearchedDataField.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
                            self.SearchedDataField.setItem(row_position, 1, QTableWidgetItem(product_name))
                            self.SearchedDataField.setItem(row_position, 2, QTableWidgetItem(str(warehouse_id)))
                            self.SearchedDataField.setItem(row_position, 3, QTableWidgetItem(warehouse_name))
                            self.SearchedDataField.setItem(row_position, 4, QTableWidgetItem(str(total_quantity)))

                elif category == "창고이름":  # Warehouse에서 검색
                    query = """
                        SELECT w.WarehouseID, w.WarehouseName, p.ProductID, p.ProductName, i.TotalQuantity
                        FROM WareHouse w
                        JOIN Inventory i ON w.WarehouseID = i.WarehouseID
                        JOIN Product p ON i.ProductID = p.ProductID
                        WHERE w.WarehouseName LIKE %s
                    """
                    cursor.execute(query, (f"%{keyword}%",))
                    results = cursor.fetchall()

                    if results:
                        for row in results:
                            warehouse_id, warehouse_name, product_id, product_name, total_quantity = row
                            # 새로운 행 추가
                            row_position = self.SearchedDataField.rowCount()
                            self.SearchedDataField.insertRow(row_position)

                            # 각 셀에 데이터 삽입
                            self.SearchedDataField.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
                            self.SearchedDataField.setItem(row_position, 1, QTableWidgetItem(product_name))
                            self.SearchedDataField.setItem(row_position, 2, QTableWidgetItem(str(warehouse_id)))
                            self.SearchedDataField.setItem(row_position, 3, QTableWidgetItem(warehouse_name))
                            self.SearchedDataField.setItem(row_position, 4, QTableWidgetItem(str(total_quantity)))

                # 결과가 없으면 안내 메시지
                if not results:
                    # row_position = self.SearchedDataField.rowCount()
                    # self.SearchedDataField.insertRow(row_position)
                    # self.SearchedDataField.setItem(row_position, 0, QTableWidgetItem("검색 결과가 없습니다."))
                    self.SearchedDataField.setRowCount(0)

            except Exception as e:
                QMessageBox.warning(self, "오류", f"검색 중 오류 발생: {str(e)}")
            finally:
                cursor.close()
                conn.close()
        else:
            QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")

    def initialize_tabs(self):
        # `Write` 권한이 없으면 InventoryControl, ProductRegistration 탭 비활성화
        if 'Write' not in self.user_authority:
            self.tabWidget.setTabEnabled(self.tabWidget.indexOf(self.InventoryControl), False)  # 재고 관리 탭
            self.tabWidget.setTabEnabled(self.tabWidget.indexOf(self.ProductControl), False)  # 상품 등록 탭

    def register_transaction(self):
        inventory_id = self.InventoryID.toPlainText().strip()
        quantity_text = self.Quantity.toPlainText().strip()
        transaction_type = self.TransactionType.currentText()
        warehouse_id = self.WarehouseID.toPlainText().strip()

        if transaction_type == "입고":
            transaction_type = "IN"
        elif transaction_type == "출고":
            transaction_type = "OUT"

        # 재고ID가 기존에 있으면 창고ID 올바른지 확인
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT WarehouseID FROM Inventory WHERE InventoryID = %s", (inventory_id,))
        result = cursor.fetchone()
        if result:
            if (result[0] != int(warehouse_id)):
                QMessageBox.warning(self, "기존 재고를 수정하기 위해서는 ", "창고ID를 맞춰야합니다.")
                return
        cursor.close()
        conn.close()

        # 입력값 유효성 검사
        if not inventory_id or not quantity_text:
            QMessageBox.warning(self, "", "입력 오류")
            return
        if not quantity_text.isdigit():
            QMessageBox.warning(self, "입력 오류", "수량은 숫자여야 합니다.")
            return
        quantity = int(quantity_text)

        # MySQL 연결
        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO InventoryTransaction (InventoryID, WarehouseID, UserID, TransactionType, Quantity)
                            VALUES (%s, %s, %s, %s, %s)""", 
                            (inventory_id, warehouse_id, self.user_id, transaction_type, quantity))

            conn.commit()
            QMessageBox.information(self, "성공", "재고 변동이 성공적으로 등록되었습니다.")
            self.load_transaction_data()  
            self.clear_inputs()
        except MySQLdb.Error as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"오류: {e}")
        finally:
            cursor.close()
            conn.close()

    def clear_inputs(self):
        """입력 필드 초기화"""
        self.InventoryID.clear()
        self.Quantity.clear()
        self.WarehouseID.clear()
        self.TransactionType.setCurrentIndex(0)

    def load_transaction_data(self):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            try:
                # InventoryTransaction 테이블에서 모든 데이터 가져오기
                query = """
                    SELECT TransactionID, InventoryID, WarehouseID, UserID, TransactionDate, TransactionType, Quantity
                    FROM InventoryTransaction
                    ORDER BY TransactionDate DESC;
                """
                cursor.execute(query)
                transactions = cursor.fetchall()

                # TransactionList 초기화
                self.TransactionList.setRowCount(0)  # 기존 데이터를 지웁니다.

                # 가져온 데이터를 테이블에 추가
                for row, transaction in enumerate(transactions):
                    # 각 행에 대해 데이터를 추가
                    self.TransactionList.insertRow(row)

                    for col, data in enumerate(transaction):
                        # 각 셀에 데이터를 추가
                        self.TransactionList.setItem(row, col, QTableWidgetItem(str(data)))

            except MySQLdb.Error as e:
                print(f"Error: {e}")
                QMessageBox.warning(self, "데이터 로드 실패", "변동사항을 로드하는데 실패했습니다.")
            finally:
                cursor.close()
                conn.close()
        else:
            QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")

    def register_product(self):
        # 입력값 가져오기
        product_name = self.ProductName.toPlainText().strip()
        product_description = self.ProductDescription.toPlainText().strip()
        unit_price_text = self.Unitprice.toPlainText().strip()

        # 유효성 검사
        if not product_name or not unit_price_text:
            QMessageBox.warning(self, "입력 오류", "모든 필드를 입력해 주세요.")
            return
        
        if not unit_price_text.isdigit():
            QMessageBox.warning(self, "입력 오류", "단가는 숫자여야 합니다.")
            return
        
        unit_price = int(unit_price_text)

        # MySQL 연결
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            try:
                # 제품 등록 쿼리 실행
                cursor.execute("""
                    INSERT INTO Product (ProductName, ProductDescription, Unitprice)
                    VALUES (%s, %s, %s)
                """, (product_name, product_description, unit_price))
                
                conn.commit()
                QMessageBox.information(self, "성공", "제품이 성공적으로 등록되었습니다.")
                
                # 제품 목록 새로고침
                self.load_product_data()
                self.clear_inputs()  # 입력 필드 초기화
            except MySQLdb.Error as e:
                QMessageBox.critical(self, "데이터베이스 오류", f"오류: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")

    def delete_product(self):
        # 선택된 제품을 가져오기
        selected_row = self.ProductTable.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "선택 오류", "삭제할 제품을 선택해 주세요.")
            return

        product_id = self.ProductTable.item(selected_row, 0).text()  # 첫 번째 열은 제품ID

        # 삭제 여부 확인
        reply = QMessageBox.question(
            self,
            "제품 삭제",
            f"선택한 제품 (ID: {product_id})을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # MySQL 연결
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()

                try:
                    # 제품 삭제 쿼리 실행
                    cursor.execute("DELETE FROM Product WHERE ProductID = %s", (product_id,))
                    conn.commit()

                    QMessageBox.information(self, "성공", "제품이 성공적으로 삭제되었습니다.")

                    # 제품 목록 새로고침
                    self.load_product_data()
                except MySQLdb.Error as e:
                    QMessageBox.critical(self, "데이터베이스 오류", f"오류: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")

    def load_product_data(self):
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()

            try:
                # 제품 데이터 로드 쿼리 실행
                cursor.execute("SELECT ProductID, ProductName, ProductDescription, UnitPrice FROM Product")
                products = cursor.fetchall()

                # 테이블 초기화
                self.ProductTable.setRowCount(0)

                # 제품 목록을 테이블에 추가
                for row, product in enumerate(products):
                    self.ProductTable.insertRow(row)
                    for col, data in enumerate(product):
                        self.ProductTable.setItem(row, col, QTableWidgetItem(str(data)))
            except MySQLdb.Error as e:
                QMessageBox.warning(self, "데이터 로드 실패", "제품 목록을 로드하는 데 실패했습니다.")
            finally:
                cursor.close()
                conn.close()
        else:
            QMessageBox.warning(self, "DB 연결 실패", "데이터베이스에 연결할 수 없습니다.")

    def clear_inputs(self):
        """입력 필드 초기화"""
        self.ProductName.clear()
        self.ProductDescription.clear()
        self.Unitprice.clear()







