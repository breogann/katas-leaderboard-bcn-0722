import streamlit as st
import os
import pandas as pd
from PIL import Image


st.markdown("<h1 style='text-align: center; color: black;'>¡Juego de las Katas Datamad1020-rev!</h1>", unsafe_allow_html=True)

image = Image.open('images/portada.jpg')
st.image (image,use_column_width=True)




os.system("curl -LJO https://raw.githubusercontent.com/agalvezcorell/codewars-kata-student-correction-ih/master/output/output.csv")

katas = pd.read_csv("output.csv")
kyu = [5, 6, 5, 5, 5, 5, 5, 6]
katas_ponderadas = {j:k for j,k in zip(katas.columns, kyu)}

katas.set_index('username', inplace=True)
katas = katas[katas.columns[11:]]
katas = katas.applymap(lambda x: 1 if x==True else 0)
    
    #Total katas
katas['TOTAL_KATAS'] = katas.sum(axis=1)

    #Ponderación
for i in katas_ponderadas:
    for j in katas.columns:
        katas[j].loc[(katas[j] == 1)] = 1*katas_ponderadas[i]
    
    #Suma por puntos
katas['PUNTOS_TOTAL'] = katas.sum(axis=1) - katas.TOTAL_KATAS
katas = katas.sort_values(by=['PUNTOS_TOTAL'], ascending=False)

paramostrar = katas["PUNTOS_TOTAL"]

st.write(
"""
Mira la tabla general
"""
)
st.dataframe(paramostrar)
st.write(
"""
Mira las katas que has hecho y los puntos que te da cada una
"""
)
st.dataframe(katas)