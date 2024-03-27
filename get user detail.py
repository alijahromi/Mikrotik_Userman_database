#You need this library
import time
from persiantools.jdatetime import JalaliDate
from datetime import datetime
import sqlite3
import paramiko
import os

username = input('Enter Username: ')

#This function convert usage from Byte to Giga Byte
def gig(adad):
    a = adad / (10**9)
    a = int(a)
    a = str(a) + ' G'
    return (a)
#This is main function
def process(user):
    #first you need to connect to your routerboard with ssh
    hostname = '10.10.10.10'
    port = 22
    username = 'your user name'
    password = 'your password'
    #and download database file
    remote_filepath = '/user-manager/sqldb'
    local_filepath = 'localfilepath'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)
    sftp = ssh.open_sftp()
    sftp.get(remote_filepath, local_filepath)
    sftp.close()
    ssh.close()
    #Then connect to sqlite database file
    con = sqlite3.connect(local_filepath)
    cur = con.cursor()
    userb = str.encode(user)
    #Here you can add or remove witch data you want
    command = '''select username, actualProfileName, downloadused,
      uploadused, activesessions, profileTillTime
        from user Where username=?'''
    find_user = cur.execute(command, (userb,))
    #This put all data in a list for use
    detail = find_user.fetchone()
    cur.close()
    con.close()
    #Use this command to remove db file if you want to run this program again
    os.remove(local_filepath)
    usr = user
    Profile = detail[1]
    if Profile == None:
        Profile = '-'
    else:
        Profile = Profile.decode()
    till = detail[5]
    if till == -1:
        till = 'Unlimited'
    elif till == -2:
        till = '-'
    else:
        till = datetime.utcfromtimestamp(till)
        till = JalaliDate(till)
        till = till.strftime("%Y/%m/%d")
    dow = gig(detail[2])
    up = gig(detail[3])
    active = detail[4]
    
    
    result = {
            'Username:': usr,
            'Profile:': Profile,
            'Till Time:': till,
            'Download:': dow,
            'Upload:': up,
            'Connections:': active
        }
    return result


process(username)