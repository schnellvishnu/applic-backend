from django.shortcuts import render
from accounts.models import Register,UserAuditHistoryOnly
from accounts.serializers import RegisterSerializer,UserHistorySerializer
from  rest_framework .views import APIView
from rest_framework .response import Response
from django.contrib.auth.models import User

# Create your views here.

class userAuthVerify(APIView):
           def post(self, request):
              userData=Register.objects.filter(email=request.data['username']).values()
              if userData:
                return Response(userData[0]['userRole'])
              else:
                return Response("notExists")    
                                      
class logInController(APIView): 
    def post(self, request):
        # print(request.data['username'])                   
        userData = Register.objects.filter(email=request.data['username']).values()
        
        if(userData):
            if(userData[0]['password'] == request.data['password']):
                
                return Response({'userrole':userData[0]['userRole'], 'username':userData[0]['email'],'employeeid':userData[0]['employeeid']})
            else:
                return Response("passwordDoesNotMatch") 
        else:
            return Response("UserDoesNotExist")
class Emailindividual(APIView):
    def get(self, request):
                    

        detailsObj =Register.objects.all()
        serializeObj = RegisterSerializer(detailsObj, many=True)
        return Response(serializeObj.data)              
    def post(self, request):
        password=request.data["password"]                      
        newpass=request.data["newpassword"]
        conpass=request.data["conpass"]# print(request.data['username'])                   
        userData = Register.objects.filter(email=request.data['username']).values()
        # detaiobj = Register.objects.filter(email=request.data['username']).update(password=newpass)
       
        
        if(userData):
            if(userData[0]['password'] == password ):
                if(newpass == conpass ):                  
                                   
                    detaiobj = Register.objects.filter(email=request.data['username']).update(password=newpass)             
                    return Response(200)
                else:
                    return Response("conpasswordDoesNotMatch")                     
                # return Response({'userrole':userData[0]['userRole'], 'username':userData[0]['email'],'employeeid':userData[0]['employeeid']})
            else:
                return Response("passwordDoesNotMatch") 
        else:
            return Response("UserDoesNotExist")
                                       


class UserAuditReportdate(APIView):  
    def get(self, request):
        detailsObj = UserAuditHistoryOnly.objects.all()
        serializeObj = UserHistorySerializer(detailsObj, many=True)
        # fromDate = request.data["datefrom"]
        # toDate = request.data["dateto"]
        # response  = ProductionReport.objects.filter( production_date=fromDate, production_date__lte=toDate)
        return Response(serializeObj.data)
    
    def post(self, request):
        serializeObj = UserHistorySerializer(data=request.data)
        v=[]
        startdate = request.data["datefrom"]
        
        toDate = request.data["dateto"]
        # fromDate=str(request.POST.get('datefrom'))
        # toDate=str(request.POST.get("dateto"))
        # response  =ProductionReport.objects.all().filter(production_date=id)
        
        response  =UserAuditHistoryOnly.objects.all().filter(datefield__range=(startdate,toDate) )
        serializeObj = UserHistorySerializer(response , many=True)
        return Response(serializeObj.data)
    
    
   
        
