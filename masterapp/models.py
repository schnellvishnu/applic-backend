from django.db import models

# Create your models here.
batch_status =(('Draft','Draft'), ('Inproduction','Inproduction'),('Running','Running')
        ,('Paused','Paused'), ('Shipping','Shipping'),('InShipping','InShipping'),  ('Closed','Closed'), ('Fullyreleased','Fullyreleased'),)
group_choices = ( ('CMO','CMO'),('CPO','CPO'),('Customer','Customer'),('Destroyer','Destroyer'),('Hospital','Hospital')
                    ,('Manufacture','Manufacture'),('Pharmacy','Pharmacy'),('Transporter','Transporter'),('Warehouse','Warehouse')
                    ,('Wholesaler','Wholesaler'))
class ProductionOrder(models.Model):
                        
    def namefile(instance,filename):
        return '/'.join(['image',str(instance.manufacturing_location),filename])                    
    id = models.AutoField(primary_key=True)
    process_order_number = models.CharField(max_length= 20, unique= True)
    created_by = models.CharField(max_length =100)
#     product_conn = models.ForeignKey(Product, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    batch_number = models.CharField(max_length=20,unique=True)
    manufacturing_location = models.CharField(max_length=40)
    gln_number =models.CharField(max_length=40,unique=True,null=True)
#     Production_line_id = models.ForeignKey(RegisteredSystem, related_name='productionline_to_batch', on_delete=models.CASCADE)
    # product_identifier = models.CharField(max_length=100)
    regulation = models.CharField(max_length=100,default=True)
    production_date =models.DateField(null=True)
    requested  = models.IntegerField(default=0)
    produced = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices = batch_status,default='Draft')
    create_shippo = models.BooleanField(default=False)
    packaging_Version = models.CharField(max_length=40,null=True)
    expiration_date = models.DateField(null=True)
    serialnoprovider=models.CharField(max_length=60,default="Tracelink")
    quantity= models.CharField(max_length=20,null=True)
    gtin_number = models.CharField(max_length=20,null=True,blank=True)
    # serial_num_pool_id = models.CharField(max_length=100)  # serialnumbers_model_id
    generic_name = models.CharField(max_length=50,null=True,blank=True)
    composition = models.CharField(max_length=100,null=True,blank=True)
    scheduled = models.DateField(max_length=100,null=True,blank=True)
    usage = models.CharField(max_length=100,null=True,blank=True)
    remark = models.CharField(max_length=100,null=True,blank=True)
    product_Image = models.ImageField(upload_to=namefile,null=True,blank=True)
    wholesalers=models.CharField(max_length=50,default="dabour")

    Markets=models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True)
    Barcodetypename = models.CharField(max_length=20, unique= True, null=True)
    model_name = models.CharField(max_length=50,null=True,blank=True)
    stock_quantity= models.CharField(max_length=50,null=True)
    shipped= models.CharField(max_length=50,null=True)
    identifier=models.CharField(max_length=100,unique=True,null=True)
    line=models.CharField(max_length=100,null=True,blank=True)
    type=models.CharField(max_length=100,null=True,blank=True)
    
    
    AT_PZN = models.CharField(max_length=100,null=True,blank=True)
    BE_ABP_CODE = models.CharField(max_length=100,null=True,blank=True)
    BR_An_visa_Registration_Number = models.CharField(max_length=100,null=True,blank=True)
    CA_DN = models.CharField(max_length=100,null=True,blank=True)
    CH_Swillme_dic = models.CharField(max_length=100, null=True,blank=True)
    CN_Subtype_Code = models.CharField(max_length=100, null=True,blank=True)
    DE_PPN = models.CharField(max_length=100,null=True,blank=True)
    DE_PZN = models.CharField(max_length=100,null=True,blank=True)
    Dosage = models.CharField(max_length=100,null=True,blank=True)
    EAN_13 = models.CharField(max_length=100,null=True,blank=True)
    Form_type = models.CharField(max_length=100,null=True,blank=True)
    Generic_Name = models.CharField(max_length=100,null=True,blank=True)
    GR_EOF_CODE = models.CharField(max_length=100,null=True,blank=True)
    HR_Croatia_National_Code = models.CharField(max_length=100,null=True,blank=True)
    IN_Product_Code = models.CharField(max_length=100,null=True,blank=True)
    internal_material_number=models.CharField(max_length=100,unique=True,blank=True)
    IT_Bollino = models.CharField(max_length=100,null=True,blank=True)
    KR_KFDA_Code = models.CharField(max_length=100,null=True,blank=True)
    License_Number = models.CharField(max_length=100,null=True,blank=True)
    Manufacturing_Date = models.DateField(null=True)
    NL_KLMP = models.CharField(max_length=100,null=True,blank=True)
    NRD_Nordic_VNR_Drug_Code = models.CharField(max_length=100,null=True,blank=True)
    Packet_type = models.CharField(max_length=100,null=True,blank=True)
    Revision_Number = models.CharField(max_length=100,null=True,blank=True)
    PT_Aim_Number = models.CharField(max_length=100,null=True,blank=True)
    
    # hrf1=models.JSONField(default={'null':'null'})
    # hrf2=models.JSONField(default={'null':'null'})
    # hrf3=models.JSONField(default={'null':'null'})
    # hrf4=models.JSONField(default={'null':'null'})
    # hrf5=models.JSONField(default={'null':'null'})
    # hrf6=models.JSONField(default={'null':'null'})
    hrf= models.JSONField(max_length=200,null=True,blank=True)
    
    
    def __str__(self):
        return self.manufacturing_location  
    
    
