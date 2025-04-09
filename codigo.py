# a1) Codigo: que sea un numero                            x != x
# a2) Codigo del pais que este entre esos codigos
# b1) estando
# b2) Formato ok
# b3) Fecha esta ok
# c1) estando
# c2) formato ok
# c3) que la fecha sea cuando se llevo a cabo el estudio
# bc1) 50<x-y<18 fecha+
# d1) que sea un numero
# d2) que este en el rango
# e1) que sea un numero
# e2) clin dentro del rango
# f1) que sea un numero
# f2) us dentro del rango
# g1) que sea un numero
# g2) con dentro del rango
# h1) all(codigos) == subj_num
# h2) esta dentro del rango
# h3) el pais matchea
import pandas as pd
import numpy as np
import re
from dateutil.relativedelta import relativedelta

df = pd.read_excel("adm.xlsx", dtype={"subjectnumber" : str})
dd = pd.read_excel("dd.xlsx")

######################### Reglas con condiciones a)

isna_country = [i for i in df.iloc[:,0] == df.iloc[:,0]]
print(f"Hay {len(isna_country) - sum(isna_country)} mujeres a las que no le cargaron el código del país")

a1 = isna_country

r1num = {int(s) for s in re.findall('\d+',dd.iloc[0,-1])}
countrycode_nice = list()
for i in range(len(df)):
    countrycode_nice.append(r1num.isdisjoint([df.iloc[i,0]]))

print(f"Hay {sum(countrycode_nice)} mujeres con un código de país incorrecto")

a2 = [not i for i in countrycode_nice]


############################ Reglas con condiciones b)

isna_birth = [i for i in df.iloc[:,1] == df.iloc[:,1]]
print(f"Hay {len(isna_birth) - sum(isna_birth)} mujeres a las que no le cargaron el id del paciente")

b1 = isna_birth


largoid = list()
for i in range(len(df)):
    largoid.append(len(df.iloc[i,1]) == 13)
    if largoid[i]:
        largoid[i] = df.iloc[i,1][0:2].isnumeric() and df.iloc[i,1][3:5].isnumeric() and df.iloc[i,1][6:10].isnumeric() and df.iloc[i,1][2] == "/" and df.iloc[i,1][5] == "/" and df.iloc[i,1][10] == "-" and df.iloc[i,1][11:13].isupper()
        
print(f"Hay {len(largoid) - sum(largoid)} mujeres a las que no le cargaron bien el formato del id del paciente")

b2 = largoid



fecha_birth = np.zeros((len(df), 3), dtype=int)
for i in range(len(df)):
    fecha_birth[i,:] = re.findall('\d+',df.iloc[i, 1])

mes31 = {1,3,5,7,8,10,12}
mes29 = {2}
mes30 = {4,6,9,11}
fecha_ok = list()

for i in range(len(df)):
    fecha_ok.append(False)
    if fecha_birth[i,1] <= 12 and fecha_birth[i,1] > 0 and fecha_birth[i,0] > 0:
        if not mes31.isdisjoint([fecha_birth[i,1]]):
            fecha_ok[i] = fecha_birth[i,0] <= 31
        elif not mes30.isdisjoint([fecha_birth[i,1]]):
            fecha_ok[i] = fecha_birth[i,0] <= 30
        elif not mes29.isdisjoint([fecha_birth[i,1]]):
            fecha_ok[i] = fecha_birth[i,0] <= 29

print(f"Hay {len(df) - sum(fecha_ok)} fechas incorrectas en el id")

b3 = fecha_ok


################################### Reglas con condiciones c)

isna_inter = [i for i in df.iloc[:,2] == df.iloc[:,2]]
print(f"Hay {len(isna_inter) - sum(isna_inter)} mujeres a las que no le cargaron la fecha de la entrevista")

c1 = isna_inter

largo_inter = list()
for i in range(len(df)):
    largo_inter.append(len(df.iloc[i,1]) == 13)
    if largo_inter[i]:
        largo_inter[i] = df.iloc[i,1][0:2].isnumeric() and df.iloc[i,1][3:5].isnumeric() and df.iloc[i,1][6:10].isnumeric() and df.iloc[i,1][2] == "/" and df.iloc[i,1][5] == "/"

print(f"Hay {len(largo_inter) - sum(largo_inter)} mujeres a las que no le cargaron bien la fecha de la entrevista")

