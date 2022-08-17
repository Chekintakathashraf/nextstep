from category . models import category
from django import forms
from store . models import Product
from store . models import Variation
from . models import Carousel

class CategoryForm(forms.ModelForm):
    cat_image = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
    class Meta:
        model  = category
        fields = ['category_name','description','cat_image']

    def __init__(self,*args,**kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)

        # self.fields['main_category'].widget.attrs['class']='form-control form-control-user'

        self.fields['category_name'].widget.attrs['placeholder']='Enter Category name'
        self.fields['category_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['category_name'].widget.attrs['type']='text'

        self.fields['description'].widget.attrs['placeholder']='Enter Category discription'
        self.fields['description'].widget.attrs['class']='form-control form-control-user'
        self.fields['description'].widget.attrs['type']='text'
        self.fields['description'].widget.attrs['row']=3


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False, error_messages = {'invalid':("image files only")}, widget=forms.FileInput)
    class Meta:
        model = Product
        fields = ['product_name','describtion','price','is_available','stock','category','image']

    def __init__(self,*args,**kwargs):
        super(ProductForm,self).__init__(*args,**kwargs)

        self.fields['product_name'].widget.attrs['placeholder']='Enter Product name'
        self.fields['product_name'].widget.attrs['class']='form-control form-control-user'
        self.fields['product_name'].widget.attrs['type']='text'

        self.fields['describtion'].widget.attrs['placeholder']='Enter Product discription'
        self.fields['describtion'].widget.attrs['class']='form-control form-control-user'
        self.fields['describtion'].widget.attrs['type']='text'
        self.fields['describtion'].widget.attrs['row']=3

        self.fields['price'].widget.attrs['placeholder']='Enter Product Price'
        self.fields['price'].widget.attrs['class']='form-control form-control-user'
        self.fields['price'].widget.attrs['type']='text'

        self.fields['stock'].widget.attrs['placeholder']='Enter Product Stock'
        self.fields['stock'].widget.attrs['class']='form-control form-control-user'
        self.fields['stock'].widget.attrs['type']='text'

        self.fields['category'].widget.attrs['class']='form-control form-control-user'

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = ['product','variation_category','variation_value','is_active']

class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = ['title','discription','banner_image','is_available']