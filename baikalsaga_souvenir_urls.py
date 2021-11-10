from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', SouvenirHome.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('addgoods/', AddGoods.as_view(), name='add_goods'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('goods/<slug:goods_slug>/', ShowGoods.as_view(), name='goods'),
    path('category/<slug:cat_slug>/', SouvenirsCategory.as_view(), name='category')

]