c2 = largo_inter


fecha_inter = np.zeros((len(df), 3), dtype=int)
for i in range(len(df)):
    fecha_inter[i,:] = re.findall('\d+',df.iloc[i, 2])

fecha_ok2 = list()
for i in range(len(df)):
    fecha_ok2.append(False)
    if fecha_inter[i,1] <= 12 and fecha_inter[i,1] > 0 and fecha_inter[i,0] > 0 and fecha_inter[i,2] > 2008 and fecha_inter[i,2] < 2015:
        if not mes31.isdisjoint([fecha_inter[i,1]]):
            fecha_ok2[i] = fecha_inter[i,0] <= 31
        elif not mes30.isdisjoint([fecha_inter[i,1]]):
            fecha_ok2[i] = fecha_inter[i,0] <= 30
        elif not mes29.isdisjoint([fecha_inter[i,1]]):
            fecha_ok2[i] = fecha_inter[i,0] <= 29
            
print(f"Hay {len(df) - sum(fecha_ok2)} fechas incorrectas de la entrevista")

c3 = fecha_ok2


############################################### Regla entre b) y c)
# ################# Trabajar con formato fecha
fecha_int_formato = pd.to_datetime(df['interview'], format='%d/%m/%Y')
fecha_birth_formato = pd.to_datetime([i[0:10] for i in df['patientid']], format='%d/%m/%Y')



# dif_fechas = fecha_formato[0] - fecha_formato[1]
# print(dif_fechas)
################# Calcular cuántos años de diferencia hay con formato fecha

años_dif = list()
ok_años_dif = list()
for i in range(len(df)):
    años_dif.append(0)
    if fecha_ok[i] and fecha_ok2[i]:
        años_dif[i] = relativedelta(fecha_int_formato[i], fecha_birth_formato[i]).years
        ok_años_dif.append(años_dif[i] < 51 and años_dif[i] > 17)

print(f"Hay {len(ok_años_dif) - sum(ok_años_dif)} mujeres que supuestamente no están en una edad fértil o no ingresaron al estudio por ser menores")

bc1 = ok_años_dif
############################################### Regla d1)

isna_etnic = [i for i in df.iloc[:,3] == df.iloc[:,3]]
print(f"Hay {len(df) - sum(isna_etnic)} datos faltantes de la etnia")
   
d1 = isna_etnic
    
# isna_etnic_pos = []
# for i in range(len(df)):
#     if df.iloc[i,3] != df.iloc[i,3]:
#         isna_etnic_pos.append([i,df.iloc[i,1]])



############################################### Regla d2)

etnic_ok = []
etnica_nice = {1,2,3,4}

for i in range(len(df)):
    etnic_ok.append(etnica_nice.isdisjoint({df.iloc[i,3]}))

print(f"Hay {sum(etnic_ok) - len(df) + sum(isna_etnic)} etnias cargadas de manera incorrecta")

d2 = [not i for i in etnic_ok]

############################################### Regla e1)

isna_scr = [i for i in df.iloc[:,4] == df.iloc[:,4]]
print(f"Hay {len(df) - sum(isna_scr)} datos faltantes del formulario scr")
    
# isna_scr_pos = []
# for i in range(len(df)):
#     if df.iloc[i,4] != df.iloc[i,4]:
#         isna_scr.append([i,df.iloc[i,1]])

e1 = isna_scr


############################################### Regla e2)

scr_ok = []
scr_nice = {1,2}

for i in range(len(df)):
    scr_ok.append(scr_nice.isdisjoint({df.iloc[i,4]}))

print(f"Hay {sum(scr_ok) - len(df) + sum(isna_scr)} formularios mal cargados de scr")

e2 = [not i for i in scr_ok] 

############################################### Regla f1)

isna_usscr = [i for i in df.iloc[:,5] == df.iloc[:,5]]
print(f"Hay {len(df) - sum(isna_usscr)} datos faltantes del formulario usscr")
    
# isna_scr_pos = []
# for i in range(len(df)):
#     if df.iloc[i,4] != df.iloc[i,4]:
#         isna_scr.append([i,df.iloc[i,1]])

f1 = isna_usscr

############################################### Regla f2)

usscr_ok = []
usscr_nice = {1,2}

for i in range(len(df)):
    usscr_ok.append(usscr_nice.isdisjoint({df.iloc[i,5]}))

