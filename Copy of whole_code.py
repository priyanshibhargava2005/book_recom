################################ IMPORT MODULES ################################

import tkinter as tk
import mysql.connector as m
from tkinter import messagebox
from PIL import Image, ImageTk
import PIL
import random as r
import webbrowser
from itertools import count, cycle

################################## THANKS PAGE #################################

def thanks():
    thank= tk.Tk()
    thank.title("findmeabook.org")
    thank.geometry("1920x1080")

    #can1
    can_thanks=tk.Canvas(thank,width=700,height=500)
    can_thanks.pack(fill="both",expand=True)

    #bgimage
    bg= tk.PhotoImage(master= thank, file= ('image.ppm'))
    can_thanks.create_image(0,0, image= bg,anchor="nw")

    #logo
    img=tk.PhotoImage(master=thank,file="logo.ppm") 
    logolab=tk.Label(thank,image=img,borderwidth = 5, relief="solid")
    logolab_can=can_thanks.create_window(720,127,window=logolab)

    #button
    button1 = tk.Button(can_thanks, text = "Exit",width=10,height=3,
                        fg="#2C041C",font="georgia",
                        bg="#E0D3AF",borderwidth = 5, relief="sunken",command=thank.destroy)
    button1.pack(pady = 20)
    button1.place(x=650,y=600)

    #line
    can_thanks.create_line(0,250,2000,250, fill="#B39861", width=5)

    #gif
    class ImageLabel(tk.Label):
        def load(self, im):
            if isinstance(im, str):
                im= PIL.Image.open(im)
            frames= []

            try:
                for i in count(1):
                    frames.append(ImageTk.PhotoImage(im.copy()))
                    im.seek(i)
            except EOFError:
                pass
            self.frames= cycle(frames)

            try:
                self.delay= im.info['duration']
            except:
                self.delay= 100

            if len(frames)==1:
                self.config(image=next(self.frames))
            else:
                self.next_frame()

        def unload(self):
            self.config(image=None)
            self.frames= None

        def next_frame(self):
            if self.frames:
                self.config(image=next(self.frames))
                self.after(self.delay, self.next_frame)
    def back_to_spec():
        thank.destroy()
        sign_login()
    back_button = Button(can_thanks, text = "Back",
                        width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=back_to_spec)
    back_button.place(x=550,y=560)

    lbl= ImageLabel(can_thanks)
    lbl.pack()
    lbl.place(x= 550, y=280)
    lbl.load("ty.gif")

    #end
    thank.mainloop()

################################# BOOK DETAILS #################################

