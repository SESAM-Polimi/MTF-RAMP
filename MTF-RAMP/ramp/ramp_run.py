# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:35:00 2019
This is the code for the open-source stochastic model for the generation of 
multi-energy load profiles in off-grid areas, called RAMP, v0.3.0.

@authors:
- Francesco Lombardi, Politecnico di Milano
- Sergio Balderrama, Université de Liège
- Sylvain Quoilin, KU Leuven
- Emanuela Colombo, Politecnico di Milano

Copyright 2019 RAMP, contributors listed above.
Licensed under the European Union Public Licence (EUPL), Version 1.2;
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
"""

#%% Import required modules

import sys,os
import pandas as pd
sys.path.append('../')

from core.stochastic_process import Stochastic_Process
from post_process import post_process as pp

# Define which input files should be considered and run. 
# Files are specified as numbers in a list (e.g. [1,2] will consider input_file_1.py and input_file_2.py)
# PROJECT A
#input_files_to_run = [r"input_files\HH - project_a_month_1.xlsx",r"input_files\HH - project_a_month_2.xlsx",r"input_files\HH - project_a_month_3.xlsx",r"input_files\HH - project_a_month_4.xlsx",r"input_files\HH - project_a_month_5.xlsx",r"input_files\HH - project_a_month_6.xlsx",r"input_files\HH - project_a_month_7.xlsx",r"input_files\HH - project_a_month_8.xlsx",r"input_files\HH - project_a_month_9.xlsx",r"input_files\HH - project_a_month_10.xlsx",r"input_files\HH - project_a_month_11.xlsx",r"input_files\HH - project_a_month_12.xlsx"]

# PROJECT B
input_files_to_run = [r"input_files\HH - project_b_month_1.xlsx",r"input_files\HH - project_b_month_2.xlsx",r"input_files\HH - project_b_month_3.xlsx",r"input_files\HH - project_b_month_4.xlsx",r"input_files\HH - project_b_month_5.xlsx",r"input_files\HH - project_b_month_6.xlsx",r"input_files\HH - project_b_month_7.xlsx",r"input_files\HH - project_b_month_8.xlsx",r"input_files\HH - project_b_month_9.xlsx",r"input_files\HH - project_b_month_10.xlsx",r"input_files\HH - project_b_month_11.xlsx",r"input_files\HH - project_b_month_12.xlsx"]



# Calls the stochastic process and saves the result in a list of stochastic profiles
for j in input_files_to_run:
    Profiles_list = Stochastic_Process(j)
    
# Post-processes the results and generates plots
    Profiles_avg, Profiles_list_kW, Profiles_series = pp.Profile_formatting(Profiles_list)
    pp.Profile_series_plot(Profiles_series) #by default, profiles are plotted as a series
    
    # sss=pp.export_series(Profiles_series,j)
    pd.DataFrame(Profiles_series).to_csv(f'results\output_file_{j.split("HH")[-1]}.csv')
    
    if len(Profiles_list) > 1: #if more than one daily profile is generated, also cloud plots are shown
        pp.Profile_cloud_plot(Profiles_list, Profiles_avg)

