import os.path

import PIL.ImageOps
import language as lng
import PIL.Image
import customtkinter as ctk
import pikepdf
import threading
import re
import json
from datetime import datetime
from customtkinter import filedialog as fd
from os import remove as delete
from os import startfile as openexplorer
from pathlib import Path
from pikepdf import *
from PIL import Image, ImageCms
from pygame import mixer
from time import sleep

data = json.load(
    open('CrimsonSimpleImageConverter\\data\\data.json', 'r', encoding='utf-8'))
mixer.init()
beep = mixer.Sound('CrimsonSimpleImageConverter\\assets\\beep.wav')
qstn = mixer.Sound('CrimsonSimpleImageConverter\\assets\\question.aiff')

"""
----------------------------------------------------------------------------------------------------------------------------------------------
Declarando a janela principal ----------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""

j_main = ctk.CTk()  # Cria a janela principal
j_main.iconbitmap('CrimsonSimpleImageConverter\\icon.ico')
j_main.geometry('1280x720')  # tamanho da janela em px
# determina se é redimensionável ou não
j_main.resizable(width=False, height=False)
j_main.title('Crimson Simple Image Converter')
ctk.set_appearance_mode(data['theme'])  # "light" ou "dark"

print(f'Idioma do Sistema: {lng.current_language}')
print(lng.opt_output4_txt[1])
"""
----------------------------------------------------------------------------------------------------------------------------------------------
Variaveis Globais ----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""

filenames = []
entry_filenames = []
entry_filelist = []
entry_filevar = []
buttons_list = []
added_images = {}
output_path = data['output_path']
forms = ['.jpg', '.png', '.gif', '.bmp', '.webp',
         '.ico', '.tiff', '.jp2', '.pdf', '.eps']
form = ''
replace_opt = ''
init_conv_opt = data['format_option']
init_rep_opt = data['replace_option']
init_rad = ctk.IntVar(value=data['output_mode'])
init_chk1 = ctk.IntVar(value=data['del_original'])
init_chk2 = ctk.IntVar(value=data['open_output'])
init_chk3 = ctk.IntVar(value=data['clean_input'])
init_chk4 = ctk.IntVar(value=data['finish_beep'])
init_chk5 = ctk.IntVar(value=data['finish_close'])