def page6(name1):
    #connection
    mydb=m.connect(host="localhost",database="project",user="root")
    cursor=mydb.cursor()
    #window assignment
    p6=tk.Toplevel()
    p6.geometry("1271x500")
    p6.title(name1)
    c6=tk.Canvas(p6,width=1000,height=700)
    c6.pack(fill="both",expand=True)

    #logo
    img2 =tk.PhotoImage(master=p6,file="logo.ppm") 
    logolab=tk.Label(p6,image=img2,borderwidth = 5, relief="solid")
    logolab_c6=c6.create_window(1042,176,window=logolab)

    #background image
    img =tk.PhotoImage(master=p6,file="image.ppm") 
    c6.create_image(0,0,image=img,anchor="nw")
    
    #fetching the book code
    n=(name1,)
    cursor.execute("SELECT bcode FROM books WHERE bname=%s", n)
    bcode=cursor.fetchone()
    #fetching the coverpage
    cursor.execute("SELECT covp FROM coverpage WHERE bcode=%s",bcode)
    cover_page= cursor.fetchone()
    #displaying the coverpage
    for c in cover_page:
        cov_img=PIL.Image.open(c)
        c_img=cov_img.resize((100,140))
        c6.covp_img=ImageTk.PhotoImage(c_img)
        coverpage=c6.covp_img
        img_lab=tk.Label(c6,image=coverpage)
        img_window=c6.create_window(100,50,anchor="nw",window=img_lab)
    #fetching the genre
    cursor.execute("SELECT genre FROM books WHERE bcode=%s", (bcode))
    genre= cursor.fetchone()
    for gen in genre:
        g= tk.Label(p6, text= gen,height=2,width=15,
                 bg="#D0A373", fg="#2C041C",anchor="center",font="Times 14",
                 borderwidth = 3, relief="solid", highlightcolor="red")
        g_window=c6.create_window(250,50,anchor="nw",window=g)
    #fetching the author
    cursor.execute("SELECT author FROM books WHERE bcode=%s", (bcode))
    author= cursor.fetchone()
    for aut in author:
        a= tk.Label(p6, text= aut,bg="#D0A373", fg="#2C041C",
                 anchor="center",font="Times 14",height=2,width=35,
                 borderwidth = 3, relief="solid", highlightcolor="red")
        a_window=c6.create_window(250,108,anchor="nw",window=a)
    #fetching the publisher
    cursor.execute("SELECT publisher FROM books WHERE bcode=%s", (bcode))
    publisher= cursor.fetchone()
    for pub in publisher:
        p= tk.Label(p6, text= pub,bg="#D0A373", fg="#2C041C",anchor="center",
                 font="Times 14",height=2,width=35,
                 borderwidth = 3, relief="solid", highlightcolor="red")
        p_window=c6.create_window(250,166,anchor="nw",window=p)
    #fetching the summary
    cursor.execute("SELECT summary FROM books WHERE bcode=%s", (bcode))
    summary= cursor.fetchone()
    for summ in summary:
        s= tk.Message(p6, text= summ,bg="#D0A373", fg="#2C041C",
                   anchor="center",font="Times 14",
                 borderwidth = 3, relief="solid", highlightcolor="red")
        s_window=c6.create_window(250,282,anchor="nw",window=s)
    #fetching the amazon link
    cursor.execute("SELECT link FROM links WHERE bcode=%s", (bcode))
    link= cursor.fetchone()
    def callback(link):
        webbrowser.open_new_tab(link)
    for lin in link:
        l= tk.Label(p6, text= link, fg= "blue", cursor= "hand2",height=2,width=70,borderwidth = 3,
                 bg="#D0A373")
        l.bind("<Button-1>", lambda e: callback(lin))
        l_window= c6.create_window(250, 224, anchor= "nw", window= l)
    
    #button
    button1 =tk. Button(c6, text = "Back to list of books",
                        width=17,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=p6.destroy)
    button1.pack(pady = 20)
    c6.create_window(900, 350, anchor= "nw", window= button1)
    #displaying the information
    p6.mainloop()

################################ RECOMENDATIONS ################################

