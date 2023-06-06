# -*- coding: utf-8 -*-
import time
import datetime
import string
import random
import string
import json
import threading
import traceback
from MScan import scan_test3 as scan
from django.views.decorators import csrf
from django.shortcuts import render,HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#认证模块
from django.contrib import auth
from django.shortcuts import redirect
# 对应数据库
from django.contrib.auth.models import User
# 装饰器，给需要登录成功后才能访问的页面统一加装饰器
from django.contrib.auth.decorators import login_required
from SenInfo import models


def login(request):
    if request.method == "GET":
        next_url = request.GET.get("next") or "/secplatform"
        print(next_url)
        return render(request, "login.html",{'next_url':next_url})

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next_url")
        user_obj = auth.authenticate(username=username, password=password)
        #print(user_obj.username)
        if not user_obj:

            return render(request, 'login.html', {'errmsg': '账号或密码不正确'})
        else:
            auth.login(request, user_obj)
            path = next_url or "/secplatform"
            print(path)
            return redirect(path)

def logout(request):
    ppp = auth.logout(request)
    print(ppp) # None
    return redirect("/login/")

def register(request):

    if request.method == "POST":
        username = request.POST.get("username2")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # if not username or not password or not password2:
        #     return render(request, 'login.html', {'register_msg': '请输入用户名或密码'})
        #
        # else:
        #     if password == password2:
        #
        #         try:
        #             User.objects.create_user(username=username, password=password)
        #             return render(request, 'login.html', {'register_msg': '注册成功'})
        #         except Exception as e:
        #             print(traceback.format_exc())
        #             return render(request, 'login.html', {'register_msg': '账号或密码输入格式有误'})
        #     else:
        #         return render(request, 'login.html', {'register_msg': '两次输入密码不一致'})

        if not username or not password or not password2:
            return HttpResponse("请输入用户名或密码")

        else:
            if password == password2:

                try:
                    User.objects.create_user(username=username, password=password)
                    return HttpResponse("注册成功")

                except Exception as e:
                    print(traceback.format_exc())
                    return HttpResponse("用户已存在或输入格式有误")

            else:
                return HttpResponse("两次输入密码不一致")


@login_required
def homepage(request):
    return render(request,"homepage.html")


@login_required
def createInfo(request):
    return render(request,"createInfo.html")


@login_required
def taskpage(request):

    task = models.Scaninfo.objects.all()
    #task = models.Scaninfo.objects.order_by("taskbegintime")
    task=task[::-1]
    paginator = Paginator(task, 10)
    currentPage = int(request.GET.get("id", 1))

    if paginator.num_pages > 15:
        if currentPage - 5 < 1:
            pageRange = range(1, 11)
        elif currentPage + 5 > paginator.num_pages:
            pageRange = range(currentPage - 5, paginator.num_pages)
        else:
            pageRange = range(currentPage - 5, currentPage + 5)
    else:
        pageRange = paginator.page_range

    try:
        task_list = paginator.page(currentPage)
    except PageNotAnInteger:
        task_list = paginator.page(1)
    except:
        task_list = paginator.page(paginator.num_pages)

    return render(request, "taskpage.html", {"task_list": task_list,
                                         "paginator": paginator,
                                         "page_range": pageRange,  # 此处自定义一个分页段
                                         "currentPage": currentPage})


@login_required
def taskinfo(request):

    taskid = request.GET['taskid']
    result = models.Scaninfo.objects.get(taskid=taskid)

    return render(request,"taskinfo.html",{"taskname": result.taskname,
                                        "starttime": result.starttime,
                                        "endtime": result.endtime,
                                        "Murl": result.Murl,
                                        "Auth_Token": result.Auth_Token,
                                        "cftk": result.cftk,
                                        "regex_str": result.regex_str,
                                        "appname": result.appname,
                                        "appid": result.appid
                                           })


@login_required
def copytask(request):
    taskid = request.POST.getlist('checkID[]')
    result = models.Scaninfo.objects.get(taskid=taskid[0])

    return render(request, "copytask.html", {"taskname": result.taskname,
                                             "starttime": result.starttime,
                                             "endtime": result.endtime,
                                             "Murl": result.Murl,
                                             "Auth_Token": result.Auth_Token,
                                             "cftk": result.cftk,
                                             "regex_str": result.regex_str,
                                             "appname": result.appname,
                                             "appid": result.appid
                                             })


@login_required
def taskdel(request):
    fullpath = request.META.get("HTTP_REFERER")
    # print(fullpath)
    # csrfmiddlewaretoken = request.POST.get('csrfmiddlewaretoken')
    # print(csrfmiddlewaretoken)
    dellist = request.POST.getlist('checkID[]')
    print(dellist)
    for i in dellist:
        models.Scaninfo.objects.filter(taskid=i).delete()

    return redirect(fullpath)

@login_required
def savetask(request):
    taskparam = {}
    if request.method == "POST":
        taskparam['starttime'] = request.POST['starttime']
        taskparam['endtime'] = request.POST['endtime']
        taskparam['Murl'] = request.POST['Murl']
        taskparam['Auth_Token'] = request.POST['Auth_Token']
        taskparam['cftk'] = request.POST['cftk']
        taskparam['regex_str'] = request.POST['regex_str']
        taskparam['taskname'] = request.POST['taskname']
        taskparam['appname'] = request.POST['appname']
        taskparam['appid'] = request.POST['appid']
        taskparam['taskbegintime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        taskparam['finishtime'] = ''
        taskparam['progress'] = ''
        taskparam['report'] = ''
        taskparam['taskid'] = ''.join(random.sample(string.ascii_letters + string.digits, 16))

        newtask = models.Scaninfo(taskid=taskparam['taskid'],
                                  taskname=taskparam['taskname'],
                                  appname=taskparam['appname'],
                                  appid=taskparam['appid'],
                                  starttime=taskparam['starttime'],
                                  endtime=taskparam['endtime'],
                                  Murl=taskparam['Murl'],
                                  Auth_Token=taskparam['Auth_Token'],
                                  cftk=taskparam['cftk'],
                                  regex_str=taskparam['regex_str'],
                                  taskbegintime=taskparam['taskbegintime'],
                                  finishtime=taskparam['finishtime'],
                                  progress=taskparam['progress'],
                                  report=taskparam['report'])

        newtask.save()

        # with open("taskinfo.json", "r+") as f:
        #     content = f.read()
        #     while len(content) == 0:
        #         with open("taskinfo.json", "r+") as f:
        #             content = f.read()
        #
        #     else:
        #         taskinfo = json.loads(content)
        #         with open("taskinfo.json", "w+") as f:
        #             taskinfo['data'].append(taskparam)
        #             #print(taskinfo)
        #             taskinfo_json = json.dumps(taskinfo)
        #             f.write(taskinfo_json)

        # 启动扫描线程
        scan1 = scan.scan_test3(**taskparam)
        thread_scan1 = threading.Thread(target=scan1.mscan)
        thread_scan1.start()
        print('启动扫描线程')

    #return taskpage(request)
    return redirect("/taskpage/")

