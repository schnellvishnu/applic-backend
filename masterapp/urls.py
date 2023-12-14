from django.urls import path
from masterapp import views
urlpatterns = [
   
   path('productionorder/', views.ProductionOrderView.as_view()),
   path('productionorder/<int:id>/', views.ProductionOrderViewIndividual.as_view()),
   
   path('ShippoauditReportdate/', views.ShippoAuditReportdate.as_view()),
   
   path('shippoint/', views.ShipPOViewget.as_view()),
    path('shippoint/<int:id>/',views.ShippoProductionordernumberGetingIndividual.as_view()),
   
   path('customer/', views.CustomersView.as_view()),
   
   path('locations/', views.LocationsView.as_view()),
   
   path('printer/', views.printerview.as_view()),
   # path('printer/update/<int:id>/', views.Printerupdateview.as_view()),
   path('printer/<int:id>/',views.Printerindividualview.as_view()),
   path('printergtin/<int:id>/',views.Printergtinview.as_view()),
   path('printerip/', views.Printeripview.as_view()),
   path('printerip/<id>/', views.Printeripgetview.as_view()),
   path('clientcommunication/',views.ClientCommunication.as_view()), 
   # path('clientcommunication1/',views.ClientCommunication1.as_view()), 
   # path('systemip/', views.SystIp),
   path('scannerdata/',views.ScannerCommunicationView.as_view()),
   path('scannerdatadelete/',views.Deletescanner.as_view()),
   path('printerprepare/',views.PrinterprepareView.as_view()),
   # path('printerprepare/<int:id>/',views.PrinterprepareGetView.as_view()),
   path('printerstop/',views.PrinterStopView.as_view()),
   
   path('printerstart/',views.PrinterStartView.as_view()),
   path('loopstop/',views.LooopStopView.as_view()), 
   
   
   # path('checkboxindividual/<int:id>/',views.Checkboxindividualview.as_view()),  
              
]



