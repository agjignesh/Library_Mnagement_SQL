try:
    import mysql.connector as sql
    ob=sql.connect(host='localhost',user='root',passwd='1407',database='main')
    cur=ob.cursor()
except Exception as e:
    print(e)

def newbook():
    try:
        cur.execute("select count(*) from book")
        pre=cur.fetchone()
        a=pre[0]
        ch="yes"
        ob.commit()
        while ch=="yes":
            Id=input("Enter Book Id : ")
            bookname=input("Enter Book Name : ")
            bookauthor=input("Enter Book Author : ")
            totalqty=int(input("Enter quantity : "))
            price=float(input("Enter book price : "))
            q="insert into book(Id,book_name,book_author,total_qty,available_qty,price)values(%s,%s,%s,%s,%s,%s)"
            v=(Id,bookname,bookauthor,totalqty,totalqty,price)
            cur.execute(q,v)
            ob.commit()
            ch = input("Do you Have more books to enter yes/no : ")
            while ch not in ("yes","no"):
                ch=input("Please Enter yes/no : ")
        cur.execute("select count(*) from book")
        final = cur.fetchone()
        b=final[0]
        print("Number of books added are",b-a)
        ob.commit()
    except Exception as e:
        print(e)

# use when new book arrive  jignesh  exception done.

def date():
    import datetime
    return datetime.date.today()

# internal use only

def newcustomer():
    try:
        import datetime
        ch="yes"
        while ch=="yes":
            id=input("Enter Book Id : ")
            q = "select book_name from book where Id=%s"
            cur.execute(q, (id,))
            b = cur.fetchone()
            ob.commit()
            bookname = b[0]
            pname=input("Enter Customer Name : ")
            cdetail=int(input("Enter Customer Phone Number enter 0 if not available : "))
            idate=date()
            ld=input("Enter number of days for which the book is lend : ")
            if ld=="":
                ld=7
                print("The book is lend for 7 days")
            else:
                ld=int(ld)
            ldate=idate+datetime.timedelta(days=ld)
            q="insert into Issued_book(Id,book_name,person_name,contact_details,issue_date,last_date,return_date,fine,transaction_id)values(%s,%s,%s,%s,%s,%s,null,0,%s)"
            a=transaction_id_genrate()
            v=(id,bookname,pname,cdetail,idate,ldate,a,)
            cur.execute(q,v)
            ob.commit()
            altertabel(id)
            q = "insert into Pending_book(Id,book_name,person_name,contact_details,issue_date,last_date,transaction_id)values(%s,%s,%s,%s,%s,%s,%s)"
            v = (id, bookname, pname, cdetail, idate, ldate,a,)
            cur.execute(q, v)
            ob.commit()
            print(f"Customer transaction Id is {a} make sure to write it down on the book")
            print()
            ch=input(" Do You have more customers yes/no : ")
            while ch not in ("yes","no"):
                ch=input("Please Enter yes/no : ")
        print("changes sucsefull")
    except Exception as e:
        print(e)

# use when new customer is there jignesh exception done.

def altertabel(id):
    try:
        q="update book set available_qty=available_qty-1 where Id=%s"
        cur.execute(q,(id,))
        ob.commit()
    except Exception as e:
        print(e)

# internal use only

def displaypast():
    try:
        q="select * from Pending_book where last_date<%s"
        x=date()
        cur.execute(q,(x,))
        data=cur.fetchall()
        print("Id      book_name    customer_name P.no  issue_date     return_date  transaction_id")                    
        for i in data:
            if i[6]!=0:
                for j in i:
                    print(j,end="     ")
                print()
        print("----------------------------------------------------------------------------------------------")
    except Exception as e:
        print(e)

# use to diplay details of those books whose last date is passed, jignesh.

