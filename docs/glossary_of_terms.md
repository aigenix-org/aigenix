# Glosario de términos biológicos e inmunológicos

---

## Bloque 1 — La base molecular: de los genes a las proteínas

**1.1. Nucleótido**
La unidad mínima de información genética. Los nucleótidos son las "letras" con las que está escrito el material genético de todos los seres vivos. Cada nucleótido tiene un nombre y se representa con una letra:

- **A** — Adenina
- **T** — Timina
- **G** — Guanina
- **C** — Citosina

Estas letras no se combinan al azar. Siguen una regla estricta de apareamiento: la Adenina (A) siempre se empareja con la Timina (T), y la Citosina (C) siempre se empareja con la Guanina (G). Esta complementariedad es la clave de cómo se copia y se transmite la información genética.

---

**1.2. ADN y ARN**

El **ADN** (ácido desoxirribonucleico) es la molécula que almacena la información genética completa de un organismo. Está formada por dos cadenas largas de nucleótidos (A, T, G, C) que se enrollan entre sí formando la célebre **doble hélice**, la estructura en espiral descubierta por Watson y Crick en 1953. Las dos cadenas están unidas precisamente por los pares A-T y C-G descritos antes. Esta doble estructura hace al ADN muy estable, lo que lo convierte en un soporte fiable para almacenar información a largo plazo. El ADN se encuentra en el núcleo de las células.

El **ARN** (ácido ribonucleico) es una molécula similar al ADN pero con diferencias importantes. En primer lugar, es de **cadena simple**, no doble hélice. En segundo lugar, usa un nucleótido diferente: en el ARN, la Timina (T) es reemplazada por el **Uracilo (U)**, de modo que las letras del ARN son A, U, G y C. El ARN actúa como una copia temporal de trabajo de una parte del ADN: cuando la célula necesita fabricar una proteína, primero copia el fragmento de ADN correspondiente en forma de ARN mensajero, y luego usa ese ARN como instrucción.

Algunos virus, como el **SARS-CoV-2**, no tienen ADN. Su material genético es directamente ARN. Esto tiene implicaciones importantes: el ARN es menos estable que el ADN, lo que hace que estos virus muten con más frecuencia.

> **Resumen comparativo:**
> - ADN: doble hélice, letras A T G C, estable, almacenado en el núcleo celular
> - ARN: cadena simple, letras A U G C, temporal, mensajero de instrucciones

---

**1.3. Gen**
Un gen es un fragmento concreto de ADN (o de ARN en algunos virus) que contiene las instrucciones para fabricar una proteína específica. Si el ADN fuera un libro de recetas, cada gen sería una receta individual. El ser humano tiene aproximadamente 20.000 genes. El SARS-CoV-2 tiene apenas unos 29, cada uno responsable de una de sus proteínas.

---

**1.4. Aminoácido**
La unidad básica de construcción de las proteínas. Existen **20 aminoácidos estándar** en todos los seres vivos, y cada uno tiene propiedades físicas y químicas distintas: algunos son hidrófilos (se disuelven bien en agua), otros hidrófobos (repelen el agua), algunos tienen carga eléctrica positiva, otros negativa. Se representan también con letras: A (alanina), G (glicina), L (leucina), etc.

Una analogía útil: si los nucleótidos son el alfabeto con el que se escribe el ADN, los aminoácidos son el alfabeto con el que se construyen las proteínas. Pero mientras el ADN usa solo 4 letras, las proteínas usan 20.

---

**1.5. Secuencia de aminoácidos**
El orden concreto en que los aminoácidos se encadenan para formar una proteína. Se escribe como una cadena de letras, una por aminoácido, por ejemplo:

```
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
```

Esta secuencia es la entrada principal de nuestro modelo. A partir de ella se calculan todas las features fisicoquímicas.

---

**1.6. Estructura tridimensional de las proteínas (plegamiento proteico)**

Conocer la secuencia de aminoácidos de una proteína es solo el punto de partida. En la realidad biológica, esa cadena lineal de aminoácidos no permanece estirada: se pliega espontáneamente en una estructura tridimensional compacta y específica, como si una cuerda larga se enroscara sobre sí misma adoptando siempre la misma forma final. Este proceso se llama **plegamiento proteico**.

El plegamiento no es aleatorio. Está determinado por las interacciones físicas y químicas entre los aminoácidos de la propia cadena: algunos se atraen, otros se repelen, algunos huyen del agua y se esconden en el interior de la proteína, otros la buscan y quedan expuestos en la superficie. El resultado es una arquitectura tridimensional precisa que define completamente la función de la proteína.

