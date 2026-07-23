import streamlit as st
import pickle
import pandas as pd
from utilities import inputs_processing, fog_classification, clock_emoji ,color_codes
import matplotlib.pyplot as plt

timeperiod_name_list = [] # Includes ["T+1","T+2"........]

def models_loading(): # Loading the models
    for i in range(1,25):
        timeperiod_name_list.append(f"T+{i}")
        with open(fr"Models\VSBK_t{i}.pkl","rb") as f:
            globals()[f"model_t{i}"] = pickle.load(f)

rmse_scores = [369.06 , 489.02 , 567.2 , 621.2 , 656.12 , 680.48 , 697.89 , 712.74 , 726.97 , 736.43 , 740.09 , 740.70 , 739.91 , 746.94 , 748.94 ,
                   748.13 , 746.52 , 739.46 , 739.46 , 732.96 , 743.94 , 748.49 , 737.45 , 740.70] #RMSE Scores

# ---------------------- PAGE INFO ---------------------- #

st.set_page_config(page_title="IMD Visibility Prediction", layout="wide",page_icon="🌫️")
 
st.markdown(
    "<h1 style='text-align: center;'>🌫️ IMD Visibility in Fog Prediction System</h1>", 
    unsafe_allow_html=True
)

# ---------------------- INPUTS ---------------------- #

date = st.date_input("Select Date",format="DD/MM/YYYY") 

col1, col2 = st.columns(2)

with col1:
    Time_hour = st.slider("Hour", 0, 23, 0)
    PM2_5 = st.number_input("PM2.5 (µg/m^3)", value=0.0)
    PM10 = st.number_input("PM10 (µg/m^3)", value=0.0)
    TMPC = st.number_input("Air Temperature (°C)", value=0.0)
    DWPC = st.number_input("Dew Point (°C)", value=0.0)

with col2:
    
    RELH = st.number_input("Relative Humidity (%)", value=0.0)
    DRCT = st.number_input("Wind Direction (degrees)", value=0.0)
    SPED = st.number_input("Wind Speed (m/s)", value=0.0)
    BLH = st.number_input("Boundary Layer Height (m)", value=0.0)
    VSBK_Current = st.number_input("Current Visibility (m)", value=0.0)
 
# ---------------------- PREDICTION ---------------------- #
 
if st.button("🔍 Predict Visibility"):

    with st.spinner("Predicting Visibility 🔍..."):

        models_loading()

        inputs = [inputs_processing(date.day,date.month,date.year,Time_hour,PM2_5,PM10,TMPC,
                    DWPC,RELH,DRCT,SPED,BLH,VSBK_Current)] # Processed Inputs

        visibility_list = [] # Stores the visibility based on given parameters
        color_list = [] # Saves the color of the box in frontend based on visibility
        category_list = [] # Saves the category of the fog
        range_pred_list = [] # Saves the range of the prediction
        upper_range_limit = [] # Saves the upper limit of visibility
        lower_range_limit = [] # Saves the lower limit of visibility
        time_emoji = clock_emoji() # Loads the clock emojis for frontend display

        for i in range(1,25):

            #Generating outputs 
            visibility = round(float(globals()[f"model_t{i}"].predict(inputs)),2)
            category = fog_classification(visibility)
            color = color_codes(visibility)
            lower_limit = max(round(visibility - rmse_scores[i-1],2),0)
            upper_limit = round(visibility + rmse_scores[i-1],2)
            range_pred = f"{lower_limit} m - {upper_limit} m "

            # Appending the lists created above
            visibility_list.append(visibility)
            color_list.append(color)
            category_list.append(category)
            lower_range_limit.append(lower_limit)
            upper_range_limit.append(upper_limit)
            range_pred_list.append(range_pred)

