# -*- coding: utf-8 -*-

# Коментарий к модулю

from common import printm

#-------------------------------------------------------------------------------
mantises = {
    24: (100.0, 110.0, 120.0, 130.0, 150.0, 160.0, 180.0, 200.0, 220.0, 240.0, 270.0, 300.0,
         330.0, 360.0, 390.0, 430.0, 470.0, 510.0, 560.0, 620.0, 680.0, 750.0, 820.0, 910.0, ),
    192: (100.0, 101.0, 102.0, 104.0, 105.0, 106.0, 107.0, 109.0, 110.0, 111.0, 113.0, 114.0,
          115.0, 117.0, 118.0, 120.0, 121.0, 123.0, 124.0, 126.0, 127.0, 129.0, 130.0, 132.0,
          133.0, 135.0, 137.0, 138.0, 140.0, 142.0, 143.0, 145.0, 147.0, 149.0, 150.0, 152.0,
          154.0, 156.0, 158.0, 160.0, 162.0, 164.0, 165.0, 167.0, 169.0, 172.0, 174.0, 176.0,
          178.0, 180.0, 182.0, 184.0, 187.0, 189.0, 191.0, 193.0, 196.0, 198.0, 200.0, 203.0,
          205.0, 208.0, 210.0, 213.0, 215.0, 218.0, 221.0, 223.0, 226.0, 229.0, 232.0, 234.0,
          237.0, 240.0, 243.0, 246.0, 249.0, 252.0, 255.0, 258.0, 261.0, 264.0, 267.0, 271.0,
          274.0, 277.0, 280.0, 284.0, 287.0, 291.0, 294.0, 298.0, 301.0, 305.0, 309.0, 312.0,
          316.0, 320.0, 324.0, 328.0, 332.0, 336.0, 340.0, 344.0, 348.0, 352.0, 357.0, 361.0,
          365.0, 370.0, 374.0, 379.0, 383.0, 388.0, 392.0, 397.0, 402.0, 407.0, 412.0, 417.0,
          422.0, 427.0, 432.0, 437.0, 442.0, 448.0, 453.0, 459.0, 464.0, 470.0, 475.0, 481.0,
          487.0, 493.0, 499.0, 505.0, 511.0, 517.0, 523.0, 530.0, 536.0, 542.0, 549.0, 556.0,
          562.0, 569.0, 576.0, 583.0, 590.0, 597.0, 604.0, 612.0, 619.0, 626.0, 634.0, 642.0,
          649.0, 657.0, 665.0, 673.0, 681.0, 690.0, 698.0, 706.0, 715.0, 723.0, 732.0, 741.0,
          750.0, 759.0, 768.0, 777.0, 787.0, 796.0, 806.0, 816.0, 825.0, 835.0, 845.0, 856.0,
          866.0, 876.0, 887.0, 898.0, 909.0, 920.0, 931.0, 942.0, 953.0, 965.0, 976.0, 988.0, ),
}
#-------------------------------------------------------------------------------
modes = [u'делителя',
         u'по отношению U (или R)',
         u'послед соединения',
         u'пар соединения',
         u'посл или пар соединения ', ]
list_nRX = (3, 6, 12, 24, 48, 96, 192)
list_dRX = ['50 %', '20 %', '10 %', '5 %', '2 %', '1 %', '0.5 %', '0.25 %', '0.1 %']
IND_1 = list_dRX.index('1 %')
IND_5 = list_dRX.index('5 %')
IND_24 = list_nRX.index(24)
p = None


