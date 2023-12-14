from django.db import models
# from traitlets import default


# reject_status =(('Specimen', 'Specimen'),('Damaged','Damaged'), ('Sample','Sample'),('Challenged','Challenged')
#             , ('Teach','Teach'), ('In Process','In Process'), ('Rejected By Camera','Rejected By Camera')
#             , ('Unused','Unused'), ('Returned Number','Returned Number'), ('Downloaded Quality', 'Downloaded Quality'))
class ProductionReport(models.Model):
    id = models.AutoField(primary_key=True)
    process_order_number = models.CharField(max_length=100, default="process order number")
    batch_number = models.CharField(max_length=100, default="batch number", unique=True)
    product_name = models.CharField(max_length=100, default="product name")
    manufacture_loc_name = models.CharField(max_length=100, default="manufacture location name")
    
    line_name = models.CharField(max_length=100, default="line name")
    system_name = models.CharField(max_length=100, default="system name")
    created_by = models.CharField(max_length=100, default="created by")
    created_at = models.DateField(null=True)
    updated_at = models.DateField(null=True)
    accepted=models.IntegerField(default=0)
    specimen=models.IntegerField(default=0)
    damaged=models.IntegerField(default=0)
    sample=models.IntegerField(default=0)
    challenged=models.IntegerField(default=0)
    teach=models.IntegerField(default=0)
    inprocess=models.IntegerField(default=0)
    rejectedbycamera=models.IntegerField(default=0)
    unused=models.IntegerField(default=0)
    production_date =models.DateField(null=True)


    A=models.IntegerField(default=0)
    B=models.IntegerField(default=0)
    C=models.IntegerField(default=0)
    D=models.IntegerField(default=0)
    E=models.IntegerField(default=0)
    F=models.IntegerField(default=0)
    G=models.IntegerField(default=0)
    H=models.IntegerField(default=0)
    I=models.IntegerField(default=0)
    J=models.IntegerField(default=0)
    K=models.IntegerField(default=0)
    L=models.IntegerField(default=0)
    M=models.IntegerField(default=0)
    N=models.IntegerField(default=0)
    O=models.IntegerField(default=0)
    P=models.IntegerField(default=0)
    Q=models.IntegerField(default=0)
    R=models.IntegerField(default=0)
    S=models.IntegerField(default=0)
    T=models.IntegerField(default=0)
    U=models.IntegerField(default=0)
    V=models.IntegerField(default=0)
    W=models.IntegerField(default=0)
    X=models.IntegerField(default=0)
    Y=models.IntegerField(default=0)
    Z=models.IntegerField(default=0)
    
    def __str__(self):
        return self.batch_number

