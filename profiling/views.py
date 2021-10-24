from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
import calendar
from calendar import HTMLCalendar
from datetime import date
from datetime import datetime,timedelta
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from .utils import Calendar
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

from django.template.loader import get_template
from .utils import render_to_pdf

#from .utils import Calendar
from .models import profile
from .models import emp_info
from .models import pat_info
from .models import salary_info
from .models import available_schedules
from .models import available_services
from .models import appointment_details
from .models import available_schedules
from .models import available_services
from .models import item_inventory
from .models import tools_items_used
from .models import procedures_done
from .models import payment
from .models import prescription_management
from .models import prescription_purchase
from .models import bills_details
from .models import stock_in
from .models import teeths
from .models import teeths_status
from .models import accounts

from .forms import changePassword 
from .forms import profileForm
from .forms import addForm
from .forms import EditForm
from .forms import emp_infoForm
from .forms import pat_infoForm
from .forms import emp_EditinfoForm
from .forms import pat_EditinfoForm
from .forms import salary_infoForm
from .forms import salary_EditinfoForm
from .forms import add_appointmentinfoForm
from .forms import add_servicesForm
from .forms import add_scheduleForm
from .forms import edit_servicesForm
from .forms import edit_scheduleForm
from .forms import add_inventoryForm
from .forms import edit_appointmentinfoForm
from .forms import edit_patinfoForm
from .forms import edit_empinfoForm
from .forms import add_tools_items_usedForm
from .forms import add_proceduresForm
from .forms import edit_tools_items_usedForm
from .forms import edit_proceduresForm
from .forms import make_paymentForm
from .forms import prescriptionForm
from .forms import edit_prescriptionForm
from .forms import buy_prescriptionForm
from .forms import calculate_paymentForm
from .forms import calculate_salaryForm
from .forms import add_billsForm
from .forms import edit_billsForm
#from .forms import stock_inForm
from .forms import add_nonperishableForm
from .forms import add_perishableForm
from .forms import add_inventoryForm2
from .forms import add_chartForm
from .forms import searchForm
from .forms import accForm

from django.views.generic import View
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.

'''
def nav(request, path):
    if path == 'home':
        return render(request,'home.html',context)
        #return redirect('home')
    elif path == 'pat':
        return render(request,'prof_view.html',context)
    elif path == 'app':
        return render(request,'appointments_addorview.html',{})
        #return redirect('appointments_addorview')
    elif path == 'inv':
        return render(request,'inventory_options.html',{})
        #return redirect('inventory_options')
    elif path == 'inc_exp':
        return render(request,'income_expense_options.html',{})
        #return redirect('income_expense_options')

    elif path == 'emp':
        if request.user.username != 'admin':
            logout(request)
            messages.error(request, "Must be an admin to access the page")
            return redirect('login_page')
        else:
            all_data_prof = profile.objects.filter(profile_type = 'Employee')
            all_data_emp_info = emp_info.objects.all()
            all_data_salary = salary_info.objects.all()
            delete_id2()
            context = {
                        'all_data_prof' : all_data_prof,
                        'all_data_emp_info' : all_data_emp_info,
                        'all_data_salary': all_data_salary,
                        'path':path,
                    }
        return render(request,'emp_view.html',context)
        #return redirect('emp_view')
'''
def changepass(request, primary_key):
    curr_user = request.user
    user = User.objects.get(pk=primary_key)
    form = PasswordChangeForm(data=request.POST, user = user)
    context = {'form':form,'curr_user':curr_user,'user':user}
    if request.method=='POST':
        if form.is_valid():
            form.save()
            if request.user == user:
                logout(request)
                messages.error(request, 'Password Changed successfully you need to log in again')
                return redirect('login_page')
            else:
                messages.error(request, f"User {user.first_name}'s Password Changed successfully")
                return redirect('accounts_view')
        else:
            #SOME ERROR
            return render(request, 'changepass.html',context)

    else:
        return render(request, 'changepass.html',context)        




class GeneratePdfSalary(View): #WALA NAGAMIT
     def get(self, request, *args, **kwargs):
        
        #getting the template
        all_data_emp_salary = salary_info.objects.all()
        context = {'all_data_emp_salary':all_data_emp_salary}
        pdf = render_to_pdf('salary_report.html',context)
         
         #rendering the template
        #return FileResponse(pdf, as_attachment=True, filename='yes.pdf')
        return HttpResponse(pdf, content_type='application/pdf')


def generate_pdf_salary(request,primary_key): 
    all_data_emp_salary = salary_info.objects.get(pk=primary_key)
    emp_name = all_data_emp_salary.profile_id.fullname
    date = all_data_emp_salary.date_given
    context = {'all_data_emp_salary':all_data_emp_salary,'emp_name':emp_name,'date':date}
    pdf = render_to_pdf('salary_report.html',context)
    return HttpResponse(pdf, content_type='application/pdf')




class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        
        #getting the template
        expired = item_inventory.objects.filter(expiry_status = 'Expired')
        good = item_inventory.objects.filter(expiry_status = 'Good for usage')
        no_expiry =  item_inventory.objects.filter(expiry_status = 'Item does not expire')
        context = {'expired':expired,'good':good,'no_expiry':no_expiry}
        pdf = render_to_pdf('create_inventory_report.html',context)
         
         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')



class GeneratePdfIncome(View): #WALA NAGAMIT
     def get(self, request, *args, **kwargs):
        #getting the template
        
        presc_details = prescription_purchase.objects.all() #total_amount
        payment_details = payment.objects.all() #total_payment
        tot_presc =  get_income_presc2()
        tot_pay = get_income_payments2()
        total_inc = tot_presc + tot_pay
        total_inc = float("%.2f" % total_inc)
        context = {'total_inc':total_inc,'presc_details':presc_details,
                    'payment_details':payment_details,'tot_presc':tot_presc,'tot_pay':tot_pay }

        pdf = render_to_pdf('income_breakdown_pdf.html',context)
        return HttpResponse(pdf, content_type='application/pdf')#rendering the template



def generate_pdf_income(request,date):#nagamit
        d = getDatee(date)
        presc_details = prescription_purchase.objects.filter(purchase_date__contains = date) 
        payment_details = payment.objects.filter(date_paid__contains = date) 
        tot_presc =  get_income_presc(date)
        tot_pay = get_income_payments(date)
        total_inc = tot_presc + tot_pay
        total_inc = float("%.2f" % total_inc)
        context = {'tot_presc':tot_presc,'tot_pay':tot_pay,'total_inc':total_inc,
                    'd':d,"date": date, 'payment_details':payment_details, 'presc_details':presc_details}
        pdf = render_to_pdf('income_breakdown_pdf.html',context)
        return HttpResponse(pdf, content_type='application/pdf')#rendering the template


def generate_pdf_expense(request,date):#nagamit
    d = getDatee(date)
    bills_data = bills_details.objects.filter(date_paid__contains = date)
    stockin_data = stock_in.objects.filter(purchase_date__contains = date)
    salary_details = salary_info.objects.filter(date_given__contains = date) 

    
    tot_bill = get_expense_bills(date)
    tot_salary = get_expense_salary(date)
    tot_stockin = get_expense_stockin(date)
    total_exp = tot_bill + tot_salary + tot_stockin
    total_exp = float("%.2f" % total_exp)


    context = {'total_exp':total_exp,'tot_stockin':tot_stockin,'tot_salary':tot_salary,'tot_bill':tot_bill,
                'd':d,"date": date,'bills_data':bills_data,'stockin_data':stockin_data,'salary_details':salary_details}
    pdf = render_to_pdf('expense_breakdown_pdf.html',context)
    return HttpResponse(pdf, content_type='application/pdf')




class GeneratePdfExpense(View): #WALA NAGAMIT
     def get(self, request, *args, **kwargs):
        #getting the template
        bills_data = bills_details.objects.all()
        stockin_data = stock_in.objects.all()
        salary_details = salary_info.objects.all()
        context = {'bills_data':bills_data,'stockin_data':stockin_data,'salary_details':salary_details}
        pdf = render_to_pdf('expense_breakdown_pdf.html',context)
         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')




