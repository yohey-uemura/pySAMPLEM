from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog


import os, sys, re, math
import numpy as np


NATOM = 86
f = open('MCMASTERe.D')
FMcMS = f.readlines()
E = np.array([float(x) for x in FMcMS[0].split()] + [float(x) for x in FMcMS[1].split()])
ATOMB = []
AMAS = {}
EDGE = {}
RMUEA = {}
RMUEB = {}
RMUE = {}
for I in range(86):
    ATOMB.append(FMcMS[2+(7*I+1)].split()[0])
    
    AMAS[ATOMB[-1]] = float(FMcMS[2+(7*I+1)].split()[1])
    EDGE[ATOMB[-1]] = np.array([float(x) for x in FMcMS[2+(7*I+2)].split()])
    RMUEA[ATOMB[-1]] = np.array([float(x) for x in FMcMS[2+(7*I+3)].split()])
    RMUEB[ATOMB[-1]] = np.array([float(x) for x in FMcMS[2+(7*I+4)].split()])
    RMUE[ATOMB[-1]] = np.array([float(x) for x in FMcMS[2+(7*I+5)].split()] + \
                      [float(x) for x in FMcMS[2+(7*I+6)].split()])


################ GUI ############################
win = Tk()
win.title("pySAMPLEM")
ELMAX=20

def show_info():
    txt = "{:^40s}".format("pySAMPLEM\n")
    txt +="{:>40s}".format("based on SAMPLEM.FOR  (V1.0)\n")
    txt +="{:>40s}".format("BY NOMURA, M. (1993)")
    messagebox.showinfo(title="pySAMPLEM: estimation of the sample amout of XAFS", message=txt)
    
menubar = Menu(win)
menu0 = Menu(menubar, tearoff=0)
menu0.add_command(label="About...", command=show_info)
menu0.add_separator()
menubar.add_cascade(label="Help", menu=menu0)

var_edge = IntVar()
f0 = Frame(win)
f = LabelFrame(f0,text='Edge')
edges = ['K', 'L1', 'L2', 'L3']
for i in range(4):
    Radiobutton(f,text=edges[i], width=4, variable=var_edge, value=i).pack(side=LEFT)
f.pack(side=LEFT,padx=10,anchor="w")

f = LabelFrame(f0,text='DENSITY')
d = Entry(f, width=5)
Label(f, text="d [g/cm^3]", font=('Arial 12'),width=8).pack(side=LEFT, anchor="w")
d.insert(0,'{:.1f}'.format(1.0))
d.pack(side=LEFT)
f.pack(side=TOP,padx=0,anchor="w")
f0.pack(side=TOP)

f0 = Frame(win)

vars_opt = []
fopt = LabelFrame(f0,text='OPTIONS (T [mm])')
for i in range(2):
    opt = Entry(fopt, width=7)
    vars_opt.append(opt)
    opt.pack(side=LEFT)

fopt.pack(side=RIGHT)

    
var_calc = IntVar()
f = LabelFrame(f0,text='TYPE')
CALCTYPE = ['T [mm]','W[mg]']
_rbs = []
for i in range(2):
    _rb = Radiobutton(f,text=CALCTYPE[i], width=8,
                variable=var_calc, value=i,
                )
    _rbs.append(_rb)
    _rb.pack(side=LEFT)

def setLabel():
    txt = 'OPTIONS (T [mm])'*(var_calc.get()==0)+'OPTIONS (W [mg])'*(var_calc.get()==1)
    fopt.configure(text=txt)
    if var_calc.get()==1:
        d.delete(0, END)
        d.insert(0,1.0)
        d.config(state='disabled')
    elif var_calc.get()==0:
        d.config(state='normal')

for _rb in _rbs:
    _rb.configure(command=setLabel)
    
f.pack(side=RIGHT,padx=0,anchor="w")

f0.pack(side=TOP)

val_cbs = []
entry_elms = []
entry_ratio = []
var_rb = IntVar()

