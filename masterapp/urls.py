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
   path('scannerdata/<int:id>/',views.Scannerindividualview.as_view()),
   path('scannerdata/update/<int:id>', views.updateScannertable.as_view()),
   path('scannerdatadelete/',views.Deletescanner.as_view()),
   path('scannerrework/',views.ScannerReworkView.as_view()),
   path('printerprepare/',views.PrinterprepareView.as_view()),
   # path('printerprepare/<int:id>/',views.PrinterprepareGetView.as_view()),
   
   path('reworkpost/',views.Reworkpostview.as_view()),
   path('printerstop/',views.PrinterStopView.as_view()),
   
   path('printerstart/',views.PrinterStartView.as_view()),
   
   path('loopstop/',views.LooopStopView.as_view()), 
   path('printergtinindividual/<int:id>/',views.PrintergtinIndividual.as_view()),
   path('scannerstatusindividual/<id>/', views.ScannerStatusIndividual.as_view()),
   path('countdata/', views.CountView.as_view()),
   
   # path('checkboxindividual/<int:id>/',views.Checkboxindividualview.as_view()),
   
          path("printer/change/<int:id>",views.Viewprinterview.as_view(),name="emp-editjob"), 
        path("printerstop/change/<int:id>",views.Jobeditstopview.as_view(),name="empstop-editjob"),
        # path('pauseprinter/',views.PausePrinter.as_view(),name="pause"),
        # path('demo/all',views.Demoview.as_view(),name="demo-all"),
        path('pause/<int:id>',views.PauseClassview.as_view(),name="pause-printer"),
        # path('search/',views.Searchview.as_view(),name="search"), 
        # path('squat',views.Runcode.as_view(),name="squat"),
        path('search/', views.searchBar, name='search'),
        path("returnserialget/<int:id>",views.ReturnsnGet.as_view(),name="return-get"),
        path("returnserialno/<int:id>",views.Returnserialnumbers.as_view(),name="return-numbres"),
        
        path("nextserial/<int:id>",views.Nextserialno.as_view(),name="next-numbres"), 
        path('indexpage/', views.listing, name='indexpage'),
        path("home",views.Candidatehomeview.as_view(),name="cand-home"),
        path("scannerhome",views.Scannermessageview.as_view(),name="scanner-message"),
        path("batchstopmess/",views.Batchstopmessageview.as_view(),name="batch-stop-message"),
        path("printererrors/",views.Errorview.as_view(),name="printer-errors"), 
        path("scannersoftware/",views.Scannersoftwareview.as_view(),name="scanner-software"), 
        path("autovisionopen/<int:id>",views.Autovisionopenview.as_view(),name="autovision"),
        path("grade/",views.Getgradedata.as_view(),name="grade"),
        path("gradecount/<int:id>",views.Gradecount.as_view(),name="gradecount"),
        
        # path("referer/",views.get_referer,name="referer"),
        
        path("signin/",views.Signinview.as_view(),name="signin"),
        path("signout/",views.signout_view,name="signout"),  


        
        path("serialnumberdownload/<int:id>",views.Serialnumberdownloadagainview.as_view(),name="serialnumberdownload"), 
              
]



# 