# ---------------------- FRONTEND ---------------------- #

    def info_card(title, value, emoji, color, category, range):
        st.markdown(f"""
                <div style="background-color: {color}; padding: 20px; margin-bottom: 10px; margin-top: 5px; 
                        border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;">
                    <div style="font-size: 30px;">{emoji}</div>
                    <div style="font-size: 25px; font-weight: bold; margin-top: 5px;">{title}</div>
                    <div style="font-size: 24px; color: #0072C6; font-weight: bold;">{value} m</div>
                    <div style="font-size: 19px; font-weight: bold; margin-top: 5px;">{category}</div>
                    <div style="font-size: 15px; color: C230B8; font-weight: bold;">Range : {range}</div>
                </div>
        """, unsafe_allow_html=True)

    for i in range(0,25,4): 
        try:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                info_card(f"T+{i+1}",visibility_list[i],time_emoji[i],color_list[i],category_list[i],range_pred_list[i])
            with col2:
                info_card(f"T+{i+2}",visibility_list[i+1],time_emoji[i+1],color_list[i+1],category_list[i+1],range_pred_list[i+1])
            with col3:
                info_card(f"T+{i+3}",visibility_list[i+2],time_emoji[i+2],color_list[i+2],category_list[i+2],range_pred_list[i+2])
            with col4:
                info_card(f"T+{i+4}",visibility_list[i+3],time_emoji[i+3],color_list[i+3],category_list[i+3],range_pred_list[i+3])
        except:
            pass

# ---------------------- SUMMARY LINE ---------------------- #

    min_visibility = min(visibility_list)
    max_visibility = max(visibility_list)

    min_time = timeperiod_name_list[visibility_list.index(min_visibility)]
    max_time = timeperiod_name_list[visibility_list.index(max_visibility)]

    avg_visibility = round(sum(visibility_list)/len(visibility_list),2)

    worst_fog = fog_classification(min_visibility)
    best_fog = fog_classification(max_visibility)

    summary_min_visi = f"The lowest predicted visibility is {min_visibility:.2f} m ({worst_fog}) during {min_time}"
    summary_max_visi = f"The highest predicted visibility is {max_visibility:.2f} m ({best_fog}) during {max_time}"
    summary_avg_visi = f"The average visibility for the forecast period is {avg_visibility:.2f} m"

    diff_0_12 = visibility_list[11] - visibility_list[0]
    diff_12_24 = visibility_list[23] - visibility_list[11]

    # ---------- Trend 0-12 ----------
    if diff_0_12 > 100:
        trend_0_12 = "improving"
        color_trend_0_12 = "#006400"
    elif diff_0_12 < -100:
        trend_0_12 = "deteriorating"
        color_trend_0_12 = "#8B0000"
    else:
        trend_0_12 = "remaining nearly constant"
        color_trend_0_12 = "#B8860B"

    # ---------- Trend 12-24 ----------
    if diff_12_24 > 100:
        trend_12_24 = "improving"
        color_trend_12_24 = "#006400"
    elif diff_12_24 < -100:
        trend_12_24 = "deteriorating"
        color_trend_12_24 = "#8B0000"
    else:
        trend_12_24 = "remaining nearly constant"
        color_trend_12_24 = "#B8860B"

    st.markdown(f"""
        <div style="background-color: #e0f7da; padding: 30px; margin-top: 20px;
                border-radius: 15px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            <div style="font-size: 25px; font-weight: bold;"> Summary of Results </div>
            <div style="font-size: 20px; font-weight: bold; color: C230B8; margin-top: 15px;">{summary_min_visi}</div>
            <div style="font-size: 20px; font-weight: bold; color: C230B8; margin-top: 15px;">{summary_max_visi}</div>
            <div style="font-size: 20px; font-weight: bold; color: C230B8; margin-top: 15px;">{summary_avg_visi}</div>
            <div style="font-size: 20px; font-weight: bold; margin-top: 15px;">
            Overall Trend :- <span style="color:{color_trend_0_12};"> {trend_0_12.upper()} </span>
            during the first 12 hours, followed by
            <span style="color:{color_trend_12_24};"> {trend_12_24.upper()} </span>
            during the next 12 hours.
        </div> """, unsafe_allow_html=True)

