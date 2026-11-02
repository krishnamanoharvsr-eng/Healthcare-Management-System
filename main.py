import mysql.connector
from tabulate import tabulate
#1-------------------------------------------------------------header--------------------------
print('''
+---------------------------------------+
|     Healthcare Management System      |
+---------------------------------------+
''')
#2-------------------------------------------------------------create necessary db----------------------------
mydb=mysql.connector.connect(host='localhost',user='root',passwd='root',database='myhms')
cursor=mydb.cursor()
#3-------------------------------connection status--------------------
def conncheck():
      if mydb.is_connected:
            print('Succesfully connected to host')
      else:
            print('Failed to connect to host')
conncheck()
#4-----------------------------------main menu--------------------------------------
def mainmenu():
    while True:
        print("1. Signup new patient")
        print("2. Login (Patient/Doctor/Admin)")
        print("3. Exit")
        print("===============================================")
        choice = input("Enter choice: ")
        print("===============================================")
        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Terminating.........")
            break
        else:
            print("Invalid choice, try again.")
#-5----------------------------------------sign up-----------------------------------
def signup():
      print('''
+-----------------+
|   SIGNUP PAGE   |
+-----------------+
for patients only''')
      try:
            uname_input = str(input('Enter your USERNAME:'))
            passwd_input = input('Enter your PASSWORD:')
            print()
            unamequery = f"SELECT * FROM doclogin WHERE uname = '{uname_input}'" 
            cursor.execute(unamequery)
            detail = cursor.fetchone()
            if detail != None:
                  print('Username ALREADY EXISTS')
                  signup()
                  print("===============================================")
            elif detail == None:
                  signupquery = f"INSERT INTO patlogin values('{uname_input}','{passwd_input}')"
                  cursor.execute(signupquery)
                  mydb.commit()
                  print('Signed up successfully!')
                  mainmenu()
                  print("===============================================")
      except Exception as e:
            print(f"Error: {e}")
#--6-----------------------------------------------login----------------------------
def login():
      print('''
+--------------+
|  LOGIN PAGE  |
+--------------+
''')
      print('Press 1 to login as PATIENT')
      print('Press 2 to login as DOCTOR')
      print('Press 3 to login as ADMINISTRATOR')
      print("===============================================")
      choice = str(input('Enter your choice: '))
      print("===============================================")
      if choice=='1':
            patlogin()
      elif choice=='2':
            doclogin()
      elif choice=='3':
            adminlogin()
      else:
            print('Invalid operation')
#logns----------------------------------------------
def patlogin():
            uname_input = str(input('Enter your USERNAME:'))
            passwd_input = input('Enter your PASSWORD:')
            unamequery = f"SELECT * FROM patlogin WHERE uname = '{uname_input}'" 
            cursor.execute(unamequery)
            detail = cursor.fetchone()
            if detail == None:
                  print('\nUsername NOT FOUND')                  
                  login()                
            elif detail[1] != passwd_input:
                  print('\nINCORRECT PASSWORD')
                  login()
            else:
                  print(f'\nLogged in..... \n\nWelcome {uname_input}...\n\n')
                  patmainmenu(uname_input)
def doclogin():
            uname_input = str(input('Enter your USERNAME:'))
            passwd_input = input('Enter your PASSWORD:')
            unamequery = f"SELECT * FROM doclogin WHERE uname = '{uname_input}'" 
            cursor.execute(unamequery)
            detail = cursor.fetchone()
            if detail == None:
                  print('\nUsername NOT FOUND')
                  login()
            elif detail[1] != passwd_input:
                  print('\nINCORRECT PASSWORD')
                  doclogin()
            else:
                  print(f'\nLogged in..... \n\nWelcome {uname_input}...\n\n')
                  docmainmenu(uname_input)
def adminlogin():
            uname_input = str(input('Enter your USERNAME:'))
            passwd_input = input('Enter your PASSWORD:')
            unamequery = f"SELECT * FROM adminlogin WHERE uname = '{uname_input}'" 
            cursor.execute(unamequery)
            detail = cursor.fetchone()
            if detail == None:
                  print('\nUsername NOT FOUND')                 
                  login()                  
            elif detail[1] != passwd_input:
                  print('\nINCORRECT PASSWORD')
                  adminlogin()
            else:
                  print(f'\nLogged in..... \n\nWelcome {uname_input}...\n\n')
                  adminmainmenu(uname_input)
#-7-----------------------------------pat main menu------------------------------------------------------------
def patmainmenu(uname_input):
    while True:
        print('''
+-------------------------+
|    PATIENT MAIN MENU    |
+-------------------------+
''')
        print("1. Create patient profile")
        print("2. View patient profile")
        print("3. Edit patient profile")
        print("4. Schedule an appointment")
        print("5. View appointments")
        print("6. Cancel appointment")
        print("7. Export prescription")
        print("8. Logout")
        print("===============================================")
        choice = input("Enter your choice: ")
        print("===============================================")
        if choice == "1":
            createprofile(uname_input)
        elif choice == "2":
            viewprofile(uname_input)
        elif choice == "3":
            editprofile(uname_input)
        elif choice == "4":
            makeappt(uname_input)
        elif choice == "5":
            viewapptpat(uname_input)
        elif choice == "6":
            delappt(uname_input)
        elif choice == "7":
            date = input('enter date of prescription')
            export_pcptn(uname_input,date)            #idk do this after export fxn
        elif choice == "8":
            print("Logging out...")
            break
        else:
            print("Invalid choice, try again.")
#--8--------------------------------doc main menu-------------------------------------------------------------------
def docmainmenu(uname_input):
    while True:
        print('''
+-------------------------+
|    DOCTOR MAIN MENU     |
+-------------------------+
''')
        print("0. View appointments")
        print("1. Clear appointment")       # show appt table where sta = and docname = uname_input pending change appt stat 
        print("2. Write prescription")            # show him appt table and then have field for user id
        print("3. Logout")
        print("===============================================")
        choice = input("Enter your choice: ")
        print("===============================================")
        if choice == "1":
            clearappt(uname_input)
        elif choice == '0':
            viewapptdoc(uname_input)
        elif choice == "2":
            makeprescription(uname_input)         #get patname in the clearappt func and view appt  
        elif choice == "3":
            print("Logging out..")
            break
        else:
            print("Invalid choice, try again.")
#--9---------------------------admin main menu-------------------------------------------------------------------
def adminmainmenu(uname_input):
    while True:
        print('''
+-------------------------------+
|    ADMINISTRATOR MAIN MENU    |
+-------------------------------+''')
        print('MANAGE STAFF')
        print("1. Add staff")
        print("2. Update salary")
        print("3. Delete staff")
        print("4. View Staff")
        print('\nMANAGE STOCKS')
        print("5. Add new item")
        print("6. Update price")
        print("7. Update quantity")
        print("8. Delete item")
        print("9. Logout")
        print('============================')
        choice = input("Enter your choice: ")
        print("===============================================")
        if choice == "1":
            addstaff()
        elif choice == "2":
            updatesalary()
        elif choice == "3":
            delstaff()
        elif choice == "4":
            viewstaff()
        elif choice == "5":
            additem() 
        elif choice == "6":
            itempriceupdate()
        elif choice == "7":
            itemqtyupdate()
        elif choice == "8":
            delitem()            
        elif choice == "9":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice, try again.")
#-10-------------------------------create patient profile------------------------------------------------------
def createprofile(uname_input):
      unamequery = f"SELECT * FROM patinfo WHERE username = '{uname_input}'"
      cursor.execute(unamequery)
      detail = cursor.fetchall()
      if detail != None:
            print('Profile already exists')                  
            print('Perhaps you want to view your profile or update it.........')
            ch = int(input('Press 1 to continue to update profile'))
            if ch == 1:
                  editprofile(uname_input)
            else:
                  print('INVALID OPERATION')
#---11----------------------------------view pat profile -----------------------------------------------------------
def viewprofile(uname_input):
      unamequery = f"SELECT * FROM patinfo WHERE username = '{uname_input}'"
      cursor.execute(unamequery)
      detail = cursor.fetchall()
      if detail == None:
            print('Profile NOT FOUND')                  
            print('Perhaps you forgot to create your profile.........')
            ch = int(input('Press 1 to continue to create profile'))
            if ch == 1:
                  createprofile(uname_input)
            else:
                  print('INVALID OPERATION')
            
      else:
            table = tabulate(detail, headers=["NAME", "USERNAME", "DOB", "GENDER","CONTACT","MAIL","EMERGENCY CONTACT","BLOOD GROUP","ADDRESS"], tablefmt="fancy_grid")    
            print(table)
#-----12-------------------------------edit pat profile-----------------------------------------------------------------
def editprofile(uname_input):
    viewprofile(uname_input)
    print("Leave blank if you don't want to change a field.")
    newname =   input('Enter your name               :')
    newdob =    input('Enter your date of birth      :')
    newgender = input('Enter your gender             :')
    newphno =   input('Enter your contact number     :')
    newmail =   input('Enter your mail id            :')
    newsosno =  input('Enter emergency contact number:')
    newbg =     input('Enter your blood group        :')
    newadd =    input('Enter your address            :')
    try:
      query = "UPDATE patinfo SET "
      updates = []
      values = []

      if newname:
            updates.append("name=%s")
            values.append(newname)
      if newdob:
            updates.append("dob=%s")
            values.append(newdob)
      if newgender:
            updates.append("gender=%s")
            values.append(newgender)
      if newphno:
            updates.append("contact=%s")
            values.append(newphno)
      if newmail:
            updates.append("mail=%s")
            values.append(newmail)
      if newsosno:
            updates.append("emergency_contact=%s")
            values.append(newsosno)
      if newbg:
            updates.append("blood_group=%s")
            values.append(newbg)
      if newadd:
            updates.append("address=%s")
            values.append(newadd)
      if updates:
            query += ", ".join(updates) + " WHERE username = %s"
            values.append(uname_input)
            cursor.execute(query, tuple(values))
            mydb.commit()
            print("Profile updated successfully!")
      else:
            print("No changes made.")
    except Exception as e:
            print(f"Error: {e}")
#13---------------------------------add item --------------------------
def additem():
      itemname = input('Enter name of the item:')
      qty =input('Enter quantity:')
      mfddate = input('Enter date of manufacture(DD/MM/YYYY):')
      expdate = input('Enter date of expiry(DD/MM/YYYY):')
      typ = input('Enter type of item:')
      price = float(input('Enter price:'))
      q = f"INSERT INTO STOCKS VALUES ('{itemname}','{qty}','{mfddate}','{expdate}','{typ}',{price})"
      cursor.execute(q)
      mydb.commit()
      print(f"New item {itemname} added successfully")
#14-------------------------delete item-----------------------------------      
def delitem():
      itemname = input('Enter name of the item:')
      namequery = f"SELECT * FROM stocks WHERE name = '{itemname}'" 
      cursor.execute(namequery)
      detail = cursor.fetchone()
      if detail == None:
            print(f"The item {itemname} was not found")
            ch = int(input("""
Press 1 to try deleting again
Press 2 to go back to admin menu
"""))
            if ch == 1:
                  delitem()
            elif ch == 2:
                  pass
                  adminmainmenu()
            else:
                  print('INVALID ACTION')
      else:
            q = f"DELETE FROM STOCKS WHERE name = '{itemname}'"
            cursor.execute(q)
            mydb.commit()
            print(f"The item {itemname} was deleted successfully")
#15--------------------------------------update price-------------------------------------
def itempriceupdate():
      itemname = input('Enter name of the item:')
      namequery = f"SELECT * FROM stocks WHERE name = '{itemname}'" 
      cursor.execute(namequery)
      detail = cursor.fetchone()
      if detail == None:
            print(f"The item {itemname} was not found")
            ch = int(input("""
Press 1 to try updating again
Press 2 to go back to admin menu
"""))
            if ch == 1:
                  itempriceupdate()
            elif ch == 2:
                  adminmainmenu()
            else:
                  print('INVALID ACTION')
      else:
            newprice = float(input('Enter new price'))
            q = f"UPDATE STOCKS SET price = '{newprice}' WHERE name = '{itemname}'"
            cursor.execute(q)
            mydb.commit()
            print(f"The price of item {itemname} was updated to {newprice} successfully")
#-----------------------------update qty---------------------------------------------
def itemqtyupdate():
      itemname = input('Enter name of the item:')
      namequery = f"SELECT * FROM stocks WHERE name = '{itemname}'" 
      cursor.execute(namequery)
      detail = cursor.fetchone()
      if detail == None:
            print(f"The item {itemname} was not found")
            ch = int(input("""
Press 1 to try updating again
Press 2 to go back to admin menu
"""))
            if ch == 1:
                  itemqtyupdate()
            elif ch == 2:
                  adminmainmenu()
            else:
                  print('INVALID ACTION')
      else:
            newqty = float(input('Enter new quantity'))
            q = f"UPDATE STOCKS SET qty = '{newqty}' WHERE name = '{itemname}'"
            cursor.execute(q)
            mydb.commit()
            print(f"The price of item {itemname} was updated to {newqty} successfully")
#-----------------------------------------add staff-------------------------------------
def addstaff(): #name desgn dept sal contact mail
      name = input('Enter name:')
      dept = input('Enter department:')
      desgn = input('Enter designation:')
      docstat = input('Doctor?-(y/n)')
      sal = input('Enter salary:')
      phno =input('Enter contact number:')
      mail = input('Enter mail id:')
      sosno =input('Enter emergency contact number:')
      bg = input('Enter blood group')
      q = f"INSERT INTO STAFF VALUES ('{name}','{dept}','{desgn}','{docstat}','{sal}','{phno}','{sosno}','{bg}','{mail}')"
      cursor.execute(q)
      mydb.commit()
      print(f"The staff member {name} was added successfully")
#-----------------------------------------delete staff-----------------------------------
def delstaff():
      name = input('Enter name of the item:')
      namequery = f"SELECT * FROM staff WHERE name = '{name}'" 
      cursor.execute(namequery)
      detail = cursor.fetchone()
      if detail == None:
            print(f"The staff member {name} was not found")
            ch = int(input("""
Press 1 to try deleting again
Press 2 to go back to actions page
"""))
            if ch == 1:
                  delstaff()
            elif ch == 2:
                  pass
                  #actions page function call
            else:
                  print('INVALID ACTION')
      else:
            q = f"DELETE FROM STAFF WHERE name = '{name}'"
            cursor.execute(q)
            mydb.commit()
            print(f"The staff member {name} was deleted successfully")
#--------------------------------------update salary-------------------------------------
def updatesalary():
      name = input('Enter name of the staff:')
      namequery = f"SELECT * FROM staff WHERE name = '{name}'" 
      cursor.execute(namequery)
      detail = cursor.fetchone()
      if detail == None:
            print(f"The item {name} was not found")
            ch = int(input("""
Press 1 to try updating again
Press 2 to go back to actions page
"""))
            if ch == 1:
                  updatesalary()
            elif ch == 2:
                  pass
                  #actions page function call
            else:
                  print('INVALID ACTION')
      else:
            newsal = float(input('Enter new salary'))
            q = f"UPDATE sTAFF SET price = '{newsal}' WHERE name = '{name}'"
            cursor.execute(q)
            mydb.commit()
            print(f"The price of item {name} was updated to {newsal} successfully")
#-------------------------------------------schedule appointments------------------
def makeappt(uname_input):
      date = input('Enter date of appointment(DD/MM/YYYY):')
      que = f"SELECT name,department,designation,mail FROM staff WHERE docstat = 'y'" 
      cursor.execute(que)
      docs = cursor.fetchall()
      table = tabulate(docs, headers=["NAME", "DEPARTMENT", "DESIGNATION", "EMAIL - ID"], tablefmt="fancy_grid")
      print(table)
      doc = input('Enter name of doctor (as displayed from above list): ')
      reason= input('Enter reason of consultation in 10 words')
      unamequery = f"SELECT * FROM staff WHERE name = '{doc}'" 
      cursor.execute(unamequery)
      detail = cursor.fetchone()
      if detail == None:
              print('Doctor NOT FOUND')                  
              patmainmenu(uname_input)
      else:
              q = f"INSERT INTO appointments VALUES ('{uname_input}','{doc}','{date}','Pending','{reason}')"
              cursor.execute(q)
              mydb.commit()
              print(f"appointment scheduled successfully with {doc} on {date}")
#---------------------------------------------cancel appointment----------------------------
def delappt(uname_input):
      print('Kindly find your appointments\n')
      viewapptpat(uname_input)
      print()
      date = input('Enter date of appointment(DD/MM/YYYY)                          :')
      doc = input('Enter name of doctor (as displayed from above appointment table:')
      cursor = mydb.cursor()
      cursor.execute(f"DELETE FROM appointments WHERE date='{date}' AND doctorname ='{doc}'")
      mydb.commit()
      print('\nAppointment successfully cancelled')
      viewapptpat(uname_input)

#-------------------------------------------view appoiment---------------------
def viewapptpat(uname_input):
      status = input('Press 1 to view all appoinments..\nPress 2 to view pending appointments..')
      if status == '1':
            cursor.execute(f"SELECT * FROM appointments WHERE Patientname = '{uname_input}'")          
            rows = cursor.fetchall()
            if not rows:
                  print("No Appointments scheduled.")
            table = tabulate(rows, headers=["Patient Name", "Doctor", "Date","Status","Reason"], tablefmt="fancy_grid")
            print(table)
      elif status == '2':
            cursor.execute(f"SELECT * FROM appointments WHERE Patientname = '{uname_input}' and status = 'pending'")
            rows = cursor.fetchall()
            if not rows:
                  print("No more pending appointments.")
            table = tabulate(rows, headers=["Patient Name", "Date", "Doctor", "Status"], tablefmt="fancy_grid")
            print(table)
      else:
            print('Invalid operation')
