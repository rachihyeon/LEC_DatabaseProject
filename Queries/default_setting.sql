CREATE VIEW UserInfoView AS
SELECT 
    u.UserID,           -- 사용자 ID
    u.Name,             -- 사용자 이름
    r.RoleName,         -- 역할 이름
    a.AuthorityName     -- 권한 이름
FROM 
    User u
JOIN 
    UserRoleMapping urm ON u.UserID = urm.UserID
JOIN 
    Roles r ON urm.RoleID = r.RoleID
JOIN 
    RoleAuthorityMapping ram ON r.RoleID = ram.RoleID
JOIN 
    Authority a ON ram.AuthorityID = a.AuthorityID;
    
    
DELIMITER $$

CREATE TRIGGER UpdateInventoryAfterTransaction
BEFORE INSERT ON InventoryTransaction
FOR EACH ROW
BEGIN
    DECLARE current_quantity INT;
    
    SELECT TotalQuantity INTO current_quantity
    FROM Inventory
    WHERE InventoryID = NEW.InventoryID;
    
    IF NEW.TransactionType = 'OUT' AND (current_quantity - NEW.Quantity) < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '수량이 음수가 될 수 없습니다. 트랜잭션을 취소합니다.';
    ELSE
        IF NEW.TransactionType = 'IN' THEN
            UPDATE Inventory
            SET TotalQuantity = TotalQuantity + NEW.Quantity
            WHERE InventoryID = NEW.InventoryID;
        ELSEIF NEW.TransactionType = 'OUT' THEN
            UPDATE Inventory
            SET TotalQuantity = TotalQuantity - NEW.Quantity
            WHERE InventoryID = NEW.InventoryID;
        END IF;
    END IF;
END$$

DELIMITER ;