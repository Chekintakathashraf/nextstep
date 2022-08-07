from django import forms
from .models import Coupon

class CouponForm(forms.ModelForm):

    class Meta:

        model = Coupon
        fields = ['coupon_code', 'quantity', 'amount']

    def _init_(self, *args, **kwargs):
        super(CouponForm, self)._init_(*args, **kwargs)
        self.fields['coupon_code'].widget.attrs['placeholder']   = 'Enter coupon code'
        self.fields['quantity'].widget.attrs['placeholder']      = 'Enter quantity of coupon'
        self.fields['amount'].widget.attrs['placeholder']        = 'Enter amount of coupon'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'