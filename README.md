# antigen_predictor

Clasificador de antigenicidad de proteínas usando Machine Learning.  
Proyecto educativo desarrollado con Python, scikit-learn y Biopython.
---
Dado un conjunto de proteínas de un patógeno, el modelo predice cuáles tienen más probabilidad de ser antigénicas (reconocidas por el sistema inmune humano), usando características calculadas a partir de su secuencia de aminoácidos.

---

## ¿Qué hace este proyecto?

Dado un archivo FASTA con secuencias de proteínas de un patógeno, el sistema predice cuáles tienen mayor probabilidad de ser antigénicas, es decir, de ser reconocidas por el sistema inmune humano.

La salida es una tabla con un score de antigenicidad (entre 0 y 1) por proteína y un gráfico de barras ordenado de mayor a menor score.

Este tipo de herramienta podría usarse como filtro rápido para priorizar candidatos vacunales in silico, reduciendo el tiempo de búsqueda inicial de antígenos. No reemplaza ensayos experimentales ni ensayos clínicos.

---

## Contexto y motivación

El proyecto es un ejercicio educativo de Machine Learning aplicado a bioinformática. El objetivo es aprender a construir un pipeline completo: desde la obtención y limpieza de datos reales hasta el despliegue de una interfaz web funcional.

Los patógenos usados como caso de estudio son **SARS-CoV-2** e **Influenza A**, por su relevancia clínica y por la abundancia de datos experimentales disponibles.

---

## Dataset

**Fuente:** [IEDB — Immune Epitope Database](https://www.iedb.org)

IEDB es una base de datos pública y gratuita que contiene datos experimentales de epítopos: fragmentos de proteínas reconocidos por el sistema inmune en ensayos de laboratorio.

**Estrategia de construcción del dataset:**

1. Descarga del archivo de exportación completo de IEDB (`epitope_full_v3.csv`).
2. Filtrado por organismo (SARS-CoV-2 e Influenza A) y por resultado de ensayo positivo.
3. Mapeo de epítopos a sus proteínas completas usando identificadores UniProt.
4. Etiquetado binario: `label = 1` para proteínas con al menos un epítopo validado experimentalmente, `label = 0` para proteínas del mismo patógeno sin evidencia de antigenicidad.
5. Resultado: archivo `data/dataset.csv` con entre 500 y 2.000 ejemplos balanceados.

> **Nota:** El archivo `epitope_full_v3.csv` (~830 MB) no está incluido en este repositorio por su tamaño. Debe descargarse manualmente desde [iedb.org/database_export_v3.php](https://www.iedb.org/database_export_v3.php) y almacenarse en Google Drive si se usan los notebooks de Colab.

---

## Features del modelo

Calculadas con **Biopython** a partir de la secuencia de aminoácidos de cada proteína:

| Feature | Descripción |
|---|---|
| Longitud | Número de aminoácidos |
| Composición de aminoácidos | Porcentaje de cada uno de los 20 aminoácidos estándar |
| Peso molecular | En Daltons |
| Punto isoeléctrico | pH al que la carga neta de la proteína es cero |
| Hidrofobicidad media | Índice GRAVY |

No se usan embeddings de modelos de lenguaje de proteínas ni features de estructura 3D.

---

## Modelo

- **Algoritmo principal:** Random Forest (scikit-learn)
- **Validación:** Cross-validation estratificada (k=5)
- **Métricas:** AUC-ROC y F1-score
- **Baseline:** clasificador de mayoría y Logistic Regression
- **Guardado:** `models/model.pkl` con joblib

---

## Estructura del repositorio

```
antigen_predictor/
│
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_dataset_construction.ipynb
│   ├── 03_features_and_model.ipynb
│   └── 04_results_and_evaluation.ipynb
│
├── app/
│   └── app.py
│
├── data/
│   └── dataset.csv
│
├── models/
│   └── model.pkl
│
├── sample_input/
│   └── covid_proteins.fasta
│
└── README.md
```

---

## Requisitos

```
Python 3.9+
biopython
scikit-learn
pandas
matplotlib
streamlit
joblib
```

Instalación:

```bash
pip install biopython scikit-learn pandas matplotlib streamlit joblib
```

---

## Cómo usar

**Entrenamiento del modelo:**  
Ejecutar los notebooks en orden (01 → 02 → 03) desde Google Colab.

**Interfaz web:**  
```bash
cd app
streamlit run app.py
```
Subir un archivo FASTA con las proteínas a evaluar. La app carga el modelo guardado y devuelve la tabla de scores y el gráfico.

---

## Limitaciones

- El modelo está entrenado únicamente con datos de SARS-CoV-2 e Influenza A. Su capacidad de generalización a otros patógenos es desconocida.
- Las features usadas son exclusivamente de secuencia. No se considera estructura 3D, glicosilación ni procesamiento celular.
- Un score alto no garantiza que la proteína sea un buen antígeno vacunal. Es un filtro orientativo, no un predictor clínico.
- El tamaño del dataset es pequeño para estándares de producción.

---

## Equipo

Proyecto desarrollado por tres estudiantes como ejercicio educativo de Machine Learning.

---

## Licencia

MIT
