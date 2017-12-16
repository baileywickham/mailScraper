from bs4 import BeautifulSoup
import imaplib
import requests
# print(raw_email)
# print(soup.get_text())

# Write email to file for checking.
# with open('email.txt', 'w') as file:
#    a = soup.prettify(encoding=None)
#    print(soup.prettify(encoding=None))
#    file.write(str(raw_email))

def main():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('bspam6969@gmail.com', 'Planes123')  # FILL PW IN
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox")  # connect to inbox.
    # subject = "You've got money"

    # result, data = mail.search(None, '(UNSEEN SUBJECT "%s")'.format(subject))
    result, data = mail.search(None, 'ALL')

    ids = data[0]  # data is a list, each list item should include an email

    id_list = ids.split()  # ids is a space separated string

    # This scrapes all mail, later it will only scrape unread paypal emails.
    # Later, we must make sure that he doesn't open any paypal emails before 
    # they get scraped, also check if this reads them or no.
    for id in id_list:
        _, data = mail.fetch(id, "RFC822")
        findSteamName(data[0][1])


def findSteamName(raw_email):
    searchString = 'yes' # this will be http://community.steam...
    start = str(raw_email).find(searchString)
    new = str(raw_email)[start:]
    end = new.find('=20')
    print(new[:end])
    # This grabs the url from the email, I used your 1 cent email
    # as a test so that is the search string in this case


def getMoreInfo(steamUrl):
    url = 'https://steamid.xyz/' + steamUrl
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser') 

    # Might not use bs4 might use string lookups instead. 
    # Also not sure what to do with this info. 

if __name__ == '__main__':
    main()
    # TODO: from username, decide how we want to add to db. 
    # Possibly run as cron job. 