print(f"Hay {sum(usscr_ok) - len(df) + sum(isna_usscr)} formularios mal cargados de usscr")

f2 = [not i for i in usscr_ok] 
############################################### Regla g1)

isna_consent = [i for i in df.iloc[:,6] == df.iloc[:,6]]
print(f"Hay {len(df) - sum(isna_consent)} datos faltantes del formulario de consentimiento")
    
# isna_scr_pos = []
# for i in range(len(df)):
#     if df.iloc[i,4] != df.iloc[i,4]:
#         isna_scr.append([i,df.iloc[i,1]])

g1 = isna_consent
############################################### Regla g2)

consent_ok = []
consent_nice = {1,2}

for i in range(len(df)):
    consent_ok.append(consent_nice.isdisjoint({df.iloc[i,6]}))

print(f"Hay {sum(consent_ok) - len(df) + sum(isna_consent)} formularios mal cargados de consentimiento")

g2 = [not i for i in consent_ok] 

############################################### Regla h1)

subj_ok = []
subj_ok2 = []
subj_ok3 = []
isna_subj = [i for i in df.iloc[:,7] == df.iloc[:,7]]
for i in range(len(df)):
    subj_ok.append(True)
    subj_ok2.append(True)
    subj_ok3.append(True)
    if len(str(df.iloc[i,7])) == 9 and str(df.iloc[i,7]).isnumeric():
        subj_ok3[i] = False 
    if df.iloc[i,4] == 2 and df.iloc[i,5] == 2 and df.iloc[i,6] == 2 and df.iloc[i,7] != df.iloc[i,7]:
       subj_ok[i] = False
    elif (df.iloc[i,4] == 1 or df.iloc[i,5] == 1 or df.iloc[i,6] == 1) and df.iloc[i,7] == df.iloc[i,7]:
        subj_ok2[i] = False



print(f"Hay {len(df) - sum(subj_ok)} numeros de sujetos que tendrian que ser cargados")

h1 = subj_ok

print(f"Hay {len(df) - sum(subj_ok2)} numeros de sujetos que no tendrian que ser cargados, \n por lo tanto no participaron del estudio por no cumplir alguno de los requisitos requeridos")

h2 = subj_ok2

print(f"Hay {len(df) - sum(isna_subj) - sum(subj_ok3)} que no estan en el rango")

h3 = [not i for i in subj_ok3] 


############################################### Regla h4)

paisbien = []
for i in range(len(df)):
    if df.iloc[i,7] == df.iloc[i,7]:
        paisbien.append({df.iloc[i,0]}.isdisjoint({int(df.iloc[i,7][0:3])}))
         
print(f"Hay {sum(paisbien)} codigos de paises mal cargados en el numero de sujeto")

h4 = [not i for i in paisbien]

matriz_valores = [a1, a2, b1, b2, b3, c1,c2,c3,bc1,d1,d2,e1,e2,f1,f2,g1,g2,h1,h2,h3,h4]
paciente_limpio = [all(valores) for valores in zip(*matriz_valores)]
print(sum(paciente_limpio))


print(pd.DataFrame(data=[[len(a1)-sum(a1), len(a2)-sum(a2), "-"],
                         [len(b1)-sum(b1), len(b2)-sum(b2) + len(df) - sum(fecha_ok), len(ok_años_dif) - sum(ok_años_dif)],
                         [len(c1)-sum(c1), len(c2)-sum(c2) + len(df) - sum(fecha_ok2), len(ok_años_dif) - sum(ok_años_dif)],
                         [len(d1)-sum(d1), len(d2)-sum(d2), "-"],
                         [len(e1)-sum(e1), sum(scr_ok) - len(df) + sum(isna_scr), "-"],
                         [len(f1)-sum(f1), sum(usscr_ok) - len(df) + sum(isna_usscr), "-"],
                         [len(g1)-sum(g1), sum(consent_ok) - len(df) + sum(isna_consent), "-"],
                         [len(h1)-sum(h1), len(df) - sum(isna_subj) - sum(subj_ok3) ,len(h2)-sum(h2) + sum(paisbien)]]))



print(h1.index(False, 16))
print(h2.index(False))
print(h3.index(False, 16))
print(h4.index(False))

print(len(set(df.iloc[:,7])))

print("No hay distintos")