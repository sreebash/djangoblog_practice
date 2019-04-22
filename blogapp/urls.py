from django.urls import path

from blogapp import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('author/<name>/', views.getauthor.as_view(), name='author'),
    path('article/<int:id>', views.getsingle.as_view(), name='single_post'),
    path('topic/<name>', views.getTopic.as_view(), name='topic'),
    path('login/', views.getLogin.as_view(), name='login'),
    path('logout/', views.getLogout.as_view(), name='logout'),
    path('create/', views.getCreate, name='create'),
    path('profile/', views.getProfile, name='profile'),
    path('update/<int:pid>', views.getUpdate, name='update'),
    path('delete/<int:pid>', views.getDelete, name='delete'),
    path('register/', views.getRegister, name='register'),
    path('topics/', views.topics, name='topics'),
    path('topic/new/', views.newTopic, name='new_topic'),

    # Account Confirmation
    path('activate/<uid>/<token>/', views.activate, name='activate'),

]
