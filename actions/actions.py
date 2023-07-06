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
            # tracker pausado y se deshace la última interacción del usuario
            return [ConversationPaused(), UserUtteranceReverted()]

class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_asignatura_tipo_dato_form"

    def validate_subject(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validar si la asignatura pedida se encuentra tratada
        if slot_value.lower() not in ALLOWED_SUBJECTS:
            subjects = ', '.join(ALLOWED_SUBJECTS[:-1]) + ' y ' + ALLOWED_SUBJECTS[-1]
            dispatcher.utter_message(text=f"De momento solo puedo informarte sobre las siguientes asignaturas: {subjects}")
            return {"asignatura": None}
        dispatcher.utter_message(text=f"OK! Entonces te interesa la materia {slot_value}.")
        return {"asignatura": slot_value}

    def validate_data_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Validar el tipo de dato

        if slot_value.lower() not in ALLOWED_DATA_TYPES:
            dispatcher.utter_message(text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}.")
            return {"tipo_dato": None}
        slot_asignatura = tracker.get_slot("asignatura")
        dispatcher.utter_message(text=f"OK! Le voy a informar sobre {slot_value} de {slot_asignatura}.")
        return {"tipo_dato": slot_value}
