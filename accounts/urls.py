from django.urls import path
from accounts import views
urlpatterns = [
    path('userAuthVerify', views.userAuthVerify.as_view()),

    path('logInController', views.logInController.as_view()),  
    path('chnew/', views.Emailindividual.as_view()), 
    
    path('userAuditReportdate/', views.UserAuditReportdate.as_view()),               
]