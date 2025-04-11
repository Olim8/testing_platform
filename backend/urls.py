from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversityViewSet, StructureTypeViewSet, LocalityTypeViewSet, DepartmentViewSet,
    SpecialtyViewSet, EducationLanguageViewSet, GroupViewSet, CountryViewSet,
    ProvinceViewSet, DistrictViewSet, TerrainViewSet, CitizenshipViewSet,
    StudentStatusViewSet, EducationFormViewSet, EducationTypeViewSet, PaymentFormViewSet,
    StudentTypeViewSet, SocialCategoryViewSet, AccommodationViewSet, StudentViewSet
)

router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'structure-types', StructureTypeViewSet)
router.register(r'locality-types', LocalityTypeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'specialties', SpecialtyViewSet)
router.register(r'education-languages', EducationLanguageViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'provinces', ProvinceViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'terrains', TerrainViewSet)
router.register(r'citizenships', CitizenshipViewSet)
router.register(r'student-statuses', StudentStatusViewSet)
router.register(r'education-forms', EducationFormViewSet)
router.register(r'education-types', EducationTypeViewSet)
router.register(r'payment-forms', PaymentFormViewSet)
router.register(r'student-types', StudentTypeViewSet)
router.register(r'social-categories', SocialCategoryViewSet)
router.register(r'accommodations', AccommodationViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]