def recom(lvl):
    
    mydb=m.connect(host="localhost",database="project",user="root")
    cursor=mydb.cursor()
    vio,rom,adv,hap,conv=specs()
    if lvl=="beginner":
        cursor.execute("SELECT books.bcode FROM specs,books WHERE books.bcode=specs.bcode AND violence=%s AND romance=%s AND adventure=%s AND happy=%s AND conventional=%s AND level='beginner'",(vio,rom,adv,hap,conv))
        recom_bcode=cursor.fetchall()
    elif lvl=="intermediate":
        cursor.execute("SELECT books.bcode FROM specs,books WHERE books.bcode=specs.bcode AND violence=%s AND romance=%s AND adventure=%s AND happy=%s AND conventional=%s AND level IN ('beginner','intermediate')",(vio,rom,adv,hap,conv))
        recom_bcode=cursor.fetchall()
    elif lvl=="advanced":
        cursor.execute("SELECT books.bcode FROM specs,books WHERE books.bcode=specs.bcode AND violence=%s AND romance=%s AND adventure=%s AND happy=%s AND conventional=%s AND level IN ('intermediate','advanced')",(vio,rom,adv,hap,conv))
        recom_bcode=cursor.fetchall()
    
    tuple1=()
    for row in recom_bcode:
        tuple1=tuple1+row

    y_coor=100
    wbook_deets=tk.Tk()
    wbook_deets.title("findmeabook.org")
    wbook_deets.geometry("1920x1080")

    #frame
    extra_frame=tk.Frame(wbook_deets,width=1850,height=1280)
    extra_frame.pack(fill="both",expand=True)
    main_canvas=tk.Canvas(extra_frame,width=1850,height=1280)

    #scrollbar
    scroll1=tk.Scrollbar(extra_frame,orient="vertical")
    scroll1.pack(side="right",fill="y")
    scroll1.config(command=main_canvas.yview)
    main_canvas.config(yscrollcommand=scroll1.set)


    #logo
    img2 =tk.PhotoImage(master=wbook_deets,file="logo.ppm") 
    logolab=tk.Label(wbook_deets,image=img2,borderwidth = 5, relief="solid")
    logolab_can1=main_canvas.create_window(1042,176,window=logolab)
    
    
    img_l=[]
    if len(tuple1)==0:
        for j in range(0,5):
            i=r.randint(101,201)
            tuple1=tuple1+(i,)
            cfb_lab=t.Label(main_canvas,text="We couldnt find any book in our existing library set to your specification;\nbut you may like:",height=4,width=55,
            bg="#D0A373", fg="#2C041C",anchor="center",font="Times 14", borderwidth = 1, relief="solid", highlightcolor="red")
            cfb_lab.place(x=100,y=0)
        
    def get_bname(name):
        global name1
        name1=name
        page6(name1)
        return name
    for i in tuple1:
        cursor.execute("SELECT covp FROM coverpage WHERE bcode=%s" %i)
        tcov_p=cursor.fetchone()
        cursor.execute("SELECT bname FROM books WHERE bcode=%s" %i)
        bname=cursor.fetchone()
        
        for j in tcov_p:
            for k in bname:
                cov_img=PIL.Image.open(j)
                c_img=cov_img.resize((100,140))
                covp_img=ImageTk.PhotoImage(c_img)
                img_l.append(covp_img)
                img=img_l[tuple1.index(i)]
                img_lab=tk.Label(main_canvas,image=img)
                img_window=main_canvas.create_window(100,y_coor,anchor="nw",window=img_lab)
                bname_button=tk.Button(main_canvas,text=k,width=30,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 3,name=k.lower(),command=lambda k=k: get_bname(k))
                bname_window=main_canvas.create_window(250,(y_coor+70),anchor="nw",window=bname_button)
        y_coor=y_coor+200
    
    main_canvas.config(scrollregion=(0,0,1850,y_coor+100))
    main_canvas.pack(fill="both",expand=True)
    #background image
    backg=PIL.Image.open("image.ppm")
    bacg=backg.resize((1850,y_coor+500))
    img =ImageTk.PhotoImage(bacg)
    bg=main_canvas.create_image(0,0,image=img,anchor="nw")
    def terminate():
        wbook_deets.destroy()
        thanks()
    exit_button = Button(main_canvas, text = "Exit.",
                        width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=terminate)
    exit_button.pack(pady = 20)
    main_canvas.create_window(942, 500, anchor= "nw", window=exit_button)

    def back_to_spec():
        wbook_deets.destroy()
        main_spec(lvl)
    back_button = Button(main_canvas, text = "Back",
                        width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=back_to_spec)
    back_button.pack(pady = 20)
    main_canvas.create_window(600, 500, anchor= "nw", window= back_button)
    wbook_deets.mainloop()
    return name1

############################# SPECIFICATIONS PAGE ##############################

