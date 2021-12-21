import pyttsx3#this converts text to speech, this i'm using it in the speak() function
import datetime as dt
import speech_recognition as sr
import pyaudio
import wikipedia#python library used to access data from wikipedia
import webbrowser
import time
import os
import smtplib
import mysql.connector
from tkinter import *
from tkcalendar import *
from heapq import heappush
from datetime import date

dateslist=[]
dict_tasks={}
dict_days={}
l_dayno=['01','02','03','04','05','06','07','08','09']
k=0
h=0

for i in range(1,32):
    if i==1:
        s=str(i)
        s=s+"st"
        dict_days[s]=l_dayno[k]
        k=k+1
    elif i==2:
        s=str(i)
        s=s+"nd"
        dict_days[s]=l_dayno[k]
        k=k+1
    elif i==3:
        s=str(i)
        s=s+"rd"
        dict_days[s] = l_dayno[k]
        k = k + 1
    elif i>=4 and i<=9:
        if h==0:
            for j in range(4,10):
                s=str(j)
                s=s+"th"
                dict_days[s]=l_dayno[k]
                k=k+1
                h=h+1
        else:
            pass
    elif i>9 and i<=20:
        s=str(i)
        s=s+"th"
        dict_days[s]=i
    elif i==21:
        s=str(i)+"st"
        dict_days[s]=i
    elif i==22:
        s=str(i)+"nd"
        dict_days[s]=i
    elif i==23:
        s=str(i)+"rd"
        dict_days[s]=i
    elif i>23 and i<=30:
        s=str(i)+"th"
        dict_days[s]=i
    elif i==31:
        s=str(i)+"st"
        dict_days[s]=i
month_dict={'january':'01','february':'02','march':'03','april':'04','may':'05','june':'06','july':'07','august':'08', 'september':'09','october':'10','november':'11','december':'12'}
def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()#extended hello, used to initiate the conversation between the smtp server
    server.starttls()#START TRANSPORT LAYER SECURITY used to encrypt the email-messages.
    server.login('mypassion4coding@gmail.com', 'mypassion4coding##')#to check if the user has a valid acoount i.e.to avoid email spamming or use of fake accounts
    server.sendmail('mypassion4coding@gmail.com',to,content)
    server.close()
def operations():
    speak("What changes do you want to make?")
    #print("What changes do you want to make?")
    query = Takecommand().lower()
    if 'update' in query:
        #print("Here is your automated planned routine")
        #speak("Here is your automated planned routine")
        #print("Choose the attribute that you want to update")
        #speak("Choose the attribute that you want to update")
        #print("What do you want to update, task name or deadline??")
        speak("What do you want to update, task name or deadline??")
        query = Takecommand().lower()
        if 'task name' in query:
            speak("Please give me the task name that you want to update")
            #print("Please give me the task name that you want to update")
            old_name = Takecommand().lower()
            speak("Please give the new task name")
            #print("Please give the new task name")
            new_task = Takecommand().lower()
            try:
                for x in dateslist:
                    if dict_tasks[x][1]==old_name:
                        dict_tasks[x][1]=new_task
                        #print("updated!!")
                        speak("updated")
                        return
            except EXCEPTION as e1:
                #print("No match found...")
                speak("No match found")
                return
        else:
            speak("Please give me the deadline that you want to update")
            #print("Please give me the task name that you want to update")
            old_name = Takecommand().lower()
            speak("Please give the new task name")
            #print("Please give the new task name")
            new_task = Takecommand().lower()
            try:
                for x in dateslist:
                    if dict_tasks[x][0] == old_name:
                        dict_tasks[x][0] = new_task
                        #print("updated!!")
                        speak("updated")
                        return
            except EXCEPTION as e1:
                #print("No match found...")
                speak("No match found")
                return

            #sql="UPDATE tasks SET name=%s Where name=%s"
            #mycursor.execute(sql,(new_task,old_name))
            #mydb.commit()
