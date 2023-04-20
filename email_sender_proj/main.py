import smtplib
import os
import tkinter as Tk
from tkinter import ttk





def send_email(message:str) -> None:
    '''
    This function sends an email to the recipient on gmail
    :param message:
    
    If you have a problem with sending the email,
    check this out:
    https://www.howto-outlook.com/howto/gmailoauth.htm
    '''
    sender = 'YOUR GMAIL'
    password = 'YOUR_APP_PASSWORD'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    try:
        server.login(sender, password)
        server.sendmail(sender, 'dergonter456@gmail.com', message)
        
        return 'Email sent successfully!'
    except Exception as _ex:
        return f'{_ex}\n check your password or login! '


    
    


if __name__ == '__main__':
    message = input('enter your message: ')
    send_email(message=message)
    
