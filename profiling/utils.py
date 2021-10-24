from datetime import datetime, timedelta
from calendar import HTMLCalendar
#from .models import Event
from .models import available_schedules
from .models import appointment_details
from io import BytesIO
from .models import *

from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa  

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, apps):
		#events_per_day = events.filter(start_time__day=day)
		pklist = []
		scheds = available_schedules.objects.filter(date__day = day)
		for i in scheds:
			pklist.append(i.id)

		#apps_per_day = apps.filter(schedule_id__in = pklist)
		apps_per_day = apps.filter(schedule_id__in = pklist).exclude(payment_status = 'Paid')
		# kani final apps = appointment_details.objects.filter(schedule_id__in = pklist).exclude(appointment_status = 'Cancelled').exclude(payment_status = 'Paid')



		d = ''
		for apps in apps_per_day:
			d += f'<li> {apps.get_html_url}</li>' 

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, apps):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, apps)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		#events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)
		pklist=[]
		sched = available_schedules.objects.filter(date__year = self.year, date__month = self.month)
		for i in sched:
			pklist.append(i.id)
		#apps = appointment_details.objects.filter(schedule_id__in = pklist)
		apps = appointment_details.objects.filter(schedule_id__in = pklist).exclude(payment_status = 'Paid')
		# kani final apps = appointment_details.objects.filter(schedule_id__in = pklist).exclude(appointment_status = 'Cancelled').exclude(payment_status = 'Paid')


		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, apps)}\n'
		return cal

def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
 
     #This part will create the pdf.
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None
