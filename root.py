from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
from tkinter import filedialog as fd

import sqlite3 as lite

from shutil import copy
from os import remove
from user import User

class Root:
    def __init__(self, window, width, heigh):
        self.window = window
        
        self.width = width
        self.heigh = heigh
        self.heigh_header = heigh // 10
        self.heigh_body = heigh

        self.visible_register = False
        self.order = 'ASC'
        self.filter = 'SELECT * FROM users ORDER BY id ASC'

        # Colors
        self.camine = '#9B1D20'
        self.timberwolf = '#D9D6D0'
        self.oxford_blue = '#011936'
        self.dodger_blue = '#1F9EFF'
        self.paynes_gray = '#66717E'
        self.black = "#000"
        self.white = "#fff"

        # Create frames
        self.frame_header = Frame(self.window, width=self.width, height=self.heigh_header, bg= self.paynes_gray, relief= FLAT)
        self.frame_header.grid(row= 0, column= 0)

        self.frame_body = Frame(self.window, width=self.width, height=self.heigh_body, bg= self.timberwolf, pady= 20, relief= FLAT)
        self.frame_body.grid(row= 1, column= 0, pady= 1, padx= 0, sticky= NSEW)

        self.con = lite.connect('database.db')
    # Show table

    def show_table(self):
        arr_items = self.view_form()
    
        self.tree = ttk.Treeview(self.frame_users, selectmode= 'browse', height=  35,columns= ('Matricula','Nome',  'CPF','Cidade', 'Estado', 'Lotação'), show= 'headings')
        
        vsb = ttk.Scrollbar(self.frame_users, orient="vertical", command=self.tree.yview)

        hsb = ttk.Scrollbar(self.frame_users, orient="horizontal", command=self.tree.xview)

        head_table = ['Matricula','Nome',  'CPF','Cidade', 'Estado', 'Lotação']
        cont_header = 1

        for col in head_table:
            col_width = 300

            if col in ('Matricula', 'Estado', 'CPF'):
                col_width = 200

            self.tree.column(col, width=col_width, anchor= 'center')
            self.tree.heading(f'#{cont_header}', text= col)
            cont_header += 1

        for dic in arr_items:
            arr_header = []
            
            for key, item in dic.items():
                if key in ('id', 'name', 'cpf', 'uf', 'city', 'uf', 'sector'):
                    arr_header.append(item)
            
            self.tree.insert('', END, values= arr_header)

        self.tree.grid(row=1, column=1)
        vsb.grid(row= 1, column= 2, sticky= NS)
        hsb.grid(row=2, column=1, sticky=EW)
        
    def open_windowUser(self):
            try:
                tree_data = self.tree.focus()
                tree_dic = self.tree.item(tree_data)
                tree_list = tree_dic['values']

                id = tree_list[0]

                dic_cols = self.view_individual_form(id)

                

                User(dic_cols[0])
                self.show_table()
            except IndexError:
                messagebox.showerror('Erro', 'Seleciona um dos itens da tabela')

    # Button Functions
    def choose_image(self):
        image_user = fd.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg")]
            )

        self.img_string = image_user
        arr_img = self.img_string.split('/')
        self.img_name = arr_img[-1]

        if self.img_string != '':
            self.btn_image.configure(text = self.img_name)

    def add_user(self):
        self.register_values = []

        for en in self.en_register.values():
            self.register_values.append(en.get())
        
        copy(self.img_string, f'img/users/{self.img_name}')
        self.img_string = f'img/users/{self.img_name}'
        self.register_values.append(self.img_string)
        self.register_values[0] = int(self.register_values[0])
            
        for i in self.register_values:
            if i == '' :
                messagebox.showerror('Erro', 'Preencha todos os campos')
                
                return 
        self.insert_form(self.register_values)

        messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

        for en in self.en_register.values():
            en.delete(0, 'end')
        self.btn_image.configure(text = 'carregar'.upper())
        
    
    def del_user(self):
        try:
            tree_data = self.tree.focus()
            tree_dic = self.tree.item(tree_data)
            tree_list = tree_dic['values']

            id = tree_list[0]

            dic_cols = self.view_individual_form(id)
            
            img = dic_cols[0]['image']
            remove(img)

            self.delete_form(id)
            self.show_table()

            messagebox.showinfo('Sucesso', 'O item foi excluido')
        except IndexError:
                messagebox.showerror('Erro', 'Seleciona um dos itens da tabela')

    def filter_order(self):
        if self.order == 'ASC':
            self.order = 'DESC'
            self.btn_filter_order.configure(text = '⬇')
        else:
            self.order = 'ASC'
            self.btn_filter_order.configure(text = '⬆')
        
        self.filter_table()
    
    def filter_table(self):
        col = self.comb_filter_col.get()

        if col == 'Matricula':
            col = 'id'
        elif col == 'Nome':
            col = 'name'
        elif col == 'Cidade':
            col = 'city'
        elif col == 'Estado':
            col = 'uf'
        else:
            col = 'sector'
        self.filter = f'SELECT * FROM users ORDER BY {col} {self.order}'

        self.show_table()

    # CRUD Functions
    # Insert data
    def insert_form(self, i):
        with self.con:
            cur = self.con.cursor()
            query = "INSERT INTO users (id, name, cpf, rg, ufRG, marital_status, date_birth, address, number, complement, neighborhood, city, uf, cep, home_phone, phone, email, admission_date, sector, cep_sector, phone_sector, bank, agency, account, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cur.execute(query, i)
   # Read data
    def view_form(self): 
        arr_row =  []

        with self.con:
            self.con.row_factory = lite.Row
            cur = self.con.cursor()
            query = self.filter
            cur.execute(query)


            rows = cur.fetchall()

            for row in rows:
                arr_row.append(dict(row))

        
        return arr_row

    def view_individual_form(self, id):
        arr_data = []
        with self.con:
            self.con.row_factory = lite.Row
            cur = self.con.cursor()
            query = f'SELECT * FROM users WHERE id = {id}'
            cur.execute(query)

            rows = cur.fetchall()

            for i in rows:
                arr_data.append(dict(i))
           
        return arr_data
    
    def delete_form(self, id):
        with self.con:
            self.con.row_factory = lite.Row
            cur = self.con.cursor()
            query = f'DELETE FROM users WHERE id = {id}'
            cur.execute(query)

    