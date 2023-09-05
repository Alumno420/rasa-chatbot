# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

# Para eliminar las tildes
import unidecode

# Para poder tratar el .sqlite que funciona como DB
import sqlite3

# clase para obtener los datos del documento .xlsx con respuestas
class manager_dataDB:
    def __init__(self, table: str, db: str):

        self.table = table
        self.db = db
        self.nombre_columnas = []
        self.data_dict = {}
        # Establecer una conexiÃ³n a la base de datos SQLite
        try:
            self.conn = sqlite3.connect(self.db)  # Reemplaza 'data.sqlite' con el nombre de tu archivo SQLite
        except sqlite3.Error as e:
            print("Error al conectar SQLite3:", e)
            exit(1)

        self.cursor = self.conn.cursor()

        # Obtener los nombres de las columnas de la tabla
        consulta_columnas = f"PRAGMA table_info({self.table});"

        try:
            self.cursor.execute(consulta_columnas)
            columnas = self.cursor.fetchall()
        except sqlite3.Error as e:
            print("Error al obtener las columnas:", e)
            self.conn.close()
            exit(1)

        for columna in columnas:
            self.nombre_columnas.append(columna[1])

            consulta_valores = f"SELECT \"{columna[1]}\" FROM data;"  # Reemplaza 'columna2' y 'nombre_tabla' segÃºn corresponda
            try:
                self.cursor.execute(consulta_valores)
                valores = self.cursor.fetchall()
                self.data_dict[columna[1]] = list(valores)
            except sqlite3.Error as e:
                print(f"Error al acceder la tabla {self.table} en 3 {self.db} :", e)
                self.conn.close()
                exit(1)

        self.conn.close()

    def obtener_index_columna(self, clave):
        if isinstance(clave, int):
            return None

        else:
            for i in self.data_dict.keys():

                if i == clave:
                    index = i
                    return index
            print(f"Error: La columna '{clave}' no existe en el archivo '{self.path}'")
            return None

    def obtener_index_fila(self, clave):
        if isinstance(clave, int):
            return clave

        else:
            for i in range(len(self.data_dict[self.nombre_columnas[0]])):

                if list(self.data_dict[self.nombre_columnas[0]][i])[0] == clave:
                    index = i
                    return index


            print(f"Error: La clave '{clave}' no existe en la DB '{self.db}'")
            return None

    def obtener_valor(self,columna, clave):
        if self.obtener_index_fila(clave) != None and self.obtener_index_columna(columna) != None:
            return list(self.data_dict[columna][self.obtener_index_fila(clave)])[0]

        else:
            print(f"Error: La columna '{columna}' y clave '{clave}' no existen en el archivo '{self.path}'")
            return None

    def obtener_valores_columna(self, columna):
        if columna not in self.data_dict:
            print(f"Error: La columna '{columna}' no existe en la DB '{self.db}'")
            return None

        output = []
        for i in self.data_dict[columna]:
            if list(i) != [''] :
                output.append(list(i)[0])
        return output

    def obtener_valores_fila(self, fila):
        output = []

        for columna in self.nombre_columnas:
            if list(self.data_dict[columna][self.obtener_index_fila(fila)])[0] != '':
                output.append(list(self.data_dict[columna][self.obtener_index_fila(fila)])[0])
        # Se elimina el primer elemento, porque contiene el nombre de la fila
        output.pop(0)
        return output

# el archivo .xlsx que contiene las respuestas, estÃ¡ en el mismo directorio
# que este archivo actions.py
data = manager_dataDB("data", "dataDB.sqlite")

# esto esrÃ¡ para evitar que el chatbot responda dos veces
was_submitted = False

# ['matematicas', 'tecnologia', 'fisica', 'aleman', 'biologia', 'dibujo artistico', 'dibujo tecnico', 'frances', 'historia', 'quimica', 'tic', 'geologia', 'literatura', 'lengua', 'lingua', 'musica', 'ingles', 'filosofia', 'economia']
# la materias que contiene la DB en .xlsx
ALLOWED_SUBJECTS = data.obtener_valores_fila("ASIGNATURA")

