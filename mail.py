from bs4 import BeautifulSoup
import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('bspam6969@gmail.com', 'Planes123')  # FILL PW IN
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox")  # connect to inbox.
subject = "You've got money"

# result, data = mail.search(None, '(UNSEEN SUBJECT "%s")'.format(subject))
result, data = mail.search(None, 'ALL')

ids = data[0]  # data is a list, each list item should include an email

id_list = ids.split()  # ids is a space separated string
latest_email_id = id_list[-1]  # get the latest

result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

raw_email = data[0][1]  # here's the body, which is raw text of the whole email
# including headers and alternate payloads

soup = BeautifulSoup(raw_email, 'html.parser')

print(raw_email)
# print(soup.get_text())

# Write email to file for checking.
with open('email.txt', 'w') as file:
    a = soup.prettify(encoding=None)
    # print(soup.prettify(encoding=None))
    file.write(str(raw_email))