def login_page(request):
    if request.user.is_authenticated == True:
        return redirect('home')

    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.error(request, f'Login success, Hi {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return render( request,'login_page.html', {})
        else:
            
            return render( request,'login_page.html', {})

@login_required
def accounts_addorview(request):
    return render(request, 'accounts_addorview.html',{})

@login_required
def accounts_make(request):
    emp_data = profile.objects.filter(profile_type='Employee')
    context = {"emp_data":emp_data}
    return render(request, 'accounts_make.html',context)

@login_required
def accounts_view(request):
    acc_data = User.objects.all()
    context ={'acc_data':acc_data}
    return render(request, 'accounts_view.html',context)

@login_required
def create_account(request,primary_key): #primary_key
    form = UserCreationForm(request.POST or None)
    #form = UserChangeForm(request.POST or None)
    emp = profile.objects.get(pk = primary_key)
    users = User.objects.all()
    temp = 0
    emp_name = ""
    for i in users:
        if i.first_name == emp.fullname:
            temp = temp + 1

    if temp == 0:
        emp_name = emp.fullname
        context = {'form':form,'emp_name':emp_name} #,'primary_key':primary_key
        #form2 = accForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            #form2.save()
            connect_user(emp_name)
            messages.error(request, 'Account Successfully created')
            return redirect('accounts_view')
        else:
            #messages.error(request, 'Kindly follow the instructions/guide given')
            return render(request,'create_account.html',context)
    else:
        context = {'form':form,'emp_name':emp_name}
        return render(request,'create_account.html',context)




def accounts_view_search(request):
    name = request.POST['name']
    acc_data = User.objects.filter(first_name__contains = name)
    context ={'acc_data':acc_data}
    return render(request, 'accounts_view_search.html',context)

def accounts_make_search(request):
    name = request.POST['name']
    emp_data = profile.objects.filter(profile_type='Employee').filter(fullname__contains = name)
    context ={'emp_data':emp_data}
    return render(request, 'accounts_make_search.html',context)



def edit_account(request, primary_key):
    user = User.objects.get(pk = primary_key)
    form = UserChangeForm(request.POST or None)
    context ={'user': user, "form":form}
    return render(request, 'edit_account.html', context)


def connect_user(emp_name):
    user = User.objects.last()
    acc = accounts.objects.last()
    user.first_name = emp_name
    user.save()


@login_required
def delete_account(request, primary_key):
    context = {'primary_key' : primary_key}
    return render(request, 'delete_account.html',context)



def delete_account_confirm(request, primary_key):
    primary_key = int(primary_key)
    user = User.objects.get(pk = primary_key)
    user.delete()
    messages.error(request, 'Account Successfully Deleted')
    return redirect('accounts_view')

def logout_user(request,message):
    if message == 'valid':
        message = 'Log out successfully'
    elif message == 'invalid':
        message = 'Must be an admin to access this page'
    logout(request)
    messages.error(request, message)
    return redirect('login_page')



@login_required
def home(request):
    #Appointments checker
    appointment_data = appointment_details.objects.filter(appointment_status = 'Ongoing')
    for things in appointment_data:
        if things.schedule_id.date < date.today():
            appointment_data2 = appointment_details.objects.get(pk = things.id)
            appointment_data2.appointment_status = 'Finished'
            appointment_data2.save()
        elif things.schedule_id.date == date.today():
            time = datetime.now() 
            time = time.strftime('%H:%M')
            if things.schedule_id.time.strftime("%H:%M") < time:
                appointment_data2 = appointment_details.objects.get(pk = things.id)
                appointment_data2.appointment_status = 'Finished'
                appointment_data2.save()
            else:
                pass
        else:
            pass
    #sched checker
    sched_data = available_schedules.objects.filter(availability = True)
    for things in sched_data:
        if things.date < date.today():
            sched2 = available_schedules.objects.get(pk = things.id)
            sched2.availability = False
            sched2.save()
        elif things.date == date.today():
            time = datetime.now() 
            time = time.strftime('%H:%M')
            if things.time.strftime("%H:%M") < time:
                sched2 = available_schedules.objects.get(pk = things.id)
                sched2.availability = False
                sched2.save()
            else:
                pass
        else:
            pass
    
    #EXPIRY CHECK
    item_deets = item_inventory.objects.all()
    for things in item_deets:
        if things.expiry_date != None:
            if things.expiry_date < date.today():
                item_data = item_inventory.objects.get(pk = things.id)
                item_data.expiry_status = 'Expired'
                item_data.save()
        elif things.expiry_date == None:
            item_data = item_inventory.objects.get(pk = things.id)
            item_data.expiry_status = 'Item does not expire'
            item_data.save()


    all_data = profile.objects.all()

    #quantity notif
    items = item_inventory.objects.all()
    q_pk = []
    low_quantity =[]
    for things in items:
        if things.quantity < 25:
            q_pk.append(things.id)
    for i in q_pk:
        low_quantity.extend(item_inventory.objects.filter(pk = i))


    #expired notif
    appoints = appointment_details.objects.all()
    item_pk = []
    expired_items = []
    for things in items:
        if things.expiry_status == 'Expired':
            item_pk.append(things.id)
    for i in item_pk:
        expired_items.extend(list(item_inventory.objects.filter(pk = i)))
   

    #expiry notif
    today = date.today()
    add = timedelta(15)
    date_pk = []
    near_expiry = []
    date_condition = today + add
    for things in items:
        if things.expiry_date != None:
            if things.expiry_date.strftime("%m/%d/%Y") < date_condition.strftime("%m/%d/%Y") and things.expiry_date.strftime("%m/%d/%Y") >= date.today().strftime("%m/%d/%Y"):
                date_pk.append(things.id)
    for i in date_pk:
        near_expiry.extend(list(item_inventory.objects.filter(pk = i)))



    #appointment notif
    appointment_dates = appointment_details.objects.all()
    app_pk = []
    appointment_now = []
    for things in appointment_dates:
        if things.schedule_id.date == today:
            app_pk.append(things.id)
    for i in app_pk:
        appointment_now.extend(list(appointment_details.objects.filter(pk=i).filter(appointment_status = 'Ongoing')))

    context={
#            'all_data':all_data, 
            'item_pk':item_pk,
            'expired_items': expired_items, 
            'appoints':appoints, 
            'low_quantity':low_quantity,
            'date_condition':date_condition,
            'near_expiry' : near_expiry,
            'appointment_now':appointment_now,
            'date_condition':date_condition
            }
    return render(request, 'home.html', context)
         

@login_required                  
def addprof(request):
         if request.method == 'POST':
                  form = addForm(request.POST or None)
                  if form.is_valid(): # and form2.is_valid()
                           form
                           form.save()
                           some_bool = valid_date()
                           if some_bool == True:
                               if form.cleaned_data.get('profile_type') == "Employee":
                                return redirect('emp_infoadd')
                               elif form.cleaned_data.get('profile_type') == "Patient":
                                return redirect('pat_infoadd')
                               else:
                                messages.error(request, 'Please supply every information and follow the given format')
                                return render(request, 'addprof.html', {})
                           else:
                            messages.error(request, 'Invalid Date')
                            return render(request, 'addprof.html', {}) #put error input (invalid input) 


                  else:
                    messages.error(request, 'Please supply every information and follow the given format')
                    return render(request, 'addprof.html', {}) #put error input (invalid input)           
         else:
            return render(request, 'addprof.html', {})#put error input


def valid_date():
    prof = profile.objects.last()
    date = prof.bday
    if date > date.today():
        prof.delete()
        return False
    else:
        return True

@login_required
def addemp(request):
         if request.method == 'POST':
                  form = addForm(request.POST or None)
                  if form.is_valid():
                           form.save()
                           some_bool = valid_dateEmp()
                           if some_bool == True:
                               if form.cleaned_data.get('profile_type') == "Employee":
                                return redirect('emp_infoadd')
                               elif form.cleaned_data.get('profile_type') == "Patient":
                                return redirect('pat_infoadd')
                               else:
                                messages.error(request, 'Please supply every information and follow the given format')
                                return render(request, 'addemp.html', {})
                           else:
                            messages.error(request, 'Invalid Date')
                            return render(request, 'addemp.html', {}) #put error input (invalid input) 
                  else:
                    messages.error(request, 'Please supply every information and follow the given format')
                    return render(request, 'addemp.html', {}) #put error input (invalid input)           
         else:
            return render(request, 'addemp.html', {})#put error input

def valid_dateEmp():
    prof = profile.objects.last()
    date = prof.bday
    if date > date.today():
        prof.delete()
        return False
    else:
        return True

def backtohome(request):
         all_data_prof = profile.objects.all()
         all_data_ecp = Ecp.objects.all()
         all_data_emp_info = emp_info.objects.all()
         all_data_prof_info = pat_info.objects.all()
         context={
        'all_data_prof':all_data_prof,
        'all_data_ecp':all_data_ecp,
        'all_data_emp_info':all_data_emp_info,
        'all_data_prof_info':all_data_prof_info
         }
         return render(request, 'home.html', context)


@login_required
def editform(request, profile_id, profiletype): 
        if profiletype == 'prescriptions': #prescription edit
            all_data_prescriptions = prescription_management.objects.get(pk = profile_id)
            key = all_data_prescriptions.patient_id_id
            context = {'all_data_prescriptions':all_data_prescriptions, 'profile_id' : profile_id,'key':key}
            if request.method == 'POST':
                form = edit_prescriptionForm(request.POST or None)
                if form.is_valid():
                    all_data_prescriptions.given_by = form.cleaned_data.get('given_by')
                    all_data_prescriptions.meds_prescription = form.cleaned_data.get('meds_prescription')
                    all_data_prescriptions.quantity = form.cleaned_data.get('quantity')
                    all_data_prescriptions.units = form.cleaned_data.get('units')
                    all_data_prescriptions.intake_instructions = form.cleaned_data.get('intake_instructions')
                    all_data_prescriptions.date_given = form.cleaned_data.get('date_given')
                    all_data_prescriptions.save()
                    primary_key = all_data_prescriptions.patient_id.id
                    messages.error(request, 'Prescription successfully edited')
                    return redirect('view_prescriptions', primary_key)
                else:
                    messages.error(request, 'Please supply every information and follow the given format')
                    return render(request,'editform.html', context)
            else:
                return render(request,'editform.html', context)



        if profiletype == 'patient':                              #EDITING PATIENT
            if request.method == 'POST':
                  all_data_prof = profile.objects.get(pk=profile_id)
                  all_data_pat_info = pat_info.objects.get(profile_id = profile_id)
                  form = addForm(request.POST or None)
                  form2 = pat_EditinfoForm(request.POST or None)
                  if form.is_valid() and form2.is_valid():
                           all_data_prof.fullname = form.cleaned_data.get('fullname')
                           all_data_prof.profile_type = form.cleaned_data.get('profile_type')
                           all_data_prof.contact_number = form.cleaned_data.get('contact_number')
                           all_data_prof.profile_fulladress = form.cleaned_data.get('profile_fulladress')
                           all_data_prof.bday = form.cleaned_data.get('bday')
                           all_data_prof.gender = form.cleaned_data.get('gender')
                           all_data_prof.ecp_fullname = form.cleaned_data.get('ecp_fullname')
                           all_data_prof.ecp_contactnum = form.cleaned_data.get('ecp_contactnum')
                           all_data_prof.ecp_relationship = form.cleaned_data.get('ecp_relationship')
                           all_data_prof.ecp_fulladress = form.cleaned_data.get('ecp_fulladress')
                           all_data_pat_info.pat_occupation = form2.cleaned_data.get('pat_occupation')
                           all_data_pat_info.pat_allergies = form2.cleaned_data.get('pat_allergies')
                           all_data_prof.save()
                           all_data_pat_info.save()
                           #context = {"all_data" : all_data}
                           return redirect('prof_view')
                  else:
                           all_data_prof = profile.objects.get(pk=profile_id)
                           all_data_pat_info = pat_info.objects.get(profile_id = profile_id)
                           context ={
                            'all_data_prof':all_data_prof,
                            'all_data_pat_info':all_data_pat_info, 
                            'profile_id':profile_id,
                           }
                           messages.error(request, 'Please supply every information and follow the given format')
                           return render(request,'editform.html', context)             
            else:
                  all_data_prof = profile.objects.get(pk=profile_id)
                  all_data_pat_info = pat_info.objects.get(profile_id = profile_id)
                  context ={
                  'all_data_prof':all_data_prof, 
                  'all_data_pat_info':all_data_pat_info,
                  'profile_id':profile_id,
                  }
                  return render(request, 'editform.html', context) #before POST



        elif profiletype == 'employee':                     #EDITING EMPLOYEE
            if request.method == 'POST':
                  all_data_prof = profile.objects.get(pk=profile_id)
                  all_data_emp_info = emp_info.objects.get(profile_id = profile_id)
                  form = addForm(request.POST or None)
                  form3 = emp_EditinfoForm(request.POST or None)
                  if form.is_valid() and form3.is_valid():
                           all_data_prof.fullname = form.cleaned_data.get('fullname')
                           all_data_prof.profile_type = form.cleaned_data.get('profile_type')
                           all_data_prof.contact_number = form.cleaned_data.get('contact_number')
                           all_data_prof.profile_fulladress = form.cleaned_data.get('profile_fulladress')
                           all_data_prof.bday = form.cleaned_data.get('bday')
                           all_data_prof.gender = form.cleaned_data.get('gender')
                           all_data_prof.ecp_fullname = form.cleaned_data.get('ecp_fullname')
                           all_data_prof.ecp_contactnum = form.cleaned_data.get('ecp_contactnum')
                           all_data_prof.ecp_relationship = form.cleaned_data.get('ecp_relationship')
                           all_data_prof.ecp_fulladress = form.cleaned_data.get('ecp_fulladress')
                           all_data_emp_info.emp_position = form3.cleaned_data.get('emp_position')
                           all_data_emp_info.emp_status = form3.cleaned_data.get('emp_status')
                           all_data_prof.save()
                           all_data_emp_info.save()
                           return redirect('viewemp')
                  else:
                           all_data_prof = profile.objects.get(pk=profile_id)
                           all_data_emp_info = emp_info.objects.get(profile_id = profile_id)
                           context ={
                            'all_data_emp_info':all_data_emp_info,
                            'all_data_prof':all_data_prof, 
                            'profile_id':profile_id,
                           }
                           messages.error(request, 'Please supply every information and follow the given format')
                           return render(request,'editform.html', context)             
            else:
                  all_data_prof = profile.objects.get(pk=profile_id)
                  all_data_emp_info = emp_info.objects.get(profile_id = profile_id)
                  context ={
                  'all_data_prof':all_data_prof,
                  'all_data_emp_info':all_data_emp_info, 
                  'profile_id':profile_id,
                  }
                  return render(request, 'editform.html', context) #wrong method



        elif profiletype == 'salary':    #EDITING SALARY
            all_data_emp_salary = salary_info.objects.get(pk = profile_id)
            key = all_data_emp_salary.profile_id.id
            context ={
                    'all_data_emp_salary':all_data_emp_salary, 
                    'profile_id':profile_id,
                    'key':key
                    }
            if request.method == 'POST':
                all_data_emp_salary = salary_info.objects.get(pk = profile_id)

                form = salary_EditinfoForm(request.POST or None)
                if form.is_valid():
                    all_data_emp_salary.regular = form.cleaned_data.get('regular')
                    all_data_emp_salary.overtime = form.cleaned_data.get('overtime')
                    all_data_emp_salary.bonus = form.cleaned_data.get('bonus')
                    all_data_emp_salary.tips = form.cleaned_data.get('tips')
                    all_data_emp_salary.severance  = form.cleaned_data.get('severance')
                    all_data_emp_salary.philhealth = form.cleaned_data.get('philhealth')
                    all_data_emp_salary.sss = form.cleaned_data.get('sss')
                    all_data_emp_salary.pagibig = form.cleaned_data.get('pagibig')
                    all_data_emp_salary.insurance = form.cleaned_data.get('insurance')
                    all_data_emp_salary.tax = form.cleaned_data.get('tax')
                    all_data_emp_salary.others = form.cleaned_data.get('others')
                    all_data_emp_salary.date_given = form.cleaned_data.get('date_given')
                    all_data_emp_salary.save()
                    calculate_salary2(profile_id)
                    p_id = all_data_emp_salary.profile_id.id
                    messages.error(request, 'Salary successfully edited') 
                    return redirect('more_salary_info',profile_id)
                else:         
                    messages.error(request, 'Please supply every information and follow the given format') 
                    return render(request, 'editform.html', context)
            else: 
                return render(request, 'editform.html', context) 



        elif profiletype == 'services': #EDITING SERVICES
                all_data_services = available_services.objects.get(pk = profile_id)
                context = {'all_data_services':all_data_services,'profile_id':profile_id,}
                if request.method == 'POST':
                    all_data_services = available_services.objects.get(pk = profile_id)
                    form = edit_servicesForm(request.POST or None)
                    if form.is_valid():  
                        old_type = all_data_services.service_type
                        old_fee = all_data_services.service_fee
                        old_avail = all_data_services.availability
                        all_data_services.service_type = form.cleaned_data.get('service_type')
                        all_data_services.service_fee = form.cleaned_data.get('service_fee')
                        all_data_services.availability = form.cleaned_data.get('availability')
                        all_data_services.save()
                        some_bool = check_services_error2(profile_id)
                        if some_bool == True:
                            messages.error(request, 'Service successfully edited')
                            return redirect('view_services')
                        else:
                            all_data_services.service_type =old_type
                            all_data_services.service_fee = old_fee
                            all_data_services.availability = old_avail
                            all_data_services.save()
                            messages.error(request, 'Service Already Exists') 
                            return render(request, 'editform.html', context)

                    else:
                        messages.error(request, 'Please supply every information and follow the given format') 
                        return render(request, 'editform.html', context)
                else:
                    return render(request, 'editform.html', context)



        elif profiletype == 'schedule': #EDITING SCHEDULE
                all_data_schedule = available_schedules.objects.get(pk = profile_id)
                context = {'all_data_schedule':all_data_schedule,}
                if request.method == 'POST':
                    form = edit_scheduleForm(request.POST or None)
                    if form.is_valid():
                        date = form.cleaned_data.get('date')
                        time = form.cleaned_data.get('time')
                        doc = form.cleaned_data.get('doctor_lastname')
                        some_bool = check_schedEdit(date,time,doc,profile_id)
                        if some_bool == 'yes':
                            all_data_schedule.date = form.cleaned_data.get('date')
                            all_data_schedule.time = form.cleaned_data.get('time')
                            all_data_schedule.doctor_lastname = form.cleaned_data.get('doctor_lastname')
                            all_data_schedule.availability = form.cleaned_data['availability']
                            temp = all_data_schedule.availability
                            all_data_schedule.save()
                            if temp == True:
                                check_avail(profile_id)
                                messages.error(request, 'Schedule successlly edited')
                                return redirect('view_schedule')
                            else:
                                messages.error(request, 'Schedule successlly edited')
                                return redirect('view_schedule')
                        elif  some_bool == 'exist':
                            messages.error(request, 'Schedule already exists')
                            return render(request, 'editform.html', context)
                        elif  some_bool == 'date':
                            messages.error(request, 'Date has already passed')
                            return render(request, 'editform.html', context)
                        elif  some_bool == 'time':
                            messages.error(request, 'Time has already passed')
                            return render(request, 'editform.html', context)
                        else:
                            messages.error(request, 'Invalid Input')
                            return render(request, 'editform.html', context)                       
                    else:
                        messages.error(request, 'Please supply every information and follow the given format')
                        return render(request, 'editform.html', context)
                else:
                    return render(request, 'editform.html', context)

    

        elif profiletype == 'inventory':  #EDITING INVENTORY
                all_data_inventory = item_inventory.objects.get(pk = profile_id)
                context = {'all_data_inventory' : all_data_inventory}
                if request.method == 'POST':
                    all_data_inventory = item_inventory.objects.get(pk = profile_id)
                    form = add_inventoryForm(request.POST or None)
                    if form.is_valid():
                        date = form.cleaned_data.get('expiry_date')
                        if form.cleaned_data.get('quantity') <= 0:
                            messages.error(request, 'Invalid Quantity')
                            return render(request, 'editform.html', context)

                        elif date != None and date < date.today():
                            messages.error(request, 'Invalid Date')
                            return render(request, 'editform.html', context)
                        else:
                            all_data_inventory.itemname = form.cleaned_data.get('itemname')
                            all_data_inventory.barcode = form.cleaned_data.get('barcode')
                            all_data_inventory.itemcategory = form.cleaned_data.get('itemcategory')
                            all_data_inventory.location = form.cleaned_data.get('location')
                            all_data_inventory.item_fee = form.cleaned_data.get('item_fee')
                            all_data_inventory.quantity = form.cleaned_data.get('quantity')
                            all_data_inventory.units = form.cleaned_data.get('units')
                            all_data_inventory.expiry_date = form.cleaned_data.get('expiry_date')
                            all_data_inventory.save()
                            update_editexp(profile_id)
                            messages.error(request, 'Item successfully edited')
                            return redirect('view_inventory')
                    else:
                        messages.error(request, 'Please supply every information and follow the given format')
                        return render(request, 'editform.html', context)
                else:
                    return render(request, 'editform.html', context)



        elif profiletype == 'appointments': #EDITING APPOINTMENTS
                all_data_available_services = available_services.objects.all()
                all_data_available_schedules = available_schedules.objects.all()
                all_data_appointments = appointment_details.objects.get(pk = profile_id)
                primary_key = profile_id
                context = {
                            'all_data_appointments' : all_data_appointments,
                            'all_data_available_schedules' : all_data_available_schedules,
                            'all_data_available_services' : all_data_available_services,
                            'primary_key':primary_key
                          }
                return render(request, 'editform.html', context)




        elif profiletype == 'procedure': #EDITING PROCEDURES
            all_data_procedures = procedures_done.objects.get(pk = profile_id)
            p_id = all_data_procedures.appointment_id.patient_id.id
            primary_key = int(all_data_procedures.appointment_id.id)
            teeth = teeths.objects.get(patient_id = p_id)
            if request.method=='POST':
                form = edit_proceduresForm(request.POST or None)
                if form.is_valid():
                    all_data_procedures.procedures_done = form.cleaned_data.get('procedures_done')
                    all_data_procedures.teeth_position = form.cleaned_data.get('teeth_position')
                    all_data_procedures.procedures_fee = form.cleaned_data.get('procedures_fee')
                    all_data_procedures.save()
                    messages.error(request, 'Procedure updated successfully')
                    return redirect('view_additional_appointment_info', primary_key)
                else:
                    messages.error(request, 'Please supply every information and follow the given format')
                    context = {'all_data_procedures' : all_data_procedures, 'teeth' : teeth,"primary_key":primary_key}
                    return render(request, 'editform.html', context)
            else:    
                context = {'all_data_procedures' : all_data_procedures, 'teeth' : teeth,"primary_key":primary_key}
                return render(request, 'editform.html', context)



        elif profiletype == 'tools_items_used': #EDITING tools/items used
            inventory = item_inventory.objects.filter(expiry_status = 'Good for usage')
            all_data_items_tools_used = tools_items_used.objects.get(pk = profile_id)
            primary_key = int(all_data_items_tools_used.appointment_id.id)
            context = {'all_data_items_tools_used' : all_data_items_tools_used, 'inventory' : inventory,'primary_key':primary_key}
            if request.method == 'POST':
                form = edit_tools_items_usedForm(request.POST or None)
                if form.is_valid():
                    before_edit = int(all_data_items_tools_used.quantity_used)
                    all_data_items_tools_used.item_id = form.cleaned_data.get('item_id')
                    all_data_items_tools_used.quantity_used = form.cleaned_data.get('quantity_used')
                    after_edit = int(all_data_items_tools_used.quantity_used)
                    some_bool = update_quantityEdit(before_edit, after_edit, int(profile_id))
                    if some_bool == True:
                        all_data_items_tools_used.units = form.cleaned_data.get('units')
    #                    all_data_items_tools_used.item_tools_fee = form.cleaned_data.get('item_tools_fee')
                        all_data_items_tools_used.date_used = form.cleaned_data.get('date_used')
                        all_data_items_tools_used.save()
                        calculate_price2(int(profile_id))
                        messages.error(request, 'Tools/Items used updated successfully')
                        return redirect('view_additional_appointment_info', primary_key)
                    else:                
                        messages.error(request, 'Quantity used exceeds the quantity available of the item')
                        return render(request, 'editform.html', context)
                else:
                    messages.error(request, 'Please supply every information and follow the given format')
                    return render(request, 'editform.html', context)
            else:
                return render(request, 'editform.html', context)



        else:     #DEFAULT PAG PROFILETYPE == NONE                                             
            all_data_prof = profile.objects.get(pk=profile_id)
            context ={
            'all_data_prof':all_data_prof, 
            'profile_id':profile_id,
            }
            return render(request, 'editform.html', context) #wrong method

def check_services_error2(profile_id):
    alldata= available_services.objects.exclude(pk = profile_id)
    data = available_services.objects.get(pk=profile_id)
    service = data.service_type.lower()
    fee = data.service_fee
    some_bool = True
    for things in alldata:
        if things.service_type.lower() == service and things.service_fee == fee:
            some_bool = False
        else:
            pass
    return some_bool






def check_schedEdit(date, time,doc,profile_id):
    schedule_new = available_schedules.objects.get(pk=profile_id)
    some_id = schedule_new.id
    schedule_all = available_schedules.objects.exclude(pk = some_id)
    for things in schedule_all:
        if things.date == date and things.time == time and things.doctor_lastname == doc:
            return"exist"
        else:
            pass
    if date < date.today():
        return 'date'

    elif date == date.today():
        timeS = datetime.now()
        timeS = timeS.strftime('%H:%M')
        if time.strftime("%H:%M") < timeS:
            return 'time'
        else:
            return 'yes'
    else:
        return 'yes'

def check_avail(profile_id):
    sched = available_schedules.objects.get(pk = profile_id)
    time = sched.time
    date = sched.date
    if date > date.today():
        sched.availability = True
        sched.save()
    elif date == date.today():
        timeS = datetime.now()
        timeS = timeS.strftime('%H:%M')
        if time.strftime("%H:%M") > timeS:
            sched.availability = True
            sched.save()
        else:
            sched.availability = False
            sched.save()
    else:
        sched.availability = False
        sched.save()
    return 0


def cancel_appointment(request, primary_key):
    appoinment_data = appointment_details.objects.get(pk = primary_key)
    appoinment_data.appointment_status = "Cancelled"
    appoinment_data.save()
    messages.error(request, 'Appointment successfully cancelled')
    return redirect('view_appointments')

def calculate_salary2(profile_id):
    salary_data = salary_info.objects.get(pk=profile_id)
    deductions =float(salary_data.others) + float(salary_data.tax) + float(salary_data.insurance) + float(salary_data.pagibig) + float(salary_data.sss) + float(salary_data.philhealth)
    salary = float(salary_data.regular) + float(salary_data.overtime) + float(salary_data.bonus) + float(salary_data.tips)+ float(salary_data.severance)
    total = salary - deductions

    deductions = "%.2f" % deductions
    salary = "%.2f" % salary
    total = "%.2f" % total

    salary_data.total_amount = total
    salary_data.total_deduction = deductions
    salary_data.total_salary = salary
    salary_data.save()
    return 0


def update_editexp(profile_id):
    item = item_inventory.objects.get(pk = profile_id)
    item.expiry_status ='Good for usage'
    item.save()
    return 0
    
def calculate_price2(profile_id):
    items_data = tools_items_used.objects.get(pk = profile_id)
    quantity = int(items_data.quantity_used)
    item_key = items_data.item_id.id
    item_details = item_inventory.objects.get(pk = item_key)
    item_fee = float(item_details.item_fee)
    items_data.item_tools_fee = quantity * item_fee
    items_data.save()
    return 0


def update_quantityEdit(before_edit, after_edit, profile_id):  #MAG REFLECT SA QUANTITY (EDIT SA tools_used
    tools_data = tools_items_used.objects.get(pk = profile_id)
    item_key = tools_data.item_id.id
    item_key = int(item_key)
    item_details = item_inventory.objects.get(pk = item_key)
    quantity_available = int(item_details.quantity)
    quantity_used = int(after_edit)
    before_edit = int(before_edit)
    a = quantity_available + before_edit
    if  a < quantity_used:
        return False
    else:
        new = quantity_available + before_edit
        item_details.quantity = new - quantity_used
        item_details.save()
        return True


def addoption(request):
    return render(request,'addoption.html', {})


def pat_infoadd(request):
    profile_data_all = profile.objects.last()
    prof_id = profile_data_all.id
    prof_id = int(prof_id)
    age = str(profile_data_all.bday)
    age = age.split('-')
    m = int(age[1])
    y = int(age[0])
    d = int(age[2])
    realage = calculate_age(m,y,d)
    teethtype = getteeth(realage)
    context = {'profile_data_all': profile_data_all, 'prof_id':prof_id, 'realage':realage,'teethtype' : teethtype }
    if request.method == "POST":
        form = pat_infoForm(request.POST or None)
        form2 = add_chartForm(request.POST or None)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            '''
            all_data_pat_info = pat_info.objects.all()
            all_data_prof = profile.objects.filter(profile_type = 'Patient')
            context = {"all_data_pat_info":all_data_pat_info, "all_data_prof":all_data_prof}
            '''
            messages.error(request, 'Patient profile added successfully')
            return redirect('prof_view')
            #return render(request, 'prof_view.html',context)
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request,'pat_info.html', context)
    else:
        return render(request,'pat_info.html', context)

def calculate_age(m,y,d):
    bday = date(y, m, d)
    days_in_year = 365.2425   
    age = int((date.today() - bday).days / days_in_year)
    return age

def getteeth(age):
    if age <= 6:
        return 'Baby'
    else:
        return 'Adult'


def view_pat_info(request, primary_key):   
    all_data_pat_info = pat_info.objects.get(profile_id = primary_key)
    key = all_data_pat_info.id
    context = {'all_data_pat_info' : all_data_pat_info,'key':key}
    return render(request, 'view_pat_info.html', context) 
   


def edit_pat_info(request, primary_key):
    all_data_pat_info = pat_info.objects.get(pk = primary_key)
    pk = all_data_pat_info.profile_id.id
    all_data_prof = profile.objects.get(pk = all_data_pat_info.profile_id.id)
    context = {'all_data_pat_info' : all_data_pat_info, 'all_data_prof' : all_data_prof,'pk':pk}
    if request.method == 'POST':
        form = edit_patinfoForm(request.POST or None)
        form2 = profileForm(request.POST or None)
        if form.is_valid() and form2.is_valid():
            date = form2.cleaned_data.get('bday')
            if date > date.today():
                messages.error(request, 'Invalid Date')
                return render(request, 'edit_pat_info.html', context)
            else:
                all_data_prof.fullname = form2.cleaned_data.get('fullname')
                all_data_prof.profile_type = form2.cleaned_data.get('profile_type')
                all_data_prof.contact_number = form2.cleaned_data.get('contact_number')
                all_data_prof.profile_fulladress = form2.cleaned_data.get('profile_fulladress')
                all_data_prof.bday = form2.cleaned_data.get('bday')
                all_data_prof.gender = form2.cleaned_data.get('gender')
                all_data_prof.ecp_fullname = form2.cleaned_data.get('ecp_fullname')
                all_data_prof.ecp_contactnum = form2.cleaned_data.get('ecp_contactnum')
                all_data_prof.ecp_relationship = form2.cleaned_data.get('ecp_relationship')
                all_data_prof.ecp_fulladress = form2.cleaned_data.get('ecp_fulladress')
                all_data_pat_info.pat_occupation= form.cleaned_data.get('pat_occupation')
                all_data_pat_info.pat_allergies = form.cleaned_data.get('pat_allergies')
                all_data_pat_info.save()
                all_data_prof.save()
                primary_key = all_data_prof.id
                messages.error(request, 'Additional Informations successfully edited')
                return redirect('view_pat_info',primary_key)
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request, 'edit_pat_info.html', context)
    else:
        
        return render(request, 'edit_pat_info.html', context)




def view_emp_info(request, primary_key):
    if request.method == 'POST':
        all_data_emp_info = emp_info.objects.get(profile_id = primary_key)
        context = {'all_data_emp_info' : all_data_emp_info}
        return render(request, 'view_emp_info.html', context) 
    else:
        all_data_emp_info = emp_info.objects.get(profile_id = primary_key)
        context = {'all_data_emp_info' : all_data_emp_info}
        return render(request, 'view_emp_info.html', context) 




def edit_emp_info(request, primary_key):
    all_data_emp_info = emp_info.objects.get(pk = primary_key)
    all_data_prof = profile.objects.get(pk=all_data_emp_info.profile_id.id)
    key = all_data_prof.id
    context = {'all_data_emp_info' : all_data_emp_info, 'all_data_prof' : all_data_prof,'key':key}
    if request.method == 'POST':
        
        form = edit_empinfoForm(request.POST or None)
        form2 = profileForm(request.POST or None)
        if form.is_valid() and form2.is_valid():
            date = all_data_prof.bday = form2.cleaned_data.get('bday')
            if date > date.today():
                messages.error(request, 'Invalid Date')
                return render(request, 'edit_emp_info.html', context)
            else:
                all_data_prof.fullname = form2.cleaned_data.get('fullname')
                all_data_prof.profile_type = form2.cleaned_data.get('profile_type')
                all_data_prof.contact_number = form2.cleaned_data.get('contact_number')
                all_data_prof.profile_fulladress = form2.cleaned_data.get('profile_fulladress')
                all_data_prof.bday = form2.cleaned_data.get('bday')
                all_data_prof.gender = form2.cleaned_data.get('gender')
                all_data_prof.ecp_fullname = form2.cleaned_data.get('ecp_fullname')
                all_data_prof.ecp_contactnum = form2.cleaned_data.get('ecp_contactnum')
                all_data_prof.ecp_relationship = form2.cleaned_data.get('ecp_relationship')
                all_data_prof.ecp_fulladress = form2.cleaned_data.get('ecp_fulladress')
                all_data_emp_info.emp_position = form.cleaned_data.get('emp_position')
                all_data_emp_info.emp_status = form.cleaned_data.get('emp_status')
                all_data_prof.save()
                all_data_emp_info.save()
                messages.error(request, 'Additional Informations successfully edited')
                return redirect('view_emp_info', key)
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request, 'edit_emp_info.html', context)
    else:
        return render(request, 'edit_emp_info.html', context)



