# -*- coding: utf-8 -*-

from jobapp import *
myvalues = ['first', 'mid', 'last', '0403@em.edu', '00010351', 'skills']
fileUploadName = '0-Model.pdf'
thejobid = '29442'
newjob = jobApp(thejobid)
newjob.autoMechanize(myvalues, fileUploadName, 'blah2.html')
# br.retrieve('http','l‌​oans.csv')[0]
# newjob.setMechanizeFormValues(myvalues)
# submitresponse = newjob.submitMechanizeForm()
# br.form.add_file(open(fileUploadName), 'application/pdf', fileUploadName, name='Skin$body$txtFileContents')
