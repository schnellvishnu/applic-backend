from accounts. models import Register,UserAuditHistoryOnly
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
                        
    class Meta:
        model =Register
        fields = "__all__"
        
class UserHistorySerializer(serializers.ModelSerializer):
                        
    class Meta:
        model =UserAuditHistoryOnly
        fields = "__all__"
        