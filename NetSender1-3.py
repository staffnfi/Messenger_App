#Version 1.3: Options menu with ability to change display name. Still needs advanced options for checking and changing nework settings.

import tkinter as tk
import socket
import threading

#View
class Interface:
    #Create root window and widgets
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Net Sender")
        self.root.geometry("300x125")
        self.root.resizable(False, False)
        self.display_name_label()
        self.display_name_entry()
        self.start_button("Ok")

    #Create main interface window
    def main_window(self):
        self.main = tk.Toplevel()
        self.main.title("Net Sender")
        self.main.geometry("300x600")
        self.main.resizable(False, False)
        self.message_screen()
        self.text_entry()
        self.submit_button("Send")
        self.address_box()
        self.menu_bar()
        
#############################################################################################
#Set up window widgets

    #Label for display name instructions
    def display_name_label(self):
        self.display_name = tk.Label(text="Enter your display name", font=('Courier', 12))
        self.display_name.pack()

    def display_name_entry(self):
        self.enter_name = tk.Entry(width=20, font=('Courier', 12))
        self.enter_name.insert(0, "Default Name")
        self.enter_name.pack(pady=5)
        
    # start button
    def start_button(self, name):
        self.start = tk.Button(self.root, text=name, width=20, font=('Courier', 12))
        self.start.pack()

##############################################################################################
#Main window widgets

    #Widget for entering text
    def text_entry(self):
        self.text_box = tk.Entry(self.main, width=48)
        self.text_box.pack()

    def address_box(self):
        self.address_entry = tk.Entry(self.main, width=15)
        self.address_entry.pack()

    #Submit button
    def submit_button(self, name):
        self.submit = tk.Button(self.main,text=name)
        self.submit.pack()

    #Main screen for conversation. State is disabled so cannot be typed into directly.
    def message_screen(self):
        self.screen = tk.Text(self.main, width=36, height=30, state="disabled")
        self.screen.pack()

    def menu_bar(self):
        self.menu = tk.Menu(self.main)
        self.optionsmenu = tk.Menu(self.menu, tearoff=0)
        self.optionsmenu.add_command(label="Change display name", command=self.name_change_window)
        self.menu.add_cascade(label="Options", menu=self.optionsmenu)
        self.main.config(menu=self.menu)


    def name_change_window(self):
        self.root.deiconify()

        
#Controller
class Controllers:
    def __init__(self):
        self.view = Interface()  # Register interface
        self.model = app_data()
        self.view.start.bind("<Button>", self.start_callback) #Binds mouse click to button for callback
        self.view.root.bind("<Return>", self.start_callback) #Binds enter to root window for callback
        self.view.enter_name.focus()

    def main_init(self):
        self.view.submit.bind("<Button>", self.btn_callback) #Binds mouse click to button
        self.view.main.bind("<Return>", self.btn_callback) #Binds enter to root window for submission of chat messages
        self.model.sock.bind((self.model.best_local_address, self.model.PORT))
        self.server = threading.Thread(target=self.recv_message).start()  # receiver runs on seperate thread to stop blocking
        self.view.main.bind("<<NameChange>>", self.name_change_callback)
        self.view.text_box.focus_force()

    #This needs to create a pop up window for users to change display name
    def name_change_callback(self, event):
        print(event)
        self.view.name_change_window()

    #Callback for start button
    def start_callback(self, event):
        self. model.display_name = self.view.enter_name.get()
        self.view.root.withdraw() #Hides setup window
        if not hasattr(self.view, "main"): 
            self.view.main_window()
            self.main_init()

    #Call back for submit button. Calls text_to_screen. Sends message via UDP
    def btn_callback(self, event):
        address = self.view.address_entry.get()
        self.model.destination_addr = address       
        text = self.model.display_name + ": " + self.view.text_box.get()
        self.text_to_screen(text)
        self.model.sock.sendto(text.encode('utf-8'), (self.model.destination_addr, self.model.PORT))  

    #Insert text in to screen and makes sure screen remains locked each time by toggling state
    def text_to_screen(self, text_in):
        self.view.screen.configure(state="normal")
        self.view.screen.insert(tk.END, text_in+"\n\n")
        self.view.screen.configure(state="disabled")
        self.view.text_box.delete(0, tk.END)

    #Listens to buffer for incoming message
    def recv_message(self):
        while True:
            #print(self.best_local_address)
            data, address = self.model.sock.recvfrom(128)  # Constantly checks message buffer and assigns last recieved data to variables
            #print(address)
            data = data.decode('utf-8')
            self.text_to_screen(data)


#Model
class app_data:
    def __init__(self):
        self.PORT = 1060
        self.best_local_address = self.find_local_address()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._destination_addr = socket.gethostname()
        self.display_name = "Default Name"

    #destination_addr getter
    @property
    def destination_addr(self):
        #print("I am in property")
        return self._destination_addr

    # destination_addr setter with primitive validation of existence of address. NEEDS MORE WORK!
    @destination_addr.setter
    def destination_addr(self, new_address):
        #print("I am in setter")
        if new_address == "":
            pass
        else:
            self._destination_addr = new_address
        #print(self._destination_addr)

    # Tries to ensure local ip is the same as used for internet connection
    def find_local_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            address = s.getsockname()[0]
            s.close()
            return address
        except:
            address = socket.gethostname()
            return address



#Unit test
if __name__ == "__main__":
    c = Controllers()
    tk.mainloop()

#if hasattr(obj, 'attr_name')