def specs():
    wspecs=tk.Tk()
    wspecs.title("findmeabook.org")
    wspecs.geometry("1920x1080")
    #can1
    can_specs=tk.Canvas(wspecs,width=700,height=500)
    can_specs.pack(fill="both",expand=True)

    #logo
    img2 =tk.PhotoImage(master=wspecs,file="logo.ppm") 
    logolab=tk.Label(wspecs,image=img2,borderwidth = 5, relief="solid")
    logolab_can=can_specs.create_window(1042,176,window=logolab)
    #background image
    img =tk.PhotoImage(master=wspecs,file="image.ppm") 
    can_specs.create_image(0,0,image=img,anchor="nw")

    ##variables
    v=tk.DoubleVar()
    r=tk.DoubleVar()
    a=tk.DoubleVar()
    h=tk.DoubleVar()
    c=tk.DoubleVar()

    ##scales
    s_vio=tk.Scale(wspecs, variable=v, from_=-1, to=1, orient= "horizontal",
                  label="               Violence",
                  font="georgia 15",background='#FFFDD0',troughcolor='#CD5C5C',length=250)
    s_vio.place(x=200,y=50)
    s_vio.set(0)
    s_rom=tk.Scale(wspecs, variable=r, from_=-1, to=1, orient= "horizontal",
                  label="               Romance",
                  font="georgia 15",background='#FFFDD0',troughcolor='#CD5C5C',length=250)
    s_rom.place(x=200,y=150)
    s_rom.set(0)
    s_adv=tk.Scale(wspecs, variable=a, from_=-1, to=1, orient= "horizontal",
                  label="               Adventure",
                  font="georgia 15",background='#FFFDD0',troughcolor='#CD5C5C',length=250)
    s_adv.place(x=200,y=250)
    s_adv.set(0)
    s_hap=tk.Scale(wspecs, variable=h, from_=-1, to=1, orient= "horizontal",
                  label="                Happy",
                  font="georgia 15",background='#FFFDD0',troughcolor='#CD5C5C',length=250)
    s_hap.place(x=200,y=350)
    s_hap.set(0)
    s_conv=tk.Scale(wspecs, variable=c, from_=-1, to=1, orient= "horizontal",
                   label="               Conventional",
                   font="georgia 15",background='#FFFDD0',troughcolor='#CD5C5C',length=250)
    s_conv.place(x=200,y=450)
    s_conv.set(0)

    
    def specs_values():
        global vio,rom,adv,hap,conv
        vio=int(v.get())+2
        rom=int(r.get())+2
        adv=int(a.get())+2
        hap=int(h.get())+2
        conv=int(c.get())+2
        wspecs.destroy()
        return vio,rom,adv,hap,conv
        
    ##button
    bspecs=tk.Button(wspecs,text="Submit!",
                    width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                    borderwidth = 5,command=specs_values).place(x=253,y=600)


    wspecs.mainloop()
    
    return vio,rom,adv,hap,conv

########################## SPECIFICATIONS START PAGE ###########################

def main_spec(lvl):
    t = tk.Tk()
    t.title('findmeabook.org')
    t.geometry("1920x1080")
    #can1
    can_start_specs=tk.Canvas(t,width=700,height=500)
    can_start_specs.pack(fill="both",expand=True)

    #logo
    img_logo =tk.PhotoImage(master=t,file="logo.ppm") 
    logolab=tk.Label(can_start_specs,image=img_logo,borderwidth = 5, relief="solid")
    logolab_can=can_start_specs.create_window(720,173,window=logolab)
    #background image
    img =tk.PhotoImage(master=t,file="image.ppm") 
    can_start_specs.create_image(0,0,image=img,anchor="nw")

    #line
    can_start_specs.create_line(0,550,2000,550, fill="#B39861", width=5)


    #specs text
    l1=tk.Label(can_start_specs,text="Now, let’s find books you’d enjoy by narrowing down to your favourite type— or current mood.\n Adjust the slider to tell us which sub-genre you would like your book to have or not have.\n If it doesn’t matter and you’re fine either way with a particular sub-genre, \n keep the slider in the middle.",
                height=5,width=70,
                bg="#D0A373", fg="#2C041C",anchor="center",font="Times 20 italic bold", borderwidth = 5, relief="solid", highlightcolor="red")
    l1.pack(side="top")
    l1.place(x=120,y=350)
    #button command
  
    def get_specs(lvl):
        
        global selected_book
        t.destroy()
        if str(type(lvl))=="<class 'tuple'>":
            for i in lvl:
                selected_book=recom(i)
        elif str(type(lvl))=="<class 'str'>":
            selected_book=recom(lvl)
        
    #button experiment
    button2 = tk.Button(can_start_specs, text = "Start!",
                        width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=lambda:get_specs(lvl))
    button2.pack(pady = 20)
    button2.place(x=650,y=560)

    def back_to_spec():
        t.destroy()
        sign_login()
    back_button = Button(can_start_specs, text = "Back",
                        width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=back_to_spec)
    back_button.place(x=550,y=560)
    #mainloop end
    t.mainloop()
    return selected_book

