# -*- coding: utf-8 -*-


inputs_params = {
                 "Users": {
                           "User name": "name",
                           "N. users": "n_users",
                           "User preference": "us_pref"
                          },
                 
                 "Appliances": {
                                "User name": "user",
                                "Number": "n",
                                "Nominal power": "P",
                                "N. of windows": "w",
                                "Tot functioning time": "t",
                                "Variable time": "r_t",
                                "Min functioning time": "c",
                                "Clustered": "fixed",
                                "N. of duty cycles": "fixed_cycle",
                                "Occasional use": "occasional_use",
                                "No variability": "flat",
                                "Power variability": "thermal_P_var",
                                "Preference index": "pref_index",
                                "Weekend/weekday": "wd_we_type",
                               },
                 
                 "Windows": {
                             "Window 1": "w1",
                             "Window 2": "w2",
                             "Window 3": "w3",
                             "Variability": "r_w",                             
                            },
                 
                 "Specific cycle 1": {
                                      "1st stage power": "P_11",
                                      "1st stage duration": "t_11",
                                      "2nd stage power": "P_12",
                                      "2nd stage duration": "t_12",
                                      "Variability": "r_c1",
                                     },
                 
                 "Specific cycle 2": {
                                      "1st stage power": "P_21",
                                      "1st stage duration": "t_21",
                                      "2nd stage power": "P_22",
                                      "2nd stage duration": "t_22",
                                      "Variability": "r_c2",
                                     },

                 "Specific cycle 3": {
                                      "1st stage power": "P_31",
                                      "1st stage duration": "t_31",
                                      "2nd stage power": "P_32",
                                      "2nd stage duration": "t_32",
                                      "Variability": "r_c3",
                                     }
                 
                }