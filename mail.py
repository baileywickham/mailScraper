from bs4 import BeautifulSoup
import imaplib
import requests
import MySQLdb
import plivo  # Text message api

# For both the mysql login and email login we should create another untracked
# file that has a class which import password. like password.db instead of
# putting text straight in. That way we can safely put it on github.
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="",
    db="nahns_sourcebans")
cur = db.cursor()


def main():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('bspam6969@gmail.com', 'Planes123')  # FILL PW IN
    mail.list()
    mail.select("inbox")  # connect to inbox.

    # subject = "You've got money"
    # result, data = mail.search(None, '(UNSEEN SUBJECT "%s")'.format(subject))
    result, data = mail.search(None, 'ALL')
    ids = data[0]  # data is a list, each list item should include an email
    id_list = ids.split()  # ids is a space separated string

    # This scrapes all mail, later it will only scrape unread paypal emails.
    # Later, we must make sure that he doesn't open any paypal emails before
    # they get scraped, also check if this reads them or no.

    # this will be community.steam...
    # TODO THIS IS THE START OF THE STRING TO SEARCH IN FINDSTEAMNAME
    findCommunity = ""
    findMoney = '$'  # Definitely needs to be tested, a lot.
    for id in id_list:
        _, data = mail.fetch(id, "RFC822")
        steamName = findSteamName(data[0][1], findCommunity)
        moneyPaid = findSteamName(data[0][1], findMoney)

	steamid = getMoreInfo(steamName) # I'm not sure if steamName is alias or url
	sqlData = sqlGetUser(steamid)  # I need to do something with getMoreInfo before I can use this
    	for row in sqlData:
        	if row[3] == 1 and row[4] == 1 and moneyPaid == '$10.00':  # Unban and vip
        		sqlUnban(alias, steamid)
	                sqlVip(alias, steamid)
        	elif row[3] == 1 and moneyPaid == '$5.00':  # If set for unban
                	sqlUnban(alias, steamid)
	        elif row[4] == 1 and moneyPaid == '$5.00': # If set for vip
        	        sqlVip(alias, steamid)
		else:
			# do logging here, i don't think texts are nessacary. Users will probably report the error before we can get to it anyway. Writing to a log file should be sufficent


def findSteamName(raw_email, searchString):
    start = str(raw_email).find(searchString)
    new = str(raw_email)[start:]
    end = new.find('=20')
    return (new[:end])
    # This now grabs text from the email. This may be
    # the most sketchy piece of code I have ever written.
    # Not even I understand how this works.


def getMoreInfo(steamUrl):
    url = 'https://steamid.xyz/' + steamUrl
    r = requests.get(url)
    toScrape = str(r.text)
    start = toScrape.find('STEAM_0')
    new = toScrape[start:]
    end = new.find()  # TODO, figure out how this ends. BAILEY: It's worth noting these are of a length n, so it can't be hardcoded
    return new[:end]

    # Might not use bs4 might use string lookups instead.
    # Also not sure what to do with this info.


def sqlGetUser(steamid):
    query = "SELECT * from nahns_store WHERE steamid='%s'" % (steamid)
    cur.execute(query)

    return cur.fetchall()


def sqlVip(alias, steamid):
    query = "INSERT INTO sb_admins (aid, user, authid, password, gid, email, validate, extraflags, immunity, srv_group, srv_flags, srv_password, lastvisit) VALUES ('99', '%s', '%s', '', '1', '', '', '', '0', 'VIP [HNS]', '', '', '0');" % (alias, authid)

    cur.execute(query)


def sqlUnban(alias, steamid):
    query = "UPDATE sb_bans SET RemovedBy = '0', RemoveType = 'U', RemovedOn = UNIX_TIMESTAMP(), ureason = 'Unbanned at community.edan.pw/store/' WHERE authid = '%s' OR name = '%s'" % (authid, alias)

    cur.execute(query)


def unbanFromServer():
    pass
    # this is the main unban part, it should call the other unban functions.
    # I'm not sure this is nessacary. sqlUnban will handle the unban entirely, unless you wanted to send an email or something

if __name__ == '__main__':
    main()
    # TODO: from username, decide how we want to add to db.
    # Possibly run as cron job.
db.close()
