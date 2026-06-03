import joblib

PATH = "models/best_model_mvp.pkl"

try:
    data = joblib.load(PATH)
    if isinstance(data, dict):
        print("📊 CONTENIDO DEL BUNDLE:")
        
        # Revisar Test
        if "test_metrics" in data:
            print("\n✅ MÉTRICAS DE TEST (Hold-out set):")
            print("Estas son las mejores para mostrar. Indican éxito con datos nuevos.")
            for k, v in data["test_metrics"].items():
                print(f" - {k}: {v:.4f}")
        
        # Revisar Validación
        if "val_metrics" in data:
            print("\n⚠️ MÉTRICAS DE VALIDACIÓN (Cross-Validation):")
            print("Son útiles, pero suelen ser más altas que las de test.")
            for k, v in data["val_metrics"].items():
                print(f" - {k}: {v:.4f}")
    else:
        print("El archivo no es un diccionario, solo contiene el objeto del modelo.")

except Exception as e:
    print(f"Error: {e}")