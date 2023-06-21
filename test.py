import streamlit as st
import pandas as pd
import numpy as np
import tables
import reservations
import datetime
from functools import wraps
from datetime import date


def decorate_it(func):
  @wraps(func)
  def wrapper (*args, **kwargs):
    st.write("Hello!")
    result = func (*args, **kwargs)
    st.write("Good luck:)")
    return result
  return wrapper

@decorate_it
def write_text(name,text):
    st.write(name,text)


page = st.sidebar.radio("Page",["Booking","Tables","Status"])


if page=="Booking":
    st.title("Managing bookings")
    now_date=date.today()
    now_time=datetime.datetime.now()
    now_h=int(now_time.strftime("%H"))
    now_m=int(now_time.strftime("%M"))

    st.header("For taking table now:")
    st.write("Time start:", now_date, now_h, ":", now_m)
    col1, col2 = st.columns(2)
    with col1:
        a_guest_count = st.number_input('Guests count',step=1, max_value=30, min_value=1,key='a_guest_count')
    with col2:
        a_period_end = st.time_input('Time end',key='a_period_end')

    now_date=date.today()
    now_time=datetime.datetime.now()
    now_h=int(now_time.strftime("%H"))
    now_m=int(now_time.strftime("%M"))

    a_guest=reservations.Guest("test","123",a_guest_count)
    a_period=reservations.Period(now_date,datetime.time(now_h, now_m),a_period_end)
    a_table=tables.all_tables[0]
    a_reservation=reservations.Reservation(a_table, a_guest, a_period)

    if st.button('Check available tables', key='av'):
        ares = list(reservations.check_availability(reservations.all_reservations, a_reservation, tables.all_tables, a_guest_count))
        if len(ares)>=1:
            st.write("Available table(s):")
            for r in ares:
                st.write(r)
        else:
            st.write("No available tables")

    st.header("For booking:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        new_guest_name = st.text_input('Guest name',key='new_guest_name')
    with col2:
        new_guest_phone = st.text_input('Guest phone',key='new_guest_phone')
    with col3:
        new_guest_count = st.number_input('Guests count',step=1, max_value=30, min_value=1, key='new_guest_count')   

    col1, col2, col3 = st.columns(3)
    with col1:
        new_period_date = st.date_input("Date",datetime.date(2022, 11, 6),key='new_period_date')
    with col2:
        new_period_start = st.time_input('Time start',datetime.time(19, 00),key='new_period_start')
    with col3:
        new_period_end = st.time_input('Time end',datetime.time(20, 00),key='new_period_end') 

    table_names = tables.load_names(tables.all_tables)
    table_name = st.selectbox('Select table 👉',table_names,key='table_name')
    
    new_guest=reservations.Guest(new_guest_name,new_guest_phone,new_guest_count)
    new_period=reservations.Period(new_period_date,new_period_start,new_period_end)
    new_table=tables.find_table(tables.all_tables,table_name)
    new_reservation=reservations.Reservation(new_table, new_guest, new_period)

    if st.button('Create new booking', key='bo'):
        res = reservations.check_reservation(reservations.all_reservations, new_reservation)
        write_text(new_guest_name,res)


    st.title("All reservations")
    df_reservations = reservations.load_reservations_df(reservations.all_reservations)
    st.dataframe(df_reservations, use_container_width=True)


elif page=="Tables":

    st.title("Managing tables")

    names = tables.load_names(tables.all_tables)

    st.text("For deleting table:")
    name_delete = st.selectbox('Select table 👉',names,key='delete')

    if st.button('Delete'):
        tables.delete(tables.all_tables,name_delete)

    st.text("For changing table's capacity:")
    col1, col2 = st.columns(2)

    with col1:
        name_capacity = st.selectbox('Select table 👉',names,key='capacity')

    with col2:
        new_capacity_change = st.text_input('New capacity',5,key='change_capacity')

    if st.button('Change capacity'):
        tables.change_capacity(name_capacity,new_capacity_change)

    st.text("For creating new table:")
    col3, col4 = st.columns(2)

    with col3:
        name_create = st.text_input('Create name for new table','Tokyo',key='create_name')
    
    with col4:
        new_capacity_create = st.text_input('New capacity',5,key='create_capacity')

    if st.button('Create'):
        tables.create(tables.all_tables,name_create,new_capacity_create)
    
    st.header("All tables:")
    df_tables = tables.load_tables_df(tables.all_tables)
    st.dataframe(df_tables, use_container_width=True)


elif page=="Status":
    st.title("All reservations")
    df_reservations = reservations.load_reservations_df(reservations.all_reservations)
    st.dataframe(df_reservations, use_container_width=True)