#------------------------------------------------------------------------------
def calc(mode, u0, du0, u1, du1, dr0, nr0, dr1, nr1, e24_1):
    """  """
    global ms_r0, ms_r1

    if mode < 2:
        #u0 = float(u0.replace(',', '.'))
        du0 = float(du0[:-2]) / 100.0
    #u1 = float(u1.replace(',', '.'))
    du1 = float(du1[:-2]) / 100.0

    ind_dr0 = list_dRX.index(dr0)
    ind_dr1 = list_dRX.index(dr1)
    dr0 = float(dr0[:-2]) / 100.0
    dr1 = float(dr1[:-2]) / 100.0

    nr0 = int(nr0)
    nr1 = int(nr1)

    if (e24_1 > 0) and (ind_dr0 == IND_1):
        ms_r0 = mantises[24][::24 // nr0]
    elif ind_dr0 > IND_5:
        ms_r0 = mantises[192][::192 // nr0]
    else:
        ms_r0 = mantises[24][::24 // nr0]

    if (e24_1 > 0) and (ind_dr1 == IND_1):
        ms_r1 = mantises[24][::24 // nr1]
    elif ind_dr1 > IND_5:
        ms_r1 = mantises[192][::192 // nr1]
    else:
        ms_r1 = mantises[24][::24 // nr1]

    printm(u'\n')
    printm(u'Рассчёт %s' % modes[mode])
    printm(u'\n')

    if mode == 0:
        printm(u'\n')
        calc_div(u0, du0, u1, du1, dr0, dr1, one=1.0)
        return
    if mode == 1:
        printm(u'\n')
        calc_div(u0, du0, u1, du1, dr0, dr1, one=0.0)
        return

    ps_rx = range(-4, 6)
    ms_r0 = [m * 10 ** ip for ip in ps_rx for m in ms_r0]
    ms_r1 = [m * 10 ** ip for ip in ps_rx for m in ms_r1]

    if mode == 2:
        calc_comb(u1, du1, dr0, dr1, c='+')
        return
    if mode == 3:
        calc_comb(u1, du1, dr0, dr1, c='#')
        return
    if mode == 4:
        calc_comb(u1, du1, dr0, dr1, c='+#')
        return
#..............................................................................


#-------------------------------------------------------------------------------
def mant_pow(x):
    px = 0
    while x >= 1.0:
        x /= 10.0
        px += 1
    while x < 0.1:
        x *= 10.0
        px -= 1
    return x, px
#..............................................................................


#-------------------------------------------------------------------------------
def god_var(r0, r1, dp):
    if p + dp > 0:
        r0 *= 10 ** (p + dp)
    if p + dp < 0:
        r1 /= 10 ** (p + dp)
    k = r0 / r1 + one1
    if flag_div and one1 == 1.0:
        k = 1 / k
    return [abs((k - knom) / knom), r0, r1]
#..............................................................................


#-------------------------------------------------------------------------------
def calc_comb(rx, drx, dr0, dr1, c='+#'):
    """  """
    fp = lambda a0, a1: a0 * a1 / (a0 + a1)
    fs = lambda a0, a1: a0 + a1

    rmin = rx * (1 - drx)
    rmax = rx * (1 + drx)

    rez = set()

    for vi, r0 in enumerate(ms_r0):
        for r1 in ms_r1:

            if '+' in c and rmin < fs(r0, r1) < rmax:
                if dr0 == dr1 and r0 < r1:
                    r0, r1 = r1, r0
                r = fs(r0, r1)
                rez.add(((r - rx) / rx, r0, '+', r1,
                        fs(r0 * (1 - dr0), r1 * (1 - dr1)),
                        r,
                        fs(r0 * (1 + dr0), r1 * (1 + dr1))))

            if '#' in c and rmin < fp(r0, r1) < rmax:
                if dr0 == dr1 and r0 > r1:
                    r0, r1 = r1, r0
                r = fp(r0, r1)
                rez.add(((r - rx) / rx, r0, '#', r1,
                        fp(r0 * (1 - dr0), r1 * (1 - dr1)),
                        r,
                        fp(r0 * (1 + dr0), r1 * (1 + dr1))))
        if not vi % 25:
            printm(u'.')

    printm(u'\n')
    printm(u'\n')

    if not rez:
        printm(u'Не смогло подобрать значений удовлетроряющих требованиям.\n')
        return

    # Фильтруем дубликаты по Ri
    for i in (1, 3):
        tmp = -1
        for x in sorted(rez, key=lambda y: (y[i], abs(y[0]))):
            if tmp != x[i]:
                tmp = x[i]
                continue
            rez.remove(x)

    # Строим шапку
    printm(u'Найдено %s значений удовлетроряющих требованиям.\n' % len(rez))
    printm(u'Точность')
    printm(u'       Резисторы         ')
    printm(u'       Значения сопротивления\n')
    printm(u' комбин.')
    printm(u'        R1   R2          ')
    printm(u'       min      средина   max       \n')

    for x in sorted(rez, key=lambda y: (abs(y[0]), y[1])):

        printm(u'%6.2g %%' % round(x[0] * 100.0, 2))
        printm(u'%10s %s %-10s  ' % (compact(x[1]), x[2],
                                     compact(x[3])))
        printm(u'%10s   %10s   %-10s\n' % (compact(x[4]),
                                           compact(x[5]),
                                           compact(x[6])))
#...............................................................................


#-------------------------------------------------------------------------------
def compact(x, d=3):
    """  """
    s = '%.*e' % (d, x)
    m, p = s.split('e')
    p = int(p)
    i, f = m.split('.')
    while f.endswith('0'):
        f = f[:-1]
    p3, p = divmod(p, 3)
    L = {-1:'m', 0:'.', 1:'K', 2:'M'}[p3]
    if p == 0:
        s = i + L + f
    elif p == 1:
        if f[:1]:
            s = i + f[:1] + L + f[1:]
        else:
            s = i + '0' + L
    elif p == 2:
        if len(f[:2]) == 2:
            s = i + f[:2] + L + f[2:]
        elif len(f[:2]) == 1:
            s = i + f[:2] + '0' + L
        else:
            s = i + '00' + L
    if s.endswith('.'):
        s = s[:-1]
    return s
#...............................................................................


#-------------------------------------------------------------------------------
def calc_div(u0, du0, u1, du1, dr0, dr1, one=1.0):
    """  """
    global knom, flag_div, p, one1
    one1 = one

    knom = u1 / u0
    flag_div = knom < 1.0
    kmin = knom * (1 - du1)
    kmax = knom * (1 + du1)

    if flag_div and one1 == 1.0:
        rmin = 1 / kmax - one1
        rmax = 1 / kmin - one1
    else:
        rmin = kmin - one1
        rmax = kmax - one1

    mmin, p = mant_pow(rmin)
    mmax = rmax / 10 ** p

    rez = []
    # Для одинаковых значений
    if mmin < 1.0 < mmax:
        rez.append(god_var(444.0, 444.0, 0))

    # Для разных значений
    for r0 in ms_r0:
        for r1 in ms_r1:
            r = r0 / r1
            if r0 != r1:
                if mmin < r < mmax:
                    rez.append(god_var(r0, r1, 0))
            if r0 < r1:
                if mmin < 10.0 * r < mmax:
                    rez.append(god_var(r0, r1, 1))
            if r0 > r1:
                if mmin < 0.1 * r < mmax:
                    rez.append(god_var(r0, r1, -1))

    if not rez:
        printm(u'Не смогло подобрать значений удовлетроряющих требованиям.\n')
        return

    # Строим шапку
    printm(u'Найдено %s значений удовлетроряющих требованиям.\n' % len(rez))
    printm(u'  Точность  ')
    printm(u'    Резисторы     ')
    printm(u'    Значения напряжения \n')
    printm(u'коэффициента')
    printm(u'      R1  R2      ')
    printm(u'     min  средина   max\n')

    for x in sorted(rez):
        kmit = x[1] / x[2] + one1
        kmin = x[1] / x[2] * (1 - dr0) / (1 + dr1) + one1
        kmax = x[1] / x[2] * (1 + dr0) / (1 - dr1) + one1

        if flag_div and one1 == 1.0:
            kmit = 1 / kmit
            kmin, kmax = 1 / kmax, 1 / kmin

        u_mit = kmit * u0
        u_min = kmin * u0 * (1 - du0)
        u_max = kmax * u0 * (1 + du0)

        printm(u'%6.2g %%    ' % round((kmit - knom) / knom * 100.0, 2))
        if x[1] == x[2] == 444.0:
            printm(u'       R  R       ')
        else:
            r0 = u'%g' % x[1]
            r1 = u'%g' % x[2]
            while r0[-1] == r1[-1] == u'0':
                r0 = r0[:-1]
                r1 = r1[:-1]
            r0 = compact(float(r0))
            r1 = compact(float(r1))
            if one1 == 1.0:
                printm(u'%8s  %-8s' % (r0, r1))
            else:
                printm(u'%8s  %-8s' % (r1, r0))
        printm(u'%8.4g  %s  %-8.4g\n' % (u_min, ('%.4g' % u_mit).center(8), u_max))
#...............................................................................