def emp_infoadd(request):
    profile_data_all = profile.objects.last()
    prof_id = profile_data_all.id
    prof_id = int(prof_id)
    context = {'profile_data_all': profile_data_all, 'prof_id':prof_id}
    if request.method == "POST":
        form = emp_infoForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.error(request, 'Employee profile added successfully')
            return redirect('emp_view')
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request,'emp_info.html', context)
    else:
        return render(request,'emp_info.html', context)


@login_required
def prof_addorview(request):
    return render(request,'prof_addorview.html', {})


@login_required
def emp_addorview(request):
    return render(request,'emp_addorview.html', {})


@login_required
def appointments_addorview(request):
    #Appointments checker
    appointment_data = appointment_details.objects.filter(appointment_status = 'Ongoing')
    for things in appointment_data:
        if things.schedule_id.date < date.today():
            appointment_data2 = appointment_details.objects.get(pk = things.id)
            appointment_data2.appointment_status = 'Finished'
            appointment_data2.save()
        elif things.schedule_id.date == date.today():
            time = datetime.now() 
            time = time.strftime('%H:%M')
            if things.schedule_id.time.strftime("%H:%M") < time:
                appointment_data2 = appointment_details.objects.get(pk = things.id)
                appointment_data2.appointment_status = 'Finished'
                appointment_data2.save()
            else:
                pass
        else:
            pass
    #sched checker
    sched_data = available_schedules.objects.filter(availability = True)
    for things in sched_data:
        if things.date < date.today():
            sched2 = available_schedules.objects.get(pk = things.id)
            sched2.availability = False
            sched2.save()
        elif things.date == date.today():
            time = datetime.now() 
            time = time.strftime('%H:%M')
            if things.time.strftime("%H:%M") < time:
                sched2 = available_schedules.objects.get(pk = things.id)
                sched2.availability = False
                sched2.save()
            else:
                pass
        else:
            pass
    #EXPIRY CHECK
    item_deets = item_inventory.objects.all()
    for things in item_deets:
        if things.expiry_date != None:
            if things.expiry_date < date.today():
                item_data = item_inventory.objects.get(pk = things.id)
                item_data.expiry_status = 'Expired'
                item_data.save()
        elif things.expiry_date == None:
            item_data = item_inventory.objects.get(pk = things.id)
            item_data.expiry_status = 'Item does not expire'
            item_data.save()

    return render(request,'appointments_addorview.html', {})


@login_required
def income_expense_options(request):
    #EXPIRY CHECK
    item_deets = item_inventory.objects.all()
    for things in item_deets:
        if things.expiry_date != None:
            if things.expiry_date < date.today():
                item_data = item_inventory.objects.get(pk = things.id)
                item_data.expiry_status = 'Expired'
                item_data.save()
        elif things.expiry_date == None:
            item_data = item_inventory.objects.get(pk = things.id)
            item_data.expiry_status = 'Item does not expire'
            item_data.save()
    return render(request, 'income_expense_options.html', {})



def prescriptions_addorview(request, primary_key):
    all_data_prof = profile.objects.get(pk = primary_key)
    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof}
    return render(request, 'prescriptions_addorview.html',context)


@login_required
def prof_view(request):
    all_data_prof = profile.objects.filter(profile_type = 'Patient')
    all_data_emp_info = emp_info.objects.all()
    all_data_pat_info = pat_info.objects.all()
    delete_id()
    context={
    'all_data_prof' : all_data_prof,
    'all_data_emp_info' : all_data_emp_info,
    'all_data_pat_info' : all_data_pat_info
    }
    return render(request,'prof_view.html',context)

def delete_id():
    listid = []
    all_data_prof = profile.objects.filter(profile_type = 'Patient')
    all_data_pat_info = pat_info.objects.all()
    temp = 0
    for i in all_data_prof:
        for j in all_data_pat_info:
            if i.id == j.profile_id.id:
                temp = temp + 1
                break
            else:
                pass
        if temp != 1:
            all_data_prof = profile.objects.get(pk = i.id)
            all_data_prof.delete()
        temp = 0


def prof_view_filter(request,order):
    all_data_prof = profile.objects.filter(profile_type = 'Patient').order_by(order)
    all_data_emp_info = emp_info.objects.all()
    all_data_pat_info = pat_info.objects.all()
    context={
    'all_data_prof' : all_data_prof,
    'all_data_emp_info' : all_data_emp_info,
    'all_data_pat_info' : all_data_pat_info
    }
    return render(request,'prof_view_filter.html',context)

def prof_view_searched(request):
    search = request.POST['search']
    if search == "":
        return redirect('prof_view')
    else:
        all_data_prof = profile.objects.filter(fullname__contains=search).filter(profile_type = 'Patient')
        all_data_pat_info = pat_info.objects.all()
        context = {'search' : search,'all_data_prof':all_data_prof,'all_data_pat_info' : all_data_pat_info}
        return render(request, 'prof_view_searched.html',context)
        

@login_required
def emp_view(request):
    if request.user.username != 'admin':
        logout(request)
        messages.error(request, "Must be an admin to access the page")
        return redirect('login_page')
    else:
        all_data_prof = profile.objects.filter(profile_type = 'Employee')
        all_data_emp_info = emp_info.objects.all()
        all_data_salary = salary_info.objects.all()
        delete_id2()
        context = {
                    'all_data_prof' : all_data_prof,
                    'all_data_emp_info' : all_data_emp_info,
                    'all_data_salary': all_data_salary
                }
        return render(request,'emp_view.html',context)

def delete_id2():
    listid = []
    all_data_prof = profile.objects.filter(profile_type = 'Employee')
    all_data_emp_info = emp_info.objects.all()
    temp = 0
    for i in all_data_prof:
        for j in all_data_emp_info:
            if i.id == j.profile_id.id:
                temp = temp + 1
                break
            else:
                pass
        if temp != 1:
            all_data_prof = profile.objects.get(pk = i.id)
            all_data_prof.delete()
        temp = 0


def emp_view_filter(request, order):
    all_data_prof = profile.objects.filter(profile_type = 'Employee').order_by(order)
    all_data_emp_info = emp_info.objects.all()
    all_data_salary = salary_info.objects.all()
    context = {
                'all_data_prof' : all_data_prof,
                'all_data_emp_info' : all_data_emp_info,
                'all_data_salary': all_data_salary
            }
    return render(request,'emp_view_filter.html',context)
        

def emp_view_searched(request):
    search = request.POST['search']
    if search =="":
        return redirect('emp_view')
    else:
        all_data_prof = profile.objects.filter(fullname__contains=search).filter(profile_type = 'Employee')
        all_data_pat_info = pat_info.objects.all()
        context = {'search' : search,'all_data_prof':all_data_prof,'all_data_pat_info' : all_data_pat_info}
        return render(request, 'emp_view_searched.html',context)
'''
 
def addsalary(request): # u can remove this
    all_data_prof = profile.objects.all()
    context = {'all_data_prof' : all_data_prof}

    return render(request, 'addsalary.html', context)


'''
def addsalaryinfo(request, profile_id):
    all_data_prof = profile.objects.get(pk = profile_id)
    context = {'all_data_prof' : all_data_prof, 'profile_id' : profile_id}
    if request.method == 'POST':
        form = salary_infoForm(request.POST or None)
        if form.is_valid(): # and form2.is_valid()
            form.save()
            return redirect('calculate_salary', profile_id)
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request, 'addsalaryinfo.html', context)
    else:
        
        return render(request, 'addsalaryinfo.html', context)



def calculate_salary(request, profile_id):
    salary_data = salary_info.objects.last()
    all_data_prof = profile.objects.get(pk = profile_id)
    primary_key = all_data_prof.id
    deductions = float(salary_data.others) + float(salary_data.tax) + float(salary_data.insurance) + float(salary_data.pagibig) + float(salary_data.sss) + float(salary_data.philhealth)
    salary = float(salary_data.regular) + float(salary_data.overtime) + float(salary_data.bonus) + float(salary_data.tips)+ float(salary_data.severance)
    total = salary - deductions
    deductions = "%.2f" % deductions
    salary = "%.2f" % salary
    total = "%.2f" % total
    if request.method == 'POST':
        form = calculate_salaryForm(request.POST or None)
        if form.is_valid():
            salary_data.total_deduction = form.cleaned_data.get('total_deduction')
            salary_data.total_salary = form.cleaned_data.get('total_salary')
            salary_data.total_amount = form.cleaned_data.get('total_amount')
            salary_data.save()
            messages.error(request, 'Salary details added successfully')
            return redirect('viewsalary', primary_key)
        else:
            context = {"salary_data" : salary_data, 'all_data_prof' : all_data_prof, 'profile_id' : profile_id, 'deductions' :deductions , 'salary' : salary, 'total' :total}
            return render(request, "calculate_salary.html" , context)
    else:
        context = {"salary_data" : salary_data, 'all_data_prof' : all_data_prof, 'profile_id' : profile_id, 'deductions' :deductions , 'salary' : salary, 'total' :total}
        return render(request, "calculate_salary.html" , context)




def viewsalary(request, primary_key):
        all_data_emp_salary = salary_info.objects.filter(profile_id = primary_key)
        all_data_prof_id = profile.objects.get(id = int(primary_key))
        key = all_data_prof_id.id
        context = {
                    'all_data_emp_salary':all_data_emp_salary,
                    'primary_key':primary_key,
                    'key':key,
        }
        return render(request,'viewsalary.html',context)

def viewsalary_filter(request, primary_key, order):
        all_data_emp_salary = salary_info.objects.filter(profile_id = primary_key).order_by(order)
        all_data_prof_id = profile.objects.get(id = int(primary_key))
        key = all_data_prof_id.id
        context = {
                    'all_data_emp_salary':all_data_emp_salary,
                    'primary_key':primary_key,
                    'key':key,
        }
        return render(request,'viewsalary_filter.html',context)

def viewsalary_search(request, primary_key):
    all_data_prof_id = profile.objects.get(id = int(primary_key))
    key = all_data_prof_id.id
    all_data_emp_salary = salary_info.objects.filter(profile_id = primary_key)
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            if date == "":
                return redirect('viewsalary', primary_key)
            else:
                all_data_emp_salary = all_data_emp_salary.filter(date_given__contains = date)
                context = {'all_data_emp_salary':all_data_emp_salary, 'primary_key': primary_key,'key':key}
                return render(request,'viewsalary_search.html',context)
        else:
            context = {'all_data_emp_salary':all_data_emp_salary, 'primary_key': primary_key,'key':key}
            return render(request,'viewsalary_search.html',context)
    else:
        context = {'all_data_emp_salary':all_data_emp_salary, 'primary_key': primary_key,'key':key}
        return render(request,'viewsalary_search.html',context)



@login_required
def add_appointments(request):
    all_data_prof = profile.objects.filter(profile_type = 'Patient')
    context = {'all_data_prof':all_data_prof,}
    return render(request,'add_appointments.html', context)

def add_appointments_search(request):
    all_data_prof = profile.objects.all()
    if request.method =="POST":
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            if name != "":
                all_data_prof = all_data_prof.filter(fullname__contains = name)
                context = {'all_data_prof':all_data_prof,'name':name}
                return render(request,'add_appointments_search.html', context)
            else:
                context = {'all_data_prof':all_data_prof,'name':name}
                return render(request,'add_appointments.html', context)
    else:
        context = {'all_data_prof':all_data_prof,'name':name}
        return render(request,'add_appointments.html', context)



def add_appointmentinfo(request,profile_id, datecondition):
    dateT = date.today()
    timeN = datetime.now()
    timeN = timeN.strftime('%H:%M:%S')
    all_data_available_services = available_services.objects.all()
#    all_data_available_schedules = available_schedules.objects.filter(date__range = [date.today(),'2050-01-31']) #MAKE BETTER FILTER
#    all_data_available_schedules = all_data_available_schedules.filter(availability = True)
    all_data_available_schedules = available_schedules.objects.filter(availability = True).filter(date__contains = datecondition)
    all_data_prof = profile.objects.get(pk = profile_id)
    context = {
                'all_data_prof' : all_data_prof,
                'all_data_available_services':all_data_available_services,
                'all_data_available_schedules':all_data_available_schedules,
                'dateT' : dateT,
                'timeN':timeN,
                'profile_id':profile_id,
                'date':datecondition,
               }
    if request.method == 'POST':
        form = add_appointmentinfoForm(request.POST or None)
        if form.is_valid():
            primary_key = int(form.cleaned_data.get('schedule_id'))
            print(primary_key)
            form.save()
            #pass_key(form.cleaned_data.get('schedule.id')) #form.cleaned_data.get('schedule_id')
            pass_key(primary_key)
#            return redirect('view_appointments')
            messages.error(request, 'Appointment details added successfully')
            return redirect('view_appointments')
        else:
            messages.error(request, 'Please supply every information and follow the given format')          
            return render(request,'add_appointmentinfo.html', context)
    else:
        return render(request,'add_appointmentinfo.html', context)



def choose_date(request, profile_id):
    profile_id = profile_id
    context = {"profile_id":profile_id}
    if request.method == "POST":
        form = searchForm(request.POST or None)
        if form.is_valid():
            datecondition = form.cleaned_data['date']
            return redirect('add_appointmentinfo', profile_id, datecondition)
        else:
            return render(request,'choose_date.html',context)
    else:
        return render(request,'choose_date.html',context)

def check_available_schedule(request, profile_id, date):
    available_sched = available_schedules.objects.filter(date__contains = date).filter(availability = True)
    dateN = getDatee2(date)
    context = {'available_sched':available_sched,'profile_id':profile_id, 'date':date,'dateN':dateN}
    return render(request,'check_available_schedule.html',context)

def check_available_services(request, profile_id, date):
    services_data = available_services.objects.filter(availability = True)
    context = {"services_data":services_data,'profile_id':profile_id, 'date':date,}
    return render(request,'check_available_services.html',context)

def check_available_services_search(request, profile_id, date):
    services_data = available_services.objects.filter(availability = True)
    if request.method =='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            services_data = services_data.filter(service_type__contains = name)
            context = {"services_data":services_data,'profile_id':profile_id, 'date':date,}
            return render(request,'check_available_services_search.html',context)
    else:
        context = {"services_data":services_data,'profile_id':profile_id, 'date':date,}
        return render(request,'check_available_services_search.html',context)

def pass_key(primary_key):
    all_data_schedule = available_schedules.objects.get(pk = primary_key)
    if all_data_schedule.availability == True:
        all_data_schedule.availability = False  
        all_data_schedule.save()
    elif all_data_schedule.availability == False:
        all_data_schedule.availability = True 
        all_data_schedule.save() 
    return 0

@login_required
def add_services(request):
    if request.method == 'POST':
        form = add_servicesForm(request.POST or None)
        if form.is_valid():
            sfee = form.cleaned_data.get("service_fee")
            stype = form.cleaned_data.get("service_type").lower()
            some_bool = check_services_error(stype,sfee)
            if some_bool == True:
                form.save()
                messages.error(request, 'Service added successfully')
                return redirect('view_services')
            else:
                messages.error(request, 'Service already exists')
                return render(request, 'add_services.html', {})

        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request, 'add_services.html', {} )
    else:
        return render(request, 'add_services.html', {})

def check_services_error(stype,sfee):
    data = available_services.objects.all()
    some_bool = True
    for i in data:
        if i.service_fee == sfee and i.service_type.lower() == stype:
            some_bool = False
        else:
            pass
    return some_bool


@login_required
def add_schedule(request):
    if request.method == 'POST':
        form = add_scheduleForm(request.POST or None)
        if form.is_valid():
            form.save()
            some_bool = check_schedule()
            if some_bool == 'exist':
                messages.error(request, 'Schedule Already Exist')
                return render(request,'add_schedule.html', {})
            elif some_bool == 'date':
                messages.error(request, 'Date already passed')
                return render(request,'add_schedule.html', {})
            elif some_bool == 'time':
                messages.error(request, 'Time already passed')
                return render(request,'add_schedule.html', {})
            else:
                messages.error(request, 'Available schedule added successfully')
                return redirect('view_schedule')
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request,'add_schedule.html', {})
    else:
        return render(request,'add_schedule.html', {})



def check_schedule():
    #schedule checker(input)
    schedule_new = available_schedules.objects.last()
    some_id = schedule_new.id
    schedule_all = available_schedules.objects.exclude(pk = some_id)
    for things in schedule_all:
        if things.date == schedule_new.date and things.time == schedule_new.time and things.doctor_lastname == schedule_new.doctor_lastname:
            schedule_new.delete()
            return "exist" 
        else:
            pass
    if schedule_new.date < date.today():
        schedule_new.delete()
        return "date" 
    elif schedule_new.date == date.today():
        time = datetime.now() 
        time = time.strftime('%H:%M')
        if schedule_new.time.strftime("%H:%M") < time:
            schedule_new.delete()
            return 'time'
        else:
            return 'yes'
    else:
        return 'yes'

    
@login_required
def view_services(request):
    all_data_services = available_services.objects.all()
#    all_data_services.service_fee = 
    context = {'all_data_services':all_data_services}
    return render(request, 'view_services.html', context)


def view_services_filter(request, order):
    all_data_services = available_services.objects.all().order_by(order)
#    all_data_services.service_fee = 
    context = {'all_data_services':all_data_services}
    return render(request, 'view_services_filter.html', context)


def view_services_search(request):
    search = request.POST['search']
    if search == "":
        return redirect('view_services')
    else:
        all_data_services = available_services.objects.filter(service_type__contains=search)
        context = {'all_data_services' : all_data_services}
        return render(request, 'view_services_search.html',context)

@login_required
def view_schedule(request):
    #SCHEDULE CHECKER
    sched_data = available_schedules.objects.filter(availability = True)
    for things in sched_data:
        if things.date < date.today():
            sched2 = available_schedules.objects.get(pk = things.id)
            sched2.availability = False
            sched2.save()
        elif things.date == date.today():
            time = datetime.now() 
            time = time.strftime('%H:%M')
            if things.time.strftime("%H:%M") < time:
                sched2 = available_schedules.objects.get(pk = things.id)
                sched2.availability = False
                sched2.save()
            else:
                pass
        else:
            pass
    all_data_schedule = available_schedules.objects.filter(availability = True)
    context = {'all_data_schedule':all_data_schedule}
    return render(request, 'view_schedule.html', context)

def view_schedule_filter(request,order):
    all_data_schedule = available_schedules.objects.filter(availability = True)
    all_data_schedule = all_data_schedule.order_by(order)
    context = {'all_data_schedule':all_data_schedule}
    return render(request, 'view_schedule_filter.html', context)



def view_schedule_search(request):
    all_data_schedule = available_schedules.objects.filter(availability = True)
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            if name == "" and date =="":
                return redirect('view_schedule')
            elif name != None:
                all_data_schedule = all_data_schedule.filter(doctor_lastname__contains = name)
                if date != None:
                    all_data_schedule = all_data_schedule.filter(date__contains=date)
                    context = {'all_data_schedule' : all_data_schedule, 'date':date,'name':name}
                else:
                    context = {'all_data_schedule' : all_data_schedule, 'date':date,'name':name}
            elif date != None:
                all_data_schedule = all_data_schedule.filter(date__contains=date)
                if name!= None:
                    all_data_schedule = all_data_schedule.filter(doctor_lastname__contains = name)
                    context = {'all_data_schedule' : all_data_schedule, 'date':date,'name':name}
                else:
                    context = {'all_data_schedule' : all_data_schedule, 'date':date,'name':name}
            return render(request, 'view_schedule_search.html',context)


'''
def edit_services(request):
    all_data_services = available_services.objects.all()
    context = {'all_data_services':all_data_services}
    return render(request, 'edit_services.html', context)

'''
'''
def edit_schedule(request):
    #SCHEDULE CHECKER
    sched_data = available_schedules.objects.filter(availability = True)
    for things in sched_data:
        if things.date < date.today():
            sched2 = available_schedules.objects.get(pk = things.id)
            sched2.availability = False
            sched2.save()
        elif things.date == date.today():
            time = datetime.now() 
            time = time.strftime('%H:%M')
            if things.time.strftime("%H:%M") < time:
                sched2 = available_schedules.objects.get(pk = things.id)
                sched2.availability = False
                sched2.save()
            else:
                pass
        else:
            pass
    all_data_schedule = available_schedules.objects.all()
    context = {'all_data_schedule' : all_data_schedule}
    return render(request, 'edit_schedule.html', context)

'''
@login_required
def inventory_options(request):
    #EXPIRY CHECK
    item_deets = item_inventory.objects.all()
    for things in item_deets:
        if things.expiry_date != None:
            if things.expiry_date < date.today():
                item_data = item_inventory.objects.get(pk = things.id)
                item_data.expiry_status = 'Expired'
                item_data.save()
        elif things.expiry_date == None:
            item_data = item_inventory.objects.get(pk = things.id)
            item_data.expiry_status = 'Item does not expire'
            item_data.save()
    return render(request,'inventory_options.html', {})


@login_required
def view_inventory(request):
    #EXPIRY CHECK
    item_deets = item_inventory.objects.all()
    for things in item_deets:
        if things.expiry_date != None:
            if things.expiry_date < date.today():
                item_data = item_inventory.objects.get(pk = things.id)
                item_data.expiry_status = 'Expired'
                item_data.save()
        elif things.expiry_date == None:
            item_data = item_inventory.objects.get(pk = things.id)
            item_data.expiry_status = 'Item does not expire'
            item_data.save()
    all_data_inventory = item_inventory.objects.all()
    context = {'all_data_inventory' : all_data_inventory}
    return render(request,'view_inventory.html', context)

