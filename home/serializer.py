from rest_framework import serializers
from .models import Account_opening_Submission

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'image', 'price', 'category']

class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account_opening_Submission
        fields = ['id', 'name', 'data', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']