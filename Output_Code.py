import pandas as pd
import warnings
from utilities import fog_classification,inputs_processing
import pickle

# ---------------------- MODEL LOADING AND PRE SETUP ---------------------- #

def models_loading():
    for i in range(1,25):
        with open(fr"Models\VSBK_t{i}.pkl","rb") as f:
            globals()[f"model_t{i}"] = pickle.load(f)

warnings.filterwarnings("ignore") # To ignore the warnings of models

# ---------------------- MAIN FUNCTION CREATION ---------------------- #

def output_gen(inputs_given : tuple , output : str , units : str , timeperiod : str , category = True , export = False):

    df = pd.DataFrame()
    fog_class_list = [] # Collects all the classification of fog for asked period of time
    visibility_pred = [] # Collects all the visibility in fog
    visibility_range = [] # Used to store upper limit when output is choosen as Range or Both
    rmse_scores = [0 , 369.06 , 489.02 , 567.2 , 621.2 , 656.12 , 680.48 , 697.89 , 712.74 , 726.97 , 736.43 , 740.09 , 740.70 , 739.91 , 746.94 , 748.94 ,
                   748.13 , 746.52 , 739.46 , 739.46 , 732.96 , 743.94 , 748.49 , 737.45 , 740.70] #RMSE Scores of each model

    models_loading() # Loading the model

    #Input Processing
    inputs = [inputs_processing(*inputs_given)]
    
