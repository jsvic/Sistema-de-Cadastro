from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
from tkinter import filedialog as fd

from PIL import Image, ImageTk

from tkcalendar import Calendar, DateEntry

from root import Root

class Main(Root):
    def __init__(self, window, width, heigh):
        super().__init__(window, width, heigh) 

        app_img = Image.open('img/logo.png')
        app_img =  app_img.resize((45, 45))
        app_img = ImageTk.PhotoImage(app_img)

        # Config frame header
        self.app_logo = Label(self.frame_header,image= app_img, text= " CADASTRO", width= 900, compound= LEFT, relief= RAISED, anchor= NW, bd= 0, font= ('Verdana 20 bold'), bg= self.paynes_gray)
        self.app_logo.image = app_img
        self.app_logo.place(x= 0, y= 25)

        self.x_navBar = width - 350
        self.y_navBar = 40
        
        self.btn_navBar_register = Button(self.frame_header, command= self.navBar, text= 'cadastro', width= 15, bg= self.timberwolf)
        self.btn_navBar_register.place(x=self.x_navBar, y=self.y_navBar)

        self.btn_navBar_users = Button(self.frame_header, command= self.navBar,text= 'usuarios', width= 15, bg= self.timberwolf)
        self.btn_navBar_users.place(x=self.x_navBar + 150, y=self.y_navBar)
    
    def register(self):
        # Create and Config frame register

        self.frame_register = Frame(self.window, width=self.width, height=self.heigh_body, bg= self.timberwolf, pady= 20, relief= FLAT)
        self.frame_register.grid(row= 1, column= 0, padx= 0, sticky= NSEW)

        for i in range(12):
            self.frame_register.columnconfigure(i, weight=1)

        for i in range(18):
            self.frame_register.rowconfigure(i, weight=1)

        self.lb_register = {'Matricula': '', 'Nome': '', 'Cpf': '', 'Rg': '', 'UF RG':'', 'Estado Civil':'', 'Data de Nascimento':'', 'Endereço':'', 'N°':'', 'Complemento':'', 'Bairro':'', 'Cidade':'', 'UF':'', 'CEP':'', 'Telefone Residencial':'', 'Telefone':'', 'Email':'', 'Data de Admissão':'', 'Lotação':'', 'CEP Lotação':'', 'Telefone Lotação':'', 'Banco':'', 'Agência':'', 'Conta':''}


        row = 0
        column = 1
        i = 0

        for lab_text in self.lb_register:
            lab = Label(self.frame_register,
            text=lab_text, width=15, bg= self.timberwolf)
            lab.grid(row= row, column= column, sticky= E, padx= 10)


            row += 2

            if row > 12:
                row = 0
                column += 3
        
            self.lb_register[lab_text]= lab

        self.lb_image = Label(self.frame_register, text= 'Imagem', width=15, bg=self.timberwolf, justify='left')
        self.lb_image.grid(row= 13, column= 11, sticky=E, padx=10)

        self.lb_register['image'] = self.lb_image

        self.en_register =  {'id': '', 'name': '', 'cpf': '', 'rg': '', 'ufRG':'', 'marital_status':'', 'date_birth':'', 'address':'', 'number':'', 'complement':'', 'neighborhood':'', 'city':'', 'uf':'', 'cep':'', 'home_phone':'', 'phone':'', 'email':'', 'admission_date':'', 'sector':'', 'cep_sector':'', 'phone_sector':'', 'bank':'', 'agency':'', 'account':''}

        row = 0

        column = 2

        for en_text in self.en_register:
            if en_text == 'date_birth' or en_text == 'admission_date':
                en = DateEntry(self.frame_register, width= 12, background= self.paynes_gray, bordewidth= 2, year= 2025)

            else:
                en = Entry(self.frame_register, width= 30, 
                justify= 'left', font= ('Ivy 10 bold'))

            en.grid(row= row, column= column, sticky= W, padx= 10)

            row += 2

            if row > 12:
                row = 0
                column += 3
        
            self.en_register[en_text]= en

        self.btn_image = Button(self.frame_register, command= self.choose_image ,text= 'carregar'.upper(), width= 25,font= ('Ivy 10 bold'), bg= self.oxford_blue, fg= self.white)
        self.btn_image.grid(row= 13, column= 12, sticky= W, padx= 10)
        #self.en_register['image'] = self.btn_image

        
        btn_add_image = Image.open('img/adicionar.png')
        btn_add_image =  btn_add_image.resize((20, 20))
        btn_add_image = ImageTk.PhotoImage(btn_add_image)

        btn_add = Button(self.frame_register, command= self.add_user, image= btn_add_image, width= 140, text= ' adicionar'.upper(), font= ('Ivy 10 bold'), compound= LEFT, relief= RAISED, anchor= N ,bg= self.oxford_blue, fg= self.white)
        btn_add.image = btn_add_image
        btn_add.grid(row= 13, column= 14, sticky= W, padx= 10)

    def users(self):
        # Create and Config frame users
        self.frame_users = Frame(self.window, width=self.width, height=self.heigh_body, bg= self.timberwolf, pady= 20, relief= FLAT)
        self.frame_users.grid(row= 1, column= 0, padx= 0, sticky= NSEW)   
        
        #self.frame_users.columnconfigure(0, weight=1)
        #self.frame_users.columnconfigure(1, weight=12)
        for i in range(7):
            self.frame_users.columnconfigure(i, weight=3)
        for i in range(20):
            self.frame_users.rowconfigure(i, weight=3)

        self.frame_users.columnconfigure(2, weight=1)

        btn_view_user = Button(self.frame_users, command= self.open_windowUser,text='ver usuario'.upper(), compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.oxford_blue, fg= self.white)
        btn_view_user.place(x= self.width - 550, y= 22)
        
        btn_del_row = Button(self.frame_users, command= self.del_user ,text='excluir'.upper(), compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.oxford_blue, fg= self.white)
        btn_del_row.place(x= self.width - 400, y= 22)

        self.btn_filter_order =  Button(self.frame_users, command= self.filter_order,text='⬆', compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.oxford_blue, fg= self.white)
        self.btn_filter_order.place(x= self.width - 300, y= 22)
        
        comb_filter_colstringVar = StringVar()
        self.comb_filter_col = ttk.Combobox(self.frame_users, textvariable= comb_filter_colstringVar)

        self.comb_filter_col['values'] = ('Matricula', 'Nome', 'Cidade', 'Estado', 'Lotação')
        self.comb_filter_col['state'] = 'readonly'
        self.comb_filter_col.set('matricula')

        self.comb_filter_col.place(x= self.width - 250, y= 28)
     
        btn_filter = Button(self.frame_users, command= self.filter_table,text='filtrar'.upper(), compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.oxford_blue, fg= self.white)
        btn_filter.grid(row= 0, column=6, pady= 15)


        self.show_table()    

    def navBar(self):
        if self.visible_register:
            self.register()
            self.frame_users.destroy()
            
            self.visible_register = False

            self.btn_navBar_register.configure(bg= self.oxford_blue, fg= self.white)
            self.btn_navBar_users.configure(bg= self.timberwolf,  fg= self.black)

        else:
            self.users()
            self.frame_register.destroy()

            self.visible_register = True

            self.btn_navBar_users.configure(bg= self.oxford_blue, fg= self.white)
            self.btn_navBar_register.configure(bg= self.timberwolf, fg= self.black)

def main():
    # Create window
    root = Tk()
    root.title('')
    root.geometry('900x600')
    style = ttk.Style(root)
    style.theme_use('clam')
    root.state('zoomed')

    Main(root, 1920, 1080).register()
    
        
    root.mainloop()

if __name__ == '__main__':
    main()