f0 = LabelFrame(win,text='CONDITIONS')
f = Frame(f0)
Label(f, text="NUM", font=('Arial 12'),width=5).pack(side=LEFT, anchor="w")
Label(f, text="element", font=('Arial 12'),width=10).pack(side=LEFT)
Label(f, text="ratio", font=('Arial 12'),width=10).pack(side=LEFT)
Label(f, text="Absorber", font=('Arial 12'),width=15).pack(side=LEFT)
f.pack(side=TOP,padx=0,anchor="w")

container = Frame(f0)
scrollbar = Scrollbar(container, orient="vertical")
canvas = Canvas(container,height=220)
scrollable_frame = ttk.Frame(canvas)
scrollbar.config(command = canvas.yview)                      
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

for i in range(ELMAX):
    f = Frame(scrollable_frame)
    val_cbs.append(IntVar(win,1*(i==0)))
    Checkbutton(f, text = "{:>02d}:".format(i+1), variable = val_cbs[-1], \
                 onvalue = 1, offvalue = 0, height=1, \
                 width = 5).pack(side=LEFT)
    a=Entry(f, width=8)
    entry_elms.append(a)
    if i==0:
        a.insert(0,'CU')
    a.pack(side=LEFT)
    b=Entry(f, width=10)
    if i==0:
        b.insert(0,'{:.1f}'.format(1.0))
    entry_ratio.append(b)
    b.pack(side=LEFT)

    Radiobutton(f,text="", width=5, variable=var_rb, value=i).pack(side=LEFT)

    f.pack(side=TOP)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side = LEFT,fill="both", expand=True)
container.pack(side=TOP)
scrollbar.pack(side=RIGHT,fill='y')

f0.pack(side=TOP)
    
f0 = LabelFrame(win,text='RESULTS')
text = Text(f0,width=55,height=12,font=('Arial 12'))
text.pack(side=TOP)
f0.pack(side=BOTTOM)

def saveText():
    txt = text.get("1.0",END)
    fname = filedialog.asksaveasfilename()
    if fname:
        f = open(fname,'w')
        for l in txt:
            f.write(l)
    else:
        messagebox.showwarning(title="NO FILE SPECIFIED", message="Please specify the file to save")

rclickmenu = Menu(text, tearoff = 0)
rclickmenu.add_command(label ="Save", command = saveText)

  
def do_popup(event):
    try:
        rclickmenu.tk_popup(event.x_root, event.y_root)
    finally:
        rclickmenu.grab_release()
  
text.bind("<Button-2>", do_popup)

def victreen(engs,coeffs,e0):
    Eb= e0/2.5
    Ea= e0*2.5
    
    # print (12398.52/engs[(engs>=Eb)*(engs<=Ea)])
    # print (coeffs[(engs>=Eb)*(engs<=Ea)])
    
    # for i, _e in enumerate(engs[(engs>=Eb)*(engs<=Ea)]):
    #     print ('{:d}, {:.1f}, {:.5f}'.format(i+1,_e,coeffs[(engs>=Eb)*(engs<=Ea)][i]))
    
    X1 = (12398.52/engs[(engs>=Eb)*(engs<=Ea)])**6
    Y1 = (12398.52/engs[(engs>=Eb)*(engs<=Ea)])**7
    Y2 = (12398.52/engs[(engs>=Eb)*(engs<=Ea)])**8
    
    # print (X1.sum(), Y1.sum(), Y2.sum())
    
    CE1 = coeffs[(engs>=Eb)*(engs<=Ea)]*(12398.52/engs[(engs>=Eb)*(engs<=Ea)])**3
    CE2 = coeffs[(engs>=Eb)*(engs<=Ea)]*(12398.52/engs[(engs>=Eb)*(engs<=Ea)])**4
    
    
    # print (">>>> CE1, CE2: "+"{:f}, {:f}".format(CE1.sum(),CE2.sum()))

    
    A3 = (CE1.sum()*Y2.sum()-CE2.sum()*Y1.sum())/(X1.sum()*Y2.sum()-Y1.sum()*Y1.sum())
    A4 = (CE1.sum()*Y1.sum()-CE2.sum()*X1.sum())/(Y1.sum()*Y1.sum()-X1.sum()*Y2.sum())
    
    # print (A3, A4)
    
    return A3*(12398.52/e0)**3+A4*(12398.52/e0)**4
    
