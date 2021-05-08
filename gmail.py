import yagmail
def send(recipient, subject, contents):
    yag = yagmail.SMTP("wlucoursefull@gmail.com")
    yag.send(to = recipient, subject = subject, contents = contents)
