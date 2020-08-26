import tkinter as tk
from tkinter import filedialog
import windowItemModule as wim
from csv2xml_m import generate as cs2exe_gen
import os


root = tk.Tk()

class Cs2Xml_Gui:
    def __init__(self,root):
        self.default_sm = "Source_model"
        self.master = root
        self.master.title("csv2xml-gui")
        self.placeInCenter(500,130)
        self.master.resizable(False,False)

        #vars
        self.csv_file_name = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.Source_model = tk.StringVar()

        # gui creation
        # frames
        self.csv_frame = tk.Frame(self.master)
        self.csv_frame.pack()
        self.output_frame = tk.Frame(self.master)
        self.output_frame.pack()
        #csv
        csv_label = tk.Label(self.csv_frame,text="Select CSV File:")
        csv_label.pack()
        self.csv_item_frame = tk.Frame(self.csv_frame)
        self.csv_item_frame.pack()

        self.csv_entry = tk.Entry(self.csv_item_frame,textvariable=self.csv_file_name,width=65)
        self.csv_entry.pack(side=tk.LEFT)

        self.csv_button = tk.Button(self.csv_item_frame,text="...",command=self.select_csv,width=5)
        self.csv_button.pack(side=tk.LEFT)
        #file output
        file_label = tk.Label(self.output_frame,text="Select Output File Path:")
        file_label.pack()
        self.file_item_frame = tk.Frame(self.output_frame)
        self.file_item_frame.pack()

        self.file_entry = tk.Entry(self.file_item_frame,textvariable=self.output_file_path,width=65)
        self.file_entry.pack(side=tk.LEFT)

        self.file_button = tk.Button(self.file_item_frame,text="...",command=self.select_output,width=5)
        self.file_button.pack(side=tk.LEFT)

        #source_model
        #self.sm = wim.Entry(self.master,label="Source_model:",stringvar=self.Source_model,pady=0,entry_config={"justify":tk.CENTER})
        self.Source_model.set(self.default_sm)

        #submit
        self.convert_o = wim.SubmitButton(self.master,buttontext="Generate",donotdestroy=True,command=self.submit)
    def select_csv(self):
        tempfilepath = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select file",filetypes = (("CSV files","*.csv"),("all files","*.*")))
        if tempfilepath is not "":
            self.csv_file_name.set(tempfilepath)
        else:
            return "User canceled save"
    def select_output(self):
        tempfilepath = filedialog.asksaveasfilename(initialdir = os.getcwd(),title = "Select file",defaultextension=".xml",filetypes = (("XML file","*.xml"), ("all files","*.*")))
        if tempfilepath is not "":
            self.output_file_path.set(tempfilepath)
        else:
            return "User canceled save"
    def submit(self):
        if self.csv_file_name.get() == "":
            self.createPopup(wtitle="Error",wdescription="Please enter/select a proper CSV file")
            return False
        if not os.path.exists(self.csv_file_name.get()):
            self.createPopup(wtitle="Error",wdescription="CSV file does not exist")
            return False
        if self.output_file_path.get() == "":
            self.createPopup(wtitle="Error",wdescription="Please enter/select a proper CSV file")
            return False
        try:
            cs2exe_gen(self.csv_file_name.get(),self.output_file_path.get(),self.Source_model.get())
        except:
            print("Error in generation")
            self.createPopup(wtitle="Error",wdescription="Error in file conversion.\nDouble check your CSV file")
            return False
        def yes():
            self.csv_file_name.set("")
            self.output_file_path.set("")
            self.Source_model.set(self.default_sm)

        if os.path.exists(self.output_file_path.get()):
            self.createPopup(wtitle="Complete",wdescription="File converted.\nConvert another file?",yfunc=yes,wtype="yn",nfunc=lambda:self.master.quit())
        else:
            self.createPopup(wtitle="Error",wdescription="Error converting file.")

        return True
    def placeInCenter(self, width,height,window=None,place=True): #fixes x,y placement of window
        if window is None:
            window=self.master
        x = (window.winfo_screenwidth() // 2) - (width //2)
        y = (window.winfo_screenheight() // 2) - (height //2)
        if place==True:
            window.geometry("{}x{}+{}+{}".format(width,height,x,y))
        else:
            window.geometry("{}x{}".format(width,height))
    def createPopup(self,wtype="message",wtitle="Popup",wdescription="Description",okfunc=None,yfunc=None,nfunc=None,oktext="Ok",ytext="Yes",ntext="No"): # creates a popup
        #two types: message and yn
        top = tk.Toplevel(self.master)
        top.resizable(False,False)
        top.title(wtitle)
        self.placeInCenter(300,85,window=top)
        frame = tk.Frame(top)
        frame.pack(side=tk.TOP)
        bframe = tk.Frame(top)
        bframe.pack()

        desc = tk.Label(frame,text=wdescription)
        desc.configure(height=3)
        desc.pack()

        if wtype == "yn":
            ybutton = tk.Button(bframe,text=ytext,width=(len(ytext)*3))
            nbutton = tk.Button(bframe,text=ntext,width=(len(ytext)*3))
            ybutton.pack(side=tk.LEFT)
            nbutton.pack(side=tk.LEFT)
            if yfunc is None:
                def yfunc():
                    top.destroy()
                ybutton.configure(command=yfunc)
            else:
                def yfunc2():
                    yfunc()
                    top.destroy()
                ybutton.configure(command=yfunc2)
            if nfunc is None:
                def nfunc():
                    top.destroy()
                nbutton.configure(command=nfunc)
            else:
                def nfunc2():
                    nfunc()
                    top.destroy()
                nbutton.configure(command=nfunc2)
        else:
            button = tk.Button(frame,text=oktext,width=(len(oktext)*3))
            button.pack()
            if okfunc is None:
                def okfunc():
                    top.destroy()
                button.configure(command=okfunc)
            else:
                def okfunc2():
                    okfunc()
                    top.destroy()
                button.configure(command=okfunc2)

if __name__ == "__main__":
    gui = Cs2Xml_Gui(root)
    root.mainloop()