################################ USER INFO PAGE ################################

##creating account
def user_info():
    global level
    wsinc.destroy()
    mydb= m.connect (host="localhost",database="project",user="root")
    mycursor=mydb.cursor()

    name,mail=user_details()
    c="false"
    while c!="true":
        if '@' in mail and '.com' in mail:
            c="true"
            continue
        elif '@' not in mail:
            messagebox.showerror("Error","NO '@' FOUND IN EMAIL.")
            name,mail=user_details()
        elif '.com' not in mail:
            messagebox.showerror("Error","NO '.com' FOUND IN EMAIL.")
            name,mail=user_details()
    def quiz():
        global c
        global level
        global n
        global wquiz
        c=0
        wquiz=tk.Tk()
        wquiz.geometry("1920x1080")
        wquiz.title('findmeabook.org')
        #can1
        can_quiz1=tk.Canvas(wquiz,width=700,height=500)
        can_quiz1.pack(fill="both",expand=True)

        #background image
        can_quiz1.img =tk.PhotoImage(master=wquiz,file="image.ppm") 
        can_quiz1.create_image(0,0,image=can_quiz1.img,anchor="nw")
        
        #logo
        can_quiz1.img_logo =tk.PhotoImage(master=wquiz,file="logo.ppm") 
        logolab=tk.Label(wquiz,image=can_quiz1.img_logo,borderwidth = 5, relief="solid")
        logolab_can=can_quiz1.create_window(900,200,window=logolab)

        
        
        ##q1
        lab_age=tk.Label(wquiz,text="How old are you?", height=2,width=20,bg="#D0A373", fg="#2C041C",anchor="center",
                        font="Times 20", borderwidth = 5,
                        relief="solid", highlightcolor="red")
        lab_agecan=can_quiz1.create_window(220,100,window=lab_age)        
        xage=tk.IntVar()
        entry_age=tk.Entry(wquiz,textvariable=xage)
        entry_age.place(x=67,y=150,height=63,width=200)
        xage.set(1)
    
        ##q2
        lab_hl=tk.Label(wquiz, height=2,width=30,bg="#D0A373", fg="#2C041C",anchor="center",
                        font="Times 20", borderwidth = 5,
                        relief="solid", highlightcolor="red",
                       text="How long have you been into reading? \n (an estimate in years)")
        lab_hlcan=can_quiz1.create_window(300,300,window=lab_hl)
        xhl=tk.IntVar()
        entry_hl=tk.Entry(wquiz,textvariable=xhl)
        entry_hl.place(x=69,y=350,height=63,width=200)
        def calc_level():
            mydb= m.connect (host="localhost",database="project",user="root")
            mycursor=mydb.cursor()
            global c
            global level
            avg= c/3
            if avg>=10 and avg<=15:
                level='beginner'
            elif avg>15 and avg<=25:
                level='intermediate'
            elif avg>25 and avg<=30:
                level='advanced'
            l=(level,name,mail)
            sql1="UPDATE USERS SET level=%s where name=%s AND mail=%s"
            mycursor.execute(sql1,l)
            mydb.commit()
        def q():
            global level
            wq_start=tk.Tk()
            wq_start.geometry("1920x1080")
            wq_start.title('findmeabook.org')
            #can1
            can_q2=tk.Canvas(wq_start,width=700,height=500)
            can_q2.pack(fill="both",expand=True)
    
            message_wq=tk.Label(wq_start,text="Now, let's have you read a short passage to calculate \n how many words you can read in one minute. \n This process will help us analyze \n how accustomed you are to reading as a habit. \n Press the 'Start Reading!' button below to \n start the timer and begin reading. \n Remember: don't try to read too fast, \n only make sure to understand as you go through it.",
                               height=9,width=45,bg="#D0A373", fg="#2C041C",anchor="center",font="Times 20 italic bold",
                               borderwidth = 5, relief="solid", highlightcolor="red")
            message_wq_can=can_q2.create_window(720,445,window=message_wq)

            #logo
            can_q2.img_logo =tk.PhotoImage(master=wq_start,file="logo.ppm") 
            logolab=tk.Label(wq_start,image=can_q2.img_logo,borderwidth = 5, relief="solid")
            logolab_can=can_q2.create_window(700,150,window=logolab)

            #background image
            can_q2.img =tk.PhotoImage(master=wq_start,file="image.ppm")
            can_q2.create_image(0,0,image=can_q2.img,anchor="nw")
                        
            def wq():             
                global nof
                wq_start.destroy()
                f=open("timer.txt","r")
                data=f.read()
                x=data.split()
                nof=len(x)
                import time
                def stop_time():
                    global c
                    global level
                    wq.destroy()
                    t2=time.perf_counter()
                    tm= (t2-t1-1)/60
                    wpm=nof/tm
                    if wpm<=100:
                        c+=10
                    elif wpm>=100 and wpm<=300:
                        c+=20
                    elif wpm>300:
                        c+=30
                    calc_level()
                    main_spec(level)
                wq=tk.Tk()
                wq.geometry("1920x1080")
                wq.title('findmeabook.org')
                #can_q
                can_q=tk.Canvas(wq,width=700,height=500)
                can_q.pack(fill="both",expand=True)

                #background image
                can_q.img =tk.PhotoImage(master=wq,file="image.ppm") 
                can_q.create_image(0,0,image=can_q.img,anchor="nw")
                
                #logo
                can_q.img_logo =tk.PhotoImage(master=wq,file="logo.ppm") 
                logolab=tk.Label(wq,image=can_q.img_logo,borderwidth = 5, relief="solid")
                logolab_can=can_q.create_window(1042,176,window=logolab)


                para=tk.Message(wq,text=data,
                               bg="#D0A373", fg="#2C041C",anchor="center",
                               font="Times 15", borderwidth = 5,
                               relief="solid", highlightcolor="red")
                f.close()
                t1=time.perf_counter()
                para.place(x=100,y=50)
                end_read=tk.Button(wq,text="I'm done.",
                    width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                    borderwidth = 5,command=stop_time)
                end_read.place(x=340,y=600)
                def back():
                    wq.destroy()
                    q()
                back_button = Button(can_q, text = "Back",
                        width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=back)
                back_button.place(x=550,y=560)
            start_read=tk.Button(wq_start,text="Start Reading!",
                    width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                    borderwidth = 5,command=wq)
            start_read.place(x=650,y=600)
            def back():
                wq_start.destroy()
                mydb= m.connect (host="localhost",database="project",user="root")
                mycursor=mydb.cursor()
                mycursor.execute("DELETE FROM USERS WHERE name=%s AND mail=%s",(name,mail))
                mydb.commit()
                sign_login()
            back_button = Button(can_q2, text = "Back",
                        width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=back)
            back_button.place(x=550,y=560)
        def q1_q2():
            mydb= m.connect (host="localhost",database="project",user="root")
            mycursor=mydb.cursor()
            wquiz.destroy()
            global c
            global n
            global level
            n=xage.get()
            hl=xhl.get()
            if n<=0:
                messagebox.showerror("Error","age cannot be negative or zero")
            elif n>=1 and n<=12:
                c+=10
            elif n>=13 and n<=25:
                c+=20
            elif n>=26:
                c+=30
            li=(n,name,mail)
            sql2="UPDATE USERS SET age=%s where name=%s AND mail=%s"
            mycursor.execute(sql2,li)
            mydb.commit()
            if hl>n or hl<0:
                messagebox.showerror("Error","invalid entry")
            elif hl>=0 and hl<=2:
                c+=10
            elif hl>=3 and hl<=5:
                c+=20
            elif hl>5:
                c+=30
            q()
        exit_button=tk.Button(wquiz,text="Next",
                    width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                    borderwidth = 5,command=q1_q2)
        exit_buttoncan=can_quiz1.create_window(170,550,window=exit_button)
        def back_to_spec():
            wquiz.destroy()
            mydb= m.connect (host="localhost",database="project",user="root")
            mycursor=mydb.cursor()
            mycursor.execute("DELETE FROM USERS WHERE name=%s AND mail=%s",(name,mail))
            mydb.commit()
            sign_login()
        back_button = Button(can_quiz1, text = "Back",
                            width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                            borderwidth = 5,command=back_to_spec)
        back_button.place(x=550,y=560)
    mycursor.execute("SELECT name,mail FROM users")
    user_record=mycursor.fetchall()
    val=(name,mail)
    if val not in user_record:
        sql="INSERT INTO USERS (name,mail)VALUES (%s,%s)"
        mycursor.execute(sql,val)
        mydb.commit()
        level=''
        quiz()
    else:
        messagebox.showerror("Error","You already have an existing account. Please sign in.")
        sign_login()

    
    mycursor.close()
    mydb.close()
