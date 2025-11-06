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
    "✏️ Update Data",
    "🗑️ Delete Data",
    "⚙️ Procedures & Functions",
    "📊 Analytics Dashboard",
    "🔍 Nested Query Demo",
    "⚡ Triggers Demo",
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
    st.subheader("📋 View Tables")
    tables = ["Farmers", "Farms", "Crops", "Crop_Seasons", "Weather_Stations", "Weather_Readings", "Cultivates", "Suitability_Assessment"]
    table = st.selectbox("Select table", tables, index=0)
    df = run_query(conn, f"SELECT * FROM `{table}`")
    st.dataframe(df, use_container_width=True)
    st.caption(f"Rows: {len(df)}")

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

elif choice == "✏️ Update Data":
    st.subheader("✏️ Update Records")
    
    update_choice = st.selectbox("Select Table to Update", [
        "Weather_Readings", "Farmers", "Farms", "Crops"
    ])
    
    if update_choice == "Weather_Readings":
        st.write("### Update Weather Reading Temperature")
        rid = st.number_input("Reading ID", min_value=1, step=1, key="update_reading")
        new_temp = st.number_input("New Temperature (°C)", step=0.1, format="%.2f")
        if st.button("Update Temperature"):
            try:
                cur = conn.cursor()
                cur.execute("UPDATE Weather_Readings SET Temperature=%s WHERE ReadingID=%s", (new_temp, rid))
                conn.commit()
                cur.close()
                st.success("🌡️ Temperature updated")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif update_choice == "Farmers":
        st.write("### Update Farmer Information")
        fid = st.number_input("Farmer ID", min_value=1, step=1, key="update_farmer")
        new_phone = st.text_input("New Phone Number")
        if st.button("Update Phone"):
            try:
                cur = conn.cursor()
                cur.execute("UPDATE Farmers SET Phone_No=%s WHERE FarmerID=%s", (new_phone, fid))
                conn.commit()
                cur.close()
                st.success("📞 Phone number updated")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif update_choice == "Farms":
        st.write("### Update Farm Area")
        farm_seq = st.number_input("Farm Seq", min_value=1, step=1, key="update_farm")
        new_area = st.number_input("New Area (acres)", min_value=0.0, step=0.1, format="%.2f")
        if st.button("Update Area"):
            try:
                cur = conn.cursor()
                cur.execute("UPDATE Farms SET Area_acres=%s WHERE FarmSeq=%s", (new_area, farm_seq))
                conn.commit()
                cur.close()
                st.success("🌾 Farm area updated")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif update_choice == "Crops":
        st.write("### Update Crop Name")
        crop_id = st.number_input("Crop ID", min_value=1, step=1, key="update_crop")
        new_name = st.text_input("New Crop Name")
        if st.button("Update Name"):
            try:
                cur = conn.cursor()
                cur.execute("UPDATE Crops SET Crop_Name=%s WHERE CropID=%s", (new_name, crop_id))
                conn.commit()
                cur.close()
                st.success("🌱 Crop name updated")
            except Exception as e:
                st.error(f"❌ Error: {e}")

