# https://studentemployment.umich.edu/JobX_Apply.aspx?JobId=
# 29415

# from bs4 import BeautifulSoup
import mechanize
import jobapp_settings
# import requests
# from pprint import pprint as pp
# 29442
# '0-Model.pdf'

# br = mechanize.Browser()
# br.set_handle_robots(False)
# br.addheaders = [('User-agent', 'Chrome')]

# self.submiturl = "https://studentemployment.umich.edu/JobX_Apply.aspx?JobId="
# jobid = '29442'
# br.open(self.submiturl + jobid)
# br.select_form('aspnetForm')

# r = requests.get(rootself.submiturl+jobid)
# soup = BeautifulSoup(r.text)
# soupform = soup.select('form')[1]
# soupform.findAll('input')
# soupform.findAll('input')[1:6]
# textcontrols = [intag['name'] for intag in soupform.findAll('input')[1:6]]
# soupform.find('textarea')
# soupform.find('textarea')['name']


class jobApp:
    def __init__(self, jobid='0'):
        self.jobid = jobid
        self.resumeLink = jobapp_settings.resumeLink
        self.baseurl = jobapp_settings.baseurl
        self.submiturl = jobapp_settings.submiturl
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [('User-agent', 'Chrome')]
        self.br.open(self.submiturl+self.jobid)

    def setMechanizeFormValues(self, textList):
        self.br.select_form('aspnetForm')
        fctrls = [t.name for t in self.br.form.controls]
        for index, setVal in enumerate(textList):
            self.br.form[fctrls[index+1]] = setVal
            print "controls: %s  value: %s" % (self.br.form.controls[index+1],
                                               self.br.form[fctrls[index+1]])

    def setMechanizeFileUpload(self, uploadFilename):
        self.br.form.add_file(open(uploadFilename),
                              'application/pdf', uploadFilename,
                              name='Skin$body$txtFileContents')

    def submitMechanizeForm(self):
        return self.br.submit()

    def getMechanizeResumeSubmit(self):
        thelink = [link for link in self.br.links()][-1]
        self.resumeLink = self.baseurl + thelink.url
        return thelink

    def autoMechanize(self, textList, uploadFilename, debughtml='blah.html'):
        self.setMechanizeFormValues(textList)
        self.setMechanizeFileUpload(uploadFilename)
        resp = self.submitMechanizeForm()
        print "\nReceipt URL: %s\n" % resp.geturl()
        print "\nReturn Info: %s\n" % resp.info()
        with open(debughtml, 'w') as f:
            f.write(resp.read())
        self.br.open(resp.geturl())
        resumeResp = self.br.follow_link(self.getMechanizeResumeSubmit())
        print "Resume URL: %s" % self.resumeLink
        rupload = resumeResp.info()['content-disposition'].split('=')[-1]
        print "Resume Upload Name: %s" % rupload


    # def getForm(self, ji):
    #     self.jobid = ji
    #     r = requests.get(self.submiturl+self.jobid)
    #     sp = BeautifulSoup(r.text)
    #     sform = sp.select('form')[1]
    #     infield = [t['name'] for t in sform.findAll('input')[1:6]]
    #     infield.append(sform.find('textarea')['name'])
    #     self.firstname['sel'] = infield[0]
    #     self.middlename['sel'] = infield[1]
    #     self.lastname['sel'] = infield[2]
    #     self.email['sel'] = infield[3]
    #     self.umid['sel'] = infield[4]
    #     self.skills['sel'] = infield[5]

    # def setValues(self, textList):
    #     self.firstname['value'] = textList[0]
    #     self.middlename['value'] = textList[1]
    #     self.lastname['value'] = textList[2]
    #     self.email['value'] = textList[3]
    #     self.umid['value'] = textList[4]
    #     self.skills['value'] = textList[5]


    # def setFileUpload(self, fileupload):
    #     self.resume = {'file': open(fileupload, 'rb')}
    #     # r = requests.post(url, files=files)

    # def buildPayload(self):
    #     payloadList = [self.firstname, self.middlename,
    #         self.lastname, self.email, self.umid, self.skills]
    #     self.payload = dict([(p['sel'], p['value']) for p in payloadList])

    # def postPayload(self):
    #         r = requests.post(self.submiturl+self.jobid,
                              # data=self.payload, files=self.resume)
    #         pp(r.text)
    #         return r
        # soupform.find('textarea')['name']
        # , firstname=, middlename=, lastname=,
        #                 email=, umid=, skills=, resume=
        # self.firstname = firstname
        # self.middlename = middlename
        # self.lastname = lastname
        # self.email = email
        # self.umid = umid
        # self.skills = skills
        # self.resume = resume



# def __main__():
#     pass
    # from jobapp import *
    # myvalues = ['first', 'mid', 'last', 'em@em.edu', 'umid', 'skills']
    # fileUploadName = '0-Model.pdf'
    # thejobid = '29442
    # newjob = jobApp(thejobid)
    # newjob.setMechanizeFormValues(myvalues)
    # newjob.getForm('29442')
    # newjob.setFileUpload(fileUploadName)
    # newjob.setValues(myvalues)
    # newjob.buildPayload()
    # print "built payload"
    # pp(newjob.payload)
    # req = newjob.postPayload()

# firstname, middlename, lastname, email, umid, skills, resume

# for control in br.form.controls:
#     print control
#     print "type=%s, name=%s value=%s" % (control.type,
                                         # control.name,
                                         # br[control.name])


# files = {'file': open(fileupload, 'rb')}
# r = requests.post(url, files=files)
# myvalues = ['first', 'mid', 'last', 'em', 'umid', 'skills']
# newjob.getForm('29442')
# newjob.setFileUpload('0-Model.pdf')
# newjob.setValues(myvalues)
