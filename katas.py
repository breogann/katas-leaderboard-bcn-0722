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

    #hasta que arreglemos esto, habrá que meter los kyu a mano
kyu = [8, 7, 7, 7, 8, 7, 5]

kyus_by_kata  = { 
    "counting-sheep-dot-dot-dot": 8,
    "counting-in-the-amazon": 7,
    "deodorant-evaporator":7,
    "fake-binary": 8,
    "tests-results": 7,
    "keep-hydrated-1": 8,
    "see-you-next-happy-year": 7,
    "pete-the-baker": 5,
    "count-the-smiley-faces": 6
}

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
katas['You_obtained'] = copia.sum(axis=1)


    #Suma por puntos
katas['TOTAL_SCORE'] = katas.sum(axis=1) - katas.You_obtained
katas = katas.sort_values(by=['TOTAL_SCORE'], ascending=False)

    #saco un df solo con la columna puntos para hacer visualización en st
paramostrar = katas[['You_obtained',"TOTAL_SCORE"]]
finalistas = katas[(katas["TOTAL_SCORE"]>= porcentaje)]["TOTAL_SCORE"]

st.markdown("<h4 style='text-align: center; color: black;'> 🚀 -------  GENERAL SCORES ------- 🚀</h4>", unsafe_allow_html=True)


st.dataframe(katas)


st.write(
f"The max score you can get so far is: {total}"
)


st.markdown("<h4 style='text-align: center; color: black;'> 🙊 -------  Total scores ------- 🙊</h4>", unsafe_allow_html=True)

st.dataframe(paramostrar)