Este concepto es crucial para la inmunología por una razón fundamental: **el sistema inmune no ve la secuencia lineal de la proteína, ve su superficie tridimensional**. Los epítopos que el sistema inmune reconoce son fragmentos que quedan físicamente expuestos en esa superficie plegada. Aminoácidos que en la secuencia lineal están muy alejados entre sí pueden quedar juntos y adyacentes tras el plegamiento, formando un epítopo. Y al contrario: aminoácidos consecutivos en la secuencia pueden quedar completamente enterrados en el interior de la proteína, invisibles para el sistema inmune.

Esto tiene una implicación directa para nuestro proyecto: **las features que usamos se calculan a partir de la secuencia lineal**. No tenemos en cuenta la estructura 3D. Esto es una limitación real y conocida del modelo. Una proteína podría tener características fisicoquímicas que el modelo asocia a antigenicidad, pero si sus epítopos potenciales quedan enterrados tras el plegamiento, no sería reconocida por el sistema inmune.

La herramienta que ha revolucionado la predicción de estructuras 3D es **AlphaFold**, desarrollada por Google DeepMind, que en 2021 resolvió uno de los grandes problemas abiertos de la biología: predecir la estructura tridimensional de una proteína a partir de su secuencia con una precisión casi equivalente a la de experimentos de laboratorio. Incorporar información de estructura 3D predicha por AlphaFold sería una de las extensiones naturales más relevantes de este proyecto, aunque requeriría un nivel de complejidad técnica fuera del alcance actual.

> **En resumen:** la secuencia es el texto escrito de la proteína. La estructura 3D es cómo ese texto se dobla y se convierte en un objeto físico. Y el sistema inmune solo interactúa con el objeto, no con el texto. Nuestro modelo trabaja con el texto, sabiendo que el objeto es lo que realmente importa.

---

**1.7. Proteína**
Una proteína es una cadena de aminoácidos que se pliega en una estructura tridimensional específica (ver 1.6). Ese plegamiento no es aleatorio: está determinado por la secuencia de aminoácidos y por las interacciones físicas y químicas entre ellos. La forma final determina la función. Las proteínas realizan casi todas las funciones de una célula: dan estructura, transportan moléculas, catalizan reacciones químicas, transmiten señales y, en el caso de los virus, permiten infectar células huésped.

---

## Bloque 2 — El patógeno y cómo nos afecta

**2.1. Patógeno**
Cualquier agente biológico capaz de causar enfermedad en un organismo huésped. Los principales tipos son virus, bacterias, hongos y parásitos. Los patógenos relevantes para este proyecto son dos virus: el **SARS-CoV-2** (causante de la COVID-19) y el **virus de la Influenza A** (causante de la gripe estacional). Un virus es esencialmente material genético, ADN o ARN, envuelto en una cápsula de proteínas llamada cápside. No tiene metabolismo propio: para reproducirse necesita infectar una célula viva y secuestrar su maquinaria.

---

**2.2. Proteína Spike**
La proteína de superficie del SARS-CoV-2 que le permite unirse a los receptores de las células humanas e infectarlas. Su nombre viene de su forma de espícula o punta visible al microscopio electrónico en la superficie del virus. Es la proteína más estudiada del coronavirus y el principal objetivo de todas las vacunas contra la COVID-19 desarrolladas hasta la fecha. En nuestra demo final, introduciremos las proteínas reales del SARS-CoV-2 en el sistema y esperamos que la proteína Spike reciba el score de antigenicidad más alto, lo que serviría como validación informal del modelo.

---

**2.3. Antiviral**
Fármaco diseñado para interferir con algún proceso vital del virus: su entrada en la célula, su replicación o el ensamblaje de nuevas partículas virales. A diferencia de las vacunas, que actúan de forma preventiva entrenando al sistema inmune antes de la infección, los antivirales se usan como tratamiento una vez que la infección ya se ha producido. No son el foco de este proyecto, pero forman parte del ecosistema de herramientas médicas en el que se enmarca.

---

## Bloque 3 — El sistema inmune: visión general

**3.1. Respuesta inmune**
El conjunto de mecanismos que el cuerpo humano activa para detectar y eliminar agentes extraños como virus, bacterias u hongos. No es un sistema único sino una red coordinada de células, órganos y moléculas que trabajan juntos. Se divide en dos grandes ramas complementarias: la inmunidad innata y la inmunidad adaptativa.

---