class Customers(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    created_by = models.CharField(max_length =100)
    company_prefix  = models.CharField(max_length=20,null=True)
    company_gln  = models.CharField(max_length=20,null=True)
    description = models.TextField()
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20) 
    zip = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ShipToLocationLookupid = models.CharField(max_length=100,null=True,blank=True)
    group = models.CharField(max_length=40,choices= group_choices,null=True,blank=True)
    status= models.BooleanField(default=False)
    # status=models.CharField(max_length=100,default="Not Confirmed")
    landmark=models.CharField(max_length=100,null=True)
    sgln_extension=models.CharField(max_length=100,null=True)
    tobusinessparylookupid=models.CharField(max_length=100,null=True)
    
    title=models.CharField(max_length=100,null=True)
    url=models.URLField(null=True)
    tracelink_username=models.CharField(max_length=100,default=True)
    siteid=models.IntegerField(null=True)
    sftp_port=models.IntegerField(null=True)
    sftp_password=models.CharField(max_length=100,default="password")
    file_sender=models.CharField(max_length=100,default=True)
    sending_system=models.CharField(max_length=100,default="system1")
    tracelink_password=models.CharField(max_length=100,default="password")
    sftp_host=models.CharField(max_length=100,null=True)
    sftp_username=models.CharField(max_length=100,default=True)
    file_receiver=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name  
    
    
class Locations(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customers,related_name='customers_to_locations',on_delete=models.CASCADE)
    created_by = models.CharField(max_length =100)
    name = models.CharField(max_length=40)
    loc_gln = models.CharField(max_length=20,unique=True)
    ShipToLocationLookupid = models.CharField(max_length=50)
    description = models.TextField(blank=True,null=True)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20) 
    zip = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    district=models.CharField(max_length=100,null=True)
    ship_to_locationlookup_id=models.CharField(max_length=100,null=True)
    tracelink_file_sender=models.CharField(max_length=100,null=True)
    sgln_extension=models.CharField(max_length=100,null=True) 

    # history =  HistoricalRecords()

    def __str__(self):
        return self.name       
    
