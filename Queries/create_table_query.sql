CREATE TABLE User (
    UserID VARCHAR(64) NOT NULL PRIMARY KEY,      -- 사용자 ID
    Password VARCHAR(512) NOT NULL,               -- 비밀번호 (해시값 저장)
    Name VARCHAR(64) NOT NULL,                    -- 이름
    Email VARCHAR(128)                            -- 이메일
);

CREATE TABLE Roles (
    RoleID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 역할 ID 
    RoleName VARCHAR(64) NOT NULL                   -- 역할 이름
);

CREATE TABLE UserRoleMapping (
    UserRoleMappingID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 역할-사용자매핑
    RoleID INT NOT NULL,                 	    -- 역할 ID(외래 키)
    UserID VARCHAR(64) NOT NULL,			    -- 사용자 ID(외래 키)
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),   -- Role 테이블 참조
    FOREIGN KEY (UserID) REFERENCES User(UserID)    -- User 테이블 참조
);

CREATE TABLE Authority (
    AuthorityID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 권한ID
    AuthorityName VARCHAR(64) NOT NULL			 -- 권한 이름
);

CREATE TABLE RoleAuthorityMapping (
    RoleAuthorityMappingID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 역할-권한매핑
    RoleID INT NOT NULL,                 	    -- 역할 ID(외래 키)
    AuthorityID INT NOT NULL,			    -- 권한 ID(외래 키)
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID),   -- Role테이블 참조
    FOREIGN KEY (AuthorityID) REFERENCES Authority(AuthorityID)    -- Authority테이블 참조
);

CREATE TABLE WareHouse (
    WarehouseID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 창고ID
    WarehouseName VARCHAR(128) NOT NULL,		 -- 창고 이름
    WarehouseLocation VARCHAR(512) NOT NULL		 -- 창고 위치(주소)
);


CREATE TABLE Product (
    ProductID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 제품 ID (자동 증가)
    ProductName VARCHAR(64) NOT NULL,                  -- 제품 이름
    ProductDescription VARCHAR(512),                   -- 제품 정보
    UnitPrice INT NOT NULL                             -- 단가
);

CREATE TABLE Inventory (
    InventoryID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 재고ID
    TotalQuantity INT NOT NULL,				 -- 재고 총 수량
    WarehouseID INT NOT NULL,				 -- 창고ID
    ProductID INT NOT NULL,				 -- 제품ID
    FOREIGN KEY (WarehouseID) REFERENCES WareHouse(WarehouseID),  -- 창고 테이블 참조(외래 키)
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)	     -- 제품 테이블 참조(외래 키)
);

CREATE TABLE InventoryTransaction (
    TransactionID INT NOT NULL PRIMARY KEY AUTO_INCREMENT, -- 변동 ID 
    InventoryID INT NOT NULL,                              -- 재고 ID (외래 키)
    WarehouseID INT NOT NULL,				   -- 창고 ID (외래 키)
    UserID VARCHAR(64) NOT NULL,                           -- 사용자 ID (외래 키)
    TransactionDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 변동 날짜
    TransactionType ENUM('IN', 'OUT') NOT NULL,            -- 변동 유형
    Quantity INT NOT NULL,				   -- 수량
    FOREIGN KEY (InventoryID) REFERENCES Inventory(InventoryID),     -- 재고 테이블 참조
    FOREIGN KEY (UserID) REFERENCES User(UserID),          -- 사용자 테이블 참조
    FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID)  -- 창고 테이블 참조
);