elif choice == "🗑️ Delete Data":
    st.subheader("🗑️ Delete Records")
    
    if st.session_state.role != "Admin":
        st.warning("⚠️ Delete operations are restricted. Admin privileges recommended.")
    
    delete_choice = st.selectbox("Select Table", [
        "Farmers", "Farms", "Crops", "Weather_Readings", "Weather_Stations"
    ])
    
    if delete_choice == "Farmers":
        fid = st.number_input("Farmer ID to Delete", min_value=1, step=1, key="del_farmer")
        if st.button("Delete Farmer", type="primary"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM Farmers WHERE FarmerID=%s", (fid,))
                conn.commit()
                cur.close()
                st.warning(f"🗑️ Farmer ID {fid} deleted")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif delete_choice == "Farms":
        farm_seq = st.number_input("Farm Seq to Delete", min_value=1, step=1, key="del_farm")
        if st.button("Delete Farm", type="primary"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM Farms WHERE FarmSeq=%s", (farm_seq,))
                conn.commit()
                cur.close()
                st.warning(f"🗑️ Farm {farm_seq} deleted")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif delete_choice == "Crops":
        crop_id = st.number_input("Crop ID to Delete", min_value=1, step=1, key="del_crop")
        if st.button("Delete Crop", type="primary"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM Crops WHERE CropID=%s", (crop_id,))
                conn.commit()
                cur.close()
                st.warning(f"🗑️ Crop {crop_id} deleted")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif delete_choice == "Weather_Readings":
        rid = st.number_input("Reading ID to Delete", min_value=1, step=1, key="del_reading")
        if st.button("Delete Reading", type="primary"):
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM Weather_Readings WHERE ReadingID=%s", (rid,))
                conn.commit()
                cur.close()
                st.warning(f"🗑️ Weather Reading {rid} deleted")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    elif delete_choice == "Weather_Stations":
        if st.session_state.role == "Admin":
            sid = st.number_input("Station ID to Delete", min_value=1, step=1, key="del_station")
            if st.button("Delete Station", type="primary"):
                try:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM Weather_Stations WHERE StationID=%s", (sid,))
                    conn.commit()
                    cur.close()
                    st.warning(f"🗑️ Station {sid} deleted")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.error("❌ Admin privileges required to delete Weather Stations")

elif choice == "⚙️ Procedures & Functions":
    st.subheader("⚙️ Stored Procedures and Functions")
    opt = st.selectbox("Select", ["GetWeatherByStation", "GetSuitability", "AvgTemperature", "AreaHectares"])

    if opt == "GetWeatherByStation":
        sid = st.number_input("Station ID", min_value=1, step=1)
        if st.button("Run Procedure"):
            cur = conn.cursor()
            cur.callproc("GetWeatherByStation", [int(sid)])
            for res in cur.stored_results():
                df = pd.DataFrame(res.fetchall(), columns=["StationID", "DateTime", "Temperature", "Humidity", "Rainfall"])
                st.dataframe(df, use_container_width=True)
            cur.close()

    elif opt == "GetSuitability":
        crop = st.text_input("Crop Name")
        if st.button("Run Procedure"):
            cur = conn.cursor()
            cur.callproc("GetSuitability", [crop])
            for res in cur.stored_results():
                df = pd.DataFrame(res.fetchall(), columns=["Crop_Name", "Season_Name", "Assessment_Score"])
                st.dataframe(df, use_container_width=True)
            cur.close()

    elif opt == "AvgTemperature":
        sid = st.number_input("Station ID", min_value=1, step=1)
        if st.button("Run Function"):
            df = run_query(conn, "SELECT AvgTemperature(%s) AS value", (int(sid),))
            st.info(f"Average Temperature: **{df.iloc[0]['value']} °C**")

    elif opt == "AreaHectares":
        fseq = st.number_input("FarmSeq", min_value=1, step=1)
        if st.button("Run Function"):
            df = run_query(conn, "SELECT AreaHectares(%s) AS value", (int(fseq),))
            st.info(f"Area in Hectares: **{df.iloc[0]['value']}**")

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
        
        st.info("✅ This demonstrates: **JOIN query** (Weather_Stations + Weather_Readings) and **AGGREGATE query** (AVG, GROUP BY)")

elif choice == "🔍 Nested Query Demo":
    st.subheader("🔍 Nested Query Demonstration")
    
    query_option = st.selectbox("Select Nested Query", [
        "Farmers with above-average farm areas",
        "Crops with above-average suitability scores",
        "Weather stations with above-average rainfall"
    ])
    
    if query_option == "Farmers with above-average farm areas":
        st.write("### Query: Farmers owning farms larger than average")
        st.code("""
SELECT Name, FarmerID
FROM Farmers
WHERE FarmerID IN (
    SELECT FarmerID FROM Farms
    WHERE Area_acres > (SELECT AVG(Area_acres) FROM Farms)
);
        """, language="sql")
        
        if st.button("Run Query", key="nested1"):
            q = """
                SELECT Name, FarmerID
                FROM Farmers
                WHERE FarmerID IN (
                    SELECT FarmerID FROM Farms
                    WHERE Area_acres > (SELECT AVG(Area_acres) FROM Farms)
                )
            """
            df = run_query(conn, q)
            if df.empty:
                st.info("No farmers found with above-average farm areas.")
            else:
                st.dataframe(df, use_container_width=True)
                st.success(f"✅ Found {len(df)} farmers with above-average farm areas")
    
    elif query_option == "Crops with above-average suitability scores":
        st.write("### Query: Crops with suitability scores above average")
        st.code("""
SELECT c.Crop_Name, AVG(sa.Assessment_Score) AS Avg_Score
FROM Suitability_Assessment sa
JOIN Crops c ON sa.CropID = c.CropID
GROUP BY c.Crop_Name
HAVING AVG(sa.Assessment_Score) > (
    SELECT AVG(Assessment_Score) FROM Suitability_Assessment
);
        """, language="sql")
        
        if st.button("Run Query", key="nested2"):
            q = """
                SELECT c.Crop_Name, AVG(sa.Assessment_Score) AS Avg_Score
                FROM Suitability_Assessment sa
                JOIN Crops c ON sa.CropID = c.CropID
                GROUP BY c.Crop_Name
                HAVING AVG(sa.Assessment_Score) > (
                    SELECT AVG(Assessment_Score) FROM Suitability_Assessment
                )
            """
            df = run_query(conn, q)
            if df.empty:
                st.info("No crops found with above-average suitability scores.")
            else:
                st.dataframe(df, use_container_width=True)
                st.success(f"✅ Found {len(df)} crops with above-average suitability")
    
    elif query_option == "Weather stations with above-average rainfall":
        st.write("### Query: Stations recording above-average rainfall")
        st.code("""
SELECT ws.Station_Name, AVG(wr.Rainfall) AS Avg_Rainfall
FROM Weather_Stations ws
JOIN Weather_Readings wr ON ws.StationID = wr.StationID
GROUP BY ws.Station_Name
HAVING AVG(wr.Rainfall) > (
    SELECT AVG(Rainfall) FROM Weather_Readings
);
        """, language="sql")
        
        if st.button("Run Query", key="nested3"):
            q = """
                SELECT ws.Station_Name, AVG(wr.Rainfall) AS Avg_Rainfall
                FROM Weather_Stations ws
                JOIN Weather_Readings wr ON ws.StationID = wr.StationID
                GROUP BY ws.Station_Name
                HAVING AVG(wr.Rainfall) > (
                    SELECT AVG(Rainfall) FROM Weather_Readings
                )
            """
            df = run_query(conn, q)
            if df.empty:
                st.info("No stations found with above-average rainfall.")
            else:
                st.dataframe(df, use_container_width=True)
                st.success(f"✅ Found {len(df)} stations with above-average rainfall")
    
    st.info("✅ This demonstrates: **NESTED query** (subquery with IN/HAVING clause)")

elif choice == "⚡ Triggers Demo":
    st.subheader("⚡ Database Triggers Demonstration")
    
    st.write("### Trigger 1: `after_weather_insert` - Logs new weather readings")
    st.code("""
CREATE TRIGGER after_weather_insert
AFTER INSERT ON Weather_Readings
FOR EACH ROW
BEGIN
  INSERT INTO Weather_Log (StationID, ActionType)
  VALUES (NEW.StationID, 'New Reading Added');
END
    """, language="sql")
    
    st.write("### Trigger 2: `validate_temperature` - Validates temperature range")
    st.code("""
CREATE TRIGGER validate_temperature
BEFORE INSERT ON Weather_Readings
FOR EACH ROW
BEGIN
  IF NEW.Temperature < -10 OR NEW.Temperature > 60 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Invalid temperature value!';
  END IF;
END
    """, language="sql")
    
    st.markdown("---")
    st.write("### Test Triggers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Insert Valid Weather Reading")
        with st.form("trigger_valid"):
            rid = st.number_input("Reading ID", min_value=1, step=1, value=9999, key="trig_valid_id")
            sid = st.number_input("Station ID", min_value=1, step=1, value=401, key="trig_valid_sid")
            temp = st.number_input("Temperature (°C)", value=25.0, step=0.1, key="trig_valid_temp")
            submitted = st.form_submit_button("Insert (Triggers Log)")
        
        if submitted:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Weather_Readings (ReadingID, StationID, DateTime, Temperature, Humidity, Rainfall) VALUES (%s, %s, NOW(), %s, 50.0, 10.0)",
                    (rid, sid, temp)
                )
                conn.commit()
                cur.close()
                st.success("✅ Reading inserted! Check the log below.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        st.write("#### Try Invalid Temperature")
        with st.form("trigger_invalid"):
            rid2 = st.number_input("Reading ID", min_value=1, step=1, value=9998, key="trig_invalid_id")
            sid2 = st.number_input("Station ID", min_value=1, step=1, value=401, key="trig_invalid_sid")
            temp2 = st.number_input("Temperature (°C)", value=100.0, step=0.1, key="trig_invalid_temp")
            submitted2 = st.form_submit_button("Insert (Should Fail)")
        
        if submitted2:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Weather_Readings (ReadingID, StationID, DateTime, Temperature, Humidity, Rainfall) VALUES (%s, %s, NOW(), %s, 50.0, 10.0)",
                    (rid2, sid2, temp2)
                )
                conn.commit()
                cur.close()
                st.success("✅ Reading inserted")
            except Exception as e:
                st.error(f"❌ Trigger prevented invalid data: {e}")
    
    st.markdown("---")
    st.write("### Weather Log (Trigger Output)")
    try:
        df_log = run_query(conn, "SELECT * FROM Weather_Log ORDER BY ActionTime DESC LIMIT 20")
        if df_log.empty:
            st.info("No log entries yet. Insert a weather reading to trigger logging.")
        else:
            st.dataframe(df_log, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not fetch log: {e}")
    
    st.info("✅ This demonstrates: **TRIGGERS** with GUI (insert triggers, validation triggers, and log viewing)")

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
