from Tkinter import *
import tkFileDialog
import os
from Communicator import Communicator
import Interpreter

class App:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(master)
        self.frame.pack(side= BOTTOM)
        self.Startup_Screen()
        
    def Startup_Screen(self):
        self.brickalicious_l = Label(self.frame, text= "BRICKALICIOUS", font = ("Helvetica", 72))
        self.brickalicious_l.grid(row = 0, column = 0, sticky = N, padx=30, pady=10)
        
        self.subtitle_l = Label(self.frame, text = "The 3D LEGO printing system", font= ("Helvetica", 28))
        self.subtitle_l.grid(row = 1, column = 0)
        
        self.credit_l = Label(self.frame, text= "brought to you by Inigo Beitia, Ollie Gallitz, Larissa Little, and Noam Rubin")
        self.credit_l.grid(row = 2, column = 0)
        
        self.choose_file_b = Button(self.frame, text="Choose File to Print", font=("Helvetica", 14),command=self.select_file)
        self.choose_file_b.grid(row=3, column = 0, sticky = S, pady=20)

    def Select_File_Screen(self):
        self.file = tkFileDialog.askopenfile(parent=self.master,mode='rb',title='Choose a file')
        if self.file != None:
            data = self.file.read()
            self.file.close()
        
        self.Begin_Printing_Screen()
        
    def Begin_Printing_Screen(self):        
        self.file_l = Label(self.frame, text = self.file.name, font=("Helvetica", 16))
        self.file_l.grid(columnspan=2, sticky=N, pady = 20, padx=10)
        
        self.change_file_b = Button(self.frame, text = "Change File", font=("Helvetica", 14), command=self.reselect_file)
        self.change_file_b.grid(row=1, column = 0, pady= 40, padx=10)
        
        self.begin_printing_b = Button(self.frame, text = "Begin Printing", font=("Helvetica", 14),command= self.begin_printing)
        self.begin_printing_b.grid(row=1, column = 1)
        
    def Printing_Screen(self):
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.grid(row=0, column=2, sticky=N+S)
        
        self.printing_l = Text(self.frame)
        self.printing_l.grid(row=0, column = 0)
        self.scrollbar.config(command=self.printing_l.yview)

        self.pause_b = Button(self.frame, text="Pause Printing", font=("Helvetica", 14),command= self.Pause_Screen)
        self.pause_b.grid(row=1, column = 0, pady=10)
        
        self.quit_b = Button(self.frame, text= "Quit Printing", font=("Helvetica", 14),command= self.to_quit)
        self.quit_b.grid(row=2, column = 0, pady=10)
        
        # Interpreter
        self.display_message("Reading file...")
        bricks = Interpreter.parsing(self.file.name)
        Interpreter.translation(bricks)
        self.display_message("Parsing file...")
        build_order = Interpreter.generate_build_order(bricks)
        self.display_message("Generating build order...")
        #build_list = Interpreter.generate_build_list(build_order)
        
        # Communication
        self.display_message("Opening communication channel...")
        com = Communicator()
        com.setup_connection()
        self.display_message("Communication established.")
        self.display_message("Printing...")
        bricks = com.print_bricks(build_order)
        for instruction in bricks:
    		  com.send_message(instruction[0], instruction[1])
        com.close_connection()
    
    def display_message(self, string):
        self.printing_l.config(state=NORMAL)
        self.printing_l.insert(0.0, string + "\n")
        self.printing_l.grid(row=0, column = 0)
        self.printing_l.config(state=DISABLED)
        self.printing_l.yview(END)    
        self.scrollbar.set(1.0,1.0)
    
    def Pause_Screen(self):
        self.printing_l.grid_forget()
        self.pause_b.grid_forget()
        self.quit_b.grid_forget()
        self.scrollbar.grid_forget()
        
        self.paused_l = Label(self.frame,text= "Job has been Paused",font=("Helvetica", 16))
        self.paused_l.grid(columnspan=2, pady=20)
        
        self.resume_b = Button(self.frame, text="Resume", font=("Helvetica", 14),command = self.resume_printing)
        self.resume_b.grid(row=1, column=0, pady=10,padx=30)
        
        self.pause_to_quit_b = Button(self.frame, text = "Quit Job", font=("Helvetica", 14),command = self.pause_to_quit)
        self.pause_to_quit_b.grid(row = 1, column = 1, pady=10,padx=30)
        
    def Quit_Screen(self):
        self.quit_text_l = Label(self.frame, text="You have chosen to quit printing",font=("Helvetica", 16))
        self.quit_text_l.grid(row = 0, column= 0, pady=20)
        
        self.restart_b = Button(self.frame, text="Restart Process", font=("Helvetica", 14),command=self.restart)
        self.restart_b.grid(row=1, column =0, pady=10)
                
    def select_file(self):
        #From Startup Screen to Select File Screen
        self.brickalicious_l.grid_forget()
        self.subtitle_l.grid_forget()
        self.credit_l.grid_forget()
        self.choose_file_b.grid_forget()
        
        self.Select_File_Screen()
        
    def reselect_file(self):
        #From Begin Printing Screen to Select File Screen
        self.file_l.grid_forget()
        self.change_file_b.grid_forget()
        self.begin_printing_b.grid_forget()
        
        self.Select_File_Screen()
        
    def begin_printing(self):
        #From Begin Printing Screen to Printing Scree
        self.file_l.grid_forget()
        self.change_file_b.grid_forget()
        self.begin_printing_b.grid_forget()
        
        self.Printing_Screen()
        
    def resume_printing(self):
        #From Pause Screen to Printing Screen
        self.paused_l.grid_forget()
        self.resume_b.grid_forget()
        self.pause_to_quit_b.grid_forget()
        
        self.Printing_Screen()
        
    def pause_to_quit(self):
        #From Pause Screen to Quit Screen
        self.paused_l.grid_forget()
        self.resume_b.grid_forget()
        self.pause_to_quit_b.grid_forget()
        
        self.Quit_Screen()
        
    def to_quit(self):
        #From Printing Screen to Quit Screen
        self.scrollbar.grid_forget()
        self.printing_l.grid_forget()
        self.pause_b.grid_forget()
        self.quit_b.grid_forget()
        
        self.Quit_Screen()
        
    def restart(self):
        #From Quit Screen to Startup Screen
        self.quit_text_l.grid_forget()
        self.restart_b.grid_forget()
        
        self.Startup_Screen()
        
    
        
root = Tk()
root.minsize(500,250)
app = App(root)

root.mainloop()

