

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this gutrans_ide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List,Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.events import SlotSet, EventType
import mysql.connector
import xlwt
from xlwt import Workbook

class ActionHello(FormAction):
    def name(self) -> Text:
        return "app_form"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        #print("required_slots(tracker: Tracker)")
        return ["trans_id","date","state"]
    def validate(self, dispatcher, tracker, domain):
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
        for slot, value in slot_values.items():
         if slot == 'trans_id':
            if value is None:
                dispatcher.utter_template('utter_ask_trans_id', tracker)
                slot_values[slot] = None
            else:
                dispatcher.utter_message("trans_id date is {}".format(value))
         elif slot == 'date':
            if value is None:
                dispatcher.utter_template('utter_ask_date', tracker)
                slot_values[slot] = None
         elif slot == 'state':
            if value is None:
               dispatcher.utter_template('utter_ask_state', tracker)
               slot_values[slot] = None
        return [SlotSet(slot, value) for slot, value in slot_values.items()]
    def slot_mappings(self) -> Dict[Text,Union[Dict, List[Dict]]]:
        return {
        "trans_id": self.from_entity(entity="trans_id",intent='query'),
        "date": self.from_entity(entity="date",intent='query'),
        "state": self.from_entity(entity="state",intent='query')
    }
    def submit(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any],
           ) -> List[Dict]:
     trans_id=tracker.get_slot('trans_id')
     date=tracker.get_slot('date')
     state=tracker.get_slot('state')
     dispatcher.utter_message(template="utter_submit", trans_id=tracker.get_slot('trans_id'),date=tracker.get_slot('date'),state=tracker.get_slot('state'))
     dispatcher.utter_message(
        "Hey, your report date is {} assigned to {} is in {} state".format(trans_id.title(),date.title(),state.title()))
     return []

class ActionHelloWorld(Action):
     def name(self) -> Text:
         return "action_app_report"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         trans_id=tracker.get_slot('trans_id')
         date=tracker.get_slot('date')
         state=tracker.get_slot('state')
         dispatcher.utter_message(trans_id)
         dispatcher.utter_message(state)
         dispatcher.utter_message(date)
         connection = mysql.connector.connect(host='localhost',database='chatbot',user='root',password='Poornima@7')
         cursor = connection.cursor()
         sql_select_query = """select * from trade_ebills where Transaction_Date = %s and Transaction_state = %s and Transaction_ID = %s"""
         cursor.execute(sql_select_query,(date,state,trans_id,))
         records = cursor.fetchall()
         wb = xlwt.Workbook()
         ws = wb.add_sheet('Application Report')
         style = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
         for r, row in enumerate(records):
                if row:
                    for c, col in enumerate(records[0]):
                         ws.write(r, c, row[c],style)
         wb.save('app_report.xls')
         dispatcher.utter_attachment('app_report.xls')
         return []
