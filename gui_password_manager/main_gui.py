import webbrowser
from tkinter import *
import ttkbootstrap as ttk
import DataStore as ds
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification

class dummy_data():
    def __init__(self):
        self.columns = ["ID","Site","Login","Password"]
        #self.data = [('1', 'http://www.google.com', 'login1', 'password1'), ('2', 'site2', 'login2', 'password2'), ('3', 'site3', 'login3', 'password3'), ('4', 'site4', 'login4', 'password4'), ('5', 'site5', 'login5', 'password5'), ('6', 'site6', 'login6', 'password6'), ('7', 'site7', 'login7', 'password7'), ('8', 'site8', 'login8', 'password8'), ('9', 'site9', 'login9', 'password9'), ('10', 'site10', 'login10', 'password10'), ('11', 'site11', 'login11', 'password11'), ('12', 'site12', 'login12', 'password12'), ('13', 'site13', 'login13', 'password13'), ('14', 'site14', 'login14', 'password14'), ('15', 'site15', 'login15', 'password15'), ('16', 'site16', 'login16', 'password16'), ('17', 'site17', 'login17', 'password17'), ('18', 'site18', 'login18', 'password18'), ('19', 'site19', 'login19', 'password19'),('20', 'site2', 'login2', 'password2'),('21', 'site2', 'login2', 'password2'),]
        self.database=ds.Database("baza", "Haselko")
        self.database.create_database()
        self.data=self.database.get_data_with_indices()

