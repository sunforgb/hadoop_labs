customers = LOAD 'warehouse/customers/000000_0' USING PigStorage(',') AS (id:int, email:chararray, hash:chararray);
cart = LOAD 'warehouse/cart/000000_0' USING PigStorage(',') as (id:int, customer:int, good:int, count:int);
goods = LOAD 'warehouse/goods/000000_0' USING PigStorage(',') as (id:int, name:chararray, price:int);
goods_shops = LOAD 'warehouse/goods_shops/000000_0' USING PigStorage(',') as (id:int, shop:int, good:int);
shops = LOAD 'warehouse/shops/000000_0' USING PigStorage(',') as (id:int, name:chararray);

tmp = JOIN customers by id, cart by customer;
tmp_2 = foreach tmp generate customers::email as email, cart::good as good_id, cart::count as count;
tmp_3 = JOIN tmp_2 by good_id, goods by id;

query_result_1 = foreach tmp_3 generate tmp_2::email as email, tmp_2::count as count, goods::name as name;

tmp = JOIN goods by id, goods_shops by good;
tmp_2 = foreach tmp generate goods::name as good_name, goods_shops::shop as shop;
tmp_3 = JOIN tmp_2 by shop, shops by id;

query_result_2 = foreach tmp_3 generate tmp_2::good_name as good_name, shops::name as shop_name;

tmp = JOIN shops by id, goods_shops by shop;
tmp_2 = foreach tmp generate FLATTEN(shops::name) as shop_name, FLATTEN(goods_shops::good) as good_id;
tmp_3 = JOIN tmp_2 by good_id, goods by id;
tmp_4 = foreach tmp_3 generate FLATTEN(tmp_2::shop_name), FLATTEN(goods::name) as good_name, FLATTEN(goods::price) as good_price;
tmp_5 = GROUP tmp_4 by shop_name;
query_result_3 = foreach tmp_5 generate group, SUM(tmp_4.good_price) as all_sum;


tmp = JOIN customers by id, cart by customer;
tmp_2 = foreach tmp generate FLATTEN(customers::email) as email, FLATTEN(cart::good) as good_id, FLATTEN(cart::count) as good_count;
tmp_3 = JOIN tmp_2 by good_id, goods by id;
tmp_4 = foreach tmp_3 generate FLATTEN(tmp_2::email) as email, FLATTEN (tmp_2::good_count * goods::price) as multiply;
tmp_5 = GROUP tmp_4 by email;
query_result_4 = foreach tmp_5 generate group, SUM(tmp_4.multiply);

tmp = join goods by id, goods_shops by good;
tmp_2 = foreach tmp generate goods::name as good_name, goods::price as price, goods_shops::shop as shop_id;
tmp_3 = join tmp_2 by shop_id, shops by id;
query_result_5 = foreach tmp_3 generate tmp_2::good_name, tmp_2::price, shops::name;

STORE query_result_1 INTO 'pigresult/query_result_1';
STORE query_result_2 INTO 'pigresult/query_result_2';
STORE query_result_3 INTO 'pigresult/query_result_3';
STORE query_result_4 INTO 'pigresult/query_result_4';
STORE query_result_5 INTO 'pigresult/query_result_5';
quit

