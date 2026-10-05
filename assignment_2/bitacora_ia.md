# **Parte 4 – Bitácora de IA**

## 1. ¿Qué le pidieron a la IA?
**a)** Le pedí que me ayudara a crear los issues siguiendo las indicaciones del mismo issue de la tarea.

**b)** Que arme la tabla de documentos obtenidos del scraping en gob.pe, siguiendo las indicaciones del issue.

**c)** Que me ayudara a armar la función para geocodificar las capitales con la API de Open-Meteo.

## 2. ¿Qué les respondió? (copien la parte relevante)
**a)** "Incluí un enlace al issue de la clase en la descripción de cada uno de los cuatro issues."

**b)** "fecha": article.find_element(By.CSS_SELECTOR, "span").text.strip()

**c)** r = requests.get(URL_GEOCODIFICACION, params=parametros, timeout=30) 
elegido = r.json()["results"][0]

## 3. ¿Qué estaba mal y cómo se dieron cuenta?
**a)** No debía de citar directamente al issue de la tarea, me di cuenta al revisar el issue del assignment_2 y ver que se veía públicamente que yo la había citado en 4 issues míos.

**b)** En la columna fecha salía literalmente "Normas y documentos legales" en todas las filas, en lugar de lo que viene después de "Publicado:", me di cuenta rápido al observar la tabla y ver que ninguna fila tenía una fecha real.

**c)** Tomaba el primer resultado a ciegas aunque fuera de otro país, me di cuenta al revisar `country_code` y `admin1` y ver que, por ejemplo, para "Chachapoyas" devolvía la destilería de Argentina y para nombres como Lima o Trujillo devolvía ciudades de EE. UU. o Venezuela.

## 4. ¿Cómo lo corrigieron?
**a)** Le pedí a la IA información de cómo restablecer eso, y me dijo que solo debía de eliminar los 4 issues creados en mi repositorio, y lo hice manualmente.

**b)** Le volví a pedir el código para sacar solo la fecha que empieza con "Publicado:", y me devolvió el código con el XPath `.//span[starts-with(normalize-space(.), 'Publicado:')]`, lo cambié manualmente y verifiqué que la tabla ya mostrara las fechas como tal.

**c)** Le volví a pedir el código para quedarse solo con resultados de Perú, y me devolvió el código que recorre la lista y devuelve el primero con `country_code == "PE"`, lo cambié manualmente con las funciones `primero_en_peru` y `normalizar` y verifiqué que las 25 capitales quedaran en el Perú y en su departamento.
