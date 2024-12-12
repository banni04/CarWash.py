import sqlite3
from datetime import datetime,timedelta 
from tkinter import *
from tkinter import Tk, Label ,ttk
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.messagebox
import requests
from io import BytesIO
import numpy as np
import cv2
from time import strftime

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
import subprocess
from reportlab.lib import colors 

total_tel = ""
car_prices = {'a': 300, 'b': 200, 'c': 450, 'd': 120}
wash_time = {'a': timedelta(hours=1),'b': timedelta(minutes=30),'c': timedelta(hours=1,minutes=30),'d': timedelta(minutes=25)}

total_bill = 0
total_price = 0

conn = sqlite3.connect("D:\SQL\python 11\clientdata.db")
cursor = conn.cursor()

#shop
#ตารางเก็บสต๊อกสินค้าของร้านค้า
cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock
                (product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL)''')
#ตารางเก็บประวัติการซื้อ 
cursor.execute('''
                CREATE TABLE IF NOT EXISTS cart
                (product_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                tel VARCHAR(10))''')
#ตารางเก็บประวัติการซื้อ ถาวร
cursor.execute('''
                CREATE TABLE IF NOT EXISTS history
                (product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                tel VARCHAR(10),
                date REAL NOT NULL)''')
#ตารางเก็บประวัติ log in
cursor.execute('''
    CREATE TABLE IF NOT EXISTS member (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        tel VARCHAR(10) NOT NULL)''')
#wash
#ตารางเก็บประวัติการล้างรถ
cursor.execute('''
    CREATE TABLE IF NOT EXISTS client (     
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30) NOT NULL,
    brand VARCHAR(30) NOT NULL,
    color VARCHAR(30) NOT NULL,
    lp VARCHAR(30) NOT NULL,
    option VARCHAR(30) NOT NULL,
    pick VARCHAR(30) NOT NULL,
    now VARCHAR(30) NOT NULL,
    cash VARCHAR(30) NOT NULL,
    time VARCHAR(30) NOT NULL,
    tel VARCHAR(10)NOT NULL)''')
#ตารางเก็บประวัติการล้างรถ ถาวร
cursor.execute('''      
    CREATE TABLE IF NOT EXISTS servicelist (     
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30) NOT NULL,
    brand VARCHAR(30) NOT NULL,
    color VARCHAR(30) NOT NULL,
    lp VARCHAR(30) NOT NULL,
    option VARCHAR(30) NOT NULL,
    pick VARCHAR(30) NOT NULL,
    now VARCHAR(30) NOT NULL,
    cash VARCHAR(30) NOT NULL,
    time VARCHAR(30) NOT NULL,
    tel VARCHAR(10)NOT NULL)''')

cursor.execute('''
            CREATE TABLE IF NOT EXISTS income_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dayt VARCHAR(30) NOT NULL,
            incomet VARCHAR(30) NOT NULL)''')

def pdf(nameget, telephone, optionget, dataget, total_bill):
    font_path = r'c:\USERS\MIKIBUNNIE\APPDATA\LOCAL\MICROSOFT\WINDOWS\FONTS\THSARABUNNEW.TTF'

    pdfmetrics.registerFont(TTFont('THSarabunNew', font_path))
    
    print(total_bill)

    title_style = ParagraphStyle(
        name='TitleStyle',
        fontSize=16,
        fontName='THSarabunNew',
        alignment=0,
        spaceAfter=12,
    )

    larger_title_style = ParagraphStyle(
        name='LargerTitleStyle',
        fontSize=22,
        fontName='THSarabunNew',
        alignment=0,
        spaceAfter=12,
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if optionget :
        optionget = optionget
    else:
        optionget = "ไม่ได้เลือก"

    if dataget :
        dataget = dataget
    else:
        dataget = "ไม่ได้เลือก"

    cursor.execute("SELECT COUNT(product_id) FROM history")
    count_all = cursor.fetchone()[0]
    def generate_report(file_name, dataget, telephone):
        doc = SimpleDocTemplate("invoiceID%s.pdf"%f"{count_all}", pagesize=letter)
        story = []

        title1 = Paragraph("ใบเสร็จรับเงิน", larger_title_style)
        story.append(title1)

        title2 = Paragraph("Receipt", larger_title_style)
        story.append(title2)

        spacing_paragraph = Paragraph("<br/><br/>", title_style)
        story.append(spacing_paragraph)

        title4 = Paragraph(f"ชื่อลูกค้า: {nameget}", title_style)
        story.append(title4)

        title5 = Paragraph(f"เบอร์โทรศัพท์: {telephone}", title_style)
        story.append(title5)

        title6 = Paragraph(f"บริการที่เลือก : {optionget}", title_style)
        story.append(title6)

        title7 = Paragraph(f"วันที่: {now}", title_style)
        story.append(title7)

        spacing_paragraph = Paragraph("________________________________________________________________", title_style)
        story.append(spacing_paragraph)

        title8 = Paragraph("ผู้ออก : บริษัท เก้าเก้า คาร์วอช จำกัด", title_style)
        story.append(title8)

        title9 = Paragraph("ที่อยู่ : 111/11 ซ.ยูนิคอร์น ถ.เรนโบว์ จ.พาวเวอร์พัฟ", title_style)
        story.append(title9)

        title10 = Paragraph("เลขผู้เสียภาษี : 0123456789123", title_style)
        story.append(title10)

        spacing_paragraph = Paragraph("________________________________________________________________", title_style)
        story.append(spacing_paragraph)

        title11 = Paragraph("รายการสินค้า", title_style)
        story.append(title11)
        

        if dataget is None:
            dataget = "ไม่มีรายการสั่งซื้อ"
            story.append(Paragraph(dataget, title_style))
        else:
            for k in dataget:
                if len(k) >= 3:  
                    line = f"ชื่อ: {k[0]} จำนวน: {k[1]}  ราคา: {k[2]}"
                    story.append(Paragraph(line, title_style))

        # if dataget is None:
        #     dataget = "ไม่มีรายการสั่งซื้อ"
        #     story.append(Paragraph(dataget, title_style))
        # else:
        #     opz = []
        #     for k in dataget:
        #         opz.append(k)
        #         line = f"ชื่อ: {k[0]} จำนวน: {k[1]}  ราคา: {k[2]}"
        #         story.append(Paragraph(line, title_style))
        
        data2 = [
            ['จำนวนเงินรวมทั้งสิ้น(บาท)', f'{total_bill}'],
        ]

        table2_width = 450
        table2 = Table(data2, colWidths=[table2_width / 3] * 3)

        table2_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'THSarabunNew'),
            ('FONTNAME', (0, 1), (-1, -1), 'THSarabunNew'),
            ('FONTSIZE', (0, 0), (-1, -1), 13),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table2.setStyle(table2_style)

        spacing_paragraph = Paragraph("<br/><br/>", title_style)
        story.append(spacing_paragraph)

        story.append(table2)

        doc.build(story)

        try:
            subprocess.Popen(['start',"invoiceID%s.pdf"%f"{count_all}"], shell=True)
        except FileNotFoundError:
            print("Could not open 'sample_report.pdf'. Make sure you have a PDF viewer installed.")

    if __name__ == '__main__':
        generate_report(f'reciepe{nameget}.pdf', dataget, telephone)

def main_member():

    def input_create(): #sign in
        member1=Toplevel(member)
        member1.title("99 Car Wash ")
        member1.geometry("1250x720+145+25")
        # global et2

        def createuser():
            username = et.get()
            password = et1.get()
            tel = et2.get()
            if len(tel) == 10 and tel.isdigit():
                
                cursor.execute('SELECT username FROM member WHERE username = ? ', (username,))
                user = cursor.fetchone()
                
                if user:
                    user=user[0]
                    
                if username == user:
                    et.delete(0, tk.END)
                    et1.delete(0, tk.END)
                    et2.delete(0, tk.END)
                    tkinter.messagebox.showinfo("แจ้งเตือน", "ขออภัย เนื่องจากท่านได้ทำการสมัครสมาชิกไว้แล้ว")
                else:
                    try:
                        cursor.execute('INSERT INTO member (username, password, tel) VALUES (?, ?, ?)', (username, password, tel))
                        conn.commit()
                        tkinter.messagebox.showinfo("แจ้งเตือน", "เรียบร้อย")
                        et.delete(0, tk.END)
                        et1.delete(0, tk.END)
                        et2.delete(0, tk.END)
                        member1.destroy()
                    except sqlite3.IntegrityError:
                        tkinter.messagebox.showinfo("แจ้งเตือน", "ขออภัย เนื่องจากท่านได้ทำการสมัครสมาชิกไว้แล้ว")
                        et.delete(0, tk.END)
                        et1.delete(0, tk.END)
                        et2.delete(0, tk.END)
            else :
                tkinter.messagebox.showinfo("แจ้งเตือน","กรุณาใส่เบอร์ให้ถูกต้อง")
                

        main=Image.open(r'D:\coding\project\pj\msignin.png')
        member1.sinbg=ImageTk.PhotoImage(main)
        Label(member1,image=member1.sinbg).place(x=0,y=0)

        et = Entry(member1, fg="black", bd=0, bg="#d9d9d9", font=('Tahoma',20),width=25)
        et.place(x=633,y=183)

        et1 = Entry(member1, fg="black", bd=0, bg="#d9d9d9", font=('Tahoma',20),width=25) 
        et1.place(x=633,y=308)

        et2 = Entry(member1, fg="black", bd=0, bg="#d9d9d9", font=('Tahoma',20),width=25)  
        et2.place(x=633,y=444)
 
        main=Image.open(r'D:\coding\project\pj\signin.png')
        member1.msingin=ImageTk.PhotoImage(main)
        Button(member1,image=member1.msingin,bd=0,command=createuser).place(x=370,y=550)

        # # Load an image for the button
        # close_image = tk.PhotoImage(file=r'D:\coding\project\pj\exit.png')  # แทน "close.png" ด้วยชื่อไฟล์ภาพของคุณ


        # # Create a button with the image and text
        # btn_close = tk.Button(member1, text="Close", image=close_image, command=member1.destroy)
        # btn_close.place(x=0, y=0)


        member1.mainloop()

    def loginuser():
        username = et.get()
        password = et1.get()

        cursor.execute('SELECT * FROM member WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if username == "admin" and password == "12345":
            tkinter.messagebox.showinfo("แจ้งเตือน", "ยินดีต้อนรับ!")
            et.delete(0, END)
            et1.delete(0, END)
            main_admin()
        elif user:
            tkinter.messagebox.showinfo("แจ้งเตือน", "ยินดีต้อนรับ!")
            et.delete(0, END)
            et1.delete(0, END)
            user_main(username)
        else:
            tkinter.messagebox.showinfo("แจ้งเตือน", "รหัสและชื่อผิด")
            et.delete(0, END)
            et1.delete(0, END)

    member = Toplevel()
    member.title("99 Car Wash ")
    member.geometry("1250x720+145+25")

    main=Image.open(r'D:\coding\project\pj\memberbg.png')
    member.mbg=ImageTk.PhotoImage(main)
    Label(member,image=member.mbg).place(x=0,y=0)

    et = Entry(member, fg="black", bd=0, bg="#d9d9d9", font=('Tahoma',20),width=25)
    et.place(x=626,y=256)

    et1 = Entry(member,fg="black",bd=0,bg="#d9d9d9",font=('Tahoma',20),width=25) 
    et1.place(x=628,y=399)

    main=Image.open(r'D:\coding\project\pj\memberlogin.png')
    member.memberlogin=ImageTk.PhotoImage(main)
    Button(member,image=member.memberlogin,bd=0,command=loginuser).place(x=133,y=518)

    main=Image.open(r'D:\coding\project\pj\membercreate.png')
    member.mcreate=ImageTk.PhotoImage(main)
    Button(member,image=member.mcreate,bd=0,command=input_create).place(x=657,y=519)

    member.mainloop()

def main_admin():
    admin=Toplevel()
    admin.title("หน้าแอดมินหลัก")
    admin.geometry("1250x720+145+25")

    main=Image.open(r'D:\coding\project\pj\main_admin.png')
    admin.shop=ImageTk.PhotoImage(main)
    Label(admin,image=admin.shop).place(x=0,y=0)

    def fix_product_a():
        po_id = et.get()
        quantity = et2.get()
        cursor.execute("UPDATE stock SET quantity = quantity + ? WHERE product_id = ?", (quantity, po_id))
        conn.commit()
        overview()
        et.delete(0,END)
        et1.delete(0,END)
        et2.delete(0,END)

    def add_product_a():
        name=et.get()
        price=et1.get()
        quantity=et2.get()

        if name and price and quantity is not None:
            cursor.execute("INSERT INTO stock (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
            conn.commit()
        else:
            tkinter.messagebox.showinfo("แจ้งเตือน","กรุณากรอกข้อความ")
        overview()
        et.delete(0,END)
        et1.delete(0,END)
        et2.delete(0,END)

    def del_product_a():
        name=et.get()
        if name :
            if name:
                cursor.execute("DELETE FROM stock WHERE name=?", (name,))
                conn.commit()
                if name:
                    cursor.execute("DELETE FROM stock WHERE product_id=?", (name,))
                    conn.commit()
                    tkinter.messagebox.showinfo("แจ้งเตือน","ลบข้อมูลแล้ว")
            else:
                tkinter.messagebox.showinfo("แจ้งเตือน","กรุณากรอกข้อความ")
        else:
            tkinter.messagebox.showinfo("แจ้งเตือน","กรุณาใส่หมายเลขที่ต้องการลบ")
        overview()

    def overview():
        
        cursor.execute("SELECT SUM(price) FROM history")
        total_price_shop = cursor.fetchone()

        cursor.execute("SELECT SUM(cash) FROM servicelist")
        total_price_wash = cursor.fetchone()

        if total_price_shop is not None:
            total_price_shop = total_price_shop[0]

        if total_price_wash is not None:
            total_price_wash = total_price_wash[0]

        if total_price_shop and total_price_wash :
            total_carwash = total_price_wash + total_price_shop 
        elif total_price_shop :
            total_carwash = total_price_shop
        elif total_price_wash:
            total_carwash = total_price_wash
        else :
            total_carwash = None

        Label(admin,text=f"{total_price_wash}",bg="#fff7e7",font=('Tahoma', 20), ).place(x=282,y=239)

        Label(admin,text=f"{total_price_shop}",bg="#fff7e7",font=('Tahoma', 20), ).place(x=282,y=300)
        
        Label(admin,text=f"{total_carwash}",bg="#fff7e7",font=('Tahoma', 20), ).place(x=282,y=363)

        cursor.execute("SELECT * FROM stock")
        products = cursor.fetchall()    

        showproducta = tk.Listbox(admin,bd=0,width=38,bg="#fff7e7",height=15, font=('Tahoma', 10))
        showproducta.place(x=931,y=97)

        if products:
            showproducta.delete(0, tk.END)

            for row in products:
                row_info = f"ID : {row[0]},: {row[1]}, ราคา : {row[2]}, จำนวน : {row[3]}"
                showproducta.insert(tk.END, row_info)
        else:
            showproducta.delete(0, tk.END)
            tkinter.messagebox.showinfo("แจ้งเตือน", "รายการของคุณว่างเปล่า")
        
        cursor.execute("SELECT * FROM member")
        lk = cursor.fetchall()    
        
        showca = tk.Listbox(admin,bd=0,width=38,bg="#fff7e7",height=12, font=('Tahoma', 10))
        showca.place(x=931,y=480)

        if lk:
            showca.delete(0, tk.END)
            for row in lk:
                row_info = f"ID : {row[0]},: {row[1]}, เบอร์ : {row[3]}"
                showca.insert(tk.END, row_info)
        else:
            showca.delete(0, tk.END)
            showca.insert(tk.END, "ตะกร้าของคุณว่างเปล่า")

    def delete():
        now=datetime.today()
        id=aet.get()
        if id:
            cursor.execute("DELETE FROM client WHERE id = ?", (id,))
            conn.commit()
            tkinter.messagebox.showinfo("แจ้งเตือน", "ลบข้อมูลแล้ว\nวันที่ลบ: " + now.ctime())
        else:
            tkinter.messagebox.showinfo("แจ้งเตือน", "ไม่มีข้อมูล หมายเลข ระบุไว้")

    def clear_data():
        now = datetime.today()
        confirm = tkinter.messagebox.askquestion("ยืนยันการลบข้อมูลทั้งหมด","คุณต้องการปิดลบข้อมูลทั้งหมดหรือไม่")
        if confirm == "yes":
            cursor.execute("DELETE FROM client ")
            conn.commit() 
            tkinter.messagebox.showinfo("แจ้งเตือน", "ลบข้อมูลทั้งหมดแล้วแล้ว\nวันที่: " + now.ctime())
        elif confirm == "no":
            tkinter.messagebox.showinfo("แจ้งเตือน", "ยกเลิกการลบข้อมูลทั้งหมดแล้วแล้ว\nวันที่: " + now.ctime())
            pass
    
    def save_data():
        ch = tkinter.messagebox.askquestion("แจ้งเตือน", "ต้องการบันทึกข้อมูลทั้งหมดหรือไม่")
        if ch == "yes":
            now = datetime.today()

            day_t = now.ctime()
            cursor.execute("SELECT SUM(servicelist.cash + history.price) FROM servicelist, history")
            total_cash = cursor.fetchone()[0]
            income_t = total_cash
        
            cursor.execute("INSERT INTO income_data (dayt,incomet) VALUES (?,?)",(day_t,income_t))
            cursor.execute("DROP TABLE client")
            tkinter.messagebox.showinfo("แจ้งเตือน", "บันทึกข้อมูลทั้งหมดแล้วแล้ว\nวันที่: " + now.ctime())
            conn.commit()

        elif ch == "no":
            pass

    def createtable():
        now = datetime.today()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS client (   
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(30) NOT NULL,
        brand VARCHAR(30) NOT NULL,
        color VARCHAR(30) NOT NULL,
        lp VARCHAR(30) NOT NULL,
        option VARCHAR(30) NOT NULL,
        pick VARCHAR(30) NOT NULL,
        now VARCHAR(30) NOT NULL,
        cash VARCHAR(30) NOT NULL,
        time VARCHAR(30) NOT NULL,
        tel VARCHAR(10) NOT NULL)''') 
        tkinter.messagebox.showinfo("แจ้งเตือน", "สร้างตารางเรียบร้อยแล้ว\nวันที่: " + now.ctime())
        
    def show_info():
        show_info_window = tk.Toplevel()
        show_info_window.title("Show Info")
        show_info_window.geometry("1410x500")

        # Create a frame to hold the Treeview and scrollbar
        frame = ttk.Frame(show_info_window)
        frame.pack(fill="both", expand=True)

        # Create a Treeview widget with columns
        columns = ("ID", "Name", "Brand", "Color", "License Plate", "Option", "Pick", "Now", "Cash", "Time", "Tel")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        # Add headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column("ID", width=2)  # คอลัมน์ "ID" ความกว้าง 2 พิกเซล
            tree.column("Name", width=30)  
            tree.column("Brand", width=20)  
            tree.column("Color", width=20)  
            tree.column("License Plate", width=20)  
            tree.column("Option", width=180)  
            tree.column("Pick", width=160)  
            tree.column("Now", width=90)  
            tree.column("Cash", width=20)  
            tree.column("Time", width=30)  
            tree.column("Tel", width=50)  

        # Connect to the SQLite database
        conn = sqlite3.connect("clientdata.db")
        cursor = conn.cursor()

        # Fetch data from the database
        cursor.execute("SELECT * FROM client")
        sdata = cursor.fetchall()

        if sdata:
            for row in sdata:
                tree.insert("", "end", values=row)
        else:
            tkinter.messagebox.showinfo("แจ้งเตือน", "ไม่มีข้อมูลในฐานข้อมูล.")

        # Create a vertical scrollbar
        vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vscrollbar.pack(side="right", fill="y")

        # Configure the Treeview to use the scrollbar
        tree.config(yscrollcommand=vscrollbar.set)

        # Pack the Treeview
        tree.pack(fill="both", expand=True)

        btn_close = tk.Button(show_info_window, width=10, text='Close', command=show_info_window.destroy)
        btn_close.pack()

        show_info_window.mainloop()
    
    et = Entry(admin, fg="black",bd=0, bg="#ffffff", font=('Tahoma',20), width=15)
    et.place(x=611,y=239)
    et1 = Entry(admin, fg="black",bd=0, bg="#ffffff", font=('Tahoma',20), width=15)
    et1.place(x=611,y=345)
    et2 = Entry(admin, fg="black",bd=0, bg="#ffffff", font=('Tahoma',20), width=15)
    et2.place(x=611,y=447)

    main=Image.open(r'D:\coding\project\pj\main_confirm.png')
    admin.mconfirm=ImageTk.PhotoImage(main)
    Button(admin,image=admin.mconfirm,bd=0,command=add_product_a).place(x=626,y=503)

    main=Image.open(r'D:\coding\project\pj\main_delete.png')
    admin.mdelete=ImageTk.PhotoImage(main)
    Button(admin,image=admin.mdelete,bd=0,command=del_product_a).place(x=625,y=554)

    main=Image.open(r'D:\coding\project\pj\deladmin.png')
    admin.deladmin=ImageTk.PhotoImage(main)
    Button(admin,image=admin.deladmin,bd=0,command=delete).place(x=270,y=535)

    main=Image.open(r'D:\coding\project\pj\clearadmin.png')
    admin.clearadmin=ImageTk.PhotoImage(main)
    Button(admin,image=admin.clearadmin,bd=0,command=clear_data).place(x=85,y=601)

    main=Image.open(r'D:\coding\project\pj\taadmin.png')
    admin.taadmin=ImageTk.PhotoImage(main)
    Button(admin,image=admin.taadmin,bd=0,command=createtable).place(x=438,y=600)

    main=Image.open(r'D:\coding\project\pj\saveadmin.png')
    admin.saveadmin=ImageTk.PhotoImage(main)
    Button(admin,image=admin.saveadmin,bd=0,command=save_data).place(x=90,y=536)

    main=Image.open(r'D:\coding\project\pj\showdataadmin.png')
    admin.showadmin=ImageTk.PhotoImage(main)
    Button(admin,image=admin.showadmin,bd=0,command=show_info).place(x=279,y=596)

    main=Image.open(r'D:\coding\project\pj\main_fix.png')
    admin.mainfix=ImageTk.PhotoImage(main)
    Button(admin,image=admin.mainfix,bd=0,command=fix_product_a).place(x=632,y=604)

    aet = Entry(admin,fg="black",bd=0,bg="#ffffff",font=('Tahoma',20),width=4)
    aet.place(x=405,y=548)

    overview()

    admin.mainloop()

