from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from typing import List, Text, Dict, Any

from actions.constants import EMISSIONS_TRANSACTION_LOG_PATH
import pandas
import logging

logger = logging.getLogger("emissions")


class ActionGetEmissionDetails(Action):

    def name(self) -> Text:
        return "action_get_emission_details"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> List[EventType]:
        emissions_data = pandas.read_csv(EMISSIONS_TRANSACTION_LOG_PATH, header=0)
        dispatcher.utter_message(
            text=f"I have details on {len(emissions_data)} emission categories."
        )
        required_emission_categories = int(tracker.get_slot("emissions_req_count"))
        if tracker.get_slot("emissions_filter") == "bottom":
            result = emissions_data.sort_values(
                by=["emissions_quantity_2023_release"], ascending=True
            )["original_inventory_sector"].unique()[: int(required_emission_categories)]
        else:
            result = emissions_data.sort_values(
                by=["emissions_quantity_2023_release"], ascending=False
            )["original_inventory_sector"].unique()[: int(required_emission_categories)]

        dispatcher.utter_message(
            f"""
        the {tracker.get_slot("emissions_filter")} 
        {required_emission_categories} are {", ".join(list(result))}"""
        )
        return [
            SlotSet("emissions_filter", None),
            SlotSet("emissions_req_count", None),
        ]


class ActionEmissionRate(Action):
    def name(self) -> Text:
        return "action_get_rate_of_emission"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[EventType]:
        emissions_data = pandas.read_csv(EMISSIONS_TRANSACTION_LOG_PATH, header=0)
        rate = tracker.get_slot("emission_rate") or "increasing"
        required_emission_categories = int(
            (tracker.get_slot("emissions_req_count")) or 10
        )
        emissions_filter = tracker.get_slot("emissions_filter") or "top"
        if "inc" in rate.casefold():
            emissions_data = emissions_data[(emissions_data["difference"] > 0)]
        else:
            emissions_data = emissions_data[(emissions_data["difference"] < 0)]

        if emissions_filter == "bottom":
            result = emissions_data.sort_values(
                by=["percent_difference"], ascending=True
            )["original_inventory_sector"].unique()[: int(required_emission_categories)]
        else:
            result = emissions_data.sort_values(
                by=["percent_difference"], ascending=False
            )["original_inventory_sector"].unique()[: int(required_emission_categories)]

        dispatcher.utter_message(
            f"""
                the {emissions_filter} 
                {required_emission_categories} with {rate}  emissions are {", ".join(list(result))}"""
        )
        return [
            SlotSet("emission_rate", None),
            SlotSet("emissions_req_count", None),
            SlotSet("emissions_filter", None),
        ]


class ActionGetTotalEmissionsPerSector(Action):
    def name(self) -> Text:
        return "action_get_total_emissions_per_sector"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[EventType]:
        sector_name = tracker.get_slot("emission_sector")
        emissions_data = pandas.read_csv(EMISSIONS_TRANSACTION_LOG_PATH, header=0)
        emissions_data = emissions_data[
            (emissions_data["original_inventory_sector"] == sector_name)
            & (emissions_data["year"] == 2021)
        ]
        total_emissions = emissions_data["emissions_quantity_2023_release"].values[0]
        dispatcher.utter_message(
            f"The total emissions of {sector_name} are {total_emissions}"
        )
