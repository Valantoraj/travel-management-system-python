from PIL import ImageTk, Image
from customtkinter import *
from tkinter import ttk, messagebox, Canvas
import sqlite3
import regex as re
import smtplib
from random import *
import mainlayout


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.resizable(0, 0)
        set_appearance_mode("dark")

        # sql
        self.conn = sqlite3.connect('user_details.db')
        self.c = self.conn.cursor()
        self.c.execute('''
              CREATE TABLE IF NOT EXISTS user_details(
                  uname TEXT,
                  password TEXT,
                  secret_code TEXT,
                  name TEXT,
                  email TEXT
              )
              ''')
        self.conn.commit()
        self.c.execute("SELECT * FROM user_details")
        print(self.c.fetchall())

        # bg image
        bg_img = Image.open("Rectangl.jpg")
        new_img = bg_img.resize((2000, 1500))
        bg_img = ImageTk.PhotoImage(new_img)

        self.canvas = Canvas(self.root, width=1536, height=836)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor=NW, image=bg_img)

        # image
        backsdull_img = Image.open("backsdull.jpg")
        backsdull_img = ImageTk.PhotoImage(backsdull_img)
        self.canvas.create_image(240, 196, anchor=NW, image=backsdull_img)

        self.login_page()
        self.conn.commit()
        self.root.mainloop()
        self.conn.close()

    def pwd_checker(self, pwd):
        if len(pwd) < 8:
            messagebox.showerror("Credential Error!", "Password should be at least 8 characters long")
            return False
        elif not re.search("[a-z]", pwd):
            messagebox.showerror("Credential Error!", "You should include at least one lowercase letter")
            return False
        elif not re.search("[A-Z]", pwd):
            messagebox.showerror("Credential Error!", "You should include at least one uppercase letter")
            return False
        elif not re.search("[0-9]", pwd):
            messagebox.showerror("Credential Error!", "You should include at least one numerical value")
            return False
        elif not re.search("[_@$]", pwd):
            messagebox.showerror("Credential Error!", "You should include at least one among '_@$'")
            return False
        elif re.search(r"\s", pwd):
            messagebox.showerror("Credential Error!", "There should be no spaces or breaks")
            return False
        else:
            return True

    def email_checker(self, email):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return True
        return False

    def login_check(self, user_id_l, password_l, frame1):
        uid = user_id_l.get()
        self.c.execute("SELECT * FROM user_details WHERE uname=(?)", (uid,))
        if not uid:
            messagebox.showerror("Credential Error!", "User Id is not entered!")
            return
        elif self.c.fetchone() is None:
            response = messagebox.askyesno("Credential Error!", "User Id Doesn't Exists You Want To Sign Up?")
            if response:
                self.sign_up_page(frame1)
            else:
                user_id_l.delete(0, 'end')
                password_l.delete(0, 'end')
            return False

        pwd = password_l.get()
        if not pwd:
            messagebox.showerror("Credential Error!", "Password is not entered!")
            return
        print(uid)
        self.c.execute("SELECT * FROM user_details WHERE uname=(?)", (uid,))
        if self.c.fetchone()[1] != pwd and pwd:
            response_pass = messagebox.askyesno("Credential Error!", "Password Is Incorrect Please Try Again or Do You Want To Reset!")
            if response_pass:
                self.reset_call(uid, frame1)
            else:
                password_l.delete(0, 'end')
            return False
        self.c.execute("SELECT rowid FROM user_details where uname=(?)", (uid,))
        rid = self.c.fetchone()[0]
        mainlayout.login_to_main(self.root, frame1, self.canvas, uid, rid)

    def login_page(self):
        frame1 = CTkFrame(master=self.root, height=650, width=400)
        frame1.place(relx=0.75, rely=0.485, anchor='center')

        CTkLabel(master=frame1, text="").pack(expand=True, pady=10)

        login_label = CTkLabel(master=frame1, text="Login", font=("Helvetica", 24))
        login_label.pack(expand=True, pady=5, padx=30)

        CTkLabel(master=frame1, text="").pack(expand=True, pady=15)

        user_id_l = CTkEntry(master=frame1, placeholder_text="User Id", height=35, width=235, corner_radius=20)
        user_id_l.pack(expand=True, pady=12, padx=90)

        password_l = CTkEntry(master=frame1, placeholder_text="password", height=35, width=235, corner_radius=20, show="*")
        password_l.pack(expand=True, pady=25, padx=70)

        login = CTkButton(master=frame1, text="Login", height=35, width=235, corner_radius=30, fg_color="#356755", command=lambda: self.login_check(user_id_l, password_l, frame1))
        login.pack(expand=True, pady=20, padx=70)

        CTkLabel(master=frame1, text="Create Your New Account?").pack(expand=True)

        sign_up_l = CTkButton(master=frame1, text="Sign Up", height=35, width=235, corner_radius=30, fg_color="#356755", command=lambda: self.sign_up_page(frame1))
        sign_up_l.pack(expand=True, pady=15, padx=70)

        CTkLabel(master=frame1, text="").pack(expand=True, pady=20)
        frame1.lift()

    def reset_call(self, uname, frame1):
        messagebox.showinfo("Please wait!","Sending OTP via registered email id.")
        frame1.destroy()
        OTP = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
        self.c.execute("SELECT email FROM user_details WHERE uname=(?)", (uname,))
        code_reset_db = (self.c.fetchone()[0])

        # otp
        receiver = code_reset_db
        sender = 'traveleasypy@gmail.com'
        sender_pwd = 'etjz keuf xudf kodp'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, sender_pwd)
        message = f'Subject: Your OTP\n\nYour OTP is: {OTP}'
        server.sendmail(sender, receiver, message)
        server.quit()

        print(code_reset_db)

        def reset_pwd():
            if not code_reset_val.get():
                messagebox.showerror("Credential Error!", "Enter your code!")
                return
            if code_reset_val.get() != OTP:
                messagebox.showerror("Credential Error!", "OTP Is Incorrect")
                return
            if code_reset_val.get() == OTP:

                def pwd_change():
                    new_password = new_pwd.get()
                    if not new_password:
                        messagebox.showerror("Credential Error!", "Enter the new password!")
                        return
                    if not self.pwd_checker(new_password):
                        return
                    self.c.execute("UPDATE user_details SET password=(?) WHERE uname=(?)", (new_password, uname))
                    self.conn.commit()
                    messagebox.showinfo("Status info", "The password had been changed")
                    self.login_page()

                frame3.destroy()

                frame4 = CTkFrame(master=self.root, height=650, width=700)
                frame4.place(relx=0.75, rely=0.485, anchor='center')
                CTkLabel(master=frame4, text="").pack(expand=True, pady=53)
                reset_label2 = CTkLabel(master=frame4, text="Reset password", font=("Helvatica", 24))
                reset_label2.pack(expand=True, padx=88)
                CTkLabel(master=frame4, text="").pack(expand=True, pady=20)
                new_pwd = CTkEntry(master=frame4, placeholder_text="New password", height=35, width=235, corner_radius=20)
                new_pwd.pack(expand=True, pady=10, padx=88)
                submit_new_pwd = CTkButton(master=frame4, text="Submit", height=35, width=235, corner_radius=30, command=pwd_change)
                submit_new_pwd.pack(expand=True, pady=35, padx=88)
                CTkLabel(master=frame4, text="").pack(expand=True, pady=53)

        frame3 = CTkFrame(master=self.root, height=650, width=700)
        frame3.place(relx=0.75, rely=0.485, anchor='center')

        CTkLabel(master=frame3, text="").pack(expand=True, pady=42)

        reset_label = CTkLabel(master=frame3, text="Reset password", font=("Helvatica", 24))
        reset_label.pack(expand=True, pady=35, padx=88)

        code_reset_val = CTkEntry(master=frame3, placeholder_text="OTP", height=35, width=235, corner_radius=20)
        code_reset_val.pack(expand=True, pady=50, padx=88)

        submit_reset = CTkButton(master=frame3, text="Submit", height=35, width=235, corner_radius=30, command=reset_pwd)
        submit_reset.pack(expand=True, pady=15)

        CTkLabel(master=frame3, text="").pack(expand=True, pady=42)

    def sign_up_page(self, frame1):
        frame1.destroy()
        frame2 = CTkFrame(master=self.root, height=526, width=415)
        frame2.place(relx=0.75, rely=0.485, anchor='center')

        CTkLabel(master=frame2, text="").pack(expand=True, pady=23)

        sign_up_label = CTkLabel(master=frame2, text="Sign Up", font=("Helvetica", 24))
        sign_up_label.pack(expand=True, pady=5, padx=30)

        CTkLabel(master=frame2, text="").pack(expand=True)

        user_id_s = CTkEntry(master=frame2, placeholder_text="User Id", height=35, width=235, corner_radius=20)
        user_id_s.pack(expand=True, pady=10, padx=90)

        password_s = CTkEntry(master=frame2, placeholder_text="Password", height=35, width=235, corner_radius=20, show="*")
        password_s.pack(expand=True, pady=10, padx=70)

        secret_code_s = CTkEntry(master=frame2, placeholder_text="Phone number", height=35, width=235, corner_radius=20)
        secret_code_s.pack(expand=True, pady=10, padx=70)

        name_s = CTkEntry(master=frame2, placeholder_text="Name", height=35, width=235, corner_radius=20)
        name_s.pack(expand=True, pady=10, padx=70)

        email_s = CTkEntry(master=frame2, placeholder_text="Email", height=35, width=235, corner_radius=20)
        email_s.pack(expand=True, pady=10, padx=70)

        sign_up = CTkButton(master=frame2, text="Sign Up", height=35, width=235, corner_radius=30, fg_color="#356755", command=lambda: self.sign_up_check(user_id_s, password_s, secret_code_s, name_s, email_s))
        sign_up.pack(expand=True, pady=35, padx=70)

        self.root.bind("<Return>", lambda event: self.sign_up_check(user_id_s, password_s, secret_code_s, name_s, email_s))

    def sign_up_check(self, user_id_s, password_s, secret_code_s, name_s, email_s):
        uid = user_id_s.get()
        if not uid:
            messagebox.showerror("Credential Error!", "Enter Your User Name!")
            return
        if 4 > len(uid) or len(uid) > 10:
            print(uid)
            messagebox.showerror("Credential Error!", "Username should be 4-16 characters long!")
            return
        pwd = password_s.get()
        print(pwd)
        if not pwd:
            messagebox.showerror("Credential Error!", "Enter Your Password!")
            return
        if not self.pwd_checker(pwd):
            return
        code = secret_code_s.get()
        print(code)
        if not code:
            messagebox.showerror("Credential Error!", "Enter Your Phone number!")
            return
        if 4 > len(code) or len(code) > 10:
            messagebox.showerror("Credential Error!", "The secret code should be 4-10 characters long!")
            return
        user_name = name_s.get()
        print(user_name)
        if not user_name:
            messagebox.showerror("Credential Error!", "Name is not entered!")
        user_email = email_s.get()
        print(user_email)
        if not user_email:
            messagebox.showerror("Credential Error!", "Enter Your Email!")
            return
        if not self.email_checker(user_email):
            messagebox.showerror("Credential Error!", "Invalid email format!")
            return

        self.c.executemany("INSERT INTO user_details VALUES(?,?,?,?,?)", [(uid, pwd, code, user_name, user_email)])
        self.conn.commit()

        user_id_s.delete(0, 'end')
        password_s.delete(0, 'end')
        secret_code_s.delete(0, 'end')
        name_s.delete(0, 'end')
        email_s.delete(0, 'end')
        self.login_page()


root = CTk()
app = MyApp(root)
