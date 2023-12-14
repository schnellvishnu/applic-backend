from django.shortcuts import render
from masterapp .models import PrinterdataTable,ProductionOrder,ScannerTable,ShipPO,Customers,Locations
from masterapp.serializers import PrinterSerializer,ProductionOrderSerializer,ScannerSerializer,LoopStopSerializer,ShipPOSerializer,CustomersSerializer,LocationSerializer
from  rest_framework .views import APIView
from rest_framework .response import Response
import socket
import json
from urllib.request import urlopen
import re as r
import threading
from django.http import HttpResponse
import itertools
from channels.generic.websocket import AsyncWebsocketConsumer
# import threading
import time
# import sys
# import os
import requests
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
              s = socket.socket()
              port=34567
              s.connect(('192.168.200.150', port))
              
              message20= "F0\x04"
              s.send(message20.encode()) 
              data20=s.recv(1024).decode() 
              
              detailsObj = PrinterdataTable.objects.get(id=id) 
              prodObj=ProductionOrder.objects.get(gtin_number=detailsObj.gtin)
              detailObj=ProductionOrder.objects.filter(gtin_number=prodObj.gtin_number).update(status="Closed")
              # serializeobj=PrinterdataTable(data=request.data)
              # if serializeobj.is_valid():
              #        serializeobj.save()
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
class Deletescanner(APIView):
       def get(self, request):
              try:
                     detailsObj = ScannerTable.objects.all()
              except:
                     return Response("Not found in database")

              detailsObj.delete()
              return Response(200)       

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
                                             
                            
                                                                  
              
             