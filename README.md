# 棲架資料庫管理系統

## Install

Developed under python 3.9.10.

git clone repository

```
git clone https://github.com/Chendada-8474/perch-mount-system.git
```

install package

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
master_port = <master post>

slave_passward = "<slave user password>"
slave_user = "<slave user name>"
slave_ip = "<slave host>"
slave_port = <slave post>

database = "perch_mount"
```


### Config for Path

create a .py file as `configs/path.py`

```python
MEDIA_ROOT = "your/media/root/dir"
TASKS_DIR_PATH = "your/shedule/detection/tasks/dir"
```


## API Documentation

https://perchmount.docs.apiary.io/#reference/0/12