from django.conf.urls import url
from . import views
app_name='orders'
urlpatterns = [
        url(r'^create/$',views.order_create,name='order_create'),
        url(r'^check_orders/$',views.check_orders,name='check_orders'),
        url(r'^check_orders/orders_(?P<order_id>\d+)/$',views.order_detail,name='order_detail'),
        url(r'^create/order_confirm/$',views.order_confirm,name='order_confirm'),
        url(r'^create/order_cancel/$',views.order_cancel,name='order_cancel'),
        url(r'^check_orders/orders_(?P<order_id>\d+)/order_remove/$',views.order_remove,name='order_remove')
]