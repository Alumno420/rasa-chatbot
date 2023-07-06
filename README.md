# rasa-chatbot: mi proyecto de STEMBach

# Eichhörnchen Tissot Projekt

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

### Árbol de archivos
- **actions**
	- ***actions.py*** : este archivo tiene el código de las acciones custom para run()

- **data**
	- ***nlu.yml*** : en este fichero se puede encontrar una serie de intents. Cada uno de los intents hace referencia posible acción del usuario.
	- ***rule.yml*** : las reglas describen fragmentos breves de conversaciones que siempre deben seguir el mismo camino.
	- ***stories.yml*** : distintos escenarios que pueden ocurrir. Contiene un nombre, unos intents del usuario con sus correspondientes nombres y las actions que ejecuta el chatbot cuando se dan.

- **models**
	- Contiene las versiones del modelo entrenado y listo. Comprimido en `.tar.gz`

- **tests**
	- ***test_stories.yml*** : este archivo contiene tests para evaluar que el chatbot se comporta como debe

- **config.yml** : contiene la configuración del chatbot en:
	- **NLU**
		* [language](https://rasa.com/docs/rasa/nlu/components/) 
		* [pipeline](https://rasa.com/docs/rasa/tuning-your-model)
	- **Rasa Core**
		* [policies](https://rasa.com/docs/rasa/core/policies/)

- **credentials.yml** : contiene credenciales para las plataformas de voz y chat

- **domain.yml** : aquí se especifican los intents, entities, spaces y actions que se han deifinido que el chatbot conoce y maneja
	* **intents:** se indican las intenciones definidas en el fichero nlu.md, representan las posibles peticiones que puede hacer el usuario
	* **entities**: variables que se van modificando conforme avanza el diálogo entre el usuario y el chatbot.
	* **slots**: se utilizan para almacenar información proporcionada por el usuario. Cada slot definido en domain.yml consiste en una clave a la cual se le asignará posteriormente un valor determinado.
	* **responses**: en este apartado se encuentran mensajes que le aparecerán al usuario por el chatbot.
	* **actions**: acciones ejecutadas por el chatbot como respuesta al mensaje del usuario.
	* **forms**: formularios utilizados por el chatbot.

- **endpoints.yml** :  contiene los diferentes endpoints que el chatbot puede usar (DB)

------------

## Orden de operación del chatbot Eichhörnchen Tissot

1. Saludar al usuario y pedir su nombre
	- Esperar el saludo del usuario y su nombre

2. Pedir al usuario con su nombre en qué le puedo ayudar
	- El usuario menciona `información` sobre `asignatura`
	- El chatbot detecta y almacena en el slot la información y procede a mostrarla
	- El chatbot pregunta si quieres más información de la asignatura y presenta opciones
	- El usuario responde cuál quiere o responde no.
3. El chatbot le pregunta al usuario si quiere conocer información de alguna o otra asignatura
	- El usuario confirma y dice el nombre
	- EL usuario niega
4. El chatbot se despide
	- El usuario se despide

### Diagrama del story de la conversación
                    
```flow
start=>start: Start
end=>end
op=>operation: Saludo & nombre
cond=>condition: Nombre sí o No?
io=>inputoutput: Entitie nombre y almacenar en slot
op2=>operation: Preguntar qué ayudar
cond2=>condition: Opcion & Asignatura sí o no
op3=>operation: Mostrar lo pedido
io2=>inputoutput: Obtner los entities y almacernarlos en slots
cond3=>condition: Preguntar por más info de la asginatura
cond4=>condition: Elegir el tipo de info de la asginatura
io3=>inputoutput: Obtner el tipo de info y almacenarlo en el slot
cond5=>condition: Info de otra asignatura?
op5=>operation: Despedida

start->op->cond
cond(no)->op
cond(yes)->io
io->op2
op2->cond2
cond2(no)->op2
cond2(yes)->io2
io2->op3
op3->cond3
cond3(yes)->cond4
cond3(no)->op2
cond4(yes)->io3
cond4(no)->end
io3->cond5
cond5(yes)->cond2
cond5(no)->op5
op5->end



```
