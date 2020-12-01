from flask import Flask, request
import pandas as pd
import markdown
import markdown.extensions.fenced_code

app = Flask(__name__)

katas = pd.read_csv("output.csv")
kyu = [5, 6, 5, 5, 5, 5, 5]
katas_ponderadas = {j:k for j,k in zip(katas.columns, kyu)}


@app.route("/")
def index():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string

@app.route("/score")
def totalkatas():
    '''It takes the dataset and returns a dataframe with two new columns: total katas and total score'''
    
    katas = pd.read_csv("output.csv")

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
    katas['PUNTOS_TOTAL'] = katas.sum(axis=1)
    katas = katas.sort_values(by=['PUNTOS_TOTAL'], ascending=False)
    
    return katas.to_json()
    
app.run("0.0.0.0", 8000, debug=True) #http://0.0.0.0:8000/

if __name__ == "__main__":
    app.run()