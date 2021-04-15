from django.conf import settings

from shop.models import Product

# sessions 的使用和 python 中的字典是类似的,中文名:会话,大概与客户关系的状态
# 如何使用会话/使用Django的认证系统 MDN的django教程以及django官方文档
class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        会话先传给客户端，处理过后再链接到会话,总之分不开，可视为一个不可分割整体的部分
        """
        self.session = request.session
        # settings.CART_SESSION_ID是一个字符串，即key,也可以通过字典的['']方式来得到
        # self.cart={'product_id':{'quantity':0,'price'=1}}是一个嵌套的字典
        # 经过__iter__方法, self.cart={'product_id':{'product':product,'quantity':0,'price'=1,'total_price':}}
        # 调用self.cart,返回其中的values，即一个字典
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def remove_all(self):
        cart=self.session[settings.CART_SESSION_ID] = {}
        self.cart=cart
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        这样一来 self.cart直接是一个可遍历对象
        返回的是处理过的self.cart.values()
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        # 因为product_ids有很多，所以filter用id__in
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        # 在 ./shop/templates/shop/base.html 的 {% with total_items=cart|length %}
        # 会被call
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


