from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from cart.forms import CartAddProductForm
from .models import Category, Product

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .oauth_client import *
import uuid
from users.models import User

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, product_id, slug):
    product = get_object_or_404(Product,
                                id=product_id,
                                slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

def login_user(request, user):
    #设置backend，直接登录，绕开authenticate验证
    # user.backend='django.contrib.auth.backends.ModelBackend'
    # 认证源是以会话为基础的,login向session中添加SESSION_KEY, 便于对用户进行跟踪:
    # @login_required修饰器修饰的view函数会先通过session key检查是否登录, 
    # 已登录用户可以正常的执行操作, 未登录用户将被重定向到login_url指定的位置
    # logout会移除request中的user信息, 并刷新session:
    setattr(user, 'backend', 'django.contrib.auth.backends.ModelBackend')
    login(request, user)

# 这里对应redirect-url
def viarezo_check(request):
    request_code=request.GET.get('code')
    if request_code:
        # state = request.GET.get('state')
        oauth_v=oauth_viarezo()
        access_token = oauth_v.get_access_token(request_code)
        # 如何验证request.session存在？
        # 如果要验证存在的必须销毁，因为access_token会过期，
        # 一次验证。似乎session可以保证一直登录着，怎么做到？
        # request.session['access_token']=access_token
        # request.session['username']=oauth_v.get_user_name(access_token)
        username=oauth_v.get_user_name()
        users=User.objects.filter(username=username)
        if users:
            login_user(request,users[0])
        else :
            # 只有用户名可以创建用户吗？
            user=User.objects.create(username=username)
            # 验证后取得信息，原有框架下仍需要密码才能登录，所以要么设置表单，
            # 要么就随便生成密码，只要验证后名字对上数据库就够了，像hyris那样
            # 密码随后设为生日？
            pwd = str(uuid.uuid1()) #生成随机密码
            user.set_password(pwd)
            user.is_active = True
            user.save()
            login_user(request,user)
        return redirect(reverse('shop:product_list'))
    else:
        return redirect(reverse('shop:product_list'))
