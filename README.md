# 技术背景

1. [redis](https://www.runoob.com/redis/redis-tutorial.html)


# 系统环境搭建

## Windows

### Mysql 服务器搭建

- 参见[菜鸟教程](https://www.runoob.com/mysql/mysql-install.html)

安装完毕后登录 mysql 修改初始密码，同时在安装的mysql目录下新建一个 my.ini 配置文件，在其中配置内容如下：

```text
[client]
# 设置mysql客户端默认字符集
default-character-set=utf8mb4
[mysqld]
# 设置3306端口
port=3306
# 设置mysql的安装目录
basedir=D:\\mysql-8.0.11
# 允许最大连接数
max_connections=20
# 服务端使用的字符集默认为8比特编码的latin1字符集
character-set-server=utf8mb4
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
```

> 这一步相当重要，决定了客户端和服务器的字符集设置，本系统采用 utf-8mb4 字符集，务必确保字符集相同。


```mysql
ALTER USER 'username'@'localhost' IDENTIFIED BY 'hhy2345678';
```

创建一个数据库 `fba`，选择 utf8mb4 编码
 
   ```sql
   CREATE DATABASE fba CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
   
注入初始数据：



> 注意：可能需要以管理员权限执行安装步骤

### Redis 服务器搭建

- 参见[菜鸟教程](https://www.runoob.com/redis/redis-install.html)

