from tkinter import *

def escreverMensagem():
    texto2["text"] = "Olá Mundo!"

janela = Tk()
janela.title("Teste de Janela")
janela.geometry("150x100")

texto = Label(janela, text="Clique No Botão!!!!!")
texto.grid(column=0, row=0, padx=20, pady=5)

botao = Button(janela, text="Clique Aqui!!!!!", command=escreverMensagem)
botao.grid(column=0, row=1, padx=20, pady=5)

texto2 = Label(janela, text="")
texto2.grid(column=0, row=2, padx=20, pady=5)

janela.mainloop()