def view_inventory_filter(request,order):
    all_data_inventory = item_inventory.objects.all().order_by(order)
    context = {'all_data_inventory' : all_data_inventory}
    return render(request,'view_inventory_filter.html', context)

def create_inventory_report(request):
    expired = item_inventory.objects.filter(expiry_status = 'Expired')
    good = item_inventory.objects.filter(expiry_status = 'Good for usage')
    no_expiry = item_inventory.objects.filter(expiry_status = 'Item does not expire')
    context = {'expired':expired,'good':good,'no_expiry':no_expiry}
    return render(request, 'create_inventory_report.html',context)

def view_inventory_search(request):
    if request.method=='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            loc = form.cleaned_data['loc']
            name = form.cleaned_data['name']
            cat = form.cleaned_data['cat']
            exp = form.cleaned_data['exp']
            code = form.cleaned_data['code']
            all_data_inventory = item_inventory.objects.all()
            if date == "" and loc == "" and name == "" and cat == "" and exp =="" and code =="":
                return redirect('view_inventory')
            else:
                context = filterloop(name,date,loc,cat,exp, code)
                return render(request,'view_inventory_search.html',context)
        else:
            return redirect('view_inventory')



'''
def edit_inventory(request):
    all_data_inventory = item_inventory.objects.all()
    context = {'all_data_inventory' : all_data_inventory}
    return render(request,'edit_inventory.html', context)
'''

@login_required
def add_inventory(request):
    if request.method == 'POST':
        form = add_inventoryForm(request.POST or None)
        if form.is_valid():
            if form.cleaned_data.get('quantity') <= 0:
                messages.error(request, 'Invalid Quantity')
                return render(request,'add_inventory.html', {})
            else:
                form.save()
                some_bool = check_exp_date()
                if some_bool == True:
                    messages.error(request, 'Item details added successfully')
                    return redirect('view_inventory')
                else:
                    messages.error(request, 'Invalid Date')
                    return render(request,'add_inventory.html', {})
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request,'add_inventory.html', {})
    else:
        return render(request,'add_inventory.html', {})


def check_exp_date():
    item = item_inventory.objects.last()
    if item.expiry_date == None:
        return True
    else:
        if item.expiry_date < date.today():
            item.delete()
            return False
        else:
            return True



def schedule_checker():
    #Schedule checker
    appointment_data = appointment_details.objects.filter(appointment_status = 'Ongoing')
    for things in appointment_data:
        if things.schedule_id.date < date.today():
            appointment_data2 = appointment_details.objects.get(pk = things.id)
            appointment_data2.appointment_status = 'Finished'
            appointment_data2.save()
        elif things.schedule_id.date == date.today():
            time = datetime.now() 
            time = time.strftime('%H:%M')
            if things.schedule_id.time.strftime("%H:%M") < time:
                appointment_data2 = appointment_details.objects.get(pk = things.id)
                appointment_data2.appointment_status = 'Finished'
                appointment_data2.save()
            else:
                pass
        else:
            pass

def appointments_checker():
    #Appointments checker
    appointment_data = appointment_details.objects.filter(appointment_status = 'Ongoing')
    for things in appointment_data:
        if things.schedule_id.date < date.today():
            appointment_data2 = appointment_details.objects.get(pk = things.id)
            appointment_data2.appointment_status = 'Finished'
            appointment_data2.save()
        elif things.schedule_id.date == date.today():
            time = datetime.now() 
            time = time.strftime('%H:%M')
            if things.schedule_id.time.strftime("%H:%M") < time:
                appointment_data2 = appointment_details.objects.get(pk = things.id)
                appointment_data2.appointment_status = 'Finished'
                appointment_data2.save()
            else:
                pass
        else:
            pass

def changecalendar(request,month,year):
    mon = int(month)
    year = int(year)
    cal = HTMLCalendar().formatmonth(year,mon)
    all_data_schedule = available_schedules.objects.all()
    all_data_services = available_services.objects.all()
    all_data_appointments = appointment_details.objects.filter(appointment_status = 'Ongoing')
    context = {
                'all_data_appointments' : all_data_appointments,
                'all_data_services' : all_data_services,
                'all_data_schedule' : all_data_schedule,
                'date_str' : date_str,
                'mon' : mon,
                'year' : year,
                'cal' : cal,
                'day' : day
              }
    return render(request, 'home.html', context)


def view_appointments_cancelled(request): 
    all_data_schedule = available_schedules.objects.all()
    all_data_services = available_services.objects.all()
    all_data_appointments = appointment_details.objects.filter(appointment_status = 'Cancelled')
    context = {
                'all_data_appointments' : all_data_appointments,
                'all_data_services' : all_data_services,
                'all_data_schedule' : all_data_schedule,
              }
    return render(request, 'view_appointments_cancelled.html', context)


def view_finished_appointments(request):
    all_data_appointments = appointment_details.objects.filter(payment_status = 'Pending')
    all_data_appointments = all_data_appointments.filter(appointment_status = 'Finished')
    context = {'all_data_appointments' : all_data_appointments}
    return render(request, 'view_finished_appointments.html', context)



def add_procedures(request, primary_key):
    all_data_appointments = appointment_details.objects.get(pk=primary_key)
    p_id = all_data_appointments.patient_id.id
    teeth = teeths.objects.get(patient_id = p_id)
    form = add_proceduresForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.error(request, 'Procedure details added successfully')
            return redirect('view_additional_appointment_info', primary_key) #return redirect('add_procedure_option')
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            context = {'primary_key':primary_key, 'form':form, 'all_data_appointments':all_data_appointments, 'teeth':teeth }
            return render(request, 'add_procedures.html', context) #put error message
    else:
        context = {'primary_key':primary_key, 'form':form, 'all_data_appointments':all_data_appointments, 'teeth':teeth }
        return render(request, 'add_procedures.html', context)



def add_procedure_option(request):
    all_data_procedures = procedures_done.objects.last()
    primary_key = all_data_procedures.appointment_id.id
    context = {'primary_key': primary_key}
    return render(request, 'add_procedure_option.html',context)



def add_tools_items_used(request, primary_key):
    all_data_appointments = appointment_details.objects.get(pk=primary_key)
    all_data_inventory = item_inventory.objects.filter(expiry_status = 'Good for usage')
    form = add_tools_items_usedForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            somebool = check_unit(primary_key)
            if somebool == True:
                some_bool = update_quantity(primary_key)
                if some_bool == True:
                    calculate_price()
                    messages.error(request, 'Tools/Item used successfully recorded')
                    return redirect('view_additional_appointment_info', primary_key)
                else:
                    messages.error(request, 'Quantity used exceeds the quantity available of the item')
                    context = {'primary_key':primary_key, 'form':form, 'all_data_appointments':all_data_appointments, 'all_data_inventory':all_data_inventory}
                    return render(request, 'add_tools_items_used.html', context) #PUT ERROR MESSAGE
            else:
                messages.error(request, 'Tools Units is Wrong')
                context = {'primary_key':primary_key, 'form':form, 'all_data_appointments':all_data_appointments, 'all_data_inventory':all_data_inventory}
                return render(request, 'add_tools_items_used.html', context) #PUT ERROR MESSAGE
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            context = {'primary_key':primary_key, 'form':form, 'all_data_appointments':all_data_appointments, 'all_data_inventory':all_data_inventory}
            return render(request, 'add_tools_items_used.html', context) #PUT ERROR MESSAGE
    else:
        context = {'primary_key':primary_key, 'form':form, 'all_data_appointments':all_data_appointments, 'all_data_inventory':all_data_inventory}
        return render(request, 'add_tools_items_used.html', context)




def check_unit(primary_key):
    items_data = tools_items_used.objects.last()
    item_key = items_data.item_id.id
    item_details = item_inventory.objects.get(pk = item_key)
    units1 = items_data.units
    units2 = item_details.units
    if units1.lower() == units2.lower():
        return True
    else:
        items_data.delete()
        return False



def calculate_price():
    items_data = tools_items_used.objects.last()
    quantity = int(items_data.quantity_used)
    item_key = items_data.item_id.id
    item_details = item_inventory.objects.get(pk = item_key)
    item_fee = float(item_details.item_fee)
    items_data.item_tools_fee = quantity * item_fee
    items_data.save()
    return 0



def update_quantity(primary_key):  #MAG REFLECT SA QUANTITY (tools_used)
    all_data_appointments = appointment_details.objects.get(pk=primary_key)
    tools_data = tools_items_used.objects.last()
    item_key = tools_data.item_id.id
    item_key = int(item_key)
    item_details = item_inventory.objects.get(pk = item_key)
    used = int(tools_data.quantity_used)
    available_q = int(item_details.quantity)
    if used <= available_q:
        after = available_q - used
        item_details.quantity = after
        item_details.save()
        return True
    else:
        tools_data.delete()
        return False 



def add_tools_items_used_option(request):
    all_data_tools_items_used = tools_items_used.objects.last()
    primary_key = all_data_tools_items_used.appointment_id.id
    context = {'primary_key': primary_key}
    return render(request, 'add_tools_items_used_option.html',context)




def view_additional_appointment_info(request, primary_key):
    all_data_tools_items_used = tools_items_used.objects.filter(appointment_id = primary_key)
    all_data_procedures = procedures_done.objects.filter(appointment_id = primary_key)
    all_data_appointments = appointment_details.objects.get(pk=primary_key)
#    pat_id = all_data_appointments.patient_id.id
#    teeth_data = teeths.objects.get(patient_id=pat_id)
#    teeth = teeth_data.teeth_type
    procedures = procedures_done.objects.filter(appointment_id = primary_key).aggregate(Sum('procedures_fee'))
    tools_fee = tools_items_used.objects.filter(appointment_id = primary_key).aggregate(Sum('item_tools_fee'))
    if procedures["procedures_fee__sum"] != None:
        tot_procedures = "%.2f" % procedures["procedures_fee__sum"]
    else:
        tot_procedures = 0
    if tools_fee["item_tools_fee__sum"] != None:
        tot_fee = "%.2f" % tools_fee["item_tools_fee__sum"]
    else:
        tot_fee = 0
        
        
    context = {
                'all_data_tools_items_used' : all_data_tools_items_used,
                'all_data_procedures' : all_data_procedures,
                'all_data_appointments' : all_data_appointments,
                'procedures' : procedures,
                'tools_fee' : tools_fee,
                'primary_key':primary_key,
                'tot_fee':tot_fee,
                'tot_procedures':tot_procedures
#                'teeth' : teeth,

              }
    return render(request, 'view_additional_appointment_info.html', context )



def make_payment(request, appointment_id, service_fee, procedures_fee, tools_fee):
    procedures_fee = "%.2f" % float(procedures_fee)
    tools_fee = "%.2f" % float(tools_fee)

    pk = appointment_details.objects.get(pk = appointment_id)
    pk = pk.id
    if request.method == 'POST':
        form = make_paymentForm(request.POST or None)
        if form.is_valid():
            form.save()
            primary_key = form.cleaned_data.get('appointment_id')
            toPaid(int(primary_key))
            messages.success(request, "Payment done successfully. Please proceed to the patient profile to see details")
            return redirect('view_appointments')
        else:
            all_data_appointments = appointment_details.objects.get(pk = appointment_id)
            if procedures_fee == 'None':
                total_payment =  float(tools_fee) #float(service_fee) +
                total_payment = "%.2f" % total_payment
            elif tools_fee == 'None':
                total_payment =  float(procedures_fee) #float(service_fee) +
                total_payment = "%.2f" % total_payment
#            elif service_fee == 'None':
#               total_payment =float(procedures_fee) + float(tools_fee)
            else:
                total_payment =  float(procedures_fee) + float(tools_fee) #float(service_fee) +
                total_payment = "%.2f" % total_payment
            messages.error(request, 'Please input all forms and follow the given format') 
            context = {'pk':pk, 'all_data_appointments' : all_data_appointments, 'procedures_fee' : procedures_fee, 'tools_fee' : tools_fee, 'total_payment' : total_payment}   #, 'service_fee' : service_fee 
            return render(request, 'make_payment.html', context) #put input error message
    else:
        all_data_appointments = appointment_details.objects.get(pk = appointment_id)
        if procedures_fee == 'None':
            total_payment =  float(tools_fee) #float(service_fee) +
            total_payment = "%.2f" % total_payment
        elif tools_fee == 'None':
            total_payment =  float(procedures_fee) #float(service_fee) +
            total_payment = "%.2f" % total_payment
#        elif service_fee == 'None':
#            total_payment =float(procedures_fee) + float(tools_fee)
        else:
            total_payment = float(procedures_fee) + float(tools_fee) #float(service_fee) + 
            total_payment = "%.2f" % total_payment
        context = {'pk':pk, 'all_data_appointments' : all_data_appointments, 'service_fee' : service_fee, 'procedures_fee' : procedures_fee, 'tools_fee' : tools_fee, 'total_payment' : total_payment}    
        return render(request, 'make_payment.html', context)



def check_inventory(request, primary_key):
     #EXPIRY CHECK
    item_deets = item_inventory.objects.all()
    for things in item_deets:
        if things.expiry_date != None:
            if things.expiry_date < date.today():
                item_data = item_inventory.objects.get(pk = things.id)
                item_data.expiry_status = 'Expired'
                item_data.save()
        elif things.expiry_date == None:
            item_data = item_inventory.objects.get(pk = things.id)
            item_data.expiry_status = 'Item does not expire'
            item_data.save()

    all_data_inventory = item_inventory.objects.all()
    context = {'all_data_inventory' : all_data_inventory, 'primary_key' : primary_key}
    return render(request,'check_inventory.html', context)


def check_inventory_filter(request, primary_key,order):
    all_data_inventory = item_inventory.objects.all().order_by(order)
    context = {'all_data_inventory' : all_data_inventory, 'primary_key' : primary_key}
    return render(request,'check_inventory_filter.html', context)

def check_inventory_search(request, primary_key):
    if request.method=='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            loc = form.cleaned_data['loc']
            name = form.cleaned_data['name']
            cat = form.cleaned_data['cat']
            exp = form.cleaned_data['exp']
            code = form.cleaned_data['code']
            key = primary_key
            all_data_inventory = item_inventory.objects.all()
            if date == "" and loc == "" and name == "" and cat == "" and exp == "" and code =="":
                return redirect('check_inventory', primary_key)
            else:
                context = filterloop2(name,date,loc,cat,exp,key,code)
                return render(request,'check_inventory_search.html', context)
        else:
            return redirect('check_inventory', primary_key)
    else:
        all_data_inventory = item_inventory.objects.all()
        context = {'all_data_inventory':all_data_inventory,'primary_key':primary_key}
        return render(request,'check_inventory.html', context)
    '''
    all_data_inventory = item_inventory.objects.all()
    context = {'all_data_inventory' : all_data_inventory, 'primary_key' : primary_key}
    return render(request,'check_inventory_search.html', context)
    '''

def check_medicine(request, primary_key):
    cat_list = ["Medicine", "Antibiotics", "Pain reliever", "Tranexamic acid"]
    item_data = item_inventory.objects.filter(itemcategory__in =cat_list).filter(expiry_status = "Good for usage")
    context = {"item_data":item_data, "primary_key":primary_key}
    return render(request,'check_medicine.html', context)

def check_medicine_filter(request, primary_key,order):
    item_data = item_inventory.objects.filter(itemcategory__contains ="medicine").filter(expiry_status = "Good for usage")
    item_data = item_data.order_by(order)
    context = {"item_data":item_data, "primary_key":primary_key}
    return render(request,'check_medicine_filter.html', context)

def check_medicine_search(request, primary_key):
    if request.method=="POST":
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            loc = form.cleaned_data['loc']
            name = form.cleaned_data['name']
            cat = form.cleaned_data['cat']
            exp = form.cleaned_data['exp']
            code = form.cleaned_data['code']
            key = primary_key
            item_data = item_inventory.objects.all()
            if date == "" and loc == "" and name == "" and cat == "" and exp == "" and code =="":
                return redirect('check_medicine', primary_key)
            else:
                context = filterloop4(name,date,loc,cat,exp,key,code)
                return render(request,'check_medicine_search.html', context)
        else:
            return redirect('check_medicine', primary_key)
    else:
        all_data_inventory = item_inventory.objects.all()
        context = {'all_data_inventory':all_data_inventory,'primary_key':primary_key}
        return render(request,'check_medicine.html', context)


def toPaid(primary_key):
    appointment = appointment_details.objects.get(pk = primary_key)
    appointment.payment_status = 'Paid'
    appointment.save()
    return 0



def view_patient_appointment_history(request, primary_key):
    all_data_appointments = appointment_details.objects.filter(patient_id = primary_key)
    appointments_finished = all_data_appointments.filter(appointment_status = 'Finished')
    appointments_cancelled = all_data_appointments.filter(appointment_status = 'Cancelled')
    context = {
                'all_data_appointments' : all_data_appointments,
                'appointments_finished' : appointments_finished,
                'appointments_cancelled' : appointments_cancelled,
                'primary_key' : primary_key,

              }
    return render(request, 'view_patient_appointment_history.html', context)


def view_patient_appointment_history_filter(request, primary_key,order):
    all_data_appointments = appointment_details.objects.filter(patient_id = primary_key).order_by(order)
    appointments_finished = all_data_appointments.filter(appointment_status = 'Finished').order_by(order)
    appointments_cancelled = all_data_appointments.filter(appointment_status = 'Cancelled').order_by(order)
    context = {
                'all_data_appointments' : all_data_appointments,
                'appointments_finished' : appointments_finished,
                'appointments_cancelled' : appointments_cancelled,
                'primary_key' : primary_key,

              }
    return render(request, 'view_patient_appointment_history_filter.html', context)


def view_patient_appointment_history_search(request, primary_key):
    services = available_services.objects.all()
    docs = available_schedules.objects.all()
    all_data_appointments = appointment_details.objects.filter(patient_id = primary_key)
    appointments_finished = all_data_appointments.filter(appointment_status = 'Finished')
    appointments_cancelled = all_data_appointments.filter(appointment_status = 'Cancelled')
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            id_list = []
            id_list2 = []
            id_list3 = []
            doc = form.cleaned_data['doc']
            service = form.cleaned_data['service']
            date = form.cleaned_data['date']
            if doc =="" and service =="" and date=="":
                return redirect('view_patient_appointment_history', primary_key)
            elif doc != "":
                docs = docs.filter(doctor_lastname__contains = doc)
                for j in docs:
                    id_list2.append(j.id)
                appointments_finished = appointments_finished.filter(schedule_id__in = id_list2)
                appointments_cancelled = appointments_cancelled.filter(schedule_id__in = id_list2)

                if service != "":
                    services = services.filter(service_type__contains = service)
                    for i in services:
                        id_list.append(i.id)
                    appointments_finished = appointments_finished.filter(service_id__in = id_list)
                    appointments_cancelled = appointments_cancelled.filter(service_id__in = id_list)
                    if date != "":
                        sched = available_schedules.objects.filter(date__contains = date)
                        for i in sched:
                            id_list3.append(i.id)
                        appointments_finished = appointments_finished.filter(schedule_id__in = id_list3)
                        appointments_cancelled = appointments_cancelled.filter(schedule_id__in = id_list3)
                        context={
                                'all_data_appointments' : all_data_appointments,
                                'appointments_finished' : appointments_finished,
                                'appointments_cancelled' : appointments_cancelled,
                                'primary_key':primary_key,
                                }
                    else:
                        context={
                                'all_data_appointments' : all_data_appointments,
                                'appointments_finished' : appointments_finished,
                                'appointments_cancelled' : appointments_cancelled,
                                'primary_key':primary_key,
                                }
                elif date != "":
                    sched = available_schedules.objects.filter(date__contains = date)
                    for i in sched:
                        id_list3.append(i.id)
                    appointments_finished = appointments_finished.filter(schedule_id__in = id_list3)
                    appointments_cancelled = appointments_cancelled.filter(schedule_id__in = id_list3)
                    context={
                                'all_data_appointments' : all_data_appointments,
                                'appointments_finished' : appointments_finished,
                                'appointments_cancelled' : appointments_cancelled,
                                'primary_key':primary_key,
                            }
                else:
                    context={
                            'all_data_appointments' : all_data_appointments,
                            'appointments_finished' : appointments_finished,
                            'appointments_cancelled' : appointments_cancelled,
                            'primary_key':primary_key,
                            }
            elif service != "":
                services = services.filter(service_type__contains = service)
                for i in services:
                    id_list.append(i.id)
                appointments_finished = appointments_finished.filter(service_id__in = id_list)
                appointments_cancelled = appointments_cancelled.filter(service_id__in = id_list)
                if date!="":
                    sched = available_schedules.objects.filter(date__contains = date)
                    for i in sched:
                        id_list3.append(i.id)
                    appointments_finished = appointments_finished.filter(schedule_id__in = id_list3)
                    appointments_cancelled = appointments_cancelled.filter(schedule_id__in = id_list3)
                    context={
                                'all_data_appointments' : all_data_appointments,
                                'appointments_finished' : appointments_finished,
                                'appointments_cancelled' : appointments_cancelled,
                                'primary_key':primary_key,
                            }
                else:
                    context={
                            'all_data_appointments' : all_data_appointments,
                            'appointments_finished' : appointments_finished,
                            'appointments_cancelled' : appointments_cancelled,
                            'primary_key':primary_key,
                            }
            elif date != "":
                sched = available_schedules.objects.filter(date__contains = date)
                for i in sched:
                    id_list3.append(i.id)
                appointments_finished = appointments_finished.filter(schedule_id__in = id_list3)
                appointments_cancelled = appointments_cancelled.filter(schedule_id__in = id_list3)
                context={
                        'all_data_appointments' : all_data_appointments,
                        'appointments_finished' : appointments_finished,
                        'appointments_cancelled' : appointments_cancelled,
                        'primary_key':primary_key,
                        }
            else:
                context = {
                            'all_data_appointments' : all_data_appointments,
                            'appointments_finished' : appointments_finished,
                            'appointments_cancelled' : appointments_cancelled,
                            'primary_key':primary_key,
                          }
            return render(request, 'view_patient_appointment_history_search.html', context)
        else:
            return render(request, 'view_patient_appointment_history_search.html', context)
    else:
        return render(request, 'view_patient_appointment_history_search.html', context)


