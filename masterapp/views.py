from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View,ListView,CreateView,DetailView,UpdateView,DeleteView,FormView,TemplateView
from masterapp.forms import PrinterForm,CustomerForm,Dummyform,Loginform
from masterapp .models import PrinterdataTable,ProductionOrder,ScannerTable,ShipPO,Customers,Locations,ReworkTable
from masterapp.serializers import PrinterSerializer,ProductionOrderSerializer,ScannerSerializer,LoopStopSerializer,ShipPOSerializer,CustomersSerializer,LocationSerializer,ReworkSerializer
from  rest_framework .views import APIView
from rest_framework .response import Response
import socket
from accounts.models import Loginmodel,Register,UserrolePermissions
import json
from urllib.request import urlopen
import re as r
import threading
from django.http import HttpResponse
import itertools
from channels.generic.websocket import AsyncWebsocketConsumer
# import threading
from django.contrib import messages
import time
# import sys
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from accounts.models import History
from accounts.serializers import HistorySerializer
import datetime

from queue import Queue
from multiprocessing import Event
from django.contrib.auth import authenticate,login,logout       
# import requests
# Create your views here.
# from multiprocessing import Process
class ProductionOrderView(APIView):
    def get(self, request):
        detailsObj =ProductionOrder.objects.all().order_by('id').reverse()
        serializeObj = ProductionOrderSerializer(detailsObj, many = True)
        return Response(serializeObj.data)
 
class ProductionOrderViewIndividual(APIView):
    def get(self, request, id):
       detailsObj = ProductionOrder.objects.all().filter(id=id)
       serializeObj = ProductionOrderSerializer(detailsObj, many=True)
       return Response(serializeObj.data)

# ...............................................................................
class ShippoAuditReportdate(APIView):  
    def get(self, request):
        detailsObj = ShipPO.objects.all()
        serializeObj =ShipPOSerializer(detailsObj, many=True)
        # fromDate = request.data["datefrom"]
        # toDate = request.data["dateto"]
        # response  = ProductionReport.objects.filter( production_date=fromDate, production_date__lte=toDate)
        return Response(200)
    
    def post(self, request):
        serializeObj = ShipPOSerializer(data=request.data)
        v=[]
        startdate = request.data["datefrom"]
        
        toDate = request.data["dateto"]
        # fromDate=str(request.POST.get('datefrom'))
        # toDate=str(request.POST.get("dateto"))
        # response  =ProductionReport.objects.all().filter(production_date=id)
        
        response  =ShipPO.objects.all().filter(shipping_date__range=(startdate, toDate))
        serializeObj = ShipPOSerializer(response , many=True)
        return Response(serializeObj.data) 
 
class ShippoProductionordernumberGetingIndividual(APIView):
       def get(self,request,id):
         detailsObj=ShipPO.objects.all().filter(process_no_original=id)
         serializeObj=ShipPOSerializer(detailsObj,many=True)
         return Response(serializeObj.data)             
class ShipPOViewget(APIView):
       def get(self, request):
         detailsObj =ShipPO.objects.all()
         serializeObj = ShipPOSerializer(detailsObj, many = True)
         return Response(serializeObj.data)  
# ........................................................................................

class CustomersView(APIView):
       def get(self, request):
         detailsObj = Customers.objects.all().order_by('-id')
         serializeObj = CustomersSerializer(detailsObj, many = True)
         return Response(serializeObj.data)
class CustomerViewIndividual(APIView):
       def get(self, request, id):
         detailsObj = Customers.objects.all().filter(id=id)
         serializeObj = CustomersSerializer(detailsObj, many=True)
         return Response(serializeObj.data) 
#   ..........................................................................
class LocationsView(APIView):
       def get(self, request):
         detailsObj = Locations.objects.all().order_by('id')
         serializeObj = LocationSerializer(detailsObj, many = True)
         return Response(serializeObj.data)
#   ................................................................................


class printerview(APIView) :
                           
                           
       def get(self,request):
            detailObj=PrinterdataTable.objects.all().order_by('-id')
            serializeobj=PrinterSerializer(detailObj,many=True)
            return Response(serializeobj.data)
       def post(self,request):
                            # detailobj= PrinterdataTable.objects.get(id=id)
                            pobj=PrinterdataTable.objects.get(gtin=request.data["gtin"])
                            pobj.status="Printed"
                            pobj.save()
                            return Response(200)
       
     
# class Printerupdateview(APIView):
#               def put(self, request, id):
#                      try:
#                        detailObj = PrinterdataTable.objects.get(id=id)
#                      except:
#                         return Response("Not found in database")
                     
#                      serializeObj = PrinterSerializer(detailObj, data=request.data)
#                      # statusdata=request.data["status"]
#                      # gtindata=request.data["gtin"]
#                      # print(statusdata)
#                      print("haiii")
#                      if serializeObj.is_valid():
#                             serializeObj.save()
#                             detailobj= PrinterdataTable.objects.get(id=id)
#                             pobj=PrinterdataTable.objects.get(gtin=detailobj.gtin)
#                             pobj.status="Printed"
#                             pobj.save()
#                             # detailobj.status="printed"
#                             print("haiii")
#                             # detailobj.save()
#                             # detailobj= PrinterdataTable.objects.filter(id=gtindata).update(status=statusdata)
#                             return Response(200)
#                      # print(detailObj.pk)
#                      return Response(serializeObj.errors)

class Printerindividualview(APIView):
       def get(self,request,id):
                detailobj=PrinterdataTable.objects.all().filter(id=id)
                serializeobj=PrinterSerializer(detailobj,many=True)
                return Response(serializeobj.data) 

class Printergtinview(APIView):
       def get(self,request,id):
                detailobj=PrinterdataTable.objects.all().filter(id=id)
                detailobj[0].status="Printed"
                
                serializeobj=PrinterSerializer(detailobj,many=True)
                detailobj[0].save()
                return Response(serializeobj.data) 
class Printeripview(APIView):
       def get(self,request):
              hostname = socket.gethostname()
              systemip = socket.gethostbyname(hostname)
              print(systemip)
              # print(socket.gethostbyname(systemip))
              
              return Response(systemip) 
class Printeripgetview(APIView):
       def get(self,request,id):
                detailobj=PrinterdataTable.objects.all().filter(ip_address=id)
                serializeobj=PrinterSerializer(detailobj,many=True)
                return Response(serializeobj.data)          
         

# class ClientCommunication(APIView):
#        def get(self,request):
#                                   # global data7                    
#               s = socket.socket()
#               port=34567
#               s.connect(('192.168.200.150', port))
       
#               message= "F0\x04"
#               s.send(message.encode()) 
#               data7=s.recv(1024).decode() 
#               print('Received from server: ' + data7)
#               return Response(200)                  
#        def printfun(self,gtin,lot,expire,serialno,printstopdata):
#               self.gtin=gtin 
#               self.lot=lot
#               self.expire=expire
#               self.serialno=serialno
#               self.printstop=printstopdata
             
#               # v=len(serialno)
           
#               s = socket.socket()
#               port=34567
#               s.connect(('192.168.200.150', port))
#               # gtinarray=["676878","8967868"]
#               # slnoarray=["","33333","444444","555555","4545545","222222"]
            
#               message= "L,schnell.lbl\x04"
#               s.send(message.encode()) 
#               data=s.recv(1024).decode()  
#               message1= "E\x04"        
#               s.send(message1.encode()) 
#               data1=s.recv(1024).decode()  
              
                                  
                               
#               for sn in serialno:
                      
                     
                     
#                             message5= "QAH\x09Datamatrix\x09gtin\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"expvalue\x09"+"serialno\x09"+"serialvalue\x04"
#                             s.send(message5.encode()) 
#                             data5=s.recv(1024).decode()
#                             # print(slno)                    
#                             # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
#                             message6= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
#                             s.send(message6.encode()) 
#                             data6=s.recv(1024).decode() 
                                   
#                             message4= "F2\x04"
#                             s.send(message4.encode()) 
#                             data4=s.recv(1024).decode()
#                             # print(sn)
#                             # serialno.remove(sn)
                            
                             
#               # print(serialno)
#               print('Received from server: ' + data5)
#               print('Received from server: ' + data6)         
#               print('Received from server: ' + data4)
#               # time.sleep(6.5)
#               return Response(200)
       
#        def post(self,request):  
#               global data,v,h;     
#               gtin=request.data["gtin"]
#               lot=request.data["lot"]
#               expire=request.data["expiration_date"]
#               id=request.data["id"]
#               serialno=[]
#               serialno=request.data["numbers"]
#               printstopdata=request.data["printstop"]
#               loopbreak=request.data["breakloop"]
#               u=4
#               # print(id)
#               # quantity=request.data["quantity"]
#               self.printfun(gtin,lot,expire,serialno,printstopdata)
#               # if u== 4:
#               # detailobj= PrinterdataTable.objects.all()
#               detailsObj = PrinterdataTable.objects.get(id=id)
#         # print(detailsObj.product_conn)
#               prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
#               print(prodObj.gtin)
              
#               s = socket.socket()
#               port=2001
#               s.connect(('192.168.200.134', port)) 
#               t=len(serialno)
#               print(t)
#               f=True
#               counter=1
#               h=[]
#               # m=0
             
#               # while True:                          
#               for i in range(t):            
#                      data=s.recv(1024).decode()                                         
#                      v=data[0]
#                      confidence=data[1]
#                      print(confidence)
#                      meanconfidence=data[2:7]
#                      h.append(serialno[counter])
                     
#                      if(v=="4" and confidence=="1" and meanconfidence>="0.800"):
#                             grade="A"
#                      elif(v=="3" and confidence=="1" and meanconfidence>="0.800"):
#                              grade="B"
#                      elif (v=="2" and confidence=="1" and meanconfidence>="0.800"):
#                             grade="C"
#                      elif (v=="1" and confidence=="1" and meanconfidence>="0.800"):
#                             grade="D"
#                      else:
#                             grade="F"  
#                      r={"serialnumber":serialno[counter],
#                             "grade":grade}
                     
#                      print(r)
#                      b=json.dumps(r)
#                      serializeobj=ScannerSerializer(data=request.data)
                            
#                      if serializeobj.is_valid():
#                             device=serializeobj.save()
#                             obj = ScannerTable.objects.get(pk=device.id)
#                                    # print( device.id)
            
#                             detailObj=ScannerTable.objects.filter(pk=device.id).update(grade=b)
#                      bj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(numbers=gh)                     
                                                               
#                      if i==printstopdata-1  :
                                   
#                             s = socket.socket()
#                             port=34567
#                             s.connect(('192.168.200.150', port))
              
#                             message= "F0\x04"
#                             s.send(message.encode()) 
#                             data7=s.recv(1024).decode() 
#                             print('Received from server: ' + data7)
#                             break
#                             # m=m+1                       
#                      counter=counter+1
                     
                                         
#               jno = json.dumps(h) 
             
              
             
