from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.Home.as_view(), name='home_page'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.Register.as_view(), name='register'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='log_user'),
    path('user/<int:pk>/update', views.UserUpdate.as_view(), name='update_user'),
    path('user/<int:pk>/delete', views.UserDelete.as_view(), name='delete_user')
]
