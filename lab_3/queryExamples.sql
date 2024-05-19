-- вывести все заказы пользователей из общей корзины
SELECT * from customers JOIN cart on customers.id==cart.customer JOIN goods on cart.good==goods.id;
-- вывести все товары в магазинах
SELECT * from goods JOIN goods_shops on goods.id==goods_shops.good JOIN shops on goods_shops.shop==shops.id;
-- вывести общую цену всех товаров для каждого магазина
SELECT name, sum(goods.price) as goods_cost from shops join goods_shops on goods_shops.shop = shops.id join goods on goods.id = goods_shops.good group by shops.name;
-- вывести обшую стоимость товаров для пользователя
SELECT email, sum(goods.price * cart.count) as goods_cost from customers join cart on cart.customer = customers.id join goods on goods.id = cart.good group by customers.email;
-- Вывести товары и цену в магазинах
SELECT goods.name, goods.price, shops.name from goods join goods_shops on goods.id = goods_shops.good join shops on shops.id = goods_shops.shop; 