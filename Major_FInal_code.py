from tkinter import *
from PIL import Image,ImageTk
import smtplib
import time
import datetime
import requests
import json
import threading
import RPi.GPIO as GPIO
from datetime import datetime


# medicine schedule
# email_based_ patient_requiedments
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT) #light
GPIO.setup(11,GPIO.OUT) #fan
GPIO.setup(13,GPIO.OUT) #bed
p = GPIO.PWM(13, 50) # GPIO 13 for PWM with 50Hz


def api_based_patient_requiements(val):
    print("send data "+ str(val))
    #url="http://127.0.0.1:8000/staff/"
    url="http://192.168.0.192:8000/staff/"
    mydict={1:"Food Request",2:"Water Request",3:"Nurse Vist",4:"Washroom Assistance",5:"Emergency!! Doctor Needed"}
    RoomID=1
    priority_dict={1:1,2:1,3:3,4:2,5:4}

    #newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data=requests.post(url,json={"RoomID":RoomID,"Text":mydict[val],"Priority":priority_dict[val]})#,headers=newHeaders)
    #print(data.json())
    #print(data.status_code)

class gui:
    def __init__(self,master):
        #main 
        self.master=master
        self.master.geometry("920x400")
        self.master.title("Major_UI")
        self.master["bg"]="Black"

        #Control_frame
        self.room_frame=LabelFrame(self.master,text="Controls",bg='black',fg="white",bd=5,highlightbackground="white",highlightcolor="white")
        self.room_frame.grid(row=1,column=0,sticky=N)

        #Middle frame
        self.middle=LabelFrame(self.master,text="Services",fg='white',bg='black',bd=5,highlightbackground="white",highlightcolor="white")
        self.middle.grid(row=1,column=1,padx=5,pady=5)

        # Images
        self.on=PhotoImage(file="on.png")
        self.plus=PhotoImage(file="plus.png")
        self.minus=PhotoImage(file="minus.png")
        self.off=PhotoImage(file="off.png")
        self.not_well=PhotoImage(file="not_well.png")
        self.food=PhotoImage(file="food.png")
        self.water=PhotoImage(file="water.png")
        self.washroom=PhotoImage(file="washroom.png")
        self.emercency_call=PhotoImage(file="Emergency_call.png")
        self.medi=PhotoImage(file="medi.png")
        self.bed=PhotoImage(file="bed.png")
        self.o2=PhotoImage(file="o2.png")
        self.heart_rate=PhotoImage(file="heart_rate.png")
        self.temperature=PhotoImage(file="thermometers.png")

        #Variables
        self.light_is_on=True
        self.curtain_is_open=True
        self.room_temp=24
        self.bed_angle=2.5
        p.start(self.bed_angle)
        #p.stop()

        #Sensors Variables
        self.oxometer=12
        self.pulse=23
        self.temp_patient=0
        
        #led pins
        GPIO.output(7,True)
        GPIO.output(11,True)
        self.count=1
        
        #time_list
        self.time_lst=["09","15","18","21"]
        #GPIO.cleanup()
        #bt=Button(self.master,text="Quit",command=self.master.destroy)
        #bt.grid(row=2,column=2,sticky=S)


    def light_switch(self):
        print("Light_switch_used")
        if self.light_is_on:
            self.light_is_on=False
            self.light_bt.config(image=self.off)
            #__________________rpi.digitalwrite__________________________________
            GPIO.output(7,False)
        else:
            self.light_is_on=True
            self.light_bt.config(image=self.on)
            #__________________rpi.digitalwrite__________________________________
            GPIO.output(7,True)

    def curtain_switch(self):
        print("Fan_used")
        if self.curtain_is_open:
            self.curtain_is_open=False
            self.curtain_bt.config(image=self.off)
            #__________________rpi.digitalwrite__________________________________
            GPIO.output(11,False)
        else:
            self.curtain_is_open=True
            self.curtain_bt.config(image=self.on)
            #__________________rpi.digitalwrite__________________________________
            GPIO.output(11,True)
    
    def temp_control_unit(self,val):
        if val:
            if self.room_temp>16:
                self.room_temp-=1
                self.temp_degree_label.config(text="  "+str(self.room_temp)+u"\N{DEGREE SIGN}"+'C  ')
                #__________________rpi.digitalwrite__________________________________
        else:
            if self.room_temp<30:
                self.room_temp+=1
                self.temp_degree_label.config(text="  "+str(self.room_temp)+u"\N{DEGREE SIGN}"+'C  ')
                #__________________rpi.digitalwrite__________________________________

    def room_control(self):
        self.light_bt=Button(self.room_frame,text="Light   ",image=self.on,compound=RIGHT,borderwidth=0,font=("Helvatica",18),bg='black',fg="white",command=self.light_switch)
        self.light_bt.grid(row=0,column=0)

        self.curtain_bt=Button(self.room_frame,text="Fan      ",image=self.on,compound=RIGHT,borderwidth=0,font=("Helvatica",15),bg='black',fg="white",command=self.curtain_switch)
        self.curtain_bt.grid(row=1,column=0,pady=2)

        #Temp_control
        temp_frame=LabelFrame(self.room_frame,text="Room Temperture\nControl",fg='white',bg='black',bd=5,highlightbackground="white",highlightcolor="white")
        temp_frame.grid(row=3,column=0)
        bt=Button(temp_frame,image=self.minus,borderwidth=0,bg='black',command=lambda: self.temp_control_unit(True))
        bt.grid(row=0,column=0)
        #self.label________________need to update in future________________________________________________
        self.temp_degree_label=Label(temp_frame,text="  "+str(self.room_temp)+u"\N{DEGREE SIGN}"+'C  ',font=("Helvatica",15))
        self.temp_degree_label.grid(row=0,column=1,padx=5)
        #__________________________________________________________________________________________________
        bt=Button(temp_frame,image=self.plus,borderwidth=0,bg='black',command=lambda: self.temp_control_unit(False))
        bt.grid(row=0,column=2)

    def bed_control_unit(self,val):
        if val:
            if self.bed_angle>2.5:
                p.start(self.bed_angle)
                self.bed_angle-=2.5
                mydict={2.5:"0",5:"45",7.5:"90",10:"120",12.5:"150"}
                self.bed_angle_label.config(text=" "+mydict[self.bed_angle]+u"\N{DEGREE SIGN}")
                #__________________rpi.digitalwrite__________________________________
                p.ChangeDutyCycle(self.bed_angle)
                #p.stop()
        else:
            if self.bed_angle<10:
                p.start(self.bed_angle)
                self.bed_angle+=2.5
                mydict={2.5:"0",5:"45",7.5:"90",10:"120",12.5:"150"}
                self.bed_angle_label.config(text=" "+mydict[self.bed_angle]+u"\N{DEGREE SIGN}")
                #__________________rpi.digitalwrite__________________________________
                p.ChangeDutyCycle(self.bed_angle)
                #p.stop()

    def bed_control(self):
        bed_cont=LabelFrame(self.room_frame,text="Bed Control",fg='white',bg='black',bd=5,highlightbackground="white",highlightcolor="white")
        bed_cont.grid(row=4,column=0,padx=5,pady=5)
        lb=Label(bed_cont,text="  Bed Angle    ",image=self.bed,compound=LEFT,font=("Helvatica",15,'bold'),bg='black',fg='white')
        lb.grid(row=0,column=0,columnspan=3)
        #button func()
        bt=Button(bed_cont,image=self.minus,borderwidth=0,bg='black',command=lambda:self.bed_control_unit(True))
        bt.grid(row=1,column=0)
        #self.label________________need to update in future________________________________________________
        self.bed_angle_label=Label(bed_cont,text="  "+str('0')+u"\N{DEGREE SIGN}",font=("Helvatica",15))
        self.bed_angle_label.grid(row=1,column=1,padx=5)
        #__________________________________________________________________________________________________
        bt=Button(bed_cont,image=self.plus,borderwidth=0,bg='black',command=lambda:self.bed_control_unit(False))
        bt.grid(row=1,column=2)

    def medicine_reminder_event(self):
        self.medicine_reminder_Button.config(bg="green")
        #______________________RPI.buzzer___________________________________

    def medicine_reminder(self):
        medicine_frame=LabelFrame(self.middle,text="Medicine Reminder",fg='white',bg='black',bd=5,highlightbackground="white",highlightcolor="white")
        medicine_frame.grid(row=1,column=0,padx=5,pady=5)
        #self.label_____________________________need_to_update_on_future___________________________________
        self.medicine_reminder_Button=Button(medicine_frame,text="Medicine Time",image=self.medi,compound=RIGHT,font=("Helvatica",15),bg='green',command=self.medicine_reminder_event)
        self.medicine_reminder_Button.grid(row=0,column=0)
        #add buzzer if want
        #___________________________________________________________________________________________________
    
    def sensor(self):
        sensor_frame=LabelFrame(self.middle,text="Connect Sensors",fg='white',bg='black',bd=5,highlightbackground="white",highlightcolor="white")
        sensor_frame.grid(row=3,column=0,padx=5,pady=5)
        lb=Label(sensor_frame,text="Oxygen",image=self.o2,compound=LEFT,font=("Helvatica",15),fg='white',bg='black')
        lb.grid(row=0,column=0,padx=0,sticky=W)
        lb=Label(sensor_frame,text=" Heart\nRate",image=self.heart_rate,compound=LEFT,font=("Helvatica",15),fg='white',bg='black')
        lb.grid(row=1,column=0,pady=0,padx=0,sticky=W)
        lb=Button(sensor_frame,text="Temp\nCheck",image=self.temperature,compound=LEFT,font=("Helvatica",15),fg="white",bg="black")
        lb.grid(row=2,column=0,padx=0,pady=0,sticky=W)
        #self.label_____________________________need_to_update_on_future___________________________________
        self.lb_O2=Label(sensor_frame,text="99"+"% ",font=("Helvatica",20),fg='white',bg='black')
        self.lb_O2.grid(row=0,column=1)
        self.lb_Pulse=Label(sensor_frame,text="72"+" bpm",font=("Helvatica",20),fg='white',bg='black')
        self.lb_Pulse.grid(row=1,column=1,)
        self.lb_temp=Label(sensor_frame,text="97"+u"\N{DEGREE SIGN}"+"F",fg='white',bg="black",font=("Helvatica",20))
        self.lb_temp.grid(row=2,column=1)
        #___________________________________________________________________________________________________


    def alert(self):
        alert_frame=LabelFrame(self.master,text="Patient Requied",fg='white',bg='black',bd=5,highlightbackground="white",highlightcolor="white")
        alert_frame.grid(row=1,column=2,padx=5,pady=10,sticky=N)
        bt=Button(alert_frame,text="Food",image=self.food,compound=LEFT,font=("Helvatica",15),fg='white',bg='black',relief=RAISED,bd=5,command=lambda: api_based_patient_requiements(1))
        bt.grid(row=0,column=0,padx=5)
        bt=Button(alert_frame,text="Water",image=self.water,compound=LEFT,font=("Helvatica",15),fg='white',bg='black',relief=RAISED,bd=5,command=lambda: api_based_patient_requiements(2))
        bt.grid(row=0,column=1)
        bt=Button(alert_frame,text="Not Feeling Well",image=self.not_well,compound=LEFT,font=("Helvatica",15),fg='white',bg='black',relief=RAISED,bd=5,command=lambda: api_based_patient_requiements(3))
        bt.grid(row=1,column=0,columnspan=2,pady=5,ipadx=2)
        bt=Button(alert_frame,text="Wash\nroom",image=self.washroom,compound=LEFT,font=("Helvatica",15),fg='white',bg='black',relief=RAISED,bd=5,command=lambda: api_based_patient_requiements(4))
        bt.grid(row=2,column=0,padx=5)
        bt=Button(alert_frame,text="Emergency",image=self.emercency_call,compound=LEFT,font=("Helvatica",15),fg='white',bg='black',relief=RAISED,bd=5,command=lambda: api_based_patient_requiements(5))
        bt.grid(row=2,column=1)

    def mlx90614_sesors_values(self):
        #pymlx90614
        from smbus2 import SMBus
        from mlx90614 import MLX90614
        bus = SMBus(1)
        sensor = MLX90614(bus, address=0x5A)
        print("ambinous temp:",sensor.get_amb_temp())
        print("obj temp:",sensor.get_obj_temp())
        #cel=str(sensor.get_obj_temp)
        #farahite=(int(cel*1.8)+32
        #print("Farahite ",farahite)
        self.temp_patient=int(sensor.get_obj_temp()*1.8)+32
        print("mlx90614: ",self.temp_patient)
        bus.close()


    def max30100_sesors_values(self):
        #pymax30100
        import time
        import max30100
        mx30 = max30100.MAX30100()
        mx30.enable_spo2()
        mx30.read_sensor()
        mx30.ir, mx30.red
        hb = int(mx30.ir/100)
        spo2=int(mx30.red/100)
        if mx30.ir != mx30.buffer_ir:
            self.pulse=hb
            print("pulse: ",hb)
        if mx30.red != mx30.buffer_red:
            self.oxometer=spo2
            print("spo2: ",spo2)
        #time.sleep(2)

    def api_based_Sensor(self):
        #url="http://127.0.0.1:8000/"
        url="http://192.168.0.192:8000/"
        data=requests.post(url,json={"Oxygen":self.oxometer,"Pulse":self.pulse,"Temprature":self.temp_patient})

    def autoplay(self):
        self.count+=1
        if self.count==10000:
            p.stop()
            GPIO.cleanup()
        self.max30100_sesors_values()
        self.mlx90614_sesors_values()
        self.lb_O2.config(text=str(self.oxometer)+" %")
        self.lb_Pulse.config(text=str(self.pulse)+" bpm")
        self.lb_temp.config(text=str(self.temp_patient)+u"\N{DEGREE SIGN}"+"F")
        self.api_based_Sensor()
        
        current_time=datetime.now()
        current_time_format=current_time.strftime("%H")
        if current_time_format == "00":
            self.time_lst=["9","15","18","21"]
        if str(current_time_format) in self.time_lst:
            self.time_lst.pop(0)
            self.medicine_reminder_Button.config(bg='red')
            print(self.time_lst)
        self.master.after(1000,self.autoplay)
    




    



root=Tk()
#root.geometry("920x400")
#root.title("Major_UI")
#root["bg"]="Black"
obj=gui(root)
obj.room_control()
obj.bed_control()
obj.medicine_reminder()
obj.alert()
obj.sensor()
#obj.max30100_sesors_values()
#obj.mlx90614_sesors_values()
obj.autoplay()
#root.after(1000,obj.autoplay())
root.mainloop()