## taking details
def user_details():
    wuser=tk.Tk()
    wuser.title('findmeabook.org')
    wuser.geometry('1920x1080')
    
    xname=tk.StringVar(wuser)
    xmail=tk.StringVar(wuser)
    def get_details():
        global name,mail
        name=xname.get()
        mail=xmail.get()
        wuser.destroy()

    #can1
    can_info=tk.Canvas(wuser,width=700,height=500)
    can_info.pack(fill="both",expand=True)

    
    #logo
    img_logo=tk.PhotoImage(master=wuser,file="logo.ppm") 
    logo=tk.Label(wuser,image=img_logo,borderwidth = 5, relief="solid")
    logo_can=can_info.create_window(220,150,window=logo)
    
    #button
    Bsubmit=tk.Button(wuser, text="Submit!",
                    width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",command=get_details,
                    borderwidth = 5)
    Bsubmit.place(x=850,y=300)

    def back_to_spec():
        wuser.destroy()
        sign_login()
    back_button = Button(can_info, text = "Back",
                        width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                        borderwidth = 5,command=back_to_spec)
    back_button.place(x=550,y=560)
    #background image
    img =tk.PhotoImage(master=wuser,file="image.ppm")
    can_info.create_image(0,0,image=img,anchor="nw")

    ## labels
    lname=tk.Label(wuser, text="Name: ",width=14,height=3,font="georgia", bg="#E0D3AF",
                    borderwidth = 5, relief="sunken")
    lname.place(x=750,y=80)

    lemail=tk.Label(wuser, text="Email: ",width=14,height=3,font="georgia", bg="#E0D3AF",
                    borderwidth = 5, relief="sunken")
    lemail.place(x=750,y=175)
    
    ##entries
    ename=tk.Entry(wuser, textvariable=xname)
    ename.place(x=900,y=80,width=200,height=63)

    eemail=tk.Entry(wuser,textvariable=xmail)
    eemail.place(x=900,y=175,width=200,height=63)

    wuser.mainloop()
    return name,mail