"""
----------------------------------------------------------------------------------------------------------------------------------------------
Funções --------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""


def save_config():
    global data
    match check_output1.get():
        case 0:
            data['del_original'] = 0
        case 1:
            data['del_original'] = 1
    match check_output2.get():
        case 0:
            data['open_output'] = 0
        case 1:
            data['open_output'] = 1
    match check_output3.get():
        case 0:
            data['clean_input'] = 0
        case 1:
            data['clean_input'] = 1
    match check_output4.get():
        case 0:
            data['finish_beep'] = 0
        case 1:
            data['finish_beep'] = 1
    match check_output5.get():
        case 0:
            data['finish_close'] = 0
        case 1:
            data['finish_close'] = 1

    with open('CrimsonSimpleImageConverter\\data\\data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print('CONFIGURAÇÕES SALVAS! ________________________')


def set_language(value=''):
    global data

    def close_window():
        """Fecha a janela de aviso."""
        res_bg.destroy()
        restart.destroy()
    if value == '[PT-BR] Português Brasileiro':
        data['language'] = 'pt-br'
    elif value == '[ENG] English':
        data['language'] = 'eng'
    elif value == '[ESP] Español':
        data['language'] = 'spa'
    else:
        data['language'] = 'eng'

    res_bg = ctk.CTkFrame(j_main, fg_color=None,
                          corner_radius=0, width=1280, height=720)
    res_bg.place(x=0, y=0)
    restart = ctk.CTkFrame(j_main, fg_color=colors['frame_c'], corner_radius=0, width=640, height=270, border_width=3,
                           border_color='crimson')
    res_lab = ctk.CTkLabel(restart, text=lng.res_lab_txt, width=600, height=28, text_color=colors['text_c'],
                           font=subtitlefont)
    res_lab.place(x=20, y=107)
    res_bt = ctk.CTkButton(restart, text='OK', text_color=colors['text_c'], font=buttonfont, fg_color=colors['button_c'],
                           hover_color='crimson', command=close_window)
    res_bt.place(x=250, y=169)
    restart.place(x=320, y=225)
    qstn.play()

    print(f'|||| IDIOMA ATUAL: {data["language"]}')


def play_beep():
    '''
    Excetuta o audio 'beep'.
    :return:
    '''
    beep.play()


def close_app():
    '''
    Fecha a Aplicaão.
    '''
    save_config()
    j_main.quit()


def show_image(image_path, filepath='', pdf=False):
    '''
    1: Abre a imagem especificada pelo caminho
    'image_path' também redimensionando para
    450x320px mantendo o aspect_ratio e a
    exibe em uma label 'lab_img_preview'.

    2: É verificado se o arquivo é um pdf ou não
    e será iniciado uma das duas funções para
    extrair os dados do arquivo e armazenados
    num variavel 'info'.
    Se for PDF: inicia 'extract_pdf_info()'.
    Se NÃO for PDF: inicia 'extract_image_info()'.

    3: A textbox 'img_info' tem seu conteúdo limpo.
    'info' convertido num dicionário ao fim das
    funções e cada item é inserido na textbox
    'img_info'.
    :param image_path: Caminho da imagem que será usada no preview.
    :param filepath: Caminho para o arquivo original.
    :param pdf: Se o arquivo é PDF ou não.
    :return:
    '''
    print(f'FILEPATH: {filepath}')
    print(f'IMAGE PATH: {image_path}')
    print(pdf)
    try:
        view_size = (450, 320)
        # Abrir a imagem usando Pillow
        img = Image.open(image_path)
        img.thumbnail(view_size, resample=Image.Resampling.LANCZOS)

        if pdf == False:
            info = extract_image_info(image_path)
            img_info.configure(state=ctk.NORMAL)
            img_info.delete('0.0', 'end')
            for key, value in info.items():
                img_info.insert('end', text=f'{key}: {value}\n\n')
            img_info.configure(state=ctk.DISABLED)
        elif pdf == True:
            info = extract_pdf_info(pdf_path=filepath)
            img_info.configure(state=ctk.NORMAL)
            img_info.delete('0.0', 'end')
            for key, value in info.items():
                img_info.insert('end', text=f'{key}: {value}\n\n')
            img_info.configure(state=ctk.DISABLED)
        print('informações Registradas')

        # Criar uma imagem para o Tkinter
        img_tk = ctk.CTkImage(light_image=img, size=img.size)

        # Atualizar a label com a nova imagem
        lab_img_preview.configure(image=img_tk)
        lab_img_preview.image = img_tk  # Manter uma referência para evitar coleta de lixo
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")


def format_pdf_date(pdf_date):
    """
    Formata a data no formato D:YYYYMMDDHHmmSS para DD\\MM\\YYYY HH:mm:SS.
    """
    if pdf_date.startswith('D:'):
        pdf_date = pdf_date[2:]
    try:
        # Extrair a parte da data, ignorando fuso horário se existir
        date_obj = datetime.strptime(pdf_date[:14], '%Y%m%d%H%M%S')
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return lng.unknow_date


def extract_pdf_info(pdf_path):
    '''
    Carrega o arquivo PDF, extrai as informações do metadata \n
    e retorna um Dicionário com elas.\n
    As informações consistem em :\n\n
    Nome do Arquivo.\n
    Tipo de Documento.\n
    Criador.\n
    Produtor.\n
    Data de Criação.\n
    Data de Modificação.\n
    Número de Páginas.\n
    Tamanho das Páginas.\n
    Tamanho do Arquivo.\n
    Versão do PDF.\n
    :param pdf_path: diretório do arquivo pdf que serão extraídas as informações.
    :return:
    '''
    # Abrir o PDF usando pikepdf
    print(pdf_path)
    try:
        with pikepdf.open(pdf_path) as pdf:
            # Obter informações gerais do PDF
            pdf_info = pdf.docinfo

            # Função para extrair metadados de forma segura
            def get_metadata(key):
                return pdf_info.get(key, lng.ex_pdf_unknow)

            # Nome do arquivo e extensão
            file_name = os.path.basename(pdf_path)
            file_extension = os.path.splitext(pdf_path)[1].upper()

            # Criador e Produtor
            creator = get_metadata('\\Creator')
            producer = get_metadata('\\Producer')

            # Data de Criação e Modificação
            creation_date_raw = get_metadata('\\CreationDate')
            print(creation_date_raw)
            creation_date = format_pdf_date(str(f'{creation_date_raw}'))

            mod_date_raw = get_metadata('\\ModDate')
            mod_date = format_pdf_date(str(f'{mod_date_raw}'))

            # Número de páginas
            num_pages = len(pdf.pages)

            # Tamanho das páginas (Largura x Altura em pontos)
            page_sizes = [(page.MediaBox[2], page.MediaBox[3])
                          for page in pdf.pages]
            page_size_w = round(page_sizes[0][0], 2)
            page_size_h = round(page_sizes[0][1], 2)

            # Tamanho do arquivo
            file_size = os.path.getsize(pdf_path)

            # Verificar se o PDF é otimizado
            # is_optimized = pdf.is_optimized

            # Versão do PDF
            pdf_version = pdf.pdf_version

            # Exibir as informações
            return {
                lng.ex_pdf_txt1: f'{file_name}',
                lng.ex_pdf_txt2: f'{file_extension}'.replace('.', ''),
                lng.ex_pdf_txt3: f'{creator}',
                lng.ex_pdf_txt4: f'{producer}',
                lng.ex_pdf_txt5: f'{creation_date}',
                lng.ex_pdf_txt6: f'{mod_date}',
                lng.ex_pdf_txt7: f'{num_pages}',
                lng.ex_pdf_txt8: str(f'({page_size_w}pts x {page_size_h}pts)'),
                lng.ex_pdf_txt9: f'{file_size} bytes',
                lng.ex_pdf_txt0: f'{pdf_version}'}
    except pikepdf.PdfError as e:
        print(f"Erro ao abrir o PDF: {e}")


def extract_image_info(image_path):
    '''
    Carrega o arquivo de Imagem, extrai as informações \n
    e retorna um Dicionário com elas.\n
    As informações consistem em :\n\n
    Nome do Arquivo.\n
    Tipo de Documento.\n
    Tamanho da Imagem.\n
    Data de Criação.\n
    Data de Modificação.\n
    Tamanho do Arquivo.\n
    :param pdf_path: diretório do arquivo pdf que serão extraídas as informações.
    :return:
    '''
    # Abrir a imagem
    image = Image.open(image_path)

    # Nome do arquivo
    filename = os.path.basename(image_path)

    # Tipo de imagem (formato)
    image_format = image.format

    # Tamanho da imagem (largura, altura)
    image_size = image.size

    # Tamanho em Disco da Imagem (bytes)
    file_size = os.path.getsize(image_path)
    # Data de criação do arquivo
    file_info = os.stat(image_path)
    creation_time = datetime.fromtimestamp(file_info.st_ctime)
    print(f'Creation time: {creation_time}')

    # Data de modificação do arquivo
    modification_time = datetime.fromtimestamp(os.path.getmtime(image_path))

    # Retornar todas as informações como um dicionário
    return {
        lng.ex_img_txt1: filename,
        lng.ex_img_txt2: image_format,
        lng.ex_img_txt3: str(f'({image_size[0]}px, {image_size[1]}px)'),
        lng.ex_img_txt4: f'{file_size} bytes',
        lng.ex_img_txt5: str(f'{creation_time.date()} {str(creation_time.hour).zfill(2)}:{str(creation_time.minute).zfill(2)}:{str(creation_time.second).zfill(2)}'),
        lng.ex_img_txt6: str(f'{modification_time.date()} {str(modification_time.hour).zfill(2)}:{
                             str(modification_time.minute).zfill(2)}:{str(modification_time.second).zfill(2)}')
    }


def on_button_click(image_path, n_file_path, pdf=False):
    '''
    Quando botão é pressionado, ele irá
    verificar se 'pdf' é True ou False e
    iniciar a função 'show_image()' com
    os parâmetros correspondentes.
    :param image_path: Caminho da imagem que será usada como preview.
    :param n_file_path: Caminho do arquivo principal na lista 'filenames[]'
    :param pdf: Se o arquivo em questão é um PDF
    :return:
    '''
    print(f'Caminho para a Imagem: {n_file_path}')
    '''
    Função chamada quando um botão é clicado.
    '''
    if pdf == False:
        show_image(image_path=image_path, filepath=n_file_path, pdf=False)
    else:
        show_image(image_path=image_path, filepath=n_file_path, pdf=True)


def load_files():
    '''
    1: Carrega os caminhos dos arquivos e armazena
    numa lista 'temp_filenames[]', formata os
    caminhos para remover os '[' e ']', verifica
    se existem caminhos duplicados na lista e
    remove as duplicatas e por fim copia os dados
    para a lista 'filenames[]'.

    2: inicia a função 'bulk_load_files()' para
    criar e organizar os botões.

    3: Limpa a lista 'temp_filenames[]'.
    '''
    global filenames
    global entry_filenames
    global entry_filevar
    global entry_filelist
    global fr_entry
    refresh_info_text(msg='Carregando Imagens...')
    try:
        temp_filenames = fd.askopenfilenames(filetypes=[("All Supported files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico;*.webp;*.tiff;*.tif;*.jp2;*.j2k;*.jfif;*.pdf"),
                                                        ('PNG (Portable Network Graphics)', '*.png'),
                                                        ('JPEG (Joint Photographic Experts Group)',
                                                         '*.jpg;*.jpeg'),
                                                        ('GIF (Graphics Interchange Format)', '*.gif'),
                                                        ('BMP (Bitmap)', '*.bmp'),
                                                        ('ICO (Icon)', '*.ico'),
                                                        ('WEBP (Web Picture format)',
                                                         '*.webp'),
                                                        ('JFIF (JPEG File Interchange Format)', '*.jfif'),
                                                        ('TIFF (Tagged Image File Format)',
                                                         '*.tiff;*.tif'),
                                                        ('JPEG2K (JPEG 2000)',
                                                         '*.jp2;*.j2k'),
                                                        ('PDF (Portable Document Format)', '*.pdf')])
        print(f'Temp List: {temp_filenames}')
        # Adicionar arquivos à lista filenames
        for c in temp_filenames:
            dr = str(c)
            # Correção na substituição
            dr = dr.replace('[', '').replace(']', '')
            if dr not in filenames:  # Evitar duplicatas
                filenames.append(dr)
        print(f'filenames List: {filenames}')
        bulk_load_files()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        temp_filenames = tuple()

        print(f'Temp List: {temp_filenames}')
        print(fr_entry.winfo_children())
        refresh_info_text(msg=f'{len(filenames)} {lng.lab_info_txt}')


def bulk_load_files():
    '''
    Limpa o dicionário 'added_images{}'.
    Processo em 3 passos:

    1: Lê todos os itens da lista 'filenames[]'
    e abre as imagens, e redimesiona elas para
    um tamanho de 100x100px, mantendo o aspect_ratio.
    E por fim armazena cada uma em 'added_images{}'.


    2: Será gerado botões com base na quantidade de
    imagens armazenadas em 'added_images{}', cada um
    carregando a imagem correspondente no param 'image='
    ou um ícone padrão caso o arquivo seja um PDF,
    cada botão vai executar a função 'on_button_click()'
    com os parâmetros definidos conforme o tipo de arquivo
    e todos dentro do frame 'fr_entry'.

    3: Cada botão será posicionado numa grid dentro do frame
    'fr_entry' que será definida com 6 colunas e 100 linhas.
    :return:
    '''
    # entry_filenames = filenames.copy()
    # print(f'entry_filenames List: {entry_filenames}')
    # safe_destroy_widgets()

    # Dicionário para armazenar botões únicos
    added_images = {}

    row, col = 0, 0
    for i in range(len(filenames)):
        try:
            if filenames[i].endswith('.pdf'):
                # p_image = get_pdf_preview(filenames[i])
                # print(f'ImagePDF {p_image}')
                icon_size = (100, 100)
                view_size = (450, 320)
                filename = os.path.basename(filenames[i])
                input_form = '.png'  # Path(filenames[i]).suffix
                inputname = Path(filename).stem + input_form
                img_name = f'{inputname}'

                orimg1 = Image.open(
                    'CrimsonSimpleImageConverter\\assets\\pdf_icon.png')
                orimg1.filename = img_name
                orimg1.thumbnail(icon_size)
                # orimg2 = Image.open('CrimsonSimpleImageConverter\\assets\\pdf_icon.png')
                # orimg2.filename = img_name
                # orimg2.thumbnail(view_size)
            else:
                icon_size = (100, 100)
                view_size = (450, 320)
                input_form = Path(filenames[i]).suffix
                inputname = Path(Image.open(
                    filenames[i]).filename).stem + input_form
                img_name = f'{inputname}'

                orimg1 = Image.open(filenames[i])
                orimg1.thumbnail(icon_size)
                # orimg2 = Image.open(filenames[i])
                # orimg2.thumbnail(view_size)
            img = ctk.CTkImage(light_image=orimg1, size=orimg1.size)
            # img2 = ctk.CTkImage(light_image=orimg2, size=orimg2.size)

            # Adicionar imagem ao dicionário de imagens únicas, substituindo a anterior se já existir
            added_images[filenames[i]] = img
            # entry_filevar.append(f'img_{img_name}')
        except Exception as e:
            print(f"Error processing file {filenames[i]}: {e}")

    # print(f'Button List: {entry_filevar}')

    # Adicionar botões ao frame com as imagens mais recentes
    for j, filepath in enumerate(added_images):
        print(filepath)
        if filepath.endswith('.pdf'):
            _i_filepath = filepath
            _filepath = 'CrimsonSimpleImageConverter\\assets\\pdf_icon.png'
            print('=' * 15, f'{_filepath}')
            button = ctk.CTkButton(fr_entry, image=added_images[filepath], text=None, width=102, height=102,
                                   border_width=None, corner_radius=0, fg_color='crimson', hover_color='indianred1',
                                   textvariable=_filepath,
                                   command=lambda f=_filepath: on_button_click(image_path=f, pdf=True,
                                                                               n_file_path=_i_filepath))
            button.grid(row=row, column=col, padx=5, pady=5)
        else:
            button = ctk.CTkButton(fr_entry, image=added_images[filepath], text=None, width=102, height=102,
                                   border_width=None, corner_radius=0, fg_color='crimson', hover_color='indianred1',
                                   textvariable=filepath,
                                   command=lambda f=filepath: on_button_click(image_path=f, pdf=False,
                                                                              n_file_path=filepath))
            button.grid(row=row, column=col, padx=5, pady=5)

        col += 1
        if col >= 6:
            col = 0
            row += 1
        if row >= 167:
            break  # Para de adicionar se atingir o limite de 100 linhas
    print(f'Converted Button List: {entry_filevar}')


def clear_files():
    '''
    Limpa os diretórios armazenados na lista 'filenames'.
    Deleta todos os botões no frame 'fr_entry'.
    Recarrega os botões no frame 'fr_entry'
    ao chamar a função 'bulk_load_files()'.
    Remove as informações na textbox 'img_info'.
    E por fim, remove a imagem da label 'lab_img_preview'.
    :return:
    '''
    print(f'OLD FILENAMES {filenames}')
    filenames.clear()
    for widget in fr_entry.winfo_children():
        widget.destroy()
    bulk_load_files()
    img_info.configure(state=ctk.NORMAL)
    img_info.delete('0.0', 'end')
    img_info.configure(state=ctk.DISABLED)
    lab_img_preview.configure(image=None)
    lab_img_preview.image = None
    refresh_info_text(f'{len(filenames)} {lng.lab_info_txt}')
    print(f'NEW FILENAMES {filenames}')


def load_output_path():
    '''
    Carrega o diretório da
    pasta de saída e substitui
    o valor de output_path.
    :return:
    '''
    global output_path
    output_path = fd.askdirectory().replace('/', '\\')+'\\'
    entry_text = ctk.StringVar(value=output_path)
    entry_output.configure(state=ctk.NORMAL, textvariable=entry_text)
    data['output_path'] = output_path
    entry_output.configure(state=ctk.DISABLED)
    print(f'{output_path}')


def set_alreadyexistent_file(value=''):
    '''
    Muda a variavel form para a\n
    opção correspondente no \n
    opt_output2.
    :param value: Opção selecionada no opt_output2.
    '''
    global replace_opt

    if value == lng.opt_output2_txt[0]:  # Perguntar
        replace_opt = value
        data['replace_option'] = 0
    elif value == lng.opt_output2_txt[1]:  # Substituir
        replace_opt = value
        data['replace_option'] = 1
    elif value == lng.opt_output2_txt[2]:  # Ignorar
        replace_opt = value
        data['replace_option'] = 2
    elif value == lng.opt_output2_txt[3]:  # Renomear
        replace_opt = value
        data['replace_option'] = 3
    else:
        replace_opt = lng.opt_output2_txt[0]  # Perguntar
        data['replace_option'] = 0
    print(f'Replace Options: {replace_opt}')


def set_output_format(value=''):
    '''
    Muda a variavel form para a\n
    opção correspondente no \n
    opt_output1.
    :param value: Opção selecionada no opt_output1.
    '''
    global form

    if value == 'JPG - .jpg, .jpeg, .jfif':
        form = forms[0]  # '.jpg'
        data['format_option'] = 0
        print('Mudou para JPG')
    elif value == 'PNG - .png':
        form = forms[1]  # '.png'
        data['format_option'] = 1
        print('Mudou para PNG')
    elif value == 'GIF - .gif':
        form = forms[2]  # '.gif'
        data['format_option'] = 2
        print('Mudou para GIF')
    elif value == 'BMP - .bmp':
        form = forms[3]  # '.bmp'
        data['format_option'] = 3
        print('Mudou para BMP')
    elif value == 'WEBP - .webp':
        form = forms[4]  # '.webp'
        data['format_option'] = 4
        print('Mudou para WEBP')
    elif value == 'ICO - .ico':
        form = forms[5]  # '.ico'
        data['format_option'] = 5
        print('Mudou para ICO')
    elif value == 'TIFF - .tiff':
        form = forms[6]  # '.tiff'
        data['format_option'] = 6
        print('Mudou para TIFF')
    elif value == 'JPEG2000 - .pj2':
        form = forms[7]  # '.jp2'
        data['format_option'] = 7
        print('Mudou para JPEG2000')
    elif value == 'PDF - .pdf':
        form = forms[8]  # '.pdf'
        data['format_option'] = 8
        print('Mudou para PDF')
    elif value == 'EPS - .eps':
        form = forms[9]  # '.eps'
        data['format_option'] = 9
        print('Mudou para EPS')
    else:
        form = forms[0]  # '.jpg'
        data['format_option'] = 0
    print(filenames)


def contains_prohibited_chars(filename):
    '''
    Checa se há um caractere "inválido"
    na string 'filename' e retorna um
    valor 'True' ou 'False'.

    Caracteres Proibidos no Windows:
        [\\\:*?"<>|]
    Caracteres Proibidos no Linux:
        [\\\]
    :param filename:
    :return:
    '''
    # Definindo os caracteres proibidos em diferentes sistemas operacionais
    prohibited_chars = r'[\\\:*?"<>|]'  # Proibidos no Windows
    prohibited_unix_mac = r'[\\\]'      # Proibidos no Unix\\Linux e macOS

    # Verificando se há caracteres proibidos na string
    if re.search(prohibited_chars, filename) or re.search(prohibited_unix_mac, filename):
        return True
    return False


def ask_replace_file_on_save(image, output, orig_name):
    '''
    Salva uma imagem, perguntando ao usuário o que fazer se o arquivo de destino já existir.\n
    Caso não exista, apenas salva normalmente.
    :param image: Imagem final que será salva.
    :param output: diretório final da imagem.
    :param orig_name: nome do arquivo original.
    :return:
    '''
    print('='*300)

    def on_replace():

        nonlocal user_choice
        user_choice = 'replace'
        procces_choices()

    def on_rename():
        nonlocal user_choice
        user_choice = 'rename'
        procces_choices()

    def on_ignore():
        nonlocal user_choice
        user_choice = 'ignore'
        procces_choices()

    def set_new_output(new_name=''):
        print('=' * 30)
        print(f'New Name: {new_name}')
        old_name = os.path.basename(output)
        print(f'Old Name: {old_name}')
        new_dir = output.replace(old_name, '')
        print(f'New Dir: {new_dir}')
        new_output = f'{new_dir}{new_name}{form}'
        print(f'New Output: {new_output}')
        image.save(new_output)
        add_to_log(f"{lng.ltxt_Converted} [ {orig_name} ] {
                   lng.ltxt_To} [ {new_name}{form} ].")
        print('=' * 30)

    def ask_user_action():
        def get_input(input=''):
            if input == 'replace':
                on_replace()
                dlg_bg.destroy()
                dialog.destroy()
            elif input == 'ignore':
                on_ignore()
                dlg_bg.destroy()
                dialog.destroy()
            elif input == 'rename':
                on_rename()
                dlg_bg.destroy()
                dialog.destroy()

        dlg_bg = ctk.CTkFrame(j_main, fg_color=None,
                              corner_radius=0, width=1280, height=720)
        dlg_bg.place(x=0, y=0)
        dialog = ctk.CTkFrame(j_main, fg_color=colors['frame_c'], corner_radius=0,
                              width=640, height=270, border_width=3, border_color='crimson')
        dlg_lab = ctk.CTkLabel(dialog, text=lng.dlg_lab_txt, width=600,
                               height=28, text_color=colors['text_c'], font=subtitlefont)
        dlg_lab.place(x=20, y=10)
        dlg_bt1 = ctk.CTkButton(dialog, text=lng.dlg_bt1_txt, text_color=colors['text_c'], width=600, font=buttonfont, fg_color=colors['button_c'], hover_color='crimson',
                                command=lambda f='replace': get_input(f))
        dlg_bt1.place(x=20, y=40)
        dlg_bt2 = ctk.CTkButton(dialog, text=lng.dlg_bt2_txt, text_color=colors['text_c'], width=600, font=buttonfont, fg_color=colors['button_c'], hover_color='crimson',
                                command=lambda f='rename': get_input(f))
        dlg_bt2.place(x=20, y=78)
        dlg_bt3 = ctk.CTkButton(dialog, text=lng.dlg_bt3_txt, text_color=colors['text_c'], width=600, font=buttonfont, fg_color=colors['button_c'], hover_color='crimson',
                                command=lambda f='ignore': get_input(f))
        dlg_bt3.place(x=20, y=116)
        dlg_info = ctk.CTkTextbox(
            dialog, text_color=colors['text_c'], width=600, height=103, font=buttonfont, fg_color=colors['buttondisable_c'])
        dlg_info.insert('0.0', lng.dlg_info_txt)
        dlg_info.place(x=20, y=154)
        dlg_info.configure(state=ctk.DISABLED)
        dialog.place(x=320, y=225)
        qstn.play()

    def rename_action():
        def print_name():
            n_name = ren_entry.get()
            if n_name == '':
                print('Escreva um nome válido!')
                ren_warning.place(x=20, y=68)
                pass
            else:
                if contains_prohibited_chars(n_name):
                    print('Escreva um nome válido!')
                    ren_warning.place(x=20, y=68)
                    pass
                else:
                    set_new_output(n_name)
                    ren_bg.destroy()
                    rename.destroy()
        nonlocal n_name
        ren_bg = ctk.CTkFrame(j_main, fg_color=None,
                              corner_radius=0, width=1280, height=720)
        ren_bg.place(x=0, y=0)
        rename = ctk.CTkFrame(j_main, fg_color=colors['frame_c'], corner_radius=0,
                              width=640, height=270, border_width=3, border_color='crimson')
        ren_lab = ctk.CTkLabel(rename, text=lng.ren_lab_txt, width=600,
                               height=28, text_color=colors['text_c'], font=titlefont)
        ren_lab.place(x=20, y=20)
        ren_warning = ctk.CTkLabel(rename, text=lng.ren_warning_txt,
                                   width=600, height=28, text_color='crimson', font=buttonfont)
        ren_warning.place(x=20, y=800)
        ren_entry = ctk.CTkEntry(rename, font=buttonfont, width=300,
                                 placeholder_text=lng.ren_entry_txt, border_color='crimson')
        n_name = ren_entry.get()
        print(f'Name New: {n_name}')
        ren_entry.place(x=170, y=121)
        ren_bt = ctk.CTkButton(rename, text='OK', text_color=colors['text_c'], font=buttonfont, fg_color=colors['button_c'], hover_color='crimson',
                               command=print_name)
        ren_bt.place(x=250, y=169)
        rename.place(x=320, y=225)
        qstn.play()

    def replace_action():
        current_name = os.path.basename(output)
        image.save(output)
        add_to_log(f"{lng.ltxt_Converted} [ {orig_name} ] {
                   lng.ltxt_To} [ {current_name} ].")

    def procces_choices():
        if user_choice == 'replace':
            replace_action()
            print(f'Substituir e Salvar como: {output}')
        elif user_choice == 'rename':
            rename_action()
            print(f'Renomear e Salvar como: {output}')
        elif user_choice == 'ignore':
            add_to_log(f"{lng.ltxt_Ignored} [ {orig_name} ] {
                       lng.ltxt_FromConversionList}.")
            print(f'Ignorar Arquivo')

    if os.path.exists(output):
        print(replace_opt)
        match lng.current_language:
            case 'pt-br':
                print('PORTUGUES')
                match replace_opt:
                    case 'Perguntar':
                        n_name = ''
                        user_choice = ''
                        ask_user_action()
                    case 'Substituir':
                        replace_action()
                    case 'Renomear':
                        rename_action()
                    case 'Ignorar':
                        add_to_log(f"{lng.ltxt_Ignored} [ {orig_name} ] {
                                   lng.ltxt_FromConversionList}.")
                        print(f'Ignorar Arquivo')
            case 'eng':
                print('INGLES')
                match replace_opt:
                    case 'Ask':
                        n_name = ''
                        user_choice = ''
                        ask_user_action()
                    case 'Replace':
                        replace_action()
                    case 'Rename':
                        rename_action()
                    case 'Ignore':
                        add_to_log(f"{lng.ltxt_Ignored} [ {orig_name} ] {
                                   lng.ltxt_FromConversionList}.")
                        print(f'Ignorar Arquivo')
            case 'spa':
                print('ESPANHOL')
                match replace_opt:
                    case 'Preguntar':
                        n_name = ''
                        user_choice = ''
                        ask_user_action()
                    case 'Reemplazar':
                        replace_action()
                    case 'Renombrar':
                        rename_action()
                    case 'Ignorar':
                        add_to_log(f"{lng.ltxt_Ignored} [ {orig_name} ] {
                                   lng.ltxt_FromConversionList}.")
                        print(f'Ignorar Arquivo')
        match replace_opt:
            case 'Perguntar', 'Ask', 'Preguntar':
                n_name = ''
                user_choice = ''
                ask_user_action()
            case 'Substituir', 'Replace', 'Reemplazar':
                replace_action()
            case 'Renomear', 'Rename', 'Renombrar':
                rename_action()
            case 'Ignorar', 'Ignore':
                add_to_log(f"{lng.ltxt_Ignored} [ {orig_name} ] {
                           lng.ltxt_FromConversionList}.")
                print(f'Ignorar Arquivo')
    else:
        current_name = os.path.basename(output)
        image.save(output)
        add_to_log(f"{lng.ltxt_Converted} [ {orig_name} ] {
                   lng.ltxt_To} [ {current_name} ].")


def check_beep():
    '''
    Se a checkbox 'check_output4'
    estiver selecionada, será
    iniciada a função 'play_beep()'.
    :return:
    '''
    valor = check_output4.get()
    if valor == 1:
        play_beep()
    else:
        pass


def check_delete_original(file="", filename="", newfilename=""):
    '''
    Se a checkbox 'check_output1'
    estiver selecionada, será
    comparado o 'filename' com
    o 'newfilename'.

    Se foremm iguais:
        Não será feito nada,
        pois o arquivo original
        foi sobrescrito.
    Se forem diferentes:
        o arquivo original será
        excluído usando a função
        'delete()' usando caminho
        armazenado em 'file'.
    :param file: Diretório do arquivo original
    :param filename: Nome do arquivo original.
    :param newfilename: Nome do novo arquivo salvo.
    :return:
    '''
    global filenames
    valor = check_output1.get()
    if valor == 1:
        if filename == newfilename:
            pass
        else:
            delete(file)
        filenames = []
        print(f'Excluído {filename}')
    else:
        pass


def check_open_output_folder(folder_path=''):
    '''
    Se a checkbox 'check_output2'
    estiver selecionada, será
    iniciada a função 'openexplorer()'
    usando 'folder_path' como
    parâmetro.
    :param folder_path:
    :return:
    '''
    valor = check_output2.get()
    if valor == 1:
        print('Abrindo Pasta de Saída...')
        openexplorer(folder_path)
    else:
        pass


def check_inputlist_clear():
    '''
    Se a checkbox 'check_output3'
    estiver selecionada, será
    iniciada a função 'clear_files()'
    :return:
    '''
    global filenames
    valor = check_output3.get()
    if valor == 1:
        print('Limpando Lista de Entrada...')
        clear_files()
        print(f'Lista de Entrada: {filenames}')
    else:
        pass


def check_close_after():
    '''
     Se a checkbox 'check_output5'
    estiver selecionada, será
    iniciada a função 'close_app()'.
    :return:
    '''
    valor = check_output5.get()
    if valor == 1:
        print('Fechando Aplicativo...')
        close_app()
    else:
        pass


def start_load_files():
    '''
    Inicia a função 'load_files()'
    em um thread separado.
    :return:
    '''
    threading.Thread(target=load_files).start()


def start_conversion():
    '''
    Inicia a função 'convert()'
    em um thread separado SE
    a lista 'filenames' não estiver
    vazia.
    Também é iniciado foco na tab 'Registro'.
    :return:
    '''
    if len(filenames) > 0:
        threading.Thread(target=convert).start()
        tab_main.set(lng.t_log)


def convert():
    '''
        Lê todos os elementos da lista filenames\n
        lê o elemento correspondente no loop e\n
        abre o arquivo com o Image.open(), em\n
        seguida armazena o caminho na var outputname\n
        e fatia a string restando apenas o nome do\n
        e adiciona a extensão form que está como string.\n
        Após isso o arquivo é salvo no diretório\n
        escolhido previamente ou no mesmo de origem.\n\n

        Após a Conversão são executadas as funções
        pós-conversõa:
            check_inputlist_clear()
            check_delete_original()
            check_beep()
            check_open_output_folder()
            check_close_after()
        form: Extensão de saída = .jpg.
    '''
    global form
    global output_path
    var = radiovar.get()
    print(f'filenames[0]: {filenames[0]}')
    add_to_log(lng.ltxt_StartingProccess)
    if filenames[0].endswith(".pdf"):
        auto_output = f'{os.path.dirname(filenames[0])}{"\\"}'
    else:
        auto_name = Path(Image.open(
            filenames[0]).filename).stem + Path(filenames[0]).suffix
        print(f'InputDir = {filenames[0]}')
        print(f'AutoName = {auto_name}')
        auto_output = filenames[0].replace(auto_name, '')
    print(f'Output format: {form}')
    for i in filenames:
        print(f'Manual Output: {output_path}')
        print(f'Auto Output: {auto_output}')
        if var == 1:  # AUTO
            if i.endswith('.pdf'):
                inputname = f'{os.path.basename(i)}'
                input_form = Path(i).suffix
                outputname = inputname.replace(input_form, form)
                print(f'InputName: {inputname}, OutputName: {outputname}')
                convert_from_pdf_file(i, inputname, outputname, auto_output)
            else:
                outputname = Path(Image.open(i).filename).stem + form
                input_form = Path(i).suffix
                inputname = Path(Image.open(i).filename).stem + input_form
                print(f'InputName: {inputname}, OutputName: {outputname}')
                if form == '.jpg':
                    convert_to_jpg_file(i, inputname, outputname, auto_output)
                    # add_to_log(f"Convertido [ {inputname} ] para [ {outputname} ].")
                    print(f"Convertido {inputname} para {outputname}")
                else:
                    convert_other_file(i, inputname, outputname, auto_output)
                    # add_to_log(f"Convertido [ {inputname} ] para [ {outputname} ].")
                    print(f"Convertido {inputname} para {outputname}")

        elif var == 0:  # MANUAL
            if i.endswith('.pdf'):
                inputname = f'{os.path.basename(i)}'
                input_form = Path(i).suffix
                outputname = inputname.replace(input_form, form)
                print(f'InputName: {inputname}, OutputName: {outputname}')
                convert_from_pdf_file(i, inputname, outputname, output_path)
            else:
                outputname = Path(Image.open(i).filename).stem + form
                input_form = Path(i).suffix
                inputname = Path(Image.open(i).filename).stem + input_form
                print(f'InputName: {inputname}, OutputName: {outputname}')
                if form == '.jpg':
                    convert_to_jpg_file(i, inputname, outputname, output_path)
                    # add_to_log(f"Convertido [ {inputname} ] para [ {outputname} ].")
                    print(f"Convertido {inputname} para {outputname}")
                else:
                    convert_other_file(i, inputname, outputname, output_path)
                    # add_to_log(f"Convertido [ {inputname} ] para [ {outputname} ].")
                    print(f"Convertido {inputname} para {outputname}")
        check_delete_original(i, inputname, outputname)
    add_to_log(lng.ltxt_ProccessFinished)
    check_inputlist_clear()
    if var == 1:
        check_beep()
        check_open_output_folder(auto_output)
        sleep(.5)
        check_close_after()
    elif var == 0:
        check_beep()
        check_open_output_folder(output_path)
        sleep(.5)
        check_close_after()


def color_mode_convert(image_file=PIL.Image.Image, input_mode='', output_mode='', auto=False, multiple=False, is_pdf=False):
    '''
    Carrega uma imagem do pillow 'image_file'
    e converte o mode de cores.
    a forma como feita será com base n 'auto'
    está ativo ou não (True|False) irá comparar
    o 'input_mode'.
    auto=True:
        Converte para RGB, caso
        o modo da imagem original seja CMYK e
        seja do tipo JPEG, ele será mantido CMYK.
    auto=False:
        Converte o modo de cor para o 'output_mode'.
    Converte
    :param image_file: Imagem que será convertida.
    :param input_mode: Modo de cor original.
    :param output_mode: Modo de cor final.
    :param auto: Modo de conversão, Automático ou não.
    :param multiple: Se serão múltiplas imagens.
    :return:
    '''
    def invert_cmyk(image_file):
        # Verifique se a imagem está em CMYK
        if image_file.mode != 'CMYK':
            raise ValueError(
                "A imagem deve estar no modo CMYK para esta operação.")

        # Carregar os canais CMYK
        c, m, y, k = image_file.split()

        # Inverter os canais
        c = Image.eval(c, lambda x: 255 - x)
        m = Image.eval(m, lambda x: 255 - x)
        y = Image.eval(y, lambda x: 255 - x)
        k = Image.eval(k, lambda x: 255 - x)

        # Juntar os canais invertidos de volta em uma imagem CMYK
        inverted_image = Image.merge('CMYK', (c, m, y, k))

        return inverted_image

    print('='*100)
    print(f'Imagem de Entrada: {image_file} | Modo de Entrada: {input_mode}')
    if is_pdf == True and input_mode == 'CMYK':
        _image_file = invert_cmyk(image_file)
        new_image_file = _image_file
    else:
        new_image_file = image_file.convert("RGB")

    print(f'Convertido de {input_mode} para RGB')
    print(f'Novo modo de Imagem : {new_image_file}')
    return new_image_file


def convert_from_pdf_file(file='', prev_name='', new_name='', output_path=''):
    '''
    Carrega o arquivo PDF do caminho 'file',
    Lê todas as páginas no arquivo e também as
    imagens contidas nelas. Assim extrai cada
    uma e converte para uma imagem pillow, e
    também converte seu modo de cor com a
    função 'color_mode_convert()' e por fim,
    salva cada imagem com um numero antes
    da extensão do arquivo caso seja mais de
    uma imagem a ser extraída.
    :param file: Caminho para o arquivo PDF.
    :param prev_name: Nome original do arquivo
    :param new_name: Novo nome do arquivo
    :param output_path: Diretório de saída
    :return:
    '''
    filename = new_name.replace(form, '')
    pdf_file = Pdf.open(file, allow_overwriting_input=True)
    count = 1
    count_img = 0
    for pagina in pdf_file.pages:
        print('\n')
        print(f'PDF Pages: {pagina.images.items()}')
        for name,  imagem in pagina.images.items():
            print(len(pdf_file.pages))
            print('=' * 100)
            if len(pdf_file.pages) > 1:
                print('~'*100)
                print('=' * 100)
                print(f'PDF Names: {name}')
                print(f'Imagem Velha : {imagem}')
                _Image = PdfImage(imagem).as_pil_image()
                print(f'Modo de Imagem Inicial: {_Image._mode}')
                print(f'Imagem ANTES : {_Image}')
                print('MAIS DE 1')
                print('Convertendo Modo de Imagem...')
                n_Image = color_mode_convert(
                    image_file=_Image, input_mode=_Image._mode, is_pdf=True)

                print(f'Imagem Nova : {n_Image}')
                new_name = f'{filename}_{count}{form}'
                n_Image.save(f'{output_path}{filename}_{count}{form}')
                add_to_log(f"{lng.ltxt_ExtractedAndConvertedFrom} [ {
                           prev_name} ] {lng.ltxt_To} [ {new_name} ].")
                count_img += 1
                print(f"Extraído e Convertido de {prev_name} para {new_name}")
                print('=' * 100)
                print('~'*100)
            else:
                print('=' * 100)
                print(f'PDF Names: {name}')
                imagem['/ColorSpace'] = pikepdf.Name('/DeviceRGB')
                _Image = PdfImage(imagem).as_pil_image()
                print(f'Modo de Imagem Inicial: {_Image._mode}')
                print(f'Imagem ANTES : {_Image}')
                print(f'Imagem ANTES : {_Image}')
                print('MENOS DE 1')
                n_Image = color_mode_convert(
                    image_file=_Image, input_mode=_Image._mode, is_pdf=True)

                print(n_Image)
                n_Image.save(f'{output_path}{new_name}')
                add_to_log(f"{lng.ltxt_Converted} [ {prev_name} ] {
                           lng.ltxt_To} [ {new_name} ].")
                count_img += 1
                print(f"Convertido {prev_name} para {new_name}")
                print('=' * 100)

            print('\n')
            count += 1
        if count_img <= 0:
            add_to_log(f"{lng.ltxt_NoImageFoundIn} [ {prev_name} ].")


def convert_to_jpg_file(file='', prev_name='', new_name='', output_path=''):
    '''
    Abre a imagem com o pillow usando
    o caminho em 'file' e converte para RGB.
    Depois gera um caminho de saída usando o
    'output_path'+'new_name' e inicia
    a função 'ask_replace_file_on_save()'.
    :param file: Caminho para a imagem.
    :param prev_name: Nome da imagem original.
    :param new_name: Nome da imagem final
    :param output_path: Diretório de saída.
    :return:
    '''
    img = Image.open(file).convert('RGB')
    out = f'{output_path}{new_name}'
    ask_replace_file_on_save(img, out, prev_name)
    # Image.open(file).convert('RGB').save(f'{output_path}{new_name}')


def convert_other_file(file='', prev_name='', new_name='', output_path=''):
    '''
    Abre a imagem com o pilow usando
    o caminho em 'file' e converte o
    modo de cor usando a função
    'color_mode_convert()', por fim,
    inicia a função 'ask_replace_file_on_save()'.
    :param file: Caminho para a imagem.
    :param prev_name: Nome da imagem original.
    :param new_name: Nome da imagem final
    :param output_path: Diretório de saída.
    :return:
    '''
    image_file = Image.open(file)
    image_file_new = color_mode_convert(
        image_file=image_file, auto=False, input_mode=image_file._mode)
    out = f'{output_path}{new_name}'
    ask_replace_file_on_save(image_file_new, out, prev_name)
    # image_file_new.save(f'{output_path}{new_name}')


def set_colors():
    """
    Reseta as cores do dicionário de cores colors
    Implementa as novas cores nos assets.
    """
    colors['text_c'] = themeset('black', 'white')
    colors['frame_c'] = themeset('gray91', 'gray20')
    colors['button_c'] = themeset('gray100', 'gray30')
    colors['buttonunselect_c'] = themeset('gray75', 'gray40')
    colors['buttonhoverunselect_c'] = themeset('gray91', 'gray60')
    colors['scrollbar_c'] = themeset('gray75', 'gray30')
    colors['buttondisable_c'] = themeset('gray75', 'gray15')
    colors['textdisable_c'] = themeset('gray20', 'gray40')
    colors['preview_c'] = themeset('gray85', 'gray30')

    fr_output1.configure(fg_color=colors['frame_c'])
    fr_output2.configure(fg_color=colors['frame_c'])
    fr_output3.configure(fg_color=colors['frame_c'])
    fr_entry.configure(
        fg_color=colors['frame_c'], scrollbar_button_color=colors['scrollbar_c'])
    fr_imgvisu.configure(fg_color=colors['frame_c'])
    fr_config1.configure(fg_color=colors['frame_c'])
    fr_config2.configure(fg_color=colors['frame_c'])
    fr_about1.configure(fg_color=colors['frame_c'])
    fr_about2.configure(
        fg_color=colors['frame_c'], scrollbar_button_color=colors['scrollbar_c'], text_color=colors['text_c'])
    fr_log.configure(
        fg_color=colors['frame_c'], scrollbar_button_color=colors['scrollbar_c'], text_color=colors['text_c'])
    tab_main.configure(text_color=colors['text_c'], )
    bt_loadfiles.configure(
        fg_color=colors['button_c'], text_color=colors['text_c'])
    bt_clear.configure(
        fg_color=colors['button_c'], text_color=colors['text_c'])
    bt_loadfolder.configure(
        fg_color=colors['button_c'], text_color=colors['text_c'])
    bt_close.configure(
        fg_color=colors['button_c'], text_color=colors['text_c'])
    bt_start.configure(
        fg_color=colors['button_c'], text_color=colors['text_c'])
    bt_output.configure(
        fg_color=colors['button_c'], text_color=colors['text_c'])
    tab_main._segmented_button.configure(fg_color=colors['button_c'], unselected_color=colors['buttonunselect_c'],
                                         unselected_hover_color=colors['buttonhoverunselect_c'])
    opt_output1.configure(fg_color=colors['button_c'], button_color=colors['button_c'],
                          dropdown_fg_color=colors['button_c'], text_color=colors['text_c'])
    opt_output2.configure(fg_color=colors['button_c'], button_color=colors['button_c'],
                          dropdown_fg_color=colors['button_c'], text_color=colors['text_c'])
    opt_output3.configure(fg_color=colors['button_c'], button_color=colors['button_c'],
                          dropdown_fg_color=colors['button_c'], text_color=colors['text_c'])
    opt_output4.configure(fg_color=colors['button_c'], button_color=colors['button_c'],
                          dropdown_fg_color=colors['button_c'], text_color=colors['text_c'])
    rad_output1.configure(border_color=colors['scrollbar_c'])
    rad_output2.configure(border_color=colors['scrollbar_c'])
    check_output1.configure(border_color=colors['scrollbar_c'])
    check_output2.configure(border_color=colors['scrollbar_c'])
    check_output3.configure(border_color=colors['scrollbar_c'])
    check_output4.configure(border_color=colors['scrollbar_c'])
    check_output5.configure(border_color=colors['scrollbar_c'])
    entry_output.configure(
        text_color=colors['text_c'], fg_color=colors['button_c'])
    lab_logo2.configure(text_color=colors['text_c'])
    lab_img_preview.configure(fg_color=colors['preview_c'])
    img_info.configure(
        fg_color=colors['preview_c'], text_color=colors['text_c'])
    radio_event()


def set_theme(valor):
    """
    Compara o valor do OptionMenu e chama o ctk.set_appearance_mode() para aplicar o tema 'Dark' ou 'Light'.\n
    E chama o set_colors() para aplicar as novas cores.\n
    :param valor: str('Escuro') ou str('Claro').
    """
    global colors
    if valor == lng.opt_output4_txt[1]:
        print('CATAPIMBAS')
        ctk.set_appearance_mode('Dark')
        data['theme'] = 'dark'
    elif valor == lng.opt_output4_txt[0]:
        ctk.set_appearance_mode('Light')
        data['theme'] = 'light'

    set_colors()


def themeset(color_l, color_d, color_m=""):
    """
    Compara se o appearance_mode()
    está no 'Light' ou 'Dark'
    e aplica as determinadas
    cores na string color_m.
    :param color_l: Cor tema Light
    :param color_d: Cor tema Dark
    :param color_m: Cor principal
    :return: Retorna o valor de color_m
    para o item no dicionário colors{}.
    """
    if ctk.get_appearance_mode() == 'Light':
        color_m = color_l
    elif ctk.get_appearance_mode() == 'Dark':
        color_m = color_d
    return color_m


def radio_event():
    '''
    Checa qual radio_button está
    ativado, se for 'rad_output1'
    então o botão 'bt_output' será
    desativado e a caixa de entrada
    'entry_output' mudará de cor.
    caso o 'rad_output2' esteja ativado,
    o inverso acontecerá.
    :return:
    '''
    valor = radiovar.get()
    if valor == 1:
        bt_output.configure(state=ctk.DISABLED,
                            fg_color=colors['buttondisable_c'])
        entry_output.configure(
            text_color=colors['textdisable_c'], fg_color=colors['buttondisable_c'])
        data['output_mode'] = 1
    else:
        entry_output.configure(
            text_color=colors['text_c'], fg_color=colors['button_c'])
        bt_output.configure(state=ctk.NORMAL, fg_color=colors['button_c'])
        data['output_mode'] = 0


def add_to_log(_text=''):
    '''
    Adiciona uma mensagem no textbox
    'fr_log' no final da linha, e rola
    o texto pra cima a cad amensagem
    adicionada.
    :param _text: Mensagem que será inserida.
    :return:
    '''
    fr_log.configure(state=ctk.NORMAL)
    fr_log.insert(ctk.END, text=f'{_text}'+'\n\n')
    fr_log.yview(ctk.END)
    fr_log.configure(state=ctk.DISABLED)


def refresh_info_text(msg=f'{len(filenames)} {lng.lab_info_txt}'):
    '''
    Atualiza a mensagem na caixa de texto 'lab_info'.
    :param msg: Mensagem a ser atualizada.
    :return:
    '''
    lab_info.delete('0.0', 'end')
    lab_info.insert('0.0', text=msg)
    print(f'INFO NUM = {len(filenames)}')


"""
----------------------------------------------------------------------------------------------------------------------------------------------
Assets ---------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""

