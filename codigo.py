# a1) Codigo: que sea un numero
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

r1num = {int(s) for s in re.findall('\d+',dd.iloc[0,-1])}
countrycode_nice = list()
for i in range(len(df)):
    countrycode_nice.append(r1num.isdisjoint([df.iloc[i,0]]))

print(f"Hay {sum(countrycode_nice)} mujeres con un código de país incorrecto")

############################ Reglas con condiciones b)

isna_birth = [i for i in df.iloc[:,1] == df.iloc[:,1]]
print(f"Hay {len(isna_birth) - sum(isna_birth)} mujeres a las que no le cargaron el id del paciente")

largoid = list()
for i in range(len(df)):
    largoid.append(len(df.iloc[i,1]) == 13)
    if largoid[i]:
        largoid[i] = df.iloc[i,1][0:2].isnumeric() and df.iloc[i,1][3:5].isnumeric() and df.iloc[i,1][6:10].isnumeric() and df.iloc[i,1][2] == "/" and df.iloc[i,1][5] == "/" and df.iloc[i,1][10] == "-" and df.iloc[i,1][11:13].isupper()
        
print(f"Hay {len(largoid) - sum(largoid)} mujeres a las que no le cargaron bien el formato del id del paciente")

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

################################### Reglas con condiciones c)

isna_inter = [i for i in df.iloc[:,2] == df.iloc[:,2]]
print(f"Hay {len(isna_inter) - sum(isna_inter)} mujeres a las que no le cargaron la fecha de la entrevista")

largo_inter = list()
for i in range(len(df)):
    largo_inter.append(len(df.iloc[i,1]) == 13)
    if largo_inter[i]:
        largo_inter[i] = df.iloc[i,1][0:2].isnumeric() and df.iloc[i,1][3:5].isnumeric() and df.iloc[i,1][6:10].isnumeric() and df.iloc[i,1][2] == "/" and df.iloc[i,1][5] == "/"

print(f"Hay {len(largoid) - sum(largoid)} mujeres a las que no le cargaron bien la fecha de la entrevista")

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


############################################### Regla d1)

isna_etnic = [i for i in df.iloc[:,3] == df.iloc[:,3]]
print(f"Hay {len(df) - sum(isna_etnic)} datos faltantes de la etnia")
    
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


############################################### Regla e1)

isna_scr = [i for i in df.iloc[:,4] == df.iloc[:,4]]
print(f"Hay {len(df) - sum(isna_scr)} datos faltantes del formulario scr")
    
# isna_scr_pos = []
# for i in range(len(df)):
#     if df.iloc[i,4] != df.iloc[i,4]:
#         isna_scr.append([i,df.iloc[i,1]])




############################################### Regla e2)

scr_ok = []
scr_nice = {1,2}

for i in range(len(df)):
    scr_ok.append(scr_nice.isdisjoint({df.iloc[i,4]}))

print(f"Hay {sum(scr_ok) - len(df) + sum(isna_scr)} formularios mal cargados de scr")

############################################### Regla f1)

isna_usscr = [i for i in df.iloc[:,5] == df.iloc[:,5]]
print(f"Hay {len(df) - sum(isna_usscr)} datos faltantes del formulario usscr")
    
# isna_scr_pos = []
# for i in range(len(df)):
#     if df.iloc[i,4] != df.iloc[i,4]:
#         isna_scr.append([i,df.iloc[i,1]])




############################################### Regla f2)

usscr_ok = []
usscr_nice = {1,2}

for i in range(len(df)):
    usscr_ok.append(usscr_nice.isdisjoint({df.iloc[i,5]}))

print(f"Hay {sum(usscr_ok) - len(df) + sum(isna_usscr)} formularios mal cargados de usscr")


############################################### Regla g1)

isna_consent = [i for i in df.iloc[:,6] == df.iloc[:,6]]
print(f"Hay {len(df) - sum(isna_consent)} datos faltantes del formulario de consentimiento")
    
# isna_scr_pos = []
# for i in range(len(df)):
#     if df.iloc[i,4] != df.iloc[i,4]:
#         isna_scr.append([i,df.iloc[i,1]])


############################################### Regla g2)

consent_ok = []
consent_nice = {1,2}

for i in range(len(df)):
    consent_ok.append(consent_nice.isdisjoint({df.iloc[i,6]}))

print(f"Hay {sum(consent_ok) - len(df) + sum(isna_consent)} formularios mal cargados de consentimiento")


############################################### Regla h1)

subj_ok = []
subj_ok2 = []
subj_ok3 = []
isna_subj = [i for i in df.iloc[:,7] == df.iloc[:,7]]
for i in range(len(df)):
    subj_ok.append(True)
    subj_ok2.append(True)
    subj_ok3.append(True)
    if df.iloc[i,7] == df.iloc[i,7] and len(str(df.iloc[i,7])) == 9 and str(df.iloc[i,7]).isnumeric():
        subj_ok3[i] = False 
    if df.iloc[i,4] == 2 and df.iloc[i,5] == 2 and df.iloc[i,6] == 2 and df.iloc[i,7] != df.iloc[i,7]:
       subj_ok[i] = False
    elif (df.iloc[i,4] == 1 or df.iloc[i,5] == 1 or df.iloc[i,6] == 1) and df.iloc[i,7] == df.iloc[i,7]:
        subj_ok2[i] = False



print(f"Hay {len(df) - sum(subj_ok)} numeros de sujetos que tendrian que ser cargados")
print(f"Hay {len(df) - sum(subj_ok2)} numeros de sujetos que no tendrian que ser cargados, \n por lo tanto no participaron del estudio por no cumplir alguno de los requisitos requeridos")
print(f"Hay {len(df) -sum(isna_subj) - sum(subj_ok3)} mal cargados")


############################################### Regla h2)

paisbien = []
for i in range(len(df)):
    if df.iloc[i,7] == df.iloc[i,7]:
        paisbien.append({df.iloc[i,0]}.isdisjoint({int(df.iloc[i,7][0:3])}))
         
print(f"Hay {sum(paisbien)} codigos de paises mal cargados en el numero de sujeto")
     
print(paisbien.index(True))




