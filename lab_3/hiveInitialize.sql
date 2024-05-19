CREATE TABLE customers(id int, email string, hash string) ROW FORMAT DELIMITED FIELDS TERMINATED by ',' stored as textfile;
CREATE TABLE cart(id int, customer int, good int, count int) ROW FORMAT DELIMITED FIELDS TERMINATED by ',' stored as textfile;
CREATE TABLE goods(id int, name string, price int) ROW FORMAT DELIMITED FIELDS TERMINATED by ',' stored as textfile;
CREATE TABLE goods_shops(id int, shop int, good int) ROW FORMAT DELIMITED FIELDS TERMINATED by ',' stored as textfile;
CREATE TABLE shops(id int, name string) ROW FORMAT DELIMITED FIELDS TERMINATED by ',' stored as textfile;

INSERT INTO customers(id, email, hash) values(1, "test@test.com", "aaa"), 
                                            (2, "qwe@qwe.com", "bbb"), 
                                            (3, "asd@asd.com", "ccc");

INSERT INTO shops(id, name) values (1, "Magnit"), (2, "ASHAN"), (3, "Fix Price");

INSERT INTO goods(id, name, price) values (1, "Apple", 10), (2, "Cucumber", 20), 
                                        (3, "Banana", 30), (4, "Orange", 25), 
                                        (5, "Mango", 70), (6, "Peach", 45), 
                                        (7, "Lemon", 5), (8, "Kiwi", 75), 
                                        (9, "Pear", 15), (10, "Pineapple", 100);
-- MAGNIT solds Apples, Cucumber, Banana, Orange
-- ASHAN solds MANGO, PEACH, LEMON, APPLE
-- Fix Price solds KIWI, PEAR, Pineapple, Banana
INSERT INTO goods_shops(id, shop, good) values (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), 
                                                (5, 2, 5), (6, 2, 6), (7, 2, 7), (8, 2, 1), 
                                                (9, 3, 8), (10, 3, 9), (11, 3, 10), (12, 3, 3);

-- test bought apples, mango, kiwi, lemon
-- qwe bought cucumber, peach, pear, pineapple
-- asd bought banana, orange, apple, mango
INSERT INTO cart (id, customer, good, count) VALUES (1, 1, 1, 5), (2, 1, 5, 6), (3, 1, 8, 10), (4, 1, 7, 2), 
                                                    (5, 2, 2, 10), (6, 2, 6, 3), (7, 2, 9, 4), (8, 2, 10, 15), 
                                                    (9, 3, 3, 15), (10, 3, 4, 6), (11, 3, 1, 5), (12, 3, 5, 8);
SELECT * from customers;
SELECT * from shops;
SELECT * from goods;
SELECT * from goods_shops;
SELECT * from cart;