**3.2. Inmunidad innata**
La primera línea de defensa del organismo. Es **rápida** (actúa en minutos u horas), **inespecífica** (responde de la misma forma ante cualquier agente extraño desconocido) y **sin memoria** (cada vez que encuentra un patógeno reacciona igual, sin importar si ya lo ha visto antes). Incluye barreras físicas como la piel, células que engullen y destruyen patógenos, y señales de alarma moleculares que activan la inflamación.

---

**3.3. Receptores de reconocimiento de patrones (PRR) y PAMPs**
Los PRR (*Pattern Recognition Receptors*) son proteínas del sistema inmune innato que detectan estructuras moleculares características de los patógenos, llamadas PAMPs (*Pathogen-Associated Molecular Patterns*, patrones moleculares asociados a patógenos). Un PAMP es una molécula típica de los microbios que las células humanas no poseen, como ciertos tipos de ARN vírico de cadena doble. Cuando un PRR detecta un PAMP, activa inmediatamente la respuesta inflamatoria. Este mecanismo explica por qué el sistema inmune reacciona ante un virus incluso la primera vez que lo encuentra, antes de haber generado anticuerpos específicos.

---

**3.4. Inmunidad adaptativa**
La segunda línea de defensa. Es más **lenta** en arrancar (tarda días o semanas en desarrollarse) pero mucho más **específica** (genera una respuesta dirigida exactamente contra el patógeno concreto) y tiene **memoria inmunológica**. Esta memoria es lo que hace que una segunda exposición al mismo patógeno, o una vacuna, genere una respuesta mucho más rápida y potente. Es la base del funcionamiento de todas las vacunas.

---

## Bloque 4 — Los actores de la inmunidad adaptativa

**4.1. Antígeno**
Cualquier molécula que el sistema inmune adaptativo es capaz de reconocer específicamente y contra la que puede generar una respuesta dirigida. En el contexto de los virus, las proteínas de la superficie del patógeno son los antígenos más relevantes. El término viene de la contracción de "generador de anticuerpos". Es importante notar que antígeno no es sinónimo de patógeno: el patógeno es el agente infeccioso completo, y el antígeno es la molécula concreta de ese patógeno que el sistema inmune reconoce.

---

**4.2. Epítopo**
El fragmento concreto y específico de un antígeno que el sistema inmune reconoce. Un antígeno puede contener muchos epítopos distintos en diferentes partes de su superficie. Los epítopos son fragmentos cortos de la proteína, normalmente de entre 8 y 20 aminoácidos aproximadamente (los epítopos para células T suelen ser más cortos, alrededor de 9–15, mientras que los de células B pueden variar más). Estos fragmentos quedan expuestos en la superficie tridimensional de la proteína y son accesibles para las células del sistema inmune.

Este concepto es el **núcleo de todo nuestro proyecto**: la base de datos IEDB cataloga cientos de miles de epítopos validados experimentalmente, es decir, fragmentos de proteínas para los que existe evidencia real de que el sistema inmune humano los reconoce. A partir de esos datos construimos nuestro dataset.

Una analogía: si una proteína fuera un castillo, el epítopo sería la puerta por la que el sistema inmune intenta entrar. Y el plegamiento 3D de la proteína determina qué puertas están accesibles y cuáles están tapiadas.

---

**4.3. Células B y células T**
Los dos tipos principales de linfocitos, que son las células especializadas de la inmunidad adaptativa. Las **células B** producen anticuerpos y son el eje de la inmunidad humoral. Las **células T** tienen dos funciones principales: coordinar y amplificar la respuesta inmune (células T colaboradoras) y destruir directamente las células del organismo que han sido infectadas por el virus (células T citotóxicas). Ambas reconocen epítopos, pero de formas distintas y en contextos diferentes.

---

**4.4. Inmunidad humoral**
La rama de la inmunidad adaptativa mediada por anticuerpos, producidos y secretados por las células B. El término "humoral" hace referencia a los fluidos corporales (sangre, linfa) en los que circulan los anticuerpos. Es especialmente eficaz para neutralizar patógenos que aún están en el espacio extracelular, antes de que entren en las células.

---

**4.5. Inmunidad celular**
La rama de la inmunidad adaptativa mediada por células T. En lugar de secretar anticuerpos, las células T reconocen y destruyen directamente las células del organismo que ya han sido infectadas por el virus y están fabricando proteínas virales en su interior. Complementa a la inmunidad humoral atacando el problema desde dentro.

---

## Bloque 5 — El reconocimiento molecular: anticuerpos y sus partes