def sign_login():
    #window
    global wsinc
    wsinc=tk.Tk()
    wsinc.title('findmeabook.org')
    wsinc.geometry("1920x1080")

    #can_sign_login
    can_sign_login=tk.Canvas(wsinc,width=700,height=500)
    can_sign_login.pack(fill="both",expand=True)
    
    Bsignin=tk.Button(can_sign_login, text="Sign In", command=sign_in,width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                    borderwidth = 5)
    Bsignin.place(x=650,y=180)
    Bcreate=tk.Button(can_sign_login, text="Create an account", command=user_info,width=15,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                    borderwidth = 5)
    Bcreate.place(x=960,y=180)

    #line
    can_sign_login.create_line(0,350,2000,350, fill="#B39861", width=7)

    #logo
    img_logo =tk.PhotoImage(master=wsinc,file="logo.ppm") 
    logolab=tk.Label(wsinc,image=img_logo,borderwidth = 5, relief="solid")
    logolab_can_sign=can_sign_login.create_window(220,150,window=logolab)

    #label
    l1=tk.Label(can_sign_login,text="Sign in if you have an existing account, \n or create a new account now!",height=4,width=42,bg="#E0D3AF",
               fg="#2C041C",anchor="center",font="Times 14 italic bold", borderwidth = 3, relief="solid", highlightcolor="red")
    l1.place(x=648,y=50)
              
    #background image
    can_sign_login.img =tk.PhotoImage(master=wsinc,file="image.ppm")
    can_sign_login.create_image(0,0,image=can_sign_login.img,anchor="nw")
    wsinc.mainloop()

    #text
    T = tk.Text(can_sign_login, height=3, width=30,bg="#FE676E",fg="#055B5C")
    T.pack()
    T.insert(t.END, "Meet your next favourite book!")
    T.place(x=250,y=500)

