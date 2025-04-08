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

df = pd.read_excel("adm.xlsx")
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








