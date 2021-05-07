from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import smtplib


global l
l=[]

class ActionSaveName(Action):

	def name(self) -> Text:
		return "action_save_name"
	
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		name= tracker.get_slot("name")
		l.append(name)
		dispatcher.utter_message(text="Thank you, {}".format(name))
		return []

class ActionSaveNumber(Action):

	def name(self) -> Text:
		return "action_save_number"
	
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		number= tracker.get_slot("number")
		l.append(number)
		dispatcher.utter_message(text="Thank you, {}".format(number))
		return []

class ActionSaveNote(Action):

	def name(self) -> Text:
		return "action_save_note"
	
	def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker,
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		note= tracker.get_slot("note")
		l.append(note)
		s="Name- "+l[0]+"\nNumber- "+l[1]+"\nMessage- "+l[2]
		l.clear()
		server=smtplib.SMTP_SSL("smtp.gmail.com",465)
		server.login("smartdoorbot@gmail.com","smartdoorv1")
		server.sendmail("smartdoorbot@gmail.com","amishtp652@hotmail.com",s)
		server.quit()
		
		dispatcher.utter_message(text="Thank you, {}".format(note))
		return []