**5.1. Anticuerpo**
Proteína producida por las células B en respuesta a un antígeno específico. Tiene forma característica de Y y se une al antígeno con una precisión extraordinaria. Esta unión puede neutralizar directamente al patógeno, impidiendo que infecte nuevas células, o marcarlo para que otras células del sistema inmune lo destruyan. Cada anticuerpo reconoce un único epítopo específico. Una persona puede producir millones de anticuerpos distintos, cada uno dirigido contra un epítopo diferente.

---

**5.2. Parátopo**
La región del anticuerpo que se une físicamente al epítopo. Si el epítopo es la cerradura, el parátopo es la llave. La complementariedad entre ambos, en forma y en carga eléctrica, determina la especificidad y la fuerza de unión. Aunque nuestro modelo no predice parátopo, entender este concepto ayuda a comprender por qué la secuencia y las propiedades fisicoquímicas de una proteína son informativas sobre su capacidad de ser reconocida.

---

**5.3. Receptor de antígeno**
Proteína de superficie de los linfocitos que reconoce específicamente un antígeno o epítopo. En las células B se llama BCR (*B Cell Receptor*) y en las células T, TCR (*T Cell Receptor*). Cada linfocito individual tiene un receptor con una especificidad única. El sistema inmune genera una diversidad enorme de receptores distintos para poder reconocer potencialmente cualquier patógeno, incluidos los que nunca ha encontrado antes.

---

**5.4. Neutralización viral**
Proceso por el que los anticuerpos se unen a proteínas clave del virus, como la proteína Spike del SARS-CoV-2, e impiden que este infecte células nuevas, bloqueando físicamente su capacidad de unirse a los receptores celulares. Los anticuerpos neutralizantes son considerados el correlato de protección más importante en muchas vacunas virales. Generar anticuerpos neutralizantes potentes y duraderos es uno de los objetivos principales del diseño de vacunas.

---

## Bloque 6 — Conceptos específicos del proyecto

**6.1. Proteína antigénica y evidencia de antigenicidad**
Una proteína se considera antigénica cuando contiene epítopos capaces de activar el sistema inmune adaptativo y existe evidencia experimental que lo confirma. En nuestro proyecto, etiquetamos una proteína como antigénica (label = 1) si tiene al menos un epítopo validado en IEDB con resultado positivo en un ensayo de laboratorio. Sin esa evidencia experimental, no podemos afirmar que una proteína sea antigénica aunque tenga características fisicoquímicas similares a otras que sí lo son. La evidencia experimental es lo que convierte una hipótesis en un dato.

---

**6.2. Score de antigenicidad**
Valor numérico entre 0 y 1 que nuestro modelo asigna a cada proteína como estimación de la probabilidad de que sea antigénica. Un score cercano a 1 indica alta probabilidad predicha, y un score cercano a 0 indica baja probabilidad. Es fundamental entender que este score no es una certeza clínica sino una **priorización estadística** basada en patrones aprendidos de datos experimentales previos. Su utilidad es orientar dónde invertir los esfuerzos experimentales primero, no reemplazar esos experimentos.

---

**6.3. Peso molecular**
La masa de una proteína, expresada en Daltons (Da) o kiloDaltons (kDa). Se calcula como la suma de las masas individuales de todos sus aminoácidos. Las proteínas más grandes tienden a tener más superficie expuesta y potencialmente más epítopos, aunque la relación no es directa ni simple. Es una de las features numéricas que nuestro modelo usa para hacer sus predicciones.

---

**6.4. Punto isoeléctrico**
El valor de pH al que la carga eléctrica neta de una proteína es exactamente cero. Por encima de ese pH la proteína adquiere carga negativa, y por debajo, carga positiva. Esta propiedad influye en cómo la proteína interactúa con otras moléculas en el entorno celular, incluidas las células del sistema inmune. Es una de las features de nuestro modelo.

---

**6.5. Hidrofobicidad media (índice GRAVY)**
Medida del carácter hidrófobo (repelente al agua) o hidrófilo (afín al agua) de una proteína en su conjunto. Se calcula como el promedio de los índices de hidrofobicidad de cada uno de sus aminoácidos. Un valor positivo indica que la proteína es, en promedio, más hidrófoba; un valor negativo indica que es más hidrófila.
Las partes de las proteínas que quedan expuestas al exterior del virus (en contacto con el agua del organismo) suelen ser más hidrófilas (valores GRAVY más bajos o negativos). Es una de las features de nuestro modelo.
GRAVY son las siglas de *Grand Average of Hydropathicity*.

---
