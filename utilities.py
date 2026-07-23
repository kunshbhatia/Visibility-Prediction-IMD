import numpy as np
            
# For Input Processing
def inputs_processing(Day : int , Month : int , Year : int ,Time_hour : int , 
                      PM2_5 : float , PM10 : float , TMPC : float , DWPC : float ,
                      RELH : float , DRCT : float , SPED : float , BLH : float , VSBK_Current : float):

    # Creating Dew Point Depression
    DPD = TMPC - DWPC # To be displayed in the inputs also 
    

    # Cyclic Encoading
    wind_x = float(np.cos(np.radians(DRCT))) 
    wind_y = float(np.sin(np.radians(DRCT)))
    
    hour_sin = float(np.sin((2*3.14*Time_hour)/24))
    hour_cos = float(np.cos((2*3.14*Time_hour)/24))

    month_sin = float(np.sin(2*np.pi*Month/12))
    month_cos = float(np.cos(2*np.pi*Month/12))

    return month_sin , month_cos , Year , hour_sin , hour_cos , PM2_5 , PM10 , TMPC , DWPC , DPD , RELH , wind_x , wind_y , SPED , BLH , VSBK_Current

#Fog Classification for final result
def fog_classification(visibility): # In meters
    
    if visibility < 50:
        return 'Very Dense Fog'
    elif visibility < 200: 
        return 'Dense Fog'
    elif visibility < 500: 
        return 'Moderate Fog'
    else: 
        return 'Shallow Fog'

def color_codes(visibility):
    
    if visibility < 50:
        color = "#FF7F7F" # Light Red
    elif visibility < 200:
        color = "#FFC080" # Light Orange
    elif visibility < 500:
        color = "#FFFF99" # Light Yellow
    else:
        color = "#90EE90" # Light Green     

    return color

def clock_emoji():
    return ["🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚","🕛","🕐","🕑","🕒","🕓","🕔","🕕","🕖","🕗","🕘","🕙","🕚","🕛"]