from rest_framework import viewsets
from .models import (
    University, StructureType, LocalityType, Department, Specialty, EducationLanguage,
    Group, Country, Province, District, Terrain, Citizenship, StudentStatus, EducationForm,
    EducationType, PaymentForm, StudentType, SocialCategory, Accommodation, Student
)
from .serializers import (
    UniversitySerializer, StructureTypeSerializer, LocalityTypeSerializer, DepartmentSerializer,
    SpecialtySerializer, EducationLanguageSerializer, GroupSerializer, CountrySerializer,
    ProvinceSerializer, DistrictSerializer, TerrainSerializer, CitizenshipSerializer,
    StudentStatusSerializer, EducationFormSerializer, EducationTypeSerializer, PaymentFormSerializer,
    StudentTypeSerializer, SocialCategorySerializer, AccommodationSerializer, StudentSerializer
)

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class StructureTypeViewSet(viewsets.ModelViewSet):
    queryset = StructureType.objects.all()
    serializer_class = StructureTypeSerializer

class LocalityTypeViewSet(viewsets.ModelViewSet):
    queryset = LocalityType.objects.all()
    serializer_class = LocalityTypeSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

class EducationLanguageViewSet(viewsets.ModelViewSet):
    queryset = EducationLanguage.objects.all()
    serializer_class = EducationLanguageSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

class TerrainViewSet(viewsets.ModelViewSet):
    queryset = Terrain.objects.all()
    serializer_class = TerrainSerializer

class CitizenshipViewSet(viewsets.ModelViewSet):
    queryset = Citizenship.objects.all()
    serializer_class = CitizenshipSerializer

class StudentStatusViewSet(viewsets.ModelViewSet):
    queryset = StudentStatus.objects.all()
    serializer_class = StudentStatusSerializer

class EducationFormViewSet(viewsets.ModelViewSet):
    queryset = EducationForm.objects.all()
    serializer_class = EducationFormSerializer

class EducationTypeViewSet(viewsets.ModelViewSet):
    queryset = EducationType.objects.all()
    serializer_class = EducationTypeSerializer

class PaymentFormViewSet(viewsets.ModelViewSet):
    queryset = PaymentForm.objects.all()
    serializer_class = PaymentFormSerializer

class StudentTypeViewSet(viewsets.ModelViewSet):
    queryset = StudentType.objects.all()
    serializer_class = StudentTypeSerializer

class SocialCategoryViewSet(viewsets.ModelViewSet):
    queryset = SocialCategory.objects.all()
    serializer_class = SocialCategorySerializer

class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer