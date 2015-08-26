from django.shortcuts import render
from django.http import HttpResponse
import json
import MySQLdb
import imaplib
import email
import time

def handle(request):
   ctr = 0
   obj = []
   try:
      print "INSIDE"
      while 1:
         if ctr==4:
            break
         ctr  = ctr+1

         time.sleep(5)

         def process_mailbox(M):
            flag = 0
            print "Try"
            rv, data = M.search(None, "(UNSEEN)")
            if rv!="OK":
               pass
            for num in data[0].split():
               rv, data = M.fetch(num, '(RFC822)') 
               if rv!="OK":
                  pass

               msg = email.message_from_string(data[0][1]) 
               ID = str(msg['Subject'])   
               print ID

               db = MySQLdb.connect("localhost","root","root","dustbin")

               cursor = db.cursor()

               sql = """SELECT * FROM data where id=%s"""%(str(ID))

               print sql
              
               cursor.execute(sql)
               results = cursor.fetchall()
               for row in results:
                  lat = row[1]
                  long = row[2]
                  print lat + " " + long


               db.close()

               obj.append("\"Latitude\":" + str(lat) + ",\"Longitude\":" + str(long))

         M = imaplib.IMAP4_SSL('imap.gmail.com')

         username = "smartdustbinserver"
         password = "coderhardware"

         try:
            M.login(username, password)
            print "Logging in."
            rv, mailboxes = M.list() 
            rv, data = M.select("INBOX") 
            if rv == "OK":
               process_mailbox(M)
               M.close()
            M.logout()
         except imaplib.IMAP4.error:
            pass      

   except:
      pass

   return render(request,'display.html',{"coordinates": obj})