#               obj = PrinterdataTable.objects.get(id=request.data["id"])
#                                    # print( device.id)
#               #print(obj.gtin)
#               detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(printed_numbers=jno)
#               updatedjson=json.loads(jno)
#               # print(updatedjson)
#               io=len(updatedjson)
#               c1=1
#               c2=0
#               for y in range(io):
#                             # print(updatedjson) 
#                      if(serialno[c1]==updatedjson[c2]):
#                                    # serialno.remove(serialno[c1])
#                             serialno.remove(serialno[c1]) 
#                      else: 
#                             c1=c1+1 
#                      c2=c2+1            #now it became correct   
#              # print(serialno)
#               gh=json.dumps(serialno)
#               obj = PrinterdataTable.objects.get(id=request.data["id"])
#               detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(numbers=gh)             
#               return Response(200)  
# ...........................................................
class ClientCommunication(APIView):
       def get(self,request):
                                  # global data7                    
              s = socket.socket()
              port=34567
              s.connect(('192.168.200.150', port))
       
              message= "F0\x04"
              s.send(message.encode()) 
              data7=s.recv(1024).decode() 
              print('Received from server: ' + data7)
              return Response(200)                  
       def printfun(self,gtin,lot,expire,serialno,printstopdata,printingtype,hrfkey,hrfvalue):
              self.gtin=gtin 
              self.lot=lot
              self.expire=expire
              self.serialno=serialno
              self.printstop=printstopdata
              self.printingtype=printingtype
              self.hrfkey=hrfkey
              self.hrfvalue=hrfvalue
              # v=len(serialno)
              print(printingtype)
              s = socket.socket()
              port=34567
              s.connect(('192.168.200.150', port))
              # gtinarray=["676878","8967868"]
              # slnoarray=["","33333","444444","555555","4545545","222222"]
                 
              
              if(printingtype=="type2"):
                     # message18="QAF\x04"
                     # s.send(message18.encode()) 
                     # data18=s.recv(1024).decode()                     
                     message= "L,new7.lbl\x04"
                     s.send(message.encode()) 
                     data=s.recv(1024).decode()  
                     message1= "E\x04"        
                     s.send(message1.encode()) 
                     data1=s.recv(1024).decode()  
                     
                                   
                                   
                     for sn in serialno:
                            
                            
                            
                                   message5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s.send(message5.encode()) 
                                   data5=s.recv(1024).decode()
                                   # print(slno)                    
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message6= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s.send(message6.encode()) 
                                   data6=s.recv(1024).decode() 
                                          
                                   message4= "F2\x04"
                                   s.send(message4.encode()) 
                                   data4=s.recv(1024).decode()
                                   # print(sn)
                                   # serialno.remove(sn)
                                   
                                   
                     # print(serialno)
                     print('Received from server: ' + data5)
                     print('Received from server: ' + data6)         
                     print('Received from server: ' + data4)
                     # time.sleep(6.5)
              elif(printingtype=="type5"):
                     print("hi")
                     message7= "L,new8.lbl\x04"
                     s.send(message7.encode()) 
                     data7=s.recv(1024).decode()  
                     message8= "E\x04"        
                     s.send(message8.encode()) 
                     data8=s.recv(1024).decode()  
                     
                                   
                                   
                     for sn in serialno:
                            
                            
                            
                                   message9= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                                   s.send(message9.encode()) 
                                   data9=s.recv(1024).decode()
                                   # print(slno)                    
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message10= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn + "(45)"+ hrfvalue+ "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn +"\x09"+hrfkey+"\x09"+hrfvalue+ "\x04"
                                   s.send(message10.encode()) 
                                   data10=s.recv(1024).decode() 
                                          
                                   message11= "F2\x04"
                                   s.send(message11.encode()) 
                                   data11=s.recv(1024).decode()
                                   # print(sn)
                                   # serialno.remove(sn)
                                   
                                   
                     # print(serialno)
                     print('Received from server: ' + data7)
                     print('Received from server: ' + data8) 
                     print('Received from server: ' + data9)
                     print('Received from server: ' + data10)         
                     print('Received from server: ' + data11)
              elif(printingtype=="type1"):
                     message12= "L,new5.lbl\x04"
                     s.send(message12.encode()) 
                     data12=s.recv(1024).decode()  
                     message13= "E\x04"        
                     s.send(message13.encode()) 
                     data13=s.recv(1024).decode()  
                     
                                   
                                   
                     for sn in serialno:
                            
                            
                            
                                   message14= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s.send(message14.encode()) 
                                   data14=s.recv(1024).decode()
                                   # print(slno)                    
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message15= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s.send(message15.encode()) 
                                   data15=s.recv(1024).decode() 
                                          
                                   message16= "F2\x04"
                                   s.send(message16.encode()) 
                                   data16=s.recv(1024).decode()
                                   # print(sn)
                                   # serialno.remove(sn)
                                   
                                   
                     # print(serialno)
                     print('Received from server: ' + data14)
                     print('Received from server: ' + data15)         
                     print('Received from server: ' + data16)
              return Response(200)
       
       def post(self,request):  
              global user_input;     
              gtin=request.data["gtin"]
              lot=request.data["lot"]
              expire=request.data["expiration_date"]
              id=request.data["id"]
              serialno=[]
              serialno=request.data["numbers"]
              printstopdata=request.data["printstop"]
              loopbreak=request.data["breakloop"]
              printingtype=request.data["type"]
              responsefield=request.data["responsefield"]
              stopbtnresponse=request.data["stopbtnresponse"]
              start_pause_btnresponse= request.data["start_pause_btnresponse"]
              # print(printingtype)
              pause_stop_btnresponse=request.data["pause_stop_btnresponse"]
              # print(hrf1)
              # if(printingtype=="type5" or printingtype=="type1"):
                 # if u== 4:
              detailobj= PrinterdataTable.objects.all()
              detailsObj = PrinterdataTable.objects.get(id=id)
              # print(detailsObj.product_conn)
              prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
              print(prodObj.gtin)
              obj = PrinterdataTable.objects.get(id=request.data["id"])
                                                        # print( device.id)
                                   #print(obj.gtin)
              detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(responsefield=responsefield)
              
              detailsObj = PrinterdataTable.objects.get(id=id) 
              prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
              print(prodObj.gtin)
              obj = PrinterdataTable.objects.get(id=request.data["id"])
                                                        # print( device.id)
                                   #print(obj.gtin)
              detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(stopbtnresponse=stopbtnresponse,start_pause_btnresponse= start_pause_btnresponse,pause_stop_btnresponse=pause_stop_btnresponse) 
           
              hrf=request.data["hrf"]
              hrfjson=json.loads(hrf)
                    
              hrf1value=hrfjson["hrf1value"]
              hrf1key=hrfjson["hrf1"]
              hrf2value=hrfjson["hrf2value"]
              hrf2key=hrfjson["hrf2"]
              hrf3value=hrfjson["hrf3value"]
              hrf3key=hrfjson["hrf3"]
              hrf4value=hrfjson["hrf4value"]
              hrf4key=hrfjson["hrf4"]
              hrf5key=hrfjson["hrf5"]
              hrf5value=hrfjson["hrf5value"]
              hrf6key=hrfjson["hrf6"]
              hrf6value=hrfjson["hrf6value"]
              if(hrf1key!="" or hrf1key!="null"):
                     hrfkey=hrf1key
              elif(hrf2key!="" or hrf2key!="null"):
                     hrfkey=hrf2key
              elif(hrf3key!="" or hrf3key!="null"):
                     hrfkey=hrf3key
              elif(hrf4key!="" or hrf4key!="null"):
                            hrfkey=hrf4key
              elif(hrf5key!="" or hrf5key!="null"):
                            hrfkey=hrf5key
              elif(hrf6key!="" or hrf6key!="null"):
                            hrfkey=hrf6key
              else:
                     hrfkey="null"
              if(hrf1value!="" or hrf1value!="null"):
                     hrfvalue=hrf1value
              elif(hrf2value!="" or hrf2value!="null"):
                     hrfvalue=hrf2value
              elif(hrf3value!="" or hrf3value!="null"):
                     hrfvalue=hrf3value
              elif(hrf4value!="" or hrf4value!="null"):
                     hrfvalue=hrf4value
              elif(hrf5value!="" or hrf5value!="null"):
                     hrfvalue=hrf5value
              elif(hrf6value!="" or hrf6value!="null"):
                     hrfvalue=hrf6value
              else:
                     hrfvalue="null"                           
                     
              # quantity=request.data["quantity"]
              self.printfun(gtin,lot,expire,serialno,printstopdata,printingtype,hrfkey,hrfvalue)
             
           
              
              s = socket.socket()
              port=2001
              # timeout=3
              s.connect(('192.168.200.134', port)) 
              t=len(serialno)
              # print(t)
             
              counter=0
              u=[]
              z=5
              
              # serialnumber=["11","22","33","44","55","66","77","88","99","10"]
              
              for j in range(t):
                                            # print(j)
                                
                     user_input =int(request.data["printstop"])
                          
                       
                           
                     while z>user_input: 
                            user_input =int(request.data["printstop"])
                            # print(serialno[counter])
                            
                            
                            data=s.recv(1024).decode()
                            print(data)                                         
                            v=data[0]
                            meanconfidence=data[2:7]
                            confidence=data[1]
                                   
                            u.append(serialno[counter])
                                   
                            jso = json.dumps(u) 
                            
                            print(serialno[counter])
                            
                            if(v=="4" and confidence=="1" and meanconfidence>="0.800"):
                                                grade="A"
                            elif(v=="3" and confidence=="1" and meanconfidence>="0.800"):
                                   grade="B"
                            elif (v=="2" and confidence=="1" and meanconfidence>="0.800"):
                                   grade="C"
                            elif (v=="1" and confidence=="1" and meanconfidence>="0.800"):
                                   grade="D"
                            else:
                                   grade="F"  
                            r={"serialnumber":serialno[counter],
                                   "grade":grade}
                            print(r)
                            b=json.dumps(r)
                            serializeobj=ScannerSerializer(data=request.data)
                            
                            if serializeobj.is_valid():
                              device=serializeobj.save()
                              obj = ScannerTable.objects.get(pk=device.id)
                                   # print( device.id)
            
                              detailObj=ScannerTable.objects.filter(pk=device.id).update(grade=b)
                            #   bj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(numbers=gh)  
                            
                            obj = PrinterdataTable.objects.get(id=request.data["id"])
                                                        # print( device.id)
                                   #print(obj.gtin)
                            detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(printed_numbers=jso)
                            updatedjson=json.loads(jso)
                            serialno.remove(serialno[counter])
                            gh=json.dumps(serialno)
                            obj = PrinterdataTable.objects.get(id=request.data["id"])
                            detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(numbers=gh)
                            
                          
                     time.sleep(6)
                                      
                     # user_input =int(request.data["printstop"])
                        
                 
                     # print('Received from server: ' + data7)
                     # print(serialnumber[counter])   
                     
                     r = requests.delete( request.data["printstop"] )
                     
                    
                     
              # if(user_input==0):        
              #        return Response(200)
              # else:
              return Response(200)  
        
                                  
