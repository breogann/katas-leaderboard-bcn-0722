import streamlit as st
import numpy as n
import os
import pandas as pd
from PIL import Image


st.markdown("<h1 style='text-align: center; color: black;'>¡Juego de las Katas Datamad1020-rev!</h1>", unsafe_allow_html=True)

image = Image.open('images/portada.jpg')
st.image (image,use_column_width=True)




os.system("curl -LJO https://raw.githubusercontent.com/agalvezcorell/codewars-kata-student-correction-ih/master/output/output.csv")

katas = pd.read_csv("output.csv")
kyu = [5, 7, 6, 5, 6, 5, 6, 6, 7, 6, 6]
pondera = {5:12, 6:9, 7:6, 8:4}
puntos = [pondera.get(a) for a in kyu]


katas.set_index('username', inplace=True)
listadrop = ['counting-sheep-dot-dot-dot',
 'fake-binary',
 'sum-mixed-array',
 'deodorant-evaporator',
 'user-class-for-banking-system',
 'counting-in-the-amazon',
 'tests-results',
 'count-the-smiley-faces',
 'see-you-next-happy-year',
 'sql-with-harry-potter-sorting-hat-comparators',
 'sql-basics-monsters-using-case']

katas = katas.drop(listadrop, axis = 1)
#katas = katas.applymap(lambda x: 1 if x==True else 0)
katas_ponderadas = {nombre:valor for nombre,valor in zip(katas.columns, puntos)}
    
    
    #Ponderación en el DF
import numpy as np
for columna in katas.columns:
    katas[f"{columna}"] = np.where(katas[f"{columna}"] == True,katas_ponderadas.get(f"{columna}"),0)

    #Total katas
katas['TOTAL_KATAS'] = katas.sum(axis=1)


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

total = sum(katas_ponderadas.values())

st.write(
f"El total de puntos es {total}"
)

