-- 계정등록
INSERT INTO user values('admin', '1234', 'CHIHYEON', 'chi-hyeon@dongguk.edu');
INSERT INTO user values('visitor', '1234', 'CHIYOONG', 'Hello@dongguk.edu');

-- 역할 등록
INSERT INTO Roles values(NULL, 'Normal');
INSERT INTO Roles values(NULL, 'Manager');
INSERT INTO Roles values(NULL, 'Administrator');

-- 권한 등록
INSERT INTO Authority values(NULL, 'Read');
INSERT INTO Authority values(NULL, 'Write');
INSERT INTO Authority values(NULL, 'Delete');

-- 역할별 권한 등록
INSERT INTO Roleauthoritymapping values(NULL, 1, 1);
INSERT INTO Roleauthoritymapping values(NULL, 2, 1);
INSERT INTO Roleauthoritymapping values(NULL, 2, 2);
INSERT INTO Roleauthoritymapping values(NULL, 3, 1);
INSERT INTO Roleauthoritymapping values(NULL, 3, 2);
INSERT INTO Roleauthoritymapping values(NULL, 3, 3);

-- 사용자에게 권한 부여
INSERT INTO userrolemapping values(NULL, 3, 'admin');
INSERT INTO userrolemapping values(NULL, 1, 'visitor');

-- 창고 등록
INSERT INTO Warehouse values(NULL, "창고A", "서울특별시 마포구");
INSERT INTO Warehouse values(NULL, "창고B", "충청북도 제천시");

-- 제품 등록
INSERT INTO Product values (NULL, '포카칩', '아주 맛있음', 1000);
INSERT INTO Product values (NULL, '라면', '매우 맛있음', 900);
INSERT INTO Product values (NULL, '세제', '못먹는 것', 10000);

-- 재고 등록
INSERT INTO Inventory values (NULL, 10, 1, 1);

-- 재고 입출고
INSERT INTO InventoryTransaction values (NULL, 6, 1, 'admin', CURRENT_TIMESTAMP, 1, 10);


INSERT INTO InventoryTransaction(InventoryID, WarehouseID, UserID, TransactionType, Quantity) VALUES (6, 1, "admin", "IN", 5);
INSERT INTO InventoryTransaction(InventoryID, WarehouseID, UserID, TransactionType, Quantity) VALUES (6, 1, "admin", "OUT", 16);