class PrinterprepareView(APIView):
                      
       def post(self,request):
              gtin=request.data["gtin"]
              preparebuttonresponse=request.data["preparebuttonresponse"]
              id=request.data["id"] 
              detailsObj = PrinterdataTable.objects.get(id=id) 
              prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
              print(prodObj.gtin)
              obj = PrinterdataTable.objects.get(id=request.data["id"])
                                                        # print( device.id)
                                   #print(obj.gtin)
              detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(preparebuttonresponse=preparebuttonresponse)               
              s = socket.socket()
              port=34567
              s.connect(('192.168.200.150', port))
              message17="QAF\x04"
              s.send(message17.encode()) 
              data17=s.recv(1024).decode() 
              
              
              # message18= "F0\x04"
              # s.send(message18.encode()) 
              # data18=s.recv(1024).decode() 
              
                                        
              print('Received from server: ' + data17)
              # print('Received from server: ' + data18)
              
              # if(d==0):
              #        # print("hi")                         
              #       os._exit(1)
              # else:
              #   print("not")
         
              
                                         
              return Response(200)
       
# class PrinterprepareGetView(APIView) :
#        def get(self, request, id):
#              detailsObj = PrinterdataTable.objects.all().filter(id=id)
#              serializeObj = CheckboxSerializer(detailsObj, many=True)
#              return Response(serializeObj.data)                          
class PrinterStopView(APIView):
       def post(self,request):
              d=request.data["breakloop"]
              printingtype=request.data["type"]
              # stopbtnresponse=request.data["stopbtnresponse"]
              # start_pause_btnresponse=request.data["start_pause_btnresponse"]
              pause_stop_btnresponse=request.data["pause_stop_btnresponse"]
              # print(stopbtnresponse)
              id=request.data["id"]   
              gtin=request.data["gtin"] 
              
              detailsObj = PrinterdataTable.objects.get(id=id) 
              prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
              detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused")
               
              detailsObj = PrinterdataTable.objects.get(id=id) 
              prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
              print(prodObj.gtin)
              obj = PrinterdataTable.objects.get(id=request.data["id"])
                                                        # print( device.id)
                                   #print(obj.gtin)
              detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(pause_stop_btnresponse=pause_stop_btnresponse)                
              s = socket.socket()
              
              port=34567
              s.connect(('192.168.200.150', port))
              message17="QAF\x04"
              s.send(message17.encode()) 
              data17=s.recv(1024).decode() 
              
              
              
              # message18= "F0\x04"
              # s.send(message18.encode()) 
              # data18=s.recv(1024).decode() 
              
                                        
              print('Received from server: ' + data17)
              # print('Received from server: ' + data18)
              
              # if(d==0):
              #        # print("hi")                         
              #       os._exit(1)
              # else:
              #   print("not")
         
                                         
              return Response(200)
             
class PrinterStartView(APIView):
                           
       def printfun(self,gtin,lot,expire,serialno,printstopdata,printingtype,hrfkey,hrfvalue):
              self.gtin=gtin 
              self.lot=lot
              self.expire=expire
              self.serialno=serialno
              self.printstop=printstopdata
              self.printingtype=printingtype
              self.hrfkey=hrfkey
              self.hrfvalue=hrfvalue
              # v=len(serialno)
              print(printingtype)
              s = socket.socket()
              port=34567
              s.connect(('192.168.200.150', port))
              # gtinarray=["676878","8967868"]
              # slnoarray=["","33333","444444","555555","4545545","222222"]
                 
              
              if(printingtype=="type2"):
                     message= "L,new7.lbl\x04"
                     s.send(message.encode()) 
                     data=s.recv(1024).decode()  
                     message1= "E\x04"        
                     s.send(message1.encode()) 
                     data1=s.recv(1024).decode()  
                     
                                   
                                   
                     for sn in serialno:
                            
                            
                            
                                   message5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s.send(message5.encode()) 
                                   data5=s.recv(1024).decode()
                                   # print(slno)                    
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message6= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s.send(message6.encode()) 
                                   data6=s.recv(1024).decode() 
                                          
                                   message4= "F2\x04"
                                   s.send(message4.encode()) 
                                   data4=s.recv(1024).decode()
                                   # print(sn)
                                   # serialno.remove(sn)
                                   
                                   
                     # print(serialno)
                     print('Received from server: ' + data5)
                     print('Received from server: ' + data6)         
                     print('Received from server: ' + data4)
                     # time.sleep(6.5)
              elif(printingtype=="type5"):
                     # print("hi")
                     message7= "L,new8.lbl\x04"
                     s.send(message7.encode()) 
                     data7=s.recv(1024).decode()  
                     message8= "E\x04"        
                     s.send(message8.encode()) 
                     data8=s.recv(1024).decode()  
                     
                                   
                                   
                     for sn in serialno:
                            
                            
                            
                                   message9= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                                   s.send(message9.encode()) 
                                   data9=s.recv(1024).decode()
                                   # print(slno)                    
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message10= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn + "(45)"+ hrfvalue+ "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn +"\x09"+hrfkey+"\x09"+hrfvalue+ "\x04"
                                   s.send(message10.encode()) 
                                   data10=s.recv(1024).decode() 
                                          
                                   message11= "F2\x04"
                                   s.send(message11.encode()) 
                                   data11=s.recv(1024).decode()
                                   # print(sn)
                                   # serialno.remove(sn)
                                   
                                   
                     # print(serialno)
                     print('Received from server: ' + data7)
                     print('Received from server: ' + data8) 
                     print('Received from server: ' + data9)
                     print('Received from server: ' + data10)         
                     print('Received from server: ' + data11)
              elif(printingtype=="type1"):
                     message12= "L,new5.lbl\x04"
                     s.send(message12.encode()) 
                     data12=s.recv(1024).decode()  
                     message13= "E\x04"        
                     s.send(message13.encode()) 
                     data13=s.recv(1024).decode()  
                     
                                   
                                   
                     for sn in serialno:
                            
                            
                            
                                   message14= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s.send(message14.encode()) 
                                   data14=s.recv(1024).decode()
                                   # print(slno)                    
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message15= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s.send(message15.encode()) 
                                   data15=s.recv(1024).decode() 
                                          
                                   message16= "F2\x04"
                                   s.send(message16.encode()) 
                                   data16=s.recv(1024).decode()
                                   # print(sn)
                                   # serialno.remove(sn)
                                   
                                   
                     # print(serialno)
                     print('Received from server: ' + data14)
                     print('Received from server: ' + data15)         
                     print('Received from server: ' + data16)
              return Response(200)
       
       def post(self,request):  
              # global data,v,h;     
              gtin=request.data["gtin"]
              lot=request.data["lot"]
              expire=request.data["expiration_date"]
              id=request.data["id"]
              serialno=[]
              serialno=request.data["numbers"]
              printstopdata=request.data["printstop"]
              loopbreak=request.data["breakloop"]
              printingtype=request.data["type"]
              preparebuttonresponse=request.data["preparebuttonresponse"]
              pause_stop_btnresponse=request.data["pause_stop_btnresponse"]
              # print(printingtype)
              start_pause_btnresponse=request.data["start_pause_btnresponse"]
              
              detailsObj = PrinterdataTable.objects.get(id=id) 
              prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
              detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Running")
              
              
              detailsObj = PrinterdataTable.objects.get(id=id) 
              prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
              print(prodObj.gtin)
              obj = PrinterdataTable.objects.get(id=request.data["id"])
                                                        # print( device.id)
                                   #print(obj.gtin)
              detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(preparebuttonresponse=preparebuttonresponse,start_pause_btnresponse=start_pause_btnresponse, pause_stop_btnresponse= pause_stop_btnresponse)
              
              # print(hrf1)
              # if(printingtype=="type5" or printingtype=="type1"):
              
              hrf=request.data["hrf"]
              hrfjson=json.loads(hrf)
                    
              hrf1value=hrfjson["hrf1value"]
              hrf1key=hrfjson["hrf1"]
              hrf2value=hrfjson["hrf2value"]
              hrf2key=hrfjson["hrf2"]
              hrf3value=hrfjson["hrf3value"]
              hrf3key=hrfjson["hrf3"]
              hrf4value=hrfjson["hrf4value"]
              hrf4key=hrfjson["hrf4"]
              hrf5key=hrfjson["hrf5"]
              hrf5value=hrfjson["hrf5value"]
              hrf6key=hrfjson["hrf6"]
              hrf6value=hrfjson["hrf6value"]
              if(hrf1key!="" or hrf1key!="null"):
                     hrfkey=hrf1key
              elif(hrf2key!="" or hrf2key!="null"):
                     hrfkey=hrf2key
              elif(hrf3key!="" or hrf3key!="null"):
                     hrfkey=hrf3key
              elif(hrf4key!="" or hrf4key!="null"):
                            hrfkey=hrf4key
              elif(hrf5key!="" or hrf5key!="null"):
                            hrfkey=hrf5key
              elif(hrf6key!="" or hrf6key!="null"):
                            hrfkey=hrf6key
              else:
                     hrfkey="null"
              if(hrf1value!="" or hrf1value!="null"):
                     hrfvalue=hrf1value
              elif(hrf2value!="" or hrf2value!="null"):
                     hrfvalue=hrf2value
              elif(hrf3value!="" or hrf3value!="null"):
                     hrfvalue=hrf3value
              elif(hrf4value!="" or hrf4value!="null"):
                     hrfvalue=hrf4value
              elif(hrf5value!="" or hrf5value!="null"):
                     hrfvalue=hrf5value
              elif(hrf6value!="" or hrf6value!="null"):
                     hrfvalue=hrf6value
              else:
                     hrfvalue="null"                           
                     
              # quantity=request.data["quantity"]
              serializeobj=PrinterSerializer(data=request.data)
              # if serializeobj.is_valid():
              print(request.data['loggedInUsername']) 
              historysave=History(modelname='PrinterdataTable',
                            savedid="noid",
                            operationdone='print start',
                            donebyuser=request.data['loggedInUsername'],
                            donebyuserrole=request.data['loggedInUserrole'], 
                            description="Started the batch of gtin"+request.data["gtin"]+"\t"+"by"+"\t"+ request.data['loggedInUsername'],
                            donedatetime=datetime.datetime.now())
              historysave.save() 
              self.printfun(gtin,lot,expire,serialno,printstopdata,printingtype,hrfkey,hrfvalue)
              
            
                                         
              return Response(200)             
                
