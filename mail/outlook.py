import win32com.client as win32

subject = '''Hi {toName},

I'm Ajay Thomas, a Master’s student of Computer Science at the University of Wisconsin-Madison. I am interested in software engineering internship opportunities at {companyName} for Summer 2017. I am hoping that you can help connect my profile with the right person internally.

The following is a glimpse of my profile:
Worked on McAfee’s (Intel Security) Data Analytics platforms (Telemetry and NORAD) comprising of various Big Data technologies like Storm, Splunk etc. for about three years in India.
I have experience in both back-end and client side development. I enjoy programming and have a couple of personal projects.
Please find my resume attached.

Thanks and Regards,
Ajay Thomas
'''.format(toName = 'ajay', companyName = 'IOTech')

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'ajosephthoma@wisc.edu'

mail.Subject = 'Application for Software Engineer Intern 2017'
mail.body = subject
attachment1 = "C:\\Users\\ajayt\\Dropbox\\USA\\internship\\final\\AjayJosephThomas_Resume.pdf"
mail.Attachments.Add(attachment1)
mail.send