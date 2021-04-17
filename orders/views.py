from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from cart.cart import Cart
from .models import OrderItem,Order
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request):
    cart = Cart(request)
    # 如果不clear就会报奇怪的错,无法序列化product对象，但在cart自己的视图中就没什么影响，
    # cart里调用以后都会修改session, session['cart']链接到创建的cart了,不然没有办法传递参数
    # cart.clear()
    # request.session['order_id']=order.id
    # cart.save()
    # request.session.modified=True
    # redirect to the payment
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart})

def order_cancel(request):
    return redirect(reverse('cart:cart_detail'))

def order_confirm(request):
    cart=Cart(request)
    current_user=request.user
    if cart.get_total_price()>0:
        order = Order.objects.create(username=current_user.username)
        for item in cart:
            OrderItem.objects.create(order=order,
                                    product=item['product'],
                                    price=item['price'],
                                    quantity=item['quantity'])
        cart.clear()
        # 如果只得到一个似乎要用get，不然报错,但可能返回两个
        # 所以要用filter,然后取第一个对象
        orders= OrderItem.objects.filter(order=order)
        return render(request,'orders/order/order_detail.html',{'order':order,'orders':orders})
    else:
        return redirect('shop:product_list')
        
def check_orders(request):
    # 没有order的时候不能check_order,写个装饰器？还是有一个None页面
    # 如果先cancel再check_order,因为session_id已经写入，但是没有确定，所以没有加入数据库中
    current_user=request.user
    orders=Order.objects.filter(username=current_user.username)
    if orders:
        order_c=orders[0]
        orders=orders.exclude(id=order_c.id)
    else:
        order_c=None
    return render(request,'orders/order/check_orders.html',{'order_c':order_c,'orders':orders})

def order_detail(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    orders=OrderItem.objects.filter(order=order)
    return render(request,'orders/order/order_detail.html',{'order':order,'orders':orders})

def order_remove(request,order_id):
    order=get_object_or_404(Order,id=order_id)
    order.delete()
    return redirect(reverse('orders:check_orders'))