from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import profile
#from .models import Ecp
from .models import emp_info
from .models import pat_info
from .models import salary_info
from .models import salary_details
from .models import appointment_details
from .models import available_services
from .models import available_schedules
from .models import item_inventory
from .models import procedures_done
from .models import tools_items_used
from .models import payment
from .models import prescription_management
from .models import prescription_purchase
from .models import bills_details
from .models import stock_in
from .models import teeths
from .models import teeths_status
from .models import accounts


class changePassword(forms.Form):
   old_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs ={'class':'form-control','type':'password'}))
   new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs ={'class':'form-control','type':'password'}))
   new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs ={'class':'form-control','type':'password'}))

   class Meta:
      model = User
      fields = ['old_password','new_password1','new_password2']

class searchForm(forms.Form):
         name = forms.CharField(max_length = 100, required = False)
         date = forms.CharField(max_length = 100, required = False)
         date2 = forms.CharField(max_length = 100, required = False)
         cat = forms.CharField(max_length = 100, required = False)
         loc = forms.CharField(max_length = 100, required = False)
         doc = forms.CharField(max_length = 100, required = False)
         service = forms.CharField(max_length = 100, required = False)
         med = forms.CharField(max_length = 100, required = False)
         exp = forms.CharField(max_length = 100, required = False)
         code = forms.CharField(max_length = 100, required = False)

                  

class accForm(forms.ModelForm):
   class Meta:
      model = accounts
      fields = ['profile_id']



class profileForm(forms.ModelForm):
         class Meta:
                  model = profile
                  fields = ['fullname', 'profile_type', 'contact_number', 'profile_fulladress', 'bday' 
                           , 'gender','ecp_fullname', 'ecp_contactnum','ecp_relationship','ecp_fulladress']

class addForm(forms.ModelForm):
         class Meta:
                  model = profile
                  fields = ['fullname', 'profile_type', 'contact_number', 'profile_fulladress', 'bday' 
                           , 'gender','ecp_fullname', 'ecp_contactnum','ecp_relationship','ecp_fulladress']

'''
class EcpForm(forms.ModelForm):
         class Meta:
                  model = Ecp
                  fields = ['ecp_fullname', 'ecp_contactnum','ecp_relationship','ecp_fulladress']
'''
class EditForm(forms.ModelForm):
         class Meta:
                  model = profile
                  fields = fields = ['fullname', 'profile_type', 'contact_number', 'profile_fulladress', 'bday' 
                           , 'gender','ecp_fullname', 'ecp_contactnum','ecp_relationship','ecp_fulladress']

class emp_infoForm(forms.ModelForm):
         class Meta:
            model = emp_info
            fields = ['profile_id','emp_position', 'emp_status']

class emp_EditinfoForm(forms.ModelForm):
         class Meta:
            model = emp_info
            fields = ['emp_position', 'emp_status']


class edit_empinfoForm(forms.ModelForm):
         class Meta:
            model = emp_info
            fields = ['emp_position', 'emp_status']


         
class pat_infoForm(forms.ModelForm):
         class Meta:
            model = pat_info
            fields = ['profile_id', 'pat_occupation', 'pat_allergies']

class edit_patinfoForm(forms.ModelForm):
         class Meta:
            model = pat_info
            fields = ['pat_occupation', 'pat_allergies']

class pat_EditinfoForm(forms.ModelForm):
         class Meta:
            model = pat_info
            fields = ['pat_occupation', 'pat_allergies']

class salary_infoForm(forms.ModelForm):
         class Meta:
            model = salary_info
            fields = ['profile_id', 'regular', 'overtime','bonus', 'tips','severance',
            'philhealth', 'sss', 'pagibig', 'insurance', 'tax', 'others','date_given'] # 'date_given'
            
class calculate_salaryForm(forms.ModelForm):
         class Meta:
            model = salary_info
            fields = ['total_salary', 'total_deduction','total_amount']

class salary_EditinfoForm(forms.ModelForm):
         class Meta:
            model = salary_info
            fields = ['regular', 'overtime','bonus', 'tips','severance',
            'philhealth', 'sss', 'pagibig', 'insurance','tax', 'others', 'date_given']


class salary_detailsForm(forms.ModelForm):
         class Meta:
            model = salary_details
            fields = ['salary_type', 'total']


