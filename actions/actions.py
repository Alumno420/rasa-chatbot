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

ALLOWED_SUBJECTS = ["tecnología", "tecnologia", "matemáticas", "matematicas", 
                    "física", "fisica"]
ALLOWED_DATA_TYPES = ["profesores", "profesor", "exámenes", "examenes"]

class ActionDefaultFallback(Action):
    def name(self) -> Text:
            return "action_default_fallback"
    def run(self, dispatcher, tracker, domain):
            # output de un mensaje de que no se ha entendido el user input
    
            message = "Disculpe, no le he entendido."
            dispatcher.utter_message(text=message)
            # se deshace la última interacción del usuario
            return [UserUtteranceReverted()]

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
        # Validar si la asignatura pedida se encuentra tratada
        subjects = []
        for i in range(len(ALLOWED_SUBJECTS)):
                if i % 2 != 0:
                    subjects.append(ALLOWED_SUBJECTS[i])
        subjects = ', '.join(subjects)
        if slot_value.lower() not in ALLOWED_SUBJECTS:
        
            dispatcher.utter_message(text=f"De momento solo puedo informarte sobre las siguientes asignaturas: {subjects}")
            return {"asignatura": None}
        dispatcher.utter_message(text=f"OK! Entonces te interesa la materia {slot_value}.")
        return {"asignatura": slot_value}

    def validate_tipo_dato(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validar el tipo de dato
        slot_asignatura = tracker.get_slot("asignatura")
        
        if slot_asignatura == None and slot_value.lower() not in ALLOWED_DATA_TYPES:
            dispatcher.utter_message(text=f"No tengo {slot_value.lower()} como tipo de dato, tengo datos de {','.join(ALLOWED_DATA_TYPES)}. Primero necesito que me digas la asignatura que te interesa.")
            return {"tipo_dato": None}

        if slot_value.lower() not in ALLOWED_DATA_TYPES and slot_asignatura != None:
            dispatcher.utter_message(text=f"No tengo {slot_value.lower()} como tipo de dato de {slot_asignatura}, tengo datos de {','.join(ALLOWED_DATA_TYPES)}.")
            return {"tipo_dato": None}
        
        if slot_asignatura == None and slot_value.lower() in ALLOWED_DATA_TYPES:
            dispatcher.utter_message(text=f"Tengo {slot_value.lower()} como tipo de dato, pero primero necesito que me digas la asignatura que te interesa.")
            return {"tipo_dato": slot_value}

        dispatcher.utter_message(text=f"OK! Le voy a informar sobre {slot_value} de {slot_asignatura}.")
        return {"tipo_dato": slot_value}
