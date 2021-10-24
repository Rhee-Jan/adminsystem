from django.contrib import admin
from .models import profile
from .models import accounts
#from .models import Ecp
from .models import pat_info
from .models import emp_info
from .models import salary_info
from .models import salary_details
from .models import expense
from .models import available_schedules
from .models import available_services
from .models import appointment_details
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

admin.site.register(prescription_management)
admin.site.register(profile)
#admin.site.register(Ecp)
admin.site.register(pat_info)
admin.site.register(emp_info)
admin.site.register(item_inventory)

admin.site.register(salary_info)
admin.site.register(salary_details)
admin.site.register(expense)

admin.site.register(available_schedules)
admin.site.register(available_services)
admin.site.register(appointment_details)
admin.site.register(procedures_done)
admin.site.register(tools_items_used)
admin.site.register(payment)
admin.site.register(prescription_purchase)
admin.site.register(bills_details)
admin.site.register(stock_in)

admin.site.register(teeths)
admin.site.register(teeths_status)

admin.site.register(accounts)
'''
#--------Not so sure fields-------

from .models import admin_account
from .models import log_in_record
from .models import salary_deductions
from .models import salary_info
admin.site.register(admin_account)
admin.site.register(log_in_record)
admin.site.register(salary_deductions)
admin.site.register(salary_info)



#------additional patient-----
from .models import(patient_allergies)
from .models import teeth_chart
from .models import tooth_procedure_history
from .models import appointment_history
admin.site.register(teeth_chart)
admin.site.register(tooth_procedure_history)
admin.site.register(appointment_history)
admin.site.register(patient_allergies)


#-------Appointment--------

from .models import appointment_details
from .models import available_schedules
from .models import available_doctors
from .models import available_services
admin.site.register(appointment_details)
admin.site.register(available_schedules)
admin.site.register(available_doctors)
admin.site.register(available_services)



from .models import procedures_done
from .models import tools_items_used

from .models import prescription_purchase
from .models import tools_items_stockout
from .models import sales_item

admin.site.register(procedures_done)
admin.site.register(tools_items_used)

admin.site.register(prescription_purchase)
admin.site.register(tools_items_stockout)
admin.site.register(sales_item)





#------inventory-------
from .models import(purchase_item)
from .models import item_inventory 
from .models import stock_out
from .models import stock_in
admin.site.register(item_inventory)
admin.site.register(stock_out)
admin.site.register(stock_in)
admin.site.register(purchase_item)



#-------income expense-----
from .models import income
from .models import income_details
from .models import sales_details
from .models import expense
from .models import purchase_details
from .models import bills_details
from .models import salary_details
admin.site.register(income)
admin.site.register(income_details)
admin.site.register(sales_details)
admin.site.register(expense)
admin.site.register(purchase_details)
admin.site.register(bills_details)
admin.site.register(salary_details)

# Register your models here.
'''