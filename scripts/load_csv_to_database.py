#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from IPython.display import display


# In[2]:


'''
   run_bash_cmdning django script and jupyter in this case have
   different working directories
   so this is done to make sure that the data path is correct for both
'''
import os
cwd = os.getcwd()
curr_dir = cwd.split(os.path.sep)[-1]
IS_NOTEBOOK = curr_dir == 'scripts'

if IS_NOTEBOOK: 
   os.chdir('../')

NEW_CWD = os.getcwd()
DATA_PATH = os.path.join(NEW_CWD, 'data','all-states-history.csv')
print('cwd before checking: ', cwd)
print('DATA_PATH: ', DATA_PATH)
print('cwd now: ', NEW_CWD)
print('IS_NOTEBOOK: ', IS_NOTEBOOK)


# In[3]:


import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


# In[4]:


''' Activate django env if is in notebook '''

if IS_NOTEBOOK:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geo_covid.settings')
    import django
    django.setup()


# In[5]:


'''
    Meta functions
'''
import subprocess

def decode_output(str):
    try:
        return str.decode('utf-8')
    except UnicodeDecodeError as e:
        return str.decode('latin-1')
def run_bash_cmd(command: str):
    print("Exec: ", command)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output: print('Out: ', decode_output(output))
    if error: print('Err: ', decode_output(error))


# In[6]:


'''
    Helper functions
'''
import shutil
import re

CASE_CONVERT_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')
def camel_case_to_snake_case(string):
    return CASE_CONVERT_PATTERN.sub('_', string).lower()

def clear_migrations():
    try:
        shutil.rmtree("./us_covid_api/migrations/")
    except BaseException as e:
        print('Fail to clear migration: ',e)

def clean_cache():
    run_bash_cmd('python manage.py clear_cache')
    run_bash_cmd('python manage.py clean_pyc')
    run_bash_cmd(f'pyclean {NEW_CWD}')

def drop_database():
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    client.drop_database('geo-covid')

def clean_and_remigrate_db():
    run_bash_cmd("python manage.py flush --noinput")
    run_bash_cmd("python manage.py makemigrations us_covid_api")
    run_bash_cmd("python manage.py migrate")

def generate_drf_spec_schema():
    # generate schema for drf_spectacular
    run_bash_cmd("python manage.py spectacular --file schema.yml")

def print_settings():
    run_bash_cmd("python manage.py print_settings")


# In[7]:


'''
    Important functions relating to script main functionality
'''
from tkinter import N
import numpy as np
from math import isnan
from us_covid_api.models import Report, State
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware

def load_reports(report_df: pd.DataFrame):
    def generate_report(report_record: pd.Series):
        try:
            state = State.objects.get(initials=report_record['state'])
        except ObjectDoesNotExist as e:
            state = State(name=report_record['state'], initials=report_record['state'])
            state.save()

        report_record.loc['state'] = state
        report_record.loc['date'] = make_aware(report_record.loc['date'])
        report_dict = {k:(v if not type(v) is float or not isnan(v) else None) for k, v in report_record.to_dict().items()}

        report_obj = Report(id=None, **report_dict)
        report_obj.save()
    report_df.apply(generate_report, axis=1)


# In[8]:


''' Testing code '''

def sample_code():
    df = pd.read_csv('data/all-states-history.csv', parse_dates=['date'])
    df.columns = list(df.columns.map(lambda x: camel_case_to_snake_case(x)))
    record = df.loc[0].copy()
    state = State(name='random', initials=record['state'])
    state.save()
    record.loc['state'] = state
    # record.pop('state')
    value_dict = record.to_dict()
    newdict = {k:(v if not type(v) is float or not isnan(v) else None) for k, v in value_dict.items()}
    print(newdict)
    obj = Report(id=None, **newdict)
    obj.save()
    print('DONE')


# In[9]:


'''
    NOTE: this is the main function & entry point of the whole script (most important)
'''

from ast import arg


def run(*args):
    # TODO: add indexes and unique constraints
    print('script args: ', args)
    # Default behavior is run all below tasks
    if 'no-clear-migrations' not in args: clear_migrations()
    if 'no-clean-cache' not in args: clean_cache()
    if 'no-drop-db' not in args: drop_database()
    if 'no-remigrate-db' not in args: clean_and_remigrate_db()
    if 'no-generate-schema' not in args: generate_drf_spec_schema()
    if 'no-print-settings' not in args: print_settings()
    print('-----DONE PREP-----------------')
    # Data processing part
    df = pd.read_csv('data/all-states-history.csv', parse_dates=['date'])
    print('Shape: ', df.shape)
    df.columns = list(df.columns.map(lambda x: camel_case_to_snake_case(x)))
    load_reports(df)
    # TODO: process data somehow
    print('Done importing')


