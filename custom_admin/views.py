from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from backend.models import Department, Group, Student, Exam, Specialty, Question
from .forms import DepartmentFilterForm, GroupFilterForm, StudentFilterForm, ExamForm
from django.core.paginator import Paginator

def dashboard(request):
    department_count = Department.objects.count()
    group_count = Group.objects.count()
    student_count = Student.objects.count()
    return render(request, 'custom_admin/dashboard.html', {'department_count': department_count, 'group_count':group_count, 'student_count': student_count})

def department_list(request):
    form = DepartmentFilterForm(request.GET)
    qs = Department.objects.all()
    if form.is_valid():
        if form.cleaned_data.get('name'):
            qs = qs.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data.get('code'):
            qs = qs.filter(code__icontains=form.cleaned_data['code'])
        if form.cleaned_data.get('active') not in [None, '']:
            qs = qs.filter(active=form.cleaned_data['active'])
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'custom_admin/department_list.html', {'departments': page_obj, 'form': form})

def group_list(request):
    form = GroupFilterForm(request.GET)
    qs = Group.objects.all()
    if form.is_valid():
        if form.cleaned_data.get('name'):
            qs = qs.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data.get('department'):
            qs = qs.filter(department__name__icontains=form.cleaned_data['department'])
        if form.cleaned_data.get('specialty'):
            qs = qs.filter(specialty__name__icontains=form.cleaned_data['specialty'])
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'custom_admin/group_list.html', {'groups': page_obj, 'form': form})

def student_list(request):
    form = StudentFilterForm(request.GET)
    qs = Student.objects.all()
    if form.is_valid():
        if form.cleaned_data.get('full_name'):
            qs = qs.filter(full_name__icontains=form.cleaned_data['full_name'])
        if form.cleaned_data.get('student_id_number'):
            qs = qs.filter(student_id_number__icontains=form.cleaned_data['student_id_number'])
        if form.cleaned_data.get('department'):
            qs = qs.filter(department__name__icontains=form.cleaned_data['department'])
        if form.cleaned_data.get('group'):
            qs = qs.filter(group__name__icontains=form.cleaned_data['group'])
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'custom_admin/student_list.html', {'students': page_obj, 'form': form})

def create_exam(request):
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            return redirect('create_exam', exam_id=exam.id)
    else:
        form = ExamForm()
    return render(request, 'custom_admin/create_exam.html', {'form': form})

def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    groups = exam.groups.all()
    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_detail', exam_id=exam.id)
    else:
        form = ExamForm(instance=exam)
    return render(request, 'custom_admin/exam_detail.html', {'exam': exam, 'form': form, 'groups': groups})

def exam_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()
    return render(request, 'custom_admin/exam_questions.html', {'exam': exam, 'questions': questions})

def add_questions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        raw_text = request.POST.get('questions_text', '')
        questions = parse_questions(raw_text)
        for q in questions:
            Question.objects.create(
                exam=exam,
                text=q['text'],
                option_a=q['options'][0],
                option_b=q['options'][1],
                option_c=q['options'][2],
                option_d=q['options'][3],
                correct_option=q['correct']
            )
        return redirect('exam_questions', exam_id=exam_id)
    return render(request, 'custom_admin/add_questions.html', {'exam': exam})

def parse_questions(raw_text):
    questions = []
    lines = raw_text.splitlines()
    current_question = None
    options = []
    correct = None

    for line in lines:
        line = line.stript()
        if not line:
            continue
        if line.startswith('#'):
            if current_question:
                questions.append({
                    'text': current_question,
                    'options': options,
                    'correct': correct
                })
            current_question = line.replace('#', '').strip()
            options = []
            correct = None
        elif line.startswith('===='):
            options.append(line.replace('====', '').strip())
            correct = chr(97 + len(options) - 1)
        elif line.startswith('++++'):
            continue
        else:
            options.append(line.strip())

    if current_question:
        questions.append({
            'text': current_question,
            'options': options,
            'correct': correct
        })
    return questions

def logout_view(request):
    logout(request)
    return redirect('dashboard')