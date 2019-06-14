import click
from datetime import datetime, date, timedelta
from settings import *
from extras import *


@click.command(help=COMMAND_HELP)
@click.option('--data_file', help=OPTION_DATA)
@click.option('--send_reminders', help=OPTION_SEND)
def validate_send(data_file, send_reminders=False):

	target_date = date.today() + timedelta(days=reminder_days) # Set reminder days before birthday
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

	if send_reminders: # Generate reminder e-mails

		import smtplib
		from email.message import EmailMessage
		import emails
		
		for happy in bd_people: # Iterate through birthday people
			for index, item in enumerate(data): # Iterate through whole list...
				if index not in skip_lines and index not in bd_people: # ... but skipping incorrect and "Birtday" ones
					
					msg = emails.Message(
						text=("Hi {},\n\nThis is a reminder that {} will be celebrating their\n\
birthday on {}.\n\nBe prepared :)\n{}".format(item[0], data[happy][0], data[happy][2], SENDER)),
						subject=("Birthday Reminder: {}'s birthday on {}".format(data[happy][0], data[happy][2])),
						mail_from=(SENDER, EMAIL_ADDRESS))
					
					# Logic to make few trials (initially 3) if not sent
					failed = 0
					while failed < 3:
						response = msg.send(
							to=(item[0], '{}'.format(item[1])),
							smtp=SMTP)
						if response.status_code not in [250]:
							if failed == 2: # Failed to send 3 times
								print("Reminder to {} was not sent".format(item[0])) 
							failed += 1
						else:
							failed = 3