##sign in window    
def sign_in():
    wsinc.destroy()
    name,mail=user_details()
    """page 4"""
    mydb= m.connect (host="localhost",database="project",user="root")
    mycursor=mydb.cursor()
    mycursor.execute("SELECT name,mail FROM users")
    user_record=mycursor.fetchall()
    c=0
    for row in user_record:
        if row[0]==name and row[1]==mail:
            mycursor.execute("SELECT level FROM users WHERE name=%s and mail=%s",(name,mail))
            level=mycursor.fetchone()
            c=1
            break
        else:
            c=0  
    if c==0:
        messagebox.showerror("Error","You dont have an existing account. Please create an account")
        sign_login()
    main_spec(level)
    return level

################################## START PAGE ##################################
mydb= m.connect (host="localhost",database="project",user="root")
mycursor=mydb.cursor()
mycursor.execute("DELETE FROM USERS WHERE age IS NULL OR level IS NULL;")
mydb.commit()
mycursor.close()
#window
page1 = tk.Tk()
page1.title('findmeabook.org')
page1.geometry("1920x1080")

#can1
can1=tk.Canvas(page1,width=700,height=500)
can1.pack(fill="both",expand=True)

#logo
img2 =tk.PhotoImage(master=page1,file="logo.ppm") 
logolab=tk.Label(page1,image=img2,borderwidth = 5, relief="solid")
logolab_can1=can1.create_window(720,173,window=logolab)

#moving text
from tkinter import *
def shift():
    x1,y1,x2,y2 = canvas.bbox("marquee")
    if(x2<0 or y1<0): #reset the coordinates
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height()//2
        canvas.coords("marquee",x1,y1)
    else:
        canvas.move("marquee", -2, 0)
    canvas.after(1000//fps,shift)

canvas=Canvas(can1,bg='#58181F')
canvas.place(x=0,y=250)
canvas.pack(fill="both")
text_var="Hello! Welcome to findmeabook.org!"
text=canvas.create_text(0,-2000,text=text_var,font=('georgia',30,'bold'),fill='white',tags=("marquee",),anchor='w')
x1,y1,x2,y2 = canvas.bbox("marquee")
width = x2-x1
height = y2-y1
canvas['width']=width
canvas['height']=height
fps=60    #Change faster/slower
shift()


#background image
img =tk.PhotoImage(master=page1,file="image.ppm") 
can1.create_image(0,0,image=img,anchor="nw")

#line
can1.create_line(0,550,2000,550, fill="#B39861", width=5)


#welcome text
l1=tk.Label(can1,text="Unsure of which book to read next? \n Come on a short journey with us as we find you your \n next favourite books while narrowing them down to best suit your taste.",
            height=4,width=55,
            bg="#D0A373", fg="#2C041C",anchor="center",font="Times 20 italic bold", borderwidth = 5, relief="solid", highlightcolor="red")
l1.pack(side="top")
l1.place(x=250,y=350)
def invoke_sign():
    page1.destroy()
    sign_login()
    
#button
button1 = tk.Button(can1, text = "Lets get started!",
                    width=14,height=3,fg="#2C041C",font="georgia", bg="#E0D3AF",
                    borderwidth = 5,command=invoke_sign)
button1.pack(pady = 20)
button1.place(x=650,y=600)

#mainloop end
page1.mainloop()
