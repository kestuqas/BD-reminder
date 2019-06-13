This is a birtday reminder app, sending e-mail messages to recipients through Gmail server.

At the beginning, after typing "reminder" command in Cotrol Line Interface,
you should use option "--data_file" after which you should indicate the path to you data file.
The app checks then if your data file is correct and throws error messages in case it finds some.

Your data file should be a CSV file with 'name surname(optional),e-mail address,birthdate" format.
Birthdays should be in the YY-MM-DD or MM-DD format.

If you're happy with your data file, after option "--data_file" you may try option "--send_reminders",
after which you should type "True".

But first set-up your e-mail address and password in the "Settings.txt" file.

The reminders will be sent to all e-mail addresses in the data file except those, which birthday is in 7 days.
