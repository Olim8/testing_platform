from rest_framework import serializers
from .models import (
    University, StructureType, LocalityType, Department, Specialty, EducationLanguage,
    Group, Country, Province, District, Terrain, Citizenship, StudentStatus, EducationForm,
    EducationType, PaymentForm, StudentType, SocialCategory, Accommodation, Student
)

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class StructureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StructureType
        fields = '__all__'

class LocalityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalityType
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'

class EducationLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationLanguage
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class TerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terrain
        fields = '__all__'

class CitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citizenship
        fields = '__all__'

class StudentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatus
        fields = '__all__'

class EducationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationForm
        fields = '__all__'

class EducationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationType
        fields = '__all__'

class PaymentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentForm
        fields = '__all__'

class StudentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentType
        fields = '__all__'

class SocialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialCategory
        fields = '__all__'

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'