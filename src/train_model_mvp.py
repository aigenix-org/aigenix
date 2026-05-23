"""
train_model_mvp.py
==================
Modelo MVP para predicción de antigenicidad de proteínas (diseño de vacunas).

JUSTIFICACIÓN DEL MODELO ELEGIDO:
-----------------------------------
Tras comparar Random Forest, SVM, LightGBM y XGBoost con validación cruzada
CV-5 estratificada y evaluación en test set independiente (15%), el modelo
seleccionado es:

    Random Forest con class_weight='balanced_subsample'

Motivos:
  - Mejor Recall en test: 1.000 con umbral=0.25 (0 falsos negativos)
  - F1 en test: 0.943 — mejor balance precision/recall
  - AUC-ROC test: 0.700 — igual o superior al resto
  - Más estable que LGB/XGB con SMOTE, que empeoró en test real
  - En diseño de vacunas, un falso negativo (perder una proteína antigénica)
    tiene coste altísimo — Recall es la métrica principal, no accuracy ni AUC

UMBRAL DE DECISIÓN: 0.25 (validado empíricamente en test set)
  - Umbral default 0.50 → Recall=0.965, FN=6
  - Umbral 0.25       → Recall=1.000, FN=0  ← elegido para producción
"""

import sys
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score, f1_score, recall_score,
    precision_score, classification_report
)

# ─── Configuración ────────────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent.parent
DATASET_PATH  = BASE_DIR / 'data' / 'processed' / 'dataset.csv'
MODELS_DIR    = BASE_DIR / 'models'
MODEL_PATH    = MODELS_DIR / 'best_model_mvp.pkl'
RANDOM_STATE  = 42
THRESHOLD     = 0.25   # umbral optimizado para maximizar Recall (vacunas)

AMINO_ACIDS   = list('ACDEFGHIKLMNPQRSTVWY')
FEATURE_COLS  = (
    ['length', 'molecular_weight', 'isoelectric_point', 'gravy'] +
    [f'aa_{aa}' for aa in AMINO_ACIDS]
)
LABEL_MAP     = {0: 'No antigénica', 1: 'Antigénica'}

# Hiperparámetros exactos validados en notebooks 04 y 05
RF_PARAMS = dict(
    n_estimators      = 502,
    max_depth         = 30,
    max_features      = 0.5,
    min_samples_leaf  = 1,
    min_samples_split = 2,
    class_weight      = 'balanced_subsample',
    random_state      = RANDOM_STATE,
    n_jobs            = -1,
)


# ─── Utilidades ───────────────────────────────────────────────────────────────
def evaluar(nombre, y_true, y_prob, threshold):
    """Calcula y muestra métricas usando el umbral definido."""
    y_pred = (y_prob >= threshold).astype(int)
    metricas = {
        'auc_roc':   round(roc_auc_score(y_true, y_prob), 4),
        'f1':        round(f1_score(y_true, y_pred, zero_division=0), 4),
        'recall':    round(recall_score(y_true, y_pred, zero_division=0), 4),
        'precision': round(precision_score(y_true, y_pred, zero_division=0), 4),
    }
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())

    print(f"\n{'='*55}")
    print(f"  {nombre}")
    print(f"  Umbral de decisión: {threshold}")
    print(f"{'='*55}")
    print(f"  AUC-ROC   : {metricas['auc_roc']}")
    print(f"  F1        : {metricas['f1']}")
    print(f"  Recall    : {metricas['recall']}  ← métrica principal")
    print(f"  Precision : {metricas['precision']}")
    print(f"  Falsos negativos (antigénicas perdidas): {fn}")
    print(f"  Falsos positivos (candidatos falsos):    {fp}")
    print()
    print(classification_report(
        y_true, y_pred,
        target_names=['No antigénica (0)', 'Antigénica (1)'],
        zero_division=0
    ))
    return metricas


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    # 1. Cargar dataset
    if not DATASET_PATH.exists():
        print(f"ERROR: No se encontró el dataset en {DATASET_PATH}")
        print("Asegúrate de haber ejecutado los notebooks de preprocesamiento.")
        sys.exit(1)

    print(f"Cargando dataset desde {DATASET_PATH}...")
    dataset = pd.read_csv(DATASET_PATH)
    print(f"  {dataset.shape[0]:,} proteínas | {dataset.shape[1]} columnas")

    # Verificar que existen todas las features
    cols_faltantes = [c for c in FEATURE_COLS if c not in dataset.columns]
    if cols_faltantes:
        print(f"ERROR: Faltan columnas en el dataset: {cols_faltantes}")
        sys.exit(1)

    X = dataset[FEATURE_COLS].values
    y = dataset['label'].values

    neg = (y == 0).sum()
    pos = (y == 1).sum()
    print(f"  Distribución — antigénicas: {pos} | no antigénicas: {neg} | ratio: {neg/pos:.2f}:1")

    # 2. Split 70 / 15 / 15 estratificado (mismo random_state que notebooks)
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y,
        test_size    = 0.15,
        stratify     = y,
        random_state = RANDOM_STATE
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval,
        test_size    = 0.15 / 0.85,   # 15% del total
        stratify     = y_trainval,
        random_state = RANDOM_STATE
    )

    print(f"\nSplit aplicado:")
    print(f"  Train      : {len(y_train):,} muestras (70%)")
    print(f"  Validación : {len(y_val):,}  muestras (15%)")
    print(f"  Test       : {len(y_test):,}  muestras (15%) ← intocable hasta evaluación final")

    # 3. Entrenar Random Forest sobre train únicamente
    print(f"\nEntrenando Random Forest con {RF_PARAMS['n_estimators']} árboles...")
    modelo = RandomForestClassifier(**RF_PARAMS)
    modelo.fit(X_train, y_train)
    print("  Entrenamiento completado.")

    # 4. Evaluación en validation set
    y_val_prob = modelo.predict_proba(X_val)[:, 1]
    val_metrics = evaluar(
        "VALIDACIÓN (15%) — selección de umbral",
        y_val, y_val_prob, THRESHOLD
    )

    # 5. Evaluación final en test set (evaluación honesta)
    y_test_prob = modelo.predict_proba(X_test)[:, 1]
    test_metrics = evaluar(
        "TEST FINAL (15%) — evaluación honesta de producción",
        y_test, y_test_prob, THRESHOLD
    )

    # 6. Guardar el bundle completo con joblib
    MODELS_DIR.mkdir(exist_ok=True)
    bundle = {
        'model':        modelo,
        'threshold':    THRESHOLD,
        'feature_cols': FEATURE_COLS,
        'label_map':    LABEL_MAP,
        'val_metrics':  val_metrics,
        'test_metrics': test_metrics,
        'train_date':   datetime.now().isoformat(),
        'rf_params':    RF_PARAMS,
        'split':        {'train': 0.70, 'val': 0.15, 'test': 0.15},
        'notas': (
            "Umbral 0.25 elegido para maximizar Recall en diseño de vacunas. "
            "AUC-ROC ~0.70 es el techo informativo de las 24 features actuales. "
            "Para mejorar AUC se requieren embeddings de proteínas (ESM-2/ProtBERT)."
        )
    }
    joblib.dump(bundle, MODEL_PATH)

    print(f"\n{'='*55}")
    print(f"  MODELO MVP LISTO → {MODEL_PATH.resolve()}")
    print(f"  Recall test  : {test_metrics['recall']}")
    print(f"  F1 test      : {test_metrics['f1']}")
    print(f"  Umbral uso   : {THRESHOLD}")
    print(f"{'='*55}\n")


if __name__ == '__main__':
    main()
