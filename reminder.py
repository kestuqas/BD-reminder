import click
from datetime import datetime, date, timedelta

@click.command(help="This is a birtday reminder app.\n\
	This app checks if your data file is correct and throws an error message in case it finds some.\n\
	Your data file should be a CSV file with 'name','e-mail address','birthdate' format.\n\
	Birthdays should be in the YY-MM-DD or MM-DD format.\n\
	The reminders will be sent to all e-mail addresses in the data file except those, which birthday is in 7 days.")

@click.option('--data_file',
			  help="Use this option to set the data file path.")

@click.option('--send_reminders', default=False,
			  help="Use this option and type 'True' to send reminders.")

def validate_send(data_file, send_reminders=False):

	target_date = date.today() + timedelta(days=7) # Set reminder days before birthday
	bd_people= [] # List of "Birthday" people
	skip_lines = [] # List of incorrect data lines

	with open(data_file, 'r') as d_file: # Read the data file, create data list
		data = d_file.read().splitlines()
		data = [line.split(',') for line in data]

	for index, line in enumerate(data):
		
		if (len(line) < 3): # Cheking if data lines are complete
			print("The line {} of data file is incomplete.".format(index+1))
			skip_lines.append(index)
		else:
			try:
				b_date = datetime.strptime(line[2], '%Y-%m-%d') # Check if birthdate format is YY-MM-DD
				if b_date > datetime.now(): # Check if birthdate is not a future date
					print("The line {} of data file contains future date.".format(index+1))
					skip_lines.append(index)
			except (ValueError, IndexError):
				
				try:
					b_date = datetime.strptime(line[2], '%m-%d') # Check if birthdate format is MM-DD
				except (ValueError, IndexError):
					print("The line {} of data file has incorrect date.".format(index+1))
					skip_lines.append(index)

			if send_reminders and index not in skip_lines:
				# Check if birthdate is in period of target_date (7 days initialy)
				if b_date.month == target_date.month and b_date.day == target_date.day:
					bd_people.append(index)

	# Generate reminder e-mails
	if send_reminders:

		import smtplib
		from email.message import EmailMessage
		from emails.template import JinjaTemplate as T

		EMAIL_ADDRESS = 'k.reimeris@gmail.com'
		EMAIL_PASSWORD = 'uacq zmfg snrs syys'

		for happy in bd_people:
			for index, item in enumerate(data):
				if index not in skip_lines and index not in bd_people:
					msg = EmailMessage()
					msg['From'] = EMAIL_ADDRESS
					msg['To'] = '{}'.format(item[1])
					msg['Subject'] = "Birthday Reminder: {}'s birthday on {}".format(data[happy][0], data[happy][2])
					msg.set_content('Hi {},\n\nThis is a reminder that {} will be celebrating their\n\
birthday on {}'.format(item[0], data[happy][0], data[happy][2]))

					server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
					server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
					server.send_message(msg)
					server.quit()

# validate_send(data_file, True)