# In[10]:


# ''' Notebook test run '''
import threading
import time
NOTEBOOK_ARGS = []

if IS_NOTEBOOK:
    print("Main    : before creating thread")
    x = threading.Thread(target=run, args = NOTEBOOK_ARGS)
    print("Main    : before running thread")
    x.start()
    x.join()
    print("Main    : wait for the thread to finish")
    print("Main    : all done")


# In[ ]:


'''
    Testing queries
'''

import timeit
from random import randrange, seed, randint
from datetime import timedelta
import datetime

# Settings
DAYS_INTERVAL = 5 
seed(0)


# Helper
def random_date(start=datetime.date(2020, 1, 13), end=datetime.date(2021, 3, 7)):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def random_state_initials():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    return states[randint(0, len(states) - 1)]

def examine_thread_speed(function, args = (), verbose = True):
    if verbose: print('--------------------------')
    # NOTE: there is threading overhead involved
    if args:
        x = threading.Thread(target=function, args = (*args, verbose,))
    else:
        new_func = lambda: function(verbose=verbose)
        x = threading.Thread(target=new_func)
    if verbose: print("Before running thread: ", function.__name__, ", arg: ", args)
    start = timeit.default_timer()
    x.start()
    x.join()
    stop = timeit.default_timer()
    time_diff = stop - start
    if verbose: print('Done, Execution Time (second): ', time_diff)
    return time_diff  


# Tests
def stats_one_day_all_states(date, verbose = True):
    if verbose: print('Date: ', date)
    time_range = (make_aware(datetime.datetime.combine(date, datetime.time.min)),
                make_aware(datetime.datetime.combine(date, datetime.time.max)))
    reports = Report.objects.filter(date__range= time_range)
    if verbose: print('Report retrieved: ', reports.count())
    if len(reports) == 0: print('No reports found at given date!')

def stats_day_range_all_states(start_day, verbose = True):
    end_day = start_day + datetime.timedelta(days=DAYS_INTERVAL)
    if verbose: print('Start day: ', start_day, ', end day: ', end_day)
    time_range = (make_aware(datetime.datetime.combine(start_day, datetime.time.min)),
                make_aware(datetime.datetime.combine(end_day, datetime.time.max)))
    reports = Report.objects.filter(date__range= time_range)
    if verbose: print('Report retrieved: ', reports.count())
    if len(reports) == 0: print('No reports found at given date!')
            
def stats_one_state_all_days(state_initials, verbose = True):
    if verbose: print('State: ', state_initials)
    state = State.objects.filter(initials=state_initials).first()
    reports = Report.objects.filter(state_id= state.id)
    if verbose: print('Report retrieved: ', reports.count())
    if len(reports) == 0: print('No reports found at given date!')
# def stats_few_state_all_days(): pass # ! OUT OF SCOPE


# Results
if IS_NOTEBOOK:
    examine_thread_speed(stats_one_day_all_states, args=(random_date(),));

    start_day = random_date()
    examine_thread_speed(stats_day_range_all_states, args=(start_day,));

    examine_thread_speed(stats_one_state_all_days, args=(random_state_initials(),));


# In[ ]:



# Helper
def benchmark(function, args_list, inner_verbose=False):
    print('-----------------------------')
    results = []
    for args in args_list:
        time_delta = examine_thread_speed(function, args, verbose=inner_verbose)
        results.append(time_delta)
    print('Run results (second): ', results)
    print('Stats: ')
    display(pd.DataFrame(results).describe())

# Settings
REPEATS = 20
dates = [random_date() for _ in range(REPEATS)]
states_initials_list = [random_state_initials() for _ in range(REPEATS)]

# Results
to_args = lambda list_val: [(x,) for x in list_val]
if IS_NOTEBOOK:
    benchmark(stats_one_day_all_states, to_args(dates))
    benchmark(stats_day_range_all_states, to_args(dates))
    benchmark(stats_one_state_all_days, to_args(states_initials_list))


# In[ ]:


if IS_NOTEBOOK:
    run_bash_cmd('jupyter nbconvert --to python .\scripts\load_csv_to_database.ipynb')

