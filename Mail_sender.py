import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_test_mail(body):
    sender_email = "mail"
    receiver_email = "mail"

    msg = MIMEMultipart()
    msg['Subject'] = '[Email Test]'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msgText = MIMEText('<b>%s</b>' % (body), 'html')
    msg.attach(msgText)

    filename = "example.txt"
    msg.attach(MIMEText(open(filename).read()))

    # with open('example.jpg', 'rb') as fp:
    #     img = MIMEImage(fp.read())
    #     img.add_header('Content-Disposition', 'attachment', filename="example.jpg")
    #     msg.attach(img)

    pdf = MIMEApplication(open("2021/01/babu_lulu.pdf", 'rb').read())
    pdf.add_header('Content-Disposition', 'attachment', filename="example.pdf")
    msg.attach(pdf)

    try:
        with smtplib.SMTP('smtp.free.fr', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("mail", "pw")
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(e)

send_test_mail("Quittance")