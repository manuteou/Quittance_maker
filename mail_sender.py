import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tablesdb import Tenant, Sql_database
import json
import os

class send_mail:
    def __init__(self, body, sender_email, password, receiver_email, smtp, port, path):
        self.body = body
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.path = path
        self.password = password
        self.smtp = smtp
        self.port = port

    def send(self):
        msg = MIMEMultipart()
        msg['Subject'] = '[Quittance de loyer]'
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        msgText = MIMEText('<b>%s</b>' % (self.body), 'html')
        msg.attach(msgText)

        filename = "message.txt"
        msg.attach(MIMEText(open(filename).read()))

        pdf = MIMEApplication(open(self.path, 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment', filename=self.body + ".pdf")
        msg.attach(pdf)

        try:
            with smtplib.SMTP(self.smtp, self.port) as smtpObj:
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(self.sender_email, self.password)
                smtpObj.sendmail(self.sender_email, self.receiver_email, msg.as_string())
                print("mail send at:", self.receiver_email)
        except Exception as e:
            print(e)


if __name__ == "__main__":

    database = Sql_database()

    directory = os.path.dirname(__file__)
    years = "2021"
    month = "02"
    with open('config.json','r') as json_files:
        config = json.load(json_files)
    for elt in database.pdf_table():
        nom, prenom, adresse, ville, sci, loyer, charges = elt
        path = os.path.join(directory, 'sci' + "\\" + years + "\\" + month + "\\") + "nom" + ".pdf"
        mail = send_mail("Quittance", config["master_mail"], config["password"], "mail", path)
        mail.send()