img_folder = ctk.CTkImage(light_image=Image.open('CrimsonSimpleImageConverter\\assets\\folder_icon_dark.png'),
                          dark_image=Image.open('CrimsonSimpleImageConverter\\assets\\folder_icon.png'), size=(24, 20))
img_folderplus = ctk.CTkImage(light_image=Image.open('CrimsonSimpleImageConverter\\assets\\folderplus_icon_dark.png'),
                              dark_image=Image.open('CrimsonSimpleImageConverter\\assets\\folderplus_icon.png'), size=(24, 20))
img_clean = ctk.CTkImage(light_image=Image.open('CrimsonSimpleImageConverter\\assets\\clean_icon_dark.png'),
                         dark_image=Image.open('CrimsonSimpleImageConverter\\assets\\clean_icon.png'), size=(28, 20))
img_convert = ctk.CTkImage(light_image=Image.open('CrimsonSimpleImageConverter\\assets\\convert_icon_dark.png'),
                           dark_image=Image.open('CrimsonSimpleImageConverter\\assets\\convert_icon.png'), size=(22, 20))
img_close = ctk.CTkImage(light_image=Image.open('CrimsonSimpleImageConverter\\assets\\close_icon_dark.png'),
                         dark_image=Image.open('CrimsonSimpleImageConverter\\assets\\close_icon.png'), size=(22, 20))
