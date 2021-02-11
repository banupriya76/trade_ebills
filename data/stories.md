## path
* greet
  - utter_greet
* query
  - app_form
  - form{"name": "app_form"}
  - form{"name": null}
  - action_app_report
* goodbye
  - utter_goodbye

## interactive_story_1
* greet
    - utter_greet
* query{"trans_id": "10878", "date": "11/21/20"}
    - slot{"date": "11/21/20"}
    - slot{"trans_id": "10878"}

## interactive_story_2
* greet
    - utter_greet
* query{"trans_id": "10878", "date": "11/21/20"}
    - slot{"date": "11/21/20"}
    - slot{"trans_id": "10878"}
    - app_form
    - form{"name": "app_form"}
    - slot{"trans_id": "10878"}
    - slot{"date": "11/21/20"}
    - slot{"trans_id": "10878"}
    - slot{"date": "11/21/20"}
    - slot{"requested_slot": "state"}
* form: query{"state": "committed"}
    - slot{"state": "committed"}
    - form: app_form
    - slot{"state": "committed"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_app_report

## interactive_story_3
* greet
    - utter_greet
* query{"trans_id": "10878", "date": "11/21/20"}
    - slot{"date": "11/21/20"}
    - slot{"trans_id": "10878"}
    - app_form
    - form{"name": "app_form"}
    - slot{"trans_id": "10878"}
    - slot{"date": "11/21/20"}
    - slot{"trans_id": "10878"}
    - slot{"date": "11/21/20"}
    - slot{"requested_slot": "state"}
* form: query{"state": "committed"}
    - slot{"state": "committed"}
    - form: app_form
    - slot{"state": "committed"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_app_report