def returnbook():
    try:
        name=input("Enter name of the person")
        q="select count(*) from pending_book where person_name=%s"
        cur.execute(q,(name,))
        z=cur.fetchone()
        ob.commit()
        data=z[0]
        if data==1:
            l="select Id from pending_book where person_name=%s"
            cur.execute(l,(name,))
            id=cur.fetchone()
            ob.commit()
            iid=id[0]
            t="update book set available_qty=available_qty+1 where Id=%s"
            cur.execute(t,(iid,))
            ob.commit()
            u="select transaction_id from pending_book where person_name=%s"
            cur.execute(u, (name,))
            transaction_i=cur.fetchone()
            transaction_id=transaction_i[0]
            fine_update(transaction_id)
            today=date()
            i="update issued_book set return_date=%s where transaction_id=%s"
            o=(today,transaction_id,)
            cur.execute(i,o)
            ob.commit()
            r = "delete from pending_book where person_name=%s"
            cur.execute(r, (name,))
            ob.commit()
            print("Changes succesfull")
            print()

        elif data==0:
            print("Please check customer name")

        else:
            number = int(input("Enter transaction_id"))
            l = "select Id from pending_book where transaction_id=%s"
            cur.execute(l, (number,))
            id = cur.fetchone()
            ob.commit()
            iid=id[0]
            t = "update book set available_qty=available_qty+1 where Id=%s"
            cur.execute(t,(iid,))
            ob.commit()
            fine_update(number)
            today=date()
            i = "update issued_book set return_date=%s where transaction_id=%s"
            o = (today,number,)
            cur.execute(i, o)
            ob.commit()
            s = "delete from pending_book where transaction_id=%s"
            cur.execute(s, (number,))
            ob.commit()
            print("Changes succesfull")
            print()
    except Exception as e:
        print(e)

# use when book is returned sarthak

def pendingbook():
    try:
        cur.execute("select book_name,person_name,contact_details,issue_date,last_date from pending_book")
        data=cur.fetchall()
        ob.commit()
        for i in data:
            if i[0]!="test":
                for j in i:
                    print(j,end="   ")
                print()
        print("----------------------------------------------------------------------------------------------")
    except Exception as e:
        print(e)

# display details of books in pending_book table, change for "enpty set" sarthak

def availablebook():
    try:
        ch="yes"
        while ch=="yes":
            choice="bi"
            if choice=='bi':
                Idd=input("Enter Id of required book : ")
                q="select available_qty from book where Id=%s"
                cur.execute(q,(Idd,))
                data=cur.fetchone()
                ob.commit()
                print("The number of books with Id",Idd,"available are",data[0])


            # search with book id

            else:
                print("Incorrect input ")
            ch=input("Do you want to Scearch for more Enter 'yes'/'no' : ")
            print("----------------------------------------------------------------------------------------------")
    except Exception as e:
        print(e)

# diplay available quantity of book sarthak

def fine_update(transaction_id):
    import datetime
    try:
        q="select last_date from issued_book where transaction_id=%s"
        cur.execute(q,(transaction_id,))
        last_dat=cur.fetchone()
        ob.commit()
        last_date=last_dat[0]
        int_last_date=last_date.toordinal()
        today=date()
        int_today=today.toordinal()
        extra=int_today-int_last_date
        if extra>0:
            q = "update issued_book set fine=%s where transaction_id=%s"
            fine=2*extra
            print(f"fine is {fine}")
            v = (fine,transaction_id,)
            cur.execute(q,v)
            ob.commit()
        else:
            print("No fine")
    except Exception as e:
        print(e)

# internal use jignesh exception done

def transaction_id_genrate():
    q="select max(transaction_id) from issued_book"
    cur.execute(q)
    v=cur.fetchone()
    new_traction_id=v[0]+1
    return new_traction_id

# internal use

def custdetailsforpendingbook():
    try:
        ch="yes"
        while ch=="yes":
            choice = input("Enter If you want to search by bookname(Enter-bn) or book id(Enter-bi) : ")
            if choice == 'bn':
                name = input("Enter Book Name : ")
                q = "select person_name,contact_details,last_date from pending_book where book_name=%s"
                cur.execute(q, (name,))
                data = cur.fetchall()
                ob.commit()
                for i in data:
                    if i[0]==0:
                        continue
                    else:
                        print("Customer name:  ",i[0],'\n',"Contact no.:   ",i[1],'\n',"Last date:     ", i[2],)
                    print("----------------------------------------------------------------------------------------------")
                ch=input("Do you want to search more enter 'yes/no' : ")

            #   search with book name

            elif choice == 'bi':
                Idd = input("Enter Id of book : ")
                q = "select person_name,contact_details,last_date from pending_book where Id=%s"
                cur.execute(q, (Idd,))
                data = cur.fetchall()
                for i in data:
                    if i[0]=="test":
                        continue
                    else:
                        print()
                        print("Customer name:  ",i[0],'\n',"Contact no.:   ",i[1],'\n',"Last date:     ", i[2])
                print("----------------------------------------------------------------------------------------------")
                ch = input("Do you want to search more enter 'yes/no' : ")

        #   search with book id

            else:
                ch="yes"
                print("Wrong input")
    except Exception as e:
        print(e)

