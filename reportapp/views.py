from rest_framework.views import APIView
from rest_framework.response import Response
from reportapp.serializers import ProductionReportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import ProductionReport
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class ProductionOrderReport(APIView):
    def get(self, request):
        detailsObj = ProductionReport.objects.all()
        serializeObj = ProductionReportSerializer(detailsObj, many=True)
        return Response(serializeObj.data)
    def post(self, request):
        serializeObj = ProductionReportSerializer(data=request.data)
       
        if serializeObj.is_valid():
            serializeObj.save()
          
           
           
            
            
            return Response(200)
        return Response(serializeObj.errors)

class ProductionOrderReportIndividual(APIView):
    def get(self, request, id):
        detailsObj = ProductionReport.objects.all().filter(batch_number=id)
        serializeObj = ProductionReportSerializer(detailsObj, many=True)
        return Response(serializeObj.data)
    #     try:
    #         detailsObj = ProductionReport.objects.get(batch_number=id)
    #     except:
    #         return Response("Not found in database")

    #     serializeObj = ProductionReportSerializer(detailsObj, data=request.data)
    #     if (serializeObj.is_valid()):
    #         return Response(serializeObj.data)

    #     return Response(serializeObj.errors)
    
    
class ProductionOrderReportdate(APIView):  
    def get(self, request):
        detailsObj = ProductionReport.objects.all()
        serializeObj = ProductionReportSerializer(detailsObj, many=True)
        # fromDate = request.data["datefrom"]
        # toDate = request.data["dateto"]
        # response  = ProductionReport.objects.filter( production_date=fromDate, production_date__lte=toDate)
        return Response(200)
    
    def post(self, request):
        serializeObj = ProductionReportSerializer(data=request.data)
        v=[]
        startdate = request.data["datefrom"]
        
        toDate = request.data["dateto"]
        # fromDate=str(request.POST.get('datefrom'))
        # toDate=str(request.POST.get("dateto"))
        # response  =ProductionReport.objects.all().filter(production_date=id)
        
        response  =ProductionReport.objects.all().filter(production_date__range=(startdate, toDate))
        serializeObj = ProductionReportSerializer(response , many=True)
        return Response(serializeObj.data)
     
        # if serializeObj.is_valid():
        #     v.append(response)                 
        #     print(v)
        #     return Response(response)
          
           
           
            
            
        # return Response(200)