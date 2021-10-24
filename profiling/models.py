from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model): 
#         prof_id = models.IntegerField(primary_key = True, default = 0)
         fullname = models.CharField(max_length = 200, null = False)
         profile_type = models.CharField(max_length = 200, null = False)
         contact_number = models.CharField(max_length = 13, validators=[MinLengthValidator(13)]) ##change to phone   ##put +63 format PhoneField(blank=False, help_text='Contact phone number')   ## ask how to validate this
#         contact_number = models.CharField(max_length = 133)
         profile_fulladress = models.CharField(max_length = 200, null = False)
         bday = models.DateField(auto_now=False, auto_now_add =False) #CHANGE TO DATE {Y M D} FORMAT
         gender = models.CharField(max_length = 200, null = False)
         ecp_fullname = models.CharField(max_length = 200, null = False)
         ecp_contactnum = models.CharField(max_length = 13, validators=[MinLengthValidator(13)])#change to phone
#         ecp_contactnum = models.CharField(max_length = 133)
         ecp_relationship = models.CharField(max_length = 200, null = False)
         ecp_fulladress = models.CharField(max_length = 200, null = False)
         added = models.DateField(auto_now=False, auto_now_add =True, null = False) #wala ni sa forms #TARUNGON PANI PAG INPUT HEHE
         update = models.DateField(auto_now=True, auto_now_add =False, null = False) #wala ni sa forms #TARUNGON PANI PAG INPUT HEHE
         

         def __str__(self):
                  return self.fullname


class accounts(models.Model):
        user_id = models.OneToOneField(User, default = 1, on_delete = models.CASCADE, db_constraint = False)
        profile_id = models.ForeignKey(profile, on_delete = models.CASCADE, default = 1, db_constraint = False)
        def __str__(self):
                  return str(self.user_id.username)


class pat_info(models.Model):
#         patient_id(P)
         profile_id = models.ForeignKey(profile, on_delete = models.CASCADE, default = 1, db_constraint = False)
         pat_occupation = models.CharField(max_length = 200,null = False, default = 'None')
         pat_allergies = models.TextField(max_length = 200,null = False, default = 'None') #THINK MORE ABOUT THIS


         def __str__(self):
                  return str(self.profile_id)



class emp_info(models.Model):
#         emp_id (P)
         profile_id = models.ForeignKey(profile, on_delete = models.CASCADE, default = 1, db_constraint = False)
         emp_position = models.CharField(max_length = 200, null = False,default = 'None') 
         emp_status = models.CharField(max_length = 200, null = False,default = 'None') #EMPPLOYED OR WALA NA SA BUSINESS DO DROPDOWN LNG


         def __str__(self):
                  return str(self.profile_id)
      

class item_inventory(models.Model):
    barcode = models.CharField(max_length = 100, default = "00000000")
    itemname = models.CharField(max_length = 200)
    itemcategory = models.CharField(max_length = 200)
    location = models.CharField(max_length = 200)
    item_fee = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    quantity = models.IntegerField(default = 0)
    units = models.CharField(max_length = 200)
    expiry_date = models.DateField(auto_now=False, auto_now_add =False, null = True, blank = True)
    expiry_status = models.CharField(max_length = 200, default = 'Good for usage')


    def __str__(self):
        return self.itemname





'''

class teeth_chart(models.Model):
#    teeth_chart_id(P)
    patient_id = models.ForeignKey(pat_info, default = 1, on_delete = models.CASCADE)
    teeth_location = models.CharField(max_length = 200)
    teeth_type = models.CharField(max_length = 200)
    health_status = models.CharField(max_length = 200)

    def __int__(self):
        return self.id

'''


class available_schedules(models.Model):
#    schedule_id (P)
    date = models.DateField(auto_now=False, auto_now_add =False)
    time = models.TimeField(auto_now=False, auto_now_add =False)
    doctor_lastname = models.CharField(max_length = 200)
    availability = models.BooleanField(default = True)

    def __int__(self): #i keep lng ni na ID para dli mag error
        return self.id
#        return f"Date: {self.date} | Time: {self.time} | Assigned Doctor: {self.doctor_lastname} | Availability: {self.availability}"



