#This can send upto 1000 messages per day using this id. Use this email id and no other.
#restart every hour or so if the execution stops

import smtplib, os, os.path, shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64


#folder created after part one make sure to have only required folders in this folder
inputFolder = "D:\\DoPy\\result"

#make sure you create an empty folder and input the path here"
#the folder needs to be empty only for the first time
#after that it will contain all the files that were already sent
#this way if the code execution stops, you can just rerun the code without any changes
extraFolder = "D:\\DoPy\\sent"

#defining the constants
fromAddress = "deaprtment.photography2@gmail.com"
password = "jeahUHzuk00"
body = "Hi,\n\nPlease find your DoPy snaps from last semester attached to this mail.\n\nIf you have already received a few mails, we apologize. We are still removing the kinks from the new software.\n\nWe are very sorry for flooding your inbox. These are the final pictures."
body = body + "\n\nRegards\nThe Department Of Photography"

#creating the smtp server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(fromAddress, password)


for folder in os.listdir(inputFolder):
    #creating a message and adding the common attributes (eg: sender, subject, etc)
    msg = MIMEMultipart()
    msg['Subject'] = "DoPy Pictures From Second Semester 2015-2016"
    msg['From'] = fromAddress

    #create a list of all the files in the folder
    attachments = [os.path.join(inputFolder, folder, f) for f in os.listdir(os.path.join(inputFolder, folder))]

    #generate email address from foldername
    #13121 ==> f2013121@pil...
    #M14059 ==> h2014059@pil...
    #P14060 ==> p14060@pil... (Not Sure)
    if folder.startswith('M') or folder.startswith('m'):
        email = "h20%s@pilani.bits-pilani.ac.in" % folder[1:]
    elif folder.startswith('P') or folder.startswith('p'):
        email = "p20%s@pilani.bits-pilani.ac.in" % folder[1:]
    else:
        email = "f20%s@pilani.bits-pilani.ac.in" % folder

    msg['To'] = email
    msg.attach(MIMEText(body))

    if len(attachments) <= 100:
        for file in attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, 'rb').read())
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename="%s" % os.path.basename(file))
            msg.attach(part)

        server.sendmail(fromAddress, email, msg.as_string())

        #shift the sent files from input folder to extrafolder
        for file in attachments:
            if not os.path.exists(os.path.join(extraFolder, folder)):
                os.mkdir(os.path.join(extraFolder, folder))
            shutil.copy(file, os.path.join(extraFolder, folder))

        #remove the folder and all its contents from input dir
        shutil.rmtree(os.path.join(inputFolder, folder))

        #print the name of the folder as log
        print(folder)

#close the server
server.close()