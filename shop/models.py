from django.urls import reverse
from django.db import models

# 模型的元数据，指的是“除了字段外的所有内容”，例如排序方式、数据库表名、
# 人类可读的单数或者复数名等等。所有的这些都是非必须的，甚至元数据本身对模型也是非必须的。
# 可以添加约束，constraints等等
class Category(models.Model):
    # 应该设置unique的
    name = models.CharField(max_length=200,
                            db_index=True)
    #slug由数字字母下划线组成，用在url中 
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)
    # Django 模型类的Meta是一个内部类，它用于定义一些Django模型类的行为特性
    # ordering排序方式， verbose name可读性高的名字
    class Meta:
        ordering = ('-name',)
        verbose_name = 'category'
        # 默认的是直接加s
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    # 通过self.slug反查url
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])



class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',on_delete=models.CASCADE,default='猪肉饺子')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    quantity_unit= models.CharField(max_length=200,default="50P")
    description = models.TextField(blank=True)
    price = models.FloatField()
    dt_info = models.CharField(max_length=200,default="None")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