# ---------------------- GRAPHICAL REPRESENTATION ---------------------- #

    st.markdown("<h2 style='text-align: center;'>Visibility Trend</h2>", unsafe_allow_html=True)
    with st.spinner("Generating Visibility Trend 📈📉"):
    
        fig, ax = plt.subplots(figsize=(20, 6)) 
        ax.fill_between(timeperiod_name_list, lower_range_limit, upper_range_limit, color='lightblue', alpha=0.9, label='Prediction Interval (±RMSE)')
        ax.plot(timeperiod_name_list, upper_range_limit, color='blue', linestyle='--', alpha=0.7, label='Upper Limit Boundary')
        ax.plot(timeperiod_name_list, lower_range_limit, color='blue', linestyle='--', alpha=0.7, label='Lower Limit Boundary')
        ax.plot(timeperiod_name_list, visibility_list, "bo" , color='#00008B', linestyle='--', linewidth=1, label='Predicted Value')
        
        for i in range(0,24,2):
            ax.text(x = timeperiod_name_list[i], y = visibility_list[i]+100, s = f"{visibility_list[i]}", ha='center') 
        for i in range(1,24,2):
            ax.text(x = timeperiod_name_list[i], y = visibility_list[i]-150, s = f"{visibility_list[i]}", ha='center') 
        
        ax.set_xlabel("Number of Observations (Hours Ahead)", fontsize=11)
        ax.set_ylabel("Visibility (m)", fontsize=11)
        plt.xticks(rotation=45)
        ax.legend(loc='best', frameon=True)
    
        st.pyplot(fig, bbox_inches='tight')

# ---------------------- INFORMATION ---------------------- #

    with st.expander("Visibility Color Guide 🤔"):
    
        st.markdown("""
        The forecast cards use a **color coded visibility scale** to help users quickly
        understand the expected fog intensity and visibility conditions. Each prediction
        is assigned a color based on the forecasted visibility, making it easier to
        identify hazardous weather conditions at a glance.

        | Color | Visibility Range (m) | Fog Category | Interpretation |
        |:------|:--------------------:|:------------|:---------------|
        | 🟩 | **≥ 501 m** | **Shallow Fog** | Visibility is relatively good with only light to no fog conditions. |
        | 🟨 | **201 - 500 m** | **Moderate Fog** | Moderate reduction in visibility. Drivers and pilots should exercise caution. |
        | 🟧 | **50 - 200 m** | **Dense Fog** | Significantly reduced visibility. Travel conditions may become hazardous. |
        | 🟥 | **< 50 m** | **Very Dense Fog** | Extremely poor visibility. High risk for transportation and outdoor operations. |
        """, unsafe_allow_html=True)

# ---------------------- DOWNLOADING CSV ---------------------- #

    with st.expander("Download in CSV Format 📥"):
        df = pd.DataFrame({
        "Time" : timeperiod_name_list,
        "Visibility (m)" : visibility_list,
        "Range of Visibility" : range_pred_list,
        "Fog Classification" : category_list
        })
      
        st.download_button("📥 Download CSV",df.to_csv(index=False),
        f"Visibility Prediction For {date.day}-{date.month}-{date.year}-T+{Time_hour}.csv")
    
# ---------------------- FOOTER ---------------------- #
st.markdown("""
    <hr style="margin-top: 2rem; margin-bottom: 0;">
    <div style="text-align: center; color: grey; font-size: 14px; padding: 10px 0;">
        Disclaimer : The data to train the models is taken from IMD's official portal
    </div>
    <div style="text-align: center; color: grey; font-size: 14px; padding: 10px 0;">
        © 2026 Kunsh Bhatia
    </div>
""", unsafe_allow_html=True) 
