import urllib
import urllib2
import cookielib
import re
import socket
import smtplib
import MySQLdb

def change_domain_ip_public(my_public_ip):
    return_value=False
    username ='imelda'
    password ='anderdok'


    cj= cookielib.CookieJar()
    opener_domain = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener_domain)

    auth_url ='http://apikesimelda.ac.id:2082/login'

    payload ={'user':username,'pass':password}


    login_data = urllib.urlencode(payload)
    login_request = urllib2.Request(auth_url,login_data)

    response = urllib2.urlopen(login_request)

    response_url= response.geturl()

    get_frontresponse_url = response_url[:-56]


    for line in range(41,43):
        part_json_url='json-api/cpanel?cpanel_jsonapi_version=2&cpanel_jsonapi_module=ZoneEdit&cpanel_jsonapi_func=edit_zone_record&domain=apikesimelda.ac.id&line='+str(line)+'&class=IN&type=A&name=siakad.apikesimelda.ac.id.&ttl=14400&address='
        url_req_zoneedit_ip =get_frontresponse_url+part_json_url+my_public_ip
        post_edit_ip = urllib2.urlopen(url_req_zoneedit_ip)
        if post_edit_ip.getcode()=='200':
            return_value=True

def check_ip_in_database(my_ip_public):
    returnval = False
    host='localhost'
    user='root'
    password='rooting'
    database='db_ip_public'
    #open connection
    connection = MySQLdb.connect(host,user,password,database)
    obj_cursor= connection.cursor()

    query ='select iptable from table_ip_public where iptable ="%s"'%(my_ip_public)
    obj_cursor.execute(query)
    results=obj_cursor.fetchone()
    if not results:
        insert_query ="insert into table_ip_public (iptable) values ('%s')"%(my_ip_public)
        obj_cursor.execute(insert_query)
        connection.commit()
        returnval=True
    return returnval
    connection.close()

def is_connected():
    try:
        my_public_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
        return my_public_ip
    except:
        pass
    return 0

def send_email(my_public_ip):
    fromaddr='bosbasri111@gmail.com '
    toaddrs='muhammadbasri444@gmail.com'
    msg = "\r\n".join(["From: bosbasri111@gmail.com ",
                       "To: muhammadbasri444@gmail.com",
                       "Subject: Perubahan Ip Public",
                       "",
                       "Terjadi Perubahan ip public = "+my_public_ip])
    username = 'bosbasri111@gmail.com '
    password = 'basri1198corse'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

if is_connected()!=0:
    ip_public= is_connected()
    checking=check_ip_in_database(ip_public)
    if checking:
        send_email(ip_public)
        execute_ip_public=change_domain_ip_public(ip_public)
    #if execute_ip_public:
    #    print "berhasil"
    