class ShipPO(models.Model):
    id = models.AutoField(primary_key=True)
    shipping_order_name = models.CharField(max_length=40)
    process_order_number=models.ForeignKey(ProductionOrder,related_name='processorderno_to_shippo',on_delete=models.CASCADE)
    source_location = models.ForeignKey(Locations,related_name='location_to_shippo',on_delete=models.CASCADE)
    destination_location = models.ForeignKey(Locations,related_name='locations_to_shipping',on_delete=models.CASCADE)
    subject_name = models.ForeignKey(Customers,related_name='customers_to_shippingpo',on_delete=models.CASCADE)
    shipping_date = models.DateField(null=True)
    shipping_time=models.TimeField(null=True)
    status = models.CharField(max_length=20, choices = batch_status,default='Shipping') # false = stock and true = shipped
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length =100)
    shipping_type = models.CharField(max_length=20,default='item')
    batch_for_export = models.CharField(max_length=100,null=True)
    exempted_from_barcoding = models.CharField(max_length=100,null=True,blank=True)
    exemption_notification_and_date = models.CharField(max_length=100,null=True,blank=True)
    exempted_country_code = models.CharField(max_length=100,null=True,blank=True)
    sold_to = models.CharField(max_length=100,null=True,blank=True)
    delivery_number = models.CharField(max_length=100,null=True,blank=True)
    # delivary_number equals to  advance_ship_notice are Batch number
    delivary_number = models.CharField(max_length=100,null=True,blank=True)
    advance_ship_notice = models.CharField(max_length=100,null=True,blank=True)
    process_no_original=models.IntegerField(null=True)

    def __str__(self) :
        return self.shipping_order_name

    
    
class PrinterdataTable(models.Model):
                        
        id=models.AutoField(primary_key=True)
        processordernumber=models.CharField(max_length=100,unique= True)
        # serialnumberjson=models.TextField(max_length=10000,null=True,blank=True)
        
      
        
        expiration_date = models.DateField(null=True)
        # gtin = models.ForeignKey(Gtins, on_delete= models.CASCADE)
        lot=models.CharField(max_length=100,null=True)
        gtin=models.CharField(max_length=100,unique= True,null=True)
        numbers=models.JSONField(null=True,blank=True)
        quantity= models.CharField(max_length=20,null=True)
        hrf= models.JSONField(null=True,blank=True)
        type=models.CharField(max_length=100,null=True)
        status=models.CharField(max_length=100,null=True)
        ip_address=models.CharField(max_length=100,null=True)
        printed_numbers=models.JSONField(null=True)
        balanced_serialnumbers=models.JSONField(null=True)
        responsefield=models.BooleanField(null=True)
        preparebuttonresponse=models.BooleanField(null=True)
        stopbtnresponse=models.BooleanField(null=True)
        start_pause_btnresponse=models.BooleanField(null=True)
        pause_stop_btnresponse=models.BooleanField(null=True)
        return_slno_btn_response=models.BooleanField(null=True)
        
        label_response=models.CharField(max_length=100,null=True)
        child_numbers=models.JSONField(null=True,blank=True)
        scannergradefield=models.JSONField(null=True,blank=True)
        
        def __str__(self):
                return str(self. id)
            
            
            
            

class ScannerTable(models.Model):
                        id=models.AutoField(primary_key=True)
                        # processordernumber=models.CharField(max_length=100,unique= True)
                        gtin=models.CharField(max_length=100,null=True)
                        numbers=models.JSONField(null=True,blank=True)
                        ip_address=models.CharField(max_length=100,null=True)
                        grade = models.JSONField(blank=True,default="[{\"serialnumber\":\"grade\"}]")
                        status=models.CharField(max_length=100,null=True)
                        def __str__(self):
                                    return str(self. id) 
class ReworkTable(models.Model):
                    id=models.AutoField(primary_key=True)
                    # processordernumber=models.CharField(max_length=100,unique= True)
                    gtin=models.CharField(max_length=100,null=True)
                    slnonumber=models.CharField(max_length=100,null=True)
                    
                    oldstatus = models.CharField(max_length=100,null=True)
                    newstatus=models.CharField(max_length=100,null=True)
                    def __str__(self):
                        return str(self. id)  
             
             
             
             
             