# display those customer details who have a cerain book sarthak

def fine_search():
    import datetime
    print("""Enter 
    1 for last 7 days 
    2 for last 30 days
    3 for custom""")
    choice=int(input("Enter your choice :"))
    if choice==1:
        total=0
        q="select Id,book_name,person_name,fine from issued_book where return_date>=%s and fine is not null"
        v=(date()-datetime.timedelta(days=7),)
        cur.execute(q,v)
        a=cur.fetchall()
        for i in a:
            print(i[0],"   ",i[1],"   ",i[2],"   ",i[3])
            total=total+i[3]
        print("Total fine collected in the last 7 days = ",total)
        ob.commit()

    elif choice==2:
        total=0
        q = "select Id,book_name,person_name,fine from issued_book where return_date>=%s and fine is not null"
        v = (date() - datetime.timedelta(days=30),)
        cur.execute(q, v)
        a = cur.fetchall()
        for i in a:
            print(i[0], "   ", i[1], "   ", i[2], "   ", i[3])
            total=total+i[3]
        print("Total fine collected in the last 7 days = ", total)
        ob.commit()

    elif choice==3:
        try:
            total=0
            s = eval(input("Enter Start date in 'yyyy,mm,dd format :'"))
            start_date = datetime.datetime(s[0], s[1], s[2])
            e = eval(input("Enter End date 'yyyy,mm,dd format' : "))
            end_date = datetime.datetime(e[0], e[1], e[2])
            q = "select Id,book_name,person_name,fine from issued_book where return_date>=%s and return_date<=%s and fine is not null"
            v=(start_date,end_date,)
            cur.execute(q,v)
            a = cur.fetchall()
            for i in a:
                print(i[0], "   ", i[1], "   ", i[2], "   ", i[3])
                total=total+i[3]
            print("Total fine collected in the last 7 days = ", total)
            ob.commit()
        except Exception as e:
            print(e)

    else:
        print("Wrong choise")
        fine_search()


def connection_check():
    if ob.is_connected():
        return 1
    else:
        return 0

menu=""" Enter 
 1 for New customer
 2 for New book
 3 for Details of book and customer whose return date has passed 
 4 if book is being returned 
 5 for Details of all the pending books
 6 to check the available quantity of a book
 7 to search for customer details who have a certain book
 8 to search and display details of fine collected
 9 to EXIT"""

zzz="yes"
while zzz=="yes":
    z = connection_check()
    if z==1:
        print(menu)
        main_choise = int(input("Please Enter your choice : "))
        print()
        if main_choise==1:
            newcustomer()
            zzz=input("Do you want to Perform more actions Enter yes/no : ")
            if zzz not in ("yes","no"):
                zzz=input("Please Enter yes/no : ")
        elif main_choise==2:
            newbook()
            zzz = input("Do you want to Perform more actions Enter yes/no : ")
            if zzz not in ("yes", "no"):
                zzz = input("Please Enter yes/no : ")
        elif main_choise==3:
            displaypast()
            zzz = input("Do you want to Perform more actions Enter yes/no : ")
            if zzz not in ("yes", "no"):
                zzz = input("Please Enter yes/no : ")
        elif main_choise==4:
            returnbook()
            zzz = input("Do you want to Perform more actions Enter yes/no : ")
            if zzz not in ("yes", "no"):
                zzz = input("Please Enter yes/no : ")
        elif main_choise==5:
            pendingbook()
            zzz = input("Do you want to Perform more actions Enter yes/no : ")
            if zzz not in ("yes", "no"):
                zzz = input("Please Enter yes/no : ")
        elif main_choise==6:
            availablebook()
            zzz = input("Do you want to Perform more actions Enter yes/no : ")
            if zzz not in ("yes", "no"):
                zzz = input("Please Enter yes/no : ")
        elif main_choise==7:
            custdetailsforpendingbook()
            zzz = input("Do you want to Perform more actions Enter yes/no : ")
            if zzz not in ("yes", "no"):
                zzz = input("Please Enter yes/no : ")
        elif main_choise==8:
            fine_search()
            zzz = input("Do you want to Perform more actions Enter yes/no : ")
            if zzz not in ("yes", "no"):
                zzz = input("Please Enter yes/no : ")
        elif main_choise==9:
            print("Thanku and have a nice day")
            zzz = "no"
        else:
            print("Wrong Choice")
            zzz="yes"
        print("----------------------------------------------------------------------------------------------")
