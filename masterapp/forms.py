from django import forms

# from django.contrib.auth.models import User
from masterapp.models import PrinterdataTable,Customers
from django.contrib.auth.forms import UserCreationForm


class PrinterForm(forms.ModelForm):
    # gtin=forms.CharField()
    # lot=forms.CharField()
    # expiration_date=forms.CharField()
    # numbers=forms.CharField(max_length=120)
    # type=forms.CharField(max_length=120)
    # hrf=forms.CharField(max_length=120)
                 
    class Meta:
            model=PrinterdataTable
            # fields = "__all__" 
             
            fields=["id","gtin","lot","expiration_date","numbers","type","hrf","start_pause_btnresponse"]
# "stopbtnresponse","pause_stop_btnresponse","return_slno_btn_response,"quantity","ip_address","printed_numbers","balanced_serialnumbers","responsefield","preparebuttonresponse",
            # fields=["gtin","lot","expiration_date","numbers","type","hrf",
            #      "start_pause_btnresponse","processordernumber"]
       


class Clientform(forms.Form):
    printerreponse=forms.CharField()
    
    
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customers
        # fields='__all__'
       
        fields=["id","name","created_by","company_prefix"]

class Dummyform(forms.Form):
    ex=forms.CharField()                     
       