class PasswordManager(ttk.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.grid(row=0, column=0)

        #variables to show and edit data on the left
        self.show_id = ttk.DoubleVar(value=0)
        self.show_site = ttk.StringVar(value="")
        self.show_password = ttk.StringVar(value="")
        self.clicked_password = ttk.StringVar(value="")
        self.show_login = ttk.StringVar(value="")
        self.is_shown = ttk.BooleanVar(value=True)
        self.show_hide_button_text = ttk.StringVar(value="Show / Hide")

        #variables to add new data
        self.add_site = ttk.StringVar(value="")
        self.add_password = ttk.StringVar(value="")
        self.add_login = ttk.StringVar(value="")

        #variables for treeview
        self.db_data=dummy_data()
        self.columns = self.db_data.columns
        self.data = self.db_data.data

        #treeview container
        self.left_container = ttk.Frame(self)
        self.left_container.pack(padx=5, pady=10, side=LEFT, fill=Y)
        self.tree = self.create_treeview()

        #add entry container
        self.middle_container = ttk.Frame(self)
        label_add = ttk.Label(self.middle_container, text="Add new", style='secondary.Tlabel')
        label_add.pack(padx=5, pady=5)
        self.create_entry_add(self.add_site,"Site URL...")
        self.create_entry_add(self.add_login, "Login...")
        self.create_entry_add(self.add_password, "Password...")
        self.create_button_add("Add Entry",self.on_add_button)
        self.middle_container.pack(side=LEFT, padx=5, pady=5,fill=Y)

        #edit/show entry container
        self.right_container = ttk.Frame(self)
        label_edit_show = ttk.Label(self.right_container, text="Edit/Show", style='secondary.Tlabel')
        label_edit_show.pack(padx=5, pady=5)
        self.create_entry_show_edit(self.show_site)
        self.create_entry_show_edit(self.show_login)
        self.create_entry_show_edit(self.show_password)
        self.create_button_edit(self.show_hide_button_text.get(),self.on_show_button)
        self.create_button_edit("Submit changes",self.on_submit_changes_button)
        self.create_button_edit("Delete entry",self.on_delete_button)
        self.right_container.pack(side=LEFT, padx=5, pady=5, fill=Y)


        #add copy buttons
        self.copy_right_container = ttk.Frame(self)
        label_add = ttk.Label(self.copy_right_container, text="", style='secondary.Tlabel')
        label_add.pack(padx=5, pady=5)
        self.create_button_open_site("Open")
        self.create_button_copy("Copy", self.on_clipboard_login_button)
        self.create_button_copy("Copy", self.on_clipboard_password_button)
        self.copy_right_container.pack(side=RIGHT, pady=5,fill=Y)

    #tworzenie treeview z haslami
    def create_treeview(self):
        a = 20
        if(len(self.data)>20):
            a=20
        else:
            a= len(self.data)
        tree = ttk.Treeview(master=self.left_container, bootstyle = "secondary", columns=self.columns, show='headings', height=a)
        tree.grid_configure(row=0,column=0,columnspan=4,rowspan=5,padx=20, pady=20)

        tree.column("ID", width=50, anchor=CENTER)
        tree.column("Login", anchor=CENTER)
        tree.column("Password", anchor=CENTER)
        tree.column("Site", anchor=CENTER)

        tree.heading("ID", text="ID")
        tree.heading("Site", text="Site")
        tree.heading("Login", text="Login")
        tree.heading("Password", text="Password")

        tree.tag_configure('change_bg',background="#20374C")

        for i in self.data:
            if(int(i[0])%2==1):
                tree.insert("", "end", values=i, tags="change_bg")
            else:
                tree.insert("", "end", values=i)
            tree.bind("<<TreeviewSelect>>",self.tree_on_click_element)

        return tree

    #funkcja klikania elementu w treeview (przypisywanie wartosci do zmiennych)
    def tree_on_click_element(self, event):
        clickedItem = self.tree.focus()
        values = self.tree.item(clickedItem)["values"]
        self.show_password.set(value=values[3])
        self.clicked_password.set(value=values[3])
        self.show_site.set(value=values[1])
        self.show_login.set(value=values[2])
        self.show_id.set(value=values[0])
        self.is_shown.set(value=True)
        self.on_show_button("arg")
        print(values)
        return

    #template do pola fomularza dodawania hasla
    def create_entry_add(self,variable,placeholder_text):

        def on_add_entry_click(event):
            if entry.get() == placeholder_text:
                entry.delete(0, "end")  # delete all the text in the entry
                entry.insert(0, '')  # Insert blank for user input
                entry.config(foreground='white')
            return

        def on_add_focusout(event):
            if entry.get() == '':
                entry.insert(0, placeholder_text)
                entry.config(foreground='grey')
            return

        entry = ttk.Entry(self.middle_container, textvariable=variable,style="secondary.Tentry")

        entry.insert(0, placeholder_text)
        entry.bind('<FocusIn>', on_add_entry_click)
        entry.bind('<FocusOut>', on_add_focusout)
        entry.config(foreground='grey')

        entry.pack(padx=10,pady=10)
        return

    #template do pola formularza edycji
    def create_entry_show_edit(self,variable):
        entry = ttk.Entry(master=self.right_container, textvariable=variable, style="secondary.Tentry")
        entry.pack(padx=10, pady=10)
        return

    #template przycisku do funkcji edycji/chowania w kolumnie po srodku
    def create_button_edit(self,text, function ):
        button = ttk.Button(self.right_container, text=text, style="secondary.Tbutton",width=17,)
        button.bind("<Button-1>", function)
        button.pack(padx=10,pady=10)
        return

    #template przycisku do kopiowania w kolumnie po prawej stronie
    def create_button_copy(self,text, function ):
        button = ttk.Button(self.copy_right_container, text=text, style="secondary.Tbutton",width=5,)
        button.bind("<Button-1>", function)
        button.pack(padx=10,pady=10)
        return

    #przycisk do otwierania strony w przegladarce
    def create_button_open_site(self,text ):
        button = ttk.Button(self.copy_right_container, text=text, style="secondary.Tbutton",width=5,)
        button.bind("<Button-1>", lambda x:webbrowser.open_new(self.show_site.get()))
        button.pack(padx=10,pady=10)
        return

    #przycisk dodania nowego hasla
    def create_button_add(self, text, function ):
        button = ttk.Button(self.middle_container, text=text, style="secondary.Tbutton", width=17)
        button.bind("<Button-1>", function)
        button.pack(padx=10, pady=10)
        return

    #funkcja do pokazywania/chowania hasla w formularzu
    def on_show_button(self,arg):
        value = self.is_shown.get()
        value = not value
        self.is_shown.set(value=value)
        output = ""
        for char in self.clicked_password.get():
            output += "*"
        if(value==False):
            self.show_password.set(value=output)
            self.show_hide_button_text.set(value="Show")
        else:
            self.show_password.set(value=self.clicked_password.get())
            self.show_hide_button_text.set(value="Hide")
        return

    #funkcja kopiowania loginu do schowka
    def on_clipboard_login_button(self,arg):
        self.clipboard_clear()
        self.clipboard_append(f"{self.show_login.get()}")
        toast = ToastNotification(
            title="Copied to clipboard",
            message="Login copied to clipboard",
            duration=2000
        )
        toast.show_toast()
        return

    #funkcja kopiowania hasla do schowka
    def on_clipboard_password_button(self,arg):
        self.clipboard_clear()
        self.clipboard_append(f"{self.clicked_password.get()}")
        toast = ToastNotification(
            title="Copied to clipboard",
            message="Password copied to clipboard",
            duration=2000
        )
        toast.show_toast()
        return

    def on_submit_changes_button(self,arg):
        self.db_data.database.modify_entry(int(self.show_id.get()), [self.show_site.get(), self.show_login.get(), self.show_password.get()])
        self.destroy()
        self.__init__(master_window=app)
        return

    def on_add_button(self,arg):
        self.db_data.database.write_to_database((self.add_site.get(), self.add_login.get(), self.add_password.get()))
        self.destroy()
        self.__init__(master_window=app)
        return

    def on_delete_button(self,arg):
        self.db_data.database.delete_from_database(int(self.show_id.get()))
        self.destroy()
        self.__init__(master_window=app)
        return

if __name__ == "__main__":
    app = ttk.Window("PasswordManager","superhero",resizable=(False,False))
    app.geometry("1150x450")
    PasswordManager(app)
    app.mainloop()