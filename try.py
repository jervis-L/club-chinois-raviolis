# yield是生成器（特殊迭代器）（generator）的一部分（带yield的函数才是真正的迭代器）
# generator有next方法，含有__next__()函数对象的都是一个迭代器
# 这一次的next开始的地方是接着上一次的next停止的地方执行的，所以调用next的时候，生成器并不会从foo函数的开始执行，
# 只是接着上一步停止的地方开始，然后遇到yield后，return出要生成的数，此步就结束
# https://blog.csdn.net/mieleizhi0522/article/details/82142856
def func():
    for i in range(0,3):
        yield i
f=func()
print(next(f))
print(next(f))
print(next(f))
# print(next(f))

# __iter__,生成可迭代的对象,必须配合next使用
# 有__next__,循环调用next方法
# https://blog.csdn.net/wangweiwells/article/details/96497148?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-6.control&dist_request_id=1329188.12604.16178943779969099&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-6.control
class test():
    def __init__(self,data=1):
        self.data = data

    def __iter__(self):
        return self
    def __next__(self):
        if self.data > 5:
            raise StopIteration
        else:
            self.data+=1
            return self.data

for item in test(3):
    print(item)
import os
os.environ['ID']=''
del os.environ['ID']
# <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
# dbOTQV2C59d7pmSwJFM60cehcOYQtr3CBJf3W1q3
# oehabIC0QrhsEm6p4mygYU5dke3nH65wqgQnr1vqtZxQR62eaKoJ4RoWwNGzXOvweLIwF9pTA84ixdUPWxYOsgy7ZJFajjlORW5cEAlVf8Rf7wo8lsXZn9XPPl1zZ2Gx