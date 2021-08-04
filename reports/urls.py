from django.urls import path
from . import views

urlpatterns = [

    # отчеты
    path('all', views.reports_all, name='reports_all'),
    path('glav_law_report', views.report_glav_law, name='report_glav_law'),
    path('report_ispolnitel', views.report_ispolnitel, name='report_ispolnitel'),
    path('ans/report_glav_law/<date_in>/<date_in_max>/<performer_id>', views.report_glav_law_ans, name='report_glav_law_ans'),
    path('ans/report_ispolnitel', views.report_ispolnitel_ans, name='report_ispolnitel_ans'),

]
