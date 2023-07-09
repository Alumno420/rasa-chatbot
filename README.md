# rasa-chatbot: mi proyecto de STEMBach
![Demo Chatbot](https://raw.githubusercontent.com/Alumno420/rasa-chatbot/main/DEMO-chatbot.png)  
### Instalación:
La última versión oficial de Rasa 6.0 tiene demasiados bugs, por lo que hay que empezar downgrading:

`pip install rasa[full]==3.5.0`

Instalar la librería de modelos de AI para texto preentrenados:

`pip install -U pip setuptools wheel`

`pip install -U spacy`

Para el modelo transformer pre entrenado en español:

`python -m spacy download es_core_news_md` 

Clonar este repositorio:

`git clone https://github.com/Alumno420/rasa-chatbot.git`

Viajar dentro del directorio del repositorio y ejecutar:

`rasa train`

`rasa shell` o `rasa interactive`

Si se tiene descargado el último release del model entrenado se puede evitar el `rasa train`:

`rasa shell --model <directorio_nombre_trained_model.tar.gz>`

## Utilidad del Chatbot
Este chatbot de Rasa fue creado para responder preguntas que podría tener los alumnos de 2º de bachillerato sobre las asignaturas.

Actualmente (release v1.5 Beta Central Volume) el chatbot puede responder preguntas del usuario sobre datos de: 
- `resumen`
- `examenes`
- `libros`
- `competencias`
- `profesores`
- `contenidos`
- `metodologia`
- `requisitos`
- `dedicacion`
- `evaluacion`
- `universidad`

sobre las asignaturas:
- `matematicas`
- `tecnologia`
- `fisica`


## Árbol de archivos
- **actions**
	- ***actions.py*** : este archivo tiene el código de las acciones custom para run(). Leer los comentarios en el archivo para conocer todo lo que hace.
   	- ***dataDB.xlsx*** : este archivo funciona como DB de la información que puede proporcionar el cahtbot. No se usó .csv por su falta de soporte por defecto de Unicode, ya que usa el formato ANSI.

- **data**
	- ***nlu.yml*** : en este fichero se puede encontrar una serie de intents. Cada uno de los intents hace referencia posible acción del usuario.
	- ***rule.yml*** : las reglas describen fragmentos breves de conversaciones que siempre deben seguir el mismo camino.
	- ***stories.yml*** : distintos escenarios que pueden ocurrir. Contiene un nombre, unos intents del usuario con sus correspondientes nombres y las actions que ejecuta el chatbot cuando se dan.

- **models**
	- Contiene las versiones del modelo entrenado y listo. Comprimido en `.tar.gz`. Al pesar más de 25MB no está en este repo, pero se puede obtener el último modelos entrenado estable en [releases](https://github.com/Alumno420/rasa-chatbot/releases/tag/v1.0-beta-snowy-trainer)

- **tests**
	- ***test_stories.yml*** : este archivo contiene tests para evaluar que el chatbot se comporta como debe

- **config.yml** : contiene la configuración del chatbot en:
	- **NLU**
		* [language](https://rasa.com/docs/rasa/nlu/components/) 
		* [pipeline](https://rasa.com/docs/rasa/tuning-your-model)
	- **Rasa Core**
		* [policies](https://rasa.com/docs/rasa/core/policies/)

- **credentials.yml** : contiene credenciales para las plataformas de voz y chat, que no se usan en este caso. 

- **domain.yml** : aquí se especifican los intents, entities, spaces y actions que se han deifinido que el chatbot conoce y maneja
	* **intents:** se indican las intenciones definidas en el fichero nlu.md, representan las posibles peticiones que puede hacer el usuario
	* **entities**: variables que se van modificando conforme avanza el diálogo entre el usuario y el chatbot. Solo se usan `nombre`, `asignatura` y `tipo_dato`
	* **slots**: se utilizan para almacenar información proporcionada por el usuario. Cada slot definido en domain.yml consiste en una clave a la cual se le asignará posteriormente un valor determinado.
	* **responses**: en este apartado se encuentran mensajes que le aparecerán al usuario por el chatbot.
	* **actions**: acciones ejecutadas por el chatbot como respuesta al mensaje del usuario.
	* **forms**: formularios utilizados por el chatbot. Solo se usa uno que obtiene los valores para `asignatura` y `tipo_Dato`

- **endpoints.yml** :  contiene los diferentes endpoints que el chatbot puede usar (DB). IMPORTANTE: contiene la salida a la que se envían las acciones (el server en el _localhost_ que monta `rasa run actions`)

------------

## Orden de operación del chatbot

1. Saludar al usuario y pedir su nombre
	- Esperar el saludo del usuario y su nombre

2. Pedir al usuario con su nombre en qué se le puede ayudar
	- El usuario menciona `tipo_dato` sobre `asignatura`
	- El chatbot los detecta, activa el `form` y almacena en el `slot` la información
	- El chatbot obtiene la información solicitada en la DB `dataDB.xlsx`
	- El chatbot muestra un mensaje con la información solicitada

3. El usuario lo agradece
	- El chatbot dice `De nada`

4. El usuario se despide
	- El chatbot se despide
	
## Notas del útlimo release:
## Beta v1.5: **Central Volume**
## Segundo release beta del rasa-chatbot de mi trabajo de STEMBach.
### Novedades:
- Añadidas en el `nlu.yml` más ejemplos en los lookup tables para el `RegexEntityExtractor` con los posibles valores de `tipo_dato` y `asignatura` que contiene la DB
- Añadidos más ejemplos del _intent_ de `informar` y de `agradecer`
- Corregido un bug en `actions.py` por no usar las _keys_ de los diccionarios que contienen los `tipos_dato` y `asignaturas` para así poder después acceder correctamente a las columnas y filas de la DB, yaq ue las _keys_ son iguales a ellas.
- Añadidas a la DB los siguientes `tipo_dato` : _requisitos_, _dedicacion_, _evaluacion_ y _universidad_
- Añadidos en el _intent_ "informar" de `nlu.yml` ejemplos para detectar correctamente los nuevos valores que pueden tomar los _entitites_

**Full Changelog**: https://github.com/Alumno420/rasa-chatbot/compare/v1.0-beta-snowy-trainer...v1.5-beta-central-volume
