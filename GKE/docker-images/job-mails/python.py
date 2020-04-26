import smtplib

text = "Hello Fasionista " + "\n\n" +  \
"We are sending a massive surprise your way, in no time. Stay tuned!"

sender = "spikeysales@loonycorn.com"
password = "JonSnow2018"

customer_emails = ['yase@loonycorn.com', 'amit.pandit@loonycorn.com', 'judy@loonycorn.com', 'ubaid.qureshi@loonycorn.com']

server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
server.login(sender,password)

for email in  customer_emails:
	server.sendmail(sender, email, text)
	
server.quit()