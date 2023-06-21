import pandas as pd
import numpy as np
import tables
import datetime

class Guest():
  def __init__(self, name, tel, guest_count):
    self.name = name
    self.tel = tel    
    self.guest_count = guest_count    


class Period():
  def __init__(self, date, start, end):
    self.date = date
    self.start = start    
    self.end = end    

class Reservation():
  def __init__(self, table, guest, period):
    self.table = table
    self.guest = guest
    self.period = period

guest1=Guest("Bob", "8234", 5)
period1=Period("2022-11-01",datetime.time(18, 30),datetime.time(22, 30))
table1=tables.table_rome
reservation1=Reservation(table1, guest1, period1)

guest2=Guest("Mia","8333",10)
period2=Period("2022-11-01",datetime.time(18, 30),datetime.time(22, 30))
table2=tables.table_paris
reservation2=Reservation(table2, guest2, period2)

guest3=Guest("Vova","8231",1)
period3=Period("2022-11-01",datetime.time(18, 00),datetime.time(20, 00))
table3=tables.table_london
reservation3=Reservation(table3, guest3, period3)

all_reservations = [reservation1,reservation2,reservation3]


def check_capacity(new_reservation):
  c = int(new_reservation.table.capacity)
  p = int(new_reservation.guest.guest_count)
  if (p<c or p==c):
    cap = "ok"
  else:
    cap = "not ok"
  return cap

def intersection(t1start,t1end,t2start,t2end):
    return (t1start <= t2start <= t1end) or (t2start <= t1start <= t2end)

def find_others(all_reservations, new_reservation):
    intersections = 0
    for r in all_reservations:
        print(r.table.name,r.period.start,r.period.start,r.period.end)
        if r.table.name==new_reservation.table.name:
            if str(r.period.date)==str(new_reservation.period.date):
                if intersection(r.period.start,r.period.end,new_reservation.period.start,new_reservation.period.end):
                    intersections+=1
    return intersections

def check_reservation(all_reservations, new_reservation):
    cap = check_capacity(new_reservation)
    intersections = find_others(all_reservations, new_reservation)
    if intersections>=1:
        res="sorry,table is not available"
    else:
        if cap=='ok':
            res = ", congratulations!"
            all_reservations.append(new_reservation)
        else:
            res=", sorry, table is too small"
    return res

def load_reservations_df(all_reservations):
    guests=[]
    tables=[]
    dates=[]
    starts=[]
    ends=[]
    
    for r in all_reservations:
        guests.append(r.guest.name)
        tables.append(r.table.name)
        dates.append(r.period.date)
        s = r.period.start.strftime('%H:%M')
        e = r.period.end.strftime('%H:%M')
        starts.append(s)
        ends.append(e)

    df_reservations = pd.DataFrame(
        {
            "Guest": guests,
            "Table": tables,
            "Date": dates,
            "Start": starts,
            "End": ends,
        })
    return df_reservations

def check_availability(all_reservations, new_reservation, all_tables, a_guest_count):
    free_tables=tables.load_names(all_tables)
    for t in all_tables:
        for r in all_reservations:
            if (str(r.period.date)==str(new_reservation.period.date) and t.name==r.table.name and intersection(r.period.start,r.period.end,new_reservation.period.start,new_reservation.period.end)):
                if t.name in free_tables:
                    free_tables.remove(t.name)
            if a_guest_count>t.capacity:
                if t.name in free_tables:
                    free_tables.remove(t.name)
    return free_tables