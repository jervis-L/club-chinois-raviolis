from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
# MDN的表单教学里面的例子也不错
# 这里并没有将form作为参数传入，而是将请求的数据(request.POST)建立一个form对象,
# 主要功能只用了cleaned_data,以及后面建了一个form的实例，用来update,以及填入的新的quantity
@login_required
@require_http_methods(["GET", "POST"])
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        # 返回自身
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_remove_all(request):
    cart=Cart(request)
    cart.remove_all()
    return redirect('cart:cart_detail')
    
@login_required
def cart_detail(request):
    cart = Cart(request)
    # 使用 for in 的时候迭代,并call `__iter__`
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update': True
            })
    return render(request, 'cart/detail.html', {'cart': cart})
