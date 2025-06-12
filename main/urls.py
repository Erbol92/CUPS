
from django.urls import path
from .views import auth, main, exit, create_order, report
urlpatterns = [
    path('',auth,name='auth' ),
    path('main/<str:room>/',main,name='main' ),
    path('logout',exit,name='logout' ),
    path('create-order/', create_order, name='create_order'),
    path('report/', report, name='report'),
    # 
]