# ['resumen', 'examenes', 'libros', 'competencias', 'profesores', 'contenidos', 'metodologia', 'requisitos', 'dedicacion', 'evaluacion', 'universidad', 'horas', 'proyectos', 'extracurriculares', 'practicas']
# los tipos de datos que contiene la DB en .xlsx
ALLOWED_DATA_TYPES = data.obtener_valores_columna("TIPO_DATO")

# Los print("[DEBUG] ...") se muestran solo en la terminal que contiene
# el hilo con el syscall a `rasa run actions` que monta el server que procesa la custom actions

# Clase para cuando el chatbt no ha entendido nada (no pilla el intent),
# hereda de rasa_sdk.Action porque es del action nlu_fallback
class ActionDefaultFallback(Action):
    def name(self) -> Text:
            return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
            # output de un mensaje de que no se ha entendido el user input
            message = "Disculpe usted, no le he entendido."
            dispatcher.utter_message(text=message)
            # se deshace la Ãºltima interacciÃ³n del usuario
            return [UserUtteranceReverted()]

# Clase para validar si la asignatura y el tipo_dato pedidos se encuentran tratados en la DB
class ValidateAsignaturaTipoDatoForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_asignatura_tipo_dato_form"

    def validate_asignatura(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        subjects = ', '.join(ALLOWED_SUBJECTS)
        asignaturas_Input = []
        tipo_dato_Input = []
        in_Input = False
        global was_submitted
        if was_submitted == True:
            print("[DEBUG] Ya fue submitted: ", was_submitted)

        # eliminar duplicados
        slot_value_purged = []
        for i in slot_value:
            if i not in slot_value_purged:
                slot_value_purged.append(i)

        print("[DEBUG] slot_value_purged: ", slot_value_purged)
        tmp1 = []
        for i in range(len(slot_value_purged)):
            if slot_value_purged[i] not in ALLOWED_SUBJECTS:
                j = slot_value_purged[i].split()
                for k in j:
                    if k in ALLOWED_SUBJECTS:
                        tmp1.append(k)
            if slot_value_purged[i] in ALLOWED_SUBJECTS:
                tmp1.append(slot_value_purged[i])

        # obtener las asignaturas que pidiÃ³ el usuario obtenido su correspondencia a las ALLOWED
        for asignat in slot_value_purged:
            input = asignat.lower()
            # Eliminar tildes
            input = unidecode.unidecode(input)
            for lista in ALLOWED_SUBJECTS:
                if input in lista:
                    asignaturas_Input.append(lista)
                    in_Input = True
                    break

        print("[DEBUG] asignaturas_Input: ", asignaturas_Input)

        # Caso en el que la asignatura dada no estÃ© en la DB
        if in_Input == False:
            #dispatcher.utter_message(text=f"De momento solo puedo informarle sobre las siguientes asignaturas: {subjects}")
            return {"asignatura": None}

        # Para comprobar si ya se tiene el tipo_dato, en caso negativo se pide, en caso positivo se muestra la info solicitada
        slot_tipo_dato = tracker.get_slot("tipo_dato")
        if slot_tipo_dato == None:
            dispatcher.utter_message(text=f"Ahora necesito que usted me diga el tipo de dato que desea.")
        else:
            # eliminar duplicados
            slot_value_purged = []
            for i in slot_tipo_dato:
                if i not in slot_value_purged:
                    slot_value_purged.append(i)

            # obtener las correspondecias de los tipos_dato en ALLOWED
            for tipoDato in slot_value_purged:
                input = tipoDato.lower()
                # Eliminar tildes
                input = unidecode.unidecode(input)
                for lista in ALLOWED_DATA_TYPES:
                    if input in lista:
                        tipo_dato_Input.append(lista)
                        in_Input = True
                        break
            print("[DEBUG] slot_value_purged (2), was_submitted: ", slot_value_purged, was_submitted)

            if was_submitted == False:
                print("[DEBUG] Ahora se hizo el was_submitted")
                was_submitted = True
                for asignatura in asignaturas_Input:
                    for tipoDato in tipo_dato_Input:
                        asignatura = asignatura.lower()
                        asignatura = unidecode.unidecode(asignatura)
                        tipoDato = tipoDato.lower()
                        tipoDato = unidecode.unidecode(tipoDato)
                        print("[DEBUG] i (asignaturas_Input),j (slot_value_purged): ", asignatura, tipoDato)
                        dispatcher.utter_message(text=f"{data.obtener_valor(asignatura,tipoDato)}\n\n")

        return {"asignatura": asignaturas_Input}

    def validate_tipo_dato(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validar el tipo de dato

        datas = ','.join(ALLOWED_DATA_TYPES)
        subs = ','.join(ALLOWED_SUBJECTS)
        tipos_dato_Input = []
        in_Input = False
        global was_submitted
        slot_value_purged = []
        asignaturas_Input = []

        # Comprobar si todavÃ­a no se ha dado el valor de la asignatura
        slot_asignatura = tracker.get_slot("asignatura")
        if slot_asignatura == None:
            #dispatcher.utter_message(text=f"Ahora necesito que usted me diga la asignatura que le interesa de estas: {subs}")
            pass
        else:
            # eliminar duplicados en asignatura
            slot_value_purged = []
            for i in slot_asignatura:
                if i not in slot_value_purged:
                    slot_value_purged.append(i)

        # obtener las asignaturas que pidiÃ³ el usuario obtenido su correspondencia a las ALLOWED
        for asignat in slot_value_purged:
            input = asignat.lower()
            # Eliminar tildes
            input = unidecode.unidecode(input)
            for lista in ALLOWED_SUBJECTS:
                if input in lista:
                    asignaturas_Input.append(lista)
                    in_Input = True
                    break

        slot_asignatura = asignaturas_Input
        print("[DEBUG] slot_asignatura: ", slot_asignatura)

        # eliminar duplicados en tipo_dato
        slot_value_purged = []
        for i in slot_value:
            if i not in slot_value_purged:
                slot_value_purged.append(i)

        print("[DEBUG] slot_value_purged: ", slot_value_purged)

        # obtener los tipo_dato que pidiÃ³ el usuario obtenido su correspondencia a las ALLOWED
        for tipoDato in slot_value_purged:
            input = tipoDato.lower()
            # Eliminar tildes
            input = unidecode.unidecode(input)

            for lista in ALLOWED_DATA_TYPES:
                if input in lista:
                    tipos_dato_Input.append(lista)
                    in_Input = True
                    break

        print("[DEBUG] tipos_dato_Input & in_Input, was_submitted: ", tipos_dato_Input, in_Input, was_submitted)

        if slot_asignatura == None and in_Input == False:
            dispatcher.utter_message(text=f"No tengo {slot_value_purged} como tipo de dato, tengo datos de {datas}. Primero necesito que usted me diga la asignatura que le interesa.")
            return {"tipo_dato": None}

        if in_Input == False and slot_asignatura != None:
            dispatcher.utter_message(text=f"No tengo {slot_value} como tipo de dato de {slot_asignatura}, tengo datos de {datas}.")
            return {"tipo_dato": None}

        if slot_asignatura == None and in_Input == True:
            dispatcher.utter_message(text=f"Tengo {slot_value} como tipo de dato, pero primero necesito que usted me diga la asignatura que le interesa.")
            return {"tipo_dato": slot_value}

        if was_submitted == False:
            print("[DEBUG] Ahora se hizo el was_submitted")
            was_submitted = True
            for asignatura in slot_asignatura:
                for tipoDato in tipos_dato_Input:
                    asignatura = asignatura.lower()
                    asignatura = unidecode.unidecode(asignatura)
                    tipoDato = tipoDato.lower()
                    tipoDato = unidecode.unidecode(tipoDato)
                    print("[DEBUG] i (slot_asignatura),j (slot_value_purged): ", asignatura, tipoDato)
                    dispatcher.utter_message(text=f"{data.obtener_valor(asignatura,tipoDato)}\n\n")

        # Se supone que esta funciÃ³n se llama siempre despuÃ©s de la primera,
        # entonces despuÃ©s de que se ejecute esta se entiene que se va a hacer un nuevo submit en el siguiente input
        # por ello se vuelve a activar la capacidad de submit con was_submittd = False
        if was_submitted == True:
            was_submitted = False

        return {"tipo_dato": slot_value}

# Para evitar que el usuario siga preguntando y el chatbot responda info ya preguntada
class ActionResetAllSlots(Action):
    def name(self):
        return "action_reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("asignatura", None), SlotSet("tipo_dato", None)]
