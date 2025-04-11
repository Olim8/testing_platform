from django.core.management.base import BaseCommand
import requests
import time
import datetime
from decouple import config
from django.utils import timezone
from backend.models import (
    University, StructureType, LocalityType, Department, Specialty, EducationLanguage,
    Group, Country, Province, District, Terrain, Citizenship, StudentStatus, EducationForm,
    EducationType, PaymentForm, StudentType, SocialCategory, Accommodation, Student
)

class Command(BaseCommand):
    help = 'Sync data from university API'

    def fetch_all_pages(self, url, headers):
        all_items = []
        page = 1
        while True:
            self.stdout.write(self.style.NOTICE(f'Fetching page {page} from {url}'))
            response = requests.get(f"{url}?page={page}", headers=headers)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f'Failed to fetch page {page}: {response.status_code} - {response.text}'))
                break
            data = response.json()
            items = data['data']['items']
            # Log if items contain None
            if None in items:
                self.stdout.write(self.style.WARNING(f'Page {page} contains None items: {items}'))
            all_items.extend(items)
            page_count = data['data']['pagination']['pageCount']
            self.stdout.write(self.style.NOTICE(f'Page {page} of {page_count}, fetched {len(items)} items'))
            if page >= page_count:
                break
            page += 1
            time.sleep(1)  # Add a 1-second delay to avoid rate limits
        # Log total items and check for None
        self.stdout.write(self.style.NOTICE(f'Total items fetched: {len(all_items)}'))
        if None in all_items:
            self.stdout.write(self.style.WARNING(f'Found None in all_items after fetching: {all_items.count(None)} occurrences'))
        return all_items

    def handle(self, *args, **options):
        bearer_token = config('BEARER_TOKEN')
        headers = {"Authorization": f"Bearer {bearer_token}"}
        base_url = "https://student.zarmeduniver.com/rest"

        # Sync departments
        dept_items = self.fetch_all_pages(f"{base_url}/v1/data/department-list", headers)
        for dept_data in dept_items:
            if dept_data is None:
                self.stdout.write(self.style.WARNING('Skipping a None department record'))
                continue
            structure_type, _ = StructureType.objects.get_or_create(
                code=dept_data['structureType']['code'],
                defaults={'name': dept_data['structureType']['name']}
            )
            locality_type, _ = LocalityType.objects.get_or_create(
                code=dept_data['localityType']['code'],
                defaults={'name': dept_data['localityType']['name']}
            )
            Department.objects.update_or_create(
                id=dept_data['id'],
                defaults={
                    'name': dept_data['name'],
                    'code': dept_data['code'],
                    'structure_type': structure_type,
                    'locality_type': locality_type,
                    'active': dept_data['active'],
                }
            )
        # Second pass to set parent relationships
        for dept_data in dept_items:
            if dept_data is None:
                continue
            dept = Department.objects.get(id=dept_data['id'])
            if dept_data['parent'] is not None:
                dept.parent = Department.objects.get(id=dept_data['parent'])
                dept.save()
        self.stdout.write(self.style.SUCCESS(f'Synced {len(dept_items)} departments successfully'))

        # Sync groups
        group_items = self.fetch_all_pages(f"{base_url}/v1/data/group-list", headers)
        for group_data in group_items:
            if group_data is None:
                self.stdout.write(self.style.WARNING('Skipping a None group record'))
                continue
            structure_type, _ = StructureType.objects.get_or_create(
                code=group_data['department']['structureType']['code'],
                defaults={'name': group_data['department']['structureType']['name']}
            )
            locality_type, _ = LocalityType.objects.get_or_create(
                code=group_data['department']['localityType']['code'],
                defaults={'name': group_data['department']['localityType']['name']}
            )
            dept, _ = Department.objects.get_or_create(
                id=group_data['department']['id'],
                defaults={
                    'name': group_data['department']['name'],
                    'code': group_data['department']['code'],
                    'structure_type': structure_type,
                    'locality_type': locality_type,
                    'parent': None if group_data['department']['parent'] is None else Department.objects.get(id=group_data['department']['parent']),
                    'active': group_data['department']['active'],
                }
            )
            spec, _ = Specialty.objects.get_or_create(
                id=group_data['specialty']['id'],
                defaults={'code': group_data['specialty']['code'], 'name': group_data['specialty']['name']}
            )
            edu_lang, _ = EducationLanguage.objects.get_or_create(
                code=group_data['educationLang']['code'],
                defaults={'name': group_data['educationLang']['name']}
            )
            Group.objects.update_or_create(
                id=group_data['id'],
                defaults={
                    'name': group_data['name'],
                    'department': dept,
                    'specialty': spec,
                    'education_lang': edu_lang,
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Synced {len(group_items)} groups successfully'))

        # Sync students
        student_items = self.fetch_all_pages(f"{base_url}/v1/data/student-list", headers)
        university, _ = University.objects.get_or_create(
            code="458",
            defaults={'name': "Zarmed Universiteti"}
        )
        skipped_records = 0
        for idx, student in enumerate(student_items):
            self.stdout.write(self.style.NOTICE(f'Processing student {idx + 1} of {len(student_items)}'))
            # Skip if student is None
            if student is None:
                self.stdout.write(self.style.WARNING(f'Skipping a None student record at index {idx}'))
                skipped_records += 1
                continue

            try:
                structure_type, _ = StructureType.objects.get_or_create(
                    code=student['department']['structureType']['code'],
                    defaults={'name': student['department']['structureType']['name']}
                )
                locality_type, _ = LocalityType.objects.get_or_create(
                    code=student['department']['localityType']['code'],
                    defaults={'name': student['department']['localityType']['name']}
                )
                dept, _ = Department.objects.get_or_create(
                    id=student['department']['id'],
                    defaults={
                        'name': student['department']['name'],
                        'code': student['department']['code'],
                        'structure_type': structure_type,
                        'locality_type': locality_type,
                        'parent': None if student['department'].get('parent') is None else Department.objects.get(id=student['department']['parent']),
                        'active': student['department'].get('active', True),
                    }
                )
                spec, _ = Specialty.objects.get_or_create(
                    id=student['specialty']['id'],
                    defaults={'code': student['specialty']['code'], 'name': student['specialty']['name']}
                )
                edu_lang, _ = EducationLanguage.objects.get_or_create(
                    code=student['group']['educationLang']['code'],
                    defaults={'name': student['group']['educationLang']['name']}
                )
                group, _ = Group.objects.get_or_create(
                    id=student['group']['id'],
                    defaults={
                        'name': student['group']['name'],
                        'department': dept,
                        'specialty': spec,
                        'education_lang': edu_lang,
                    }
                )
                country, _ = Country.objects.get_or_create(
                    code=student['country']['code'],
                    defaults={'name': student['country']['name']}
                )
                province, _ = Province.objects.get_or_create(
                    code=student['province']['code'],
                    defaults={'name': student['province']['name'], 'parent': None}
                )
                current_province_code = student.get('currentProvince', {}).get('code')
                current_province, _ = Province.objects.get_or_create(
                    code=current_province_code if current_province_code else '',
                    defaults={'name': student.get('currentProvince', {}).get('name', ''), 'parent': None}
                )
                district, _ = District.objects.get_or_create(
                    code=student['district']['code'],
                    defaults={'name': student['district']['name'], 'parent': province}
                )
                current_district_code = student.get('currentDistrict', {}).get('code')
                current_district, _ = District.objects.get_or_create(
                    code=current_district_code if current_district_code else '',
                    defaults={'name': student.get('currentDistrict', {}).get('name', ''), 'parent': current_province}
                )
                terrain, _ = Terrain.objects.get_or_create(
                    code=student['terrain']['code'],
                    defaults={'name': student['terrain']['name']}
                )
                current_terrain_code = student.get('currentTerrain', {}).get('code')
                current_terrain, _ = Terrain.objects.get_or_create(
                    code=current_terrain_code if current_terrain_code else '',
                    defaults={'name': student.get('currentTerrain', {}).get('name', '')}
                )
                citizenship, _ = Citizenship.objects.get_or_create(
                    code=student['citizenship']['code'],
                    defaults={'name': student['citizenship']['name']}
                )
                student_status, _ = StudentStatus.objects.get_or_create(
                    code=student['studentStatus']['code'],
                    defaults={'name': student['studentStatus']['name']}
                )
                education_form, _ = EducationForm.objects.get_or_create(
                    code=student['educationForm']['code'],
                    defaults={'name': student['educationForm']['name']}
                )
                education_type, _ = EducationType.objects.get_or_create(
                    code=student['educationType']['code'],
                    defaults={'name': student['educationType']['name']}
                )
                payment_form, _ = PaymentForm.objects.get_or_create(
                    code=student['paymentForm']['code'],
                    defaults={'name': student['paymentForm']['name']}
                )
                student_type, _ = StudentType.objects.get_or_create(
                    code=student['studentType']['code'],
                    defaults={'name': student['studentType']['name']}
                )
                social_category, _ = SocialCategory.objects.get_or_create(
                    code=student['socialCategory']['code'],
                    defaults={'name': student['socialCategory']['name']}
                )
                accommodation, _ = Accommodation.objects.get_or_create(
                    code=student['accommodation']['code'],
                    defaults={'name': student['accommodation']['name']}
                )
                Student.objects.update_or_create(
                    id=student['id'],
                    defaults={
                        'university': university,
                        'full_name': student['full_name'],
                        'short_name': student['short_name'],
                        'first_name': student['first_name'],
                        'second_name': student['second_name'],
                        'third_name': student['third_name'],
                        'gender': student['gender']['name'],
                        'birth_date': timezone.make_aware(datetime.datetime.fromtimestamp(student['birth_date'])) if student.get('birth_date') else None,
                        'student_id_number': student['student_id_number'],
                        'image': student['image'],
                        'avg_gpa': student['avg_gpa'],
                        'avg_grade': student['avg_grade'],
                        'total_credit': student['total_credit'],
                        'country': country,
                        'province': province,
                        'current_province': current_province if current_province_code else None,
                        'district': district,
                        'current_district': current_district if current_district_code else None,
                        'terrain': terrain,
                        'current_terrain': current_terrain if current_terrain_code else None,
                        'citizenship': citizenship,
                        'student_status': student_status,
                        'education_form': education_form,
                        'education_type': education_type,
                        'payment_form': payment_form,
                        'student_type': student_type,
                        'social_category': social_category,
                        'accommodation': accommodation,
                        'department': dept,
                        'specialty': spec,
                        'group': group,
                        'level': student['level']['name'],
                        'semester': student['semester']['name'],
                        'education_year': student['educationYear']['name'],
                        'year_of_enter': student['year_of_enter'],
                        'roommate_count': student['roommate_count'],
                        'is_graduate': student['is_graduate'],
                        'total_acload': student['total_acload'],
                        'other': student['other'],
                        'created_at': timezone.make_aware(datetime.datetime.fromtimestamp(student['created_at'])) if student.get('created_at') else None,
                        'updated_at': timezone.make_aware(datetime.datetime.fromtimestamp(student['updated_at'])) if student.get('updated_at') else None,
                    }
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing student at index {idx}: {str(e)}'))
                skipped_records += 1
                continue

        self.stdout.write(self.style.SUCCESS(f'Synced {len(student_items) - skipped_records} students successfully, skipped {skipped_records} records'))

        self.stdout.write(self.style.SUCCESS('Data sync completed'))