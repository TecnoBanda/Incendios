import sidebarlib as sd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier

st.header("PREDICCIÓN DE RIESGO DE INCENDIO EN EL DEPARTAMENTO DE COCHABAMBA")
st.image("cerrotunari.jpg")

url = "https://www.meteoblue.com/es/tiempo/historyclimate/weatherarchive/cochabamba_bolivia_3919968"

st.write("""
        Somos un equipo denominado TecnoBanda, representando al Colegio San Agustín en las Olimpiadas STEM+ 2023 en Cochabamba, Bolivia. Nuestra meta primordial radica en la creación de una plataforma capaz de emplear inteligencia artificial para predecir y evaluar el riesgo de incendios. Este proyecto busca no solo facilitar las labores de los bomberos, sino también proporcionar una herramienta eficiente para el control y mitigación de incendios, al alcance de toda la población y sobre todo de las instituciones que requieren toda la ayuda posible para contrarrestar este problema latente en nuestra sociedad.

        El enfoque de este prototipo se centra en representar el riesgo de incendios en todo el departamento de Cochabamba. Sin embargo, su aplicabilidad se extiende para ser implementado en diferentes municipios y departamentos mediante la sustitución de la base de datos manteniendo la estructura de columnas y los códigos de programación.

        Los datos pertinentes para el departamento de Cochabamba, siguiendo el mismo formato, se encuentran disponibles en el siguiente enlace de [MeteoBlue](%s).
         
        A continuación, se encuentra un tutorial de como manejar la página web.
"""%url)
st.video("https://youtu.be/4UjXIj6seI4")
data=pd.read_csv("Data_clima_Clasificaction.csv")


st.image("incendios.jpg")
#SIDEBAR CONFIG
st.sidebar.title("INFORMACIÓN IMPORTANTE")
st.sidebar.header("Completar cada sección")

#SIDEBAR DATA GOES TO PANDAS DATASET SHOWN ON TABLE
dataframe = sd.user_input()

#MAIN PAGE
st.subheader("Datos Ingresados")
st.write(dataframe)

st.subheader("")
st.subheader("Datos de entrenamiento")
st.write(data)

#CORRELATION HEATMAP
st.subheader("Mapa De Correlación")
st.write("Seleccionar la casilla en caso de querer revisar el gráfico")

df= pd.read_csv("Data_clima_Clasificaction.csv")
graph_type= st.checkbox('Gráfico de correlación')
if graph_type:
    fig, ax = plt.subplots(figsize=(15,15))
    # Create the heatmap
    sns.heatmap(df.corr(), annot=True, cmap="bwr", fmt=".2f", linewidths=.5)
    # Display the plot
    st.pyplot(fig)
           
           
           
           
#GRADIENT BOOSTING 



# Split the data into features (X) and target (y)
X = data.drop('Incendio', axis=1)
y = data['Incendio']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
lr_list = [0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]


st.subheader("Precisión del Algoritmo (Gradient Boosting)")
with st.expander("**Datos Extra**"):
    for learning_rate in lr_list:
        gb_clf = GradientBoostingClassifier(n_estimators=20, learning_rate=learning_rate, max_features=2, max_depth=2, random_state=0)
        gb_clf.fit(X_train, y_train)

        st.write("Ritmo de Aprendizaje: ", learning_rate)
        st.write("Puntaje de Precisión (Entrenamiento): {0:.3f}".format(gb_clf.score(X_train, y_train)))
        st.write("Puntaje de Precisión (Validación): {0:.3f}".format(gb_clf.score(X_test, y_test)))


gb_clf2 = GradientBoostingClassifier(n_estimators=20, learning_rate=0.5, max_features=2, max_depth=2, random_state=0)
gb_clf2.fit(X_train, y_train)
predictions = gb_clf2.predict(X_test)
prediction = gb_clf2.predict(dataframe.to_numpy())

st.write("**Matriz de Confusión:**")
st.write('''
         1 significa que si hay riesgo de alta probabilidad de incendio\n
         0 significa que no hay riesgo de alta probabilidad de incendio
         ''')
st.write(pd.DataFrame(confusion_matrix(y_test, predictions)))

st.write("**Reporte de Clasificación:**")
st.dataframe(classification_report(y_test, predictions, output_dict=True))


st.subheader("Resultado del Modelo")

st.write("Resultado de la predicción: " + str(prediction[0]))

if int(prediction) == 1:
    st.write("Existe una :red[**alta**] probabilidad de riesgo de incendio", )
else:
    st.write("Existe una :green[**baja**] probabilidad de riesgo de incendio")
    

for i in range(10):
    st.write("")
    

st.markdown("""
<style>
.big-font {
    position: absolute !important;
    font-size:13px !important;
    line-height:5px !important;
    right:100px !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="big-font">INFO</p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">Olimpiadas STEM+ 2023</p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">Grupo: TecnoBanda</p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">Colegio San Agustín</p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">CBBA - Bolivia</p>', unsafe_allow_html=True)

