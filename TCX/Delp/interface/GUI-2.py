import tkinter
import tkinter.messagebox
import customtkinter
import serial

porta_serial = None
status_serial = "Desativada"
status_maquina = "Parada"
erro = "NAE"
customtkinter.set_appearance_mode("System")  # Modos: Dark e light
customtkinter.set_default_color_theme("blue")  # Temas: 

texto = f"Status da conexão serial: {status_serial}\n"
texto += f"Status da máquina: {status_maquina}\n"
texto += f"Informação de erro: {erro}"

class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        global texto

        self.title("Delp")
        self.iconbitmap('./Delp/interface/img/logo.ico')
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.senha_var = tkinter.StringVar()
        self.senha_var.trace("w", self.validar_senha)

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,width=180,corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ Lada Esquerdo ============

        # Configuração do Grid (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   
        self.frame_left.grid_rowconfigure(5, weight=1)  
        self.frame_left.grid_rowconfigure(8, minsize=20)   
        self.frame_left.grid_rowconfigure(11, minsize=10) 

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left, text="Delp-Projetct", text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Start conexão serial",
                                                command=self.button_event_startSerial)

        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Stop conexão serial",
                                                command=self.button_event_stopSerial)

        self.button_2.grid(row=3, column=0, pady=10, padx=20)


        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)

        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ Lado Direito ============

        # Configuração Grid (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ Centro ============

        # Configuração Grid (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   height=250,
                                                   text=texto,
                                                   text_color=("black"),
                                                   corner_radius=6,  
                                                   fg_color=("white"),  
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)


        # ============ Lado Direito ============

        self.radio_var = tkinter.IntVar(value=0)

        self.combobox_1 = customtkinter.CTkComboBox(master=self.frame_right,
                                                    values=["Erro1", "Erro2", "Erro3"])

        self.combobox_1.grid(row=0, column=2, columnspan=1, pady=10, padx=20, sticky="we")


        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Password",
                                            state=tkinter.DISABLED,
                                            textvariable=self.senha_var)
        self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")
        

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Digite a senha",
                                                border_width=2,
                                                border_color=("red"), # <- custom border_width
                                                fg_color=None,  # <- no fg_colora
                                                command=self.button_event_desbloquear,
                                                state=tkinter.DISABLED)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Dark")
        self.combobox_1.set("Status de erros")
        
        

    # Função inicia o ros e manda os paramentos pro carrinho

    def button_event_startSerial(self):
        global porta_serial
        global status_serial, status_maquina, erro

        try:
            porta_serial = serial.Serial('COM7', 9600)  # Substitua 'COM7' pela porta serial correta

            #atualizar
            status_serial = "Ativo"
            status_maquina = "Funcionado"
            self.atualizar_info(status_serial, status_maquina, erro)

            self.entry.configure(state=tkinter.NORMAL,
                                 placeholder_text="Password")

            self.receber_dados()

        except Exception as e:
            tkinter.messagebox.showerror("Conexão Serial", f"Erro ao estabelecer a conexão Serial: {str(e)}")

    def button_event_stopSerial(self):
        global porta_serial

        if porta_serial is not None:
            porta_serial.close()
            porta_serial = None

            #Atualizar
            status_serial = "Desativo"
            status_maquina = "Parada"
            self.atualizar_info(status_serial, status_maquina, erro)

        else:
            tkinter.messagebox.showwarning("Conexão Serial", "Nenhuma conexão Serial ativa!")

    def enviar_dados(self, valor):
        global porta_serial
        print("Dado enviado")

        if porta_serial is not None:
            try:
                porta_serial.write(str(valor).encode())
            except Exception as e:
                tkinter.messagebox.showerror("Envio de Dados", f"Erro ao enviar dados: {str(e)}")
        else:
            tkinter.messagebox.showwarning("Envio de Dados", "Nenhuma conexão Serial ativa!")

    def receber_dados(self):
        global porta_serial
        global status_maquina, erro

        if porta_serial is not None and porta_serial.in_waiting > 0:
            dados = porta_serial.readline().decode().rstrip()
            print(dados)
            if(dados == "12"):
                status_maquina = "Parada"
                self.atualizar_info(status_serial, status_maquina, erro)

            elif(dados == "13"):
                status_maquina = "Funcionando"
                erro = "NAE"
                self.atualizar_info(status_serial, status_maquina, erro)
            
            elif (dados == "31"):
                erro = "Sensor_Ultra_Sonico"
                self.atualizar_info(status_serial, status_maquina, erro)
        self.after(100, self.receber_dados)

    def button_event_desbloquear(self):
        senha = self.senha_var.get()
        print("Senha digitada:", senha)
        self.enviar_dados(senha)
        self.entry.delete(0, tkinter.END)

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()
    
    def validar_senha(self, *args):
        senha = self.senha_var.get()
        if senha:
            self.button_5.configure(state=tkinter.NORMAL,
                                    text="Desbloquear",
                                    border_color=("green"))  # Habilita o botão
        else:
            self.button_5.configure(state=tkinter.DISABLED,
                                    text="Digite a senha",
                                    border_color=("red"))
            
    def atualizar_info(self, status_serial, status_maquina, erro):
        texto = f"Status da conexão serial: {status_serial}\n"
        texto += f"Status da máquina: {status_maquina}\n"
        texto += f"Informação do erro: {erro}"
        self.label_info_1.configure(text=texto)

    

if __name__ == "__main__":
    app = App()
    app.mainloop()
    