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
    "➕ Add Farmer",
    "✏️ Update Data",
]
if st.session_state.role == "Admin":
    menu.append("🗑️ Delete Data")
menu += ["⚙️ Procedures & Functions", "📊 Analytics Dashboard"]

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

elif choice == "➕ Add Farmer":
    st.subheader("➕ Add New Farmer")
    with st.form("farmer_form"):
        fid = st.number_input("Farmer ID", min_value=1, step=1)
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        dob = st.date_input("Date of Birth")
        submitted = st.form_submit_button("Add Farmer")
    if submitted:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Farmers (FarmerID, Name, Phone_No, DOB) VALUES (%s, %s, %s, %s)",
            (fid, name, phone, dob)
        )
        conn.commit()
        cur.close()
        st.success(f"✅ Farmer '{name}' added")

elif choice == "✏️ Update Data":
    st.subheader("✏️ Update Weather Reading")
    rid = st.number_input("Reading ID", min_value=1, step=1)
    new_temp = st.number_input("New Temperature (°C)", step=0.1, format="%.2f")
    if st.button("Update Temperature"):
        cur = conn.cursor()
        cur.execute("UPDATE Weather_Readings SET Temperature=%s WHERE ReadingID=%s", (new_temp, rid))
        conn.commit()
        cur.close()
        st.success("🌡️ Temperature updated")

elif choice == "🗑️ Delete Data" and st.session_state.role == "Admin":
    st.subheader("🗑️ Delete Farmer (Admin only)")
    fid = st.number_input("FarmerID", min_value=1, step=1)
    if st.button("Delete Farmer"):
        cur = conn.cursor()
        cur.execute("DELETE FROM Farmers WHERE FarmerID=%s", (fid,))
        conn.commit()
        cur.close()
        st.warning(f"Farmer ID {fid} deleted")

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

# clean up
conn.close()
