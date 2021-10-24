"""ADMINSYS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from profiling import views as prof_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #path('nav/<path>',prof_views.nav, name="nav"),
    path('admin/', admin.site.urls),
    path('', prof_views.login_page, name = 'login_page'),
    path('home/', prof_views.home, name = 'home'),
    path('addprof/' , prof_views.addprof, name='addprof'),
#    path('generate_pdf/' , prof_views.generate_pdf, name='generate_pdf'),
    path('accounts_addorview/' , prof_views.accounts_addorview, name='accounts_addorview'),
    path('accounts_view/' , prof_views.accounts_view, name='accounts_view'),
    path('accounts_make/' , prof_views.accounts_make, name='accounts_make'),
    path('accounts_view_search/' , prof_views.accounts_view_search, name='accounts_view_search'),
    

    path('changepass/<primary_key>/' , prof_views.changepass, name='changepass'),
    path('accounts_make_search/' , prof_views.accounts_make_search, name='accounts_make_search'),
    path('create_account/<primary_key>' , prof_views.create_account, name='create_account'), #primary_key

    path('delete_account/<primary_key>' , prof_views.delete_account, name='delete_account'),
    path('delete_account_confirm/<primary_key>' , prof_views.delete_account_confirm, name='delete_account_confirm'),
    path('edit_account/<primary_key>' , prof_views.edit_account, name='edit_account'),
    path('logout_user/<message>' , prof_views.logout_user, name='logout_user'),
    path('create_inventory_report/' , prof_views.create_inventory_report, name='create_inventory_report'),

    path('pdf/', prof_views.GeneratePdf.as_view(), name="generate"),
    path('income/', prof_views.GeneratePdfIncome.as_view(), name="income_to_pdf"),
    path('expense/', prof_views.GeneratePdfExpense.as_view(), name="expense_to_pdf"),
    path('salary/', prof_views.GeneratePdfSalary.as_view(), name="salary_to_pdf"),

    path('generate_pdf_salary/<primary_key>' , prof_views.generate_pdf_salary, name='generate_pdf_salary'),
    path('generate_pdf_income/<date>' , prof_views.generate_pdf_income, name='generate_pdf_income'),
    path('generate_pdf_expense/<date>' , prof_views.generate_pdf_expense, name='generate_pdf_expense'),
    
#    path('income/<date>', prof_views.GeneratePdfIncome.as_view(), name="income_to_pdf"),
#    path('expense/<date>', prof_views.GeneratePdfExpense.as_view(), name="expense_to_pdf"),


#    path('editprof/' , prof_views.editprof, name='editprof'),
#    path('editemp/' , prof_views.editemp, name='editemp'),
    path('backtohome/' , prof_views.backtohome, name='backtohome'),
    path('editform/<profile_id>/<profiletype>' , prof_views.editform, name='editform'), 
#    path('deleteprof/<profile_id>/<deletefrom>' , prof_views.deleteprof, name='deleteprof'),
    path('addoption/' , prof_views.addoption, name='addoption'),
    path('addemp/' , prof_views.addemp, name='addemp'),
    path('pat_infoadd/' , prof_views.pat_infoadd, name='pat_infoadd'),
    path('emp_infoadd/' , prof_views.emp_infoadd, name='emp_infoadd'),
    path('prof_addorview/' , prof_views.prof_addorview, name='prof_addorview'),
    path('prof_view/' , prof_views.prof_view, name='prof_view'),
    path('emp_view/' , prof_views.emp_view, name='emp_view'),
    path('emp_addorview/' , prof_views.emp_addorview, name='emp_addorview'),
#    path('addsalary/' , prof_views.addsalary, name='addsalary'), 
    path('addsalaryinfo/ <profile_id>' , prof_views.addsalaryinfo, name='addsalaryinfo'),
    path('viewsalary/ <primary_key>' , prof_views.viewsalary, name='viewsalary'),
#    path('editsalary/' , prof_views.editsalary, name='editsalary'),
    path('appointments_addorview/' , prof_views.appointments_addorview, name='appointments_addorview'),
    path('add_appointments/' , prof_views.add_appointments, name='add_appointments'),
    path('add_appointmentinfo/<profile_id>/<datecondition>' , prof_views.add_appointmentinfo, name='add_appointmentinfo'),
    path('add_services/' , prof_views.add_services, name='add_services'),
    path('add_schedule/' , prof_views.add_schedule, name='add_schedule'),
    path('view_schedule/' , prof_views.view_schedule, name='view_schedule'),
    path('view_services/' , prof_views.view_services, name='view_services'),
#    path('edit_services/' , prof_views.edit_services, name='edit_services'),
#    path('edit_schedule/' , prof_views.edit_schedule, name='edit_schedule'),
    path('inventory_options/' , prof_views.inventory_options, name='inventory_options'),
    path('view_inventory/' , prof_views.view_inventory, name='view_inventory'),
#    path('edit_inventory/' , prof_views.edit_inventory, name='edit_inventory'),
    path('add_inventory/' , prof_views.add_inventory, name='add_inventory'),
    path('view_appointments/' , prof_views.CalendarView.as_view(), name='view_appointments'), 
    #path('view_appointments/' , prof_views.view_appointments, name='view_appointments'),
#    path('edit_appointments/' , prof_views.edit_appointments, name='edit_appointments'),
    path('income_expense_options/' , prof_views.income_expense_options, name='income_expense_options'),
    path('view_pat_info/ <primary_key>' , prof_views.view_pat_info, name='view_pat_info'),
    path('edit_pat_info/ <primary_key>' , prof_views.edit_pat_info, name='edit_pat_info'),
    path('view_emp_info/ <primary_key>' , prof_views.view_emp_info, name='view_emp_info'),
    path('edit_emp_info/ <primary_key>' , prof_views.edit_emp_info, name='edit_emp_info'),
#    path('pass_key/ <primary_key>', prof_views.pass_key, name='pass_key'), ##
    path('view_finished_appointments/' , prof_views.view_finished_appointments, name='view_finished_appointments'),
    path('add_procedures/ <primary_key>' , prof_views.add_procedures, name='add_procedures'),
    path('add_tools_items_used/ <primary_key>' , prof_views.add_tools_items_used, name='add_tools_items_used'),
#    path('add_more_procedure/' , prof_views.add_more_procedure, name='add_more_procedure'),
    path('add_procedure_option/ ' , prof_views.add_procedure_option, name='add_procedure_option'),

#    path('add_more_tools_items_used/' , prof_views.add_more_tools_items_used, name='add_more_tools_items_used'),
    path('add_tools_items_used_option/' , prof_views.add_tools_items_used_option, name='add_tools_items_used_option'),
    path('view_additional_appointment_info/ <primary_key>' , prof_views.view_additional_appointment_info, name='view_additional_appointment_info'),


#    path('edit_additional_appointment_info/ <primary_key>' , prof_views.edit_additional_appointment_info, name='edit_additional_appointment_info'),
    path('make_payment/<appointment_id>/<service_fee>/<procedures_fee>/<tools_fee>' , prof_views.make_payment, name='make_payment'),

    path('check_inventory/ <primary_key>' , prof_views.check_inventory, name='check_inventory'),
    path('view_patient_appointment_history/ <primary_key>' , prof_views.view_patient_appointment_history, name='view_patient_appointment_history'),

    path('view_only_appointment_history/ <primary_key>' , prof_views.view_only_appointment_history, name='view_only_appointment_history'),

    path('view_only_payment_history/ <primary_key>' , prof_views.view_only_payment_history, name='view_only_payment_history'),


#    path('edit_appointments_cancelled/' , prof_views.edit_appointments_cancelled, name='edit_appointments_cancelled'),
    path('view_appointments_cancelled/' , prof_views.view_appointments_cancelled, name='view_appointments_cancelled'),

    path('prescriptions_addorview/ <primary_key>' , prof_views.prescriptions_addorview, name='prescriptions_addorview'),


    path('add_prescriptions/ <primary_key>' , prof_views.add_prescriptions, name='add_prescriptions'),

    path('view_prescriptions/ <primary_key>', prof_views.view_prescriptions, name='view_prescriptions'),
#    path('edit_prescriptions/ <primary_key>', prof_views.edit_prescriptions, name='edit_prescriptions'),
    path('buy_prescriptions/ <primary_key>', prof_views.buy_prescriptions, name='buy_prescriptions'),
    path('view_bought_prescriptions/ <primary_key>', prof_views.view_bought_prescriptions, name='view_bought_prescriptions'),

    path('calculate_payment/ <primary_key>', prof_views.calculate_payment, name='calculate_payment'),

    path('calculate_salary/ <profile_id>', prof_views.calculate_salary, name='calculate_salary'),

    path('teeth_chart/ <primary_key>', prof_views.teeth_chart, name='teeth_chart'),
    path('change_teeth/ <primary_key>', prof_views.change_teeth, name='change_teeth'),
    
#    path(r'^teeth_status/?P<primary_key>/?P<teeth_pos>$', prof_views.teeth_status, name='teeth_status'),

#    path(r'^teeth_history/?P<primary_key>/?P<teeth_pos>$', prof_views.teeth_history, name='teeth_history'),


    path('teeth_status/?P<primary_key>/?P<teeth_pos>', prof_views.teeth_status, name='teeth_status'),

    path('teeth_history/?P<primary_key>/?P<teeth_pos>', prof_views.teeth_history, name='teeth_history'),



    path('stock_out_option' , prof_views.stock_out_option, name='stock_out_option'),

    path('view_stockout_tools' , prof_views.view_stockout_tools, name='view_stockout_tools'),

    path('view_stockout_presc' , prof_views.view_stockout_presc, name='view_stockout_presc'),

    path('income_options' , prof_views.income_options, name='income_options'),

    path('expense_options' , prof_views.expense_options, name='expense_options'),

    path('view_appointment_income' , prof_views.view_appointment_income, name='view_appointment_income'),

    path('view_presc_income' , prof_views.view_presc_income, name='view_presc_income'),

    path('view_salary_expense' , prof_views.view_salary_expense, name='view_salary_expense'),
    path('view_expired_items' , prof_views.view_expired_items, name='view_expired_items'),




    path('bills_options' , prof_views.bills_options, name='bills_options'),
    path('add_bills' , prof_views.add_bills, name='add_bills'),
    path('view_bills' , prof_views.view_bills, name='view_bills'),
#    path('edit_bills' , prof_views.edit_bills, name='edit_bills'),
    path('edit_billForm/ <primary_key>' , prof_views.edit_billForm, name='edit_billForm'),

    

    path('stock_in_options' , prof_views.stock_in_options, name='stock_in_options'),
    path('add_new_item/<itemname>/<barcode>/<itemcategory>/<location>/<item_fee>/<quantity>/<units>' , prof_views.add_new_item, name='add_new_item'),
    path('add_nonperishableList' , prof_views.add_nonperishableList, name='add_nonperishableList'),
    path('add_perishableList/<itemname>/<barcode>/<itemcategory>/<location>/<item_fee>/<quantity>/<units>/<expiry_date>' , prof_views.add_perishableList, name='add_perishableList'),
    path('add_nonperishable/ <primary_key>' , prof_views.add_nonperishable, name='add_nonperishable'),
#    path('add_perishable/ <primary_key>' , prof_views.add_perishable, name='add_perishable'),


    path('add_inventory2' , prof_views.add_inventory2, name='add_inventory2'),
    path('add_inventory3' , prof_views.add_inventory3, name='add_inventory3'),
    path('view_stockin_expense' , prof_views.view_stockin_expense, name='view_stockin_expense'),

    path('changecalendar/<month>/<year>' , prof_views.changecalendar, name='changecalendar'), #

    
    path('prof_view_searched' , prof_views.prof_view_searched, name='prof_view_searched'),
    path('emp_view_searched' , prof_views.emp_view_searched, name='emp_view_searched'),
    path('view_services_search' , prof_views.view_services_search, name='view_services_search'),
    path('view_schedule_search' , prof_views.view_schedule_search, name='view_schedule_search'),
    path('view_inventory_search' , prof_views.view_inventory_search, name='view_inventory_search'),

    path('check_inventory_search/<primary_key>' , prof_views.check_inventory_search, name='check_inventory_search'),
    path('viewsalary_search/<primary_key>' , prof_views.viewsalary_search, name='viewsalary_search'),
    path('view_salary_expense_search' , prof_views.view_salary_expense_search, name='view_salary_expense_search'),
    path('view_bills_search' , prof_views.view_bills_search, name='view_bills_search'),
    path('view_stockin_expense_search' , prof_views.view_stockin_expense_search, name='view_stockin_expense_search'),
    path('view_appointment_income_search' , prof_views.view_appointment_income_search, name='view_appointment_income_search'),
    path('view_presc_income_search' , prof_views.view_presc_income_search, name='view_presc_income_search'),

    path('view_prescriptions_search/<primary_key>' , prof_views.view_prescriptions_search, name='view_prescriptions_search'),
    path('view_patient_appointment_history_search/ <primary_key>' , prof_views.view_patient_appointment_history_search, name='view_patient_appointment_history_search'),
    path('view_bought_prescriptions_search/ <primary_key>' , prof_views.view_bought_prescriptions_search, name='view_bought_prescriptions_search'),

    
    path('view_stockout_tools_search' , prof_views.view_stockout_tools_search, name='view_stockout_tools_search'),
    
    path('view_expired_items_search' , prof_views.view_expired_items_search, name='view_expired_items_search'),
    path('view_stockout_presc_search' , prof_views.view_stockout_presc_search, name='view_stockout_presc_search'),
    path('teeth_history_search/?P<primary_key>/?P<teeth_pos>', prof_views.teeth_history_search, name='teeth_history_search'),
#    path('view_stockout_tools_search' , prof_views.view_stockout_tools_search, name='view_stockout_tools_search'),
#    path('view_stockout_tools_search' , prof_views.view_stockout_tools_search, name='view_stockout_tools_search'),


    path(r'^view_stockin_expense_filter/?P<query>/?P<order>$' , prof_views.view_stockin_expense_filter, name='view_stockin_expense_filter'),


    path('prof_view_filter/<order>' , prof_views.prof_view_filter, name='prof_view_filter'),

    path('emp_view_filter/<order>' , prof_views.emp_view_filter, name='emp_view_filter'),

    path('view_services_filter/<order>' , prof_views.view_services_filter, name='view_services_filter'),
    
    path('view_schedule_filter/<order>' , prof_views.view_schedule_filter, name='view_schedule_filter'),

    path('viewsalary_filter/<primary_key>/<order>' , prof_views.viewsalary_filter, name='viewsalary_filter'),

    path('view_stockout_tools_filter/<order>' , prof_views.view_stockout_tools_filter, name='view_stockout_tools_filter'),

    path('view_stockout_presc_filter/<order>' , prof_views.view_stockout_presc_filter, name='view_stockout_presc_filter'),

    path('view_expired_items_filter/<order>' , prof_views.view_expired_items_filter, name='view_expired_items_filter'),

    path('view_salary_expense_filter/<order>' , prof_views.view_salary_expense_filter, name='view_salary_expense_filter'),
    path('view_bills_filter/<order>' , prof_views.view_bills_filter, name='view_bills_filter'),
    path('view_appointment_income_filter/<order>' , prof_views.view_appointment_income_filter, name='view_appointment_income_filter'),
    path('view_presc_income_filter/<order>' , prof_views.view_presc_income_filter, name='view_presc_income_filter'),
    path('view_prescriptions_filter/<primary_key>/<order>' , prof_views.view_prescriptions_filter, name='view_prescriptions_filter'),
    path('view_bought_prescriptions_filter/<primary_key>/<order>' , prof_views.view_bought_prescriptions_filter, name='view_bought_prescriptions_filter'),
    path('view_patient_appointment_history_filter/<primary_key>/<order>' , prof_views.view_patient_appointment_history_filter, name='view_patient_appointment_history_filter'),
    path('teeth_history_filter/<primary_key>/<teeth_pos>/<order>' , prof_views.teeth_history_filter, name='teeth_history_filter'),

    
    path('view_inventory_filter/<order>' , prof_views.view_inventory_filter, name='view_inventory_filter'),
    path('check_inventory_filter/<primary_key>/<order>' , prof_views.check_inventory_filter, name='check_inventory_filter'),
#    path('view_inventory_filter/<order>' , prof_views.view_inventory_filter, name='view_inventory_filter'),
#    path('view_inventory_filter/<order>' , prof_views.view_inventory_filter, name='view_inventory_filter'),
#    path('view_inventory_filter/<order>' , prof_views.view_inventory_filter, name='view_inventory_filter'),
#    path('view_inventory_filter/<order>' , prof_views.view_inventory_filter, name='view_inventory_filter'),
    path('add_appointments_search/' , prof_views.add_appointments_search, name='add_appointments_search'),
    path('check_medicine/<primary_key>' , prof_views.check_medicine, name='check_medicine'),
    path('check_medicine_search/<primary_key>' , prof_views.check_medicine_search, name='check_medicine_search'),
    path('check_medicine_filter/<primary_key>/<order>' , prof_views.check_medicine_filter, name='check_medicine_filter'),

    path('total_monthly_expense/' , prof_views.total_monthly_expense, name='total_monthly_expense'),
    path('total_monthly_income/' , prof_views.total_monthly_income, name='total_monthly_income'),
    
    path('total_monthly_profit/' , prof_views.total_monthly_profit, name='total_monthly_profit'),

    path('more_salary_info/<primary_key>' , prof_views.more_salary_info, name='more_salary_info'),

    
    path('add_nonperishableList_search/' , prof_views.add_nonperishableList_search, name='add_nonperishableList_search'),
    path('add_nonperishableList_filter/<order>' , prof_views.add_nonperishableList_filter, name='add_nonperishableList_filter'),

    path('expense_breakdown/<date>' , prof_views.expense_breakdown, name='expense_breakdown'),
    path('income_breakdown/<date>' , prof_views.income_breakdown, name='income_breakdown'),
    path('income_breakdown_pdf/<date>' , prof_views.income_breakdown_pdf, name='income_breakdown_pdf'),

    path('cancel_appointment/<primary_key>', prof_views.cancel_appointment, name='cancel_appointment'),
    path('choose_date/<profile_id>', prof_views.choose_date, name='choose_date'),

    path('check_available_schedule/<profile_id>/<date>', prof_views.check_available_schedule, name='check_available_schedule'),
    path('check_available_services/<profile_id>/<date>', prof_views.check_available_services, name='check_available_services'),
    path('check_available_services_search/<profile_id>/<date>', prof_views.check_available_services_search, name='check_available_services_search'),


    #path('choose_date/<profile_id>', prof_views.choose_date, name='choose_date'),

#############################################################################################################################################################

    #url(r'^index/$', views.index, name='index'),
    #url('', views.CalendarView.as_view(), name='calendar'),
    #url(r'^event/new/$', views.event, name='event_new'),
    #url(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