def calendar_view():
    def print_sel():
        root=Tk()
        dead=cal.selection_get()





    cal = Calendar(root,
                    font="Arial 14", selectmode='day',
                    cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    Button(root, text="ok", command=print_sel).pack()
def priority_queue(d,t_n):
    d1=str(d)
    day=d1.split("-")
    heappush(dateslist,day[-1])
    dict_tasks[day[-1]]=(d,t_n)
    #print(dateslist)
    for x in day:
        day.remove(x)

def dateentry_view(root):
    def print_sel():
        d=cal.get_date()
        t_n = name.get()
        #print(d,t_n)
        priority_queue(d,t_n)
    #top = Toplevel(root)
    Label(root,text="Task Name").pack(padx=10,pady=10)
    name=StringVar()
    taskname=Entry(root,textvariable=name).pack(padx=10,pady=10)
    Label(root, text='set deadline').pack(padx=10, pady=10)
    cal = DateEntry(root, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)
    Button(root, text="set", command=print_sel).pack()

#engine=pyttsx3.speak("hello Madiha, hope you are doing well...how could i help you??")

def grabdate():
    def print_sel():
        d=cal.get_date()
        #t_n = name.get()
        #print(d)
        d1 = str(d)
        day = d1.split("-")
    root=Tk()
    cal=DateEntry(root, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack()
    Button(root, text="Grab date", command=print_sel).pack()


def speak(audio):
    engine.say(audio)
    engine.runAndWait() #with out this the speech is not audible to me
def Takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold=1 #im using this to say that while i give command and in that span if i pause for 2 seconds then do not complete the phrase and take that as a command
        audio=r.listen(source)
        try:#here we are recongnizing the speech that we collected using listen method
            print("Recognizing....")
            query=r.recognize_google(audio,language='en-in')
            print("User said: ",query)
        except Exception as e:
            print("Say it again please")
            query=Takecommand().lower()
            return query

        return query
def scheduling_tasks():
    root=Tk()
    dateentry_view(root)
    #Button(root, text='schedule tasks', command=dateentry_view(root)).pack(padx=10, pady=10)
    root.mainloop()

    speak("Any more tasks to schedule")
    print("Any more tasks to schedule")
    query = Takecommand().lower()
    if 'no' in query:
        return
    scheduling_tasks()
    return
def display_mytasks(mytaskslist):
    num = 1
    for x in mytaskslist:
        #print("Task Number-", num)
        #print(x)
        speak("Task number")
        j = str(num)
        speak(j)
        speak(x)
        num=num+1

    return
def setup_db():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="10mother#_mysql", database="one")
    mycursor = mydb.cursor()
    return (mydb,mycursor)
if __name__ == '__main__':
    engine = pyttsx3.init('sapi5')#sapi5 is microsoft speeech API
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    print("yippee")
    speak("HelLo Madiha!!what do you want me to do??")
    hour=int(dt.datetime.now().hour)
    minutes=int(dt.datetime.now().minute)
    l1=1
    while(True):
            query=Takecommand().lower()#here we are taking the query of the user to understand what th user wants
    #and using lower() because now we have to check and compare the users query whether it is opening google or youtube and so on

            if 'quit' in query:
                break
            elif 'wikipedia' in query:
                speak('searching')
                results=wikipedia.summary(query,sentences=2)
                print(results)
                speak(results)
        #print(results)
            elif 'open youtube' in query:
                webbrowser.open("youtube.com")
            elif 'open google' in query:
                webbrowser.open("google.com")
            elif 'open stack overflow' in query:
                webbrowser.open("stackoverflow.com")
            elif 'the time' in query:
                strTime=dt.datetime.now().strftime("%H hours %M minutes and %S seconds")
                speak(f"it is {strTime}")
            elif 'open pycharm' in query:
                pycharm_path="C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.2.1\\bin\\pycharm64.exe"
                os.startfile(pycharm_path)
            elif 'open zoom' in query:

                zoom_path="C:\\Users\\jahan\\AppData\\Roaming\\Zoom\\bin_00\\Zoom.exe"
                os.startfile(zoom_path)
            elif 'email to' in query:
                #speak("What should be the subject")
                #subject=Takecommand().lower()
                print("What should be the content??")
                speak("What should be the content")
                try:
                    content=Takecommand()
                    to="example@gmail.com"
                    #msg=f'Subject:{subject}\n\n{content}'
                    sendEmail(to,content)
                    print("Email has been sent!!")
                    speak("Email has been sent")
                except EXCEPTION as e:
                    speak("sorry!your email wasn't sent, try again in some time")
                    print("sorry!your email wasn't sent, try again in some time")
            elif 'task' in query or 'tasks' in query:
                (mydb,mycursor)=setup_db()
                mycursor.execute("select count(name) from tasks")
                result=mycursor.fetchone()
                print(result)
                count_value=result[0]
                if count_value==0:
                    #print("No tasks are scheduled for today")
                    speak("No tasks are scheduled for today")
                    #print("Do you want to schedule tasks??")
                    speak("Do you want to schedule tasks??")
                    query=Takecommand().lower()
                    if 'yes' in query or 'yep' in query or 'yeah' in query:
                        #print("cool!!feed your tasks")
                        speak("cool!!feed your tasks")
                        #root=Tk()
                        scheduling_tasks()
                        for x in dateslist:
                            (t_name, t_deadline) = dict_tasks[x]
                            sql = "INSERT INTO tasks values(%s,%s)"
                            val = (t_name, t_deadline)
                            mycursor.execute(sql, (t_deadline, t_name))
                            mydb.commit()
                        speak("Added!!")
                        dict_tasks.clear()
                else:
                    if 'today' in query:
                        todays_date=date.today().strftime("%Y-%m-%d")
                        #print("Here are your tasks for today")
                        #speak("Here are your tasks for today")
                        sql_query="select name from tasks where deadline=%s"
                        mycursor.execute(sql_query, (todays_date,))
                        mytaskslist=mycursor.fetchall()
                        if mytaskslist==[]:
                            speak("No tasks are scheduled for today")
                            print("No tasks are scheduled for today")
                            speak("do you want to schedule tasks??")
                            print("do you want to schedule tasks??")
                            query=Takecommand().lower()
                            if 'yes' in query or 'yep' in query or 'yeah' in query:
                                speak("cool!!feed your tasks")
                                print("cool!Feed your tasks")
                                scheduling_tasks()
                                for x in dateslist:
                                    (t_name, t_deadline) = dict_tasks[x]
                                    sql = "INSERT INTO tasks values(%s,%s)"
                                    val = (t_name, t_deadline)
                                    mycursor.execute(sql, (t_deadline, t_name))
                                    mydb.commit()
                                speak("Added!!")
                                dict_tasks.clear()

                            else:
                                speak("okay")
                        else:
                            for x in mytaskslist:
                                speak(x)
                                print(x)
                        #display_mytasks(mytaskslist)
                    elif 'tomorrow' in query:
                        todays_date = date.today().strftime("%Y-%m-%d")
                        #print("Here are your tasks for tomorrow")
                        #speak("Here are your tasks for tomorrow")
                        #sql_query = "select name from tasks where deadline=%s"

                       # mytaskslist = mycursor.fetchall()
                        todays_date = date.today().strftime("%Y-%m-%d")
                        l = todays_date.split("-")
                        curr_date = int(l[-1])
                        curr_date = curr_date + 1
                        l[-1] = str(curr_date)
                        i = 0
                        s=""
                        for x in l:
                            s = s + x
                            if i != (len(l) - 1):
                                s = s + "-"
                            i = i + 1
                        sql_query="select name from tasks where deadline=%s"
                        mycursor.execute(sql_query, (s,))
                        resultset=mycursor.fetchall()
                        if resultset!=[]:
                            display_mytasks(resultset)
                        #print(resultset)
                        else:
                            speak("No tasks are scheduled for tomorrow")
                            speak("Do you want to schedule tasks??")
                            query=Takecommand().lower()
                            if 'yes' in query or 'yep' in query or 'yeah' in query:
                                #print("cool!!feed your tasks")
                                speak("cool!!feed your tasks")
                                # root=Tk()
                                #scheduling_tasks()
                                scheduling_tasks()
                                for x in dateslist:
                                    (t_name, t_deadline) = dict_tasks[x]
                                    sql = "INSERT INTO tasks values(%s,%s)"
                                    val = (t_name, t_deadline)
                                    mycursor.execute(sql, (t_deadline, t_name))
                                    mydb.commit()
                                speak("Added!!")
                    elif 'deadline' in query:
                        try:
                            buffered_task_list=query.split(" ")
                            buffered_name=buffered_task_list[-1]
                            buffered_name_2=buffered_task_list[-2]
                            final_name=buffered_name_2+" "+buffered_name
                            sql_query="select deadline from tasks where name=%s"
                            mycursor.execute(sql_query, (final_name,))
                            resultset=mycursor.fetchall()
                        #print(resultset)
                            speak(resultset[0][0])
                        except EXCEPTION as e:
                            speak("No such task exists in your tasks list")
                            speak("do you want to add this to your schedule??")
                            query=Takecommand().lower()
                            if 'yes' in query or 'yep' in query or 'yeah' in query:
                                scheduling_tasks()
                                for x in dateslist:
                                    (t_name, t_deadline) = dict_tasks[x]
                                    sql = "INSERT INTO tasks values(%s,%s)"
                                    val = (t_name, t_deadline)
                                    mycursor.execute(sql, (t_deadline, t_name))
                                    mydb.commit()
                                speak("Added!!")
                                dict_tasks.clear()
                    elif 'on' in query:
                        value=query.split(" ")
                        p1=value[-1]+"-"
                        #print(p1,type(p1))
                        #print(dict_days)
                        #p2=value[-2]
                        p2=value[-2].lower()
                        #print(p2)
                        p21=month_dict[p2]+"-"
                        #print(p21,type(p21))
                        try:
                            p3=str(dict_days[value[-4]])
                        except Exception as e:
                            p3=str(dict_days[value[-3]])
                        #mid="-"
                        date_str=p1+p21+p3
                        #print(date_str)
                        sql_query="select name from tasks where deadline=%s"
                        mycursor.execute(sql_query, (date_str,))
                        resultset=mycursor.fetchall()
                        if resultset==[]:
                            speak("No tasks are scheduled on this day")
                        else:
                            speak("the tasks are")
                            for x in resultset:
                                speak(x)
                                print(x)
                        #print(p3,type(p3))