img_logo = ctk.CTkImage(light_image=Image.open('CrimsonSimpleImageConverter\\assets\\logo.png'),
                        dark_image=Image.open('CrimsonSimpleImageConverter\\assets\\logo.png'), size=(250, 250))
img_previewbg = ctk.CTkImage(light_image=Image.open(
    'CrimsonSimpleImageConverter\\assets\\preview_bg.png'), size=(450, 320))
colors = {'text_c': themeset('black', 'white'), 'frame_c': themeset('gray91', 'gray20'), 'button_c': themeset('gray100', 'gray30'),
          'buttonunselect_c': themeset('gray75', 'gray40'), 'buttonhoverunselect_c': themeset('gray91', 'gray60'),
          'scrollbar_c': themeset('gray75', 'gray30'), 'buttondisable_c': themeset('gray75', 'gray15'),
          'textdisable_c': themeset('gray45', 'gray40'), 'preview_c': themeset('gray85', 'gray30')}

titlefont = ctk.CTkFont(family='Arial', size=24, weight='bold')
subtitlefont = ctk.CTkFont(family='Arial', size=16, weight='bold')
buttonfont = ctk.CTkFont(family='Arial', size=12, weight='bold')
logfont = ctk.CTkFont(family='Arial', size=14, weight='bold')

