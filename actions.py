

# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
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

class ActionHello(action_app_report):
    def name(self) -> Text:
        return "app_form"
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        #print("required_slots(tracker: Tracker)")
        return ["ticket","team","state"]
    def validate(self, dispatcher, tracker, domain):
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher, tracker, domain))
        for slot, value in slot_values.items():
         if slot == 'ticket':
            if value is None:
                dispatcher.utter_template('utter_ask_ticket', tracker)
                slot_values[slot] = None
            else:
                dispatcher.utter_message("Ticket Type is {}".format(value))
         elif slot == 'team':
            if value is None:
                dispatcher.utter_template('utter_ask_team', tracker)
                slot_values[slot] = None
         elif slot == 'state':
            if value is None:
               dispatcher.utter_template('utter_ask_state', tracker)
               slot_values[slot] = None
        return [SlotSet(slot, value) for slot, value in slot_values.items()]
    def slot_mappings(self) -> Dict[Text,Union[Dict, List[Dict]]]:
        return {
        "ticket": self.from_entity(entity="ticket",intent='query'),
        "team": self.from_entity(entity="team",intent='query'),
        "state": self.from_entity(entity="state",intent='query')
    }
    def submit(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any],
           ) -> List[Dict]:
     ticket=tracker.get_slot('ticket')
     team=tracker.get_slot('team')
     state=tracker.get_slot('state')
     dispatcher.utter_message(template="utter_submit", ticket=tracker.get_slot('ticket'),team=tracker.get_slot('team'),state=tracker.get_slot('state'))
     dispatcher.utter_message(
        "Hey, your report type is {} assigned to {} is in {} state".format(ticket.title(),team.title(),state.title()))
     return []

class ActionHelloWorld(Action):
     def name(self) -> Text:
         return "action_hello_world"
     def run(self, dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         ticket=tracker.get_slot('ticket')
         team=tracker.get_slot('team')
         state=tracker.get_slot('state')
         dispatcher.utter_message(ticket)
         dispatcher.utter_message(state)
         dispatcher.utter_message(team)
         tick=ticket[0:2]
         if tick.lower() == 'sr' or 'se':
             connection = mysql.connector.connect(host='localhost',database='chatbot',user='root',password='Poornima@7')
             cursor = connection.cursor()
             sql_select_query = """select * from sr where Task_Related_Historical_Support_Group = %s and Task_Related_Historical_State = %s"""
             cursor.execute(sql_select_query,(team,state,))
             records = cursor.fetchall()
             wb = xlwt.Workbook()
             ws = wb.add_sheet('SERVICE REQUEST REPORT')
             style = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
             for r, row in enumerate(records):
                if row:
                    for c, col in enumerate(records[0]):
                         ws.write(r, c, row[c],style)
             wb.save('report.xls')
             dispatcher.utter_attachment('report.xls')
         if tick.lower() == 'in':
             connection = mysql.connector.connect(host='localhost',database='chatbot',user='root',password='Poornima@7')
             cursor = connection.cursor()
             sql_select_query = """select * from incident where Incident_ci_name = %s and Incident_state = %s"""
             cursor.execute(sql_select_query,(team,state,))
             records = cursor.fetchall()
             wb = xlwt.Workbook()
             ws = wb.add_sheet('INCIDENT_REPORT')
             style = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
             for r, row in enumerate(records):
                if row:
                    for c, col in enumerate(records[0]):
                        ws.write(r, c, row[c],style)
             wb.save('report.xls')
             dispatcher.utter_attachment('report.xls')
         '''column_headings = [
							'Task_Reference_Number',
							'Beginning_of_Previous_Week',
							'Previous_Sunday',
							'Task_Submitted_Date_Time',
							'Task_Closed_Date_Time',
							'Task_Priority',
							'CI',
							'CI_Name',
                            'Task_Related_Historical_Support_Group',
                            'Task_Related_Historical_State',
                            'Assignment_group'
		 ]
         ws.write(0,0,'Task_Reference_Number',style)
         ws.write(0,1,'Beginning_of_Previous_Week',style)
         ws.write(0,2,'Previous_Sunday',style)
         ws.write(0,3,'Task_Submitted_Date_Time',style)
         ws.write(0,4,'Task_Closed_Date_Time',style)
         ws.write(0,5,'Task_Priority',style)
         ws.write(0,6,'CI',style)
         ws.write(0,7,'CI_Name',style)
         ws.write(0,8,'Task_Related_Historical_Support_Group',style)
         ws.write(0,9,'Task_Related_Historical_State',style)
         ws.write(0,10,'Assignment_group',style)
         for r, row in enumerate(records):
            if row:
                for c, col in enumerate(records[0]):
                    ws.write(r, c, row[c],style)
         wb.save('report.xls')
         dispatcher.utter_attachment('report.xls')'''
         return []