def view_only_appointment_history(request, primary_key):
    all_data_tools_items_used = tools_items_used.objects.filter(appointment_id = primary_key)
    all_data_procedures = procedures_done.objects.filter(appointment_id = primary_key)
    all_data_appointments = appointment_details.objects.get(pk=primary_key)
    new_primary_key = all_data_appointments.patient_id.id
    context = { 'all_data_appointments' : all_data_appointments,
                'all_data_tools_items_used' : all_data_tools_items_used,
                'all_data_procedures' : all_data_procedures,
                'new_primary_key' : new_primary_key,
              }
    return render(request, 'view_only_appointment_history.html', context)



def view_only_payment_history(request, primary_key):
    all_data_payment = payment.objects.get(appointment_id = primary_key)
    context = {'all_data_payment' : all_data_payment, 'primary_key' : primary_key}
    return render(request, 'view_only_payment_history.html', context)



def add_prescriptions(request, primary_key):
    all_data_prof = profile.objects.get(pk = primary_key)
    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof}
    if request.method == 'POST':
        form = prescriptionForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.error(request, 'Patient prescription added successfully')
            return redirect('view_prescriptions', primary_key)
        else:
            messages.error(request, 'Please input all forms and follow the given format')
            return render(request,'add_prescriptions.html', context)
    else:
        return render(request, 'add_prescriptions.html', context)


#def check_presc_error():

#    if i.date_given ==var and i.intake_instructions.lower()==var and i.units.lower()==var and i.quantity==var and i.meds_prescription.lower()==var  and i.given_by.lower()==var and i.patient_id==var
   
    
    
    
    


def view_prescriptions(request, primary_key):
    all_data_prof = profile.objects.get(pk = primary_key)
    all_data_prescriptions = prescription_management.objects.filter(patient_id = primary_key)
    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'all_data_prescriptions' : all_data_prescriptions}
    return render(request, 'view_prescriptions.html', context)

def view_prescriptions_filter(request, primary_key, order):
    all_data_prof = profile.objects.get(pk = primary_key)
    all_data_prescriptions = prescription_management.objects.filter(patient_id = primary_key).order_by(order)
    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'all_data_prescriptions' : all_data_prescriptions}
    return render(request, 'view_prescriptions_filter.html', context)

def view_prescriptions_search(request, primary_key):
    all_data_prof = profile.objects.get(pk = primary_key)
    all_data_prescriptions = prescription_management.objects.filter(patient_id = primary_key)
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            if name == "":
                return redirect('view_prescriptions', primary_key)
            else:
                all_data_prescriptions = all_data_prescriptions.filter(meds_prescription__contains = name)
                context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'all_data_prescriptions' : all_data_prescriptions}
        else:
            context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'all_data_prescriptions' : all_data_prescriptions}
        return render(request, 'view_prescriptions_search.html', context)
    else:
        context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'all_data_prescriptions' : all_data_prescriptions}
        return render(request, 'view_prescriptions_search.html', context)


def buy_prescriptions(request, primary_key):
    cat_list = ["Medicine", "Antibiotics", "Pain reliever", "Tranexamic acid"]
    all_data_inv = item_inventory.objects.filter(itemcategory__in = cat_list).filter(expiry_status = "Good for usage")
    all_data_inventory = all_data_inv.filter(expiry_status = 'Good for usage')
    all_data_prof = profile.objects.get(pk = primary_key)
    context = {'all_data_prof' : all_data_prof, 'primary_key' : primary_key, 'all_data_inventory' : all_data_inventory}
    if request.method == 'POST':
        form = buy_prescriptionForm(request.POST or None)
        if form.is_valid():
            form.save()
            some_bool = update_quantity2(primary_key)
            if some_bool == True:
                return redirect('calculate_payment', primary_key)
            else:
                messages.error(request, 'Invalid Quantity or Units')
                return render(request, 'buy_prescriptions.html', context )
        else:
            messages.error(request, 'Please Complete the form and follow the given format')
            return render(request, 'buy_prescriptions.html', context )
    else:
        return render(request, 'buy_prescriptions.html', context )



def update_quantity2(primary_key): #MAG REFLECT SA QUANTITY PRESCRIPTION BUY
    presc_info = prescription_purchase.objects.last()
    item_key = presc_info.item_id.id
    item_details = item_inventory.objects.get(pk = item_key)
    used = int(presc_info.quantity)
    units1 = presc_info.units
    units2 = item_details.units
    available_q = int(item_details.quantity)
    if used == 0:
        presc_info.delete()
        return False
    elif used <= available_q:
        after = available_q - used
        item_details.quantity = after
        if units1.lower() == units2.lower():
            item_details.save()
            return True
        else:
            presc_info.delete()
            return False
    
    else:
        presc_info.delete()
        return False




def calculate_payment(request, primary_key):
    purchase_data = prescription_purchase.objects.last()
    all_data_prof = all_data_prof = profile.objects.get(pk = primary_key)
    price = float(purchase_data.item_id.item_fee)
    q = int(purchase_data.quantity)
    total_amount = price * q
    context = {'primary_key' : primary_key, 'purchase_data':purchase_data, 'all_data_prof' : all_data_prof, 'total_amount' : total_amount}
    form = calculate_paymentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            purchase_data.total_amount = form.cleaned_data.get('total_amount')
            purchase_data.payment_method = form.cleaned_data.get('payment_method')
            purchase_data.save()
            messages.error(request, 'Prescription purchased successfully')
            return redirect('view_bought_prescriptions', primary_key)
        else:
            messages.error(request, 'Please Complete the form and follow the given format')
            return render(request, 'calculate_payment.html', context)
    else:
        return render(request, 'calculate_payment.html', context)



def view_bought_prescriptions(request, primary_key):
    purchase_data = prescription_purchase.objects.filter(patient_id = primary_key)
    a = profile.objects.get(pk = primary_key)
    pname = a.fullname
    context = {'purchase_data' : purchase_data, 'primary_key' : primary_key,'pname':pname }
    return render(request, 'view_bought_prescriptions.html', context )

def view_bought_prescriptions_filter(request, primary_key,order):
    purchase_data = prescription_purchase.objects.filter(patient_id = primary_key).order_by(order)
    a = profile.objects.get(pk = primary_key)
    pname = a.fullname
    context = {'purchase_data' : purchase_data, 'primary_key' : primary_key,'pname':pname }
    return render(request, 'view_bought_prescriptions_filter.html', context )

def view_bought_prescriptions_search(request, primary_key):
    purchase_data = prescription_purchase.objects.filter(patient_id = primary_key)
    a = profile.objects.get(pk = primary_key)
    pname = a.fullname

    list1 = []
    list2 = []
    list3 = []
    for i in purchase_data:
        list1.append(i.item_id.id)
    items = item_inventory.objects.filter(pk__in = list1)
    if request.method=='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            if name == "" and code =="":
                return redirect('view_bought_prescriptions', primary_key)
            elif name != "":
                items = items.filter(itemname__contains = name)
                for i in items:
                    list2.append(i.id)
                purchase_data = purchase_data.filter(item_id__in = list2)

                if code !="":
                    items = items.filter(barcode__contains = code)
                    for i in items:
                        list3.append(i.id)
                    purchase_data = purchase_data.filter(item_id__in = list3)
                    context = {'purchase_data' : purchase_data, 'primary_key' : primary_key,'pname':pname }
                else:
                    context = {'purchase_data' : purchase_data, 'primary_key' : primary_key,'pname':pname }
            elif code!="":
                items = items.filter(barcode__contains = code)
                for i in items:
                    list3.append(i.id)
                purchase_data = purchase_data.filter(item_id__in = list3)
                context = {'purchase_data' : purchase_data, 'primary_key' : primary_key,'pname':pname }
            else:
                context = {'purchase_data' : purchase_data, 'primary_key' : primary_key,'pname':pname }
        else:
            context = {'purchase_data' : purchase_data, 'primary_key' : primary_key,'pname':pname }
        return render(request, 'view_bought_prescriptions_search.html', context )
    else:
        context = {'purchase_data' : purchase_data, 'primary_key' : primary_key,'pname':pname }
        return render(request, 'view_bought_prescriptions_search.html', context )

    


def teeth_chart(request, primary_key):
    procedures_data = procedures_done.objects.filter(patient_id = primary_key)
    procedures_data = list(procedures_data)
    teeth_data = teeths.objects.get(patient_id = primary_key)
    teeth = teeths.objects.get(patient_id = primary_key)
    all_data_prof = profile.objects.get(pk = primary_key)
    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth' : teeth, 'procedures_data':procedures_data,'teeth_data':teeth_data}
    return render(request, 'teeth_chart.html', context)


def change_teeth(request, primary_key):
    teeth_data = teeths.objects.get(patient_id = primary_key)
    if teeth_data.teeth_type == 'Adult':
        teeth_data.teeth_type = 'Baby'
    else:
        teeth_data.teeth_type = 'Adult'
    teeth_data.save()
    messages.error(request, 'Teeth Type successfully Changed')
    return redirect('teeth_chart', primary_key)


def teeth_status(request, primary_key, teeth_pos):
    all_data_prof = profile.objects.get(pk = primary_key)
    procedure_data = procedures_done.objects.filter(teeth_position = teeth_pos)
    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth_pos' :teeth_pos, 'procedure_data' : procedure_data}
    return render(request, 'teeth_status.html', context)



def teeth_history(request, primary_key, teeth_pos):
    all_data_prof = profile.objects.get(pk = primary_key)
    procedure_data = procedures_done.objects.filter(teeth_position = teeth_pos)
    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth_pos' :teeth_pos, 'procedure_data' : procedure_data}
    return render(request, 'teeth_history.html', context)

def teeth_history_filter(request, primary_key, teeth_pos,order):
    all_data_prof = profile.objects.get(pk = primary_key)
    procedure_data = procedures_done.objects.filter(teeth_position = teeth_pos).order_by(order)
    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth_pos' :teeth_pos, 'procedure_data' : procedure_data}
    return render(request, 'teeth_history_filter.html', context)

def teeth_history_search(request, primary_key, teeth_pos):
    list1 = []
    list2 = []
    all_data_prof = profile.objects.get(pk = primary_key)
    procedure_data = procedures_done.objects.filter(teeth_position = teeth_pos)
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            if name == "" and date =="":
                return redirect('teeth_history', primary_key, teeth_pos)
            elif name != "":
                procedure_data = procedure_data.filter(procedures_done__contains = name)
                if date!= "":
                    sched = available_schedules.objects.filter(date__contains = date)
                    for i in sched:
                        list1.append(i.id)
                    appointments = appointment_details.objects.filter(schedule_id__in = list1)
                    for i in appointments:
                        list2.append(i.id)
                    procedure_data = procedure_data.filter(appointment_id__in = list2)
                    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth_pos' :teeth_pos, 'procedure_data' : procedure_data}
                else:
                    context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth_pos' :teeth_pos, 'procedure_data' : procedure_data}
            elif date!= "":
                sched = available_schedules.objects.filter(date__contains = date)
                for i in sched:
                    list1.append(i.id)
                appointments = appointment_details.objects.filter(schedule_id__in = list1)
                for i in appointments:
                    list2.append(i.id)
                procedure_data = procedure_data.filter(appointment_id__in = list2)
                context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth_pos' :teeth_pos, 'procedure_data' : procedure_data}

            else:
                context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth_pos' :teeth_pos, 'procedure_data' : procedure_data}
            return render(request, 'teeth_history_search.html', context)
    else:
        context = {'primary_key' : primary_key, 'all_data_prof' : all_data_prof, 'teeth_pos' :teeth_pos, 'procedure_data' : procedure_data}
        return render(request, 'teeth_history_search.html', context)



def stock_out_option(request):
    return render(request, 'stock_out_option.html', {})



def view_stockout_presc(request):
    prescription_data = prescription_purchase.objects.all()
    context = {'prescription_data' : prescription_data}
    return render(request, 'view_stockout_presc.html', context)

def view_stockout_presc_filter(request,order):
    prescription_data = prescription_purchase.objects.all().order_by(order)
    context = {'prescription_data' : prescription_data}
    return render(request, 'view_stockout_presc_filter.html', context)

def view_stockout_presc_search(request):
    prescription_data = prescription_purchase.objects.all()
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            med = form.cleaned_data['med']
            code = form.cleaned_data['code']
            loc = form.cleaned_data['loc']
            cat = form.cleaned_data['cat']
            if date == "" and med =="" and name =="" and code =="" and loc =="" and cat =="":
                return redirect('view_stockout_presc')
            else:
                context = get_context(name, date, med, code,loc,cat)
                return render(request, 'view_stockout_presc_search.html', context)
                
        else:
            context = {'prescription_data' : prescription_data}
            return render(request, 'view_stockout_presc_search.html', context)
    else:
        context = {'prescription_data' : prescription_data}
        return render(request, 'view_stockout_presc_search.html', context)





def view_stockout_tools(request):
    tools_data = tools_items_used.objects.all()
    context = {'tools_data' : tools_data}
    return render(request, 'view_stockout_tools.html', context)


def view_stockout_tools_filter(request,order):
    tools_data = tools_items_used.objects.all().order_by(order)
    context = {'tools_data' : tools_data}
    return render(request, 'view_stockout_tools_filter.html', context)

def view_stockout_tools_search(request):
    ids = []
    ids2 = []
    ids3 = []
    ids4 = []
    ids5 = []
    ids6 = []
    tools_data = tools_items_used.objects.all()
    if request.method=='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            code = form.cleaned_data['code']
            loc = form.cleaned_data['loc']
            cat = form.cleaned_data['cat']
            if name == "" and date =="" and code =="" and loc =="" and cat == "":
                return redirect('view_stockout_tools')
            elif name != '':
                items = item_inventory.objects.filter(itemname__contains =name)
                for i in items:
                    ids.append(i.id)
                tools_data = tools_data.filter(item_id__in = ids)
                if date!= '':
                    dates = available_schedules.objects.filter(date__contains = date)
                    for i in dates:
                        ids2.append(i)
                    datesfromapp = appointment_details.objects.filter(schedule_id__in = ids2)
                    for i in datesfromapp:
                        ids3.append(i)
                    tools_data = tools_data.filter(appointment_id__in = ids3)
                    context = {'tools_data' : tools_data}
                    if code != "":
                        items = item_inventory.objects.filter(barcode__contains =code)
                        for i in items:
                            ids4.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids4)
                        context = {'tools_data' : tools_data}
                        if loc !="":
                            items = item_inventory.objects.filter(location__contains = loc)
                            for i in items:
                                ids5.append(i.id)
                            tools_data = tools_data.filter(item_id__in = ids5)
                            context = {'tools_data' : tools_data}
                            if cat !="":
                                items = item_inventory.objects.filter(itemcategory__contains = cat)
                                for i in items:
                                    ids6.append(i.id)
                                tools_data = tools_data.filter(item_id__in = ids6)
                                context = {'tools_data' : tools_data}    
                                return render(request, 'view_stockout_tools_search.html', context)
                            else:
                                context = {'tools_data' : tools_data}
                                return render(request, 'view_stockout_tools_search.html', context)
                        elif cat != "":
                            items = item_inventory.objects.filter(itemcategory__contains = cat)
                            for i in items:
                                ids6.append(i.id)
                            tools_data = tools_data.filter(item_id__in = ids6)
                            context = {'tools_data' : tools_data}  
                            return render(request, 'view_stockout_tools_search.html', context)
                        else:
                            context = {'tools_data' : tools_data}
                            return render(request, 'view_stockout_tools_search.html', context)
                    elif loc !="":
                        items = item_inventory.objects.filter(location__contains = loc)
                        for i in items:
                            ids5.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids5)
                        context = {'tools_data' : tools_data}
                        if cat !="":
                            items = item_inventory.objects.filter(itemcategory__contains = cat)
                            for i in items:
                                ids6.append(i.id)
                            tools_data = tools_data.filter(item_id__in = ids6)
                            context = {'tools_data' : tools_data}    
                            return render(request, 'view_stockout_tools_search.html', context)
                        else:
                            context = {'tools_data' : tools_data}
                            return render(request, 'view_stockout_tools_search.html', context)
                    elif cat != "":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            ids6.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids6)
                        context = {'tools_data' : tools_data}  
                        return render(request, 'view_stockout_tools_search.html', context)
                    else:
                        context = {'tools_data' : tools_data}
                        return render(request, 'view_stockout_tools_search.html', context)
                elif code != "":
                    items = item_inventory.objects.filter(barcode__contains =code)
                    for i in items:
                        ids4.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids4)
                    context = {'tools_data' : tools_data}
                    if loc !="":
                        items = item_inventory.objects.filter(location__contains = loc)
                        for i in items:
                            ids5.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids5)
                        context = {'tools_data' : tools_data}
                        if cat !="":
                            items = item_inventory.objects.filter(itemcategory__contains = cat)
                            for i in items:
                                ids6.append(i.id)
                            tools_data = tools_data.filter(item_id__in = ids6)
                            context = {'tools_data' : tools_data}    
                            return render(request, 'view_stockout_tools_search.html', context)
                        else:
                            context = {'tools_data' : tools_data}
                            return render(request, 'view_stockout_tools_search.html', context)
                    elif cat != "":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            ids6.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids6)
                        context = {'tools_data' : tools_data}  
                        return render(request, 'view_stockout_tools_search.html', context)
                    else:
                        context = {'tools_data' : tools_data}
                        return render(request, 'view_stockout_tools_search.html', context)
                elif loc !="":
                    items = item_inventory.objects.filter(location__contains = loc)
                    for i in items:
                        ids5.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids5)
                    context = {'tools_data' : tools_data}
                    if cat !="":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            ids6.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids6)
                        context = {'tools_data' : tools_data}    
                        return render(request, 'view_stockout_tools_search.html', context)
                    else:
                        context = {'tools_data' : tools_data}
                        return render(request, 'view_stockout_tools_search.html', context)
                elif cat != "":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        ids6.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids6)
                    context = {'tools_data' : tools_data}  
                    return render(request, 'view_stockout_tools_search.html', context)
                else:
                    context = {'tools_data' : tools_data}
                    return render(request, 'view_stockout_tools_search.html', context)
            elif date!= '':
                dates = available_schedules.objects.filter(date__contains = date)
                for i in dates:
                    ids2.append(i)
                datesfromapp = appointment_details.objects.filter(schedule_id__in = ids2)
                for i in datesfromapp:
                    ids3.append(i)
                tools_data = tools_data.filter(appointment_id__in = ids3)
                context = {'tools_data' : tools_data}
                if code != "":
                    items = item_inventory.objects.filter(barcode__contains =code)
                    for i in items:
                        ids4.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids4)
                    context = {'tools_data' : tools_data}
                    if loc !="":
                        items = item_inventory.objects.filter(location__contains = loc)
                        for i in items:
                            ids5.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids5)
                        context = {'tools_data' : tools_data}
                        if cat !="":
                            items = item_inventory.objects.filter(itemcategory__contains = cat)
                            for i in items:
                                ids6.append(i.id)
                            tools_data = tools_data.filter(item_id__in = ids6)
                            context = {'tools_data' : tools_data}    
                            return render(request, 'view_stockout_tools_search.html', context)
                        else:
                            context = {'tools_data' : tools_data}
                            return render(request, 'view_stockout_tools_search.html', context)
                    elif cat != "":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            ids6.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids6)
                        context = {'tools_data' : tools_data}  
                        return render(request, 'view_stockout_tools_search.html', context)
                    else:
                        context = {'tools_data' : tools_data}
                        return render(request, 'view_stockout_tools_search.html', context)
                elif loc !="":
                    items = item_inventory.objects.filter(location__contains = loc)
                    for i in items:
                        ids5.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids5)
                    context = {'tools_data' : tools_data}
                    if cat !="":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            ids6.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids6)
                        context = {'tools_data' : tools_data}    
                        return render(request, 'view_stockout_tools_search.html', context)
                    else:
                        context = {'tools_data' : tools_data}
                        return render(request, 'view_stockout_tools_search.html', context)
                elif cat != "":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        ids6.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids6)
                    context = {'tools_data' : tools_data}  
                    return render(request, 'view_stockout_tools_search.html', context)
                else:
                    context = {'tools_data' : tools_data}
                    return render(request, 'view_stockout_tools_search.html', context)
            elif code != "":
                items = item_inventory.objects.filter(barcode__contains =code)
                for i in items:
                    ids4.append(i.id)
                tools_data = tools_data.filter(item_id__in = ids4)
                context = {'tools_data' : tools_data}
                if loc !="":
                    items = item_inventory.objects.filter(location__contains = loc)
                    for i in items:
                        ids5.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids5)
                    context = {'tools_data' : tools_data}
                    if cat !="":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            ids6.append(i.id)
                        tools_data = tools_data.filter(item_id__in = ids6)
                        context = {'tools_data' : tools_data}    
                        return render(request, 'view_stockout_tools_search.html', context)
                    else:
                        context = {'tools_data' : tools_data}
                        return render(request, 'view_stockout_tools_search.html', context)
                elif cat != "":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        ids6.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids6)
                    context = {'tools_data' : tools_data}  
                    return render(request, 'view_stockout_tools_search.html', context)
                else:
                    context = {'tools_data' : tools_data}
                    return render(request, 'view_stockout_tools_search.html', context)
            elif loc !="":
                items = item_inventory.objects.filter(location__contains = loc)
                for i in items:
                    ids5.append(i.id)
                tools_data = tools_data.filter(item_id__in = ids5)
                context = {'tools_data' : tools_data}
                if cat !="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        ids6.append(i.id)
                    tools_data = tools_data.filter(item_id__in = ids6)
                    context = {'tools_data' : tools_data}    
                    return render(request, 'view_stockout_tools_search.html', context)
                else:
                    context = {'tools_data' : tools_data}
                    return render(request, 'view_stockout_tools_search.html', context)
            elif cat != "":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    ids6.append(i.id)
                tools_data = tools_data.filter(item_id__in = ids6)
                context = {'tools_data' : tools_data}  
                return render(request, 'view_stockout_tools_search.html', context)
            else:
                context = {'tools_data' : tools_data}
                return render(request, 'view_stockout_tools_search.html', context)
        else:
            context = {'tools_data' : tools_data}
            return render(request, 'view_stockout_tools_search.html', context)
    else:
        context = {'tools_data' : tools_data}
        return render(request, 'view_stockout_tools_search.html', context)







