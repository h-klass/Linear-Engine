import numpy as np
import tkinter as tk

# check is string contains valid numerical signs
def is_num(num):
    try:
        if isinstance(float(num),float) or num == "":
            return True
    except:
        if num == "" or num == "-":
            return True
        else:
            return False

# main menu process
def menuHandler():
    # initialize tkinker window
    root = tk.Tk()
    root.title = "Vector and Matrix input window"

    # declare frames (in descending order of nested)
    menu = tk.Frame(root)
    vectormenu = tk.Frame(menu)
    matrixmenu = tk.Frame(menu)

    # menu variables
    ventriesvar = [tk.StringVar() for n in range(3)]
    addvectorvar = tk.BooleanVar()
    addvectorvar.set(False)
    mentriesvar = [tk.StringVar() for i in range(9)]
    for i in range(3):
        ventriesvar[i].set(1)
    for i in range(9):
        if i==0 or i==4 or i==8:
            mentriesvar[i].set(1)
        else:
            mentriesvar[i].set(0)
    setmatrixvar = tk.BooleanVar()
    setmatrixvar.set(False)
    intvalidation = root.register(is_num)

    # menu widget declarations
    ventries = [tk.Entry(vectormenu,textvariable=ventriesvar[n],width=2,validate='key',validatecommand=(intvalidation,'%P')) for n in range(3)]
    labelvector = tk.Label(vectormenu, text='Configure Vector')
    addvectorbutton = tk.Button(vectormenu, text="Add Vector", command= lambda: addvectorvar.set(True))
    mentries = [tk.Entry(matrixmenu,textvariable=mentriesvar[n],width=2,validate='key',validatecommand=(intvalidation,'%P')) for n in range(9)]
    labelmatrix = tk.Label(matrixmenu,text='Configure Matrix')
    setmatrixbutton = tk.Button(matrixmenu, text="Set Matrix", command= lambda: setmatrixvar.set(True))

    # menu widget placement
    menu.grid(column=0,row=0)
    vectormenu.grid(column=1,row=0,sticky="n")
    labelvector.grid(column=0,row=0)
    for n in range(3):
        ventries[n].grid(column=0,row=(n+1))
    addvectorbutton.grid(column=0,row=4)
    matrixmenu.grid(column=2,row=0,sticky="n")
    labelmatrix.grid(column=0,row=0,columnspan=3)
    for n in range(9):
        mentries[n].grid(column=np.mod(n,3),row=int(np.floor(n/3))+1)
    setmatrixbutton.grid(column=1,row=4)

    # return vectors and matrices and if they should be updated
    outvector = []
    def addvector(*args):
        vectortemp = [0 for i in range(3)]
        for n in range(3):
            vectortemp[n] = float(ventriesvar[n].get())
            ventriesvar[n].set(0)
        outvector.append(vectortemp)
    addvectorvar.trace_add("write", addvector)
    root.mainloop()
    outmatrix = [[0 for i in range(3)] for j in range(3)]
    for n in range(9):
        outmatrix[int(np.floor(n/3))][np.mod(n,3)] = float(mentriesvar[n].get())
    return outvector,outmatrix,[addvectorvar.get(),setmatrixvar.get()]