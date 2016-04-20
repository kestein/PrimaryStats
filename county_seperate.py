#!/usr/bin/python

# -*- coding: utf-8 -*-
import json

dems = {}
gop = {}


def seperate_parties(states):
   """
   Seperates candidates into dem/gop by state

   :param states: Dictionary with state results for the primaries
   """
   for election in states:
      state = election["state_id"]
      county_results = []
      for county in election["counties"]:
         county_d = {
            "fips": county["fips"],
            "name": county["name"],
            "results": county["results"],
          }
         county_results.append(county_d)
      if election["party_id"] == "republican":
         gop[state] = county_results
      elif election["party_id"] == "democrat":
         dems[state] = county_results
      else:
         continue


def load_data():
   """
   Capture a subset of the data from all the primaries

   :return: A list of states' data
   """
   states = []
   with open("data/primaries.json", "r") as f:
      total = json.load(f)
      for race in total["races"]:
         if race["race_type"] != "president" or \
            not race["report"]:
            continue
         states.append(
            {
               "party_id": race["party_id"],
               "state_id": race["state_id"],
               "candidates": race["candidates"],
               "election_date": race["election_date"],
               "counties": race["counties"]
            }
         )
   return states

 
def main():
   states = load_data()
   seperate_parties(states)
   with open("data/dems-county.json", "w") as f:
      json.dump(dems, f)
   with open("data/gop-county.json", "w") as f:
      json.dump(gop, f)
   

if __name__ == "__main__":
   main()