#--------------------------------------------
def clearappt(uname_input):
      print('Kindly find your appointments\n')
      viewapptdoc(uname_input)
      print()
      date = input('Enter date of appointment(DD/MM/YYYY)                          :')
      cursor = mydb.cursor()
      cursor.execute(f"UPDATE appointments set status = 'cleared' WHERE date='{date}' AND doctorname ='{uname_input}'")
      mydb.commit()
      print('\nAppointment successfully Cleared')
      viewapptpat(uname_input)

      
#---------------------------------------------
def viewapptdoc(uname_input):
      type = int(input('Press 1 to View all pending appointments,\nPress 2 to Select patient'))
      if type == 1:
            try:
                  cursor.execute(f"SELECT * FROM appointments WHERE doctorname = '{uname_input}' and status = 'pending'")          ############################
                  rows = cursor.fetchall()
                  if not rows:
                        print("No Appointments scheduled.")
                  table = tabulate(rows, headers=["Patient", "Doctor","Date","Status","Reason"], tablefmt="fancy_grid")
                  print(table)
            except Exception as e:
                  print(f" Error: {e}")
      elif type == 2:
            n = input('Enter patient ID:')
            try:
                  cursor.execute(f"SELECT * FROM appointments WHERE docname = '{uname_input}' and status = 'pending'")          ############################
                  rows = cursor.fetchall()
                  if not rows:
                        print("No Appointments scheduled.")
                  table = tabulate(rows, headers=["Patient", "Doctor","Date","Status","Reason"], tablefmt="fancy_grid")
                  print(table)
            except Exception as e:
                  print(f" Error: {e}")
#-------------------------------------
def makeprescription(uname_input):
    viewapptdoc(uname_input)
    pname_input = input('Enter username of patient:')
    date = input("Enter date of patient appointment to make a prescription: ")
    print("\nEnter medicine details one by one. Leave blank when finished.\n")
    prescriptions = []
    while True:
        medicine = input("Enter Medicine Name (or leave blank to finish): ")
        if medicine.lower() == '':
            break
        dosage = input("Enter Dosage: ").strip()
        prescriptions.append((pname_input, date, medicine, dosage))
        print("Medicine added.\n")

    if prescriptions:
        query = f"INSERT INTO prescriptions (uname_input, date, medicine_name, dosage) VALUES ( %s, %s, %s, %s)"
        cursor.executemany(query, prescriptions)
        mydb.commit()
        print(f"\n {len(prescriptions)} medicine(s) added successfully for {pname_input}'s appointment on {date}!")
    else:
        print("\nNo medicines entered. Nothing added.")
#----------------------------------------------------------------------        
def export_pcptn(uname_input, date):
    try:
        query = "SELECT medicine_name, dosage FROM prescriptions WHERE uname_input = %s AND date = %s"
        cursor.execute(query, (uname_input, date))
        medicines = cursor.fetchall()
        
        if not medicines:
            print("No prescription found for this patient and date.")
            return
        
        filename = f"prescription_{uname_input}_{date.replace('/', '-')}.txt"
        
        with open(filename, 'w') as file:
            file.write("=" * 50 + "\n")
            file.write("PRESCRIPTION\n")
            file.write("=" * 50 + "\n\n")
            file.write(f"Patient Username: {uname_input}\n")
            file.write(f"Date: {date}\n")
            file.write("-" * 50 + "\n\n")
            file.write("MEDICINES:\n")
            file.write("-" * 50 + "\n")
            
            for idx, (medicine_name, dosage) in enumerate(medicines, 1):
                file.write(f"{idx}. {medicine_name}\n")
                file.write(f"   Dosage: {dosage}\n\n")
            
            file.write("=" * 50 + "\n")
        
        print(f"✓ Prescription exported successfully to {filename}")
    
    except Exception as e:
        print(f"Error exporting prescription: {e}")      
#-------------------------------
def viewstaff():
    cursor.execute(f"SELECT * FROM Staff")          ############################
    rows = cursor.fetchall()
    table = tabulate(rows, headers=["Name", "Department","Designation","Doctor Status","Salary","Contact","Emergency contact","Blood group","Mail"], tablefmt="fancy_grid")
    print(table)
#------------------------------------
if __name__ == "__main__":
    mainmenu()
