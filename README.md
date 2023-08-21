# 棲架資料庫管理系統

## Install

Developed under python 3.9.10.

git clone repository

```
git clone https://github.com/Chendada-8474/perch-mount-system.git
```

install packages

```
pip install -r requirements.txt
```

create two necessary config files


### Config for MySQL connection

create a .py file as `configs/mysql.py`

`mysql.py` allow a master slave architecture setting. If there is not  master slave architecture, set the variable as same.

```python
master_passward = "<master user password>"
master_user = "<master user name>"
master_ip = "<master host>"
master_port = "<master port>"

slave_passward = "<slave user password>"
slave_user = "<slave user name>"
slave_ip = "<slave host>"
slave_port = "<slave port>"

database = "perch_mount"
```

### Config for Path

create a .py file as `configs/path.py`

```python
MEDIA_ROOT = "your/media/root/dir"
TASKS_DIR_PATH = "your/shedule/detection/tasks/dir"
```


## Initialize Database

### Create Schema

create perch_mount database

```sql
mysql> CREATE DATABASE perch_mount;
```

create user

```sql
mysql> CREATE USER '<your user name>'@'hostname' IDENTIFIED BY '<your password>';
```

authorize database
```sql
mysql> GRANT ALL PRIVILEGES ON perch_mount.* TO '<your user name>'@'hostname';
```


## Run Server

## API Documentation

https://perchmount.docs.apiary.io/