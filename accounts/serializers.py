from accounts. models import Register,UserAuditHistoryOnly,UserrolePermissions,History
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
                        
    class Meta:
        model =Register
        fields = "__all__"
        
class UserHistorySerializer(serializers.ModelSerializer):
                        
    class Meta:
        model =UserAuditHistoryOnly
        fields = "__all__"
        
        
class UserrolePermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserrolePermissions
        fields="__all__"        
        
class HistorySerializer(serializers.ModelSerializer):
                        
    class Meta:
        model =History
        fields = "__all__"