def expense_options(request):
    return render(request, 'expense_options.html',{})



def income_options(request):
    return render(request, 'income_options.html',{})


@login_required
def view_appointment_income(request):
    payment_details = payment.objects.all()
    context = {'payment_details' : payment_details}
    return render(request, 'view_appointment_income.html',context)

def view_appointment_income_filter(request,order):
    payment_details = payment.objects.all().order_by(order)
    context = {'payment_details' : payment_details}
    return render(request, 'view_appointment_income_filter.html',context)

def view_appointment_income_search(request):
    list1 = []
    llist1 = []
    list2 = []
    llist2 = []
    list3 = []
    llist3 = []
    payment_details = payment.objects.all()
    if request.method =='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            name = form.cleaned_data['name']
            service = form.cleaned_data['service']
            doc = form.cleaned_data['doc']
            appointments = appointment_details.objects.all()
            if date =="" and name=="" and service =="" and doc =="":
                return redirect('view_appointment_income')
            elif date != "":
                payment_details = payment_details.filter(date_paid__contains = date)
                if name != "":
                    prof = profile.objects.filter(fullname__contains = name)
                    for i in prof:
                        list1.append(i.id)
                    appointments = appointments.filter(patient_id__in = list1)
                    for i in appointments:
                        llist1.append(i.id)
                    payment_details = payment_details.filter(appointment_id__in = llist1)

                    if service != "":
                        service = available_services.objects.filter(service_type__contains= service)
                        for i in service:
                            list2.append(i.id)
                        appointments = appointments.filter(service_id__in =list2)
                        for i in appointments:
                            llist2.append(i.id)
                        payment_details = payment_details.filter(appointment_id__in = llist2)

                        if doc != "":
                            sched = available_schedules.objects.filter(doctor_lastname__contains = doc)
                            for i in sched:
                                list3.append(i.id)
                            appointments = appointments.filter(schedule_id__in = list3)
                            for i in appointments:
                                llist3.append(i.id)
                            payment_details = payment_details.filter(appointment_id__in = llist3)
                            context = {'payment_details' : payment_details}

                        else:
                            context = {'payment_details' : payment_details}

                    elif doc != "":
                        sched = available_schedules.objects.filter(doctor_lastname__contains = doc)
                        for i in sched:
                            list3.append(i.id)
                        appointments = appointments.filter(schedule_id__in = list3)
                        for i in appointments:
                            llist3.append(i.id)
                        payment_details = payment_details.filter(appointment_id__in = llist3)
                        context = {'payment_details' : payment_details}

                    else:
                        context = {'payment_details' : payment_details}

                elif service != "":
                    service = available_services.objects.filter(service_type__contains= service)
                    for i in service:
                        list2.append(i.id)
                    appointments = appointments.filter(service_id__in = list2)
                    for i in appointments:
                        llist2.append(i.id)
                    payment_details = payment_details.filter(appointment_id__in = llist2)

                    if doc != "":
                        sched = available_schedules.objects.filter(doctor_lastname__contains = doc)
                        for i in sched:
                            list3.append(i.id)
                        appointments = appointments.filter(schedule_id__in = list3)
                        for i in appointments:
                            llist3.append(i.id)
                        payment_details = payment_details.filter(appointment_id__in = llist3)
                        context = {'payment_details' : payment_details}

                    else:
                        context = {'payment_details' : payment_details}

                elif doc != "":
                    sched = available_schedules.objects.filter(doctor_lastname__contains = doc)
                    for i in sched:
                        list3.append(i.id)
                    appointments = appointments.filter(schedule_id__in = list3)
                    for i in appointments:
                        llist3.append(i.id)
                    payment_details = payment_details.filter(appointment_id__in = llist3)
                    context = {'payment_details' : payment_details}

                else:
                    context = {'payment_details' : payment_details}


            elif name != "":
                prof = profile.objects.filter(fullname__contains = name)
                for i in prof:
                    list1.append(i.id)
                appointments = appointments.filter(patient_id__in = list1)
                for i in appointments:
                    llist1.append(i.id)
                payment_details = payment_details.filter(appointment_id__in = llist1)

                if service !="":
                    service = available_services.objects.filter(service_type__contains= service)
                    for i in service:
                        list2.append(i.id)
                    appointments = appointments.filter(service_id__in = list2)
                    for i in appointments:
                        llist2.append(i.id)
                    payment_details = payment_details.filter(appointment_id__in = llist2)

                    if doc != "":
                        sched = available_schedules.objects.filter(doctor_lastname__contains = doc)
                        for i in sched:
                            list3.append(i.id)
                        appointments = appointments.filter(schedule_id__in = list3)
                        for i in appointments:
                            llist3.append(i.id)
                        payment_details = payment_details.filter(appointment_id__in = llist3)
                        context = {'payment_details' : payment_details}

                    else:
                        context = {'payment_details' : payment_details}

                elif doc != "":
                    sched = available_schedules.objects.filter(doctor_lastname__contains = doc)
                    for i in sched:
                        list3.append(i.id)
                    appointments = appointments.filter(schedule_id__in = list3)
                    for i in appointments:
                        llist3.append(i.id)
                    payment_details = payment_details.filter(appointment_id__in = llist3)
                    context = {'payment_details' : payment_details}

                else:
                    context = {'payment_details' : payment_details}

            elif service !="":
                service = available_services.objects.filter(service_type__contains= service)
                for i in service:
                    list2.append(i.id)
                appointments = appointments.filter(service_id__in =list2)
                for i in appointments:
                    llist2.append(i.id)
                payment_details = payment_details.filter(appointment_id__in = llist2)

                if doc !="":
                    sched = available_schedules.objects.filter(doctor_lastname__contains = doc)
                    for i in sched:
                        list3.append(i.id)
                    appointments = appointments.filter(schedule_id__in = list3)
                    for i in appointments:
                        llist3.append(i.id)
                    payment_details = payment_details.filter(appointment_id__in = llist3)
                    context = {'payment_details' : payment_details}

                else:
                    context = {'payment_details' : payment_details}
            elif doc != "":
                sched = available_schedules.objects.filter(doctor_lastname__contains = doc)
                for i in sched:
                    list3.append(i.id)
                appointments = appointments.filter(schedule_id__in = list3)
                for i in appointments:
                    llist3.append(i.id)
                payment_details = payment_details.filter(appointment_id__in = llist3)
                context = {'payment_details' : payment_details}

            else:
                context = {'payment_details' : payment_details}

            return render(request, 'view_appointment_income_search.html',context)

        else:
            context = {'payment_details' : payment_details}
            return render(request, 'view_appointment_income_search.html',context)
    else:
        context = {'payment_details' : payment_details}
        return render(request, 'view_appointment_income_search.html',context)

@login_required
def view_presc_income(request):
    presc_details = prescription_purchase.objects.all()
    context = {'presc_details' : presc_details}
    return render(request, 'view_presc_income.html',context)

def view_presc_income_filter(request,order):
    presc_details = prescription_purchase.objects.all().order_by(order)
    context = {'presc_details' : presc_details}
    return render(request, 'view_presc_income_filter.html',context)

def view_presc_income_search(request):
    presc_details = prescription_purchase.objects.all()
    listid = []
    listid2 = []
    listid3 = []
    if request.method =='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            name = form.cleaned_data['name']
            med = form.cleaned_data['med']
            code = form.cleaned_data['code']
            if date == "" and name =="" and med =="" and code =="":
                return redirect('view_presc_income')

            elif date != "":
                presc_details = presc_details.filter(purchase_date__contains = date)
                if name !="":
                    pat = profile.objects.filter(fullname__contains = name)
                    for i in pat:
                        listid.append(i.id)
                    presc_details = presc_details.filter(patient_id__in = listid)
                    if med != "":
                        item = item_inventory.objects.filter(itemname__contains = med)
                        for i in item:
                            listid2.append(i.id)
                        presc_details = presc_details.filter(item_id__in = listid2)
                        if code !="":
                            item = item_inventory.objects.filter(barcode__contains = code)
                            for i in item:
                                listid3.append(i.id)
                            presc_details = presc_details.filter(item_id__in = listid3)
                            context = {'presc_details' : presc_details}
                        else:
                            context = {'presc_details' : presc_details}
                    elif code !="":
                        item = item_inventory.objects.filter(barcode__contains = code)
                        for i in item:
                            listid3.append(i.id)
                        presc_details = presc_details.filter(item_id__in = listid3)
                        context = {'presc_details' : presc_details}

                    else:
                        context = {'presc_details' : presc_details}
                elif med !="":
                    item = item_inventory.objects.filter(itemname__contains = med)
                    for i in item:
                        listid2.append(i.id)
                    presc_details = presc_details.filter(item_id__in = listid2)
                    if code !="":
                        item = item_inventory.objects.filter(barcode__contains = code)
                        for i in item:
                            listid3.append(i.id)
                        presc_details = presc_details.filter(item_id__in = listid3)
                        context = {'presc_details' : presc_details}
                    else:
                        context = {'presc_details' : presc_details}


                elif code !="":
                    item = item_inventory.objects.filter(barcode__contains = code)
                    for i in item:
                        listid3.append(i.id)
                    presc_details = presc_details.filter(item_id__in = listid3)
                    context = {'presc_details' : presc_details}
                else:
                    context = {'presc_details' : presc_details}


            elif name !="":
                pat = profile.objects.filter(fullname__contains = name)
                for i in pat:
                    listid.append(i.id)
                presc_details = presc_details.filter(patient_id__in = listid)
                if med !="":
                    item = item_inventory.objects.filter(itemname__contains = med)
                    for i in item:
                        listid2.append(i.id)
                    presc_details = presc_details.filter(item_id__in = listid2)
                    if code !="":
                        item = item_inventory.objects.filter(barcode__contains = code)
                        for i in item:
                            listid3.append(i.id)
                        presc_details = presc_details.filter(item_id__in = listid3)
                        context = {'presc_details' : presc_details}
                    else:
                        context = {'presc_details' : presc_details}

                elif code !="":
                    item = item_inventory.objects.filter(barcode__contains = code)
                    for i in item:
                        listid3.append(i.id)
                    presc_details = presc_details.filter(item_id__in = listid3)
                    context = {'presc_details' : presc_details}        
                else:
                    context = {'presc_details' : presc_details}

            elif med !="":
                item = item_inventory.objects.filter(itemname__contains = med)
                for i in item:
                    listid2.append(i.id)
                presc_details = presc_details.filter(item_id__in = listid2)
                if code !="":
                    item = item_inventory.objects.filter(barcode__contains = code)
                    for i in item:
                        listid3.append(i.id)
                    presc_details = presc_details.filter(item_id__in = listid3)
                    context = {'presc_details' : presc_details}
                else:
                    context = {'presc_details' : presc_details}
            elif code !="":
                item = item_inventory.objects.filter(barcode__contains = code)
                for i in item:
                    listid3.append(i.id)
                presc_details = presc_details.filter(item_id__in = listid3)
                context = {'presc_details' : presc_details}        
            else:
                context = {'presc_details' : presc_details}

        else:
            context = {'presc_details' : presc_details}

        return render(request, 'view_presc_income_search.html',context)
    else:
        context = {'presc_details' : presc_details}
        return render(request, 'view_presc_income_search.html',context)



@login_required
def view_salary_expense(request):
    salary_details = salary_info.objects.all()
    context = {'salary_details' : salary_details}
    return render(request, 'view_salary_expense.html',context)

def view_salary_expense_filter(request,order):
    salary_details = salary_info.objects.all().order_by(order)
    context = {'salary_details' : salary_details}
    return render(request, 'view_salary_expense_filter.html',context)


def view_salary_expense_search(request):
    salary_details = salary_info.objects.all()
    if request.method =='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            if date!= "": 
                salary_details = salary_details.filter(date_given__contains = date)
                context = {'salary_details' : salary_details}
                return render(request,'view_salary_expense_search.html',context)
            elif date == "":
                return redirect('view_salary_expense')
            else:
                context = {'salary_details' : salary_details}
                return render(request,'view_salary.html',context)

        else:
            context = {'salary_details' : salary_details}
            return render(request,'view_salary_expense.html',context)
    else:
        context = {'salary_details' : salary_details}
        return render(request,'view_salary_expense_search.html',context)


def bills_options(request):
    return render(request, 'bills_options.html',{})
   

@login_required
def add_bills(request):
    name = []
    names = profile.objects.filter(profile_type = 'Employee')
    for i in names:
        name.append(i.fullname)

    context = {'name':name}
    if request.method=='POST':
        form = add_billsForm(request.POST or None)
        if form.is_valid():
            btype = form.cleaned_data.get("bill_type").lower()
            bmonth =  form.cleaned_data.get("bill_month")
            byear = form.cleaned_data.get("bill_year")
            some_bool=check_data(btype,bmonth,byear)
            if some_bool == True:
                form.save()
                messages.error(request, 'Bill expense successfully recorded')
                return redirect('view_bills')
            else:
                messages.error(request, 'Billing details already exist in the database')
                return render(request, 'add_bills.html',context)
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request, 'add_bills.html',context)
    else:
        return render(request, 'add_bills.html',context)

def check_data(btype,bmonth,byear):
    data = bills_details.objects.all()
    some_bool = True
    for i in data:
        if i.bill_type.lower() == btype and i.bill_month == bmonth and i.bill_year == byear:
            some_bool = False
        else:
            pass
    return some_bool


@login_required
def view_bills(request):
    bills_data = bills_details.objects.all()
    context = {'bills_data' : bills_data}
    return render(request, 'view_bills.html',context)  

def view_bills_filter(request,order):
    bills_data = bills_details.objects.all().order_by(order)
    context = {'bills_data' : bills_data}
    return render(request, 'view_bills_filter.html',context)  


def view_bills_search(request):
    bills_data = bills_details.objects.all()
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            date2 = form.cleaned_data['date2']
            name = form.cleaned_data['name']
            if date =="" and date2 =="" and name =="":
                return redirect('view_bills')
            if date!="":
                date = date.split('-')
                m = date[1]
                y = date[0]
                month = getmonth(m)
                y = str(y)
                month = str(month)
            if name != "":

                bills_data = bills_data.filter(bill_type__contains = name)
                if date != "":
                    bills_data = bills_data.filter(bill_year__contains = y)
                    bills_data = bills_data.filter(bill_month__contains = month)
                    if date2 != "":
                        bills_data = bills_data.filter(date_paid__contains = date2)
                        context = {'bills_data' : bills_data }
                        return render(request, 'view_bills_search.html',context)
                    else:
                        context = {'bills_data' : bills_data }
                        return render(request, 'view_bills_search.html',context)
                elif date2 != "":
                    bills_data = bills_data.filter(date_paid__contains = date2)
                    context = {'bills_data' : bills_data }
                    return render(request, 'view_bills_search.html',context)

                else:
                    context = {'bills_data' : bills_data }
                    return render(request, 'view_bills_search.html',context)
            elif date != "":
                bills_data = bills_data.filter(bill_year__contains = y)
                bills_data = bills_data.filter(bill_month__contains = month)
                if date2 != "":
                    bills_data = bills_data.filter(date_paid__contains = date2)
                    context = {'bills_data' : bills_data }
                    return render(request, 'view_bills_search.html',context)
                else:
                    context = {'bills_data' : bills_data }
                    return render(request, 'view_bills_search.html',context)
            elif date2 != "":
                bills_data = bills_data.filter(date_paid__contains = date2)
                context = {'bills_data' : bills_data }
                return render(request, 'view_bills_search.html',context)
            else:
                context = {'bills_data' : bills_data }
                return render(request, 'view_bills_search.html',context)
            
        else:
            context = {'bills_data' : bills_data }
            return render(request, 'view_bills_search.html',context) 
    else:
        context = {'bills_data' : bills_data }
        return render(request, 'view_bills_search.html',context) 


def getmonth(m):
    m = str(m)
    if m == '01':
        return 'January'
    elif m == '02':
        return 'Febuary'
    elif m == '03':
        return 'March'
    elif m == '04':
        return 'April'
    elif m == '05':
        return 'May'
    elif m == '06':
        return 'June'
    elif m == '07':
        return 'July'
    elif m == '08':
        return 'August'
    elif m == '09':
        return 'September'
    elif m == '10':
        return 'October'
    elif m == '11':
        return 'November'
    elif m == '12':
        return 'December'
    else:
        return ""

                


def edit_billForm(request, primary_key):
    name = []
    names = profile.objects.filter(profile_type = 'Employee')
    for i in names:
        name.append(i.fullname)
    bills_data = bills_details.objects.get(pk = primary_key)
    context = {'bills_data' : bills_data,'name':name}
    if request.method == 'POST':
        form = edit_billsForm(request.POST or None)
        if form.is_valid():
            bills_data.bill_type = form.cleaned_data.get('bill_type')
            btype = form.cleaned_data.get('bill_type')
            bills_data.bill_month = form.cleaned_data.get('bill_month')
            bmonth = form.cleaned_data.get('bill_month')
            bills_data.bill_year = form.cleaned_data.get('bill_year')
            byear = form.cleaned_data.get('bill_year')
            bills_data.total_amount = form.cleaned_data.get('total_amount')
            bills_data.paid_by = form.cleaned_data.get('paid_by')
            bills_data.date_paid = form.cleaned_data.get('date_paid')
            some_bool = check_bill_error(primary_key, btype, bmonth, byear)
            if some_bool == True:
                bills_data.save()
                messages.error(request, 'Bill expense successfully edited')
                return redirect('view_bills')
            else:
                messages.error(request, 'Billing data already exists in the database')
                return render(request, 'edit_billForm.html',context)

        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request, 'edit_billForm.html',context)
    else:
        return render(request, 'edit_billForm.html',context)       

def check_bill_error(primary_key, btype, bmonth, byear):
    alldata = bills_details.objects.exclude(pk = primary_key)
    some_bool = True
    for things in alldata:
        if things.bill_type.lower() == btype.lower() and things.bill_month == bmonth and things.bill_year == byear:
            some_bool = False
        else:
            pass
    return some_bool




def view_expired_items(request):
    #EXPIRY CHECK
    item_deets = item_inventory.objects.all()
    for things in item_deets:
        if things.expiry_date != None:
            if things.expiry_date < date.today():
                item_data = item_inventory.objects.get(pk = things.id)
                item_data.expiry_status = 'Expired'
                item_data.save()
        elif things.expiry_date == None:
            item_data = item_inventory.objects.get(pk = things.id)
            item_data.expiry_status = 'Item does not expire'
            item_data.save()

    all_data_inventory = item_inventory.objects.filter(expiry_status = 'Expired')
    context = {'all_data_inventory':all_data_inventory}
    return render(request, 'view_expired_items.html',context)  

def view_expired_items_filter(request,order):
    all_data_inventory = item_inventory.objects.filter(expiry_status = 'Expired').order_by(order)
    context = {'all_data_inventory':all_data_inventory}
    return render(request, 'view_expired_items_filter.html',context)  

def view_expired_items_search(request):
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            date = form.cleaned_data['date']
            loc = form.cleaned_data['loc']
            name = form.cleaned_data['name']
            cat = form.cleaned_data['cat']
            code = form.cleaned_data['code']
            all_data_inventory = item_inventory.objects.all()
            if date == "" and loc == "" and name == "" and cat == "" and code =="":
                return redirect('view_expired_items')
            else:
                context = filterloop3(name,date,loc,cat,code)
            return render(request,'view_expired_items_search.html',context)
        else:
            return redirect('view_expired_items')
    else:
        all_data_inventory = item_inventory.objects.filter(expiry_status = 'Expired')
        context = {'all_data_inventory':all_data_inventory}
        return render(request, 'view_expired_items_search.html',context)






