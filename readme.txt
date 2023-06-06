1、下载完结包并解压--》pycharm打开项目--》创建虚拟环境-进入虚拟环境--》安装依赖库
pip install -r requirements.txt


2、初始化数据库（推荐新方法）
```
python manage.py migrate
```

3、创建管理员账户
在初始化完数据库之后，需要创建一个管理员账户来管理整个MrDoc，在项目路径下打开命令行终端，运行如下命令：:

```
 python manage.py createsuperuser
```
按照提示输入用户名、电子邮箱地址和密码即可。

4、启动运行
在完成上述步骤之后，即可运行使用。

方法1：在测试环境中，可以使用Django自带的服务器运行，其命令为：` python manage.py runserver`:
方法2：进到项目下直接start.bat启动



3、退出
Ctrl+C
venv\Scripts\deactivate.bat