class available_services(models.Model):
#    service_id (P)
    service_type = models.CharField(max_length = 200)
    service_fee = models.DecimalField(max_digits = 10, decimal_places = 2)
    availability = models.BooleanField(default = True)

    def __str__(self):
        return self.service_type
#    def __str__(self):
#        return self.service_type
#        return f"Service: {self.service_type}, Service Fee: Php. {self.service_fee}"



class appointment_details(models.Model):
#    appointment_id(P)
    appointment_type = models.CharField(max_length = 200)
    patient_id = models.ForeignKey(profile, default = 1, on_delete = models.CASCADE)
    schedule_id = models.ForeignKey(available_schedules, default = 1, on_delete = models.CASCADE)
    service_id = models.ForeignKey(available_services, default = 1, on_delete = models.CASCADE)
    complain = models.CharField(max_length = 200)
    appointment_status = models.CharField(max_length = 200, default ="Ongoing")
    payment_status = models.CharField(max_length = 200, default ="Pending") 

    def __int__(self):
        return self.id

    @property
    def get_html_url(self):
        url = reverse('editform', args=(self.id, 'appointments'))
        return f'<a class="cal_data" href="{url}"> <span style="display: block;"><b>Patient:</b> {self.patient_id.fullname}</span> <span style="display: block;"> <b>Time:</b> {self.schedule_id.time }</span> <span style="display: block;"><b>Status:</b> {self.appointment_status}</span> <br></br> </a>'

#        return f'<a style="color: #000000"href="{url}"> {self.patient_id.fullname}, Time: {self.schedule_id.time }, Status: {self.appointment_status} </a>'

    '''
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    '''

class teeths(models.Model):
    patient_id = models.ForeignKey(profile, on_delete=models.CASCADE, default = 1)
    LCI_left = models.CharField(max_length = 200,default = 'Lower Central Incisor(Left)')
    LLI_left = models.CharField(max_length = 200,default = 'Lower Lateral Incisor(Left)')
    LC_left = models.CharField(max_length = 200,default = 'Lower Canine(Left)')
    LF_left = models.CharField(max_length = 200,default = 'Lower First Molar(Left)')
    LSM_left = models.CharField(max_length = 200,default = 'Lower Second Molar(Left)')
    LCI_right = models.CharField(max_length = 200,default = 'Lower Central Incisor(Right)')
    LLI_right = models.CharField(max_length = 200,default = 'Lower Lateral Incisor(Right)')
    LC_right = models.CharField(max_length = 200,default = 'Lower Canine(Right)')
    LFM_right = models.CharField(max_length = 200,default = 'Lower First Molar(Right)')
    LSM_right = models.CharField(max_length = 200,default = 'Lower Second Molar(Right)')
    UCI_left = models.CharField(max_length = 200,default = 'Upper Central Incisor(Left)')
    ULI_left = models.CharField(max_length = 200,default = 'Upper Lateral Incisor(Left)')
    UC_left = models.CharField(max_length = 200,default = 'Upper Canine(Left)')
    UF_left = models.CharField(max_length = 200,default = 'Upper First Molar(Left)')
    USM_left = models.CharField(max_length = 200,default = 'Upper Second Molar(Left)')
    UCI_right = models.CharField(max_length = 200,default = 'Upper Central Incisor(Right)')
    ULI_right = models.CharField(max_length = 200,default = 'Upper Lateral Incisor(Right)')
    UC_right = models.CharField(max_length = 200,default = 'Upper Canine(Right)')
    UFM_right = models.CharField(max_length = 200,default = 'Upper First Molar(Right)')
    USM_right = models.CharField(max_length = 200,default = 'Upper Second Molar(Right)')


    UTM_right = models.CharField(max_length = 200,default = 'Upper Third Molar(Right)')
    UTM_left = models.CharField(max_length = 200,default = 'Upper Third Molar(Left)')
    LTM_right = models.CharField(max_length = 200,default = 'Lower Third Molar(Right)')
    LTM_left = models.CharField(max_length = 200,default = 'Lower Third Molar(Left)')


    U2PM_right = models.CharField(max_length = 200,default = 'Upper 2nd Premolar(Right)')
    U2PM_left = models.CharField(max_length = 200,default = 'Upper 2nd Premolar(Left)')
    L2PM_right = models.CharField(max_length = 200,default = 'Lower 2nd Premolar(Right)')
    L2PM_left = models.CharField(max_length = 200,default = 'Lower 2nd Premolar(Left)')

    U1PM_right = models.CharField(max_length = 200,default = 'Upper 1st Premolar(Right)')
    U1PM_left = models.CharField(max_length = 200,default = 'Upper 1st Premolar(Left)')
    L1PM_right = models.CharField(max_length = 200,default = 'Lower 1st Premolar(Right)')
    L1PM_left = models.CharField(max_length = 200,default = 'Lower 1st Premolar(Left)')


    teeth_type = models.CharField(max_length = 200, default = 'Adult')











    teeth_type = models.CharField(max_length = 200, default = 'Adult')



    def __int__(self):
        return self.id