def stock_in_options(request):
    return render(request,'stock_in_options.html',{}) 



def add_nonperishableList(request):
    items_data = item_inventory.objects.filter(expiry_date = None)
    context = {'items_data' : items_data}
    return render(request,'add_nonperishableList.html',context) 

def add_nonperishableList_search(request):
    items_data = item_inventory.objects.filter(expiry_date = None)
    if request.method == 'POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            code = form.cleaned_data['code']
            loc = form.cleaned_data['loc']
            name = form.cleaned_data['name']
            cat = form.cleaned_data['cat']
#            exp = form.cleaned_data['exp']
            if code == "" and loc == "" and name == "" and cat == "":
                return redirect('add_nonperishableList')
            else:
                context = filterloop5(name,code,loc,cat)
                return render(request,'add_nonperishableList_search.html',context)
        else:
            context = {'items_data' : items_data}
            return render(request,'add_nonperishableList_search.html',context) 


    


            

def add_nonperishableList_filter(request, order):
    items_data = item_inventory.objects.filter(expiry_date = None).order_by(order)
    context = {'items_data' : items_data}
    return render(request,'add_nonperishableList_filter.html',context) 



def add_perishableList(request,itemname ,barcode,itemcategory,location,item_fee, quantity, units,expiry_date):
    item_data = item_inventory.objects.last()
    some_id = int(item_data.id) 
    items_data = item_inventory.objects.filter(expiry_date__isnull = False)
    context = {'itemname' : itemname, 'some_id' : some_id, 'quantity': quantity, 'units' : units,
    'barcode':barcode,'itemcategory':itemcategory,'location':location,'item_fee':item_fee,  
    'expiry_date':expiry_date}
    if request.method == 'POST':
        form = add_perishableForm(request.POST or None)
        form2 = add_inventoryForm(request.POST or None)
        if form.is_valid() and form2.is_valid():
            form.save()
            some_bool = check_stockin()
            if some_bool == True:
                form2.save()
                messages.error(request, 'Item details added successfully')
                return redirect('view_inventory')
            else:
                messages.error(request, 'Please supply every information and follow the given format')
                return render(request,'add_perishableList.html',context)

        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request,'add_perishableList.html',context) 
    else:        
        return render(request,'add_perishableList.html',context)  

def check_stockin():
    data = stock_in.objects.last()
    if data.manufacturer == None or data.purchase_date == None or data.total_payment == None or data.quantity_added == 0:
        data.delete()
        return False
    else:
        return True

def add_inventory2(request):
#    context = {'itemname' : itemname, 'quantity' : quantity}
    if request.method == 'POST':
        form = add_inventoryForm(request.POST or None)
        if form.is_valid():
            itemname = form.cleaned_data.get('itemname')
            barcode = form.cleaned_data.get('barcode')
            itemcategory=form.cleaned_data.get('itemcategory')   
            location=form.cleaned_data.get('location')
            item_fee=form.cleaned_data.get('item_fee')
            quantity=form.cleaned_data.get('quantity') 
            units=form.cleaned_data.get('units')
            expiry_date=form.cleaned_data.get('expiry_date')
            if form.cleaned_data.get('quantity') <=0:
                messages.error(request, 'Invalid Quantity')
                return render(request,'add_inventory2.html', {})
            else:
                #form.save()
                some_bool = check_exp_date2(expiry_date)
                if some_bool == True:
                    return redirect('add_perishableList',itemname ,barcode,itemcategory,location,item_fee, quantity, units,expiry_date)
                else:
                    messages.error(request, 'Invalid Date')
                    return render(request,'add_inventory2.html', {})
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request,'add_inventory2.html', {})
    else:
        return render(request,'add_inventory2.html', {})

def check_exp_date2(expiry_date):
    if expiry_date == None:
        return False
        
    elif expiry_date < date.today():
        return False
    else:
        return True
            



def add_new_item(request, itemname ,barcode,itemcategory,location,item_fee, quantity, units):
    item_data = item_inventory.objects.last()
    some_id = int(item_data.id) 
    items_data = item_inventory.objects.filter(expiry_date__isnull = False)
    context = {'itemname' : itemname, 'some_id' : some_id, 'quantity': quantity, 'units' : units,
     'barcode':barcode,'itemcategory':itemcategory,'location':location,'item_fee':item_fee,}
    if request.method == 'POST':
        form = add_nonperishableForm(request.POST or None)
        form2 = add_inventoryForm2(request.POST or None)
        if form.is_valid() and form2.is_valid():
            form.save()
            some_bool = check_stockin()
            if some_bool == True:
                form2.save()
                messages.error(request, 'Item details added successfully')
                return redirect('view_inventory')
            else:
                messages.error(request, 'Please supply every information and follow the given format')
                return render(request,'add_new_item.html',context) 
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request,'add_new_item.html',context) 
    else:
        return render(request,'add_new_item.html',context) 


def add_inventory3(request):
#    context = {'itemname' : itemname, 'quantity' : quantity}
    if request.method == 'POST':
        form = add_inventoryForm2(request.POST or None)
        if form.is_valid():
            itemname = form.cleaned_data.get('itemname')
            barcode = form.cleaned_data.get('barcode')
            itemcategory=form.cleaned_data.get('itemcategory')   
            location=form.cleaned_data.get('location')
            item_fee=form.cleaned_data.get('item_fee')
            quantity=form.cleaned_data.get('quantity') 
            units=form.cleaned_data.get('units')
            expiry_date=form.cleaned_data.get('expiry_date')

            #quantity = form.cleaned_data.get('quantity')
            if quantity <= 0:
                messages.error(request, 'Invalid Quantity')
                return render(request,'add_inventory3.html', {})

            else:
                #form.save()
                #itemname = form.cleaned_data.get('itemname')
                #quantity = form.cleaned_data.get('quantity')
                #units = form.cleaned_data.get('units')
                return redirect('add_new_item',itemname ,barcode,itemcategory,location,item_fee, quantity, units)
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request,'add_inventory3.html', {})
    else:
        return render(request,'add_inventory3.html', {})

@login_required
def view_stockin_expense(request):
    stockin_data = stock_in.objects.all()
    context = {'stockin_data' : stockin_data}
    return render(request,'view_stockin_expense.html', context)


def view_stockin_expense_search(request):
    stockin_data = stock_in.objects.all()
    listid = []
    if request.method=='POST':
        form = searchForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            code = form.cleaned_data['code']
            if name =="" and date =="" and code =="":
                return redirect('view_stockin_expense')
            elif name != "":
                stockin_data = stockin_data.filter(item_name__contains = name)
                if date != "":
                    stockin_data = stockin_data.filter(purchase_date__contains = date)
                    if code != "":
                        items = item_inventory.objects.filter(barcode__contains = code)
                        for i in items:
                            listid.append(i.id)
                        stockin_data = stockin_data.filter(item_id__in = listid)
                        context = {'stockin_data' : stockin_data}
                    else:
                        context = {'stockin_data' : stockin_data}
                elif code != "":
                    items = item_inventory.objects.filter(barcode__contains = code)
                    for i in items:
                        listid.append(i.id)
                    stockin_data = stockin_data.filter(item_id__in = listid)
                    context = {'stockin_data' : stockin_data}
                else:
                    context = {'stockin_data' : stockin_data}
            elif date != "":
                stockin_data = stockin_data.filter(purchase_date__contains = date)
                if code != "":
                    items = item_inventory.objects.filter(barcode__contains = code)
                    for i in items:
                        listid.append(i.id)
                    stockin_data = stockin_data.filter(item_id__in = listid)
                    context = {'stockin_data' : stockin_data}
                else:
                    context = {'stockin_data' : stockin_data}
            elif code != "":
                    items = item_inventory.objects.filter(barcode__contains = code)
                    for i in items:
                        listid.append(i.id)
                    stockin_data = stockin_data.filter(item_id__in = listid)
                    context = {'stockin_data' : stockin_data}
            else:
                context = {'stockin_data' : stockin_data}

            return render(request,'view_stockin_expense_search.html', context)
        else:
            context = {'stockin_data' : stockin_data}
            return render(request,'view_stockin_expense_search.html', context)
    else:
        context = {'stockin_data' : stockin_data}
        return render(request,'view_stockin_expense_search.html', context)

'''
def view_stockin_expense_filter(request, query, order):
#    query = list(query)
#    some_list = []
#    for i in query:
#        some_list.append(i.id)
#    stockin_data = stock_in.objects.filter(pk__in = some_list)
    stockin_data = stock_in.objects.all()
    stockin_data = stockin_data.order_by(order)
    context = {'stockin_data' : stockin_data,'token':order}
    return render(request,'view_stockin_expense_filter.html', context)

'''

def view_stockin_expense_filter(request, query, order):
#    query = list(query)
#    some_list = []
#    for i in query:
#        some_list.append(i.id)
#    stockin_data = stock_in.objects.filter(pk__in = some_list)
    stockin_data = stock_in.objects.all()
    stockin_data = stockin_data.order_by(order)
    context = {'stockin_data' : stockin_data}
    return render(request,'view_stockin_expense_filter.html', context)


def add_nonperishable(request, primary_key):
    item_data = item_inventory.objects.get(pk = primary_key)
    units = item_data.units
    context = {'item_data' : item_data, 'units' : units}
    if request.method == 'POST':
        form = add_nonperishableForm(request.POST or None)
        if form.is_valid():
            if form.cleaned_data.get('quantity_added') <= 0:
                messages.error(request, 'Invalid Quantity')
                return render(request,'add_nonperishable.html',context)

            else:
                form.save()
                some_bool = check_stockin()
                if some_bool == True:
                    update_quantityStockin(primary_key)
                    messages.error(request, 'Item stock-in successfully')
                    return redirect('view_inventory') #NOT SURE WHERE TO REDIRECT
                else:
                    messages.error(request, 'Please supply every information and follow the given format')
                    return render(request,'add_nonperishable.html',context)
        else:
            messages.error(request, 'Please supply every information and follow the given format')
            return render(request, 'add_nonperishable.html', context) 
    else:
        return render(request, 'add_nonperishable.html', context)          


def update_quantityStockin(primary_key):
    item_data = item_inventory.objects.get(pk = primary_key)
    stockin_data = stock_in.objects.last()
    quantity_added = int(stockin_data.quantity_added)
    quantity_available = int(item_data.quantity)
    new_quantity = quantity_added + quantity_available
    item_data.quantity = new_quantity
    item_data.save()
    return 0



def filterloop(name,date,loc,cat,exp,code):
            all_data_inventory = item_inventory.objects.all()
            if name != "":
                all_data_inventory = all_data_inventory.filter(itemname__contains = name)
                if date != "":
                    all_data_inventory = all_data_inventory.filter(expiry_date__contains = date)
                    if loc != "":
                        all_data_inventory = all_data_inventory.filter(location__contains = loc)
                        if cat != "":
                            all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                            if exp != "":
                                all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                                if code != "":
                                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                    context = {'all_data_inventory' : all_data_inventory,}
                                    return context
                                else:
                                    context = {'all_data_inventory' : all_data_inventory,}
                                    return context
                            elif code != "":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                        elif exp == "":
                            all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                            if code != "":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                        elif code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context

                    elif cat != "":
                        all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                        if exp != "":
                            all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                            if code != "":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                        elif code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context

                    elif exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context


                elif loc != "": 
                    all_data_inventory = all_data_inventory.filter(location__contains = loc)
                    if cat != "":
                        all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                        if exp != "":
                            all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                            if code != "":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                        elif code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context

                    elif exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context

                elif cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context

                elif exp != "":
                    all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                    if code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                elif code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context

            elif date != "":
                all_data_inventory = all_data_inventory.filter(expiry_date__contains = date)
                if cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if loc != "": 
                        all_data_inventory = all_data_inventory.filter(location__contains = loc)
                        if exp != "":
                            all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                            if code != "":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                        elif code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                elif loc != "":
                    all_data_inventory = all_data_inventory.filter(location__contains = loc)
                    if exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                elif exp != "":
                    all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                    if code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                elif code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context

            elif loc != "":  
                all_data_inventory = all_data_inventory.filter(location__contains = loc)
                if cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context

                elif exp != "":
                    all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                    if code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                elif code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context

            elif cat != "":
                all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                if exp != "":
                    all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                    if code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                elif code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
            elif exp != "":
                all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                if code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
            elif code != "":
                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                context = {'all_data_inventory' : all_data_inventory,}
                return context
            else:
                context = {'all_data_inventory' : all_data_inventory,}
                return context

           




def filterloop2(name,date,loc,cat,exp,key, code): 
            all_data_inventory = item_inventory.objects.all()
            primary_key = key
            if name != "":
                all_data_inventory = all_data_inventory.filter(itemname__contains = name)
                if date != "":
                    all_data_inventory = all_data_inventory.filter(expiry_date__contains = date)
                    if loc != "":
                        all_data_inventory = all_data_inventory.filter(location__contains = loc)
                        if cat != "":
                            all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                            if exp != "":
                                all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                                if code !="":
                                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                    return context
                                else:
                                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                    return context
                            elif code!="":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                        elif exp == "":
                            all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                            if code !="":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                        elif code!="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context

                    elif cat != "":
                        all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                        if exp != "":
                            all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                            if code !="":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                        elif code!="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context

                    elif exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code !="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                    elif code!="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context


                elif loc != "": 
                    all_data_inventory = all_data_inventory.filter(location__contains = loc)
                    if cat != "":
                        all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                        if exp != "":
                            all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                            if code !="":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                        elif code!="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                    elif exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code !="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                    elif code!="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context

                elif cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code !="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                    elif code!="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context

                elif exp != "":
                    all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                    if code !="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                elif code!="":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context

            elif date != "":
                all_data_inventory = all_data_inventory.filter(expiry_date__contains = date)
                if cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if loc != "": 
                        all_data_inventory = all_data_inventory.filter(location__contains = loc)
                        if exp != "":
                            all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                            if code !="":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                                return context
                        elif code!="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                    elif exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code !="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                    elif code!="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context

                elif loc != "":
                    all_data_inventory = all_data_inventory.filter(location__contains = loc)
                    if exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code !="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                    elif code!="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context

                elif exp != "":
                    all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                    if code !="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                elif code!="":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context

            elif loc != "":  
                all_data_inventory = all_data_inventory.filter(location__contains = loc)
                if cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if exp != "":
                        all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                        if code !="":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                            return context
                    elif code!="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context

                elif exp != "":
                    all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                    if code !="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                elif code!="":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context

            elif cat != "":
                all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                if exp != "":
                    all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                    if code !="":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                        return context
                elif code!="":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context
            elif exp != "":
                all_data_inventory = all_data_inventory.filter(expiry_status__contains = exp)
                if code !="":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                    return context
            elif code!="":
                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                return context
            else:
                context = {'all_data_inventory' : all_data_inventory,'primary_key':primary_key}
                return context



def filterloop3(name,date,loc,cat,code):
            all_data_inventory = item_inventory.objects.filter(expiry_status = 'Expired')
            if name != "":
                all_data_inventory = all_data_inventory.filter(itemname__contains = name)
                if date != "":
                    all_data_inventory = all_data_inventory.filter(expiry_date__contains = date)
                    if loc != "":
                        all_data_inventory = all_data_inventory.filter(location__contains = loc)
                        if cat != "":
                            all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                            if code != "":
                                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context
                            else:
                                context = {'all_data_inventory' : all_data_inventory,}
                                return context

                        elif code != "":
                            ll_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context

                    elif cat != "":
                        all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context

                elif loc != "": 
                    all_data_inventory = all_data_inventory.filter(location__contains = loc)
                    if cat != "":
                        all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context

                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context

                elif cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context

                elif code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                
            elif date != "":
                all_data_inventory = all_data_inventory.filter(expiry_date__contains = date)
                if cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if loc != "": 
                        all_data_inventory = all_data_inventory.filter(location__contains = loc)
                        if code != "":
                            all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                        else:
                            context = {'all_data_inventory' : all_data_inventory,}
                            return context
                    elif code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context

                elif loc != "":
                    all_data_inventory = all_data_inventory.filter(location__contains = loc)
                    if code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                elif code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context


            elif loc != "":  
                all_data_inventory = all_data_inventory.filter(location__contains = loc)
                if cat != "":
                    all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                    if code != "":
                        all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                    else:
                        context = {'all_data_inventory' : all_data_inventory,}
                        return context
                elif code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context

            elif cat != "":
                all_data_inventory = all_data_inventory.filter(itemcategory__contains = cat)
                if code != "":
                    all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
                else:
                    context = {'all_data_inventory' : all_data_inventory,}
                    return context
            elif code != "":
                all_data_inventory = all_data_inventory.filter(barcode__contains = code)
                context = {'all_data_inventory' : all_data_inventory,}
                return context
            else:
                context = {'all_data_inventory' : all_data_inventory,}
                return context


def filterloop4(name,date,loc,cat,exp,key,code): 
            item_data = item_inventory.objects.filter(itemcategory__contains='medicine').filter(expiry_status = 'Good for usage')
            primary_key = key
            if name != "":
                item_data = item_data.filter(itemname__contains = name)
                if date != "":
                    item_data = item_data.filter(expiry_date__contains = date)
                    if loc != "":
                        item_data = item_data.filter(location__contains = loc)
                        if cat != "":
                            item_data = item_data.filter(itemcategory__contains = cat)
                            if exp != "":
                                item_data = item_data.filter(expiry_status__contains = exp)
                                if code !="":
                                    item_data = item_data.filter(barcode__contains = code)
                                    context = {'item_data' : item_data,'primary_key':primary_key}
                                    return context
                                else:
                                    context = {'item_data' : item_data,'primary_key':primary_key}
                                    return context
                            elif code != "":
                                item_data = item_data.filter(barcode__contains = code)
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                            else:
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                        elif exp == "":
                            item_data = item_data.filter(expiry_status__contains = exp)
                            if code !="":
                                item_data = item_data.filter(barcode__contains = code)
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                            else:
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                        elif code != "":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context

                    elif cat != "":
                        item_data = item_data.filter(itemcategory__contains = cat)
                        if exp != "":
                            item_data = item_data.filter(expiry_status__contains = exp)
                            if code !="":
                                item_data = item_data.filter(barcode__contains = code)
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                            else:
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                        elif code != "":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context

                    elif exp != "":
                        item_data = item_data.filter(expiry_status__contains = exp)
                        if code !="":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                    elif code != "":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context


                elif loc != "": 
                    item_data = item_data.filter(location__contains = loc)
                    if cat != "":
                        item_data = item_data.filter(itemcategory__contains = cat)
                        if exp != "":
                            item_data = item_data.filter(expiry_status__contains = exp)
                            if code !="":
                                item_data = item_data.filter(barcode__contains = code)
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                            else:
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                        elif code != "":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                    elif exp != "":
                        item_data = item_data.filter(item_data = exp)
                        if code !="":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                    elif code != "":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context

                elif cat != "":
                    item_data = item_data.filter(itemcategory__contains = cat)
                    if exp != "":
                        item_data = item_data.filter(expiry_status__contains = exp)
                        if code !="":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                    elif code != "":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                elif exp != "":
                    item_data = item_data.filter(expiry_status__contains = exp)
                    if code !="":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                elif code != "":
                    item_data = item_data.filter(barcode__contains = code)
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context
                else:
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context

            elif date != "":
                item_data = item_data.filter(expiry_date__contains = date)
                if cat != "":
                    item_data = item_data.filter(itemcategory__contains = cat)
                    if loc != "": 
                        item_data = item_data.filter(location__contains = loc)
                        if exp != "":
                            item_data = item_data.filter(expiry_status__contains = exp)
                            if code !="":
                                item_data = item_data.filter(barcode__contains = code)
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                            else:
                                context = {'item_data' : item_data,'primary_key':primary_key}
                                return context
                        elif code != "":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                    elif exp != "":
                        item_data = item_data.filter(expiry_status__contains = exp)
                        if code !="":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                    elif code != "":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                elif loc != "":
                    item_data = item_data.filter(location__contains = loc)
                    if exp != "":
                        item_data = item_data.filter(expiry_status__contains = exp)
                        if code !="":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                    elif code != "":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context

                elif exp != "":
                    item_data = item_data.filter(expiry_status__contains = exp)
                    if code !="":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                elif code != "":
                    item_data = item_data.filter(barcode__contains = code)
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context
                else:
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context

            elif loc != "":  
                item_data = item_data.filter(location__contains = loc)
                if cat != "":
                    item_data = item_data.filter(itemcategory__contains = cat)
                    if exp != "":
                        item_data = item_data.filter(expiry_status__contains = exp)
                        if code !="":
                            item_data = item_data.filter(barcode__contains = code)
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                        else:
                            context = {'item_data' : item_data,'primary_key':primary_key}
                            return context
                    elif code != "":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context

                elif exp != "":
                    item_data = item_data.filter(expiry_status__contains = exp)
                    if code !="":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                elif code != "":
                    item_data = item_data.filter(barcode__contains = code)
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context
                else:
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context

            elif cat != "":
                item_data = item_data.filter(itemcategory__contains = cat)
                if exp != "":
                    item_data = item_data.filter(expiry_status__contains = exp)
                    if code !="":
                        item_data = item_data.filter(barcode__contains = code)
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                    else:
                        context = {'item_data' : item_data,'primary_key':primary_key}
                        return context
                elif code != "":
                    item_data = item_data.filter(barcode__contains = code)
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context
                else:
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context
            elif exp != "":
                item_data = item_data.filter(expiry_status__contains = exp)
                if code !="":
                    item_data = item_data.filter(barcode__contains = code)
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context
                else:
                    context = {'item_data' : item_data,'primary_key':primary_key}
                    return context
            elif code != "":
                item_data = item_data.filter(barcode__contains = code)
                context = {'item_data' : item_data,'primary_key':primary_key}
                return context
            else:
                context = {'item_data' : item_data,'primary_key':primary_key}
                return context