def main_shop():
    
    def input_product_to_cart():
        # id = et.get()
        # quantity = int(et1.get())
        tel = et2.get()
        
        if len(tel) == 10 and tel.isdigit():
            
            id = et.get()

            if id:
                try:
                    quantity = int(et1.get())
                    if quantity:
                        cursor.execute("SELECT product_id, name, price FROM stock WHERE product_id=?", (id,))
                        result = cursor.fetchone()

                        # Continue with the rest of your code using 'id', 'quantity', and 'result'

                    else:
                        tkinter.messagebox.showinfo("แจ้งเตือน", "กรุณากรอกจำนวนสินค้า")
                except ValueError:
                    tkinter.messagebox.showinfo("แจ้งเตือน", "กรุณากรอกจำนวนสินค้าเป็นตัวเลข")
            else:
                tkinter.messagebox.showinfo("แจ้งเตือน", "กรุณากรอกชื่อสินค้า")

            if result:
                pid,name,price = result

            else:
                tkinter.messagebox.showinfo("แจ้งเตือน","ไม่มีสินค้า")
                return
            
        

            cursor.execute("SELECT quantity FROM stock WHERE name=?", (name,))
            stock_quantity = cursor.fetchone()
            
            if stock_quantity :
                stock_quantity = stock_quantity[0]

            if stock_quantity >= quantity:
                cursor.execute("SELECT quantity FROM cart WHERE name=? AND tel=?", (name, tel))
                cart_quantity = cursor.fetchone()

                if cart_quantity:
                    new_quantity = cart_quantity[0] + quantity
                    cursor.execute("UPDATE cart SET quantity = ? WHERE name = ? AND tel = ?", (new_quantity, name, tel))
                else:
                    cursor.execute("INSERT INTO cart (product_id,name, quantity, tel, price) VALUES (?, ?, ?, ?,?)", (pid,name, quantity, tel, price))


                cursor.execute("UPDATE stock SET quantity = quantity - ? WHERE name = ?", (quantity, name))
                conn.commit()
                
                et.delete(0, END)
                et1.delete(0, END)
                
            else:
                tkinter.messagebox.showinfo("แจ้งเตือน","ไม่สามารถเพิ่มรายการที่เลือก")
            re()
        else:
                tkinter.messagebox.showinfo("แจ้งเตือน","กรุณาใส่เบอร์ให้ถูกต้อง")
                
    def del_product_from_cart():
        name = et.get()
        quantity = int(et1.get())
        tel = et2.get()

        if len(tel) == 10 and tel.isdigit():
            cursor.execute("SELECT quantity FROM cart WHERE product_id=? AND tel=?", (name, tel))
            cart_quantity = cursor.fetchone()

            if cart_quantity:
                cart_quantity = cart_quantity[0]

                if quantity > 0 and quantity <= cart_quantity:

                    cursor.execute("UPDATE cart SET quantity = quantity - ? WHERE product_id = ? AND tel = ?", (quantity, name, tel))
                    cursor.execute("UPDATE stock SET quantity = quantity + ? WHERE product_id = ?", (quantity, name))
                    conn.commit()

                    cursor.execute("SELECT quantity FROM cart WHERE product_id = ? AND tel = ?", (name, tel))
                    cart_quantity = cursor.fetchone()

                    if cart_quantity:
                        cart_quantity = cart_quantity[0]

                        if cart_quantity <= 0:
                            cursor.execute("DELETE FROM cart WHERE product_id = ? AND tel = ?", (name, tel))
                            conn.commit()
                    else:
                        pass
                else:
                    tkinter.messagebox.showinfo("แจ้งเตือน", "จำนวนไม่ถูกต้อง")
            else:
                tkinter.messagebox.showinfo("แจ้งเตือน", f"{name} ไม่อยู่ในตะกร้า")

            re()
            et.delete(0, END)
            et1.delete(0, END)
        else:
            tkinter.messagebox.showinfo("แจ้งเตือน", "กรุณาใส่เบอร์ให้ถูกต้อง")
        
    def re():
        tel=et2.get()

        cursor.execute("SELECT SUM(stock.price * cart.quantity) FROM cart JOIN stock ON cart.name = stock.name WHERE cart.tel = ?", (tel,))
        total_price = cursor.fetchone()[0]

        Label(root,text=f"{total_price}",bd=0, bg="#fab548",width=10, font=('Tahoma',20)).place(x=200,y=618)

        showitem = tk.Listbox(root, width=48, height=18,bd=0, bg="#fff7e7", font=('Tahoma', 12))
        showitem.place(x=75,y=214)

        cursor.execute("SELECT product_id,name,quantity,price FROM cart WHERE tel=?", (tel,))
        cart_items = cursor.fetchall()
        
        if cart_items:
            showitem.delete(0, tk.END)

            for row in cart_items:
                row_info = f"{row[0]}.{row[1]} จำนวน : {row[2]} ราคาต่อชิ้น : {row[3]}"
                showitem.insert(tk.END, row_info)
        else:
            showitem.delete(0, tk.END)
            tkinter.messagebox.showinfo("แจ้งเตือน", "รายการของคุณว่างเปล่า")

        showproducts = tk.Listbox(root, width=30, height=25,bd=0, bg="#fff7e7", font=('Tahoma', 12))
        showproducts.place(x=928,y=115)

        cursor.execute("SELECT * FROM stock")
        products = cursor.fetchall()
        if products:
            showproducts.delete(0, tk.END)

            for row in products:
                row_info = f"{row[0]}.{row[1]} ราคา : {row[2]} จำนวน : {row[3]}"
                showproducts.insert(tk.END, row_info)
        else:
            showproducts.delete(0, tk.END)
            tkinter.messagebox.showinfo("แจ้งเตือน", "รายการของคุณว่างเปล่า")

    def pay():
        telephone = et2.get()

        def ok():
            date1 = datetime.now().strftime("%Y-%m-%d ")
            time = datetime.now().strftime("%H:%M:%S")

            cursor.execute("SELECT SUM(stock.price * cart.quantity) FROM cart JOIN stock ON cart.name = stock.name WHERE cart.tel = ?", (telephone,))
            total_prices = cursor.fetchone()[0]
            
            cursor.execute("SELECT name,quantity,price FROM cart WHERE tel=?", (telephone,))
            dataget = cursor.fetchall()

            if dataget:
                    for a in dataget:
                        n,q,p=a

                        cursor.execute("INSERT INTO history (name, quantity, price, tel,current_date,time_only) VALUES (?, ?, ?, ?, ?,?)", 
                            (n, q, total_prices, telephone, date1,time))

            cursor.execute("SELECT username FROM member WHERE tel=?", (telephone,))
            nameget = cursor.fetchone()

            if nameget:
                nameget=nameget[0]

            if total_prices:
                total_bill = total_prices

            optionget = None
            
            pdf(nameget,telephone,optionget,dataget,total_bill)

            cursor.execute("DELETE FROM cart WHERE tel = ?", (telephone,))
            conn.commit()
            tkinter.messagebox.showinfo("แจ้งเตือน", "ชำระเงินเรียบร้อยแล้ว")

        def payment(telephone):
            cursor.execute("SELECT SUM(stock.price * cart.quantity) FROM cart JOIN stock ON cart.name = stock.name WHERE cart.tel = ?", (telephone,))
            total_prices = cursor.fetchone()[0]

            total_bill = 0
            total_bill = total_prices
        
            if total_bill:
                total_bill = int(total_bill)

            else:
                tkinter.messagebox.showinfo("แจ้งเตือน", "รายการของคุณว่างเปล่า")

            return total_bill
        
        def bill():
            bills=Toplevel()
            bills.title("บิล")
            bills.geometry("500x600+145+25")

            def run(sum):

                Label(bills,text=f"{sum}",bg="#ffffff",font=('Tahoma', 20), ).place(x=348,y=480)

                showitem = tk.Listbox(bills, width=30, height=10,bd=0, bg="#fffae3", font=('Tahoma', 8))
                showitem.place(x=50,y=234)

                cursor.execute("SELECT name,quantity,price FROM cart WHERE tel=?", (telephone,))
                cart_items = cursor.fetchall()

                if cart_items:
                    showitem.delete(0, tk.END)

                    for row in cart_items:
                        row_info = f"ชื่อ : {row[0]}, จำนวน : {row[1]} , ราคา/ชิ้น : {row[2]}"
                        showitem.insert(tk.END, row_info)

            main=Image.open(r'D:\coding\project\pj\bill.png')
            bills.bb=ImageTk.PhotoImage(main)
            Label(bills,image=bills.bb).place(x=0,y=0)

            main=Image.open(r'D:\coding\project\pj\nice.png')
            bills.nn=ImageTk.PhotoImage(main)
            Button(bills,image=bills.nn,bd=0,command=ok).place(x=413,y=522)

            sum = payment(telephone)

            run(sum)

            text = "https://promptpay.io/0953929205/" + str(sum) + ".png"
            image_url = text

            response = requests.get(image_url)

            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                
                if image.mode != 'L':
                    image = image.convert('L')

                image = image.resize((int(image.width*0.5),int(image.height*0.5)))
                img_tk = ImageTk.PhotoImage(image)
                qr = Label(bills, image=img_tk)
                qr.image = img_tk  
                qr.place(x=155, y=434)

            else:
                print("Failed to download the image. HTTP status code:", response.status_code)

            bills.mainloop()
        
        bill()
        
    ##หลัก##########################

    root=Toplevel()
    root.title("ร้านค้า")
    root.geometry("1250x720+140+25")

    main=Image.open(r'D:\coding\project\pj\shop.png')
    root.shop=ImageTk.PhotoImage(main)
    Label(root,image=root.shop).place(x=0,y=0)

    et = Entry(root, fg="black",bd=0, bg="#fff7e7", font=('Tahoma',20), width=15)   #name
    et.place(x=611,y=255)
    et1 = Entry(root, fg="black",bd=0, bg="#fff7e7", font=('Tahoma',20), width=15)  #quantity
    et1.place(x=611,y=358)
    et2 = Entry(root, fg="black",bd=0, bg="#fab548", font=('Tahoma',20), width=21)  #tel
    et2.place(x=564,y=469)
    
    if total_tel is not None:
        et2.insert(0,total_tel)

    main=Image.open(r'D:\coding\project\pj\delshop.png')
    root.delshop=ImageTk.PhotoImage(main)
    Button(root,image=root.delshop,bd=0,command=del_product_from_cart).place(x=627,y=571)

    main=Image.open(r'D:\coding\project\pj\confirmshop.png')
    root.confirmshop=ImageTk.PhotoImage(main)
    Button(root,image=root.confirmshop,bd=0,command=input_product_to_cart).place(x=624,y=523)

    main=Image.open(r'D:\coding\project\pj\checkbill.png')
    root.checkbill=ImageTk.PhotoImage(main)
    Button(root,image=root.checkbill,bd=0,command=pay).place(x=622,y=616)

    main=Image.open(r'D:\coding\project\pj\reshop.png')
    root.reshop=ImageTk.PhotoImage(main)
    Button(root,image=root.reshop,bd=0,command=re).place(x=445,y=130)

    showproducts = tk.Listbox(root, width=30, height=25,bd=0, bg="#fff7e7", font=('Tahoma', 12))
    showproducts.place(x=928,y=115)

    cursor.execute("SELECT * FROM stock")
    products = cursor.fetchall()
    if products:
        showproducts.delete(0, tk.END)

        for row in products:
            row_info = f"{row[0]}.{row[1]} ราคา : {row[2]} จำนวน : {row[3]}"
            showproducts.insert(tk.END, row_info)
    else:
        showproducts.delete(0, tk.END)
        tkinter.messagebox.showinfo("แจ้งเตือน", "สต๊อกสินค้าว่างเปล่า.")

    root.mainloop()

