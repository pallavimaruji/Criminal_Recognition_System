import smtplib
content="Success"
mail=smtplib.SMTP('smtp.gmail.com',587)
mail.ehlo()
mail.starttls()
mail.login('nakulswims@gmail.com','bajrangbali1')
mail.sendmail('nakulswims@gmail.com','pallaviagarwal8696@gmail.com',content)
mail.close()

