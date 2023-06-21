import pandas as pd
import numpy as np

class Table():
  def __init__(self, name, capacity):
    self.name = name
    self.capacity = capacity


def change_capacity(name, capacity):
    for t in all_tables:
      if t.name==name:
        t.capacity=capacity


def create(all_tables, name, capacity):
    table=Table(name,capacity)
    all_tables.append(table)
    return all_tables

def delete(all_tables, name):
    for t in all_tables:
        if t.name==name:
           all_tables=all_tables.remove(t) 
    return all_tables


table_rome=Table("Rome",10)
table_paris=Table("Paris",10)
table_london=Table("London",10)

all_tables = [table_rome,table_paris,table_london]

def load_tables_df(all_tables):
  names=[]
  capacities=[]
  
  for t in all_tables:
    names.append(t.name)
    capacities.append(t.capacity)
    
  df_tables = pd.DataFrame(
            {
                "table name": names,
                "capacity": capacities,
            })
  return df_tables

def load_names(all_tables):
  names=[]
  for t in all_tables:
    names.append(t.name)
  return names

def find_table(all_tables,name):
    for t in all_tables:
        if t.name==name:
            return t