class LooopStopView(APIView):
                             
       def post(self,request):
              # time.sleep(3)                    
              gtin=request.data["gtin"]
              id=request.data["id"]
              serialno=request.data["numbers"]
              # print(serialno)
              return_slno_btn_response=request.data["return_slno_btn_response"]
              
              serializeobj=PrinterSerializer(data=request.data)
              # print("kooi")
              # if serializeobj.is_valid():
              #        print(request.data['loggedInUsername']) 
              
              c1=0
              hf=len(serialno)
              for i in range(hf):
                     serialno.remove(serialno[c1])
                     break
              y=[]
              
              detailsObj = PrinterdataTable.objects.get(id=id)
              prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
              y.append(serialno)
              jyo = json.dumps(y)
               
              detailObj2=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(balanced_serialnumbers=jyo,status="Printed",return_slno_btn_response=return_slno_btn_response)
              # updatedjson=json.loads(jno)
              # io=len(updatedjson)
              y.clear()  
  
              
              # gh=json.dumps(serialno)
              
              obj = PrinterdataTable.objects.get(id=request.data["id"])
              detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(numbers=y)
              historysave=History(modelname='PrinterdataTable',
                       
                            savedid="noid",
                            operationdone='return',
                            donebyuser=request.data['loggedInUsername'],
                            donebyuserrole=request.data['loggedInUserrole'], 
                            description="Batch closed and returned balance serial numbers of the gtin"+request.data["gtin"]+"\t"+"by"+"\t"+ request.data['loggedInUsername'],
                            donedatetime=datetime.datetime.now())
              print(request.data['loggedInUsername'])  
                     
              historysave.save()
              s = socket.socket()
              port=34567
              s.connect(('192.168.200.150', port))
              
              message20= "F0\x04"
              s.send(message20.encode()) 
              data20=s.recv(1024).decode() 
              
              detailsObj = PrinterdataTable.objects.get(id=id) 
              prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
              detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Closed")
         
              return Response(200)                    

                  
# class Checkboxindividualview(APIView):
#        def get(self,request,id):
#               detailobj= PrinterdataTable.objects.all().filter(gtin=id)
#               serializeobj=CheckboxSerializer(detailobj,many=True)
#               return Response(serializeobj.data)                                                               
                              
                            
# class ScannerCommunicationView(APIView):
                             
#               def get(self,request):
#                      # s = socket.socket()
#                      # port=2001
#                      # s.connect(('192.168.200.134', port))
#                      i=1
#                      while i<10:
#                             # data=s.recv(1024).decode()
#                      # v=int(data)
#                      # while (v < 8):
#                      #        data=s.recv(1024).decode()
#                      #        z=int(data)                       
#                      # #      print(z)
#                      # # return Response(z)
                      
#                      # # valuearr=[]
#                      #        i=8
#                      #        if z< i:
#                      #               data=s.recv(1024).decode()
#                      #               w=int(data)
                            
#                             print(i)
#                             i=i+1       
#                             return Response(i)
                            
class ScannerCommunicationView(APIView):
       def get(self,request):
              detailobj=ScannerTable.objects.all()
             
              
              serializeobj=ScannerSerializer(detailobj,many=True)
              return Response(serializeobj.data)                     
                           
       def post(self,request):
                     detailobj= ScannerTable.objects.all()
                                      
              # def getval():
                     s = socket.socket()
                     port=2001
                     s.connect(('192.168.200.134', port))             
                     dummycount = 8
                     data=s.recv(1024).decode()
                     # print(data)
                     v=data[0]
                     h=data[38:]
                     # print(v)
                     # print(h)
                     g=int(v)
                     while (g < dummycount):
                            data=s.recv(1024).decode()
                            v=data[0]
                            h=data[38:]
                            # print(h)
                                               
                            dummycount = dummycount + 1
                            # print(v)
                            # print(h)
                            # print(data)
                            if v=="4":
                               grade="A"
                            elif v=="3":
                                   grade="B"
                            elif v=="2":
                                   grade="C"
                            elif v=="1":
                                   grade="D"
                            else:
                                   grade="F"  
                            r={"serialnumber":h,
                               "grade":grade}
                            # print(r)                                              
                            # l=[]
                            # j=[]
                            # l.append(h)
                            # j.append(grade)
                            
                            # gradewithserialno = dict(zip(l, j))
                       
                            b=json.dumps(r)
                            serializeobj=ScannerSerializer(data=request.data)
                            
                            if serializeobj.is_valid():
                                   device=serializeobj.save()
                                   obj = ScannerTable.objects.get(pk=device.id)
                                   # print( device.id)
            
                            detailObj=ScannerTable.objects.filter(pk=device.id).update(grade=b)
                            print(device.id)
                            # print(b)
                            # for i in l:
                            #        response={
                            #               "result":i
                            #               }
                            #        print(response)
                                                
             
              
                     return Response(200)
class ScannerReworkView(APIView):
       # def get(self,request):
       #        detailobj=ScannerTable.objects.all()
             
              
       #        serializeobj=ScannerSerializer(detailobj,many=True)
       #        return Response(serializeobj.data)                     
                           
       def post(self,request):
                     detailobj= ScannerTable.objects.all()
                     gtin=request.data["gtin"]             
              # def getval():
                     s = socket.socket()
                     port=2001
                     s.connect(('192.168.200.134', port))             
                     dummycount = 8
                     data=s.recv(1024).decode()
                     # print(data)
                     v=data[0]
                     h=data[38:]
                     decodedtext=data[1:48]
                     # print(decodedtext)
                     # print(v)
                     # print(h)
                    
                     r={"serialnumber":h,
                               "decodedtext":decodedtext}
                        
                     # detailsObj = ScannerTable.objects.all().filter(gtin=gtin) 
                     # prodObj=ScannerTable.objects.filter(gtin=detailsObj[0].gtin)
                     # c=0
                     # for i in detailsObj:
                                                 
                     #        n=json.loads(detailsObj[c].grade)  
                           
                     #        if n["serialnumber"]==h:
                     #                  print(detailsObj[c].status)                 
                                 
                                   
                            
                     #        c=c+1
                     serializeobj=ScannerSerializer(data=request.data)
                     if  serializeobj.is_valid():
                                                
                            historysave=History(modelname='ScannerTable',
                                   savedid="noid",
                                   operationdone='rework',
                                   donebyuser=request.data['loggedInUsername'],
                                   donebyuserrole=request.data['loggedInUserrole'], 
                                   description="Rework of serial number"+h+"started"+"\t"+"by"+"\t"+ request.data['loggedInUsername'],
                                   donedatetime=datetime.datetime.now())
                            historysave.save()
                       
                     b=json.dumps(r)
                            
                            # print(b)
                            # for i in l:
                            #        response={
                            #               "result":i
                            #               }
                            #        print(response)
                                                
                     return Response(b)
class Scannerindividualview(APIView):
       def get(self,request,id):
                detailobj=ScannerTable.objects.all().filter(id=id)
                serializeobj=ScannerSerializer(detailobj,many=True)
                return Response(serializeobj.data) 
class updateScannertable(APIView):
       def put(self, request, id):
              try:
                     detailObj =ScannerTable.objects.get(id=id)
              except:
                     return Response("Not found in database")

              serializeObj = ScannerSerializer(detailObj, data=request.data)
              if serializeObj.is_valid():
                     serializeObj.save()
                     return Response(200)       
              return Response(serializeObj.errors) 

class Deletescanner(APIView):
       def get(self, request):
              try:
                     detailsObj = ScannerTable.objects.all()
              except:
                     return Response("Not found in database")

              detailsObj.delete()
              return Response(200)   
class PrintergtinIndividual(APIView):
       def get(self, request, id):
        detailsObj = PrinterdataTable.objects.all().filter(gtin=id)
        serializeObj = PrinterSerializer(detailsObj, many=True)
        return Response(serializeObj.data)    

# class ScannerCommunicationView(AsyncWebsocketConsumer,APIView):
#        def get(self,request):
#               async def connect(self):
#                      await self.accept()
#                      # s = socket.socket()
#                      # port=2001
#                      # s.connect(('192.168.200.134', port))       
#               async def disconnect(self, close_code):
#                      pass
#               async def receive(self, text_data):
#                      pass
#               return Response(200)


class Reworkpostview(APIView):
 
    def post(self,request):
            serializeobj= ReworkSerializer(data=request.data)
            if serializeobj.is_valid():
                serializeobj.save()
                return Response(200)
            return Response(serializeobj.errors)
                                             
class ScannerStatusIndividual(APIView):
       def get(self, request, id):
       
        detailsObj = ScannerTable.objects.all().filter(gtin=id)
        serializeObj = ScannerSerializer(detailsObj, many=True)
        return Response(serializeObj.data)                              
                                                                  
class CountView(APIView):
                                     
                           
       def get(self,request):
                     # global c; 
                     s = socket.socket()
                     port=2001
                     s.connect(('192.168.200.134', port)) 
                     # data=s.recv(1024).decode()
                     # v=data[0]
                     # h=data[2:7]
                     # print(h)
                     l=[]
                     for i in range(10):
                            data=s.recv(1024).decode()
                            v=data[0]
                            h=data[2:7]
                            l.append(i)                  
                     print(len(l))
                            
                     return Response(len(l))
# ......................................................................

class Autovisionopenview(View):
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            os.system('start D:\Omron\AutoVision\AutoVISION.exe') 
            qs=PrinterdataTable.objects.get(id=id)
            # d=Viewprinterview.q.get()
            # print(qs.ip_address)
            form=PrinterForm(request.POST,instance=qs)
            obj = PrinterdataTable.objects.get(id=id)
            detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(preparebuttonresponse=1)

            # print(detailObj.responsefield)s:
            return  render(request,"scannersoftware.html",{"job":qs})
        else:
            return redirect("signin")
class Jobeditstopview(View):
       def get(self,request,id):
        qs=PrinterdataTable.objects.get(id=id)
        form=PrinterForm(instance=qs)
        return render(request,"cu-edit.html",{"form":form})

       def post(self,request,id):
        qs=PrinterdataTable.objects.get(id=id)
        form=PrinterForm(request.POST,instance=qs)
        if form.is_valid():                  
            form.save()
            return redirect("all-jobs") 
        else:
            return render(request,"cu-edit.html",{"form":form}) 
                        
class Demoview(ListView):
    model = PrinterdataTable
    context_object_name = "demos"
    template_name = "demo-list.html"
    # def get(self,request):
    #     qs=Jobs.objects.all()
    #     return render(request,"emp-listjob.html",{"jobs":qs})
    def get_queryset(self):
        return PrinterdataTable.objects.all() 
class listprinter(ListView):
    model = PrinterdataTable
    context_object_name = "jobs"
    template_name = "cu-list.html"
   
 
def searchBar(request):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            if request.method == 'GET':
                query = request.GET.get('query')
                # print(query)
                if query:
                    jobs = PrinterdataTable.objects.filter(gtin=query) 
                    return render(request, 'cu-list.html', {'page_obj':jobs,'search':1})
                else:
                    print("No information to show")
                    return render(request, 'cu-list.html', {})
        else:
            return redirect("signin")    
         
