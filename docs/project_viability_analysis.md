# Clasificador de Antigenicidad de Proteínas mediante Machine Learning

### Una herramienta educativa en la intersección entre la inteligencia artificial y la inmunología

---

## Bloque 1 — El problema que queremos atacar

Cuando un nuevo patógeno aparece, como ocurrió con el SARS-CoV-2 en 2020, los científicos se enfrentan a una pregunta urgente: ¿contra qué parte del virus debería reaccionar el sistema inmune? Un virus puede tener decenas de proteínas. No todas son iguales de visibles para el sistema inmune, y no todas son buenos blancos para una vacuna.

El proceso tradicional de identificar qué proteínas son antigénicas, es decir, cuáles provocan una respuesta inmune, implica ensayos de laboratorio costosos, lentos y que requieren infraestructura especializada. En el contexto de una pandemia, ese tiempo es crítico.

La pregunta que guía nuestro proyecto es: **¿puede un modelo de Machine Learning, entrenado con datos experimentales ya existentes, ayudar a priorizar qué proteínas merecen ser estudiadas primero?**

La respuesta, con matices importantes que veremos, es que sí, y eso es lo que vamos a construir.

---

## Bloque 2 — Qué vamos a construir exactamente

El sistema recibe como entrada un archivo FASTA, que es el formato estándar para representar secuencias de proteínas en bioinformática. A partir de esas secuencias, calcula automáticamente una serie de características fisicoquímicas: longitud, composición de aminoácidos, peso molecular, punto isoeléctrico e hidrofobicidad. Con esas características, un modelo de Random Forest entrenado previamente asigna a cada proteína un score entre 0 y 1 que representa la probabilidad estimada de que sea antigénica.

La salida es una tabla ordenada de candidatos y un gráfico de barras. No más. No es un diagnóstico, no es una vacuna, no es una predicción clínica. Es una lista de candidatos priorizados para que un investigador decida dónde poner la lupa primero.

---

## Bloque 3 — El concepto clave: el epítopo

Para entender por qué este proyecto tiene sentido, hay que entender qué es un epítopo, porque es el corazón de todo el dataset.

Cuando el sistema inmune detecta un patógeno, no reacciona contra el patógeno entero. Reacciona contra fragmentos específicos de sus proteínas, fragmentos de apenas unos pocos aminoácidos de longitud. Esos fragmentos se llaman **epítopos**.

Un epítopo es, en cierta forma, la "firma molecular" que el sistema inmune aprende a reconocer. Si una proteína contiene epítopos validados experimentalmente, significa que hay evidencia real de que el sistema inmune humano la detecta. Esa proteína es, por definición, antigénica.

La base de datos que usamos, IEDB, contiene cientos de miles de epítopos identificados en ensayos de laboratorio durante décadas de investigación. Es la mayor colección pública de este tipo en el mundo. Nosotros vamos a usar esa información para construir nuestro dataset: una proteína es positiva si tiene al menos un epítopo validado en IEDB, y negativa si es una proteína del mismo patógeno sin evidencia de antigenicidad.

Esto es importante porque nuestro modelo no aprende de opiniones ni de simulaciones. Aprende de experimentos reales.

---

## Bloque 4 — Por qué este dataset y no otro

IEDB tiene varias propiedades que lo hacen ideal para un proyecto educativo de estas características.

Es gratuito y descargable sin restricciones. Está mantenido por el National Institute of Allergy and Infectious Diseases de Estados Unidos, lo que garantiza su calidad y trazabilidad. Contiene datos experimentales de múltiples patógenos, incluidos SARS-CoV-2 e Influenza A, que son los que usaremos. Y cada epítopo viene acompañado de metadatos que nos permiten rastrear de qué proteína viene y si el resultado del ensayo fue positivo o negativo.

No usamos Kaggle, no usamos datasets sintéticos, no usamos datos de segunda mano. Usamos la fuente primaria que usan los investigadores reales.

---

## Bloque 5 — Qué modelos estudiamos y por qué

El modelo principal es **Random Forest**, y la elección no es arbitraria.

Random Forest funciona bien con datasets pequeños, que es exactamente nuestra situación con entre 500 y 2.000 ejemplos. Es robusto frente al sobreajuste. Y tiene una propiedad pedagógica muy valiosa: produce automáticamente una medida de importancia de cada feature, lo que nos permite responder a la pregunta de qué características fisicoquímicas de una proteína son más relevantes para predecir su antigenicidad. Eso convierte el modelo no solo en una herramienta de predicción sino en una herramienta de comprensión.

