import streamlit as st
import numpy as np
import os
import pandas as pd
from PIL import Image

    #título API
st.markdown("<h2 style='text-align: center; color: black;'>🔥🥋 Databcn0722 Katas game! 🥋🔥</h2>", unsafe_allow_html=True)
    #imagen de portada api
image = Image.open('images/portada.jpg')
st.image (image,use_column_width=True)

    #saca el archivo del repo de katas que usamos para ver quién saca
os.system("curl -LJO https://raw.githubusercontent.com/PauPerL/codewars-kata-student-correction-ih/master/output/output.csv")
katas = pd.read_csv("output.csv", error_bad_lines=False)
print(katas.head())

    #hasta que arreglemos esto, habrá que meter los kyu a mano
kyu = [8, 7, 7, 7, 8, 7, 5]

#countingsheep: 8
#counting in the amazon: 7
#deodorant: 7
#test-results:7
#keep hydrated: 8
# see you next happy year: 7
#pete the baker: 5


#count the simley faces: 6
#fake binary: 8



#week_4_0321 = [6, 7, 6]

    #diccionario con puntos que le damos a las katas
pondera = {5:12, 6:9, 7:6, 8:4}

    #transformamos lista kyu a lista puntos reales
puntos = [pondera.get(a) for a in kyu]

    #seteamos el index del dataframe por USERNAME del alumnado
katas.set_index("username", inplace=True)

    #katas = katas.applymap(lambda x: 1 if x==True else 0)
katas_ponderadas = {nombre:valor for nombre,valor in zip(katas.columns, puntos)}

    #total de puntos que puedes tener
total = sum(katas_ponderadas.values())

    #Porcentaje para participar en el sorteo
porcentaje = (total * 40) / 100

    
    #Ponderación en el DF
for columna in katas.columns:
    katas[f"{columna}"] = np.where(katas[f"{columna}"] == True,katas_ponderadas.get(f"{columna}"),0)

    #Voy a hacer una copia del df con 1 en vez de ponderación para sacar un count

copia = katas.copy()
copia = copia.applymap(lambda x: 1 if x!=0 else 0)


    #Total katas
katas['Has_Sacado'] = copia.sum(axis=1)


    #Suma por puntos
katas['PUNTOS_TOTAL'] = katas.sum(axis=1) - katas.Has_Sacado
katas = katas.sort_values(by=['PUNTOS_TOTAL'], ascending=False)

    #saco un df solo con la columna puntos para hacer visualización en st
paramostrar = katas[['Has_Sacado',"PUNTOS_TOTAL"]]
finalistas = katas[(katas["PUNTOS_TOTAL"]>= porcentaje)]["PUNTOS_TOTAL"]

st.markdown("<h4 style='text-align: center; color: black;'> 🚀 -------  GENERAL SCORES ------- 🚀</h4>", unsafe_allow_html=True)


st.dataframe(katas)


st.write(
f"The max score you can get so far is: {total}"
)


st.markdown("<h4 style='text-align: center; color: black;'> 🙊 -------  Total scores ------- 🙊</h4>", unsafe_allow_html=True)

st.dataframe(paramostrar)
