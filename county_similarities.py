#!/usr/bin/python

# -*- coding: utf-8 -*-
import json

# Generate percentages of votes for each candidate per county per party
# Compare b/w GOP and DEMS
""" Output data
   state:
      county:
         gop
         dem
         % overlap
"""


def find_most_votes(county_results):
   """
   Find the candidate that received the most votes in the county
   :param dict county_results: The results of the county's primary
   :return str: The key for the candidate that got the most votes
   """
   most = -1
   cand = ""
   for candidate in county_results:
      if county_results[candidate] > most:
         cand = candidate
         most = county_results[candidate]
   return cand


def find_county(gop, county):
   """
   Find the county in the list
   :param list gop: List of county primary elections
   :param str county: The name of the county to find
   :return dict: The dict containing that county's primary results
   """
   for c in gop:
      if c["fips"] == county:
         return c
   return None


def find_candidate_distances(dems, gop):
   """
   :param dict dems: The democratic primaries
   :param dict gop: The republican primaries
   :return list: Similarity list between parties
   """
   similarities = {}
   for state in dems:
      # Only calculate for a state with both primaries completed
      if state not in gop:
         continue
      county_sims = []
      for d_county in dems[state]:
         g_county = find_county(gop[state], d_county["fips"])
         # If that county does not exist in gop move on
         if g_county is None:
            continue
         dem_cand = find_most_votes(d_county["results"])
         gop_cand = find_most_votes(g_county["results"])
         dem_percent = d_county["results"][dem_cand]
         gop_percent = g_county["results"][gop_cand]
         # Cannot measure overlap if no one voted
         if dem_percent == 0 or gop_percent == 0:
            continue
         overlap = 100*min(dem_percent, gop_percent)/max(dem_percent, gop_percent)
         county_sims.append(
            {
               "fips": d_county["fips"],
               "name": d_county["name"],
               "dem": dem_cand,
               "gop": gop_cand,
               "overlap": overlap
            }
         )
      similarities[state] = county_sims
   return similarities


def process_county_percentages(county):
   """
   Converts raw vote numbers into percentages
   :param dict county: The results of the county's primary
   :return dict: The county results in percentages
   """
   total_votes = 0
   percentages = {}
   for candidate in county:
      total_votes += county[candidate]
   # Really? There are counties where no one votes. For shame GOP Zavala, TX
   if total_votes == 0:
      total_votes = 1
   for candidate in county:
      percentages[candidate] = county[candidate]/(total_votes*1.0)*100
   return percentages



def process_state_percentages(state):
   """
   Process percentage votes for all counties
   :param list counties: A list of county primaries
   :return list: A list of county primaries in percentage form
   """
   percentages = []
   for county in state:
      county["results"] = process_county_percentages(county["results"])
      percentages.append(county)
   return percentages


def load(file_name):
   """
   Loads county voting data into the party's dict
   :param str file_name: The json file to load
   :return dict: All of that party's data
   """
   with open(file_name, "r") as f:
      party_data = json.load(f)
   return party_data


def main():
   gop = load("data/gop-county.json")
   dems = load("data/dems-county.json")
   for state in gop:
      gop[state] = process_state_percentages(gop[state])
   for state in dems:
      dems[state] = process_state_percentages(dems[state])
   similarities = find_candidate_distances(dems, gop)
   with open("data/similar.json", "w") as f:
      json.dump(similarities, f)


if __name__ == "__main__":
   main()
