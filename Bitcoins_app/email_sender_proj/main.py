import smtplib
import os
from email.mime.text import MIMEText


def send_email(message):
    '''
    This function sends an email to the recipient on gmail
    :param message:
    
    If you have a problem with sending the email,
    check this out:
    https://www.howto-outlook.com/howto/gmailoauth.htm
    '''
    sender = 'YOUR GMAIL'
    password = 'YOUR PASSWORD'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    try:
        server.login(sender, password)
        server.sendmail(sender, 'RECIPIENT', message)
        
        return 'Email sent successfully!'
    except Exception as _ex:
        return f'{_ex}\n check your password or login! '

def main():
    message = input('Enter message: ')
    print(send_email(message=message))
    
    


if __name__ == '__main__':
    main()