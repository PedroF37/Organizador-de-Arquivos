# -------------------------------------------------------------------------- #
# IMPORTAÇÕES


# tkinter
from tkinter import Tk, Frame, Label, Button, PhotoImage
from tkinter.messagebox import showinfo, showwarning
from tkinter.filedialog import askdirectory

from tkinter.ttk import Style, Combobox

# matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# pathlib
from pathlib import Path

# os
from os import chdir, getcwd

# sys
from sys import exit

# views
from views import list_directory, organize_files
from views import compress_files, compress_all_files
from views import delete_files, delete_all_files


# -------------------------------------------------------------------------- #
# CONSTANTES


# Cores
COLOR1 = '#464646'  # Fundo
COLOR2 = '#ffffff'  # Letra
COLOR3 = '#676767'  # Linha de separação

# Home do usuário
home = Path.home()


# -------------------------------------------------------------------------- #
# FUNÇÕES


def choose_folder():
    """Cuida da escolha da pasta alvo."""
    try:
        target_folder = askdirectory(initialdir=home)
    # Para não dar um erro feioso se fechar a janela principal
    except Exception as err:
        exit()
    else:
        '''
        dicionario tem como chave a extensão e como valor o número
        de arquivos com essa extensão. Em ext_list, uso do facto de que
        por padrão o dicionário retorna a chave, logo não precisa colocar
        filedict.keys(). number_list e legend_list são para o gráfico pie.
        ext_list é para os combobox. legend_list é algo como: .pdf : 35

        O "if target_folder:", trata do caso de apertar botão de cancelar.
        Quando isso acontece, dá erro de "TypeError" e mesmo com except não
        sei como tratar de forma que não apareca outra mensagem feiosa
        na tela. Logo, temos "if target_folder:" ...
        '''
        if target_folder:
            size, filedict = list_directory(target_folder)
            number_list = [number for number in filedict.values()]
            ext_list = [ext for ext in filedict]
            legend_list = [
                f'{ext} : {number}'
                for ext, number in filedict.items()
            ]

            # Aqui, é para o caso de não ter arquivos, não mostrar
            # a legenda e o título sem o gráfico (que fica feioso kk)
            if size > 0:
                pie_graph(size, number_list, legend_list)
            else:
                showinfo('', 'Pasta selecionada está vazia')
                return

            # 'insert('.*')', para dar opção de compactar/deletar
            # todos os arquivos
            ext_list.insert(0, '.*')

            delete_combobox['values'] = ext_list
            extension_combobox['values'] = ext_list

            organize_button['state'] = 'active'
            compact_button['state'] = 'active'
            delete_button['state'] = 'active'

            organize_button['command'] = lambda: organize(target_folder)
            compact_button['command'] = lambda: compress(target_folder)
            delete_button['command'] = lambda: choose_delete(target_folder)
        else:
            exit()


def organize(target_folder):
    """Cuida de chamar função que organiza arquivos."""
    organize_files(target_folder)
    showinfo('', 'Arquivos organizados com sucesso')
    reset_app()


def compress(target_folder):
    """Cuida de chamar função que compacta arquivos."""
    if not extension_combobox.get():
        showwarning('', 'Tem que selecionar uma extensão')
        return
    # TODOS os arquivos
    elif extension_combobox.get() == '.*':
        compress_all_files(target_folder)
    else:
        # Somente para a extensão escolhida
        compress_files(target_folder, extension_combobox.get())

    showinfo('', 'Arquivos comprimidos com sucesso')
    reset_app()


def choose_delete(target_folder):
    """Cuida de chamar função que deleta arquivos."""
    if not delete_combobox.get():
        showwarning('', 'Tem que selecionar uma extensão')
        return
    # Age sob TODOS os arquivos
    elif delete_combobox.get() == '.*':
        delete_all_files(target_folder)
    else:
        # Somente para a extensão escolhida
        delete_files(target_folder, delete_combobox.get())

    showinfo('', 'Arquivos deletados com sucesso')
    reset_app()


def pie_graph(size, number_list, legend_list):
    """
    Cuida de mostrar gráfico pizza
    com as extensões e número por cada
    extensão no diretório.
    """
    graph = plt.Figure(figsize=(5, 3), dpi=90)
    ax = graph.add_subplot(111)

    ax.pie(
        number_list,
        wedgeprops=dict(width=0.3),
        shadow=True, startangle=90
    )

    # Deu um trabalhão para descobrir
    # como fazer isto!! kkk
    ax.set_title(
        f'Tamanho Total: {size} MB',
        color='w', weight='bold',
        fontsize=10
    )

    ax.legend(
        legend_list, loc="lower center",
        bbox_to_anchor=(1.30, 0.50),
        title='Quantidade'
    )

    # Coloca o fundo do gráfico igual ao fundo do app
    graph.patch.set_facecolor(COLOR1)

    canvas = FigureCanvasTkAgg(graph, output_frame)
    canvas.get_tk_widget().place(x=-60, y=0)


