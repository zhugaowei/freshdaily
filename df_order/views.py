from django.shortcuts import render,redirect,HttpResponse
# from django.http import HttpResponse
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import *
from .models import *
from django.db import transaction
from datetime import datetime
from decimal import Decimal

# Create your views here.
def order(request):
    # 查询用户对象
    print(1)
    user = UserInfo.objects.get(id = request.session['user_id'])
    print(2)
    # 查询勾选的商品信息
    print(user)
    # print()
    a=request.GET.get('cart_id')
    print(a)

    get = request.GET
    cart_ids = get.getlist('cart_id')

    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    print(cart_ids)
    context = {'title':'提交订单',
               'carts':carts,
               'user':user,
               'cart_ids':','.join(cart_ids),
               }
    print(carts)
    return render(request,'df_order/place_order.html',context)


'''
事务：一旦操作失败则全部回退
1、创建订单对象
2、判断商品的库存
3、创建详单对象
4、修改商品库存
5、删除购物车
'''
@transaction.atomic
@user_decorator.login
def order__handle(request):
    print('haha')
    tran_id = transaction.savepoint()
    cart_ids = request.POST.get('cart_ids')
    try:
        #创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '{}{}'.format(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        order.odate = now
        print(request.POST.get('address'))
        order.oaddress = request.POST.get('address')
        order.ototal = 0
        order.save()
        #创建详单信息
        # 创建详单对象
        cart_ids = [int(item) for item in cart_ids.split(',')]
        print (cart_ids)
        total = 0
        for id1 in cart_ids:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询购物信息
            cart = CartInfo.objects.get(id=id1)
            # 库存
            goods = cart.goods
            if goods.gkuncun >= cart.count:
                goods.gkuncun = cart.goods.gkuncun - cart.count
                goods.save()
                # 完善详单信息
                detail.goods_id = goods.id  # 做聚合查询

                price = goods.gprice
                detail.price = price
                count = cart.count

                detail.count = count
                detail.subtotal = price * count
                detail.save()
                total = total + price * count
                cart.delete()
            else:  # 如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)  # 失败回滚
                return redirect('/cart/')
                # 保存总价
        if total > 88:
            order.ototal = total
        else:
            order.ototal = total + 10
        order.save()
        transaction.savepoint_commit(tran_id)  # 提交事务
    except Exception as e:
        print ('================%s' % e)
        transaction.savepoint_rollback(tran_id)
    return redirect('/user/order/1/')
    # return render(request,'df_user/user_center_order.html',context)