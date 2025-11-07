import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import get_connection

# ------------------ Page setup & theme ------------------
st.set_page_config(page_title="🌾 AgriWeather Database System", layout="wide")
st.markdown("""
<style>
    .main { background-color:#0f1116; }
    h1,h2,h3 { color:#e8f5e9; }
    .css-1d391kg, .css-ffhzg2 { color:#c8e6c9 !important; } /* body text */
    .stButton>button {
        background: linear-gradient(90deg, #43a047, #1b5e20);
        color: #fff; font-weight:600; border-radius:10px;
    }
    .stButton>button:hover { background:#2e7d32; }
    .block-container { padding-top:2rem; }
</style>
""", unsafe_allow_html=True)

# ------------------ Session bootstrap ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

# ------------------ Helpers ------------------
def stop_if_no_conn(conn):
    if not conn:
        st.error("❌ Could not connect to MySQL. Check `db_config.py`, MySQL service, and DB name.")
        st.stop()

def run_query(conn, sql, params=None, dict_cursor=True):
    """Run a SELECT and return DataFrame."""
    cur = conn.cursor(dictionary=dict_cursor)
    cur.execute(sql, params or ())
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows)

# ------------------ Login screen ------------------
if not st.session_state.logged_in:
    st.title("🔐 Login to Agriculture Weather DB System")
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        conn = get_connection()
        stop_if_no_conn(conn)
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Users WHERE Username=%s AND Password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            st.session_state.logged_in = True
            st.session_state.role = user["Role"]
            st.session_state.username = user["Username"]
            st.success(f"✅ Welcome {user['Username']}  •  Role: {user['Role']}")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
    st.stop()

# ------------------ App layout ------------------
left, right = st.columns([7, 1])
with left:
    st.title("🌾 Agriculture Weather Database System")
    st.write("Efficient management of farms, crops, and weather insights.")
with right:
    st.caption(f"👤 **{st.session_state.username}**  •  *{st.session_state.role}*")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()

# Sidebar
menu = [
    "🏠 Home",
    "📋 View Data",
    "➕ Create Records",
    "🌤 Weather Insights",
    "📊 Analytics Dashboard",
    "🏆 Leaderboard",
]
if st.session_state.role == "Admin":
    menu.append("👥 User Management")

choice = st.sidebar.radio("Navigate", menu)

# Single shared connection
conn = get_connection()
stop_if_no_conn(conn)

# ------------------ Pages ------------------
if choice == "🏠 Home":
    st.subheader("Welcome to AgriWeather 🌦️")
    st.write(
        "This system helps farmers and administrators track crop performance, "
        "manage weather data, and assess environmental suitability."
    )
    st.image(
        "https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=1600&auto=format&fit=crop",
        caption="Farms, Crops & Weather",
        use_container_width=True
    )

