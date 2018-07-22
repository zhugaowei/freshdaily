from django.shortcuts import render, redirect, HttpResponse
from hashlib import sha1
from .models import *
from df_goods.models import *
from django.http import JsonResponse, HttpResponseRedirect
from . import user_decorator

# Create your views here.
def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    #接受用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    #判断两次输入的密码
    if upwd != upwd2:
        return redirect('/user/register/')
    #密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf8"))
    upwd3 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功，转到登录页
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GRT.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

# def login_handle(request):
#     """处理登录请求"""
#     post = request.POST
#     uname = post.get('username')
#     upwd = post.get('pwd')
#     re_pwd = post.get('remember_pwd', 0)
#
#     # 数据表查询
#     users = UserInfo.objects.filter(uname=uname)  # []
#     if len(users) == 1:
#         s1 = sha1()
#         s1.update(upwd.encode("utf8"))
#         if s1.hexdigest() == users[0].upwd:
#             res = HttpResponseRedirect('/user/info/')
#
#             # 记住用户名密码
#             if re_pwd != 0:
#                 res.set_cookie('uname', uname)
#             else:
#                 res.set_cookie('uname', '', max_age=-1)
#             request.session['user_id'] = users[0].id  # 可以直接通过id号查信息
#             request.session['user_name'] = uname  # 很多页面用到姓名
#             return res
#         else:
#             context = {
#                 'title': '用户登录',
#                 'error_name': 0,
#                 'error_pwd': 1,
#                 'uname': uname,
#                 'upwd': upwd
#             }
#             return render(request, 'user/login.html', context)
#     else:
#         context = {
#             'title': '用户登录',
#             'error_name': 1,
#             'error_pwd': 0,
#             'uname': uname,
#             'upwd': upwd
#         }
#         return render(request, 'user/login.html', context)
def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    #根据用户名查询对象
    # user = UserInfo.objects.filter(uname=uname)
    # print(uname)
    #判断：如果未查到在用户名错，如果查到再判断密码是否正确，正确则转到用户中心
    user = UserInfo.objects.filter(uname=uname)  # []
    if len(user) == 1:
        s1 = sha1()
        print(1)
        s1.update(upwd.encode("utf8"))
        if s1.hexdigest() == user[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            if jizhu!=0:
                red.set_cookie('uname',uname)
                print(3)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            print(2)
            print(request.session['user_name'])
            return red
        else:
            print('1')
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        print('2')
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

@user_decorator.login
def info(request):

    user_email = UserInfo.objects.get(id = request.session['user_id']).uemail
    #最近浏览
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    if goods_ids != '':
        goods_ids = goods_ids.split(',')
        for goods_id in goods_ids:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    user = UserInfo.objects.get(id=request.session['user_id'])
    goods = GoodsInfo()
    context = {
        'title':'用户中心',
        'user':user,
        'goods_list':goods_list,
    }
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request):
    context={'title':'用户中心'}
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id = request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context={'tiele':'用户中心','user':user}
    return render(request,'df_user/user_center_site.html',context)


def logout(request):
	request.session.flush()
	return redirect('/user/login/')

# def logout(request):
#     request.sission.flush()
#     return redirect('/')