class procedures_done(models.Model):
#    procedure_id (P)
    appointment_id = models.ForeignKey(appointment_details, on_delete = models.CASCADE, default = 1, db_constraint = False)
    procedures_done = models.CharField(max_length=200)
    patient_id = models.ForeignKey(profile, on_delete = models.CASCADE, default = 1, db_constraint = False)
#    teeth_position = models.ForeignKey(teeths, on_delete = models.CASCADE, default = 1, db_constraint = False)
    teeth_position = models.CharField(max_length=200, default = None)
    procedures_fee = models.DecimalField(max_digits=10,decimal_places=2)


    def __int__(self):
        return self.id



class tools_items_used(models.Model):
#    tools_items_used_id (P)
    appointment_id = models.ForeignKey(appointment_details, on_delete = models.CASCADE, default = 1, db_constraint = False)
    item_id = models.ForeignKey(item_inventory, default = 1, on_delete = models.CASCADE)
#    item_name = models.CharField(max_length=200)
    quantity_used = models.IntegerField() #put minimum and maximum ani tas i-base sa pila ang nasa inventory ##CHECK LATER
    units = models.CharField(max_length=200)
    item_tools_fee = models.DecimalField(max_digits=10,decimal_places=2, default = 0)
    date_used = models.DateField(auto_now=False, auto_now_add =False)


    def __int__(self):
        return self.id




class payment(models.Model):
#    payment_id (P)
    appointment_id = models.ForeignKey(appointment_details, default = 1, on_delete= models.CASCADE)
    total_payment = models.DecimalField(max_digits = 10, decimal_places= 2)
    payment_method = models.CharField(max_length=200)
    date_paid = models.DateField(auto_now=False, auto_now_add =False)


    def __int__(self):
        return self.id

'''
class appointment_details(models.Model):
#    appointment_id(P)
    appointment_type = models.CharField(max_length = 200)
    patient_id = models.ForeignKey(profile, default = 1, on_delete = models.CASCADE)
    schedule_id = models.ForeignKey(available_schedules, default = 1, on_delete = models.CASCADE)
    service_id = models.ForeignKey(available_services, default = 1, on_delete = models.CASCADE)
    complain = models.CharField(max_length = 200)
    appointment_status = models.CharField(max_length = 200, default ="Ongoing")
    payment_status = models.CharField(max_length = 200, default ="Pending") 

'''

class prescription_management(models.Model):
#    prescription_id (P)
    patient_id = models.ForeignKey(profile, default = 1, on_delete = models.CASCADE)
    given_by = models.CharField(max_length=200)
    meds_prescription = models.CharField(max_length=200)
    quantity = models.IntegerField() 
    units = models.CharField(max_length=200)
    intake_instructions = models.CharField(max_length=1000, default = 'None')
    date_given = models.DateField(auto_now=False, auto_now_add =False)
    #presc_status = models.CharField(max_length=200, default = 'Ongoing')

    def __int__(self):
        return self.id

'''

class appointment_history(models.Model):
#    history_id (P)
    patient_id = models.ForeignKey(pat_info, default = 1, on_delete = models.CASCADE)
    appointment_id = models.ForeignKey(appointment_details, default = 1, on_delete= models.CASCADE)
    payment_id = models.ForeignKey(payment, default = 1, on_delete=models.CASCADE)
    prescription_id = models.ForeignKey(prescription_management, default = 1, on_delete=models.CASCADE)

    def __int__(self):
        return self.id



class tooth_procedure_history(models.Model):
    teeth_chart_id = models.ForeignKey(teeth_chart, default = 1, on_delete=models.CASCADE)
    history_id = models.ForeignKey(appointment_history, default = 1, on_delete= models.CASCADE)
    procedures_one = models.CharField(max_length = 200)
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __int__(self):
        return self.id



class patient_allergies(models.Model):
    patient_id = models.ForeignKey(pat_info, default = 1, on_delete = models.CASCADE)
    pat_allergies = models.CharField(max_length=200)

    def __int__(self):
        return self.id

'''