def listing(request) :
        hostname = socket.gethostname()
        systemip = socket.gethostbyname(hostname)
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""):
                           
            
            posts1 = PrinterdataTable.objects.all().filter(status="Running")
            if posts1:
                p = Paginator(posts1, 5)  
        
        
                page_num=request.GET.get('page',1)
           
            
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
           
                context = {'page_obj':page
                    }
                # return render(request, 'cu-list.html', context)                   
           
            else:
                posts = PrinterdataTable.objects.all().filter(ip_address=systemip)                        
                p = Paginator(posts, 5)  # creating a paginator object
            # getting the desired page number from url
            
                page_num=request.GET.get('page',1)
                # print(p.num_pages)
                
                try:
                    page=p.page(page_num)
                except EmptyPage:
                    page=p.page(1)
                # print(page)
                context = {'page_obj':page
                        } 
                
                            
            return render(request, 'cu-list.html', context)
        else:
            return redirect("signin")
 
class PauseClassview(View):
    pausestart=0
   
    # y=str(0)
    qu=Queue()
    event=Event()
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""):  
            qs=PrinterdataTable.objects.get(id=id)
            serial=qs.numbers
            serialno=json.loads(serial)
            form=PrinterForm(request.POST,instance=qs)
            obj = PrinterdataTable.objects.get(id=id)
            detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(label_response=0,start_pause_btnresponse=0)
            print(obj.start_pause_btnresponse)
            serilength=len(serialno)
            print(serilength)
            return render(request,"pause-start.html",{"qs":qs,'lp':1,"sc":serilength,})
        else:
            return redirect("signin")
        
    # def get(self,request):
    #     qs=Jobs.objects.all()
    #     return render(request,"emp-listjob.html",{"jobs":qs})
   
    def printerfun1(self,num,serialno,qu,event,gtin,lot,expire,hrfkey,hrfvalue,type,id):
        self.serialno=serialno
        self.gtin=gtin
        self.expire=expire
        self.lot=lot
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.type=type  
        self.id=id
        print(hrfvalue)
        print(hrfkey)
     
        
        slle=len(serialno)                   
        s = socket.socket()
        port=34567
        s.connect(('192.168.200.150', port))
      
        
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(start_pause_btnresponse=1)
        # message51= "I6\x04"
        # # "I6\x04"
        # s.send(message51.encode()) 
        # data51=s.recv(1024).decode() 
        # dataex=int(data51[:-1])
        
        # message53= "K8\x04"
      
        # s.send(message53.encode()) 
        # data53=s.recv(1024).decode() 
        # data53ex=data53[:-1]
        # print(data52ex)
        # if(dataex==100):
        #      return redirect("printer-errors") 
        # message52= "K7\x04"
        # # "I6\x04"
        # s.send(message52.encode()) 
        # data52=s.recv(1024).decode() 
        # print(data52)
        
        
        # data51extract= data51[:-4]
        # print(data51)
        # if(data51>0):
        #     return redirect("printer-errors")               
       
        
        # detailsobj2 = PrinterdataTable.objects.get(id=id) 
        # prodObj=ProductionOrder.objects.get(gtin_number=detailsobj2.gtin)
        # detailObj3=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Running")
        # print(obj.start_pause_btnresponse)
        # else:
        # message100= "QAM,5\x04"
        # s.send(message100.encode()) 
        # data100=s.recv(1024).decode() 
        # print("data100"+data100) 
        if(type=="type2"):
                                    
                message= "L,new7.lbl\x04"
                s.send(message.encode()) 
                data=s.recv(1024).decode()  
                message1= "E\x04"        
                s.send(message1.encode()) 
                data1=s.recv(1024).decode()
                
                   
                
                
                n=2
                d1=0
                a=0
                b=1 
                c=0
                d=5             
                upjso=[]                        
                while(n>0):
                        
                            if(PauseClassview.qu.empty()):
                                                                    
                                if d1==1:
                                    # while (n>0):
                                        
                                        for f in range(c,d):
                                            for sn in serialno[a:b]:              
                                            # for sn in kh:
                                                
                                                # print(a)
                                                message5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                                s.send(message5.encode()) 
                                                data5=s.recv(1024).decode()
                                                                        # print(slno)                    
                                                                
                                                message6= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                s.send(message6.encode()) 
                                                data6=s.recv(1024).decode() 
                                                                                
                                                message4= "F2\x04"
                                                s.send(message4.encode()) 
                                                data4=s.recv(1024).decode()
                                                
                                                a=a+1
                                                b=b+1   
                                            c=d
                                            d=d+5
                                        
                                # print('Received from server5: ' + data5)
                                # print('Received from server6: ' + data6)         
                                # print('Received from server4: ' + data4)    
                            else:
                                d1=PauseClassview.qu.get()
                                # print("podo")
                                # print(d1)
                                
                                if d1==0:
                                        a=0
                                        b=1 
                                        c=0
                                        d=5
                                        s8 = socket.socket()
                                        port8=34567
                                        s8.connect(('192.168.200.150', port8)) 
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(start_pause_btnresponse=0,label_response=1)
                                        
                                        detailsObj = PrinterdataTable.objects.get(id=id) 
                                        prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                                        detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused") 
                                        message32="QAF\x04"
                                        s8.send(message32.encode()) 
                                        data36=s8.recv(1024).decode()
                                        # print(data36) 
                                        break
                                                        
                                                    
                                                                    
                                        
                                        
                                        
                                        
                                    
                        
                        
                        
                        
                        
                        
        elif(type=="type5"):
                        #  print("hi")
                      
                        message7= "L,new8.lbl\x04"
                        s.send(message7.encode()) 
                        data7=s.recv(1024).decode()  
                        message8= "E\x04"        
                        s.send(message8.encode()) 
                        data8=s.recv(1024).decode()
                        
                        detailsobj2 = PrinterdataTable.objects.get(id=id) 
                        prodObj=ProductionOrder.objects.get(gtin_number=detailsobj2.gtin)
                        detailObj3=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Running")
                        
                                    
                        n1=2
                        d1=0
                        a1=0
                        b1=1 
                        c1=0
                        d2=5             
                        upjso=[]
                                            
                        while (n1>0):
                                
                                    if(PauseClassview.qu.empty()):
                                                                            
                                        if d1==1:
                                            # while (n>0):
                                                
                                                for f in range(c1,d2):
                                                    for sn in serialno[a1:b1]:              
                                                    # for sn in kh:
                                                        
                                                        # print(sn)
                                                        message9= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                                                        s.send(message9.encode()) 
                                                        data9=s.recv(1024).decode()
                                                        # print(a1)
                                                        
                                                        #     print(upjso)
                                                        # print(slno)                    
                                                        # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                                        message10= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "(45)" + hrfvalue + "\x09" + "Exp"+ "\x09" + expire + "\x09" + "Lot" + "\x09" + lot + "\x09" + "Gtin" + "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                                                        s.send(message10.encode()) 
                                                        data10=s.recv(1024).decode() 
                                                                
                                                        message11= "F2\x04"
                                                        s.send(message11.encode()) 
                                                        data11=s.recv(1024).decode()
                                                
                                                        # print(a1)
                                                        # # serialno[a1:b1]
                                                        # upjso.append(serialno[a1:b1])
                                                        # jso=json.dumps(upjso)
                                                        # # print(jso)
                                                        
                                                        # obj = PrinterdataTable.objects.get(id=id)
                                                        # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(printed_numbers=jso)
                                                        
                                                        a1=a1+1
                                                        b1=b1+1
                                                        
                                                    c1=d2
                                                    d2=d2+5
                                            
                                        # print('Received from server5: ' + data5)
                                        # print('Received from server6: ' + data6)         
                                        # print('Received from server4: ' + data4)    
                                    else:
                                        d1=PauseClassview.qu.get()
                                        # print("podo")
                                        # print(d1)
                                        
                                        if d1==0:
                                                a1=0
                                                b1=1 
                                                c1=0
                                                d2=5
                                                s8 = socket.socket()
                                                port8=34567
                                                s8.connect(('192.168.200.150', port8))  
                                                obj = PrinterdataTable.objects.get(id=id)
                                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(start_pause_btnresponse=0,label_response=1)
                                                
                                                detailsObj = PrinterdataTable.objects.get(id=id) 
                                                prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                                                detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused")
                                                message32="QAF\x04"
                                                s8.send(message32.encode()) 
                                                data36=s8.recv(1024).decode()
                                                # print(data36) 
                                                break
                                
                                
                                
                                
                                    # print(sn)
                                    # serialno.remove(sn)
                                    
                                    
                                    
                                    
                        # print(serialno)
                        #  print('Received from server: ' + data7)
                        #  print('Received from server: ' + data8) 
                        #  print('Received from server: ' + data9)
                        #  print('Received from server: ' + data10)         
                        #  print('Received from server: ' + data11)
        elif(type=="type1"):
                        message12= "L,new5.lbl\x04"
                        s.send(message12.encode()) 
                        data12=s.recv(1024).decode()  
                        message13= "E\x04"        
                        s.send(message13.encode()) 
                        data13=s.recv(1024).decode()
                        n2=2
                        d1=0
                        a2=0
                        b2=1 
                        c2=0
                        d3=5             
                                            
                        while (n2>0):
                                
                                    if(PauseClassview.qu.empty()):
                                                                            
                                        if d1==1:
                                            # while (n>0):
                                                
                                                for f in range(c2,d3):
                                                    for sn in serialno[a2:b2]:              
                                                    # for sn in kh:
                                                        
                                                        # print(a)
                                                        message14= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                                        s.send(message14.encode()) 
                                                        data14=s.recv(1024).decode()
                                                        
                                                                # print(slno)                    
                                                                # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                                        message15= "QAC\x09"  + "(01)" + gtin + "(21)" + sn + "(10)" + lot + "(17)" + expire + "(45)" + hrfvalue + "\x09" + "Exp\x09" + expire + "\x09" + "Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                        # message15= "QAC\x09" + "(01)" +  gtin +  "(10)" + lot + "(17)" + expire +  "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                                        s.send(message15.encode()) 
                                                        data15=s.recv(1024).decode() 
                                                                        
                                                        message16= "F2\x04"
                                                        s.send(message16.encode()) 
                                                        data16=s.recv(1024).decode()
                                                            
                                                        a2=a2+1
                                                        b2=b2+1
                                                        
                                                    c2=d3
                                                    d3=d3+5      
                                    else:
                                        d1=PauseClassview.qu.get()
                                        # print("podo")
                                        # print(d1)
                                        
                                        if d1==0:
                                                a2=0
                                                b2=1 
                                                c2=0
                                                d3=5
                                                s8 = socket.socket()
                                                port8=34567
                                                s8.connect(('192.168.200.150', port8)) 
                                                obj = PrinterdataTable.objects.get(id=id)
                                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(start_pause_btnresponse=0,label_response=1)
                                                
                                                detailsObj = PrinterdataTable.objects.get(id=id) 
                                                prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
                                                detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Paused")
                                                message32="QAF\x04"
                                                s8.send(message32.encode()) 
                                                data36=s8.recv(1024).decode()
                                                # print(data36)
                                                
                                                break
                                        
                                    
                                    
                                    
                                    
                                  
                                                                 
                     
                                                       
                                
                    #  print('Received from server14: ' + data14)
                    #  print('Received from server15: ' + data15)         
                    #  print('Received from server16: ' + data16)
    

    def scannerfun1(self,num,serialno,qu,event):
        self.serialno=serialno                  
        counter=0
        d=0
        n=1
        s1 = socket.socket()
        port1=2001
        s1.connect(('192.168.200.134', port1))
        
        s = socket.socket()
        port=34567
        s.connect(('192.168.200.150', port))
        while True: 
            if(PauseClassview.qu.empty()):
                if d==1:
                    data=s1.recv(1024).decode() 
                    # time.sleep(4)
                    print(serialno[counter]) 
                    counter=counter+1
                    # print(counter)     
                time.sleep(1)    
            else:
                d=PauseClassview.qu.get()
                if d==0:
                    # if Viewprinterview.event.is_set():            
                    break
                # elif d==1:                   
                #     # data=s1.recv(1024).decode() 
                    # time.sleep(4)
                #     print(serialno[counter]) 
                #     counter=counter+1
                time.sleep(1)  
    def post(self,request,id):
        qs=PrinterdataTable.objects.get(id=id)
        form=PrinterForm(request.POST,instance=qs)
         
        gtin=qs.gtin 
        ponumber=qs.processordernumber
        expire =str(qs.expiration_date)
        lot=qs.lot 
        type=qs.type
        hrf=qs.hrf  
        # if type== "type1" or type == "type5":        
        #     hrf=qs.hrf          
        #     if hrf == "":        
        #         hrfvalue = ""
        #         hrfkey= ""
        #     elif hrf != "":
        # print(hrf)                           
        hrfjson=json.loads(hrf)
                # print(hrfjson) 
        hrf1value=hrfjson["hrf1value"]
        hrf1key=hrfjson["hrf1"]
        hrf2value=hrfjson["hrf2value"]
        hrf2key=hrfjson["hrf2"]  
        hrf3value=hrfjson["hrf3value"]
        hrf3key=hrfjson["hrf3"]        
                # print(hrf3key)
                # print(hrf3value)
        hrf4value=hrfjson["hrf4value"]
        hrf4key=hrfjson["hrf4"]
        hrf5key=hrfjson["hrf5"]
        hrf5value=hrfjson["hrf5value"]
        hrf6key=hrfjson["hrf6"]
        hrf6value=hrfjson["hrf6value"]
                # print(hrf5key)
                # print(hrf5value)
                # print(hrf1key)    
                # else:
                #     hrfkey="null"        
        if(hrf1value!=""):
            hrfvalue=hrf1value
                    
        elif(hrf2value!=""):
            hrfvalue=hrf2value
        elif(hrf3value!=""):
            hrfvalue=hrf3value
        elif(hrf4value!=""):
            hrfvalue=hrf4value
        elif(hrf5value!=""):
            hrfvalue=hrf5value
        elif(hrf6value!=""):
            hrfvalue=hrf6value 
        print(hrfvalue)    
        if(hrf1key!="" and hrf1key!="null"):
            hrfkey=hrf1key 
            # print(hrfkey)      
        elif(hrf2key!="" and hrf2key!="null"):
            hrfkey=hrf2key
            # print(hrfkey) 
        elif(hrf3key!="" and hrf3key!="null"):
            hrfkey=hrf3key
            # print(hrfkey) 
        elif(hrf4key!="" and hrf4key!="null"):
            hrfkey=hrf4key
            # print(hrfkey) 
        elif(hrf5key!="" and  hrf5key!="null"):
            hrfkey=hrf5key
            # print(hrfkey) 
        elif(hrf6key!="" and hrf6key!="null"):
            hrfkey=hrf6key 
            # print(hrfkey)                         
                # print("hrf1value is:"+ hrf1value)       
                # print(hrfkey)
                # print(hrfvalue)        
        # print(hrfkey)
        # print(hrfvalue)
        try:
            serial=qs.numbers
            serialno=json.loads(serial)
            serialnum=qs.numbers
            serilength=len(serialno)
            print(serilength)
        except:
            print("pause printing because serialnumber are empty")
            serilength=0
            
        s = socket.socket()
        port=34567
        s.connect(('192.168.200.150', port))
        
        message51= "I6\x04"
        # "I6\x04"
        s.send(message51.encode()) 
        data51=s.recv(1024).decode() 
        dataex=int(data51[:-1])
        # print(dataex)          
        message53= "K8\x04"
        s.send(message53.encode()) 
        data53=s.recv(1024).decode() 
        data53ex=data53[:-1]                    
        if(PauseClassview.pausestart==0):                     
            PauseClassview.pausestart=1 
            PauseClassview.qu.put(PauseClassview.pausestart)
            # print(PauseClassview.pausestart)
            x1 = threading.Thread(target=PauseClassview.printerfun1,args=(self,10,serialno, PauseClassview.qu, PauseClassview.event,gtin,lot,expire,hrfkey,hrfvalue,type,id,))
            # y1.start()
            # print("hi")
            x1.start()                        
        elif(PauseClassview.pausestart==1):
            PauseClassview.pausestart=0                    
            PauseClassview.qu.put(PauseClassview.pausestart)
            # print(PauseClassview.pausestart)
        return render(request, 'pause-start.html', {'qs': qs,'pd':1,"sc":serilength,"prer":dataex,"warningmess":data53ex})
         
    def get_queryset(self):
        return PrinterdataTable.objects.all()     
 
