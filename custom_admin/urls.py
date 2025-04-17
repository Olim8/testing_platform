from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('departments/', views.department_list, name='department_list'),
    path('groups/', views.group_list, name='group_list'),
    path('students/', views.student_list, name='student_list'),
    path('exams_list/', views.exams_list, name="exams_list"),
    path('create-exam/', views.create_exam, name='create_exam'),
    path('logout/', views.logout_view, name='logout'),
    path('exam/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('exam/<int:exam_id>/questions/', views.exam_questions, name='exam_questions'),
    path('exam/<int:exam_id>/add-questions/', views.add_questions, name='add_questions'),
    # path('exam/<int:exam_id>/add-group/', views.add_group, name='add_group'),
    # path('exam/<int:exam_id>/results/', views.exam_results, name='exam_results'),
]