def reset_app():
    """Cuida de resetar todo o app."""
    chdir(home)
    organize_button['state'] = 'disabled'
    compact_button['state'] = 'disabled'
    delete_button['state'] = 'disabled'
    delete_combobox['values'] = ''
    delete_combobox.set('')
    extension_combobox['values'] = ''
    extension_combobox.set('')


# -------------------------------------------------------------------------- #
# JANELA


window = Tk()
window.title('')
window.geometry('800x400')
window.resizable(width=False, height=False)
window.configure(background=COLOR1)

style = Style(window)
style.theme_use('clam')


# -------------------------------------------------------------------------- #
# FRAMES


title_frame = Frame(window, width=800, height=50, bg=COLOR1)
title_frame.grid(row=0, column=0, sticky='nw')

operation_frame = Frame(window, width=400, height=350, bg=COLOR1)
operation_frame.grid(row=1, column=0, sticky='nw')

output_frame = Frame(window, width=400, height=350, bg=COLOR1)
output_frame.place(x=400, y=50)


# -------------------------------------------------------------------------- #
# CONFIGURANDO TITLE_FRAME


logo = PhotoImage(file='icones/logo.png')
title_label = Label(
    title_frame, width=800, image=logo,
    text='   Organizador de Arquivos',
    compound='left', font=('Roboto 15 bold'),
    anchor='nw', bg=COLOR1, fg=COLOR2
)
title_label.place(x=10, y=10)

separator_label = Label(
    title_frame, width=800,
    text='', font=('Roboto 1'),
    bg=COLOR3
)
separator_label.place(x=0, y=48)


# -------------------------------------------------------------------------- #
# CONFIGURANDO OPERATION_FRAME


# Escolher pasta
folder_choose_label = Label(
    operation_frame, width=70,
    text='Selecione a pasta',
    font=('Roboto 10 bold'), anchor='nw',
    fg=COLOR2, bg=COLOR1
)
folder_choose_label.place(x=15, y=15)

folder_img = PhotoImage(file='icones/folder.png')
folder_button = Button(
    operation_frame, width=100, image=folder_img, text='PASTA',
    compound='left', font=('Roboto 8 bold'), anchor='nw',
    relief='ridge', overrelief='sunken', bd=0, borderwidth=0,
    bg=COLOR1, fg=COLOR2, activebackground=COLOR1,
    activeforeground=COLOR2, command=choose_folder
)
folder_button.place(x=10, y=40)


# Opção para organizar arquivos
organize_label = Label(
    operation_frame, width=70, text='Organizar Arquivos',
    font=('Roboto 10 bold'), anchor='nw',
    fg=COLOR2, bg=COLOR1
)
organize_label.place(x=160, y=15)

organize_img = PhotoImage(file='icones/organize.png')
organize_button = Button(
    operation_frame, width=100, image=organize_img, text='ORGANIZAR',
    compound='left', font=('Roboto 8 bold'), anchor='nw',
    relief='ridge', overrelief='sunken', bd=0, borderwidth=0,
    bg=COLOR1, fg=COLOR2, activebackground=COLOR1,
    activeforeground=COLOR2
)
organize_button['state'] = 'disabled'
organize_button.place(x=160, y=40)


# Opção para comprimirr arquivos
compact_label = Label(
    operation_frame, width=70, text='Comprimir Arquivos',
    font=('Roboto 10 bold'), anchor='nw',
    fg=COLOR2, bg=COLOR1
)
compact_label.place(x=10, y=80)

extension_combobox = Combobox(operation_frame, width=12)
extension_combobox['state'] = 'readonly'
extension_combobox.place(x=10, y=105)

compact_img = PhotoImage(file='icones/compact.png')
compact_button = Button(
    operation_frame, width=100, image=compact_img, text='COMPRIMIR',
    compound='left', font=('Roboto 8 bold'), anchor='nw',
    relief='ridge', overrelief='sunken', bd=0, borderwidth=0,
    bg=COLOR1, fg=COLOR2, activebackground=COLOR1,
    activeforeground=COLOR2
)
compact_button['state'] = 'disabled'
compact_button.place(x=160, y=105)


# Opção para deletar arquivos
delete_label = Label(
    operation_frame, width=70, text='Deletar Arquivos',
    font=('Roboto 10 bold'), anchor='nw',
    fg=COLOR2, bg=COLOR1
)
delete_label.place(x=10, y=135)

delete_combobox = Combobox(operation_frame, width=12)
delete_combobox['state'] = 'readonly'
delete_combobox.place(x=10, y=160)

delete_img = PhotoImage(file='icones/delete.png')
delete_button = Button(
    operation_frame, width=100, image=delete_img, text='DELETAR',
    compound='left', font=('Roboto 8 bold'), anchor='nw',
    relief='ridge', overrelief='sunken', bd=0, borderwidth=0,
    bg=COLOR1, fg=COLOR2, activebackground=COLOR1,
    activeforeground=COLOR2
)
delete_button['state'] = 'disabled'
delete_button.place(x=160, y=160)


# -------------------------------------------------------------------------- #
# LOOP


window.mainloop()


# -------------------------------------------------------------------------- #
