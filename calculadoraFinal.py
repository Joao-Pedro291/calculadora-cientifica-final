import tkinter as tk
from tkinter import simpledialog
import math
import random
from fractions import Fraction
import re

janela = tk.Tk()
janela.title("Calc")
janela.configure(bg="black")

caixaCalc = tk.Entry(janela, font=("Arial", 20), justify="right", width=20, bd=5, relief="sunken")
caixaCalc.insert(0, "0")
caixaCalc.grid(row=0, column=0, columnspan=6, pady=15, padx=5)

frame_cientifico = tk.Frame(janela, bg="black")
frame_cientifico.grid(row=1, column=0, columnspan=6)
frame_normal = tk.Frame(janela, bg="black")
frame_normal.grid(row=2, column=0, columnspan=6)

shift_ativo = False
ultimo_resultado = 0
hyp_ativo = False
shift_labels = {"1": "s-sum", "2": "s-var", "0": "rnd", ".": "Ran#", "=": "%"}
botoes_shift = {}

def ativar_shift():
    global shift_ativo
    shift_ativo = not shift_ativo
    for key, botao in botoes_shift.items():
        botao.config(text=shift_labels[key] if shift_ativo else key)

def adicionar_texto(texto):
    atual = caixaCalc.get()
    if atual == "0":
        caixaCalc.delete(0, tk.END)
    caixaCalc.insert(tk.END, texto)

def calcular():
    global ultimo_resultado
    expressao = caixaCalc.get()
    try:
        expressao = expressao.replace("×", "*").replace("÷", "/")
        if "*10**(" in expressao and not expressao.endswith(")"):
            expressao += ")"
        resultado = eval(expressao)
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, str(resultado))
        ultimo_resultado = resultado
    except:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "Erro")

def deletar():
    atual = caixaCalc.get()
    if len(atual) > 1:
        caixaCalc.delete(len(atual)-1, tk.END)
    else:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "0")

def limpar():
    caixaCalc.delete(0, tk.END)
    caixaCalc.insert(0, "0")

def trig(func):
    global shift_ativo, hyp_ativo
    try:
        valor = float(caixaCalc.get())
        if shift_ativo:
            if func == "sin":
                res = math.degrees(math.asin(valor))
            elif func == "cos":
                res = math.degrees(math.acos(valor))
            elif func == "tan":
                res = math.degrees(math.atan(valor))
        else:
            if func == "sin":
                res = math.sinh(valor) if hyp_ativo else math.sin(math.radians(valor))
            elif func == "cos":
                res = math.cosh(valor) if hyp_ativo else math.cos(math.radians(valor))
            elif func == "tan":
                res = math.tanh(valor) if hyp_ativo else math.tan(math.radians(valor))
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, str(round(res, 6)))
    except:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "Erro")
    finally:
        shift_ativo = False
        for key, botao in botoes_shift.items():
            botao.config(text=key)

def ponto_duplo():
    try:
        txt = caixaCalc.get().strip()
        if not txt:
            return
        if ':' in txt or len(re.findall(r'[-]?\d+(?:\.\d+)?', txt)) >= 3:
            nums = list(map(float, re.findall(r'[-]?\d+(?:\.\d+)?', txt)))
            if len(nums) < 3:
                caixaCalc.delete(0, tk.END)
                caixaCalc.insert(0, "Entrada inválida DMS→Decimal")
                return
            g, m, s = nums[0], nums[1], nums[2]
            dec = abs(g) + m/60 + s/3600
            if g < 0:
                dec *= -1
            caixaCalc.delete(0, tk.END)
            caixaCalc.insert(0, str(round(dec,6)))
        else:
            val = float(txt)
            sinal = -1 if val < 0 else 1
            val = abs(val)
            graus = int(val)
            minutos = int((val - graus) * 60)
            segundos = round(((val - graus) * 60 - minutos) * 60,2)
            dms_str = f"{graus * sinal}° {minutos}' {segundos}\""
            caixaCalc.delete(0, tk.END)
            caixaCalc.insert(0, dms_str)
    except:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "Erro")

def inverter_sinal():
    try:
        valor = float(caixaCalc.get())
        valor *= -1
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, str(valor))
    except:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "Erro")

def toggle_hyp():
    global hyp_ativo
    hyp_ativo = not hyp_ativo

