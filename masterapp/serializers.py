from masterapp.models import PrinterdataTable,ProductionOrder,ScannerTable,ShipPO,Customers,Locations,ReworkTable
from rest_framework import serializers

class ProductionOrderSerializer(serializers.ModelSerializer):
                        
    class Meta:
        model = ProductionOrder
        fields =['id','process_order_number','serialnoprovider','batch_number','manufacturing_location','regulation','production_date',
        'expiration_date','packaging_Version','created_by','internal_material_number',"requested","produced","line","gtin_number","type","status"]
        
class LocationSerializer(serializers.ModelSerializer):
                        
    class Meta:
        model =Locations
        fields = ['id','customer_id','name','created_by','loc_gln','address','zip','state']        
        
        # fields="__all__"
class CustomersSerializer(serializers.ModelSerializer):
                        
    class Meta:
        model =Customers
        fields =['id','name','created_by','address','zip','group','country','state','city','status']        
        
class ShipPOSerializer(serializers.ModelSerializer):
                        
    class Meta:
        model = ShipPO
        fields="__all__"        

class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model=PrinterdataTable
        fields=["id","numbers","expiration_date","lot","gtin","processordernumber","quantity","hrf","type","status","ip_address","printed_numbers","balanced_serialnumbers","responsefield","preparebuttonresponse","stopbtnresponse","start_pause_btnresponse","pause_stop_btnresponse","return_slno_btn_response"]

# class CheckboxSerializer(serializers.ModelSerializer):
#         class Meta:
#                     model=PrinterdataTable
#                     fields=["id", "preparebuttonresponse","gtin"]
                                

class LoopStopSerializer(serializers.ModelSerializer):
    class Meta:
        model=PrinterdataTable
        fields=["id","numbers","gtin"]          
        
         
class ScannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=ScannerTable
        fields=["id","grade","gtin","status"]        
class ReworkSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReworkTable
        fields=["id","gtin","slnonumber","oldstatus","newstatus"]      