"""
----------------------------------------------------------------------------------------------------------------------------------------------
Abas -----------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""

tab_main = ctk.CTkTabview(j_main, border_width=0, corner_radius=6,
                          segmented_button_selected_color='crimson', segmented_button_selected_hover_color='indianred1',
                          width=1250, height=700, text_color=colors['text_c'])
tab_main.add(lng.t_input)  # Entrada
tab_main.add(lng.t_output)  # Saída
tab_main.add(lng.t_log)  # Registro
tab_main.add(lng.t_settings)  # Configurações
tab_main.add(lng.t_about)  # Sobre
tab_main._segmented_button.configure(font=buttonfont, fg_color=colors['button_c'],
                                     unselected_color=colors['buttonunselect_c'], unselected_hover_color=colors['buttonhoverunselect_c'])
tab_main.pack()

"""
Conteúdo aba ENTRADA -------------------------------------------------------------------------------------------------------------------------
"""
lab_info = ctk.CTkTextbox(tab_main.tab(lng.t_input),
                          font=buttonfont, width=315, height=28)
lab_info.insert('0.0', text=f'{len(filenames)} {lng.lab_info_txt}')
lab_info.place(x=620, y=10)

bt_loadfiles = ctk.CTkButton(tab_main.tab(lng.t_input), text=lng.bt_load_files_txt, width=180,
                             fg_color=colors['button_c'], hover_color='crimson', font=buttonfont,
                             image=img_folder, text_color=colors['text_c'], command=start_load_files)
bt_loadfiles.place(x=20, y=10)
bt_loadfolder = ctk.CTkButton(tab_main.tab(lng.t_input), text=lng.bt_load_folder_txt, width=180,
                              fg_color=colors['button_c'], hover_color='crimson', font=buttonfont,
                              image=img_folderplus, text_color=colors['text_c'])
bt_loadfolder.place(x=220, y=10)
bt_clear = ctk.CTkButton(tab_main.tab(lng.t_input), text=lng.bt_clear_txt, width=180,
                         fg_color=colors['button_c'], hover_color='crimson', font=buttonfont,
                         image=img_clean, text_color=colors['text_c'], command=clear_files)
bt_clear.place(x=420, y=10)
bt_start = ctk.CTkButton(tab_main.tab(lng.t_input), text=lng.bt_satrt_txt, width=125,
                         fg_color=colors['button_c'], hover_color='crimson', font=buttonfont,
                         image=img_convert, text_color=colors['text_c'], command=start_conversion)
bt_start.place(x=950, y=10)
bt_close = ctk.CTkButton(tab_main.tab(lng.t_input), text=lng.bt_close_txt, width=125,
                         fg_color=colors['button_c'], hover_color='crimson', font=buttonfont,
                         image=img_close, text_color=colors['text_c'], command=close_app)
bt_close.place(x=1095, y=10)
fr_entry = ctk.CTkScrollableFrame(tab_main.tab(lng.t_input), width=700, height=585, fg_color=colors['frame_c'],
                                  scrollbar_button_color=colors['scrollbar_c'], scrollbar_button_hover_color='crimson')
fr_entry.place(x=20, y=48)
fr_imgvisu = ctk.CTkFrame(tab_main.tab(lng.t_input),
                          width=470, height=596, fg_color=colors['frame_c'])
lab_img_preview = ctk.CTkLabel(
    fr_imgvisu, text=None, width=450, height=320, fg_color=colors['preview_c'])
lab_img_preview.place(x=10, y=10)
img_info = ctk.CTkTextbox(fr_imgvisu, width=450, height=245, fg_color=colors['preview_c'],
                          scrollbar_button_color=colors['scrollbar_c'], scrollbar_button_hover_color='crimson',
                          font=buttonfont, text_color=colors['text_c'], corner_radius=0)
img_info.insert('0.0', text=' ')
img_info.configure(state=ctk.DISABLED)
img_info.place(x=10, y=340)
fr_imgvisu.place(x=750, y=48)

"""
Conteúdo aba SAÍDA--------------------------------------------------------------------------------------------------------------------------
"""
# Labels Principais da Tab SAÍDA
lab_output1 = ctk.CTkLabel(tab_main.tab(
    lng.t_output), text=lng.lab_output1_txt, font=titlefont).place(x=20, y=10)
lab_output2 = ctk.CTkLabel(tab_main.tab(
    lng.t_output), text=lng.lab_output2_txt, font=titlefont).place(x=20, y=168)
lab_output3 = ctk.CTkLabel(tab_main.tab(
    lng.t_output), text=lng.lab_output3_txt, font=titlefont).place(x=20, y=326)

# Frame1 da Tab SAÍDA
fr_output1 = ctk.CTkFrame(tab_main.tab(lng.t_output),
                          width=1135, height=100, fg_color=colors['frame_c'])
# Radial Buttons do Frame1
if output_path == '':
    radiovar = ctk.IntVar(value=1)
else:
    radiovar = init_rad
rad_output1 = ctk.CTkRadioButton(fr_output1, text=lng.rad_output1_txt, font=subtitlefont, radiobutton_height=16,
                                 radiobutton_width=16,
                                 border_width_unchecked=3, border_width_checked=8, fg_color='crimson',
                                 hover_color='indianred1', border_color=colors['scrollbar_c'],
                                 variable=radiovar, value=1, command=radio_event)
rad_output1.place(x=20, y=10)
rad_output2 = ctk.CTkRadioButton(fr_output1, text=lng.rad_output2_txt, font=subtitlefont, radiobutton_height=16,
                                 radiobutton_width=16,
                                 border_width_unchecked=3, border_width_checked=8, fg_color='crimson',
                                 hover_color='indianred1', border_color=colors['scrollbar_c'],
                                 variable=radiovar, value=0, command=radio_event)
rad_output2.place(x=20, y=48)
# Entrada de Texto do Frame1
if output_path != '':
    entrytext = ctk.StringVar(value=output_path)
else:
    entrytext = ctk.StringVar(value=lng.entry_output_txt)
entry_output = ctk.CTkEntry(fr_output1, width=700, text_color=colors['text_c'], textvariable=entrytext,
                            state=ctk.DISABLED, fg_color=colors['button_c'])
entry_output.place(x=120, y=48)
# Botão de Load Path do Frame1
bt_output = ctk.CTkButton(fr_output1, text="", width=50, fg_color=colors['button_c'], hover_color='crimson',
                          image=img_folder, command=load_output_path)
bt_output.place(x=830, y=48)
# Posicionamento do Frame1
fr_output1.place(x=85, y=48)
# Fim do Frame1

# Frame 2 da Tab SAÍDA
fr_output2 = ctk.CTkFrame(tab_main.tab(lng.t_output),
                          width=1135, height=100, fg_color=colors['frame_c'])
# Option Button do Frame2
conv_options = ['JPG - .jpg, .jpeg, .jfif', 'PNG - .png', 'GIF - .gif',
                'BMP - .bmp', 'WEBP - .webp', 'ICO - .ico', 'TIFF - .tiff',
                'JPEG2000 - .pj2', 'PDF - .pdf', 'EPS - .eps']  # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
var_options1 = ctk.StringVar(value=conv_options[init_conv_opt])
opt_output1 = ctk.CTkOptionMenu(fr_output2, variable=var_options1,
                                values=conv_options, width=350,
                                fg_color=colors['button_c'], button_color=colors['button_c'], button_hover_color='crimson',
                                dropdown_fg_color=colors['button_c'], dropdown_hover_color='crimson',
                                text_color=colors['text_c'], command=set_output_format)
opt_output1.place(x=20, y=10)
opt_output1.set(var_options1.get())
# Posicionamento do Frame
fr_output2.place(x=85, y=206)
# Fim do Frame2

# Frame 3 da Tab SAÍDA
fr_output3 = ctk.CTkFrame(tab_main.tab(lng.t_output),
                          width=1135, height=280, fg_color=colors['frame_c'])
# Labels do Frame3
lab_output4 = ctk.CTkLabel(
    fr_output3, text=lng.lab_output4_txt, font=subtitlefont)
lab_output4.place(x=20, y=10)
lab_output5 = ctk.CTkLabel(
    fr_output3, text=lng.lab_output5_txt, font=subtitlefont)
lab_output5.place(x=20, y=84)
# Option Button do Frame3
var_options2 = ctk.StringVar(value=lng.opt_output2_txt[init_rep_opt])
opt_output2 = ctk.CTkOptionMenu(fr_output3, variable=var_options2,
                                values=lng.opt_output2_txt, width=175,
                                fg_color=colors['button_c'], button_color=colors['button_c'], button_hover_color='crimson',
                                dropdown_fg_color=colors['button_c'], dropdown_hover_color='crimson',
                                text_color=colors['text_c'], command=set_alreadyexistent_file)
opt_output2.set(var_options2.get())
opt_output2.place(x=290, y=10)
# Check Box do Frame3
check1_var = init_chk1
check2_var = init_chk2
check3_var = init_chk3
check4_var = init_chk4
check5_var = init_chk5
check_output1 = ctk.CTkCheckBox(fr_output3, checkbox_width=16, checkbox_height=16, text=lng.check_output1_txt,
                                font=buttonfont,
                                hover_color='indianred1', checkmark_color='white', fg_color='crimson',
                                border_width=3, corner_radius=0, border_color=colors['scrollbar_c'],
                                variable=check1_var, onvalue=1, offvalue=0)
check_output1.place(x=20, y=48)
check_output2 = ctk.CTkCheckBox(fr_output3, checkbox_width=16, checkbox_height=16, text=lng.check_output2_txt,
                                font=buttonfont, hover_color='indianred1', checkmark_color='white', fg_color='crimson',
                                border_width=3, corner_radius=0, border_color=colors['scrollbar_c'],
                                variable=check2_var, onvalue=1, offvalue=0)
check_output2.place(x=40, y=114)
check_output3 = ctk.CTkCheckBox(fr_output3, text=lng.check_output3_txt, checkbox_width=16, checkbox_height=16,
                                font=buttonfont,
                                hover_color='indianred1', checkmark_color='white', fg_color='crimson',
                                border_width=3, corner_radius=0, border_color=colors['scrollbar_c'],
                                variable=check3_var, onvalue=1, offvalue=0)
check_output3.place(x=40, y=144)
check_output4 = ctk.CTkCheckBox(fr_output3, text=lng.check_output4_txt, checkbox_width=16, checkbox_height=16,
                                font=buttonfont,
                                hover_color='indianred1', checkmark_color='white', fg_color='crimson',
                                border_width=3, corner_radius=0, border_color=colors['scrollbar_c'],
                                variable=check4_var, onvalue=1, offvalue=0)
check_output4.place(x=40, y=174)
check_output5 = ctk.CTkCheckBox(fr_output3, text=lng.check_output5_txt, checkbox_width=16, checkbox_height=16,
                                font=buttonfont,
                                hover_color='indianred1', checkmark_color='white', fg_color='crimson',
                                border_width=3, corner_radius=0, border_color=colors['scrollbar_c'],
                                variable=check5_var, onvalue=1, offvalue=0)
check_output5.place(x=40, y=204)
# Posicionamento do Frame
fr_output3.place(x=85, y=364)
# Fim do Frame3

"""
Conteúdo aba REGISTRO -------------------------------------------------------------------------------------------------------------------------
"""
lab_log = ctk.CTkLabel(tab_main.tab(lng.t_log),
                       text=lng.lab_log_txt, font=titlefont).place(x=20, y=10)
fr_log = ctk.CTkTextbox(tab_main.tab(lng.t_log), width=1135, height=595, fg_color=colors['frame_c'],
                        scrollbar_button_color=colors['scrollbar_c'], scrollbar_button_hover_color='crimson',
                        font=logfont, text_color=colors['text_c'])
fr_log.place(x=85, y=48)
fr_log.configure(state=ctk.DISABLED)

"""
Conteúdo aba CONFIGURAÇÕES ------------------------------------------------------------------------------------------------------------
"""
# Labels Principais da Tab CONFIGURAÇÕES
lab_config1 = ctk.CTkLabel(tab_main.tab(
    lng.t_settings), text=lng.lab_config1_txt, font=titlefont).place(x=20, y=10)
lab_config2 = ctk.CTkLabel(tab_main.tab(
    lng.t_settings), text=lng.lab_config2_txt, font=titlefont).place(x=20, y=118)

# Frame1 da Tab CONFIGURAÇÕES
fr_config1 = ctk.CTkFrame(tab_main.tab(lng.t_settings),
                          width=625, height=50, fg_color=colors['frame_c'])
# Option Button do Frame1
opt_output3 = ctk.CTkOptionMenu(fr_config1,
                                values=['[PT-BR] Português Brasileiro',
                                        '[ENG] English', '[ESP] Español'],
                                fg_color=colors['button_c'], button_color=colors['button_c'], button_hover_color='crimson',
                                dropdown_fg_color=colors['button_c'], dropdown_hover_color='crimson', width=585,
                                text_color=colors['text_c'], command=set_language)
opt_output3.place(x=20, y=10)
if data['language'] == 'pt-br':
    opt_output3.set('[PT-BR] Português Brasileiro')
elif data['language'] == 'eng':
    opt_output3.set('[ENG] English')
elif data['language'] == 'spa':
    opt_output3.set('[ESP] Español')
# Posicionamento do Frame1
fr_config1.place(x=85, y=48)
# Fim do Frame2

# Frame2 da Tab CONFIGURAÇÕES
fr_config2 = ctk.CTkFrame(tab_main.tab(lng.t_settings),
                          width=625, height=50, fg_color=colors['frame_c'])
# Option Button do Frame2
opt_output4 = ctk.CTkOptionMenu(fr_config2,
                                values=lng.opt_output4_txt, fg_color=colors[
                                    'button_c'], button_color=colors['button_c'],
                                button_hover_color='crimson',
                                dropdown_fg_color=colors['button_c'], dropdown_hover_color='crimson', width=585,
                                text_color=colors['text_c'], command=set_theme)
opt_output4.place(x=20, y=10)
if data['theme'] == 'light':
    opt_output4.set(lng.opt_output4_txt[0])
elif data['theme'] == 'dark':
    opt_output4.set(lng.opt_output4_txt[1])
# Posicionamento do Frame2
fr_config2.place(x=85, y=156)
# Fim do Frame2

"""
Conteúdo aba SOBRE -------------------------------------------------------------------------------------------------------------------
"""

fr_about1 = ctk.CTkFrame(tab_main.tab(lng.t_about),
                         width=500, height=300, fg_color=colors['frame_c'])
lab_logo1 = ctk.CTkLabel(fr_about1, text="", image=img_logo).place(x=125, y=5)
lab_logo2 = ctk.CTkLabel(fr_about1, text='Crimson Simple Image Converter',
                         font=titlefont, text_color=colors['text_c'])
lab_logo2.place(x=65, y=265)
fr_about1.pack(pady=10)
fr_about2 = ctk.CTkTextbox(tab_main.tab(lng.t_about), width=1135, height=310, fg_color=colors['frame_c'],
                           scrollbar_button_color=colors['scrollbar_c'], scrollbar_button_hover_color='crimson',
                           font=subtitlefont, text_color=colors['text_c'])
fr_about2.insert('0.0', text='Crimson Simple Image Converter version 1.0.0.0 - windows (20\\08\\2024)\n\n'
                             + 'Email: alexrocha6839@gmail.com\n\n' +
                 'Linkedin: linkedin.com\\in\\alxrochadev\n\n'
                             + 'Programming by Alex Rocha (Requiemd)\n\n' + 'Logo by Alex Rocha (Requiemd)\n\n'
                             + 'Icons by Alex Rocha (Requiemd)')
fr_about2.configure(state=ctk.DISABLED)
fr_about2.pack(pady=10)

"""
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""

print(opt_output1.get())
print(f'{filenames}')
print(f'{output_path}')
set_output_format()
set_alreadyexistent_file()
radio_event()
j_main.protocol("WM_DELETE_WINDOW", close_app)
j_main.mainloop()
