from rest_framework import serializers
from .models import Job, Application
from accounts.models import Profile

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id',
            'recruiter',
            'category',
            'title',
            'description',
            'salary',
            'city',
            'area',
            'latitude',
            'longitude',
            'created_at'
        ]
        read_only_fields = ['recruiter', 'created_at']


class ApplicantSerializer(serializers.ModelSerializer):
    seeker_details = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = [
            'id',
            'status',
            'applied_at',
            'seeker_details'
        ]

    def get_seeker_details(self, obj):
        profile = Profile.objects.get(user=obj.seeker)

        return {
            "user_id": obj.seeker.id,
            "username": obj.seeker.username,
            "city": profile.city,
            "area": profile.area,
            "experience_years": profile.experience_years,
            "category": profile.category.name if profile.category else None
        }
    

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'status',
            'applied_at'
        ]
        read_only_fields = ['status', 'applied_at']

