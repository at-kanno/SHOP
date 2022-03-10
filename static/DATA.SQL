CREATE TABLE products (
	pid serial PRIMARY KEY,
	code VARCHAR ( 100 ) NOT NULL,
	name VARCHAR ( 100 ) NOT NULL,
	image VARCHAR ( 100 ) NOT NULL,
	category VARCHAR ( 50 ) NOT NULL,
	price INT NOT NULL,
	brand VARCHAR ( 100 ) NOT NULL,
	discount INT NOT NULL,
	width INT NOT NULL,
	height INT NOT NULL
);

INSERT INTO products(pid, code,name,image,category,price,brand,discount, width, height) VALUES
    (1,'00001','The Visible Ops Handbook（見える運用）','VO.jpg', '書籍', 3000, 'ITPI', 1000, 207, 293);
INSERT INTO products(pid, code,name,image,category,price,brand,discount, width, height) VALUES
    (2,'00002', 'ITILの基礎', 'ITIL3.jpg', '書籍', 2500, 'マイナビ出版', 1500, 207, 293);
INSERT INTO products(pid, code,name,image,category,price,brand,discount, width, height) VALUES
    (3,'00003', 'ＤＸ時代のサービスマネジメント', 'DX.jpg', '書籍', 2180, '技術評論社', 2000, 245, 346);



CREATE TABLE IF NOT EXISTS USER_TABLE
      (user_id INTEGER PRIMARY KEY,
      lastname TEXT, firstname TEXT, lastyomi TEXT, firstyomi TEXT,
      tel1 TEXT, tel2 TEXT, tel3 TEXT, zip1 TEXT, zip2 TEXT,
      company TEXT, department TEXT, prefecture TEXT, city TEXT,
      town TEXT, building TEXT, mail_adr TEXT, status INTEGER,
      password TEXT, stage INTEGER);



INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(1, "官野", "あつし", "かんの", "あつし", "048", "235", "4486", "351", "0035", "オリーブネット株式会社",
 "代表取締役", "埼玉県", "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "aaa", "kanno@olivenet.co.jp" );

UPDATE USER_TABLE SET PASSWORD = 'V+KzypVRAqRVKVnEUjIaE2uDCyRLdcMH+3N33/8o5R6+K3uW9AUicrOsJXrZH3oU' where user_id=1;

INSERT INTO USER_TABLE (user_id, lastname, firstname, lastyomi, firstyomi,
tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town, building,
status, password, mail_adr) VALUES
(2, "メール", "送信者", "メール", "そうしん", "048", "235", "4486", "351", "0035", "オリーブネット株式会社",
 "CIO", "埼玉県", "朝霞市", "朝志ヶ丘", "朝志ヶ丘ビルディング", 3, "ArkOliveNet2022", "itil4exercise@gmail.com" );


=============================
CREATE TABLE `product` (
  `pid` int(11) NOT NULL,
  `code` varchar(255) NOT NULL,
  `name` varchar(70) DEFAULT NULL,
  `image` varchar(255) NOT NULL,
  `category` varchar(70) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `discount` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`pid`, `code`, `name`, `image`, `category`, `price`, `discount`) VALUES
(3, 'EDNALAN01', 'Samsung Galaxy A10S', '2.jpg', 'Mobile', 520, 100),
(4, 'EDNALAN02', 'Samsung Galaxy Win Duos', '3.jpg', 'Mobile', 1600, 500),
(5, 'EDNALAN03', 'Women Summer Spaghetti Strap Down', '4.jpg', 'Woman Dresess', 2020, 1250),
(6, 'EDNALAN04', 'Honda TMX Alpha Clamp', '5.jpg', 'Motorcycle', 320, 50);

ALTER TABLE `product`
  ADD PRIMARY KEY (`pid`);

ALTER TABLE `product`
  MODIFY `pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=250;
COMMIT;
----------------------------------------------




