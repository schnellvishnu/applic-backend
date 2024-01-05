from django.urls import path
from accounts import views
urlpatterns = [
    path('userAuthVerify', views.userAuthVerify.as_view()),
    path('userrolePermissionsRead', views.UserrolePermissionsRead.as_view()),
    path('logInController', views.logInController.as_view()),  
    path('chnew/', views.Emailindividual.as_view()), 
    path('userAuditReportdate/', views.UserAuditReportdate.as_view()),  
    #---------------------------------------------------------------------------
    path('history/', views.AuditLogView.as_view()),
    # path('auditlog/update/<int:pk>', views.updateAuditlog.as_view()),
    path('history/delete/<int:pk>', views.deleteAuditlog.as_view()),
    path('historymodel/<id>/', views.HistoryemployeandmodelIndividual.as_view()),
    path('historymodelname/<id>/', views.HistoryemployeandmodelnameIndividual.as_view()),
    path('historyindividualoperator/<id>/', views.HistoryIndividual.as_view()), 
    path('profile/<id>/', views.RegisterIndividual.as_view()), 
    path('logoutController', views.logoutController.as_view()),           
]