from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url('gettime', views.search_time, name='search_time'),  # 获得首末班车时间表
    url('judgequestion', views.judge_question, name='judge_question')
]