Como punto de comparación usaremos un clasificador trivial de mayoría, que simplemente predice siempre la clase más frecuente, y opcionalmente Logistic Regression. Esto nos permite contextualizar los resultados.

No usamos deep learning porque nuestro dataset es demasiado pequeño para aprovecharlo, y porque queremos que el proyecto sea interpretable y explicable, no una caja negra.

---

## Bloque 6 — Qué esperamos obtener, siendo realistas

Seamos honestos con lo que este proyecto puede y no puede hacer.

Lo que esperamos obtener es un modelo con un AUC-ROC entre 0.70 y 0.85, que es un rango razonable para un clasificador binario entrenado con features de secuencia únicamente. Para la demo final, usaremos las proteínas reales del SARS-CoV-2 como Spike, Nucleocápside, Membrana y Envelope, y esperamos que la proteína Spike, que es la más estudiada y la más antigénica, reciba el score más alto. Si eso ocurre, tendremos una validación informal pero visualmente convincente de que el modelo captura algo real.

Lo que no esperamos es superar a herramientas especializadas como VaxiJen, que llevan años de desarrollo y usan métodos más sofisticados. Tampoco esperamos que el modelo generalice perfectamente a patógenos muy distintos de los dos con los que entrenamos.

El valor del proyecto no está en el rendimiento absoluto. Está en haber construido el pipeline completo, haberlo entendido y ser capaces de explicarlo y criticarlo.

---

## Bloque 7 — Por dónde se podría ampliar

El proyecto está diseñado para ser un punto de partida, no un punto final. Las extensiones naturales más accesibles serían las siguientes.

En el corto plazo, añadir un tercer patógeno al dataset, como Mycobacterium tuberculosis, ampliaría la diversidad de los datos y el alcance del modelo. Incorporar features adicionales como la accesibilidad superficial de los aminoácidos, cuando la estructura 3D está disponible en bases de datos como PDB, añadiría información biológicamente relevante.

En el medio plazo, el salto más significativo sería incorporar embeddings de modelos de lenguaje de proteínas como ESM-2 de Meta. Estos modelos, entrenados sobre millones de secuencias de proteínas, capturan información contextual que las features fisicoquímicas simples no pueden ver. Requieren GPU para la inferencia, pero los embeddings se pueden precalcular y reutilizar.

En el largo plazo, la integración con datos de estructura 3D predicha por AlphaFold abriría la puerta a features de accesibilidad superficial que son muy relevantes biológicamente, ya que el sistema inmune solo puede detectar fragmentos que estén expuestos en la superficie de la proteína.

---

## Bloque 8 — Por qué esto importa más allá del aula

La pandemia de COVID-19 mostró con claridad que el tiempo entre la identificación de un patógeno y el desarrollo de una vacuna es uno de los cuellos de botella más críticos en salud pública global. En ese contexto, cualquier herramienta que acelere la fase de priorización de candidatos, aunque sea en días o semanas, tiene valor real.

Las herramientas de screening in silico como la que construimos no reemplazan el laboratorio. Pero sí pueden actuar como un primer filtro que orienta dónde invertir los recursos experimentales más escasos. En un mundo donde el coste de un ensayo de laboratorio puede ser de miles de euros y semanas de trabajo, reducir el espacio de búsqueda inicial tiene un impacto concreto.

Más allá de la aplicación directa, el proyecto ilustra algo que creemos importante: que los datos experimentales acumulados durante décadas por la comunidad científica, depositados en bases de datos abiertas como IEDB, pueden ser reutilizados con herramientas de Machine Learning accesibles para extraer conocimiento nuevo. Eso es ciencia abierta funcionando.

---

## Bloque 9 — Por qué es un buen proyecto de fin de estudios

Este proyecto toca de forma práctica casi todos los conceptos centrales de un curso de Machine Learning: obtención y limpieza de datos reales, ingeniería de features, elección y justificación del modelo, validación correcta con cross-validation estratificada, métricas apropiadas para datasets desbalanceados, interpretabilidad del modelo y despliegue en una interfaz usable.

No es un ejercicio con un dataset de Iris o de precios de casas. Es un problema real, con datos reales, en un dominio con impacto social demostrable. Y al mismo tiempo está acotado de forma que es completamente realizable en el tiempo disponible.

---