def calcular_nCr():
    try:
        entrada = caixaCalc.get()
        n, r = map(int, re.findall(r'\d+', entrada))
        resultado = math.comb(n, r)
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, str(resultado))
    except:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "Erro")

def calcular_pol():
    try:
        entrada = caixaCalc.get()
        nums = list(map(float, re.findall(r'[-+]?\d*\.\d+|\d+', entrada)))
        if len(nums) != 2:
            raise ValueError
        x, y = nums
        r = math.sqrt(x**2 + y**2)
        theta = math.degrees(math.atan2(y, x))
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, f"{round(r,6)}, {round(theta,6)}°")
    except:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "Erro")

def calcular_X1():
    try:
        valor = float(caixaCalc.get())
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, str(valor))
    except:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "Erro")

def abc():
    try:
        txt = caixaCalc.get().strip()
        if ' ' in txt and '/' in txt:
            partes = txt.split(' ')
            inteiro = int(partes[0])
            fracao = partes[1]
            numerador, denominador = map(int, fracao.split('/'))
            valor = inteiro + numerador/denominador
            caixaCalc.delete(0, tk.END)
            caixaCalc.insert(0, str(round(valor,6)))
        else:
            valor = float(txt)
            inteiro = int(valor)
            resto = valor - inteiro
            if resto == 0:
                caixaCalc.delete(0, tk.END)
                caixaCalc.insert(0, str(inteiro))
                return
            frac = Fraction(resto).limit_denominator(1000)
            caixaCalc.delete(0, tk.END)
            caixaCalc.insert(0, f"{inteiro} {frac.numerator}/{frac.denominator}")
    except:
        caixaCalc.delete(0, tk.END)
        caixaCalc.insert(0, "Erro")

def processar_botao(label):
    global shift_ativo, ultimo_resultado
    try:
        if shift_ativo:
            if label == "s-sum":
                entrada = simpledialog.askstring("s-sum", "Digite números separados por vírgula:")
                if entrada:
                    numeros = list(map(float, entrada.split(',')))
                    soma = sum(numeros)
                    caixaCalc.delete(0, tk.END)
                    caixaCalc.insert(0, str(soma))
                    ultimo_resultado = soma
            elif label == "s-var":
                entrada = simpledialog.askstring("s-var", "Digite números separados por vírgula:")
                if entrada:
                    numeros = list(map(float, entrada.split(',')))
                    media = sum(numeros)/len(numeros)
                    variancia = sum((x-media)**2 for x in numeros)/len(numeros)
                    caixaCalc.delete(0, tk.END)
                    caixaCalc.insert(0, str(variancia))
                    ultimo_resultado = variancia
            elif label == "rnd":
                valor = random.randint(0,100)
                caixaCalc.delete(0, tk.END)
                caixaCalc.insert(0, str(valor))
                ultimo_resultado = valor
            elif label == "Ran#":
                valor = random.random()
                caixaCalc.delete(0, tk.END)
                caixaCalc.insert(0, str(valor))
                ultimo_resultado = valor
            elif label == "%":
                calcular()
                caixaCalc.insert(tk.END, "/100")
            shift_ativo = False
            for key, botao in botoes_shift.items():
                botao.config(text=key)
            return

        if label in ["sin","cos","tan"]:
            trig(label)
        elif label == "(-)":
            inverter_sinal()
        elif label == ".''":
            ponto_duplo()
        elif label == "hyp":
            toggle_hyp()
        elif label == "nCr":
            calcular_nCr()
        elif label == "pol((":
            calcular_pol()
        elif label == "X^1":
            calcular_X1()
        elif label == "a b/c":
            abc()
        else:
            if label == "EXP":
                caixaCalc.insert(tk.END,"*10**(")
            elif label == "Ans":
                caixaCalc.insert(tk.END,str(ultimo_resultado))
            elif label == "=":
                calcular()
            elif label == "DEL":
                deletar()
            elif label == "AC":
                limpar()
            elif label == "x^2":
                valor = float(caixaCalc.get())
                caixaCalc.delete(0,tk.END)
                caixaCalc.insert(0,str(valor**2))
            elif label == "x^3":
                valor = float(caixaCalc.get())
                caixaCalc.delete(0,tk.END)
                caixaCalc.insert(0,str(valor**3))
            elif label == "√":
                valor = float(caixaCalc.get())
                caixaCalc.delete(0,tk.END)
                caixaCalc.insert(0,str(math.sqrt(valor)))
            elif label == "x^-1":
                valor = float(caixaCalc.get())
                caixaCalc.delete(0,tk.END)
                caixaCalc.insert(0,str(1/valor))
            elif label == "log":
                valor = float(caixaCalc.get())
                caixaCalc.delete(0,tk.END)
                caixaCalc.insert(0,str(math.log10(valor)))
            elif label == "ln":
                valor = float(caixaCalc.get())
                caixaCalc.delete(0,tk.END)
                caixaCalc.insert(0,str(math.log(valor)))
            else:
                adicionar_texto(label)
    except:
        caixaCalc.delete(0,tk.END)
        caixaCalc.insert(0,"Erro")