# ---------------------- DIV ON THE BASIS OF OUTPUT ---------------------- #

    if output == "point":
        
        if timeperiod == "all":
            df['Time Period'] = ['T+1', 'T+2', 'T+3', 'T+4', 'T+5', 'T+6', 'T+7', 'T+8', 'T+9', 'T+10', 'T+11', 'T+12', 'T+13', 'T+14', 'T+15', 'T+16', 'T+17', 'T+18', 'T+19', 'T+20', 'T+21', 'T+22', 'T+23', 'T+24']
            for i in range(1,25):
                globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
                fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
                
                if units == "m":
                    visibility_pred.append(globals()[f"model_pred_t{i}"])
                elif units == "km":
                    globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_pred_t{i}"]/1000),2)
                    visibility_pred.append(globals()[f"model_pred_t{i}"])
                else:
                    raise ValueError("Units must be 'm' or 'km'")
    
    
        elif isinstance(timeperiod, tuple): 
            start,end = timeperiod
            temp_time_period  = []
            for i in range(start,end+1): 
                time_period_input = f"T+{i}"
                temp_time_period.append(time_period_input)
                globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
                fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
                if units == "m":
                    visibility_pred.append(globals()[f"model_pred_t{i}"])
                elif units == "km":
                    globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_pred_t{i}"]/1000),2)
                    visibility_pred.append(globals()[f"model_pred_t{i}"])
                else:
                    raise ValueError("Units must be 'm' or 'km'")
                    
            df['Time Period'] = temp_time_period
    
        elif isinstance(timeperiod, int):
            i = timeperiod
            df['Time Period'] = [f"T+{i}"]
            globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
            fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
            
            if units == "m":
                visibility_pred.append(globals()[f"model_pred_t{i}"])
            elif units == "km":
                globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_pred_t{i}"]/1000),2)
                visibility_pred.append(globals()[f"model_pred_t{i}"])
            else:
                raise ValueError("Units must be 'm' or 'km'")
    
        else:
            raise ValueError("Timeperiod must be 'all', a tuple or an integer")

        df[f'Visibility Point Prediction in {units.upper()} of Point Value'] = visibility_pred

    elif output == "range":
        
        if timeperiod == "all":
            df['Time Period'] = ['T+1', 'T+2', 'T+3', 'T+4', 'T+5', 'T+6', 'T+7', 'T+8', 'T+9', 'T+10', 'T+11', 'T+12', 'T+13', 'T+14', 'T+15', 'T+16', 'T+17', 'T+18', 'T+19', 'T+20', 'T+21', 'T+22', 'T+23', 'T+24']
            for i in range(1,25):
                globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
                fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
                
                if units == "m":
                    visibility_range.append(f"{max(round(globals()[f"model_pred_t{i}"]-rmse_scores[i],2),0)} - {round(globals()[f"model_pred_t{i}"] + rmse_scores[i],2)}")
                elif units == "km":
                    globals()[f"model_pred_t{i}_min"] = max(round(float((globals()[f"model_pred_t{i}"]-rmse_scores[i])/1000),2),0)
                    globals()[f"model_pred_t{i}_max"] = max(round(float((globals()[f"model_pred_t{i}"]+rmse_scores[i])/1000),2),0)
                    visibility_range.append(f"{globals()[f"model_pred_t{i}_min"]} - {globals()[f"model_pred_t{i}_max"]}")
                else:
                    raise ValueError("Units must be 'm' or 'km'")
    
    
        elif isinstance(timeperiod, tuple): 
            start,end = timeperiod
            temp_time_period  = []
            for i in range(start,end+1): 
                time_period_input = f"T+{i}"
                temp_time_period.append(time_period_input)
                globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
                fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
                
                if units == "m":
                    visibility_range.append(f"{max(round(globals()[f"model_pred_t{i}"]-rmse_scores[i],2),0)} - {round(globals()[f"model_pred_t{i}"] + rmse_scores[i],2)}")
                elif units == "km":
                    globals()[f"model_pred_t{i}_min"] = max(round(float((globals()[f"model_pred_t{i}"]-rmse_scores[i])/1000),2),0)
                    globals()[f"model_pred_t{i}_max"] = max(round(float((globals()[f"model_pred_t{i}"]+rmse_scores[i])/1000),2),0)
                    visibility_range.append(f"{globals()[f"model_pred_t{i}_min"]} - {globals()[f"model_pred_t{i}_max"]}")
                else:
                    raise ValueError("Units must be 'm' or 'km'")
                    
            df['Time Period'] = temp_time_period
    
        elif isinstance(timeperiod, int):
            i = timeperiod
            df['Time Period'] = [f"T+{i}"]
            globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
            fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
            
            if units == "m":
                visibility_range.append(f"{max(round(globals()[f"model_pred_t{i}"]-rmse_scores[i],2),0)} - {round(globals()[f"model_pred_t{i}"] + rmse_scores[i],2)}")
            elif units == "km":
                globals()[f"model_pred_t{i}_min"] = max(round(float((globals()[f"model_pred_t{i}"]-rmse_scores[i])/1000),2),0)
                globals()[f"model_pred_t{i}_max"] = max(round(float((globals()[f"model_pred_t{i}"]+rmse_scores[i])/1000),2),0)
                visibility_range.append(f"{globals()[f"model_pred_t{i}_min"]} - {globals()[f"model_pred_t{i}_max"]}")
            else:
                raise ValueError("Units must be 'm' or 'km'")
    
        else:
            raise ValueError("Timeperiod must be 'all', a tuple or an integer")        
                
        df[f'Visibility Range in {units.upper()} of Point Value'] = visibility_range

    elif output == "both":
        
        if timeperiod == "all":
            df['Time Period'] = ['T+1', 'T+2', 'T+3', 'T+4', 'T+5', 'T+6', 'T+7', 'T+8', 'T+9', 'T+10', 'T+11', 'T+12', 'T+13', 'T+14', 'T+15', 'T+16', 'T+17', 'T+18', 'T+19', 'T+20', 'T+21', 'T+22', 'T+23', 'T+24']
            for i in range(1,25):
                globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
                fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
                
                if units == "m":
                    visibility_range.append(f"{max(round(globals()[f"model_pred_t{i}"]-rmse_scores[i],2),0)} - {round(globals()[f"model_pred_t{i}"] + rmse_scores[i],2)}")
                    visibility_pred.append(globals()[f"model_pred_t{i}"])
                elif units == "km":
                    globals()[f"model_pred_t{i}_min"] = max(round(float((globals()[f"model_pred_t{i}"]-rmse_scores[i])/1000),2),0)
                    globals()[f"model_pred_t{i}_max"] = max(round(float((globals()[f"model_pred_t{i}"]+rmse_scores[i])/1000),2),0)
                    visibility_range.append(f"{globals()[f"model_pred_t{i}_min"]} - {globals()[f"model_pred_t{i}_max"]}")
                    globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_pred_t{i}"]/1000),2)
                    visibility_pred.append(globals()[f"model_pred_t{i}"])
                else:
                    raise ValueError("Units must be 'm' or 'km'")
    
    
        elif isinstance(timeperiod, tuple): 
            start,end = timeperiod
            temp_time_period  = []
            for i in range(start,end+1): 
                time_period_input = f"T+{i}"
                temp_time_period.append(time_period_input)
                globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
                fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
                
                if units == "m":
                    visibility_range.append(f"{max(round(globals()[f"model_pred_t{i}"]-rmse_scores[i],2),0)} - {round(globals()[f"model_pred_t{i}"] + rmse_scores[i],2)}")
                    visibility_pred.append(globals()[f"model_pred_t{i}"])
                elif units == "km":
                    globals()[f"model_pred_t{i}_min"] = max(round(float((globals()[f"model_pred_t{i}"]-rmse_scores[i])/1000),2),0)
                    globals()[f"model_pred_t{i}_max"] = max(round(float((globals()[f"model_pred_t{i}"]+rmse_scores[i])/1000),2),0)
                    visibility_range.append(f"{globals()[f"model_pred_t{i}_min"]} - {globals()[f"model_pred_t{i}_max"]}")
                    globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_pred_t{i}"]/1000),2)
                    visibility_pred.append(globals()[f"model_pred_t{i}"])
                else:
                    raise ValueError("Units must be 'm' or 'km'")
                    
            df['Time Period'] = temp_time_period
    
        elif isinstance(timeperiod, int):
            i = timeperiod
            df['Time Period'] = [f"T+{i}"]
            globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
            fog_class_list.append(fog_classification(globals()[f"model_pred_t{i}"]))
                
            if units == "m":
                visibility_range.append(f"{max(round(globals()[f"model_pred_t{i}"]-rmse_scores[i],2),0)} - {round(globals()[f"model_pred_t{i}"] + rmse_scores[i],2)}")
                visibility_pred.append(globals()[f"model_pred_t{i}"])
            elif units == "km":
                globals()[f"model_pred_t{i}_min"] = max(round(float((globals()[f"model_pred_t{i}"]-rmse_scores[i])/1000),2),0)
                globals()[f"model_pred_t{i}_max"] = max(round(float((globals()[f"model_pred_t{i}"]+rmse_scores[i])/1000),2),0)
                visibility_range.append(f"{globals()[f"model_pred_t{i}_min"]} - {globals()[f"model_pred_t{i}_max"]}")
                globals()[f"model_pred_t{i}"] = round(float(globals()[f"model_pred_t{i}"]/1000),2)
                visibility_pred.append(globals()[f"model_pred_t{i}"])
            else:
                raise ValueError("Units must be 'm' or 'km'")
    
        else:
            raise ValueError("Timeperiod must be 'all', a tuple or an integer")        

        df[f'Visibility in {units.upper()} of Point Value'] = visibility_pred
        df[f'Visibility Range in {units.upper()} of Point Value'] = visibility_range 

    else:
        raise ValueError("Output must be 'point', 'range' or 'both'")

    # For Category to be in final dataset or not
    if category == True:
        df['Fog Classification'] = fog_class_list
    elif category == False:
        pass
    else:
        raise ValueError("""Category must be either True or False [Without " "]""")

    if export == True:
        df.to_csv(f"Fog Prediction for {inputs_given[0]}-{inputs_given[1]}-{inputs_given[2]}-T{inputs_given[3]}.csv",index=False)
        print("------------> File Saved !!! <------------")
    elif export == False:
        pass 
    else:
        raise ValueError("""Category must be either True or False [Without " "]""")

    return df


if __name__ == "__main__":
    print(output_gen((13,1,2025,0,171.6546875,255.7205882,10,10,100,250,3,156.1938,0),"both","m",'all',True,False) ) # Just for example