class prescription_purchase(models.Model):
#    purchase_id(P)
#    prescription_id = models.ForeignKey(prescription_management, default = 1, on_delete= models.CASCADE)
    patient_id = models.ForeignKey(profile, default = 1, on_delete = models.CASCADE)
#    meds_bought = models.CharField(max_length=200) #this should be in inventory
    item_id = models.ForeignKey(item_inventory, default = 1, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1) #put minimum and maximum ani tas i-base sa pila ang nasa inventory ##CHECK LATER
    units = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    payment_method = models.CharField(max_length=200, default = 'None')
    purchase_date = models.DateField(auto_now=False, auto_now_add =False)


    def __int__(self):
        return self.id

'''

class stock_out(models.Model):
#    stock_out_id
    item_id = models.ForeignKey(item_inventory, default = 1, on_delete=models.CASCADE)
    stock_out_type = models.CharField(max_length = 200)
    quantity_stock_out = models.IntegerField(default = 0)
    units = models.CharField(max_length = 200)
    date_used_expired = models.DateField(auto_now=False, auto_now_add =False)
    stock_out_reason = models.CharField(max_length = 200)

    def __int__(self):
        return self.id

'''

class stock_in(models.Model):  #NON PERISHABLE
#    stock_in_id
    item_id = models.ForeignKey(item_inventory, on_delete=models.CASCADE, null = True, blank = True)
    item_name = models.CharField(max_length = 200, default = 'None')
#    stock_in_type = models.CharField(max_length = 200)
    quantity_added = models.IntegerField(default = 0)
    units = models.CharField(max_length = 200)
#    date_added = models.DateField(auto_now=False, auto_now_add =False)
#    stock_in_reason = models.CharField(max_length = 200)
#    stock_in_id = models.ForeignKey(stock_in, default = 1, on_delete=models.CASCADE)
    total_payment = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    purchase_date = models.DateField(auto_now=False, auto_now_add =False, null = True, blank = True)
    manufacturer = models.CharField(max_length = 200, null = True, blank = True)

    def __int__(self):
        return self.id


'''
class stock_in_perishable(models.Model):  #NON PERISHABLE
#    stock_in_id
    item_id = models.ForeignKey(item_inventory, default = 1, on_delete=models.CASCADE)
#    stock_in_type = models.CharField(max_length = 200)
    quantity_added = models.IntegerField(default = 0)
    units = models.CharField(max_length = 200)
#    date_added = models.DateField(auto_now=False, auto_now_add =False)
#    stock_in_reason = models.CharField(max_length = 200)
#    stock_in_id = models.ForeignKey(stock_in, default = 1, on_delete=models.CASCADE)
    total_payment = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    purchase_date = models.DateField(auto_now=False, auto_now_add =False, null = True, blank = True)
    manufacturer = models.CharField(max_length = 200, null = True, blank = True)

    def __int__(self):
        return self.id
'''
















'''


class tools_items_stockout(models.Model):
    stock_out_id = models.ForeignKey(stock_out, default = 1, on_delete = models.CASCADE)
    tools_items_used_id = models.ForeignKey(tools_items_used, default = 1, on_delete = models.CASCADE)


    def __int__(self):
        return self.id



class sales_item(models.Model):
    stock_out_id = models.ForeignKey(stock_out, default = 1, on_delete = models.CASCADE)
    purchase_id = models.ForeignKey(prescription_purchase, default = 1, on_delete = models.CASCADE) 


    def __int__(self):
        return self.id



class admin_account(models.Model):
    emp_id = models.ForeignKey(emp_info, default = 1, on_delete = models.CASCADE)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200) #PASSWORD DAPAT NI HA

    def __int__(self):
        return self.id



class log_in_record(models.Model):
    emp_id = models.ForeignKey(emp_info, default = 1, on_delete = models.CASCADE)
    date_log_in = models.DateField(auto_now=False, auto_now_add =False)

    def __int__(self):
        return self.id

'''