def calc():
    text.delete('1.0', END)
    INPUT = {
    ########INPUT ATOMIC RATIO#########
        'RATIO' :{},
    ########INPUT ABSORBER ########
        'ABS': '',
    #######   EDGE (K: 0, L1: 1, L2: 2, L3: 3) ######
        'EDGE': 0,
    ####### DENSITY g/cm^3 #######
        'DENS': 1.0,
    ####### OPTIONS #######
        'OPTIONS': [],
    }
    try:
        print (d.get())
        INPUT['DENS'] = float(d.get())
        INPUT['EDGE'] = var_edge.get()
        for i in range(ELMAX):
            if val_cbs[i].get():
                el = entry_elms[i].get().rstrip().replace(' ','').upper()
                r = entry_ratio[i].get().rstrip().replace(' ','')
                if not (el in ATOMB):
                    messagebox.showwarning(title="NOT FOUND", message="please check the symbol of the element {:02d}".format(i+1))
                    break
                if not (re.match('^\d+(\.\d+)?$',r)):
                    messagebox.showwarning(title="NOT A VALUE: RATIO", message="please check the ratio of the element {:02d}".format(i+1))
                    break
                INPUT['RATIO'][el] = float(r)
                if var_rb.get() == i:
                    INPUT['ABS'] = el

        for i, _entry in enumerate(vars_opt):
            print (_entry)
            if (re.match('^\d+(\.\d+)?$',_entry.get().rstrip())):
                INPUT['OPTIONS'].append(float(_entry.get().rstrip()))
                
                    
        if INPUT['ABS'] =='':
            messagebox.showwarning(title="NO ABSORBER", message="Please select the correct absorber")
        else:
            results = {
                'rmu': np.array([]),
                'rmass': np.array([])
            }

            for EL in INPUT['RATIO'].keys():
                if EL == INPUT['ABS']:
                    results['rmu'] = np.append(results['rmu'],RMUEB[EL][INPUT['EDGE']]*AMAS[EL]*INPUT['RATIO'][EL])
                    results['rmass'] = np.append(results['rmass'],AMAS[EL]*INPUT['RATIO'][EL])
                    print ('{:s}, {:.5f}'.format(EL, RMUEB[EL][INPUT['EDGE']]*AMAS[EL]*INPUT['RATIO'][EL]))
                else:
                    #### Above K edge ####
                    if EDGE[INPUT['ABS']][INPUT['EDGE']] > EDGE[EL][0]:
                        arrEng = np.append(E,EDGE[EL][EDGE[EL]>100])
                        coeffs = np.append(RMUE[EL],RMUEA[EL][EDGE[EL]>100])
                        c = victreen(arrEng,coeffs,EDGE[INPUT['ABS']][INPUT['EDGE']])
                        print ('{:s}, {:.5f}'.format(EL, c))

                    elif EDGE[INPUT['ABS']][INPUT['EDGE']] < EDGE[EL][3]:
                        arrEng = np.append(E,EDGE[EL][EDGE[EL]>100]-100)
                        coeffs = np.append(RMUE[EL],RMUEB[EL][EDGE[EL]>100])
                        c = victreen(arrEng,coeffs,EDGE[INPUT['ABS']][INPUT['EDGE']])
                        print ('{:s}, {:.5f}'.format(EL, c))
                    else:
                        arrEng = np.append(E,EDGE[EL][EDGE[EL]>100])
                        arrEng = np.append(arrEng,EDGE[EL][EDGE[EL]>100]-100)
                        coeffs = np.append(RMUE[EL],RMUEA[EL][EDGE[EL]>100])
                        coeffs = np.append(coeffs,RMUEA[EL][EDGE[EL]>100])
                        c = victreen(arrEng,coeffs,EDGE[INPUT['ABS']][INPUT['EDGE']])
                        print ('{:s}, {:.5f}'.format(EL, c))

                    results['rmu'] = np.append(results['rmu'],c*AMAS[EL]*INPUT['RATIO'][EL])
                    results['rmass'] = np.append(results['rmass'],AMAS[EL]*INPUT['RATIO'][EL])

            xabs = (results['rmu'].sum()+((RMUEA[INPUT['ABS']][INPUT['EDGE']]-RMUEB[INPUT['ABS']][INPUT['EDGE']])*AMAS[INPUT['ABS']]*INPUT['RATIO'][INPUT['ABS']]))\
                /results['rmass'].sum()
            bg =  (results['rmu'].sum())/results['rmass'].sum()

            ####### Display the results ######
            arrSTRINGS = []

            _txt = ''
            for EL in INPUT['RATIO'].keys():
                _txt += '{:>5s}: '.format(EL) + '{:>.2f}, '.format(INPUT['RATIO'][EL])
            arrSTRINGS.append('{:^60s}'.format(">>>>>"*4+'  CONDITIONS  '+"<<<<<"*4))
            arrSTRINGS.append('{:<60s}'.format("     * COMPOSITION: "+_txt[:-2]))
            arrSTRINGS.append('{:<60s}'.format("     * DENSITY [g/cm^3]: "+str(INPUT['DENS'])))
            arrSTRINGS.append('{:<60s}'.format("     * ABSORBER, EDGE: "+INPUT['ABS']+', '+edges[INPUT['EDGE']]+'\n'))
            arrSTRINGS.append('{:^60s}'.format("#"*21+"  RESULTS  "+"#"*25))
            _txt = ''
            for x in ["Low ut", "High ut", "Delta ut", "Thickness [mm]"*(var_calc.get()==0)+"Weight [mg]"*(var_calc.get()==1)]:
                _txt += '{:^15s}'.format(x)
            arrSTRINGS.append('{:^60s}'.format(_txt))
            power = (var_calc.get()==0)*1 +(var_calc.get()==1)*3
            ####### Hight ut = 4 ######
            T1 = 4.0/(xabs*INPUT['DENS'])
            low_ut = (bg*INPUT['DENS'])*T1
            high_ut = 4.0
            Delta = high_ut - low_ut

            _txt = ''
            for x in [low_ut, high_ut, Delta, T1*10**power]:
                _txt += '{:^15.3f}'.format(x)
            arrSTRINGS.append('{:^60s}'.format(_txt))

            ####### Hight ut = 2.55 ######
            T1 = 2.55/(xabs*INPUT['DENS'])
            low_ut = (bg*INPUT['DENS'])*T1
            high_ut = 2.55
            Delta = high_ut - low_ut

            _txt = ''
            for x in [low_ut, high_ut, Delta, T1*10**power]:
                _txt += '{:^15.3f}'.format(x)
            arrSTRINGS.append('{:^60s}'.format(_txt))

            ####### DELTA ut = 1.0 ######
            Delta = 1.0
            T1 = Delta/(xabs*INPUT['DENS']-bg*INPUT['DENS'])
            low_ut = (bg*INPUT['DENS'])*T1
            high_ut = xabs*INPUT['DENS']*T1

            _txt = ''
            for x in [low_ut, high_ut, Delta, T1*10**power]:
                _txt += '{:^15.3f}'.format(x)
            arrSTRINGS.append('{:^60s}'.format(_txt))

            arrSTRINGS.append('  {:^60s}'.format('-'*58))

            if len(INPUT['OPTIONS']) > 0:
                for x in INPUT['OPTIONS']:

                    T1 = x/10**power
                    low_ut = (bg*INPUT['DENS'])*T1
                    high_ut = xabs*INPUT['DENS']*T1
                    Delta = high_ut - low_ut
                    _txt = ''
                    for _x in [low_ut, high_ut, Delta, x]:
                        _txt += '{:^15.3f}'.format(_x)
                    arrSTRINGS.append('{:^60s}'.format(_txt))

            arrSTRINGS.append('{:^60s}'.format('#'*55))
            txt = ''
            for l in arrSTRINGS:
                txt += l+'\n'
            text.insert(INSERT,txt[:-1])
            # messagebox.showinfo(title="RESAULTS", message=txt[:-1])
    except Exception as e:
        print (e)
        messagebox.showwarning(title="NOT A VALUE: DENSITY", message="Please check the value of the density")
    #messagebox.showinfo(title="RESULTS", message="TEST")
    

f = Frame(win)
pB = Button(f,text="calculate",width=10,command=calc)
pB.pack(side=RIGHT)
f.pack(side=TOP)

win.config(menu=menubar)
win.mainloop()
