from django.urls import path
from .import views
urlpatterns = [
    path('',views.adminpanel,name='adminpanel'),
    path('admin_login/',views.admin_login,name="admin_login"),

    path('user_accounts_table/',views.user_accounts_table,name="user_accounts_table"),
    path('ban_user/<int:id>/',views.ban_user,name="ban_user"),
    path('unban_user/<int:id>/',views.unban_user,name='unban_user'),
    
    path('category_table/',views.category_table,name="category_table"),
    path('add_category/',views.addcategory,name="add_category"),
    path('editcategory/<int:id>/',views.editcategory,name="editcategory"),
    path('delete/<int:id>/',views.deletecategory,name="deletecategory"),

    path('order_table/<int:id>/',views.order_table,name='order_table'),
    path('order_accepted/<int:order_id>',views.order_accepted,name="order_accepted"),
    path('order_completed/<int:order_id>',views.order_completed,name="order_completed"),
    path('order_cancelled/<int:order_id>',views.order_cancelled,name="order_cancelled"),
    path('order_details/<int:order_id>/',views.order_details, name='order_details'),

    path('store_table/<int:id>/',views.store_table,name="store_table"),

    path('add_product/',views.add_product,name="add_product"),
    path('edit_product/<int:id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:id>/',views.delete_product,name="delete_product"),

    path('add_variations/',views.add_variations,name="add_variations"),
    path('delete_variations/<int:id>/',views.delete_variations,name="delete_variations"),

    path('home_table/',views.home_table,name="home_table"),

    path('add_carousels/',views.add_carousels,name="add_carousels"),
    path('edit_carousel/<int:id>/',views.edit_carousel,name='edit_carousel'),
    path('carousel_not_available/<int:id>/',views.carousel_not_available,name="carousel_not_available"),
    path('caraousel_available/<int:id>/',views.caraousel_available,name='caraousel_available'),
    path('delete_carousel/<int:id>/',views.delete_carousel,name="delete_carousel"),

]