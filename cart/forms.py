from django import forms
# Form 的声明语法，与声明Model非常相似，并且共享相同的字段类型
# 这里可以设置数量选项为10的倍数,步长为10就行
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 100)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
