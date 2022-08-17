#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""    Программа sel_res_tk.py - графическая оболочка для
    программы-модуля sel_res_cp.py  для получения
    вариантов комбинаций резисторов. """

#                Автор: Л.М.Матвеев

import common
common.pyscr = u'pyscripter' in dir()
from common import trm_code, pyscr


#------------------------------------------------------------------------------
def printm(s):
    """ Печать Юникод-строк в терминал и скриптер.
        Автоматический перевод строки не производится. """

    if pyscr:
        sys.stdout.write(s)
    else:
#        sys.stdout.write(s.encode(trm_code))
        sys.stdout.write(s)
    if prn_only:
        return
    txt.insert(END, s)
    txt.yview(END)
    root.update()
#..............................................................................
# Переопределение функции печати
common.printm = printm

from os.path import join, split
# import tkMessageBox
from tkinter import messagebox
from sel_res_cp import calc, list_dRX, list_nRX, IND_1, IND_5, modes

# from Tkinter import *
# import tkinter as tk
from tkinter import *
# from ttk import *
from tkinter.ttk import *

root = Tk()

photo_files = ['D.gif', 'X.gif', 'S.gif', 'P.gif', 'SP.gif']

#------------------------------------------------------------------------------
root.title(u'  Подбор резисторов')
root.resizable(False, False)  # запрет изм разм окна по гориз и по верт

frm1 = LabelFrame(root, labelanchor='n', text=u' Возможные варианты ')
frm1.pack(side=LEFT)


#------------------------------------------------------------------------------
txt = Text(frm1, font="Consolas 10", height=27)
scr = Scrollbar(frm1, command=txt.yview)
txt.configure(yscrollcommand=scr.set)
scr.grid(row=0, column=1, sticky=NS, padx=3, pady=3)
txt.grid(row=0, column=0, padx=3, pady=4)
#..............................................................................


#------------------------------------------------------------------------------
def cmd_btn_clr():
    """  """
    txt.delete('1.0', END)
#..............................................................................

mults_in = (1e-3, 1., 1e3, 1e6)
units_in = ({u'm', u'м'},
            {u'', u'.'},
            {u'k', u'к', u'K', u'К'},
            {u'M', u'М'})


#------------------------------------------------------------------------------
def str_to_val(s):
    """ Преобразует сокращённое обозначение величины в значение """

    frag_types = u''  # Типы фрагментов
    frags = []

    # Разбор входной строки на фрагменты типов d,p,e
    ch0_type = u''
    frag = u''
    for ch in s:  # .lower()
        # Определяем тип символа
        if ch == u' ':
            continue
        elif ch.isdigit():
            ch_type = u'd'  # цифра
        elif ch in u',.':
            ch_type = u'p'  # точка
        else:
            ch_type = u'e'  # другое

        # Новый ли тип символа тип символа
        if not frag:
            ch0_type = ch_type
        elif ch0_type != ch_type:
            frags.append(frag)
            frag = u''
            frag_types += ch0_type
            ch0_type = ch_type
        frag += ch
    else:
        frags.append(frag)
        frag_types += ch0_type

    # Сокращённое символьное обозначение ЕИ
    i = frag_types.find(u'e')
    if i >= 0:
        pref_meas = frags[i]
    elif u'p' in frag_types:
        pref_meas = u'.'
    else:
        pref_meas = u''
    # Поиск индекса символьного обозначения ЕИ
    for ind, variants in enumerate(units_in):
        if pref_meas[:1] in variants:
            break
    else:
        return -1  # Несоответвтующее правилам число

    # Выделение значения
    if     (frag_types == u'ded' and len(frags[1]) == 1 or
            frag_types == u'dpde' or
            frag_types == u'dpd'):
        number = frags[0] + u'.' + frags[2]
    elif   (frag_types == u'ed' and len(frags[0]) == 1 or
            frag_types == u'pde' or
            frag_types == u'pd'):
        number = u'.' + frags[1]
    elif   (frag_types == u'd' or
            frag_types == u'de' or
            frag_types == u'dp' or
            frag_types == u'dpe'):
        number = frags[0]
    else:
        return -1  # Несоответвтующее правилам число

    return float(number) * mults_in[ind]
#..............................................................................


#------------------------------------------------------------------------------
def cmd_btn_ok():
    """  """
    global old_ent_U0, old_ent_U1

    if rb_mode_var.get() < 2:
        u0 = str_to_val(ent_U0_var.get().replace(',', '.'))
        if u0 < 0:
            messagebox.showerror(
                title=u'Недопустимый формат числа',
                message=u'Исправить введённое значение "U0"')
            return
    else:
        u0 = -1
    u1 = str_to_val(ent_U1_var.get().replace(',', '.'))
    if u1 < 0:
        if rb_mode_var.get() < 2:
            messagebox.showerror(
                title=u'Недопустимый формат числа',
                message=u'Исправить введённое значение "U1"')
            return
        messagebox.showerror(
            title=u'Недопустимый формат числа',
            message=u'Исправить введённое значение "R необходимое"')
        return

    old_ent_U0 = ent_U0_var.get() if ent_U0_var.get() else old_ent_U0
    old_ent_U1 = ent_U1_var.get() if ent_U1_var.get() else old_ent_U1

    calc(mode=rb_mode_var.get(),
         u0=u0,#ent_U0_var.get(),
         du0=cbb_dU0.get(),
         u1=u1,#ent_U1_var.get(),
         du1=cbb_dU1.get(),
         dr0=cbb_dR0.get(),
         nr0=cbb_nR0.get(),
         dr1=cbb_dR1.get(),
         nr1=cbb_nR1.get(),
         e24_1=chb_E24_1_var.get())

#..............................................................................


ini_file_name = join(split(sys.argv[0])[0], 'ini.py')

old_rb_mode = 0
old_ent_U0 = u'1.0'
old_ent_U1 = u'3.0'
old_cbb_dU0 = IND_1 + 3
old_cbb_dU1 = IND_1
old_chb_E24_1 = 0
old_chb_RX = 1
old_cbb_dRi = [IND_5, IND_5]
old_cbb_nRji = tuple([[i if i < len(list_nRX) else len(list_nRX) - 1,
                       i if i < len(list_nRX) else len(list_nRX) - 1]
                      for i, _ in enumerate(list_dRX)])
try:
#    execfile(ini_file_name)
    exec(open(ini_file_name).read())
except (SyntaxError, IOError):
    old_rb_mode = 0
    old_ent_U0 = u'1.0'
    old_ent_U1 = u'3.0'
    old_cbb_dU0 = IND_1 + 3
    old_cbb_dU1 = IND_1
    old_chb_E24_1 = 0
    old_chb_RX = 1
    old_cbb_dRi = [IND_5, IND_5]
    old_cbb_nRji = tuple([[i if i < len(list_nRX) else len(list_nRX) - 1,
                           i if i < len(list_nRX) else len(list_nRX) - 1]
                          for i, _ in enumerate(list_dRX)])


#------------------------------------------------------------------------------
def set_old_values():
    """"""
    global photo
    cbb_dR0['values'] = list_dRX
    cbb_dR1['values'] = list_dRX
    cbb_dR0.current(old_cbb_dRi[0])  # Не возбуждает "ev_cbb_nr0(_)"
    cbb_dR1.current(old_cbb_dRi[1])

    j = cbb_dR0.current()
    cbb_nR0['values'] = ['%i' % n
                         for k, n in enumerate(list_nRX)
                         if k <= j and (cbb_dR0.get() != '1 %' or not chb_E24_1_var.get() or k <= IND_5)]
    if old_cbb_nRji[j][0] >= len(cbb_nR0['values']):
        cbb_nR0.current(len(cbb_nR0['values'])-1)
    else:
        cbb_nR0.current(old_cbb_nRji[j][0])

    j = cbb_dR1.current()
    cbb_nR1['values'] = ['%i' % n
                         for k, n in enumerate(list_nRX)
                         if k <= j and (cbb_dR1.get() != '1 %' or not chb_E24_1_var.get() or k <= IND_5)]
    if old_cbb_nRji[j][1] >= len(cbb_nR1['values']):
        cbb_nR1.current(len(cbb_nR1['values'])-1)
    else:
        cbb_nR1.current(old_cbb_nRji[j][1])

    if old_chb_RX:
        cbb_dR1.set(cbb_dR0.get())
        cbb_nR1.set(cbb_nR0.get())

        cbb_nR1['state'] = DISABLED
        cbb_dR1['state'] = DISABLED
        lab_R1['state'] = DISABLED

    cbb_dU0['values'] = list_dRX
    cbb_dU0.current(old_cbb_dU0)
    cbb_dU1['values'] = list_dRX
    cbb_dU1.current(old_cbb_dU1)

    if rb_mode_var.get() >= 2:
        #lab_U0['text'] = ''
        lab_U0X['text'] = ''
        lab_dU0X['text'] = ''
        #lab_U1['text'] = 'Rн'
        lab_U1X['text'] = 'R необходимое'
        cbb_dU0.set('')
        ent_U0_var.set('')
        cbb_dU0['state'] = DISABLED
        ent_U0['state'] = DISABLED

    photo = PhotoImage(file=photo_files[rb_mode_var.get()])
    lab_image['image'] = photo
#..............................................................................


#------------------------------------------------------------------------------
def save_old_values():
    """"""
    prg_code = 'utf-8'
    ss = [u'# -*- coding: %s -*-\n\n' % prg_code,
          u'old_rb_mode = %s\n' % rb_mode_var.get(),
          u'old_ent_U0 = u"%s"\n' % (ent_U0_var.get() if ent_U0_var.get() else old_ent_U0),
          u'old_ent_U1 = u"%s"\n' % ent_U1_var.get(),
          u'old_cbb_dU0 = %s\n' % old_cbb_dU0,
          u'old_cbb_dU1 = %s\n' % old_cbb_dU1,
          u'old_chb_E24_1 = %s\n' % chb_E24_1_var.get(),
          u'old_chb_RX = %s\n' % chb_RX_var.get(),
          u'old_cbb_dRi = [%s, %s]\n' % tuple(old_cbb_dRi), u'old_cbb_nRji = (\n']
    for x in old_cbb_nRji:
        ss.append(u'    [%s, %s],\n' % tuple(x))
    ss.append(u')\n')

    fd = open(ini_file_name, 'wb')
    fd.write(u''.join(ss).encode(prg_code))
    fd.close()
    printm(u'\n    Сохранение файла состояния произведено.\n')
    printm(u'    %s\n' % ini_file_name.replace(u'/', u'\\'))
#..............................................................................


#------------------------------------------------------------------------------
frm2 = Frame(root)
frm2.pack()


frm_mode = LabelFrame(frm2, text=u' Подбор резисторов: ', labelanchor='n')
frm_mode.grid(row=1, column=0, columnspan=2, padx=3, sticky="w")
#..............................................................................
frm_all = LabelFrame(frm2, text=u' параметры ', labelanchor='n')
frm_all.grid(row=7, column=0, columnspan=2, padx=3, sticky="w")

curr_row = -1
#------------------------------------------------------------------------------
curr_row += 1

#  0  +++++++++++++++++++++++++++++++++++++++
chb_E24_1_var = BooleanVar(value=old_chb_E24_1)


def cmd_chb_e24_1():
    j = cbb_dR0.current()
    cbb_nR0['values'] = ['%i' % n
                         for k, n in enumerate(list_nRX)
                         if k <= j and (cbb_dR0.get() != '1 %' or not chb_E24_1_var.get() or k <= IND_5)]
    if old_cbb_nRji[j][0] >= len(cbb_nR0['values']):
        cbb_nR0.current(len(cbb_nR0['values'])-1)
    else:
        cbb_nR0.current(old_cbb_nRji[j][0])

    j = cbb_dR1.current()
    cbb_nR1['values'] = ['%i' % n
                         for k, n in enumerate(list_nRX)
                         if k <= j and (cbb_dR1.get() != '1 %' or not chb_E24_1_var.get() or k <= IND_5)]
    if old_cbb_nRji[j][1] >= len(cbb_nR1['values']):
        cbb_nR1.current(len(cbb_nR1['values'])-1)
    else:
        cbb_nR1.current(old_cbb_nRji[j][1])

    if chb_RX_var.get():
        cbb_dR1.set(cbb_dR0.get())
        cbb_nR1.set(cbb_nR0.get())

chb_E24_1 = Checkbutton(
    frm_all, text=u'мантисы 1%-х из E24', command=cmd_chb_e24_1,
    onvalue=True, offvalue=False, variable=chb_E24_1_var)
chb_E24_1.grid(row=curr_row, column=0, columnspan=3, sticky="w")

#------------------------------------------------------------------------------
curr_row += 1

#  0  +++++++++++++++++++++++++++++++++++++++
chb_RX_var = BooleanVar(value=old_chb_RX)


def cmd_chb_rx():
    """  """
    if chb_RX_var.get():
        cbb_dR1.set(cbb_dR0.get())
        cbb_nR1.set(cbb_nR0.get())
        cbb_nR1['state'] = DISABLED
        cbb_dR1['state'] = DISABLED
        lab_R1['state'] = DISABLED
    else:
        cbb_dR1.current(old_cbb_dRi[1])
        cbb_nR1.current(old_cbb_nRji[old_cbb_dRi[1]][1])
        cbb_nR1['state'] = NORMAL
        cbb_dR1['state'] = NORMAL
        lab_R1['state'] = NORMAL

chb_RX = Checkbutton(
    frm_all, text=u'R1 и R2 однотипные', command=cmd_chb_rx,
    onvalue=True, offvalue=False, variable=chb_RX_var)
chb_RX.grid(row=curr_row, column=0, columnspan=3, sticky="w")

#------------------------------------------------------------------------------
curr_row += 1

#  1  +++++++++++++++++++++++++++++++++++++++
lab_dRX = Label(frm_all, text=u'точность')
lab_dRX.grid(row=curr_row, column=1)

#  2  +++++++++++++++++++++++++++++++++++++++
lab_nRX = Label(frm_all, text=u'из мантис')
lab_nRX.grid(row=curr_row, column=2)

#------------------------------------------------------------------------------
curr_row += 1

#  0  +++++++++++++++++++++++++++++++++++++++
lab_R0 = Label(frm_all, text=u'R1')
lab_R0.grid(row=curr_row, column=0, sticky="e")

#  2  +++++++++++++++++++++++++++++++++++++++


def ev_cbb_nr0(_):
    """  """
    j = cbb_dR0.current()
    n = cbb_nR0.current()
    old_cbb_nRji[j][0] = n
    if chb_RX_var.get():
        cbb_nR1.set(cbb_nR0.get())

cbb_nR0 = Combobox(frm_all, width=7)
cbb_nR0.grid(row=curr_row, column=2)
cbb_nR0.bind('<<ComboboxSelected>>', ev_cbb_nr0)

#  1  +++++++++++++++++++++++++++++++++++++++


def ev_cbb_dr0(_):
    """  """
    j = cbb_dR0.current()
    old_cbb_dRi[0] = j
    cbb_nR0['values'] = ['%i' % n
                         for k, n in enumerate(list_nRX)
                         if k <= j and (cbb_dR0.get() != '1 %' or not chb_E24_1_var.get() or k <= IND_5)]

    if old_cbb_nRji[j][0] >= len(cbb_nR0['values']):
        cbb_nR0.current(len(cbb_nR0['values'])-1)
    else:
        cbb_nR0.current(old_cbb_nRji[j][0])

    if chb_RX_var.get():
        cbb_dR1.set(cbb_dR0.get())
        cbb_nR1.set(cbb_nR0.get())

cbb_dR0 = Combobox(frm_all, width=7, )
cbb_dR0.grid(row=curr_row, column=1)
cbb_dR0.bind('<<ComboboxSelected>>', ev_cbb_dr0)
#------------------------------------------------------------------------------
curr_row += 1

#  0  +++++++++++++++++++++++++++++++++++++++
lab_R1 = Label(frm_all, text=u'R2')
lab_R1.grid(row=curr_row, column=0, sticky="e")


#  2  +++++++++++++++++++++++++++++++++++++++
def ev_cbb_nr1(_):
    """  """
    j = cbb_dR1.current()
    m = cbb_nR1.current()
    old_cbb_nRji[j][1] = m

cbb_nR1 = Combobox(frm_all, width=7)
cbb_nR1.grid(row=curr_row, column=2)
cbb_nR1.bind('<<ComboboxSelected>>', ev_cbb_nr1)


#  1  +++++++++++++++++++++++++++++++++++++++
def ev_cbb_dr1(_):
    """  """
    j = cbb_dR1.current()
    old_cbb_dRi[1] = j

    cbb_nR1['values'] = ['%i' % n
                         for k, n in enumerate(list_nRX)
                         if k <= j and (cbb_dR1.get() != '1 %' or not chb_E24_1_var.get() or k <= IND_5)]

    if old_cbb_nRji[j][1] >= len(cbb_nR1['values']):
        cbb_nR1.current(len(cbb_nR1['values'])-1)
    else:
        cbb_nR1.current(old_cbb_nRji[j][1])


cbb_dR1 = Combobox(frm_all, width=7, )
cbb_dR1.grid(row=curr_row, column=1)
cbb_dR1.bind('<<ComboboxSelected>>', ev_cbb_dr1)
#..............................................................................


#------------------------------------------------------------------------------
curr_row += 1

lab_U0X = Label(frm_all, text=u'U опорное')
lab_U0X.grid(row=curr_row, column=0, columnspan=2)

lab_dU0X = Label(frm_all, text=u'допуск')
lab_dU0X.grid(row=curr_row, column=2)

#------------------------------------------------------------------------------
curr_row += 1

#  1  +++++++++++++++++++++++++++++++++++++++
ent_U0_var = StringVar(value=old_ent_U0)
ent_U0 = Entry(frm_all, width=10, textvariable=ent_U0_var)
ent_U0.grid(row=curr_row, column=1)


#  2  +++++++++++++++++++++++++++++++++++++++
def ev_cbb_du0(_):
    global old_cbb_dU0
    old_cbb_dU0 = cbb_dU0.current()

cbb_dU0 = Combobox(frm_all, width=7, )
cbb_dU0.grid(row=curr_row, column=2)
cbb_dU0.bind('<<ComboboxSelected>>', ev_cbb_du0)

#------------------------------------------------------------------------------
curr_row += 1

lab_U1X = Label(frm_all, text=u'U выходное')
lab_U1X.grid(row=curr_row, column=0, columnspan=2)

lab_dU1X = Label(frm_all, text=u'Фильтр')
lab_dU1X.grid(row=curr_row, column=2)

#------------------------------------------------------------------------------
curr_row += 1

#  1  +++++++++++++++++++++++++++++++++++++++
ent_U1_var = StringVar(value=old_ent_U1)
ent_U1 = Entry(frm_all, width=10, textvariable=ent_U1_var)
ent_U1.grid(row=curr_row, column=1)


#  2  +++++++++++++++++++++++++++++++++++++++
def ev_cbb_du1(_):
    global old_cbb_dU1
    old_cbb_dU1 = cbb_dU1.current()

cbb_dU1 = Combobox(frm_all, width=7, )
cbb_dU1.grid(row=curr_row, column=2)
cbb_dU1.bind('<<ComboboxSelected>>', ev_cbb_du1)

#------------------------------------------------------------------------------
curr_row += 1

#  1  +++++++++++++++++++++++++++++++++++++++
btn_CLR = Button(frm_all, text='Очистить', width=9, command=cmd_btn_clr)
btn_CLR.grid(row=curr_row, column=1)
btn_CLR.bind('<Button-1>')
#btn_CLR.bind("<Escape>")

#  2  +++++++++++++++++++++++++++++++++++++++
btn_OK = Button(frm_all, text='Оk', width=9, command=cmd_btn_ok)
btn_OK.grid(row=curr_row, column=2, padx=5, pady=5)
btn_OK.bind('<Button-1>')
#btn_OK.bind("<Return>")
#..............................................................................

#------------------------------------------------------------------------------
curr_row += 1


#------------------------------------------------------------------------------
def cmd_rb_mode():
    """  """
    global photo
    if rb_mode_var.get() >= 2:
        lab_U0X['text'] = ''
        lab_dU0X['text'] = ''
        lab_U1X['text'] = u'R необходимое'
        cbb_dU0.set('')
        ent_U0_var.set('')
        cbb_dU0['state'] = DISABLED
        ent_U0['state'] = DISABLED
    else:
        lab_U0X['text'] = u'U опорное'
        lab_dU0X['text'] = u'Допуск'
        lab_U1X['text'] = u'U выходное'
        cbb_dU0.current(old_cbb_dU0)
        ent_U0_var.set(old_ent_U0)
        cbb_dU0['state'] = NORMAL
        ent_U0['state'] = NORMAL

    photo = PhotoImage(file=photo_files[rb_mode_var.get()])
    lab_image['image'] = photo
#..............................................................................


#------------------------------------------------------------------------------
rb_mode_var = IntVar(value=old_rb_mode)
for i, t in enumerate(modes):
    rb_mode = Radiobutton(
        frm_mode, text=t, value=i,
        command=cmd_rb_mode, variable=rb_mode_var)
    rb_mode.grid(row=i, sticky="w")
    rb_mode.bind('<Button-1>')

lab_image = Label(frm_mode, text=u'image')
lab_image.grid(row=len(modes), padx=2, pady=2)
#..............................................................................

set_old_values()

prn_only = False
root.mainloop()
# noinspection PyRedeclaration
prn_only = True


save_old_values()