class Viewprinterview(View):
    threadstart=0
    pausestart=0
    
    q=Queue()
    event=Event()
    
    def get(self,request,id):
        # if not get_referer(request):
        #     raise HttpResponse(404)
           
        # else:
            uname = Loginmodel.objects.get(id=2)
            loginname=uname.loginuname
            if(loginname!=""):             
                qs=PrinterdataTable.objects.get(id=id)
                # d=Viewprinterview.q.get()
                # print(qs.ip_address)
                form=PrinterForm(request.POST,instance=qs)
                # obj = PrinterdataTable.objects.get(id=id)
                # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(stopbtnresponse=0)

                # print(detailObj.responsefield)
                return render(request,"cu-edit.html",{"qs":qs})
            else:
                return redirect("signin")
    
    
    def printerfun(self,num,serialno,q,event,gtin,lot,expire,hrfkey,hrfvalue,type,id):
        self.serialno=serialno
        self.gtin=gtin
        self.expire=expire
        self.lot=lot
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.type=type 
        self.id=id
                    
        s2 = socket.socket()
        port2=34567
        s2.connect(('192.168.200.150', port2))
        # print(type)
        
       
        if(type=="type2"):
                                
                    message= "L,new7.lbl\x04"
                    s2.send(message.encode()) 
                    data=s2.recv(1024).decode()  
                    message1= "E\x04"        
                    s2.send(message1.encode()) 
                    data1=s2.recv(1024).decode()
                    uy1=serialno[0:1]
                    
                    for sn in uy1:                
                    # for sn in serialno :
                           
                            
                            
                                   message5= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s2.send(message5.encode()) 
                                   data5=s2.recv(1024).decode()
                                   # print(slno)                    
                          
                                   message6= "QAC\x09" + "(17)"+expire+"(10)" + lot + "(01)" +  gtin + "(21)" + sn +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "Gtin\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s2.send(message6.encode()) 
                                   data6=s2.recv(1024).decode() 
                                          
                                   message4= "F2\x04"
                                   s2.send(message4.encode()) 
                                   data4=s2.recv(1024).decode()
                                   
                                   
                     # print(serialno)
                     
                    print('Received from server: ' + data5)
                    print('Received from server: ' + data6)         
                    print('Received from server: ' + data4)
                    # obj = PrinterdataTable.objects.get(id=id)
                    # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(label_response=data4[0]) 
                    
        elif(type=="type5"):
                    #  print("hi")
                     message7= "L,new8.lbl\x04"
                     s2.send(message7.encode()) 
                     data7=s2.recv(1024).decode()  
                     message8= "E\x04"        
                     s2.send(message8.encode()) 
                     data8=s2.recv(1024).decode()
                     uy2=serialno[0:1]
                     print(hrfkey)
                     print("hi")
                     print(hrfvalue)             
                     for sn in uy2: 
                        message9= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x09"+"hrf"+"\x09hrfvalue"+"\x04"
                        s2.send(message9.encode()) 
                        data9=s2.recv(1024).decode()
                                   # print(slno)                    
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                        message10= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn + "(45)"+ hrfvalue+ "\x09" + "Exp\x09" + expire + "\x09"+"Lot" + "\x09" + lot + "\x09" + "Gtin"+ "\x09" +  gtin + "\x09" + "Slno" + "\x09" + sn + "\x09" + hrfkey + "\x09" + hrfvalue + "\x04"
                        s2.send(message10.encode()) 
                        data10=s2.recv(1024).decode() 
                                          
                        message11= "F2\x04"
                        s2.send(message11.encode()) 
                        data11=s2.recv(1024).decode()
                                   # print(sn)
                                   # serialno.remove(sn)            
                     # print(serialno)
                     print('Received from server: ' + data7)
                     print('Received from server: ' + data8) 
                     print('Received from server: ' + data9)
                     print('Received from server: ' + data10)         
                     print('Received from server: ' + data11)
                    #  obj = PrinterdataTable.objects.get(id=id)
                    #  detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(label_response=data11[0]) 
        elif(type=="type1"):
                     message12= "L,new5.lbl\x04"
                     s2.send(message12.encode()) 
                     data12=s2.recv(1024).decode()  
                     message13= "E\x04"        
                     s2.send(message13.encode()) 
                     data13=s2.recv(1024).decode()
                     uy=serialno[0:1]               
                     for sn in uy:
                                   message14= "QAH\x09datamatrix\x09gtin1\x09gtinvalue\x09"+ "lot\x09" +"lotvalue\x09"+"exp\x09"+"exp1\x09"+"slno\x09"+"slnovalue\x04"
                                   s2.send(message14.encode()) 
                                   data14=s2.recv(1024).decode()
                                   # print(slno)                    
                                   # message6= "QAC\x09" + "55555777779(10)45612(21)\x09GTIN\x09" + gtin+"\x09"+ "lot\x09" + lot +"\x09" +"exp\x09" + expire+"\x09"+"serialno\x09"+sn+"\x04"
                                   message15= "QAC\x09" + "(17)" + expire + "(10)" + lot + "(01)" +  gtin + "(21)" + sn +"(45)"+ hrfvalue +  "\x09" + "Exp\x09" + expire + "\x09Lot" + "\x09" + lot + "\x09" + "GTIN\x09" +  gtin + "\x09Slno" + "\x09" + sn + "\x04"
                                   s2.send(message15.encode()) 
                                   data15=s2.recv(1024).decode() 
                                          
                                   message16= "F2\x04"
                                   s2.send(message16.encode()) 
                                   data16=s2.recv(1024).decode()
                                   # print(sn)
                                   # serialno.remove(sn)
                            
                                   
                         
                     # print(serialno)
                     
                     print('Received from server: ' + data14)
                     print('Received from server: ' + data15)         
                     print('Received from server: ' + data16)
                    #  print(data16[0])
                    #  obj = PrinterdataTable.objects.get(id=id)
                    #  detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(label_response=data16[0])
                    #  print(obj.label_response) 

    def scannerfun(self,num,id,gtin,serialno,sl,printednumbers,q,event,lot,expire,hrfkey,hrfvalue,ip_address,child_numbers):
        self.id=id                    
        self.serialno=serialno
        self.sl=sl
        self.printednumbers=printednumbers
        # print(printednumbers)
        self.gtin=gtin
        self.lot=lot
        self.expire=expire
        self.hrfkey=hrfkey
        self.hrfvalue=hrfvalue
        self.ip_address=ip_address
        self.child_numbers=child_numbers
        # print(gtin)                      
        counter=0
        d=0
        co=-1
        n=1
        s3 = socket.socket()
        port4=2001
        s3.connect(('192.168.200.134', port4))
        s3.settimeout(5)
        
        s4 = socket.socket()
        port=34567
        s4.connect(('192.168.200.150', port))
        
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin)
        print(obj.printed_numbers)
        
        sllen=len(sl)
        print("sllen count")
        print(sllen)
        upjso=[]
        # upjso.append(obj.printed_numbers)
        cd=0
        drg=[]  
        # try: 
        #     data=s3.recv(1024).decode()
        # except:
        #         print("scanner is  not responding")
        #         return redirect("scanner-message")   
        while True: 
           
                if(Viewprinterview.q.empty()):
                    try:          
                        data=s3.recv(1024).decode()
                                         
                                         
                        v=data[0]
                        meanconfidence=data[2:7]
                        confidence=data[1]
                        textbatch=data[4:18]
                        print(textbatch)                
                                         
                        if d==1:
                            
                            # time.sleep(4)
                            # print(sl[counter])
                            try:
                                upjso.append(sl[counter])
                            except:
                                print("No serialnumbers available for printing")
                               
                            serilength=len(serialno)
                            # print(serilength)
                            try:
                                if(v=="4" and confidence=="1" and meanconfidence>="0.800"):
                                            grade="A"
                                elif(v=="3" and confidence=="1" and meanconfidence>="0.800"):
                                            grade="B"
                                elif (v=="2" and confidence=="1" and meanconfidence>="0.800"):
                                            grade="C"
                                elif (v=="1" and confidence=="1" and meanconfidence>="0.800"):
                                            grade="D"
                                else:
                                            grade="F" 
                                            
                                r={"serialnumber":sl[counter],
                                            "grade":grade}
                                if(gtin==textbatch):
                                    print(r)
                                    b=json.dumps(r)
                                    gradeupdation=ScannerTable(
                                    #    id=idcount, 
                                    gtin=gtin,
                                    ip_address=ip_address,
                                    grade=b,
                                    status="NO"
                                    )
                                    gradeupdation.save()
                                    obj = PrinterdataTable.objects.get(id=id)
                                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(scannergradefield=b)
                                    jso=json.dumps(upjso)
                                # print(jso)
                                    serialno.remove(sl[counter])
                                    gh=json.dumps(serialno)
                                    print(sl[counter])
                                    obj = PrinterdataTable.objects.get(id=id)
                                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(printed_numbers=jso,numbers=gh)
                                    updatedjson=json.loads(jso)
                                    # if d==0:
                                    #     break 
                                    
                                    
                                    
                                    if(counter==sllen-1):
                                        print(serialno)                    
                                        del serialno[:]
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(numbers=serialno)                  
                                        print("detecte serialnumber cleared")     
                                    counter=counter+1
                                else:
                                                        
                                    print("not equal")
                                    r={"serialnumber":sl[counter],
                                            "grade":"Not Detected"}
                                    print(r)
                                    b=json.dumps(r)
                                    gradeupdation=ScannerTable(
                                    #    id=idcount, 
                                    gtin=gtin,
                                    ip_address=ip_address,
                                    numbers=b,
                                    status="NO"
                                    )
                                    gradeupdation.save()
                                    obj = PrinterdataTable.objects.get(id=id)
                                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(scannergradefield=b)
                                    jso=json.dumps(upjso)
                                    # vpo=[]
                                    # vpo.append(child_numbers)
                                    # jso.insert(0,sl[counter]+child_numbers)
                                    # vpojson=json.dumps(jso)
                                    
                                    
                                    # print(jso)
                                  
                                    serialvar=sl[counter]
                                    serialno.remove(sl[counter])
                                    serialno.append(serialvar)
                                    
                                    drg.append(serialvar)
                                    drgjson=json.dumps(drg)
                                    gh=json.dumps(serialno)
                                    
                                            
                                  
                                    # serialno.remove(sl[counter])
                                  
                                    # ph=json.dumps(serialno)
                                    
                                    obj = PrinterdataTable.objects.get(id=id)
                                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(numbers=gh,child_numbers=drgjson)
                                    
                                   
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                   
                                    
                                    # th=json.dumps(serialno)
                                    
                                    # obj = PrinterdataTable.objects.get(id=id)
                                    # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(numbers=th,child_numbers=th)
                                   
                            
                                    # print(counter)
                                    if(counter==sllen-1):
                                        print(serialno)                    
                                        del serialno[:]
                                        obj = PrinterdataTable.objects.get(id=id)
                                        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(numbers=serialno)
                                        print("not detecte serialnumber cleared")                  
                                    counter=counter+1
                                
                                    
                                    
                                                            
                            
                            except:
                                print("serialnumbers finished")
                                
                                # del serialno[:]
                                # obj = PrinterdataTable.objects.get(id=id)
                                # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(numbers=serialno)
                                # print("serialnumbers list cleared")
                         
               
                                
                                
                
                    
                        
                        
                        # jso=json.dumps(upjso)
                        # # print(jso)
                        # serialno.remove(sl[counter])
                        # gh=json.dumps(serialno)
                        # print(sl[counter])
                        # obj = PrinterdataTable.objects.get(id=id)
                        # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(printed_numbers=jso,numbers=gh)
                        # updatedjson=json.loads(jso)
                        # # if d==0:
                        # #     break 
                        # counter=counter+1
                        # # idcount=idcount+1
                    except socket.timeout:
                        print("Didn't receive data! [Timeout 5s]")      
                        
                        
                  
                    # time.sleep(1)    
                else:
                        d=Viewprinterview.q.get()
                        print(d)
                        if d==0:
                                # if(gtin==textbatch):                
                                #     upjso.remove(sl[counter-1])
                                #     jso=json.dumps(upjso) 
                                #     serialno.insert(0,sl[counter-1]) 
                                #     # serialno.append(sl[counter-1])
                                #     gh=json.dumps(serialno)
                                #     print(serialno)
                                #     obj = PrinterdataTable.objects.get(id=id)
                                #     detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(printed_numbers=jso,numbers=gh) 
                                # else:        
                                print("Batch stop But Not update")
                                                                   
                            
                                
                                
                                
                                            
                                message30= "F0\x04"
                                s4.send(message30.encode()) 
                                data30=s4.recv(1024).decode()
                                obj = PrinterdataTable.objects.get(id=id)
                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(stopbtnresponse=1,return_slno_btn_response=0,status="Stopped")
                                        
                                detailsObj1 = PrinterdataTable.objects.get(id=id) 
                                prodObj=ProductionOrder.objects.get(gtin_number=detailsObj1.gtin)
                                detailObj2=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Closed")
                                        
                                obj = PrinterdataTable.objects.get(id=id)
                                detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(responsefield=0)
                                                    
                                break
                                 
                    
                        # time.sleep(1)
        
                       
        # print(counter)                      
                # elif d==0:
                #     break
                            
    def post(self,request,id):
        # global y  
        # self.running=True 
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""):                 
            qs=PrinterdataTable.objects.get(id=id)
            form=PrinterForm(request.POST,instance=qs)
            form2=PrinterForm(request.POST,instance=qs)
            
            id=qs.id    
            gtin=qs.gtin 
            ponumber=qs.processordernumber
            expire =str(qs.expiration_date)
            lot=qs.lot
            type=qs.type
            hrf=qs.hrf 
            printednumbers=qs.printed_numbers
            ip_address=qs.ip_address
            child_numbers=qs.child_numbers
            print(printednumbers) 
                                        
            hrfjson=json.loads(hrf) 
            hrf1value=hrfjson["hrf1value"]
            hrf1key=hrfjson["hrf1"]
            hrf2value=hrfjson["hrf2value"]
            hrf2key=hrfjson["hrf2"]
            hrf3value=hrfjson["hrf3value"]
            hrf3key=hrfjson["hrf3"]
            hrf4value=hrfjson["hrf4value"]
            hrf4key=hrfjson["hrf4"]
            hrf5key=hrfjson["hrf5"]
            hrf5value=hrfjson["hrf5value"]
            hrf6key=hrfjson["hrf6"]
            hrf6value=hrfjson["hrf6value"]
            if(hrf1key!="" or hrf1key!="null"):
                hrfkey=hrf1key
            elif(hrf2key!="" or hrf2key!="null"):
                hrfkey=hrf2key
            elif(hrf3key!="" or hrf3key!="null"):
                hrfkey=hrf3key
            elif(hrf4key!="" or hrf4key!="null"):
                hrfkey=hrf4key
            elif(hrf5key!="" or hrf5key!="null"):
                hrfkey=hrf5key
            elif(hrf6key!="" or hrf6key!="null"):
                hrfkey=hrf6key
            else:
                hrfkey="null"
            if(hrf1value!="" or hrf1value!="null"):
                hrfvalue=hrf1value
            elif(hrf2value!="" or hrf2value!="null"):
                hrfvalue=hrf2value
            elif(hrf3value!="" or hrf3value!="null"):
                hrfvalue=hrf3value
            elif(hrf4value!="" or hrf4value!="null"):
                hrfvalue=hrf4value
            elif(hrf5value!="" or hrf5value!="null"):
                hrfvalue=hrf5value
            elif(hrf6value!="" or hrf6value!="null"):
                hrfvalue=hrf6value
            else:
                hrfvalue="null"
            print(hrfkey)
            print(hrfvalue)
            try:    
                serial=qs.numbers
                serialnum=qs.numbers
                serialno=json.loads(serial)
                sl=json.loads(serialnum)
            except:
                print("No serialnumber available inviewprinterview")
                    
            # sk=len(sl)
            # print(sk)
            # print(serialno[0:10])
            # childjson= json.dumps(serialno[0:10])
            # obj = PrinterdataTable.objects.get(id=id)
            # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(child_numbers=childjson)
            # childserialnum=qs.child_numbers
            # print(childserialnum)
            # childsl=json.loads(childserialnum)
            # so1=json.dumps(serialno[11:13])
            # obj = PrinterdataTable.objects.get(id=id)
            # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(child_numbers=so1)
            
            
            
            
            
        
            # v=Viewprinterview() 
            # obj = PrinterdataTable.objects.get(id=id)
            
            # detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(responsefield=0)
            try:
                s5 = socket.socket()
                port1=2001
                s5.connect(('192.168.200.134', port1))
            except:
                return redirect("scanner-message")
            try:
                s4 = socket.socket()
                port=34567
                s4.connect(('192.168.200.150', port))
                message52= "K7\x04"
        
                s4.send(message52.encode()) 
                data52=s4.recv(1024).decode() 
                data52ex=data52[:-1]
                print(data52ex)
                
            
                
                
                if(Viewprinterview.threadstart==0):
                                        
                    
                    # print(data10)
                    
                    if  TimeoutError:
                        messages.success(request,"your application has posted successfully")                
                                        
                    obj = PrinterdataTable.objects.get(id=id)
                
                    detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(responsefield=1,stopbtnresponse=0,return_slno_btn_response=1,status="Running")                     
                    Viewprinterview.threadstart=1
                    Viewprinterview.q.put(Viewprinterview.threadstart)
                    
                    # print(Viewprinterview.threadstart)
                    y = threading.Thread(target=self.scannerfun,args=(10,id,gtin,serialno,sl,printednumbers,Viewprinterview.q,Viewprinterview.event,lot,expire,hrfkey,hrfvalue,ip_address,child_numbers))
                    x = threading.Thread(target=self.printerfun,args=(10,serialno,Viewprinterview.q,Viewprinterview.event,gtin,lot,expire,hrfkey,hrfvalue,type,id))
                    y.start()
                    x.start()
                    # (print("hi"))
                    # sd=Viewprinterview.q.get()    
                    # self.get_context_data(Viewprinterview.q)                        
                elif(Viewprinterview.threadstart==1):
                    Viewprinterview.threadstart=0                    
                    Viewprinterview.q.put(Viewprinterview.threadstart)
                    # v.terminate()
                    # print(Viewprinterview.threadstart)
                    Viewprinterview.event.set()
                    
                    
                    return redirect("batch-stop-message")
                
                    
                # sd=Viewprinterview.q.get()     
                # return HttpResponse(200)
                
                return render(request, 'cu-edit.html', {'sd':1,'qs': qs,'yu':0,'errormess':data52ex})
            except:
                print("An exception occurred")
                # messages.success(request, "Please Turn On the Printer")
                return redirect("cand-home")
        else:
            return redirect("signin")    
        
