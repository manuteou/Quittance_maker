import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json
import os

class send_mail:
    def __init__(self, body, sender_email, password, receiver_email, path):
        self.body = body
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.path = path
        self.password = password

    def send(self):
        msg = MIMEMultipart()
        msg['Subject'] = '[Email Test]'
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email

        msgText = MIMEText('<b>%s</b>' % (self.body), 'html')
        msg.attach(msgText)

        filename = "example.txt"
        msg.attach(MIMEText(open(filename).read()))

        pdf = MIMEApplication(open(self.path, 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment', filename="example.pdf")
        msg.attach(pdf)

        try:
            with smtplib.SMTP('smtp.free.fr', 587) as smtpObj:
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(self.sender_email, self.password)
                smtpObj.sendmail(self.sender_email, self.receiver_email, msg.as_string())
        except Exception as e:
            print(e)


if __name__ == "__main__":

    directory = os.path.dirname(__file__)
    years = "2021"
    month = "02"

    with open("config.json") as json_file:
        config = json.load(json_file)

    with open("locataire.txt") as json_file:
        locataire = json.load(json_file)
        path = os.path.join(directory, locataire['sci'] + "\\" + years + "\\" + month + "\\") + locataire["nom"] + ".pdf"
        mail = send_mail("Quittance", config["master_mail"], config["password"], locataire["mail"], path)
        mail.send()