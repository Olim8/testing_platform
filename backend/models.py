from django.db import models

class University(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class StructureType(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class LocalityType(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=20)
    structure_type = models.ForeignKey(StructureType, on_delete=models.SET_NULL, null=True, blank=True)
    locality_type = models.ForeignKey(LocalityType, on_delete=models.SET_NULL, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Specialty(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class EducationLanguage(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True)
    education_lang = models.ForeignKey(EducationLanguage, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Province(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class District(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Terrain(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Citizenship(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StudentStatus(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EducationForm(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EducationType(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PaymentForm(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StudentType(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SocialCategory(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100, blank=True)
    second_name = models.CharField(max_length=100, blank=True)
    third_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10)
    birth_date = models.DateTimeField(null=True, blank=True)
    student_id_number = models.CharField(max_length=20, unique=True, db_index=True)
    image = models.URLField(max_length=500, blank=True)
    avg_gpa = models.FloatField(default=0.0)
    avg_grade = models.FloatField(default=0.0)
    total_credit = models.IntegerField(default=0)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    current_province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_province_set')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    current_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_district_set')
    terrain = models.ForeignKey(Terrain, on_delete=models.SET_NULL, null=True, blank=True)
    current_terrain = models.ForeignKey(Terrain, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_terrain_set')
    citizenship = models.ForeignKey(Citizenship, on_delete=models.SET_NULL, null=True, blank=True)
    student_status = models.ForeignKey(StudentStatus, on_delete=models.SET_NULL, null=True, blank=True)
    education_form = models.ForeignKey(EducationForm, on_delete=models.SET_NULL, null=True, blank=True)
    education_type = models.ForeignKey(EducationType, on_delete=models.SET_NULL, null=True, blank=True)
    payment_form = models.ForeignKey(PaymentForm, on_delete=models.SET_NULL, null=True, blank=True)
    student_type = models.ForeignKey(StudentType, on_delete=models.SET_NULL, null=True, blank=True)
    social_category = models.ForeignKey(SocialCategory, on_delete=models.SET_NULL, null=True, blank=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.CharField(max_length=20, blank=True)
    semester = models.CharField(max_length=20, blank=True)
    education_year = models.CharField(max_length=20, blank=True)
    year_of_enter = models.IntegerField(null=True, blank=True)
    roommate_count = models.IntegerField(null=True, blank=True)
    is_graduate = models.BooleanField(default=False)
    total_acload = models.IntegerField(null=True, blank=True)
    other = models.TextField(blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.full_name
    
class Exam(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(verbose_name="Izoh")
    oquv_reja = models.CharField(max_length=100, verbose_name="O'quv reja")
    oquv_yili = models.CharField(max_length=20, verbose_name="O'quv yili", default="2024 (2024-2025)")
    semester = models.CharField(max_length=20, verbose_name="Semestr")
    subject = models.CharField(max_length=255, verbose_name="Fanlar")
    nazorat_turi = models.CharField(max_length=50, verbose_name="Nazorat turi", choices=[
        ("Umumiy", "Umumiy"),
        ("Yakuniy nazorat", "Yakuniy nazorat")
    ])
    faol = models.BooleanField(verbose_name="Faol", default=True, choices=[(True, "Ha"), (False, "Yo'q")])
    boshlanish = models.DateTimeField(verbose_name="Boshlanish")
    tugash = models.DateTimeField(verbose_name="Tugash")
    vaqti_daqiqa = models.PositiveIntegerField(verbose_name="Vaqti (daqiqa)")
    maks_ball = models.PositiveIntegerField(verbose_name="Maks. ball")
    urinishlar = models.PositiveIntegerField(verbose_name="Urinishlar")
    savollar_soni = models.PositiveIntegerField(verbose_name="Savollar soni")
    tasodifiy = models.BooleanField(verbose_name="Tasodifiy", default=False, choices=[(True, "Ha"), (False, "Yo'q")])
    groups = models.ManyToManyField('Group', related_name='exams', blank=True, verbose_name="Guruhlar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Imtihon"
        verbose_name_plural = "Imtihonlar"

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Savol matni")
    option_a = models.CharField(max_length=255, verbose_name="a) Variant")
    option_b = models.CharField(max_length=255, verbose_name="b) Variant")
    option_c = models.CharField(max_length=255, verbose_name="c) Variant")
    option_d = models.CharField(max_length=255, verbose_name="d) Variant")
    correct_option = models.CharField(max_length=1, choices=[
        ('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')
    ], verbose_name="To'g'ri javob")

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"