def main_wash():
    
    def deldel():
        et.delete(0,END)
        et1.delete(0,END)
        et2c_var.set('')
        et3.delete(0,END)
        et4.delete(0,END)
        et5.delete(0,END)
        et6c_var.set('')
        et7.delete(0,END)

    def input_customer():
        now = datetime.today()
        name = et1.get()
        brand = et3.get()
        color = et4.get()
        lp = et5.get()
        pick = et6c_var.get()
        option = et2c_var.get()  
        tel=et7.get()
        
        if not name or not brand or not color or not lp or not pick or not option:
            tkinter.messagebox.showwarning("แจ้งเตือน", "โปรดกรอกค่าให้ครบทุกช่อง")

        else:
            name = et1.get()
            brand = et3.get()
            color = et4.get()

        if  brand.isalpha() and color.isalpha():
            lp = et5.get()

            if len(tel) == 10 and tel.isdigit():
                cash, op = 0, ''
                result_time = None

                if option == '':
                    tkinter.messagebox.showerror("แจ้งเตือน", "โปรดเลือกบริการที่ต้องการ.")
                    return 
                if pick == '':
                    tkinter.messagebox.showerror("แจ้งเตือน", "โปรดเลือกพนักงาน")
                    return 

                if option == 'a = ล้างภายนอกรถ ราคา 300 บาท':
                    op = 'a'
                elif option == 'b = ล้างภายในรถ ราคา 200 บาท':
                    op = 'b'
                elif option == 'c = ล้างทั้งภายนอกและภายในรถ ราคา 450 บาท':
                    op = 'c'
                elif option == 'd = ล้างรถมอเตอร์ไซค์ ราคา 120 บาท':
                    op = 'd'

                if op in car_prices:
                    cash = car_prices[op]
                    add_time = wash_time[op]
                    result_time = now + add_time
                    result_time_str = result_time.strftime("%H:%M:%S")
                    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("INSERT INTO client (name, brand, color, lp, option, pick, now, cash, time, tel) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (name,brand, color, lp, option, pick, now_str, cash, result_time_str,tel))
                conn.commit()
                tkinter.messagebox.showinfo("แจ้งเตือน", "บันทึกข้อมูลแล้ว\nวันที่มาลงทะเบียน: " + now.ctime())
                deldel()
            else:
                tkinter.messagebox.showinfo("แจ้งเตือน","กรุณาใส่เบอร์ให้ถูกต้อง")
                et7.delete(0,END)
        else:
            tkinter.messagebox.showwarning("แจ้งเตือน", "โปรดกรอก brand,color เป็นตัวอักษรเท่านั้น")
            

    def update_customer():
        conn.execute('''SELECT * FROM client''') 
        now = datetime.today()
        id = et.get()
        name = et1.get()
        brand = et3.get()
        color = et4.get()
        lp = et5.get()
        pick = et6c_var.get()
        option = et2c_var.get()
        cash, op = 0,''
        result_time = None

        if not name or not brand or not color or not lp or not pick or not option:
            tkinter.messagebox.showwarning("แจ้งเตือน", "โปรดกรอกค่าให้ครบทุกช่อง")

        else:
            name = et1.get()
            brand = et3.get()
            color = et4.get()

        if brand.isalpha() and color.isalpha():
                

            if option == 'a = ล้างภายนอกรถ ราคา 300 บาท':
                op = 'a'
            elif option == 'b = ล้างภายในรถ ราคา 200 บาท':
                op = 'b'
            elif option == 'c = ล้างทั้งภายนอกและภายในรถ ราคา 450 บาท':
                op = 'c'
            elif option == 'd = ล้างรถมอเตอร์ไซค์ ราคา 120 บาท':
                op = 'd'

            if op in car_prices:
                cash = car_prices[op]
                add_time = wash_time[op]
                result_time = now + add_time
                result_time_str = result_time.strftime("%H:%M:%S")
                now_str = now.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE client SET name=?, brand=?, color=?, lp=?, option=?, pick=?, now=?, cash=?, time=? WHERE id=?",
                    (name, brand, color, lp, option, pick, now_str, cash, result_time_str, id))

            conn.commit()
            tkinter.messagebox.showinfo("แจ้งเตือน", "แก้ไขข้อมูลแล้ว\nวันที่มาลงทะเบียน: " + now.ctime())
        else:
            tkinter.messagebox.showwarning("แจ้งเตือน", "โปรดกรอก name,brand,color เป็นตัวอักษรเท่านั้น")
    
    def show_cus_id():
        show = Toplevel(wash)
        show.title("show info")
        show.geometry("398x500")

        # Create a frame to hold the Treeview and scrollbar
        frame = ttk.Frame(show)
        frame.pack(fill="both", expand=True)

        # Create a custom style for the Treeview
        tree_style = ttk.Style()
        tree_style.configure("Custom.Treeview", font=("Helvetica", 12))  # Adjust the font style here

        # Create a Treeview widget with columns and apply the custom style
        columns = ("ID", "Name", "Time", "Cash")
        tree = ttk.Treeview(frame, columns=columns, show="headings", style="Custom.Treeview")

        # Add headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column("ID", width=2)
            tree.column("Name", width=30)
            tree.column("Time", width=20)
            tree.column("Cash", width=20)

        # Connect to the SQLite database
        conn = sqlite3.connect("clientdata.db")
        cursor = conn.cursor()

        cursor.execute('''SELECT id,name,time,cash FROM client''')
        clid = cursor.fetchall()
        if clid:
            for row in clid:
                tree.insert("", "end", values=row)
        else:
            tkinter.messagebox.showinfo("แจ้งเตือน", "รายการของคุณว่างเปล่า")
            
        # Create a vertical scrollbar
        vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vscrollbar.pack(side="right", fill="y")

        # Configure the Treeview to use the scrollbar
        tree.config(yscrollcommand=vscrollbar.set)

        # Pack the Treeview
        tree.pack(fill="both", expand=True)

        btn_close = tk.Button(show, width=10, text='Close', command=show.destroy)
        btn_close.pack()

        show.mainloop()

    def check():
        customer_id = et.get()
        if customer_id:
            cursor.execute("SELECT * FROM client WHERE id=?", (customer_id,))
            customer_data = cursor.fetchone()
            
            if customer_data:
                et1.delete(0,END)
                et1.insert(0, customer_data[1])  
                et2c_var.set(customer_data[5])  
                et3.delete(0,END)
                et3.insert(0, customer_data[2]) 
                et4.delete(0,END)
                et4.insert(0, customer_data[3])
                et5.delete(0,END)
                et5.insert(0, customer_data[4]) 
                et6c_var.set(customer_data[6])
                et7.insert(0, customer_data[10]) 

    def pay():
        
        telephone = et7.get()

        def ok():
            cursor.execute("SELECT name, brand, color, lp, option, pick, now, cash, time, tel FROM client WHERE tel=?", (telephone,))
            data1 = cursor.fetchone()

            if data1 :
                name, brand, color, lp, option, pick, now, cash, time, tel = data1

            if data1 :
                cursor.execute("INSERT INTO servicelist (name, brand, color, lp, option, pick, now, cash, time, tel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (name, brand, color, lp, option, pick, now, cash, time, telephone))
                
            cursor.execute("SELECT name,cash,option FROM client WHERE tel=?", (telephone,))
            op = cursor.fetchone()

            if op:
                nameget,cash1,optionget=op

            print(nameget,cash1,optionget)

            total_bill = cash1
            data= ''

            pdf(nameget,telephone,optionget,data,total_bill)

            cursor.execute("DELETE FROM client WHERE tel = ?", (telephone,))
            conn.commit()
            tkinter.messagebox.showinfo("แจ้งเตือน", "ชำระเงินเรียบร้อยแล้ว")
            
        def payment(telephone):
            print(telephone)
            cursor.execute("SELECT SUM(cash) FROM client WHERE tel=?",(telephone,))
            total_pricew = cursor.fetchone()[0] 
            total_bill = 0

            total_bill = total_pricew
        
            if total_bill:
                total_bill = int(total_bill)
            
            else:
                tkinter.messagebox.showinfo("แจ้งเตือน", "รายการของคุณว่างเปล่า")
            print(total_bill)

            return total_bill
        
        def bill():
            bills=Toplevel()
            bills.title("บิล")
            bills.geometry("500x600+145+25")
            def run(sum):

                Label(bills,text=f"{sum}",bg="#ffffff",font=('Tahoma', 20), ).place(x=348,y=480)

                showcar = tk.Listbox(bills, width=28, height=10,bd=0, bg="#fffae3", font=('Tahoma', 8))
                showcar.place(x=286,y=234)

                cursor.execute("SELECT brand,cash FROM client WHERE tel=?", (telephone,))
                car_item = cursor.fetchall()

                showcar.delete(0, tk.END)

                if car_item:
                    for row in car_item:
                        row_info = f"แบรนด์ : {row[0]}, ราคา : {row[1]}"
                        showcar.insert(tk.END, row_info)
                else:
                    pass

            main=Image.open(r'D:\coding\project\pj\bill.png')
            bills.bb=ImageTk.PhotoImage(main)
            Label(bills,image=bills.bb).place(x=0,y=0)

            main=Image.open(r'D:\coding\project\pj\nice.png')
            bills.nn=ImageTk.PhotoImage(main)
            Button(bills,image=bills.nn,bd=0,command=ok).place(x=413,y=522)

            sum = payment(telephone)
            if sum:
                run(sum)
                text = "https://promptpay.io/0953929205/" + str(sum) + ".png"
                image_url = text

                response = requests.get(image_url)

                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    
                    if image.mode != 'L':
                        image = image.convert('L')

                    image = image.resize((int(image.width*0.5),int(image.height*0.5)))
                    img_tk = ImageTk.PhotoImage(image)
                    qr = Label(bills, image=img_tk)
                    qr.image = img_tk  
                    qr.place(x=155, y=434)

                else:
                    print("Failed to download the image. HTTP status code:", response.status_code)

                Button(bills,width=20,height=20,bg="black",command=ok).place(x=500,y=500)
            
            bills.mainloop()
        
        bill()

    
    wash = Toplevel()
    wash.title("99 Car Wash ")
    wash.geometry("1366x768+80+10")
    
    main=Image.open(r'D:\coding\project\pj\menu1.png')
    wash.bgm=ImageTk.PhotoImage(main)
    Label(wash,image=wash.bgm).place(x=0,y=0)

    main=Image.open(r'D:\coding\project\pj\save bt.png')
    wash.btsave=ImageTk.PhotoImage(main)
    Button(wash,image=wash.btsave,bd=0,command=input_customer).place(x=835,y=486)

    main=Image.open(r'D:\coding\project\pj\show bt.png')
    wash.btshow=ImageTk.PhotoImage(main)
    Button(wash,image=wash.btshow,bd=0,command=show_cus_id).place(x=615,y=632)

    main=Image.open(r'D:\coding\project\pj\pay bt.png')
    wash.pay=ImageTk.PhotoImage(main)
    Button(wash,image=wash.pay,bd=0,command=pay).place(x=838,y=636)

    main=Image.open(r'D:\coding\project\pj\fix bt.png')
    wash.btfix=ImageTk.PhotoImage(main)
    Button(wash,image=wash.btfix,bd=0,command=update_customer).place(x=328,y=632)

    main=Image.open(r'D:\coding\project\pj\clear bt.png')
    wash.btclear=ImageTk.PhotoImage(main)
    Button(wash,image=wash.btclear,bd=0,command=deldel).place(x=35,y=632)

    main=Image.open(r'D:\coding\project\pj\check bt.png')
    wash.btcheck=ImageTk.PhotoImage(main)
    Button(wash,image=wash.btcheck,bd=0,command=check).place(x=1060,y=574)

    et1 = Entry(wash,fg="black",bd=0,bg="#ffffff",font=('Tahoma',20),width=20)  #name
    et1.place(x=224,y=214)

    # et2c_var = tk.StringVar() 
    # et2c = ttk.Combobox(wash,font=('Tahoma',20),width=20,textvariable=et2c_var) #car_type
    # et2c['values'] = ('a = ล้างภายนอกรถ ราคา 300 บาท','b = ล้างภายในรถ ราคา 200 บาท','c = ล้างทั้งภายนอกและภายในรถ ราคา 450 บาท','d = ล้างรถมอเตอร์ไซค์ ราคา 120 บาท')
    # et2c.place(x=294,y=318)

    et3 = Entry(wash,fg="black",bd=0,bg="#ffffff",font=('Tahoma',20),width=20)  #brand
    et3.place(x=904,y=316)

    et4 = Entry(wash,fg="black",bd=0,bg="#ffffff",font=('Tahoma',20),width=20)  #color
    et4.place(x=273,y=412)

    et5 = Entry(wash,fg="black",bd=0,bg="#ffffff",font=('Tahoma',20),width=15)  #lp
    et5.place(x=1067,y=420)

    # et6c_var = tk.StringVar() 
    # et6c = ttk.Combobox(wash,font=('Tahoma',20),width=15,textvariable=et6c_var)
    # et6c['values'] = ('นางสาวบรรณิศา พันธุ์ฟุ้ง 653050423-3','นายชนกันต์ เครือสิงห์ 653050417-8')
    # et6c.place(x=331,y=518)

    et = Entry(wash,fg="black",bd=0,bg="#ffffff",font=('Tahoma',20),width=4)  #id
    et.place(x=1144,y=672)

    

    et7 = Entry(wash,fg="black",bd=0,bg="#ffffff",font=('Tahoma',20),width=20)  #tel
    et7.place(x=857,y=213)

    if total_tel is not None:
        et7.insert(0,total_tel)

    def set_value(et_var, value):
        et_var.set(value)

    et2c_var = tk.StringVar()
    value_label_et2c = tk.Label(wash, textvariable=et2c_var, font=('Tahoma', 20))
    value_label_et2c.place(x=200, y=260)

    et6c_var = tk.StringVar()
    value_label_et6c = tk.Label(wash, textvariable=et6c_var, font=('Tahoma', 20))
    value_label_et6c.place(x=300, y=580)

    def create_button_with_image(x, y, image_path, value, et_var):
        img = PhotoImage(file=image_path)
        button = tk.Button(wash, image=img, command=lambda: set_value(et_var, value))
        button.image = img  # Important to keep the reference to the image
        button.place(x=x, y=y)

    # Create buttons with images for et2c_var
    create_button_with_image(270, 310, r'D:\coding\project\pj\outwashcar.png', 'a = ล้างภายนอกรถ ราคา 300 บาท', et2c_var)
    create_button_with_image(370, 310, r'D:\coding\project\pj\inwashcar.png', 'b = ล้างภายในรถ ราคา 200 บาท', et2c_var)
    create_button_with_image(470, 310, r'D:\coding\project\pj\bothwashcar.png', 'c = ล้างทั้งภายนอกและภายในรถ ราคา 450 บาท', et2c_var)
    create_button_with_image(570, 310, r'D:\coding\project\pj\motorbikewash.png', 'd = ล้างรถมอเตอร์ไซค์ ราคา 120 บาท', et2c_var)

    # Create buttons with images for et6c_var
    create_button_with_image(440, 510, r'D:\coding\project\pj\bunnie.png', 'นางสาวบรรณิศา พันธุ์ฟุ้ง 653050423-3', et6c_var)
    create_button_with_image(500, 510, r'D:\coding\project\pj\newines.png', 'นายชนกันต์ เครือสิงห์ 653050417-8', et6c_var)

    # wash.mainloop()

    wash.mainloop()

def main_car_wash_program():
    mains=tk.Tk()
    mains.title("ร้านหลัก")
    mains.geometry("1366x768+80+10")

    main=Image.open(r'D:\coding\project\pj\main.png')
    mains.main=ImageTk.PhotoImage(main)
    Label(mains,image=mains.main).place(x=0,y=0)

    main=Image.open(r'D:\coding\project\pj\mlogin.png')
    mains.mlogin=ImageTk.PhotoImage(main)
    Button(mains,image=mains.mlogin,bd=0,command=main_member).place(x=834,y=278)

    main=Image.open(r'D:\coding\project\pj\mwash.png')
    mains.mwash=ImageTk.PhotoImage(main)
    Button(mains,image=mains.mwash,bd=0,command=main_wash).place(x=836,y=429)

    main=Image.open(r'D:\coding\project\pj\mshop.png')
    mains.mshop=ImageTk.PhotoImage(main)
    Button(mains,image=mains.mshop,bd=0,command=main_shop).place(x=837,y=560)

    clock = None

    # Function to update the time
    def runTime():
        
        timeString = strftime("%d %B %Y\n%H:%M:%S %p")
        if clock:
            clock.config(text=timeString)
        mains.after(1000, runTime)

    # Create the clock label
    clock = tk.Label(mains, font=("DB HELVETHAICAMON X BD", 20), justify=tk.CENTER, fg="black", bg="white")
    clock.place(x=1120, y=8)
    runTime()

    # Get and display the date
    day = strftime("%d")
    month = strftime("%B")
    year = strftime("%Y")
    date = str(day + "/" + month + "/" + year)
    # tk.Label(mains, text=date, font=("Bebas Neue Regular", 20), bg="#e8dfab", fg="#307d9b").place(x=200, y=72)

    
    
    # btn_close = tk.Button(mains, width=10, text='Close', command=mains.destroy)
    # btn_close.pack()

    mains.mainloop()

def user_main(username):
    user=Toplevel()
    user.title("หน้าหลักลูกค้า")
    user.geometry("1250x720+145+25")

    main=Image.open(r'D:\coding\project\pj\usermain.png')
    user.usermain=ImageTk.PhotoImage(main)
    Label(user,image=user.usermain).place(x=0,y=0)

    def pay():
        cursor.execute("SELECT tel FROM member WHERE username = ?",(username,))
        telephone = cursor.fetchone()
        if telephone:
            telephone=telephone[0]

        def ok():
            date1 = datetime.now().strftime("%Y-%m-%d ")
            time = datetime.now().strftime("%H:%M:%S")
            cursor.execute("SELECT SUM(stock.price * cart.quantity) FROM cart JOIN stock ON cart.name = stock.name WHERE cart.tel = ?", (telephone,))
            total_prices = cursor.fetchone()[0]
            
            cursor.execute("SELECT name, quantity,price FROM cart WHERE tel=?", (telephone,))
            dataget = cursor.fetchall()
            if dataget:
                for d in dataget:
                    n,q,p = d

            cursor.execute("INSERT INTO history (name, quantity, price, tel,current_date,time_only) VALUES (?, ?, ?, ?, ?,?)", 
                               (n, q, total_prices, telephone, date1,time))
            
            cursor.execute("SELECT name, brand, color, lp, option, pick, now, cash, time, tel FROM client WHERE tel=?", (telephone,))
            data1 = cursor.fetchone()
            
            if data1 :
                name, brand, color, lp, option, pick, now, cash, time, tel = data1
            else:
                pass
            
            if data1 :
                cursor.execute("INSERT INTO servicelist (name, brand, color, lp, option, pick, now, cash, time, tel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (name, brand, color, lp, option, pick, now, cash, time,telephone))

            cursor.execute("SELECT username FROM member WHERE tel=?", (telephone,))
            nameget = cursor.fetchone()

            if nameget:
                nameget=nameget[0]

            cursor.execute("SELECT cash FROM client WHERE tel=?", (telephone,))
            cash1 = cursor.fetchone()

            if cash1 :
                cash1 = float(cash1[0])


            if total_prices is None:
                total_billg = cash1
                
            elif cash1 is None:
                total_billg = total_prices

            else:
                total_billg = total_prices + cash1
                print(f"เช็ค {total_bill}")

            cursor.execute("SELECT option FROM client WHERE tel=?", (telephone,))
            optionget = cursor.fetchone()
            
            pdf(nameget,telephone,optionget,dataget,total_billg)
            
            cursor.execute("DELETE FROM cart WHERE tel = ?", (telephone,))
            cursor.execute("DELETE FROM client WHERE tel = ?", (telephone,))
            conn.commit()
        
            total_tel = ''
            tkinter.messagebox.showinfo("แจ้งเตือน", "ชำระเงินเรียบร้อยแล้ว")

        def payment(telephone):
            telephone
            print(f" เบอร์ {telephone}")
            cursor.execute("SELECT SUM(stock.price * cart.quantity) FROM cart JOIN stock ON cart.name = stock.name WHERE cart.tel = ?", (telephone,))
            total_prices = cursor.fetchone()[0]

            cursor.execute("SELECT SUM(cash) FROM client WHERE tel=?",(telephone,))
            total_pricew = cursor.fetchone()[0] 

            total_bill = 0

            print(total_prices)
            print(total_pricew)

            if total_prices is None:
                total_bill=total_pricew

            elif total_pricew is None:
                total_bill=total_prices

            else :
                total_bill = total_prices + total_pricew
                print(f" gg gg {total_bill}")
        
            if total_bill:
                total_bill = int(total_bill)
            
                
            else:
                tkinter.messagebox.showinfo("แจ้งเตือน", "รายการของคุณว่างเปล่า")

            if total_bill > 2000:
                discount_percent = 15
            elif total_bill > 1000:
                discount_percent = 8
            else:
                discount_percent = 0

            discount = (total_bill * discount_percent) / 100
            print(f"เต็ม {total_bill}")
            print(f"ลด {discount}")

            total_bill-=discount
            return total_bill
    
        
        def bill():
            bills=Toplevel()
            bills.title("บิล")
            bills.geometry("500x600+145+25")

            def run(sum):

                Label(bills,text=f"{sum}",bg="#ffffff",font=('Tahoma', 20), ).place(x=348,y=480)

                showitem = tk.Listbox(bills, width=30, height=10,bd=0, bg="#fffae3", font=('Tahoma', 8))
                showitem.place(x=50,y=234)

                cursor.execute("SELECT name,quantity,price FROM cart WHERE tel=?", (telephone,))
                cart_items = cursor.fetchall()

                if cart_items:
                    showitem.delete(0, tk.END)

                    for row in cart_items:
                        row_info = f"ชื่อ : {row[0]}, จำนวน : {row[1]} , ราคา/ชิ้น : {row[2]}"
                        showitem.insert(tk.END, row_info)
                else:
                    pass

                showcar = tk.Listbox(bills, width=28, height=10,bd=0, bg="#fffae3", font=('Tahoma', 8))
                showcar.place(x=286,y=234)

                cursor.execute("SELECT brand,cash FROM client WHERE tel=?", (telephone,))
                car_item = cursor.fetchall()
                showcar.delete(0, tk.END)

                if car_item:
                    for row in car_item:
                        row_info = f"แบรนด์ : {row[0]}, ราคา : {row[1]}"
                        showcar.insert(tk.END, row_info)
                else:
                    pass
 
            main=Image.open(r'D:\coding\project\pj\bill.png')
            bills.bb=ImageTk.PhotoImage(main)
            Label(bills,image=bills.bb).place(x=0,y=0)
            
            sum = payment(telephone)
            run(sum)
            if sum:
                print(sum)
                text = "https://promptpay.io/0953929205/" + str(sum) + ".png"
                image_url = text

                response = requests.get(image_url)

                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    
                    if image.mode != 'L':
                        image = image.convert('L')

                    image = image.resize((int(image.width*0.5),int(image.height*0.5)))
                    img_tk = ImageTk.PhotoImage(image)
                    qr = Label(bills, image=img_tk)
                    qr.image = img_tk  
                    qr.place(x=155, y=434)

                else:
                    print("Failed to download the image. HTTP status code:", response.status_code)

                main=Image.open(r'D:\coding\project\pj\nice.png')
                bills.nn=ImageTk.PhotoImage(main)
                Button(bills, image=bills.nn, bd=0, command=ok).place(x=413, y=522)

            bills.mainloop()
        
        bill()

    def sun():
        showitem = tk.Listbox(user, width=20, height=10,bd=0, bg="#ffffff", font=('Tahoma', 12))
        showitem.place(x=325,y=264)

        showcar = tk.Listbox(user, width=20, height=10,bd=0, bg="#ffffff", font=('Tahoma', 12))
        showcar.place(x=100,y=264)

        cursor.execute("SELECT SUM(stock.price * cart.quantity) FROM cart JOIN stock ON cart.name = stock.name WHERE tel=?",(telephone,))
        total_prices = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(cash) FROM client WHERE tel=?",(telephone,))
        total_pricew = cursor.fetchone()[0] 

        total_bill = 0

        if total_prices is None:
            total_bill=total_pricew

        elif total_pricew is None:
            total_bill=total_prices

        else :
            total_bill = total_prices + total_pricew
    
        if total_bill:
            total_bill = int(total_bill)
        print(total_bill)

        Label(user,text=f"{total_bill}",bg="#fab548",font=('Tahoma', 12), ).place(x=133,y=536)

        cursor.execute("SELECT name,quantity,price FROM cart WHERE tel=?", (telephone,))
        cart_items = cursor.fetchall()

        if cart_items:
            showitem.delete(0, tk.END)
            for row in cart_items:
                row_info = f"ชื่อ : {row[0]}, จำนวน : {row[1]} , ราคา/ชิ้น : {row[2]}"
                showitem.insert(tk.END, row_info)
    
        cursor.execute("SELECT brand,cash FROM client WHERE tel=?", (telephone,))
        car_item = cursor.fetchall()
        
        if car_item:
            showcar.delete(0, tk.END)
            for row in car_item:
                row_info = f"แบรนด์ : {row[0]}, ราคา : {row[1]}"
                showcar.insert(tk.END, row_info)
 
    main=Image.open(r'D:\coding\project\pj\usershop.png')
    user.usershop=ImageTk.PhotoImage(main)
    Button(user,image=user.usershop,bd=0,command=main_shop).place(x=901,y=374)

    main=Image.open(r'D:\coding\project\pj\userwash.png')
    user.userwash=ImageTk.PhotoImage(main)
    Button(user,image=user.userwash,bd=0,command=main_wash).place(x=873,y=481)

    main=Image.open(r'D:\coding\project\pj\userbill.png')
    user.userbill=ImageTk.PhotoImage(main)
    Button(user,image=user.userbill,bd=0,command=pay).place(x=833,y=582)  
    
    cursor.execute("SELECT tel FROM member WHERE username = ?",(username,))
    telephone = cursor.fetchone()
    
    if telephone:
        telephone = telephone[0]

    global total_tel
    total_tel = telephone

    Label(user,text=f"{username}",bg="#fff7e7",font=('Tahoma', 20), ).place(x=931,y=194)
    Label(user,text=f"{telephone}",bg="#fab548",font=('Tahoma', 18), ).place(x=891,y=303)

    main=Image.open(r'D:\coding\project\pj\reshop.png')
    user.rs=ImageTk.PhotoImage(main)
    Button(user,image=user.rs,bd=0,command=sun).place(x=458,y=133) 
    sun()

    user.mainloop()

main_car_wash_program()

conn.close()