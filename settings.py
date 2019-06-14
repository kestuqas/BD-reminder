SENDER = 'Administrator'
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
reminder_days = 7 # Days to remind before the birthdate
trials = 3 # Number of trials to send the reminder
SMTP = {'host': 'smtp.gmail.com', 
	    'port': 465, 
	    'ssl': True, 
	    'user': EMAIL_ADDRESS, 
	    'password': EMAIL_PASSWORD}