elif choice == "📋 View Data":
    st.subheader("📋 View and Manage Data")
    tables = ["Farmers", "Farms", "Crops", "Crop_Seasons", "Weather_Stations", "Weather_Readings", "Cultivates", "Suitability_Assessment"]
    table = st.selectbox("Select table", tables, index=0)
    df = run_query(conn, f"SELECT * FROM `{table}`")
    st.dataframe(df, use_container_width=True)
    st.caption(f"Rows: {len(df)}")
    
    # Update and Delete operations
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### ✏️ Update Record")
        if table == "Farmers":
            with st.form("update_farmer", clear_on_submit=False):
                fid = st.number_input("Farmer ID", min_value=1, step=1, key="upd_farmer_id")
                new_name = st.text_input("Name")
                new_phone = st.text_input("Phone Number")
                new_dob = st.date_input("Date of Birth")
                submitted = st.form_submit_button("✏️ Update Farmer")
            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE Farmers SET Name=%s, Phone_No=%s, DOB=%s WHERE FarmerID=%s", 
                               (new_name, new_phone, new_dob, fid))
                    conn.commit()
                    cur.close()
                    st.success("✅ Farmer updated")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        elif table == "Farms":
            with st.form("update_farm", clear_on_submit=False):
                farm_seq = st.number_input("Farm Seq", min_value=1, step=1, key="upd_farm_seq")
                new_name = st.text_input("Farm Name")
                new_area = st.number_input("Area (acres)", min_value=0.0, step=0.1, format="%.2f")
                new_farmer_id = st.number_input("Farmer ID", min_value=1, step=1)
                submitted = st.form_submit_button("✏️ Update Farm")
            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE Farms SET Farm_Name=%s, Area_acres=%s, FarmerID=%s WHERE FarmSeq=%s", 
                               (new_name, new_area, new_farmer_id, farm_seq))
                    conn.commit()
                    cur.close()
                    st.success("✅ Farm updated")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        elif table == "Crops":
            with st.form("update_crop", clear_on_submit=False):
                crop_id = st.number_input("Crop ID", min_value=1, step=1, key="upd_crop_id")
                new_name = st.text_input("Crop Name")
                submitted = st.form_submit_button("✏️ Update Crop")
            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE Crops SET Crop_Name=%s WHERE CropID=%s", (new_name, crop_id))
                    conn.commit()
                    cur.close()
                    st.success("✅ Crop updated")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        elif table == "Crop_Seasons":
            with st.form("update_season", clear_on_submit=False):
                season_id = st.number_input("Season ID", min_value=1, step=1, key="upd_season_id")
                new_name = st.text_input("Season Name")
                new_start = st.date_input("Start Date")
                new_end = st.date_input("End Date")
                submitted = st.form_submit_button("✏️ Update Season")
            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE Crop_Seasons SET Season_Name=%s, Start_Date=%s, End_Date=%s WHERE SeasonID=%s", 
                               (new_name, new_start, new_end, season_id))
                    conn.commit()
                    cur.close()
                    st.success("✅ Season updated")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        elif table == "Weather_Stations":
            with st.form("update_station", clear_on_submit=False):
                station_id = st.number_input("Station ID", min_value=1, step=1, key="upd_station_id")
                new_name = st.text_input("Station Name")
                new_state = st.text_input("State")
                new_city = st.text_input("City")
                submitted = st.form_submit_button("✏️ Update Station")
            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE Weather_Stations SET Station_Name=%s, State=%s, City=%s WHERE StationID=%s", 
                               (new_name, new_state, new_city, station_id))
                    conn.commit()
                    cur.close()
                    st.success("✅ Station updated")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        elif table == "Weather_Readings":
            with st.form("update_reading", clear_on_submit=False):
                rid = st.number_input("Reading ID", min_value=1, step=1, key="upd_reading_id")
                new_temp = st.number_input("Temperature (°C)", step=0.1, format="%.2f")
                new_humidity = st.number_input("Humidity (%)", step=0.1, format="%.2f")
                new_rainfall = st.number_input("Rainfall (mm)", step=0.1, format="%.2f")
                submitted = st.form_submit_button("✏️ Update Reading")
            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE Weather_Readings SET Temperature=%s, Humidity=%s, Rainfall=%s WHERE ReadingID=%s", 
                               (new_temp, new_humidity, new_rainfall, rid))
                    conn.commit()
                    cur.close()
                    st.success("✅ Weather reading updated")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        elif table == "Suitability_Assessment":
            with st.form("update_suitability", clear_on_submit=False):
                season_id = st.number_input("Season ID", min_value=1, step=1, key="upd_suit_season")
                station_id = st.number_input("Station ID", min_value=1, step=1, key="upd_suit_station")
                crop_id = st.number_input("Crop ID", min_value=1, step=1, key="upd_suit_crop")
                new_score = st.number_input("Assessment Score", min_value=0.0, max_value=10.0, step=0.1, format="%.2f")
                submitted = st.form_submit_button("✏️ Update Assessment")
            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE Suitability_Assessment SET Assessment_Score=%s WHERE SeasonID=%s AND StationID=%s AND CropID=%s", 
                               (new_score, season_id, station_id, crop_id))
                    conn.commit()
                    cur.close()
                    st.success("✅ Assessment updated")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        else:
            st.info(f"Update operation: Select a record ID and modify the fields, then click update.")
    
    with col2:
        st.write("### 🗑️ Delete Record")
        
        # Check if user has delete permission
        can_delete = True
        if table == "Weather_Stations" and st.session_state.role != "Admin":
            can_delete = False
            st.warning("⚠️ Admin privileges required to delete Weather Stations")
        
        if can_delete:
            if table == "Farmers":
                with st.form("delete_farmer", clear_on_submit=False):
                    fid = st.number_input("Farmer ID", min_value=1, step=1, key="del_farmer_id")
                    submitted = st.form_submit_button("🗑️ Delete", type="primary")
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Farmers WHERE FarmerID=%s", (fid,))
                        conn.commit()
                        cur.close()
                        st.warning(f"🗑️ Farmer {fid} deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            elif table == "Farms":
                with st.form("delete_farm", clear_on_submit=False):
                    farm_seq = st.number_input("Farm Seq", min_value=1, step=1, key="del_farm_seq")
                    submitted = st.form_submit_button("🗑️ Delete", type="primary")
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Farms WHERE FarmSeq=%s", (farm_seq,))
                        conn.commit()
                        cur.close()
                        st.warning(f"🗑️ Farm {farm_seq} deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            elif table == "Crops":
                with st.form("delete_crop", clear_on_submit=False):
                    crop_id = st.number_input("Crop ID", min_value=1, step=1, key="del_crop_id")
                    submitted = st.form_submit_button("🗑️ Delete", type="primary")
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Crops WHERE CropID=%s", (crop_id,))
                        conn.commit()
                        cur.close()
                        st.warning(f"🗑️ Crop {crop_id} deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            elif table == "Weather_Readings":
                with st.form("delete_reading", clear_on_submit=False):
                    rid = st.number_input("Reading ID", min_value=1, step=1, key="del_reading_id")
                    submitted = st.form_submit_button("🗑️ Delete", type="primary")
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Weather_Readings WHERE ReadingID=%s", (rid,))
                        conn.commit()
                        cur.close()
                        st.warning(f"🗑️ Reading {rid} deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            elif table == "Weather_Stations":
                with st.form("delete_station", clear_on_submit=False):
                    sid = st.number_input("Station ID", min_value=1, step=1, key="del_station_id")
                    submitted = st.form_submit_button("🗑️ Delete", type="primary")
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Weather_Stations WHERE StationID=%s", (sid,))
                        conn.commit()
                        cur.close()
                        st.warning(f"🗑️ Station {sid} deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            elif table == "Crop_Seasons":
                with st.form("delete_season", clear_on_submit=False):
                    season_id = st.number_input("Season ID", min_value=1, step=1, key="del_season_id")
                    submitted = st.form_submit_button("🗑️ Delete", type="primary")
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Crop_Seasons WHERE SeasonID=%s", (season_id,))
                        conn.commit()
                        cur.close()
                        st.warning(f"🗑️ Season {season_id} deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            elif table == "Cultivates":
                with st.form("delete_cultivates", clear_on_submit=False):
                    farm_seq = st.number_input("Farm Seq", min_value=1, step=1, key="del_cult_farm")
                    crop_id = st.number_input("Crop ID", min_value=1, step=1, key="del_cult_crop")
                    season_id = st.number_input("Season ID", min_value=1, step=1, key="del_cult_season")
                    submitted = st.form_submit_button("🗑️ Delete", type="primary")
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Cultivates WHERE FarmSeq=%s AND CropID=%s AND SeasonID=%s", 
                                   (farm_seq, crop_id, season_id))
                        conn.commit()
                        cur.close()
                        st.warning(f"🗑️ Cultivation record deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            elif table == "Suitability_Assessment":
                with st.form("delete_suitability", clear_on_submit=False):
                    season_id = st.number_input("Season ID", min_value=1, step=1, key="del_suit_season")
                    station_id = st.number_input("Station ID", min_value=1, step=1, key="del_suit_station")
                    crop_id = st.number_input("Crop ID", min_value=1, step=1, key="del_suit_crop")
                    submitted = st.form_submit_button("🗑️ Delete", type="primary")
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("DELETE FROM Suitability_Assessment WHERE SeasonID=%s AND StationID=%s AND CropID=%s", 
                                   (season_id, station_id, crop_id))
                        conn.commit()
                        cur.close()
                        st.warning(f"🗑️ Assessment deleted")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            else:
                st.info(f"Select a table with delete support")

elif choice == "➕ Create Records":
    st.subheader("➕ Create New Records")
    
    table_choice = st.selectbox("Select Table", [
        "Farmers", "Farms", "Crops", "Crop_Seasons", 
        "Weather_Stations", "Weather_Readings", "Cultivates", "Suitability_Assessment"
    ])
    
    if table_choice == "Farmers":
        with st.form("farmer_form"):
            fid = st.number_input("Farmer ID", min_value=1, step=1)
            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number")
            dob = st.date_input("Date of Birth")
            submitted = st.form_submit_button("Add Farmer")
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Farmers (FarmerID, Name, Phone_No, DOB) VALUES (%s, %s, %s, %s)",
                    (fid, name, phone, dob)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ Farmer '{name}' added")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif table_choice == "Farms":
        with st.form("farm_form"):
            farm_seq = st.number_input("Farm Seq", min_value=1, step=1)
            farm_name = st.text_input("Farm Name")
            area = st.number_input("Area (acres)", min_value=0.0, step=0.1, format="%.2f")
            farmer_id = st.number_input("Farmer ID", min_value=1, step=1)
            submitted = st.form_submit_button("Add Farm")
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Farms (FarmSeq, Farm_Name, Area_acres, FarmerID) VALUES (%s, %s, %s, %s)",
                    (farm_seq, farm_name, area, farmer_id)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ Farm '{farm_name}' added")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif table_choice == "Crops":
        with st.form("crop_form"):
            crop_id = st.number_input("Crop ID", min_value=1, step=1)
            crop_name = st.text_input("Crop Name")
            submitted = st.form_submit_button("Add Crop")
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Crops (CropID, Crop_Name) VALUES (%s, %s)",
                    (crop_id, crop_name)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ Crop '{crop_name}' added")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif table_choice == "Crop_Seasons":
        with st.form("season_form"):
            season_id = st.number_input("Season ID", min_value=1, step=1)
            season_name = st.text_input("Season Name")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            submitted = st.form_submit_button("Add Season")
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Crop_Seasons (SeasonID, Season_Name, Start_Date, End_Date) VALUES (%s, %s, %s, %s)",
                    (season_id, season_name, start_date, end_date)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ Season '{season_name}' added")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif table_choice == "Weather_Stations":
        with st.form("station_form"):
            station_id = st.number_input("Station ID", min_value=1, step=1)
            station_name = st.text_input("Station Name")
            state = st.text_input("State")
            city = st.text_input("City")
            submitted = st.form_submit_button("Add Station")
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Weather_Stations (StationID, Station_Name, State, City) VALUES (%s, %s, %s, %s)",
                    (station_id, station_name, state, city)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ Station '{station_name}' added")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif table_choice == "Weather_Readings":
        with st.form("reading_form"):
            reading_id = st.number_input("Reading ID", min_value=1, step=1)
            station_id = st.number_input("Station ID", min_value=1, step=1)
            datetime_val = st.text_input("DateTime (YYYY-MM-DD HH:MM:SS)", value="2025-11-06 12:00:00")
            temperature = st.number_input("Temperature (°C)", step=0.1, format="%.2f")
            humidity = st.number_input("Humidity (%)", step=0.1, format="%.2f")
            rainfall = st.number_input("Rainfall (mm)", step=0.1, format="%.2f")
            submitted = st.form_submit_button("Add Reading")
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Weather_Readings (ReadingID, StationID, DateTime, Temperature, Humidity, Rainfall) VALUES (%s, %s, %s, %s, %s, %s)",
                    (reading_id, station_id, datetime_val, temperature, humidity, rainfall)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ Weather Reading {reading_id} added")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif table_choice == "Cultivates":
        with st.form("cultivates_form"):
            farm_seq = st.number_input("Farm Seq", min_value=1, step=1)
            crop_id = st.number_input("Crop ID", min_value=1, step=1)
            season_id = st.number_input("Season ID", min_value=1, step=1)
            submitted = st.form_submit_button("Add Cultivation")
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Cultivates (FarmSeq, CropID, SeasonID) VALUES (%s, %s, %s)",
                    (farm_seq, crop_id, season_id)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ Cultivation record added")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif table_choice == "Suitability_Assessment":
        with st.form("suitability_form"):
            season_id = st.number_input("Season ID", min_value=1, step=1)
            station_id = st.number_input("Station ID", min_value=1, step=1)
            crop_id = st.number_input("Crop ID", min_value=1, step=1)
            score = st.number_input("Assessment Score", min_value=0.0, max_value=10.0, step=0.1, format="%.2f")
            submitted = st.form_submit_button("Add Assessment")
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Suitability_Assessment (SeasonID, StationID, CropID, Assessment_Score) VALUES (%s, %s, %s, %s)",
                    (season_id, station_id, crop_id, score)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ Suitability Assessment added")
            except Exception as e:
                st.error(f"❌ Error: {e}")

elif choice == "🌤 Weather Insights":
    # ==============================
    # ⚙ Weather Data Analysis
    # ==============================
    
    st.subheader("⚙ Weather Data Analysis")
    
    with st.expander("🌦 Get Weather Data by Station"):
        st.write("Retrieve detailed readings and compute average temperature for a specific weather station.")
    
        station_id = st.text_input("Enter Station ID", key="proc_station_id")
    
        if st.button("Get Weather Data", key="btn_proc_weather"):
            if station_id.strip() == "":
                st.warning("Please enter a valid Station ID.")
            else:
                try:
                    cur = conn.cursor()
                    
                    # -----------------------------
                    # 1️⃣ Run Stored Procedure: GetWeatherByStation
                    # -----------------------------
                    cur.callproc("GetWeatherByStation", [station_id])
                    for result in cur.stored_results():
                        data = result.fetchall()
                        if data:
                            df = pd.DataFrame(
                                data,
                                columns=["StationID", "DateTime", "Temperature", "Humidity", "Rainfall"]
                            )
                            st.success(f"✅ Weather readings for Station {station_id}")
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.info(f"No readings found for Station {station_id}")
    
                    # -----------------------------
                    # 2️⃣ Run Function: AvgTemperature
                    # -----------------------------
                    avg_query = "SELECT AvgTemperature(%s) AS AvgTemp"
                    cur.execute(avg_query, (station_id,))
                    avg_result = cur.fetchone()
    
                    if avg_result and avg_result[0] is not None:
                        avg_temp = round(avg_result[0], 2)
                        st.markdown(
                            f"<h4 style='color:#76c893;'>🌡 Average Temperature: "
                            f"<b>{avg_temp} °C</b></h4>", unsafe_allow_html=True
                        )
                    else:
                        st.info("No average temperature data found for this station.")
    
                    cur.close()
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    
    # ---------------------------------------
    # 🌾 Get Crop Suitability
    # ---------------------------------------
    with st.expander("🌾 Get Crop Suitability"):
        st.write("View suitability results for a specific crop by name.")
    
        crop_name = st.text_input("Enter Crop Name (e.g., Wheat)", key="proc_crop_name")
    
        if st.button("Get Suitability Data", key="btn_proc_suitability"):
            if crop_name.strip() == "":
                st.warning("Please enter a crop name.")
            else:
                try:
                    cur = conn.cursor()
                    
                    # Run Stored Procedure: GetSuitability
                    cur.callproc("GetSuitability", [crop_name])
                    for result in cur.stored_results():
                        data = result.fetchall()
                        if data:
                            df = pd.DataFrame(
                                data,
                                columns=["Crop_Name", "Season_Name", "Assessment_Score"]
                            )
                            st.success(f"✅ Suitability results for {crop_name}")
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.info(f"No suitability data found for crop '{crop_name}'")
    
                    cur.close()
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    
    # ---------------------------------------
    # 🌡 Average Temperature
    # ---------------------------------------
    with st.expander("🌡 Average Temperature Analysis"):
        st.write("Compute the average temperature for a specific station.")
    
        station_id_func = st.text_input("Enter Station ID", key="func_station_id")
    
        if st.button("Calculate Average Temperature", key="btn_func_avgtemp"):
            if station_id_func.strip() == "":
                st.warning("Please enter a valid Station ID.")
            else:
                try:
                    df = run_query(conn, "SELECT AvgTemperature(%s) AS AvgTemp", (station_id_func,))
                    avg_val = df.iloc[0]["AvgTemp"]
    
                    if avg_val is not None:
                        st.success(f"🌡 Average Temperature at Station {station_id_func}: {round(avg_val,2)} °C")
                    else:
                        st.info("No readings available for this station.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    
    # ---------------------------------------
    # 🌾 Area Conversion
    # ---------------------------------------
    with st.expander("🌾 Convert Farm Area to Hectares"):
        st.write("Convert a farm's area from acres to hectares.")
    
        farm_seq = st.text_input("Enter Farm Sequence ID", key="func_farmseq")
    
        if st.button("Convert Area", key="btn_func_area"):
            if farm_seq.strip() == "":
                st.warning("Please enter a valid Farm Sequence ID.")
            else:
                try:
                    df = run_query(conn, "SELECT AreaHectares(%s) AS AreaHa", (farm_seq,))
                    ha_val = df.iloc[0]["AreaHa"]
    
                    if ha_val is not None:
                        st.success(f"🌾 Farm {farm_seq} area in hectares: {round(ha_val,2)} ha")
                    else:
                        st.info("No data found for this farm.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

elif choice == "📊 Analytics Dashboard":
    st.subheader("📊 Weather Analytics")
    q = """
        SELECT ws.State, AVG(wr.Rainfall) AS Avg_Rainfall, AVG(wr.Temperature) AS Avg_Temp
        FROM Weather_Stations ws
        JOIN Weather_Readings wr ON ws.StationID = wr.StationID
        GROUP BY ws.State
        ORDER BY ws.State;
    """
    df = run_query(conn, q)

    if df.empty:
        st.warning("No data available.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(df, x="State", y="Avg_Rainfall", title="🌧️ Average Rainfall by State", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.line(df, x="State", y="Avg_Temp", markers=True, title="🌡️ Average Temperature by State")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Insights")
        st.write("- Use rainfall & temperature averages to decide crop–season suitability.")
        st.write("- Monsoon states show higher rainfall; consider rice, sugarcane, etc.")

elif choice == "🏆 Leaderboard":
    st.subheader("🏆 Leaderboard & Rankings")
    st.write("Discover top performers based on various metrics")
    
    search_category = st.selectbox("What would you like to search for?", [
        "🌾 High-Performing Farmers",
        "🌱 Best Crops for Cultivation",
        "🌧️ High Rainfall Stations"
    ])
    
    if search_category == "🌾 High-Performing Farmers":
        st.write("### Find Farmers with Large Farms")
        st.write("This search finds farmers who own farms larger than the average farm size in the system.")
        
        # Show average farm size first
        avg_query = "SELECT AVG(Area_acres) AS avg_area FROM Farms"
        avg_df = run_query(conn, avg_query)
        if not avg_df.empty:
            avg_area = avg_df.iloc[0]['avg_area']
            st.metric("Average Farm Size", f"{avg_area:.2f} acres")
        
        if st.button("🔍 Search for High-Performing Farmers", key="search_farmers"):
            # Using nested subquery
            q = """
                SELECT f.Name, f.FarmerID, fa.Farm_Name, fa.Area_acres
                FROM Farmers f
                JOIN Farms fa ON f.FarmerID = fa.FarmerID
                WHERE f.FarmerID IN (
                    SELECT FarmerID FROM Farms
                    WHERE Area_acres > (SELECT AVG(Area_acres) FROM Farms)
                )
                ORDER BY fa.Area_acres DESC
            """
            df = run_query(conn, q)
            if df.empty:
                st.info("No farmers found with above-average farm areas.")
            else:
                st.success(f"✅ Found {len(df)} farmers with farms larger than average")
                st.dataframe(df, use_container_width=True)
                
                # Show visualization
                if len(df) > 0:
                    import plotly.express as px
                    fig = px.bar(df, x="Name", y="Area_acres", title="Farm Sizes (Above Average)", 
                                color="Area_acres", labels={"Area_acres": "Area (acres)"})
                    st.plotly_chart(fig, use_container_width=True)
    
    elif search_category == "🌱 Best Crops for Cultivation":
        st.write("### Find Top-Rated Crops")
        st.write("This search finds crops with suitability scores higher than the system average.")
        
        # Show average suitability score
        avg_query = "SELECT AVG(Assessment_Score) AS avg_score FROM Suitability_Assessment"
        avg_df = run_query(conn, avg_query)
        if not avg_df.empty:
            avg_score = avg_df.iloc[0]['avg_score']
            st.metric("Average Suitability Score", f"{avg_score:.2f} / 10")
        
        if st.button("🔍 Search for Best Crops", key="search_crops"):
            # Using nested subquery with HAVING
            q = """
                SELECT c.Crop_Name, AVG(sa.Assessment_Score) AS Avg_Score, COUNT(*) AS Assessment_Count
                FROM Suitability_Assessment sa
                JOIN Crops c ON sa.CropID = c.CropID
                GROUP BY c.Crop_Name
                HAVING AVG(sa.Assessment_Score) > (
                    SELECT AVG(Assessment_Score) FROM Suitability_Assessment
                )
                ORDER BY Avg_Score DESC
            """
            df = run_query(conn, q)
            if df.empty:
                st.info("No crops found with above-average suitability scores.")
            else:
                st.success(f"✅ Found {len(df)} crops with above-average suitability")
                st.dataframe(df, use_container_width=True)
                
                # Show visualization
                if len(df) > 0:
                    import plotly.express as px
                    fig = px.bar(df, x="Crop_Name", y="Avg_Score", title="Top-Rated Crops", 
                                color="Avg_Score", labels={"Avg_Score": "Suitability Score"})
                    st.plotly_chart(fig, use_container_width=True)
    
    elif search_category == "🌧️ High Rainfall Stations":
        st.write("### Find Stations with High Rainfall")
        st.write("This search finds weather stations recording rainfall higher than the system average.")
        
        # Show average rainfall
        avg_query = "SELECT AVG(Rainfall) AS avg_rainfall FROM Weather_Readings"
        avg_df = run_query(conn, avg_query)
        if not avg_df.empty:
            avg_rainfall = avg_df.iloc[0]['avg_rainfall']
            st.metric("Average Rainfall", f"{avg_rainfall:.2f} mm")
        
        if st.button("🔍 Search for High Rainfall Stations", key="search_stations"):
            # Using nested subquery with HAVING
            q = """
                SELECT ws.Station_Name, ws.State, ws.City, AVG(wr.Rainfall) AS Avg_Rainfall
                FROM Weather_Stations ws
                JOIN Weather_Readings wr ON ws.StationID = wr.StationID
                GROUP BY ws.Station_Name, ws.State, ws.City
                HAVING AVG(wr.Rainfall) > (
                    SELECT AVG(Rainfall) FROM Weather_Readings
                )
                ORDER BY Avg_Rainfall DESC
            """
            df = run_query(conn, q)
            if df.empty:
                st.info("No stations found with above-average rainfall.")
            else:
                st.success(f"✅ Found {len(df)} stations with above-average rainfall")
                st.dataframe(df, use_container_width=True)
                
                # Show visualization
                if len(df) > 0:
                    import plotly.express as px
                    fig = px.bar(df, x="Station_Name", y="Avg_Rainfall", title="High Rainfall Stations", 
                                color="Avg_Rainfall", labels={"Avg_Rainfall": "Avg Rainfall (mm)"})
                    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **Note:** These searches use nested SQL queries (subqueries) to compare against average values.")

elif choice == "👥 User Management" and st.session_state.role == "Admin":
    st.subheader("👥 User Management (Admin Only)")
    
    tab1, tab2 = st.tabs(["Create User", "View Users"])
    
    with tab1:
        st.write("### Create New User")
        with st.form("user_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["User", "Admin"])
            submitted = st.form_submit_button("Create User")
        
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Users (Username, Password, Role) VALUES (%s, %s, %s)",
                    (username, password, role)
                )
                conn.commit()
                cur.close()
                st.success(f"✅ User '{username}' created with role '{role}'")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with tab2:
        st.write("### All Users")
        df_users = run_query(conn, "SELECT Username, Role FROM Users")
        st.dataframe(df_users, use_container_width=True)
    
    st.info("✅ This demonstrates: **USER CREATION and PRIVILEGED ACCESS** with GUI")

# clean up
conn.close()
