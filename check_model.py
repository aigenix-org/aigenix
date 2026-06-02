import joblib

# Cambia la ruta si es necesario
PATH = "models/best_model_mvp.pkl"

try:
    contenido = joblib.load(PATH)
    print("--- INFORMACIÓN DEL MODELO ---")
    print(f"Tipo de objeto: {type(contenido)}")

    if isinstance(contenido, dict):
        print("✅ Es un DICCIONARIO (Bundle). Contiene estas llaves:")
        for llave in contenido.keys():
            print(f" - {llave}")
        
        # Verificar si las métricas están dentro
        if "test_metrics" in contenido:
            print("\n✅ MÉTRICAS ENCONTRADAS:")
            print(contenido["test_metrics"])
        else:
            print("\n❌ NO HAY MÉTRICAS ('test_metrics') en el diccionario.")
    else:
        print("❌ Es SOLO EL MODELO (no es un diccionario).")
        print("Para ver métricas, debes guardar el modelo como un diccionario.")

except Exception as e:
    print(f"Error al cargar el archivo: {e}")