def filterloop5(name,code,loc,cat):
            items_data = item_inventory.objects.filter(expiry_date = None)
            if name != "":
                items_data = items_data.filter(itemname__contains = name)
                if code != "":
                    items_data = items_data.filter(barcode__contains = code)
                    if loc != "":
                        items_data = items_data.filter(location__contains = loc)
                        if cat != "":
                            items_data = items_data.filter(itemcategory__contains = cat)
                            context = {'items_data' : items_data,}
                            return context
                        elif cat == "":
                            context = {'items_data' : items_data,}
                            return context
                    elif cat != "":
                        items_data = items_data.filter(itemcategory__contains = cat)
                        context = {'items_data' : items_data,}
                        return context
                    elif cat == "":
                            context = {'items_data' : items_data,}
                            return context
                elif loc != "": 
                    items_data = items_data.filter(location__contains = loc)
                    if cat != "":
                        items_data = items_data.filter(itemcategory__contains = cat)
                        context = {'items_data' : items_data,}
                        return context
                    elif cat == "":
                        context = {'items_data' : items_data,}
                        return context
                elif cat != "":
                    items_data = items_data.filter(itemcategory__contains = cat)
                    context = {'items_data' : items_data,}
                    return context
                elif cat == "":
                    context = {'items_data' : items_data,}
                    return context
            elif code != "":
                items_data = items_data.filter(barcode__contains = code)
                if cat != "":
                    items_data = items_data.filter(itemcategory__contains = cat)
                    if loc != "": 
                        items_data = items_data.filter(location__contains = loc)
                        context = {'items_data' : items_data,}
                        return context
                    elif loc == "":
                        context = {'items_data' : items_data,}
                        return context
                elif loc != "":
                    items_data = items_data.filter(location__contains = loc)
                    context = {'items_data' : items_data,}
                    return context
                elif loc == "":
                    context = {'items_data' : items_data,}
                    return context
            elif loc != "":  
                items_data = items_data.filter(location__contains = loc)
                if cat != "":
                    items_data = items_data.filter(itemcategory__contains = cat)
                    context = {'items_data' : items_data,}
                    return context
                elif cat == "":
                    context = {'items_data' : items_data,}
                    return context
            elif cat != "":
                items_data = items_data.filter(itemcategory__contains = cat)
                context = {'items_data' : items_data,}
                return context
            else:
                items_data = item_inventory.objects.filter(expiry_date = None)
                context = {'items_data' : items_data}
                return context




def get_context(name, date, med,code, loc, cat):
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    prescription_data = prescription_purchase.objects.all()
    if name != "":
        pat = profile.objects.filter(fullname__contains = name)
        for i in pat:
            list1.append(i.id)
        prescription_data = prescription_data.filter(patient_id__in = list1)
        if med != "":
            items = item_inventory.objects.filter(itemname__contains = med)
            for i in items:
                list2.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list2)
            if date !="":
                prescription_data = prescription_data.filter(purchase_date__contains = date)
                context = {'prescription_data' : prescription_data}
                if code != "":
                    items = item_inventory.objects.filter(barcode__contains = code)
                    for i in items:
                        list4.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list4)
                    if loc != "":
                        items = item_inventory.objects.filter(location__contains = loc)
                        for i in items:
                            list5.append(i.id)
                        prescription_data = prescription_data.filter(item_id__in = list5)
                        if cat!="":
                            items = item_inventory.objects.filter(itemcategory__contains = cat)
                            for i in items:
                                list6.append(i.id)
                            prescription_data = prescription_data.filter(item_id__in = list6)
                            context = {'prescription_data' : prescription_data}
                            return context
                        else:
                            context = {'prescription_data' : prescription_data}
                            return context
                    elif cat !="":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            list6.append(i.id)
                        prescription_data = prescription_data.filter(item_id__in = list6)
                        context = {'prescription_data' : prescription_data}
                        return context

                    else:
                        context = {'prescription_data' : prescription_data}
                        return context

                elif loc != "":
                    items = item_inventory.objects.filter(location__contains = loc)
                    for i in items:
                        list5.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list5)
                    if cat!="":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            list6.append(i.id)
                        prescription_data = prescription_data.filter(item_id__in = list6)
                        context = {'prescription_data' : prescription_data}
                        return context
                    else:
                        context = {'prescription_data' : prescription_data}
                        return context
                elif cat !="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context

            elif code != "":
                items = item_inventory.objects.filter(barcode__contains = code)
                for i in items:
                    list4.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list4)
                if loc != "":
                    items = item_inventory.objects.filter(location__contains = loc)
                    for i in items:
                        list5.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list5)
                    if cat!="":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            list6.append(i.id)
                        prescription_data = prescription_data.filter(item_id__in = list6)
                        context = {'prescription_data' : prescription_data}
                        return context
                    else:
                        context = {'prescription_data' : prescription_data}
                        return context
                elif cat !="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context

            elif loc != "":
                items = item_inventory.objects.filter(location__contains = loc)
                for i in items:
                    list5.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list5)
                if cat!="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context
            elif cat !="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context
        elif date != "":
            prescription_data = prescription_data.filter(purchase_date__contains = date)
            context = {'prescription_data' : prescription_data}
            if code != "":
                items = item_inventory.objects.filter(barcode__contains = code)
                for i in items:
                    list4.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list4)
                if loc != "":
                    items = item_inventory.objects.filter(location__contains = loc)
                    for i in items:
                        list5.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list5)
                    if cat!="":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        context = {'prescription_data' : prescription_data}
                        return context
                        for i in items:
                            list6.append(i.id)
                        prescription_data = prescription_data.filter(item_id__in = list6)
                    else:
                        context = {'prescription_data' : prescription_data}
                        return context

                elif cat !="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                else:
                    context = {'prescription_data' : prescription_data}
                    return context

            elif loc != "":
                items = item_inventory.objects.filter(location__contains = loc)
                for i in items:
                    list5.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list5)
                if cat !="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context
            elif cat !="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context



        elif code != "":
            items = item_inventory.objects.filter(barcode__contains = code)
            for i in items:
                list4.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list4)
            if loc != "":
                items = item_inventory.objects.filter(location__contains = loc)
                for i in items:
                    list5.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list5)
                if cat!="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context
            elif cat !="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context

        elif loc != "":
            items = item_inventory.objects.filter(location__contains = loc)
            for i in items:
                list5.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list5)
            if cat!="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context
        elif cat !="":
            items = item_inventory.objects.filter(itemcategory__contains = cat)
            for i in items:
                list6.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list6)
            context = {'prescription_data' : prescription_data}
            return context
        else:
            context = {'prescription_data' : prescription_data}
            return context


    elif med !="":
        items = item_inventory.objects.filter(itemname__contains = med)
        for i in items:
            list2.append(i.id)
        prescription_data = prescription_data.filter(item_id__in = list2)
        if date!="":
            prescription_data = prescription_data.filter(purchase_date__contains = date)
            context = {'prescription_data' : prescription_data}
            if code != "":
                items = item_inventory.objects.filter(barcode__contains = code)
                for i in items:
                    list4.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list4)
                if loc != "":
                    items = item_inventory.objects.filter(location__contains = loc)
                    for i in items:
                        list5.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list5)
                    if cat!="":
                        items = item_inventory.objects.filter(itemcategory__contains = cat)
                        for i in items:
                            list6.append(i.id)
                        prescription_data = prescription_data.filter(item_id__in = list6)
                        context = {'prescription_data' : prescription_data}
                        return context
                    else:
                        context = {'prescription_data' : prescription_data}
                        return context
                elif cat !="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context

            elif loc != "":
                items = item_inventory.objects.filter(location__contains = loc)
                for i in items:
                    list5.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list5)
                if cat!="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context
            elif cat !="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context

        elif code != "":
            items = item_inventory.objects.filter(barcode__contains = code)
            for i in items:
                list4.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list4)
            if loc != "":
                items = item_inventory.objects.filter(location__contains = loc)
                for i in items:
                    list5.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list5)
                if cat!="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context
            elif cat !="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context

        elif loc != "":
            items = item_inventory.objects.filter(location__contains = loc)
            for i in items:
                list5.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list5)
            if cat!="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context
        elif cat !="":
            items = item_inventory.objects.filter(itemcategory__contains = cat)
            for i in items:
                list6.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list6)
            context = {'prescription_data' : prescription_data}
            return context
        else:
            context = {'prescription_data' : prescription_data}
            return context

    elif date != "":
        prescription_data = prescription_data.filter(purchase_date__contains = date)
        context = {'prescription_data' : prescription_data}
        if code != "":
            items = item_inventory.objects.filter(barcode__contains = code)
            for i in items:
                list4.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list4)
            if loc != "":
                items = item_inventory.objects.filter(location__contains = loc)
                for i in items:
                    list5.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list5)
                if cat!="":
                    items = item_inventory.objects.filter(itemcategory__contains = cat)
                    for i in items:
                        list6.append(i.id)
                    prescription_data = prescription_data.filter(item_id__in = list6)
                    context = {'prescription_data' : prescription_data}
                    return context
                else:
                    context = {'prescription_data' : prescription_data}
                    return context
            elif cat !="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context

        elif loc != "":
            items = item_inventory.objects.filter(location__contains = loc)
            for i in items:
                list5.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list5)
            if cat!="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context
        elif cat !="":
            items = item_inventory.objects.filter(itemcategory__contains = cat)
            for i in items:
                list6.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list6)
            context = {'prescription_data' : prescription_data}
            return context
        else:
            context = {'prescription_data' : prescription_data}
            return context

    elif code != "":
        items = item_inventory.objects.filter(barcode__contains = code)
        for i in items:
            list4.append(i.id)
        prescription_data = prescription_data.filter(item_id__in = list4)
        if loc != "":
            items = item_inventory.objects.filter(location__contains = loc)
            for i in items:
                list5.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list5)
            if cat!="":
                items = item_inventory.objects.filter(itemcategory__contains = cat)
                for i in items:
                    list6.append(i.id)
                prescription_data = prescription_data.filter(item_id__in = list6)
                context = {'prescription_data' : prescription_data}
                return context
            else:
                context = {'prescription_data' : prescription_data}
                return context
        elif cat !="":
            items = item_inventory.objects.filter(itemcategory__contains = cat)
            for i in items:
                list6.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list6)
            context = {'prescription_data' : prescription_data}
            return context
        else:
            context = {'prescription_data' : prescription_data}
            return context
    elif loc != "":
        items = item_inventory.objects.filter(location__contains = loc)
        for i in items:
            list5.append(i.id)
        prescription_data = prescription_data.filter(item_id__in = list5)
        if cat!="":
            items = item_inventory.objects.filter(itemcategory__contains = cat)
            for i in items:
                list6.append(i.id)
            prescription_data = prescription_data.filter(item_id__in = list6)
        else:
            context = {'prescription_data' : prescription_data}
            return context
    elif cat !="":
        items = item_inventory.objects.filter(itemcategory__contains = cat)
        for i in items:
            list6.append(i.id)
        prescription_data = prescription_data.filter(item_id__in = list6)
        context = {'prescription_data' : prescription_data}
        return context
    else:
        context = {'prescription_data' : prescription_data}
        return context



@login_required
def total_monthly_income(request):
    if request.method =="POST":
        date = request.POST['date']
        if date !="":
            d = getDatee(date)
            
            presc_details = prescription_purchase.objects.filter(purchase_date__contains = date) #total_amount
            payment_details = payment.objects.filter(date_paid__contains = date) #total_payment
            tot_presc =  get_income_presc(date)
            tot_pay = get_income_payments(date)
            total_inc = tot_presc + tot_pay
            total_inc = float("%.2f" % total_inc)

            context = {'total_inc':total_inc,'d':d,'date': date,'presc_details':presc_details,'payment_details':payment_details,'tot_presc':tot_presc,'tot_pay':tot_pay}
            return render(request, 'total_monthly_income.html', context)
        else:
            messages.error(request, 'Please Choose date')
            return render(request, 'total_monthly_income.html', {})
    else:
        return render(request, 'total_monthly_income.html', {})


@login_required
def total_monthly_expense(request):
    if request.method =="POST":
        date = request.POST['date']
        if date !="":
            d = getDatee(date)
            bills_data = bills_details.objects.filter(date_paid__contains = date) 
            stockin_data = stock_in.objects.filter(purchase_date__contains = date)#total_payment///purchase_date
            salary_details = salary_info.objects.filter(date_given__contains = date)#total_amount //date_given
            tot_bill = get_expense_bills(date)
            tot_salary = get_expense_salary(date)
            tot_stockin = get_expense_stockin(date)
            total_exp = tot_bill + tot_salary + tot_stockin
            total_exp = float("%.2f" % total_exp)
            context = {'total_exp':total_exp,'d':d, 'bills_data':bills_data,'stockin_data':stockin_data,'salary_details':salary_details,
                        'date': date,'tot_salary':tot_salary,'tot_stockin':tot_stockin,'tot_bill':tot_bill}
            return render(request, 'total_monthly_expense.html', context)
        else:
            messages.error(request, 'Please Choose date')
            return render(request, 'total_monthly_expense.html', {})
    else:
        return render(request, 'total_monthly_expense.html', {})


@login_required
def total_monthly_profit(request):
    if request.method =="POST":
        date = request.POST['date']
        if date !="":
            d = getDatee(date)

            #EXPENSE CALC
            bills_data = get_bill_query(date)   
            stockin_data = stock_in.objects.filter(purchase_date__contains = date)#total_payment///purchase_date
            salary_details = salary_info.objects.filter(date_given__contains = date)#total_amount //date_given
            tot_bill = get_expense_bills(date)
            tot_salary = get_expense_salary(date)
            tot_stockin = get_expense_stockin(date)
            total_exp = tot_bill + tot_salary + tot_stockin
            total_exp = float("%.2f" % total_exp)
            


            #INCOME CALC
            presc_details = prescription_purchase.objects.filter(purchase_date__contains = date) #total_amount
            payment_details = payment.objects.filter(date_paid__contains = date) #total_payment
            tot_presc =  get_income_presc(date)
            tot_pay = get_income_payments(date)
            total_inc = tot_presc + tot_pay
            total_inc = float("%.2f" % total_inc)

            total_p = total_inc - total_exp
            total_p = float("%.2f" % total_p)


            context = {'date': date,'d':d,'total_exp':total_exp,'total_inc':total_inc,'total_p':total_p }
            return render(request, 'total_monthly_profit.html', context)


        else:
            messages.error(request, 'Please Choose date')
            return render(request, 'total_monthly_profit.html', {})
    else:
        return render(request, 'total_monthly_profit.html', {})



def getDatee(date):
    date = date.split('-')
    m = date[1]
    y = date[0]
    month = getmonth(m)
    y = str(y)
    month = str(month)
    return f"{month} {y}"

def getDatee2(date):
    date = date.split('-')
    m = date[1]
    y = date[0]
    d = date[2]
    month = getmonth(m)
    y = str(y)
    month = str(month)
    return f"{month}, {d} {y}"


def get_income_presc(date):
    presc_details = prescription_purchase.objects.filter(purchase_date__contains = date) #total_amount
    tot_presc =  presc_details.aggregate(Sum('total_amount'))
    if tot_presc['total_amount__sum'] != None:
        tot_presc = float("%.2f" % tot_presc["total_amount__sum"])
        return tot_presc
        
    else:
        return 0

def get_income_presc2():
    presc_details = prescription_purchase.objects.all() #total_amount
    tot_presc =  presc_details.aggregate(Sum('total_amount'))
    if tot_presc['total_amount__sum'] != None:
        tot_presc = float("%.2f" % tot_presc["total_amount__sum"])
        return tot_presc
        
    else:
        return 0
    

def get_income_payments(date):
    payment_details = payment.objects.filter(date_paid__contains = date)
    tot_pay = payment_details.aggregate(Sum('total_payment'))
    if tot_pay["total_payment__sum"] != None:
        tot_pay = float("%.2f" % tot_pay["total_payment__sum"])
        return tot_pay
        
    else:
        return 0

def get_income_payments2():
    payment_details = payment.objects.all()
    tot_pay = payment_details.aggregate(Sum('total_payment'))
    if tot_pay["total_payment__sum"] != None:
        tot_pay = float("%.2f" % tot_pay["total_payment__sum"])
        return tot_pay
        
    else:
        return 0
        
def get_expense_bills(date):
    '''
    d = date.split('-')
    m = d[1]
    y = str(d[0])
    month = str(getmonth(m))
    bills_data = bills_details.objects.all()
    bills_data = bills_data.filter(bill_year__contains = y)
    bills_data = bills_data.filter(bill_month__contains = month) 
    '''
    bills_data = bills_details.objects.filter(date_paid__contains = date)
    tot_bill = bills_data.aggregate(Sum('total_amount'))
    if tot_bill['total_amount__sum'] != None:
        tot_bill = float("%.2f" % tot_bill['total_amount__sum'])
        return tot_bill
    else:
        return 0

def get_bill_query(date):
    d = date.split('-')
    m = d[1]
    y = str(d[0])
    month = str(getmonth(m))
    bills_data = bills_details.objects.all()
    bills_data = bills_data.filter(bill_year__contains = y)
    bills_data = bills_data.filter(bill_month__contains = month)
    return bills_data



def get_expense_stockin(date):
    stockin_data = stock_in.objects.filter(purchase_date__contains = date)
    tot_stockin = stockin_data.aggregate(Sum('total_payment'))
    if tot_stockin['total_payment__sum'] != None:
        tot_stockin = float("%.2f" % tot_stockin['total_payment__sum'])
        return tot_stockin

    else:
        return 0


def get_expense_salary(date):
    salary_details = salary_info.objects.filter(date_given__contains = date)
    tot_salary = salary_details.aggregate(Sum('total_amount'))
    if tot_salary['total_amount__sum'] != None:
        tot_salary = float("%.2f" % tot_salary['total_amount__sum'])
        return tot_salary
    else:
        return 0

def more_salary_info(request, primary_key):
    all_data_emp_salary = salary_info.objects.get(pk = primary_key)
    key = all_data_emp_salary.profile_id.id
    context = {"all_data_emp_salary" : all_data_emp_salary,"primary_key":primary_key, 'key':key }
    return render(request, 'more_salary_info.html' ,context)


def income_breakdown(request, date):
    d = getDatee(date)
    presc_details = prescription_purchase.objects.filter(purchase_date__contains = date) 
    payment_details = payment.objects.filter(date_paid__contains = date) 
    tot_presc =  get_income_presc(date)
    tot_pay = get_income_payments(date)
    total_inc = tot_presc + tot_pay
    total_inc = float("%.2f" % total_inc)

    context = {'tot_presc':tot_presc,'tot_pay':tot_pay,'total_inc':total_inc,
                'd':d,"date": date, 'payment_details':payment_details, 'presc_details':presc_details}
    return render(request,'income_breakdown.html',context )

def income_breakdown_pdf(request, date): #wala nagamit
    d = getDatee(date)
    presc_details = prescription_purchase.objects.filter(purchase_date__contains = date) 
    payment_details = payment.objects.filter(date_paid__contains = date) 
    context = {
                'd':d,"date": date, 'payment_details':payment_details, 'presc_details':presc_details}
    return render(request,'income_breakdown_pdf.html',context )



def expense_breakdown(request, date):
    d = getDatee(date)
    bills_data = bills_details.objects.filter(date_paid__contains = date)
    stockin_data = stock_in.objects.filter(purchase_date__contains = date)
    salary_details = salary_info.objects.filter(date_given__contains = date) 

    tot_bill = get_expense_bills(date)
    tot_salary = get_expense_salary(date)
    tot_stockin = get_expense_stockin(date)
    total_exp = tot_bill + tot_salary + tot_stockin
    total_exp = float("%.2f" % total_exp)

    context = {'total_exp':total_exp,'tot_stockin':tot_stockin,'tot_salary':tot_salary,'tot_bill':tot_bill,
                'd':d,"date": date,'bills_data':bills_data,'stockin_data':stockin_data,'salary_details':salary_details}
    return render(request,'expense_breakdown.html',context )

def expense_breakdown_pdf(request, date): #WALA NAGAMIT
    d = getDatee(date)
    bills_data = bills_details.objects.filter(date_paid__contains = date)
    stockin_data = stock_in.objects.filter(purchase_date__contains = date)
    salary_details = salary_info.objects.filter(date_given__contains = date) 
    context = {'d':d,"date": date,'bills_data':bills_data,'stockin_data':stockin_data,'salary_details':salary_details}
    return render(request,'expense_breakdown_pdf.html',context )        


class CalendarView(generic.ListView):
    schedule_checker()
    appointments_checker()
    model = appointment_details
    template_name = 'view_appointments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
        

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