class Candidatehomeview(TemplateView):
                                template_name = "messagepage.html"
            
            
class Scannermessageview(TemplateView):
            template_name = "Scannermessage.html"

class Batchstopmessageview(TemplateView):
    
                  
        template_name = "Batch-stop-message.html"                       
class Errorview(TemplateView):
                        
       
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            template_name = "printererror.html" 
        
class Scannersoftwareview(TemplateView):
                                            
            
        template_name = "scannersoftware.html"            
    
                          
class Returnserialnumbers(View):
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            qs=PrinterdataTable.objects.get(id=id)
            form=PrinterForm(request.POST,instance=qs)
            y=[]
            y1=[]
            detailsObj = PrinterdataTable.objects.get(id=id)
            prodObj=PrinterdataTable.objects.get(gtin=detailsObj.gtin)
            serialno=prodObj.numbers
            
            if(serialno!=[]):
                detailObj2=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(balanced_serialnumbers=serialno,status="Printed")
                y.clear()
                obj = PrinterdataTable.objects.get(id=id)
                detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(numbers=y)   
            else:
                try:
                    child_number=prodObj.child_numbers
                    childnojson=json.loads(child_number)
                    # print(childnojson)
                    
                except:
                    print("no child_numbers")
                    childnojson=[] 
                y1.append(serialno+childnojson)
                y2 = list(np.concatenate(y1))
                print(y2)
                newjson=json.dumps(y2)
                obj = PrinterdataTable.objects.get(id=id)
                detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(balanced_serialnumbers=newjson,status="Printed")
                y2.clear()
                obj = PrinterdataTable.objects.get(id=id)
                detailObj=PrinterdataTable.objects.filter(gtin=prodObj.gtin).update(child_numbers=y2)
                  
            return render(request,"returnserial.html",{"qs":qs})                              
        else:
            return redirect("signin")                       
                                
        
                          

