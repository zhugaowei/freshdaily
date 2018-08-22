from django.shortcuts import render, redirect
from django.http import JsonResponse
from df_user import user_decorator
from .models import *

# Create your views here.
@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'page_name': 1,
        'carts': carts,
    }
    return render(request,'df_cart/cart.html',context)

@user_decorator.login
def add(requset,gid,count):
    uid = requset.session['user_id']
    gid = int(gid)
    count = int(count)
    #查询购物车中是否已经有此商品，如果有则数量加一，如果没有则新增
    carts = CartInfo.objects.filter(user_id = uid,goods_id = gid)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count+count
    else:
         cart = CartInfo()
         cart.user_id = uid
         cart.goods_id = gid
         cart.count = count
    cart.save()
    if requset.is_ajax():
        count=CartInfo.objects.filter(user_id=requset.session['user_id']).count()
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/')

@user_decorator.login
def edit(requset,cart_id,count):
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        count1 = count
        cart.count = count
        cart.save()
        data = {'ok':0}
    except Exception as e:
        data = {'ok':count1}
        # print(11 )
    return JsonResponse(data)

def delete(request,id):
    try:
        cart = CartInfo.objects.get(pk = id)
        cart.delete()
        data = {'ok':1}
    except Exception as e:
        data = {'ok':0}
    return JsonResponse(data)

