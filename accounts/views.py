from django.shortcuts import render
from accounts.models import Register,UserAuditHistoryOnly,UserrolePermissions,History
from accounts.serializers import RegisterSerializer,UserHistorySerializer,UserrolePermissionsSerializer,HistorySerializer
from  rest_framework .views import APIView
from rest_framework .response import Response
from django.contrib.auth.models import User
import datetime
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
                historySave = History(modelname='Login Details',

                savedid="noid",

                operationdone='Login Application Server',

                donebyuser=userData[0]['Name'],

                donebyuserrole=userData[0]['userRole'],

                donedatetime=datetime.datetime.now(),

                # historyText="Loggedin the user " +userData[0]['Name']+ ", whose role is " + userData[0]['userRole'])
                )
                historySave.save() 
                
                userhistorySave = UserAuditHistoryOnly(modelname='Login Details',

                

                operationdone='Login Application Server',

                donebyuser=userData[0]['email'],

                donebyuserrole=userData[0]['userRole'],

                donedatetime=datetime.datetime.now(),

                # historyText="Loggedin the user " +userData[0]['Name']+ ", whose role is " + userData[0]['userRole'])
                )
                userhistorySave.save() 
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
                    historySave = History(modelname='Register',

                    savedid="noid",

                    operationdone='Password Changed',

                    donebyuser=userData[0]['Name'],

                    donebyuserrole=userData[0]['userRole'],

                    donedatetime=datetime.datetime.now(),

                # historyText="Loggedin the user " +userData[0]['Name']+ ", whose role is " + userData[0]['userRole'])
                    )
                    historySave.save()               
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
    
    
class UserrolePermissionsRead(APIView):
    def get(self, request):
        detailsObj = UserrolePermissions.objects.all().order_by('id')
        serializeObj = UserrolePermissionsSerializer(detailsObj, many = True)
        return Response(serializeObj.data)
    
#-------------------------------------------------------------------------------
class AuditLogView(APIView):
    def get(self, request):
        detailsObj = History.objects.all()
        serializeObj = HistorySerializer(detailsObj, many = True)
        return Response(serializeObj.data)

class HistoryemployeandmodelIndividual(APIView):
                                        
    def get(self, request,id):
        # email=request.data["email"]
                          
        detailsObj = History.objects.all().filter(donebyemployeeid=id).order_by('-id')
       
        serializeObj = HistorySerializer(detailsObj, many = True)
        return Response(serializeObj.data)
                            

class HistoryemployeandmodelnameIndividual(APIView):
                                        
    def get(self, request,id):
        # email=request.data["email"]
                          
        detailsObj = History.objects.all().filter(modelname=id).order_by('-id')
       
        serializeObj = HistorySerializer(detailsObj, many = True)
        return Response(serializeObj.data)
 
class HistoryIndividual(APIView):
    def get(self, request, id):
        detailsObj =History.objects.all().filter(donebyuserrole=id).order_by('-id')
        serializeObj = HistorySerializer(detailsObj, many=True)
        return Response(serializeObj.data)
    
    
                            
class deleteAuditlog(APIView):
    def delete(self, request, pk):
        try:
            detailsObj = History.objects.get(pk=pk)
        except:
            return Response("Not found in database")

        detailsObj.delete()
        return Response(200)
class RegisterIndividual(APIView):
    def get(self, request, id):
        detailsObj =Register.objects.all().filter(email=id).order_by('-id')
        serializeObj = RegisterSerializer(detailsObj, many=True)
        return Response(serializeObj.data)


class logoutController(APIView):
                    
    def post(self,request):

        username=request.data["username"]

        userrole=request.data["userrole"]

        historySave = History(modelname='LogOut Details',

                            savedid="noid",

                            operationdone='Logout in Applicationserver',

                            donebyuser=username,

                            donebyuserrole=userrole,

                            donedatetime=datetime.datetime.now(),

                            # historyText="Loggedout the user " +username+ ", whose role is " + userrole)
                            )
        historySave.save()
        
        userhistorySave = UserAuditHistoryOnly(modelname='Login Details',

                

                

                            operationdone='logout in Application Server',

                            donebyuser=username,

                            donebyuserrole=userrole,

                            donedatetime=datetime.datetime.now(),

                # historyText="Loggedin the user " +userData[0]['Name']+ ", whose role is " + userData[0]['userRole'])
                )
        userhistorySave.save() 

        return Response(200)    
   
        
