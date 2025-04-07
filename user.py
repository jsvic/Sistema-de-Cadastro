from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox
from tkinter import filedialog as fd

from PIL import Image, ImageTk

import sqlite3 as lite

from tkcalendar import Calendar, DateEntry

from shutil import copy
from os import remove

class User:
    def __init__(self, dic):
        # Colors
        self.camine = '#9B1D20'
        self.timberwolf = '#D9D6D0'
        self.oxford_blue = '#011936'
        self.dodger_blue = '#1F9EFF'
        self.paynes_gray = '#66717E'
        self.black = "#000"
        self.white = "#fff"

        self.con = lite.connect('database.db')

        self.window =  Toplevel()
        self.window.title(dic['name'])
        self.window.geometry('865x550')
        self.window.resizable(width= FALSE, height= FALSE)
        style = ttk.Style(self.window )
        style.theme_use('clam')

        self.frame_user = Frame(self.window, width=550, height= 855, bg= self.timberwolf, relief= FLAT)
        self.frame_user.grid(row= 0 , column= 0)

        for i in range(7):
            self.frame_user.columnconfigure(i, weight= 1)
        
        for i in range(9):
            self.frame_user.rowconfigure(i, weight= 3)
        
        col = 1
        row = 1

        for key, value in dic.items():
            if key != 'image':
                lb = Label(self.frame_user, text= key.upper(), width= 15, bg= self.timberwolf, fg= self.oxford_blue)
                lb.grid(row= row, column= col, sticky=N, padx= 2, pady= 20)
                
                col += 2
                if col >= 5:
                    col = 0
                    row += 1
            else:
                img_string = dic['image']
                img_user = Image.open(img_string)
                img_user = img_user.resize((30, 30))
                img_user = ImageTk.PhotoImage(img_user)

                lb_img = Label(self.frame_user, image= img_user, width= 15, height= 20)
                lb_img.image = img_user
                lb_img.grid(row= 1, column= 0, sticky=N, padx= 2, pady= 20)

                self.img_user = value
                self.img_string = value
                arr_img = self.img_string.split('/')
                self.img_name = arr_img[-1]
        

        col = 2
        row = 1

        self.ls_entrys = []

        for key, value in dic.items():
            if key not in ('date_birth', 'admission_date', 'image'):
                en = Entry(self.frame_user, width= 20, 
                justify= 'left', font= ('Ivy 10 bold'))

                en.grid(row= row, column= col, sticky= W, padx= 3, pady= 20)
                en.insert(0, value)

                en.configure(state='disabled')
                
                col += 2
                if col >= 6:
                    col = 1
                    row += 1
                self.ls_entrys.append(en)
            elif key in ('date_birth', 'admission_date'):
                en = DateEntry(self.frame_user, width= 12, background= self.paynes_gray, bordewidth= 2, year= 2025)
                en.configure(state='disabled')
                en.grid(row= row, column= col, sticky= W, padx= 3, pady= 20)
                en.insert(0, value)
            
                col += 2
                if col >= 6:
                    col = 1
                    row += 1
                
                self.ls_entrys.append(en)
            
        self.btn_user_update =  Button(self.frame_user, text='atualizar'.upper(), command= self.update_user, compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.oxford_blue, fg= self.white)
        self.btn_user_update.grid(row= 9, column= 5)
    
    def cancel_update(self):
        self.btn_update_confirm.destroy()
        self.btn_update_cancel.destroy()
        self.btn_user_update =  Button(self.frame_user, text='atualizar'.upper(), command= self.update_user, compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.oxford_blue, fg= self.white)
        self.btn_user_update.grid(row= 9, column= 5)
    
    def choose_image(self):
        image_user = fd.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg")]
            )

        self.img_string = image_user
        arr_img = self.img_string.split('/')
        self.img_name = arr_img[-1]

        if self.img_string != '':
            self.btn_update_image.configure(text = self.img_name)
        remove(self.img_user)
        copy(self.img_string, f'img/users/{self.img_name}')
        self.img_string = f'img/users/{self.img_name}'
        #self.ls_entrys.append(self.img_string)            
        self.img_user = self.img_string

    def confirm_update(self):
        self.ls_values = []
    
        for i in self.ls_entrys:
            print(i.get())
            print(i)
            self.ls_values.append(i.get())

        
        self.ls_values.append(self.img_user)
        id_user = self.ls_values[0]
        self.ls_values.pop(0)
        self.ls_values.append(id_user)

        print('='*50)
        print(self.ls_values)
        print(self.ls_values[24])
        print(self.img_user)
        print('='*50)

        with self.con:
            cur = self.con.cursor()

            query = f'UPDATE users SET name = ?, cpf = ?, rg = ?, ufRG = ?, marital_status = ?, date_birth = ?, address = ?, number = ?, complement = ?, neighborhood = ?, city = ?, uf = ?, cep = ?, home_phone = ?, phone = ?, email = ? ,admission_date= ?, sector = ?, cep_sector = ?, phone_sector = ?, bank = ?, agency = ?, account = ?, image = ? WHERE id = ?'
            cur.execute(query, self.ls_values)

        messagebox.showinfo('Sucesso', 'Os dados foram atualizados com sucesso')

        self.window.destroy()

    def update_user(self):
        self.btn_user_update.destroy()
        

        self.btn_update_image =  Button(self.frame_user, text='imagem'.upper(), command=self.choose_image, compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.dodger_blue, fg= self.white)
        self.btn_update_image.grid(row= 9, column= 3)

        self.btn_update_cancel =  Button(self.frame_user, text='cancelar'.upper(), command= self.cancel_update, compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.camine, fg= self.white)
        self.btn_update_cancel.grid(row= 9, column= 4)

        self.btn_update_confirm =  Button(self.frame_user, text='confimar'.upper(), command=self.confirm_update, compound= LEFT, anchor= NW, overrelief= RIDGE, font= ('Ivy 10 bold'), bg= self.dodger_blue, fg= self.white)
        self.btn_update_confirm.grid(row= 9, column= 5)
        

        for i in self.ls_entrys[1:]:
            i.configure(state='normal')
        
        


