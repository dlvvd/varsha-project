from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from typing import List, Text


class ActionIntroduceYourself(Action):

    def name(self) -> Text:
        return "action_give_introduction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[EventType]:
        dispatcher.utter_message(
            text="Hey there! I am Varsha, the Climate bot! Nice to meet you "
        )


class ActionListOfActions(Action):

    def name(self) -> Text:
        return "action_get_list_of_performable_actions"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[EventType]:
        dispatcher.utter_message(
            f"""
            I am striving to be an expert in the Climate related Technologies.
            Currently I can answer your questions on emissions.
            """
        )
        dispatcher.utter_message(
            f"""
            I can provide information on 
            - Which industries are contributing to the emissions
            - Which industries are reducing their emissions
            - Which industries are increasing their emissions
            """
        )
