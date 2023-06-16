# -*- coding: utf-8 -*-

#%% Initialisation of a model instance

import numpy as np 
import importlib
import pandas as pd
import math
from ramp.core.constants import inputs_params
from ramp.core.core import User
import importlib
import copy


def yearly_pattern():
    '''
    Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour
    '''
    #Yearly behaviour pattern
    Year_behaviour = np.zeros(365)
    Year_behaviour[5:365:7] = 1
    Year_behaviour[6:365:7] = 1
    
    return(Year_behaviour)


def user_defined_inputs(j):
    '''
    Imports an input file and returns a processed User_list
    '''

    file = copy.deepcopy(j)
    file = file[:-3]
    file = file.replace("\\",".")
    file_module = importlib.import_module(f"{file}")
    
    User_list = file_module.User_list

    return(User_list)


def Initialise_model(file):
    '''
    The model is ready to be initialised
    '''
    df = pd.read_excel(file,sheet_name="Profiles",header=None,usecols=[0],nrows=1)
    num_profiles = df.iloc[0,0]
    print('Please wait...') 
    Profile = [] #creates an empty list to store the results of each code run, i.e. each stochastically generated profile
    
    return (Profile, num_profiles)
    

def Initialise_from_excel(file):
    
    users = pd.read_excel(file, sheet_name="Users", index_col=[0], header=[0])    
    appliances = pd.read_excel(file, sheet_name="Appliances", index_col=[0,1], header=[0,1]).iloc[2:,:]

    User_list = []
    
    
    for u in list(users.index):
        if " " in u:  # check if name contains spaces
            u = u.replace(" ","_")
            
        instruction = "User("+inputs_params['Users'][users.index.names[0]] + "=" + "'" + u + "'"
        for p in list(users.columns):
            instruction += ", "+ inputs_params['Users'][p] + "=" + str(users.loc[u,p])
        instruction += ")"
                
        exec(u + " = " + instruction)
        
        
    for a in range(appliances.shape[0]):
        
        appliance = appliances.index.get_level_values(0)[a]
        user = appliances.index.get_level_values(1)[a] 
        
        if " " in appliance:  # check if name contains spaces
            appliance = appliance.replace(" ","_")
        if " " in user:  # check if name contains spaces
            user = user.replace(" ","_")
            
        # basic information
        bi_instruction = appliance + " = " + user + "." + "Appliance(user=" + "'" + user + "'" 
        basic_information = appliances.loc[:,("Basic information",slice(None))]
        basic_information = basic_information.droplevel(0,axis=1)
        
        for p in range(basic_information.shape[1]):

            if type(basic_information.iloc[a,p]) != str:
                if math.isnan(basic_information.iloc[a,p]) == False:
                    bi_instruction += ", " + inputs_params['Appliances'][basic_information.columns[p]] + "=" + str(basic_information.iloc[a,p])
            else:
                bi_instruction += ", " + inputs_params['Appliances'][basic_information.columns[p]] + "=" + "'" + basic_information.iloc[a,p] + "'"
            
        bi_instruction += ")"
        
        exec(bi_instruction)
        eval(appliance).user = eval(user)
        
        
        # windows information
        win_instruction = appliance + ".windows("
        windows_information = appliances.loc[:,("Windows",slice(None))]
        windows_information = windows_information.droplevel(0,axis=1)
        
        for w in range(windows_information.shape[1]):
            
            if "Window" in windows_information.columns[w]:
                if type(windows_information.iloc[a,w]) != float and type(windows_information.iloc[a,w]) != np.float64:
                    win_instruction += inputs_params["Windows"][windows_information.columns[w]] + "=" + "["+windows_information.iloc[a,w]+"]" + ","
             
            else:
                if type(windows_information.iloc[a,w]) == float or type(windows_information.iloc[a,w]) == np.float64:
                    if math.isnan(windows_information.iloc[a,w]) == False:
                        win_instruction += inputs_params["Windows"][windows_information.columns[w]] + "=" + str(windows_information.iloc[a,w]) + ","
                    
        win_instruction += ")"
        
        eval(win_instruction)

    for u in list(users.index):
        User_list += [eval(u)] 

    return User_list


def Initialise_inputs(j):
    
    Year_behaviour = yearly_pattern()
    
    input_format = j.split(".")[-1]

    if input_format == "py":
        user_list = user_defined_inputs(j)
    elif input_format == "xlsx":
        user_list = Initialise_from_excel(j)
        
    
    # Calibration parameters
    '''
    Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
    They regulate the probabilities defining the largeness of the peak window and the probability of coincident switch-on within the peak window
    '''
    peak_enlarg = 0.15 #percentage random enlargement or reduction of peak time range length
    mu_peak = 0.5 #median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
    s_peak = 0.5 #standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned
    op_factor = 0.5 #off-peak coincidence calculation parameter

    return (peak_enlarg, mu_peak, s_peak, op_factor, Year_behaviour, user_list)

