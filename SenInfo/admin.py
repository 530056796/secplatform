from django.contrib import admin
from SenInfo.models import Scaninfo

# Register your models here.

class ControlScaninfo(admin.ModelAdmin):
    #自定义表在admin管理后台的数据列表展示页面里展示哪几个表字段内容，需要重写属性list_display
    # 重写属性list_display，来设置展示的表字段
    list_display = (
    'taskid', 'taskname', 'appname', 'appid', 'starttime', 'endtime', 'Murl', 'Auth_Token', 'cftk', 'regex_str',
    'taskbegintime', 'finishtime', 'progress', 'report')

    # 重写属性search_fields，把表字段name的值当做搜索条件
    search_fields = ("taskname",)

#注册该数据模型到 admin
admin.site.register(Scaninfo,ControlScaninfo)
