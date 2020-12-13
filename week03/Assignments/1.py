# 在 Linux 环境下，安装 MySQL5.6 以上版本，修改字符集为 UTF8mb4 并验证，新建一个数据库 testdb，并为该数据库增加远程访问的用。

# 将修改字符集的配置项、验证字符集的 SQL 语句作为作业内容提交
SET character_set_client = utf8mb4 ;
show variables like '%character%';

# 将增加远程用户的 SQL 语句作为作业内容提交
grant all privileges on *.* to test_user@localhost identified by 'test_passwd' with grant option;
grant all privileges on *.* to test_user@"%" identified by 'test_passwd' with grant option;
