import json

"""
Aqui serão armazenadas as variáveis que determinarão os textos da UI
"""
data = json.load(
    open('.\\data\\data.json', 'r', encoding='utf-8'))
current_language = data['language']  # pt-br, en, spa
translate_dict = {}


def load_translation(language='eng'):
    print(f'Carregando arquivo de Linguagem...')
    with open(f'.\\data\\lang_{language}.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def change_language():
    global translate_dict
    # print(f'Idioma mudou para {lang}.')
    # current_language = lang
    translate_dict = load_translation(current_language)


def text(key):
    return translate_dict.get(key, key)


def m_text(key, value):
    return translate_dict.get(key, value)


change_language()


"""
----------------------------------------------------------------------------------------------------------------------------------------------
Textos da Tab Entrada ------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""
t_input = text('text_01')
lab_info_txt = text('text_02')
bt_load_files_txt = text('text_03')
bt_load_folder_txt = text('text_04')
bt_clear_txt = text('text_05')
bt_satrt_txt = text('text_06')
bt_close_txt = text('text_07')
"""
----------------------------------------------------------------------------------------------------------------------------------------------
Textos da Tab Saída --------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""
t_output = text('text_08')
lab_output1_txt = text('text_09')
lab_output2_txt = text('text_10')
lab_output3_txt = text('text_11')
rad_output1_txt = text('text_12')
rad_output2_txt = text('text_13')
entry_output_txt = text('text_14')
lab_output4_txt = text('text_15')
lab_output5_txt = text('text_16')
opt_output2_txt = [translate_dict['text_17'][0], translate_dict['text_17']
                   [1], translate_dict['text_17'][2], translate_dict['text_17'][3]]
opt_output2_default_txt = opt_output2_txt[0]  # Igual a 'Perguntar'
check_output1_txt = text('text_18')
check_output2_txt = text('text_19')
check_output3_txt = text('text_20')
check_output4_txt = text('text_21')
check_output5_txt = text('text_22')
"""
----------------------------------------------------------------------------------------------------------------------------------------------
Textos da Tab Registros ----------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""
t_log = text('text_23')
lab_log_txt = text('text_24')
"""
----------------------------------------------------------------------------------------------------------------------------------------------
Textos da Tab Configurações ------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""
t_settings = text('text_25')
lab_config1_txt = text('text_26')
lab_config2_txt = text('text_27')
opt_output4_txt = [translate_dict['text_28'][0], translate_dict['text_28'][1]]
"""
----------------------------------------------------------------------------------------------------------------------------------------------
Textos da Tab Sobre --------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""
t_about = text('text_29')
lab_logo2_txt = text('text_30')
"""
----------------------------------------------------------------------------------------------------------------------------------------------
Textos de Funções ----------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
"""
# rename_action()-----------------------------------------------
ren_lab_txt = text('text_31')
ren_warning_txt = text('text_32')
ren_entry_txt = text('text_33')
# ask_user_action()---------------------------------------------
dlg_lab_txt = text('text_34')
dlg_bt1_txt = text('text_35')
dlg_bt2_txt = text('text_36')
dlg_bt3_txt = text('text_37')
dlg_info_txt = translate_dict['text_38'][0] + translate_dict['text_38'][1] + \
    translate_dict['text_38'][2] + \
    translate_dict['text_38'][3] + translate_dict['text_38'][4]
# set_alreadyexistent_file()------------------------------------
# usar: rep_options[0] ou rep_options[1] ou rep_options[2] ou rep_options[3]
rep_options = opt_output2_txt
# extract_image_info()------------------------------------------
ex_img_txt1 = text('text_39')
ex_img_txt2 = text('text_40')
ex_img_txt3 = text('text_41')
ex_img_txt4 = text('text_42')
ex_img_txt5 = text('text_43')
ex_img_txt6 = text('text_44')
# extract_pdf_info()---------------------------------------------
ex_pdf_unknow = text('text_45')
ex_pdf_txt1 = text('text_46')
ex_pdf_txt2 = text('text_47')
ex_pdf_txt3 = text('text_48')
ex_pdf_txt4 = text('text_49')
ex_pdf_txt5 = text('text_50')
ex_pdf_txt6 = text('text_51')
ex_pdf_txt7 = text('text_52')
ex_pdf_txt8 = text('text_53')
ex_pdf_txt9 = text('text_54')
ex_pdf_txt0 = text('text_55')
# format_pdf_date()---------------------------------------------
unknow_date = text('text_56')
# add_to_log()--------------------------------------------------
ltxt_Converted = text('text_57')
ltxt_ExtractedAndConvertedFrom = text('text_58')
ltxt_To = text('text_59')
ltxt_StartingProccess = text('text_60')
ltxt_NoImageFoundIn = text('text_61')
ltxt_ProccessFinished = text('text_62')
ltxt_Ignored = text('text_63')
ltxt_FromConversionList = text('text_64')
# -------------------------------------------------------------
res_lab_txt = text('text_65')


print(t_input)
print(dlg_info_txt)
print(opt_output2_txt)