def criar_botao(frame,texto,linha,coluna,cor="lightgray",fg="black",largura=6,altura=2,colspan=1,rowspan=1,shiftable=False):
    botao = tk.Button(frame,text=texto,font=("Arial",12,"bold"),fg=fg,bg=cor,width=largura,height=altura,relief="raised",bd=2,command=lambda t=texto: processar_botao(t))
    botao.grid(row=linha,column=coluna,columnspan=colspan,rowspan=rowspan,padx=3,pady=3,sticky="nsew")
    if shiftable:
        botoes_shift[texto] = botao
    if texto=="SHIFT":
        botao.config(command=ativar_shift)
    return botao

criar_botao(frame_cientifico,"SHIFT",0,0,fg="orange")
criar_botao(frame_cientifico,"ALPHA",0,1,fg="red")
criar_botao(frame_cientifico,"REPLAY",0,2,colspan=2,rowspan=2)
criar_botao(frame_cientifico,"MODE\nCLR",0,4)
criar_botao(frame_cientifico,"ON",0,5)

criar_botao(frame_cientifico,"x^-1",1,0)
criar_botao(frame_cientifico,"nCr",1,1)
criar_botao(frame_cientifico,"pol((",1,4)
criar_botao(frame_cientifico,"X^1",1,5)
criar_botao(frame_cientifico,"a b/c",2,0)
criar_botao(frame_cientifico,"√",2,1)
criar_botao(frame_cientifico,"x^2",2,2)
criar_botao(frame_cientifico,"^",2,3)
criar_botao(frame_cientifico,"log",2,4)
criar_botao(frame_cientifico,"ln",2,5)

criar_botao(frame_cientifico,"(-)",3,0)
criar_botao(frame_cientifico,".''",3,1)
criar_botao(frame_cientifico,"hyp",3,2)
criar_botao(frame_cientifico,"sin",3,3)
criar_botao(frame_cientifico,"cos",3,4)
criar_botao(frame_cientifico,"tan",3,5)

criar_botao(frame_cientifico,"rcl",4,0)
criar_botao(frame_cientifico,"eng",4,1)
criar_botao(frame_cientifico,"(",4,2)
criar_botao(frame_cientifico,")",4,3)
criar_botao(frame_cientifico,",",4,4)
criar_botao(frame_cientifico,"M+",4,5)

for i in range(6):
    frame_cientifico.grid_columnconfigure(i,weight=1)

criar_botao(frame_normal,"7",0,0)
criar_botao(frame_normal,"8",0,1)
criar_botao(frame_normal,"9",0,2)
criar_botao(frame_normal,"DEL",0,3,cor="orange",fg="white")
criar_botao(frame_normal,"×",0,4)

criar_botao(frame_normal,"4",1,0)
criar_botao(frame_normal,"5",1,1)
criar_botao(frame_normal,"6",1,2)
criar_botao(frame_normal,"AC",1,3,cor="red",fg="white")
criar_botao(frame_normal,"÷",1,4)

criar_botao(frame_normal,"1",2,0)
criar_botao(frame_normal,"2",2,1)
criar_botao(frame_normal,"3",2,2)
criar_botao(frame_normal,"+",2,3)
criar_botao(frame_normal,"EXP",2,4)

criar_botao(frame_normal,"0",3,0)
criar_botao(frame_normal,".",3,1)
criar_botao(frame_normal,"=",3,2,cor="green",fg="white")
criar_botao(frame_normal,"-",3,3)
criar_botao(frame_normal,"Ans",3,4)

for i in range(5):
    frame_normal.grid_columnconfigure(i,weight=1)

janela.mainloop()
