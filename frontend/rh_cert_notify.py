#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2018, Abnerson Malivert <amaliver@redhat.com>
# import libraries
import requests
import pandas as pd
import numpy as np
import smtplib
import re
import ssl
import ldap

from email.message import EmailMessage

"""
Email function for one recipient
recipient is one email
Password for redhat account will be standard input for the time being
Execute with email_recipient("example@company.com")
"""
def get_info(lists_len,dfs):
    data_table = []
    x = 0
    while x < lists_len:
        list_data = dfs[1].iloc[x][0]
        split_data = re.split('Date:|Current|Until:|Technologies|Used:', str(list_data))
        exam_name = split_data[0]
        exam_date = split_data[1]
        exam_ex_date = split_data[3]
        tech_used = split_data[5]
        data_table.append([exam_name,tech_used,exam_date,exam_ex_date])
        x += 3
    return data_table 

def get_owner_name(dfs):
    owner_info = dfs[0].iloc[1][0] + ' ' + dfs[0].iloc[1][1]
    return owner_info


def get_owner_info(owner):
    ldap_server = ldap.initialize('ldap://ldap.corp.redhat.com')
    ldap_server.simple_bind('dc=redhat,dc=com')
    search_result = ldap_server.search("dc=redhat,dc=com", ldap.SCOPE_SUBTREE, "cn=%s" % owner)
    ldap_server.set_option(ldap.OPT_REFERRALS, 0)
    result_type, result_data = ldap_server.result(search_result, 0)
    email = [ sub['mail'] for sub in result_data ]
    print(str(email))

def send_email(recipient):
    sender = "rhemailnotifier@gmail.com"
    msg = EmailMessage()

    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = "Expiring certification"

    msg.set_content("Hello")

    s = smtplib.SMTP("smtp.gmail.com")
    s.starttls()
    s.login("rhemailnotifier@gmail.com", input("Sender password: "))
    s.sendmail(sender, recipient, msg.as_string())
    s.quit()

def  main():
    # specify the url
    src_url = 'https://www.redhat.com/rhtapps/services/verify?certId=140-177-544'
    dfs = pd.read_html(src_url)
    owner = get_owner_name(dfs)
    # owner_info = dfs[0].iloc[1][0] + ' ' + dfs[0].iloc[1][1]
    # print(owner_info)
    list_len = len(dfs[1]) - 3
    result = get_info(list_len,dfs)
    #print(result)

if __name__ == "__main__":
    main()