class ReturnsnGet(View):
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""): 
            qs=PrinterdataTable.objects.get(id=id)
            # d=Viewprinterview.q.get()
            # print(qs.ip_address)
            form=PrinterForm(request.POST,instance=qs)
            return render(request,"returnserial.html",{"qs":qs})
        else:
            return redirect("signin") 
                    
                    
                    
class Nextserialno(Viewprinterview):
    so1=[]                  
    def get(self,id):
        qs=PrinterdataTable.objects.get(id=id)
        serialno=qs.numbers
       
        serial=json.loads(serialno)
        print(serial[11:14])
        # form=PrinterForm(request.POST,instance=qs)
        so1=json.dumps(serial[11:14])
        print(so1)
        obj = PrinterdataTable.objects.get(id=id)
        
        detailObj=PrinterdataTable.objects.filter(gtin=obj.gtin).update(child_numbers=so1)
        return so1

class Getgradedata(ListView):
   def get(self,request):
        qs=ScannerTable.objects.all().order_by('-id')
        # fs=PrinterdataTable.objects.get(id=id)
        
        
        p = Paginator(qs, 2)  # creating a paginator object
    # getting the desired page number from url
       
        page_num=request.GET.get('page',1)
        # print(p.num_pages)
        
        try:
            page=p.page(page_num)
        except EmptyPage:
            page=p.page(1)
        # print(page)
        context = {'page_obj':  page,
                  }
        return render(request,"Grade.html",context)
    
class Gradecount(ListView):
    def get(self,request,id):
        uname = Loginmodel.objects.get(id=2)
        loginname=uname.loginuname
        if(loginname!=""):                     
            qs=PrinterdataTable.objects.get(id=id)
            try:
                val=qs.child_numbers
                serial=qs.numbers
                serialno=json.loads(serial)
                serialnum=qs.numbers
                serilength=len(serialno)
            
                print(val)
            except:
                print("no grade")
                serilength=0
        
            
            
        
            return render(request,"gradecount.html",{"qs":qs,"sc":serilength})       
        else:
            return redirect("signin")
class Serialnumberdownloadagainview(View):
    # def get(self,request,id):
    #     qs=PrinterdataTable.objects.get(id=id)
    #     # d=Viewprinterview.q.get()
    #     # print(qs.ip_address)
    #     form=PrinterForm(request.POST,instance=qs)
    #     return HttpResponse(200)                
                        
    def get(self,request,id):
                            
                           
                      
        qs=PrinterdataTable.objects.get(id=id)
        # print(qs.numbers)
        jsonArray=[]
        jsonArray=json.loads(qs.numbers)
        
        
        # print(jsonArray)
        # jsonString = json.dumps(jsonArray)
        #         # print(jsonString[0:10])
        # childjson= json.loads(jsonString)
        # s1=[]
        print(qs.child_numbers)
        jlo=json.loads(qs.child_numbers)
        
        # s1.append(qs.child_numbers)
        # s1.append(jsonArray[0:10])
        
        s2=json.dumps(jlo+jsonArray[0:10])
        # print(s2)
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(id=id).update(child_numbers=s2)
        
        
        
        
        
        del jsonArray[0:10]
        gh=json.dumps(jsonArray)
                # print(jsi)
                # jsonArray.remove(jsi)
                
        obj = PrinterdataTable.objects.get(id=id)
        detailObj=PrinterdataTable.objects.filter(id=id).update(numbers=gh)
        
        return HttpResponse(200)                

class Signinview(FormView):
    form_class = Loginform
    template_name = "login.html"
    def post(self,request,*args,**kwargs):
        form=Loginform(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
          
            
            # print(userrole)
            userData=Register.objects.filter(email=uname).values()
            try:
                ud=Register.objects.get(email=uname)
            # print(ud.userRole)
            except:
                print("An exception occurred")            
            
            if userData:
#                 if(userData[0]['password']== pwd):

                   userData1=""
                   userData1=Register.objects.filter(password=pwd).values()
                #    pd=Register.objects.get(password=pwd)
                #    print(pd.userRole)
                   
                  
                #    for ele in userData1:
                #         print(ele['userRole'])                   
                                            
                #    userData2=UserrolePermissions.objects.filter(activity_name="printerjobs").values()
                   if  userData1:
                            ud=Register.objects.get(email=uname)
                            print(ud.userRole)
                            # login(request,ud.userRole)
                           
                            bt=ud.userRole
                            uname=ud.Name
                            perm=UserrolePermissions.objects.filter(activity_name="printerjobs").values()
                            if bt=="admin":
                                if(perm[0]['admin']['READ']=="Checked"):
                                    obj = Loginmodel.objects.get(id=2)
                                    detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname)                     
                                    return  redirect("indexpage")
                                else:
                                     return HttpResponse ("Permission Denied!!!")                    
                            elif bt=="operator":
                                # print(perm[0]['operator']['READ'])
                                if(perm[0]['operator']['READ']=="Checked"):
                                      obj = Loginmodel.objects.get(id=2)
                                      detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname)                  
                                      return  redirect("indexpage")                   
                                                        
                                    #     hostname = socket.gethostname()
                                    #     systemip = socket.gethostbyname(hostname)
                                    #     posts = PrinterdataTable.objects.all().filter(ip_address=systemip)
                                    #     p = Paginator(posts, 5)  # creating a paginator object
                                    # # getting the desired page number from url
                                    
                                    #     page_num=request.GET.get('page',1)
                                    #     # print(p.num_pages)
                                        
                                    #     try:
                                    #         page=p.page(page_num)
                                    #     except EmptyPage:
                                    #         page=p.page(1)
                                    #     # print(page)
                                    #     context = {'page_obj':  page,
                                    #                'name':ud.Name} 
                                    #     return  render(request,'cu-list.html',context)
                                    # return render(request, 'scannersoftware.html', {'sd':ud.Name})
                                else:
                                     return HttpResponse ("Permission Denied!!!")  
                            elif bt=="supervisor":
                                                    # print(perm[0]['operator']['READ'])
                                if(perm[0]['supervisor']['READ']=="Checked"):
                                      obj = Loginmodel.objects.get(id=2)
                                      detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname)                     
                                      return  redirect("indexpage")
                                else:
                                     return HttpResponse ("Permission Denied!!!")
                            elif bt=="masterdata":
                                                    # print(perm[0]['operator']['READ'])
                                if(perm[0]['masterdata']['READ']=="Checked"):
                                      obj = Loginmodel.objects.get(id=2)
                                      detailObj=Loginmodel.objects.filter(id=2).update(loginuname=uname)                     
                                      return  redirect("indexpage")
                                else:
                                     return HttpResponse ("Permission Denied!!!")                            
                   else:
                      return HttpResponse ("Password is incorrect!!!")
            else:
                  return HttpResponse ("User does not exit")
           
        
        else:
          return render(request, 'login.html' )     
                  
 
def signout_view(request,*args,**kwargs):
        obj = Loginmodel.objects.get(id=2)
        detailObj=Loginmodel.objects.filter(id=2).update(loginuname="") 
        logout(request)
        return redirect("signin")
                          
                          
                          
                                                 
                     
                                                     
                     
                    
                                                
                     
              
                            
             