class salary_info(models.Model):
    #salary_id (P)
    profile_id = models.ForeignKey(profile, default = 1, on_delete = models.CASCADE)
    regular = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    overtime = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    tips = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    severance = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    philhealth = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    sss = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    pagibig = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    insurance = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    others = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2, default = 0)
    total_amount = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    date_given = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.profile_id)


class expense(models.Model):
    exp_type = models.CharField(max_length = 200) #SALES OR INCOME FROM APPOINTMENTS
    exp_date = models.DateField(auto_now=False, auto_now_add =False)

    def __int__(self):
        return self.id



class salary_details(models.Model):
    exp_id = models.ForeignKey(expense, default = 1, on_delete = models.CASCADE)
    salary_type = models.CharField(max_length = 200)
    salary_id = models.ForeignKey(salary_info, default = 1, on_delete = models.CASCADE)
    total = models.DecimalField(max_digits = 10, decimal_places = 2)
    

    def __int__(self):
        return self.id


'''
class salary_deductions(models.Model):
    salary_id = models.ForeignKey(salary_info, default = 1, on_delete = models.CASCADE)
    philhealth = models.DecimalField(max_digits=10, decimal_places=2)
    sss = models.DecimalField(max_digits=10, decimal_places=2)
    pagibig = models.DecimalField(max_digits=10, decimal_places=2)
    insurance = models.DecimalField(max_digits=10, decimal_places=2)
    others = models.DecimalField(max_digits=10, decimal_places=2)
    total_deduction = models.DecimalField(max_digits=10, decimal_places=2)

    def __int__(self):
        return self.id
'''

'''

class purchase_item(models.Model):
    stock_in_id = models.ForeignKey(stock_in, default = 1, on_delete=models.CASCADE)
    total_payment = models.DecimalField(max_digits = 10, decimal_places = 2)
    itempurchase_date = models.DateField(auto_now=False, auto_now_add =False)
    manufacturer = models.CharField(max_length = 200)

    def __int__(self):
        return self.id
         


class income(models.Model):
    inc_type = models.CharField(max_length = 200) #SALES OR INCOME FROM APPOINTMENTS
    inc_date = models.DateField(auto_now=False, auto_now_add =False)

    def __int__(self):
        return self.id



class income_details(models.Model):
    inc_id = models.ForeignKey(income, default = 1, on_delete = models.CASCADE)
    payment_id = models.ForeignKey(payment, default = 1, on_delete = models.CASCADE)

    def __int__(self):
        return self.id



class sales_details(models.Model):
    inc_id = models.ForeignKey(income, default = 1, on_delete = models.CASCADE)
    purchase_id = models.ForeignKey(prescription_purchase, default = 1, on_delete = models.CASCADE) 

    def __int__(self):
        return self.id



class purchase_details(models.Model):
    exp_id = models.ForeignKey(expense, default = 1, on_delete = models.CASCADE)
    itempurchase_id = models.ForeignKey(purchase_item, on_delete = models.CASCADE)

    def __int__(self):
        return self.id

'''

class bills_details(models.Model):
#    exp_id = models.ForeignKey(expense, default = 1, on_delete = models.CASCADE)
    bill_type = models.CharField(max_length = 200)
    bill_month = models.CharField(max_length = 200, default = 'January')
    bill_year = models.CharField(max_length = 200, default = '2020')
    total_amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    paid_by = models.CharField(max_length = 200)
    date_paid = models.DateField(auto_now=False, auto_now_add =False)

    def __int__(self):
        return self.id

'''

class Ecp(models.Model):
         profile_id = models.ForeignKey(profile, on_delete=models.CASCADE)
         ecp_fullname = models.CharField(max_length = 200)
         ecp_contactnum = models.CharField(max_length = 200)#change to phone
         ecp_relationship = models.CharField(max_length = 200)
         ecp_fulladress = models.CharField(max_length = 200)

         def __str__(self):
                  return self.ecp_fullname
'''  



class teeths_status(models.Model):
    teeth_id = models.ForeignKey(teeths, on_delete=models.CASCADE, default = 1)
    status = models.CharField(max_length = 200, default = 'No data')
    procedure_id = models.ForeignKey(procedures_done, on_delete=models.CASCADE, default = 1)

    def __int__(self):
        return self.id