class add_appointmentinfoForm(forms.ModelForm):
         class Meta:
            model = appointment_details
            fields = ['appointment_type', 'patient_id', 'schedule_id', 'service_id','complain']

class edit_appointmentinfoForm(forms.ModelForm):
         class Meta:
            model = appointment_details
            fields = ['appointment_type', 'complain', 'appointment_status'] #ADD APPOINTMENT STATUS HERE

class add_servicesForm(forms.ModelForm):
         class Meta:
            model = available_services
            fields = ['service_type', 'service_fee']
            

class edit_servicesForm(forms.ModelForm):
         class Meta:
            model = available_services
            fields = ['service_type', 'service_fee', 'availability']
            

class add_scheduleForm(forms.ModelForm):
         class Meta:
            model = available_schedules
            fields = ['date', 'time', 'doctor_lastname']

class edit_scheduleForm(forms.ModelForm):
         class Meta:
            model = available_schedules
            fields = ['date', 'time', 'doctor_lastname','availability']

class add_inventoryForm(forms.ModelForm):
         class Meta:
            model = item_inventory
            fields = ['itemname', 'barcode','itemcategory', 'location','item_fee', 'quantity','units', 'expiry_date'] #, 'expiry_date'

class add_proceduresForm(forms.ModelForm):
         class Meta:
            model = procedures_done
            fields = ['appointment_id', 'procedures_done','patient_id', 'teeth_position', 'procedures_fee']

class add_tools_items_usedForm(forms.ModelForm):
         class Meta:
            model = tools_items_used
            fields = ['appointment_id', 'item_id', 'quantity_used', 'units', 'date_used'] #'item_tools_fee', 
class edit_proceduresForm(forms.ModelForm):
         class Meta:
            model = procedures_done
            fields = [ 'procedures_done', 'teeth_position', 'procedures_fee']

class edit_tools_items_usedForm(forms.ModelForm):
         class Meta:
            model = tools_items_used
            fields = ['item_id', 'quantity_used', 'units',  'date_used'] #'item_tools_fee',

class make_paymentForm(forms.ModelForm):
         class Meta:
            model = payment
            fields = ['appointment_id', 'total_payment', 'payment_method', 'date_paid']
                  

class prescriptionForm(forms.ModelForm):
         class Meta:
            model = prescription_management
            fields = ['patient_id', 'given_by', 'meds_prescription', 'quantity', 'units','intake_instructions', 'date_given'] #, 'presc_status'

class edit_prescriptionForm(forms.ModelForm):
         class Meta:
            model = prescription_management
            fields = [ 'given_by', 'meds_prescription', 'quantity', 'units','intake_instructions', 'date_given'] #, 'presc_status'

class buy_prescriptionForm(forms.ModelForm):
         class Meta:
            model = prescription_purchase
            fields = [ 'patient_id', 'item_id', 'quantity', 'units', 'purchase_date']

class calculate_paymentForm(forms.ModelForm):
         class Meta:
            model = prescription_purchase
            fields = [ 'total_amount', 'payment_method']

class add_billsForm(forms.ModelForm):
         class Meta:
            model = bills_details
            fields = ['bill_type','bill_month','bill_year','total_amount','paid_by','date_paid',]



class edit_billsForm(forms.ModelForm):
         class Meta:
            model = bills_details
            fields = ['bill_type','bill_month','bill_year','total_amount','paid_by','date_paid',]


'''
class stock_inForm(forms.ModelForm):
         class Meta:
            model = stock_in
            fields = ['item_id','quantity_added','units','date_added']
'''

class add_nonperishableForm(forms.ModelForm):
         class Meta:
            model = stock_in
            fields = ['item_id','item_name','quantity_added','units', 'total_payment', 'purchase_date', 'manufacturer']

class add_perishableForm(forms.ModelForm):
         class Meta:
            model = stock_in
            fields = ['item_id','item_name','quantity_added','units', 'total_payment', 'purchase_date', 'manufacturer']

class add_inventoryForm2(forms.ModelForm):
         class Meta:
            model = item_inventory
            fields = ['itemname', 'barcode', 'itemcategory', 'location','item_fee', 'quantity','units']

class add_chartForm(forms.ModelForm):
         class Meta:
            model = teeths
            fields = ['patient_id','teeth_type']