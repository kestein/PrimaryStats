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
      state_index = {}
      for dumbo in election["candidates"]:
         candidate = dumbo["candidate_id"]
         state_index[candidate] = dumbo["percent"]
      if election["party_id"] == "republican":
         gop[state] = state_index
      elif election["party_id"] == "democrat":
         dems[state] = state_index
      else:
         continue


def load_data():
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
               "election_date": race["election_date"]
            }
         )
   return states

 
def main():
   states = load_data()
   seperate_parties(states)
   with open("data/dems-state.json", "w") as f:
      json.dump(dems, f)
   with open("data/gop-state.json", "w") as f:
      json.dump(gop, f)
   

if __name__ == "__main__":
   main()
