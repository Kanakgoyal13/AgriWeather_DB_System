import streamlit as st
import pandas as pd
import plotly.express as px
from db_config import get_connection
from datetime import datetime

# ------------------ Page setup & theme ------------------
st.set_page_config(page_title="🌾 AgriWeather National Agricultural System", layout="wide")
st.markdown("""
<style>
/* ======== Global Background & Font ======== */
html, body, [data-testid="stAppViewContainer"], .main, .stApp {
    background-color: #f3efea !important;  /* light beige */
    color: #2d2d2d !important;  /* readable neutral dark text */
    font-family: 'Inter', sans-serif !important;
}

/* ======== Headings ======== */
h1, h2, h3, h4, h5 {
    color: #1b4332 !important;  /* dark green for emphasis */
    font-weight: 800 !important;
}
h1 {
    text-shadow: 1px 1px 2px #dce8d2;
}
p, label, span, div {
    color: #2e3b2d !important;
}

/* ======== Sidebar ======== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #edf6e5 0%, #e6f1cf 100%) !important;
    color: #1b4332 !important;
    border-right: 2px solid #c5e1a5 !important;
}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    color: #1b4332 !important;
    font-weight: 700 !important;
}
div[data-baseweb="radio"] label {
    background-color: #f5fbe9 !important;
    border-radius: 10px !important;
    padding: 8px 12px !important;
    color: #2e7d32 !important;
    border: 1px solid #c8e6c9 !important;
    margin-bottom: 6px !important;
    transition: all 0.2s ease-in-out;
}
div[data-baseweb="radio"] label:hover {
    background-color: #dcedc8 !important;
    transform: translateX(4px);
}
div[data-baseweb="radio"] input:checked + div {
    background-color: #81c784 !important;
    color: white !important;
    font-weight: 600 !important;
}

/* ======== Buttons ======== */
.stButton>button {
    background: white !important;
    color: #1b4332 !important;
    font-weight: 700 !important;
    border: 2px solid #81c784 !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
}
.stButton>button:hover {
    background: #f1f8e9 !important;
    transform: scale(1.04);
    color: #0d2600 !important;
    border-color: #66bb6a !important;
}

/* ======== Inputs & Forms ======== */
.stTextInput>div>div>input, textarea, select {
    background-color: #ffffff !important;
    color: #1b1b1b !important;
    border: 1px solid #a5d6a7 !important;
    border-radius: 8px !important;
    padding: 8px !important;
}
.stTextInput>div>div>input:focus {
    border-color: #81c784 !important;
    box-shadow: 0 0 8px #a5d6a7 !important;
}
.stForm {
    background-color: rgba(255,255,255,0.9) !important;
    border-radius: 15px !important;
    border: 1px solid #e0e0e0 !important;
    padding: 1.5rem !important;
    box-shadow: 0 0 10px rgba(0,0,0,0.05) !important;
}

/* ======== Data Tables ======== */
[data-testid="stDataFrame"] {
    background-color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #ddd !important;
    box-shadow: 0 1px 5px rgba(0,0,0,0.08) !important;
}
[data-testid="stDataFrame"] th {
    background-color: #e6f1cf !important;
    color: #1b4332 !important;
    font-weight: 700 !important;
}
[data-testid="stDataFrame"] td {
    color: #2e3b2d !important;
}

/* ======== Alerts & Messages ======== */
.stAlert {
    background-color: #fff8e1 !important;
    color: #2e3b2d !important;
    border-left: 4px solid #81c784 !important;
    border-radius: 8px !important;
}
.stSuccess {
    background-color: #f1f8e9 !important;
    border-left: 4px solid #66bb6a !important;
    color: #2e3b2d !important;
}
.stWarning {
    background-color: #fff3e0 !important;
    border-left: 4px solid #fbc02d !important;
}
.stError {
    background-color: #ffebee !important;
    border-left: 4px solid #e57373 !important;
}

/* ======== Metrics ======== */
div[data-testid="stMetricValue"] {
    color: #1b4332 !important;
    font-weight: 800 !important;
}

/* ======== Expanders ======== */
.streamlit-expanderHeader {
    background: linear-gradient(90deg, #f1f8e9, #e6f1cf) !important;
    color: #1b4332 !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
}
.streamlit-expanderHeader:hover {
    background: linear-gradient(90deg, #dcedc8, #f0f4c3) !important;
}

/* ======== Chart Background ======== */
.js-plotly-plot .plotly {
    background-color: #fdfcf8 !important;
}

/* ======== Footer ======== */
footer, .stMarkdown center {
    color: #5d4037 !important;
}
hr {
    border: 1px solid #d7ccc8 !important;
}
/* ======== FIX for SelectBox & Dropdowns ======== */
div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #1b4332 !important;
    border: 1px solid #a5d6a7 !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] * {
    background-color: #ffffff !important;
    color: #1b4332 !important;
}

div[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #c5e1a5 !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important;
}

ul[role="listbox"] {
    background-color: #fefdfb !important;
    border-radius: 8px !important;
    border: 1px solid #c5e1a5 !important;
}

li[role="option"] {
    background-color: #ffffff !important;
    color: #1b4332 !important;
    padding: 6px 10px !important;
    border-radius: 5px !important;
}
li[role="option"]:hover {
    background-color: #e8f5e9 !important;
    color: #0b2600 !important;
}
li[aria-selected="true"] {
    background-color: #c8e6c9 !important;
    color: #0b2600 !important;
    font-weight: 600 !important;
}

/* ======== FIX for Text Inputs & Date Inputs ======== */
div[data-baseweb="input"] {
    background-color: #ffffff !important;
    border: 1px solid #a5d6a7 !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
div[data-baseweb="input"]:hover {
    border-color: #81c784 !important;
}
div[data-baseweb="input"] input {
    color: #1b4332 !important;
    background-color: #ffffff !important;
}

/* ======== Calendar Popup ======== */
div[data-baseweb="calendar"] {
    background-color: #ffffff !important;
    border: 1px solid #c5e1a5 !important;
    border-radius: 10px !important;
}
div[data-baseweb="calendar"] button {
    background-color: #f0f4c3 !important;
    color: #1b4332 !important;
}
div[data-baseweb="calendar"] button:hover {
    background-color: #c5e1a5 !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------ Session bootstrap ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.farmer_id = None
    st.session_state.farmer_name = None

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
    st.title("🔐 Login to National Agriculture Management System")
    st.write("### Welcome to AgriWeather - India's Digital Agricultural Platform")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image("agriweather.jpg", use_container_width=True, caption="Empowering Indian Agriculture")
    
    with col2:
        with st.form("login_form", clear_on_submit=False):
            st.write("#### 👤 Please Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("🚪 Login", use_container_width=True)

        if submit:
            conn = get_connection()
            stop_if_no_conn(conn)
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM Users WHERE Username=%s AND Password=%s", (username, password))
            user = cur.fetchone()
            
            if user:
                st.session_state.logged_in = True
                st.session_state.role = user["Role"]
                st.session_state.username = user["Username"]
                st.session_state.farmer_id = user.get("FarmerID")
                
                # Get farmer name if this is a farmer login
                if st.session_state.farmer_id:
                    cur.execute("SELECT Name FROM Farmers WHERE FarmerID=%s", (st.session_state.farmer_id,))
                    farmer = cur.fetchone()
                    if farmer:
                        st.session_state.farmer_name = farmer["Name"]
                
                cur.close()
                conn.close()
                st.success(f"✅ Welcome {st.session_state.farmer_name or user['Username']}  •  Role: {user['Role']}")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
                cur.close()
                conn.close()
        
        st.info("**Default Credentials:**\n\n📊 Reporter: `reporter` / `reporter123`")
    
    st.stop()

# ------------------ App layout ------------------
left, right = st.columns([7, 1])
with left:
    if st.session_state.role == "Reporter":
        st.title("📊 National Agriculture Management System")
        st.write("Reporter Dashboard - Managing National Agricultural Data")
    else:
        st.title(f"🌾 Welcome, {st.session_state.farmer_name}!")
        st.write("Your Personal Agricultural Assistant")

with right:
    role_icon = "📊" if st.session_state.role == "Reporter" else "👨‍🌾"
    st.caption(f"{role_icon} **{st.session_state.farmer_name or st.session_state.username}**")
    st.caption(f"*{st.session_state.role}*")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.farmer_id = None
        st.session_state.farmer_name = None
        st.rerun()

# Single shared connection
conn = get_connection()
stop_if_no_conn(conn)

# ------------------ Role-Based Menu ------------------
if st.session_state.role == "Reporter":
    menu = [
        "🏠 National Dashboard",
        "👨‍🌾 Farmer Registry",
        "🌾 Farm Registry",
        "🌱 Crop & Season Management",
        "🌤️ Weather Stations",
        "📊 National Analytics",
        "🏆 National Leaderboard",
        "⚙️ Weather Insights",
    ]
else:  # Farmer
    menu = [
        "🏠 My Dashboard",
        "🌾 My Farms",
        "🌱 My Cultivation",
        "📅 Plan Cultivation",
        "🌤️ Weather Info",
        "📈 My Performance",
        "💡 Recommendations",
        "👤 My Profile",
    ]

choice = st.sidebar.radio("Navigate", menu)

# ==================== REPORTER PAGES ====================
if st.session_state.role == "Reporter":
    
    if choice == "🏠 National Dashboard":
        st.subheader("📊 National Overview")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            farmer_count_df = run_query(conn, "SELECT COUNT(*) as count FROM Farmers")
            farmer_count = farmer_count_df.iloc[0]['count'] if not farmer_count_df.empty else 0
            st.metric("👨‍🌾 Total Farmers", farmer_count)
        
        with col2:
            farm_area_df = run_query(conn, "SELECT SUM(Area_acres) as total FROM Farms")
            total_area = farm_area_df.iloc[0]['total'] if not farm_area_df.empty and farm_area_df.iloc[0]['total'] else 0
            st.metric("🌾 Total Farm Area", f"{total_area:.1f} acres")
        
        with col3:
            # Count pending farm requests (we'll create this table)
            try:
                pending_df = run_query(conn, "SELECT COUNT(*) as count FROM Farm_Requests WHERE Status='Pending'")
                pending_count = pending_df.iloc[0]['count'] if not pending_df.empty else 0
            except:
                pending_count = 0
            st.metric("⏳ Pending Requests", pending_count)
        
        with col4:
            season_df = run_query(conn, "SELECT COUNT(*) as count FROM Crop_Seasons WHERE CURDATE() BETWEEN Start_Date AND End_Date")
            active_seasons = season_df.iloc[0]['count'] if not season_df.empty else 0
            st.metric("📅 Active Seasons", active_seasons)
        
        st.markdown("---")
        
        # Pending Farm Requests Section
        st.write("### ⏳ Pending Farm Registration Requests")
        try:
            # Create Farm_Requests table if it doesn't exist
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS Farm_Requests (
                    RequestID INT AUTO_INCREMENT PRIMARY KEY,
                    FarmerID INT NOT NULL,
                    Farm_Name VARCHAR(100),
                    Area_acres DECIMAL(10,2),
                    Status VARCHAR(20) DEFAULT 'Pending',
                    Request_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (FarmerID) REFERENCES Farmers(FarmerID) ON DELETE CASCADE
                )
            """)
            conn.commit()
            cur.close()
            
            pending_requests = run_query(conn, """
                SELECT fr.RequestID, f.Name as Farmer_Name, fr.Farm_Name, fr.Area_acres, fr.Request_Date
                FROM Farm_Requests fr
                JOIN Farmers f ON fr.FarmerID = f.FarmerID
                WHERE fr.Status = 'Pending'
                ORDER BY fr.Request_Date DESC
            """)
            
            if pending_requests.empty:
                st.info("✅ No pending farm registration requests")
            else:
                st.dataframe(pending_requests, use_container_width=True)
                
                # Approval form
                with st.form("approve_farm"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        request_id = st.number_input("Request ID to Process", min_value=1, step=1)
                    with col_b:
                        action = st.selectbox("Action", ["Approve", "Reject"])
                    
                    submitted = st.form_submit_button("Process Request")
                    
                    if submitted:
                        try:
                            cur = conn.cursor()
                            # Get request details
                            cur.execute("SELECT * FROM Farm_Requests WHERE RequestID=%s", (request_id,))
                            request = cur.fetchone()
                            
                            if request and action == "Approve":
                                # Get next FarmSeq
                                cur.execute("SELECT COALESCE(MAX(FarmSeq), 0) + 1 as next_seq FROM Farms")
                                next_seq = cur.fetchone()[0]
                                
                                # Insert into Farms
                                cur.execute(
                                    "INSERT INTO Farms (FarmSeq, Farm_Name, Area_acres, FarmerID) VALUES (%s, %s, %s, %s)",
                                    (next_seq, request[2], request[3], request[1])
                                )
                                # Update request status
                                cur.execute("UPDATE Farm_Requests SET Status='Approved' WHERE RequestID=%s", (request_id,))
                                conn.commit()
                                st.success(f"✅ Farm '{request[2]}' approved and added to registry!")
                                st.rerun()
                            elif request and action == "Reject":
                                cur.execute("UPDATE Farm_Requests SET Status='Rejected' WHERE RequestID=%s", (request_id,))
                                conn.commit()
                                st.warning(f"❌ Request {request_id} rejected")
                                st.rerun()
                            else:
                                st.error("Request not found")
                            
                            cur.close()
                        except Exception as e:
                            st.error(f"Error: {e}")
        except Exception as e:
            st.warning(f"Farm requests feature initializing... {e}")
        
        st.markdown("---")
        
        # Recent Activities
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.write("### 📋 Recent Farmer Registrations")
            recent_farmers = run_query(conn, "SELECT FarmerID, Name, Phone_No FROM Farmers ORDER BY FarmerID DESC LIMIT 5")
            if not recent_farmers.empty:
                st.dataframe(recent_farmers, use_container_width=True, hide_index=True)
            else:
                st.info("No farmers registered yet")
        
        with col_right:
            st.write("### 🌾 Recent Farm Additions")
            recent_farms = run_query(conn, """
                SELECT f.FarmSeq, f.Farm_Name, f.Area_acres, fa.Name as Farmer_Name
                FROM Farms f
                JOIN Farmers fa ON f.FarmerID = fa.FarmerID
                ORDER BY f.FarmSeq DESC
                LIMIT 5
            """)
            if not recent_farms.empty:
                st.dataframe(recent_farms, use_container_width=True, hide_index=True)
            else:
                st.info("No farms registered yet")
    
    elif choice == "👨‍🌾 Farmer Registry":
        st.subheader("👨‍🌾 Farmer Registry Management")
        
        tab1, tab2, tab3 = st.tabs(["📋 View All Farmers", "➕ Register New Farmer", "✏️ Update Farmer"])
        
        with tab1:
            st.write("### All Registered Farmers")
            farmers_df = run_query(conn, "SELECT * FROM Farmers ORDER BY FarmerID")
            st.dataframe(farmers_df, use_container_width=True)
            st.caption(f"Total Farmers: {len(farmers_df)}")
        
        with tab2:
            st.write("### Register New Farmer")
            st.info("💡 A user account will be automatically created for the farmer to access the system")
            
            with st.form("register_farmer"):
                col1, col2 = st.columns(2)
                with col1:
                    farmer_id = st.number_input("Farmer ID", min_value=1, step=1)
                    name = st.text_input("Full Name")
                    phone = st.text_input("Phone Number")
                with col2:
                    dob = st.date_input("Date of Birth")
                    username = st.text_input("Username for System Access", help="This will be used for login")
                    password = st.text_input("Initial Password", type="password", value="farmer123")
                
                submitted = st.form_submit_button("Register Farmer & Create Account")
                
                if submitted:
                    try:
                        cur = conn.cursor()
                        # Insert farmer
                        cur.execute(
                            "INSERT INTO Farmers (FarmerID, Name, Phone_No, DOB) VALUES (%s, %s, %s, %s)",
                            (farmer_id, name, phone, dob)
                        )
                        # Create user account
                        cur.execute(
                            "INSERT INTO Users (Username, Password, Role, FarmerID) VALUES (%s, %s, %s, %s)",
                            (username, password, 'Farmer', farmer_id)
                        )
                        conn.commit()
                        cur.close()
                        st.success(f"✅ Farmer '{name}' registered successfully!")
                        st.success(f"🔐 User account created - Username: {username}, Password: {password}")
                        st.info("👉 The farmer can now login and manage their farms")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        with tab3:
            st.write("### Update Farmer Information")
            with st.form("update_farmer"):
                fid = st.number_input("Farmer ID", min_value=1, step=1)
                new_name = st.text_input("Name")
                new_phone = st.text_input("Phone Number")
                new_dob = st.date_input("Date of Birth")
                submitted = st.form_submit_button("Update Farmer")
                
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute("UPDATE Farmers SET Name=%s, Phone_No=%s, DOB=%s WHERE FarmerID=%s", 
                                   (new_name, new_phone, new_dob, fid))
                        conn.commit()
                        cur.close()
                        st.success("✅ Farmer information updated")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        # Add Delete Tab
        st.markdown("---")
        st.write("### 🗑️ Delete Farmer")
        st.warning("⚠️ Warning: Deleting a farmer will also delete all their farms, cultivations, and user account!")
        
        with st.form("delete_farmer"):
            del_farmer_id = st.number_input("Farmer ID to Delete", min_value=1, step=1, key="del_farmer")
            confirm_delete = st.checkbox("I understand this will delete all related data (farms, cultivations, user account)")
            submitted_delete = st.form_submit_button("🗑️ Delete Farmer")
            
            if submitted_delete:
                if not confirm_delete:
                    st.error("❌ Please confirm deletion by checking the box")
                else:
                    try:
                        cur = conn.cursor()
                        # Check if farmer exists
                        cur.execute("SELECT Name FROM Farmers WHERE FarmerID=%s", (del_farmer_id,))
                        farmer = cur.fetchone()
                        if farmer:
                            # Delete in proper order to handle foreign key constraints
                            # 1. Delete cultivations (references farms)
                            cur.execute("DELETE FROM Cultivates WHERE FarmSeq IN (SELECT FarmSeq FROM Farms WHERE FarmerID=%s)", (del_farmer_id,))
                            # 2. Delete farm requests
                            cur.execute("DELETE FROM Farm_Requests WHERE FarmerID=%s", (del_farmer_id,))
                            # 3. Delete farms (references farmer)
                            cur.execute("DELETE FROM Farms WHERE FarmerID=%s", (del_farmer_id,))
                            # 4. Delete user account (references farmer)
                            cur.execute("DELETE FROM Users WHERE FarmerID=%s", (del_farmer_id,))
                            # 5. Delete farmer
                            cur.execute("DELETE FROM Farmers WHERE FarmerID=%s", (del_farmer_id,))
                            conn.commit()
                            st.success(f"✅ Farmer '{farmer[0]}' and all related data deleted successfully")
                            st.rerun()
                        else:
                            st.error(f"❌ No farmer found with ID {del_farmer_id}")
                        cur.close()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    elif choice == "🌾 Farm Registry":
        st.subheader("🌾 Farm Registry Management")
        
        tab1, tab2, tab3 = st.tabs(["📋 View All Farms", "➕ Add New Farm", "🗑️ Delete Farm"])
        
        with tab1:
            farms_df = run_query(conn, """
                SELECT f.FarmSeq, f.Farm_Name, f.Area_acres, fa.Name as Farmer_Name, fa.FarmerID
                FROM Farms f
                JOIN Farmers fa ON f.FarmerID = fa.FarmerID
                ORDER BY f.FarmSeq
            """)
            st.dataframe(farms_df, use_container_width=True)
            st.caption(f"Total Farms: {len(farms_df)}")
        
        with tab2:
            st.write("### Add New Farm to Registry")
            
            # Get list of farmers for dropdown
            farmers_list = run_query(conn, "SELECT FarmerID, Name FROM Farmers ORDER BY Name")
            
            if farmers_list.empty:
                st.warning("⚠️ Please register farmers first before adding farms")
            else:
                with st.form("add_farm"):
                    farm_seq = st.number_input("Farm Sequence ID", min_value=1, step=1)
                    farm_name = st.text_input("Farm Name")
                    area = st.number_input("Area (acres)", min_value=0.0, step=0.1, format="%.2f")
                    
                    # Dropdown for farmer selection
                    farmer_options = [f"{row['FarmerID']} - {row['Name']}" for _, row in farmers_list.iterrows()]
                    selected_farmer = st.selectbox("Select Farmer", farmer_options)
                    farmer_id = int(selected_farmer.split(" - ")[0])
                    
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
                            st.success(f"✅ Farm '{farm_name}' added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
        
        with tab3:
            st.write("### 🗑️ Delete Farm")
            st.warning("⚠️ Warning: Deleting a farm will also delete all cultivation records for this farm!")
            
            with st.form("delete_farm"):
                del_farm_seq = st.number_input("Farm Sequence ID to Delete", min_value=1, step=1, key="del_farm")
                confirm_delete = st.checkbox("I understand this will delete all related cultivation data")
                submitted_delete = st.form_submit_button("🗑️ Delete Farm")
                
                if submitted_delete:
                    if not confirm_delete:
                        st.error("❌ Please confirm deletion by checking the box")
                    else:
                        try:
                            cur = conn.cursor()
                            # Check if farm exists
                            cur.execute("SELECT Farm_Name FROM Farms WHERE FarmSeq=%s", (del_farm_seq,))
                            farm = cur.fetchone()
                            if farm:
                                # Delete farm (cascade will handle related records)
                                cur.execute("DELETE FROM Farms WHERE FarmSeq=%s", (del_farm_seq,))
                                conn.commit()
                                st.success(f"✅ Farm '{farm[0]}' and all related data deleted successfully")
                                st.rerun()
                            else:
                                st.error(f"❌ No farm found with ID {del_farm_seq}")
                            cur.close()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
    
    elif choice == "🌱 Crop & Season Management":
        st.subheader("🌱 Crop & Season Management")
        
        tab1, tab2, tab3 = st.tabs(["🌾 Crops", "🌿 Cultivation Records", "📊 Sustainability"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write("### Available Crops")
                crops_df = run_query(conn, "SELECT * FROM Crops ORDER BY CropID")
                st.dataframe(crops_df, use_container_width=True)
            
            with col2:
                st.write("### Add New Crop")
                with st.form("add_crop"):
                    crop_id = st.number_input("Crop ID", min_value=1, step=1)
                    crop_name = st.text_input("Crop Name")
                    submitted = st.form_submit_button("Add Crop")
                    
                    if submitted:
                        try:
                            cur = conn.cursor()
                            cur.execute("INSERT INTO Crops (CropID, Crop_Name) VALUES (%s, %s)", (crop_id, crop_name))
                            conn.commit()
                            cur.close()
                            st.success(f"✅ Crop '{crop_name}' added")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
        
        with tab2:
            st.write("### All Cultivation Records")
            cultivation_df = run_query(conn, """
                SELECT c.FarmSeq, f.Farm_Name, fa.Name as Farmer_Name, 
                       cr.Crop_Name, cs.Season_Name
                FROM Cultivates c
                JOIN Farms f ON c.FarmSeq = f.FarmSeq
                JOIN Farmers fa ON f.FarmerID = fa.FarmerID
                JOIN Crops cr ON c.CropID = cr.CropID
                JOIN Crop_Seasons cs ON c.SeasonID = cs.SeasonID
                ORDER BY fa.Name, f.Farm_Name
            """)
            st.dataframe(cultivation_df, use_container_width=True)
            st.caption(f"Total Cultivation Records: {len(cultivation_df)}")
        
        with tab3:
            st.write("### Crop Sustainability Assessments")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                suitability_df = run_query(conn, """
                    SELECT c.Crop_Name, cs.Season_Name, ws.Station_Name, sa.Assessment_Score
                    FROM Suitability_Assessment sa
                    JOIN Crops c ON sa.CropID = c.CropID
                    JOIN Crop_Seasons cs ON sa.SeasonID = cs.SeasonID
                    JOIN Weather_Stations ws ON sa.StationID = ws.StationID
                    ORDER BY sa.Assessment_Score DESC
                """)
                st.dataframe(suitability_df, use_container_width=True)
            
            with col2:
                st.write("#### Add Assessment")
                with st.form("add_suitability"):
                    season_id = st.number_input("Season ID", min_value=1, step=1)
                    station_id = st.number_input("Station ID", min_value=1, step=1)
                    crop_id = st.number_input("Crop ID", min_value=1, step=1)
                    score = st.number_input("Score (0-10)", min_value=0.0, max_value=10.0, step=0.1)
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
                            st.success("✅ Assessment added")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
    
    elif choice == "🌤️ Weather Stations":
        st.subheader("🌤️ Weather Station Management")
        
        tab1, tab2, tab3 = st.tabs(["📍 Stations", "📊 Weather Readings", "➕ Add Reading"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            with col1:
                stations_df = run_query(conn, "SELECT * FROM Weather_Stations ORDER BY StationID")
                st.dataframe(stations_df, use_container_width=True)
            
            with col2:
                st.write("### Add New Station")
                with st.form("add_station"):
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
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
        
        with tab2:
            st.write("### Recent Weather Readings")
            readings_df = run_query(conn, """
                SELECT wr.ReadingID, ws.Station_Name, wr.DateTime, wr.Temperature, wr.Humidity, wr.Rainfall
                FROM Weather_Readings wr
                JOIN Weather_Stations ws ON wr.StationID = ws.StationID
                ORDER BY wr.DateTime DESC
                LIMIT 50
            """)
            st.dataframe(readings_df, use_container_width=True)
        
        with tab3:
            st.write("### Add New Weather Reading")
            with st.form("add_reading"):
                reading_id = st.number_input("Reading ID", min_value=1, step=1)
                station_id = st.number_input("Station ID", min_value=1, step=1)
                datetime_val = st.text_input("DateTime (YYYY-MM-DD HH:MM:SS)", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                st.error("⚠️ Temperature must be between -10°C and 60°C")
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
                        st.success(f"✅ Weather Reading added")
                        st.rerun()
                    except Exception as e:
                        if "Invalid temperature value" in str(e):
                            st.error("🚫 Trigger Validation Failed: Temperature must be between -10°C and 60°C!")
                        else:
                            st.error(f"❌ Error: {e}")
    
    elif choice == "📊 National Analytics":
        st.subheader("📊 National Analytics Dashboard")
        
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

            st.markdown("### 📈 Insights")
            st.write("- Use rainfall & temperature averages to guide crop-season sustainability recommendations")
            st.write("- Monsoon states show higher rainfall; ideal for rice, sugarcane, etc.")
    
    elif choice == "🏆 National Leaderboard":
        st.subheader("🏆 National Leaderboard & Rankings")
        st.write("Discover top performers based on various metrics")
        
        search_category = st.selectbox("What would you like to search for?", [
            "🌾 High-Performing Farmers",
            "🌱 Best Crops for Cultivation",
            "🌧️ High Rainfall Stations"
        ])
        
        if search_category == "🌾 High-Performing Farmers":
            st.write("### Find Farmers with Large Farms")
            
            avg_query = "SELECT AVG(Area_acres) AS avg_area FROM Farms"
            avg_df = run_query(conn, avg_query)
            if not avg_df.empty:
                avg_area = avg_df.iloc[0]['avg_area']
                st.metric("Average Farm Size", f"{avg_area:.2f} acres")
            
            if st.button("🔍 Search for High-Performing Farmers"):
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
                    
                    if len(df) > 0:
                        fig = px.bar(df, x="Name", y="Area_acres", title="Farm Sizes (Above Average)", 
                                    color="Area_acres", labels={"Area_acres": "Area (acres)"})
                        st.plotly_chart(fig, use_container_width=True)
        
        elif search_category == "🌱 Best Crops for Cultivation":
            st.write("### Find Top-Rated Crops")
            
            avg_query = "SELECT AVG(Assessment_Score) AS avg_score FROM Suitability_Assessment"
            avg_df = run_query(conn, avg_query)
            if not avg_df.empty:
                avg_score = avg_df.iloc[0]['avg_score']
                st.metric("Average Sustainability Score", f"{avg_score:.2f} / 10")
            
            if st.button("🔍 Search for Best Crops"):
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
                    st.info("No crops found with above-average sustainability scores.")
                else:
                    st.success(f"✅ Found {len(df)} crops with above-average sustainability")
                    st.dataframe(df, use_container_width=True)
                    
                    if len(df) > 0:
                        fig = px.bar(df, x="Crop_Name", y="Avg_Score", title="Top-Rated Crops", 
                                    color="Avg_Score", labels={"Avg_Score": "Sustainability Score"})
                        st.plotly_chart(fig, use_container_width=True)
        
        elif search_category == "🌧️ High Rainfall Stations":
            st.write("### Find Stations with High Rainfall")
            
            avg_query = "SELECT AVG(Rainfall) AS avg_rainfall FROM Weather_Readings"
            avg_df = run_query(conn, avg_query)
            if not avg_df.empty:
                avg_rainfall = avg_df.iloc[0]['avg_rainfall']
                st.metric("Average Rainfall", f"{avg_rainfall:.2f} mm")
            
            if st.button("🔍 Search for High Rainfall Stations"):
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
                    
                    if len(df) > 0:
                        fig = px.bar(df, x="Station_Name", y="Avg_Rainfall", title="High Rainfall Stations", 
                                    color="Avg_Rainfall", labels={"Avg_Rainfall": "Avg Rainfall (mm)"})
                        st.plotly_chart(fig, use_container_width=True)
    
    elif choice == "⚙️ Weather Insights":
        st.subheader("⚙️ Weather Data Analysis")
        
        with st.expander("🌦 Get Weather Data by Station"):
            st.write("Retrieve detailed readings and compute average temperature for a specific weather station.")
            station_id = st.text_input("Enter Station ID", key="proc_station_id")
            
            if st.button("Get Weather Data", key="btn_proc_weather"):
                if station_id.strip() == "":
                    st.warning("Please enter a valid Station ID.")
                else:
                    try:
                        cur = conn.cursor()
                        cur.callproc("GetWeatherByStation", [station_id])
                        for result in cur.stored_results():
                            data = result.fetchall()
                            if data:
                                df = pd.DataFrame(data, columns=["StationID", "DateTime", "Temperature", "Humidity", "Rainfall"])
                                st.success(f"✅ Weather readings for Station {station_id}")
                                st.dataframe(df, use_container_width=True)
                            else:
                                st.info(f"No readings found for Station {station_id}")
                        
                        avg_query = "SELECT AvgTemperature(%s) AS AvgTemp"
                        cur.execute(avg_query, (station_id,))
                        avg_result = cur.fetchone()
                        
                        if avg_result and avg_result[0] is not None:
                            avg_temp = round(avg_result[0], 2)
                            st.markdown(f"<h4 style='color:#76c893;'>🌡 Average Temperature: <b>{avg_temp} °C</b></h4>", unsafe_allow_html=True)
                        else:
                            st.info("No average temperature data found for this station.")
                        
                        cur.close()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        with st.expander("🌾 Get Crop Sustainability"):
            st.write("View sustainability results for a specific crop by name.")
            crop_name = st.text_input("Enter Crop Name (e.g., Wheat)", key="proc_crop_name")
            
            if st.button("Get Sustainability Data", key="btn_proc_sustainability"):
                if crop_name.strip() == "":
                    st.warning("Please enter a crop name.")
                else:
                    try:
                        cur = conn.cursor()
                        cur.callproc("GetSuitability", [crop_name])
                        for result in cur.stored_results():
                            data = result.fetchall()
                            if data:
                                df = pd.DataFrame(data, columns=["Crop_Name", "Season_Name", "Assessment_Score"])
                                st.success(f"✅ Sustainability results for {crop_name}")
                                st.dataframe(df, use_container_width=True)
                            else:
                                st.info(f"No sustainability data found for crop '{crop_name}'")
                        cur.close()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
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

# ==================== FARMER PAGES ====================
else:  # Farmer role
    
    if choice == "🏠 My Dashboard":
        st.subheader(f"Welcome back, {st.session_state.farmer_name}! 👨‍🌾")
        
        # Personal metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            my_farms_df = run_query(conn, "SELECT COUNT(*) as count FROM Farms WHERE FarmerID=%s", (st.session_state.farmer_id,))
            my_farms_count = my_farms_df.iloc[0]['count'] if not my_farms_df.empty else 0
            st.metric("🌾 My Farms", my_farms_count)
        
        with col2:
            my_area_df = run_query(conn, "SELECT SUM(Area_acres) as total FROM Farms WHERE FarmerID=%s", (st.session_state.farmer_id,))
            my_area = my_area_df.iloc[0]['total'] if not my_area_df.empty and my_area_df.iloc[0]['total'] else 0
            st.metric("📏 Total Area", f"{my_area:.1f} acres")
        
        with col3:
            my_crops_df = run_query(conn, """
                SELECT COUNT(DISTINCT c.CropID) as count 
                FROM Cultivates c
                JOIN Farms f ON c.FarmSeq = f.FarmSeq
                WHERE f.FarmerID=%s
            """, (st.session_state.farmer_id,))
            my_crops = my_crops_df.iloc[0]['count'] if not my_crops_df.empty else 0
            st.metric("🌱 Crops Growing", my_crops)
        
        st.markdown("---")
        
        # Top 3 Recommended Crops
        st.write("### 🌟 Top 3 Recommended Crops for Current Season")
        
        # Get current season
        current_season = run_query(conn, """
            SELECT SeasonID, Season_Name 
            FROM Crop_Seasons 
            WHERE CURDATE() BETWEEN Start_Date AND End_Date
            LIMIT 1
        """)
        
        if not current_season.empty:
            season_id = int(current_season.iloc[0]['SeasonID'])
            season_name = current_season.iloc[0]['Season_Name']
            
            # Get top 3 crops for current season
            top_crops = run_query(conn, """
                SELECT c.Crop_Name, AVG(sa.Assessment_Score) as Avg_Score
                FROM Suitability_Assessment sa
                JOIN Crops c ON sa.CropID = c.CropID
                WHERE sa.SeasonID=%s
                GROUP BY c.Crop_Name
                ORDER BY Avg_Score DESC
                LIMIT 3
            """, (season_id,))
            
            if not top_crops.empty:
                st.info(f"📅 Current Season: **{season_name}**")
                cols = st.columns(3)
                for idx, (_, crop) in enumerate(top_crops.iterrows()):
                    with cols[idx]:
                        rank_emoji = ["🥇", "🥈", "🥉"][idx]
                        score = crop['Avg_Score']
                        
                        if score >= 8:
                            color = "#2e7d32"
                        elif score >= 6:
                            color = "#558b2f"
                        else:
                            color = "#827717"
                        
                        st.markdown(f"""
                        <div style="background-color: {color}; padding: 15px; border-radius: 10px; text-align: center; color: white;">
                            <h3>{rank_emoji}</h3>
                            <h4>{crop['Crop_Name']}</h4>
                            <h2>{score:.1f}/10</h2>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No crop recommendations available for the current season")
        else:
            st.warning("No active season found")
        
        st.markdown("---")
        
        # Quick Overview
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.write("### 🌾 My Farms Overview")
            my_farms = run_query(conn, """
                SELECT FarmSeq, Farm_Name, Area_acres 
                FROM Farms 
                WHERE FarmerID=%s
                ORDER BY FarmSeq
            """, (st.session_state.farmer_id,))
            
            if not my_farms.empty:
                st.dataframe(my_farms, use_container_width=True, hide_index=True)
            else:
                st.info("You haven't registered any farms yet. Request farm registration in 'My Farms' section.")
        
        with col_right:
            st.write("### 🌡️ Current Weather Conditions")
            latest_weather = run_query(conn, """
                SELECT ws.Station_Name, wr.Temperature, wr.Humidity, wr.Rainfall, wr.DateTime
                FROM Weather_Readings wr
                JOIN Weather_Stations ws ON wr.StationID = ws.StationID
                ORDER BY wr.DateTime DESC
                LIMIT 1
            """)
            
            if not latest_weather.empty:
                w = latest_weather.iloc[0]
                st.success(f"📍 **{w['Station_Name']}** - {w['DateTime']}")
                c1, c2, c3 = st.columns(3)
                c1.metric("🌡️ Temp", f"{w['Temperature']:.1f}°C")
                c2.metric("💧 Humidity", f"{w['Humidity']:.0f}%")
                c3.metric("🌧️ Rainfall", f"{w['Rainfall']:.1f}mm")
            else:
                st.info("No weather data available")
        
        st.markdown("---")
        st.write("### 🌱 Current Cultivation")
        my_cultivation = run_query(conn, """
            SELECT f.Farm_Name, c.Crop_Name, cs.Season_Name
            FROM Cultivates cult
            JOIN Farms f ON cult.FarmSeq = f.FarmSeq
            JOIN Crops c ON cult.CropID = c.CropID
            JOIN Crop_Seasons cs ON cult.SeasonID = cs.SeasonID
            WHERE f.FarmerID=%s
            ORDER BY f.Farm_Name
        """, (st.session_state.farmer_id,))
        
        if not my_cultivation.empty:
            st.dataframe(my_cultivation, use_container_width=True, hide_index=True)
        else:
            st.info("No active cultivation records. Plan your cultivation in 'Plan Cultivation' section.")
    
    elif choice == "🌾 My Farms":
        st.subheader("🌾 My Farms")
        
        tab1, tab2 = st.tabs(["📋 View My Farms", "➕ Request New Farm"])
        
        with tab1:
            my_farms = run_query(conn, """
                SELECT FarmSeq, Farm_Name, Area_acres 
                FROM Farms 
                WHERE FarmerID=%s
                ORDER BY FarmSeq
            """, (st.session_state.farmer_id,))
            
            if not my_farms.empty:
                st.dataframe(my_farms, use_container_width=True)
                st.caption(f"You own {len(my_farms)} farm(s)")
                
                # Show detailed view for each farm
                st.write("### Farm Details")
                for _, farm in my_farms.iterrows():
                    with st.expander(f"🌾 {farm['Farm_Name']} ({farm['Area_acres']} acres)"):
                        # Show crops on this farm
                        crops_on_farm = run_query(conn, """
                            SELECT c.Crop_Name, cs.Season_Name
                            FROM Cultivates cult
                            JOIN Crops c ON cult.CropID = c.CropID
                            JOIN Crop_Seasons cs ON cult.SeasonID = cs.SeasonID
                            WHERE cult.FarmSeq=%s
                        """, (farm['FarmSeq'],))
                        
                        if not crops_on_farm.empty:
                            st.write("**Crops Currently Growing:**")
                            st.dataframe(crops_on_farm, use_container_width=True, hide_index=True)
                        else:
                            st.info("No crops currently planted on this farm")
            else:
                st.info("You don't have any registered farms yet. Request a new farm below.")
        
        with tab2:
            st.write("### Request New Farm Registration")
            st.info("💡 Your request will be sent to the Reporter for approval")
            
            with st.form("request_farm"):
                farm_name = st.text_input("Farm Name")
                area = st.number_input("Area (acres)", min_value=0.0, step=0.1, format="%.2f")
                submitted = st.form_submit_button("Submit Request")
                
                if submitted:
                    try:
                        cur = conn.cursor()
                        cur.execute(
                            "INSERT INTO Farm_Requests (FarmerID, Farm_Name, Area_acres, Status) VALUES (%s, %s, %s, 'Pending')",
                            (st.session_state.farmer_id, farm_name, area)
                        )
                        conn.commit()
                        cur.close()
                        st.success(f"✅ Farm registration request submitted for '{farm_name}'")
                        st.info("⏳ Waiting for Reporter approval...")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            # Show pending requests
            st.write("### My Pending Requests")
            pending = run_query(conn, """
                SELECT RequestID, Farm_Name, Area_acres, Status, Request_Date
                FROM Farm_Requests
                WHERE FarmerID=%s AND Status='Pending'
                ORDER BY Request_Date DESC
            """, (st.session_state.farmer_id,))
            
            if not pending.empty:
                st.dataframe(pending, use_container_width=True)
            else:
                st.info("No pending requests")
    
    elif choice == "🌱 My Cultivation":
        st.subheader("🌱 My Cultivation Records")
        
        my_cultivation = run_query(conn, """
            SELECT f.FarmSeq, f.Farm_Name, c.Crop_Name, cs.Season_Name, sa.Assessment_Score
            FROM Cultivates cult
            JOIN Farms f ON cult.FarmSeq = f.FarmSeq
            JOIN Crops c ON cult.CropID = c.CropID
            JOIN Crop_Seasons cs ON cult.SeasonID = cs.SeasonID
            LEFT JOIN Suitability_Assessment sa ON 
                sa.CropID = cult.CropID AND sa.SeasonID = cult.SeasonID
            WHERE f.FarmerID=%s
            ORDER BY f.Farm_Name, cs.Season_Name
        """, (st.session_state.farmer_id,))
        
        if not my_cultivation.empty:
            st.dataframe(my_cultivation, use_container_width=True)
            st.caption(f"Total cultivation records: {len(my_cultivation)}")
            
            # Visualize crop diversity
            if len(my_cultivation) > 0:
                st.write("### 📊 Your Crop Diversity")
                crop_counts = my_cultivation['Crop_Name'].value_counts()
                fig = px.pie(values=crop_counts.values, names=crop_counts.index, 
                            title="Crops Distribution Across Your Farms")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No cultivation records yet. Start planning in 'Plan Cultivation' section!")
    
    elif choice == "📅 Plan Cultivation":
        st.subheader("📅 Plan Your Cultivation")
        st.write("Register what you're planning to grow this season")
        
        # Get farmer's farms
        my_farms = run_query(conn, "SELECT FarmSeq, Farm_Name FROM Farms WHERE FarmerID=%s", (st.session_state.farmer_id,))
        
        if my_farms.empty:
            st.warning("⚠️ You need to have at least one registered farm before planning cultivation.")
            st.info("Request a new farm in 'My Farms' section")
        else:
            # Get available crops and seasons
            crops_df = run_query(conn, "SELECT CropID, Crop_Name FROM Crops ORDER BY Crop_Name")
            seasons_df = run_query(conn, "SELECT SeasonID, Season_Name FROM Crop_Seasons ORDER BY SeasonID")
            
            with st.form("plan_cultivation"):
                st.write("### Select Your Plan")
                
                # Farm selection
                farm_options = [f"{row['FarmSeq']} - {row['Farm_Name']}" for _, row in my_farms.iterrows()]
                selected_farm = st.selectbox("Select Your Farm", farm_options)
                farm_seq = int(selected_farm.split(" - ")[0])
                
                # Crop selection
                crop_options = [f"{row['CropID']} - {row['Crop_Name']}" for _, row in crops_df.iterrows()]
                selected_crop = st.selectbox("Select Crop", crop_options)
                crop_id = int(selected_crop.split(" - ")[0])
                
                # Season selection
                season_options = [f"{row['SeasonID']} - {row['Season_Name']}" for _, row in seasons_df.iterrows()]
                selected_season = st.selectbox("Select Season", season_options)
                season_id = int(selected_season.split(" - ")[0])
                
                # Show sustainability score if available
                sustainability = run_query(conn, """
                    SELECT Assessment_Score 
                    FROM Suitability_Assessment 
                    WHERE CropID=%s AND SeasonID=%s
                    LIMIT 1
                """, (crop_id, season_id))
                
                if not sustainability.empty:
                    score = sustainability.iloc[0]['Assessment_Score']
                    if score >= 7:
                        st.success(f"🌟 Sustainability Score: {score}/10 - Excellent choice!")
                    elif score >= 5:
                        st.info(f"⭐ Sustainability Score: {score}/10 - Good choice")
                    else:
                        st.warning(f"⚠️ Sustainability Score: {score}/10 - Consider alternatives")
                else:
                    st.info("No sustainability data available for this combination")
                
                submitted = st.form_submit_button("Register Cultivation Plan")
                
                if submitted:
                    try:
                        cur = conn.cursor()
                        # Check if already exists
                        cur.execute(
                            "SELECT COUNT(*) FROM Cultivates WHERE FarmSeq=%s AND CropID=%s AND SeasonID=%s",
                            (farm_seq, crop_id, season_id)
                        )
                        exists = cur.fetchone()[0]
                        
                        if exists > 0:
                            st.warning("⚠️ This cultivation plan already exists")
                        else:
                            cur.execute(
                                "INSERT INTO Cultivates (FarmSeq, CropID, SeasonID) VALUES (%s, %s, %s)",
                                (farm_seq, crop_id, season_id)
                            )
                            conn.commit()
                            st.success("✅ Cultivation plan registered successfully!")
                            st.balloons()
                        
                        cur.close()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    elif choice == "🌤️ Weather Info":
        st.subheader("🌤️ Weather Information")
        
        tab1, tab2 = st.tabs(["📊 Recent Readings", "🔍 Search by Station"])
        
        with tab1:
            st.write("### Recent Weather Readings")
            recent_weather = run_query(conn, """
                SELECT ws.Station_Name, wr.DateTime, wr.Temperature, wr.Humidity, wr.Rainfall
                FROM Weather_Readings wr
                JOIN Weather_Stations ws ON wr.StationID = ws.StationID
                ORDER BY wr.DateTime DESC
                LIMIT 20
            """)
            
            if not recent_weather.empty:
                st.dataframe(recent_weather, use_container_width=True)
                
                # Show trend chart
                st.write("### 📈 Temperature Trend (Last 20 readings)")
                fig = px.line(recent_weather, x="DateTime", y="Temperature", 
                             title="Temperature Over Time", markers=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No weather data available")
        
        with tab2:
            st.write("### Search Weather by Station")
            
            stations = run_query(conn, "SELECT StationID, Station_Name FROM Weather_Stations ORDER BY Station_Name")
            station_options = [f"{row['StationID']} - {row['Station_Name']}" for _, row in stations.iterrows()]
            selected_station = st.selectbox("Select Weather Station", station_options)
            station_id = int(selected_station.split(" - ")[0])
            
            if st.button("Get Weather Data"):
                station_weather = run_query(conn, """
                    SELECT DateTime, Temperature, Humidity, Rainfall
                    FROM Weather_Readings
                    WHERE StationID=%s
                    ORDER BY DateTime DESC
                    LIMIT 30
                """, (station_id,))
                
                if not station_weather.empty:
                    st.dataframe(station_weather, use_container_width=True)
                    
                    # Calculate averages
                    avg_temp = station_weather['Temperature'].mean()
                    avg_humidity = station_weather['Humidity'].mean()
                    total_rainfall = station_weather['Rainfall'].sum()
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("🌡️ Avg Temp", f"{avg_temp:.1f}°C")
                    col2.metric("💧 Avg Humidity", f"{avg_humidity:.0f}%")
                    col3.metric("🌧️ Total Rainfall", f"{total_rainfall:.1f}mm")
                else:
                    st.info("No data for this station")
    
    elif choice == "📈 My Performance":
        st.subheader("📈 My Performance Analysis")
        
        # Compare with national averages
        st.write("### How You Compare Nationally")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # My average farm size
            my_avg = run_query(conn, """
                SELECT AVG(Area_acres) as avg_area 
                FROM Farms 
                WHERE FarmerID=%s
            """, (st.session_state.farmer_id,))
            my_avg_area = my_avg.iloc[0]['avg_area'] if not my_avg.empty and my_avg.iloc[0]['avg_area'] else 0
            
            # National average
            national_avg = run_query(conn, "SELECT AVG(Area_acres) as avg_area FROM Farms")
            national_avg_area = national_avg.iloc[0]['avg_area'] if not national_avg.empty else 0
            
            st.metric("🌾 My Avg Farm Size", f"{my_avg_area:.2f} acres", 
                     delta=f"{(my_avg_area - national_avg_area):.2f} vs national avg")
        
        with col2:
            # My crop diversity
            my_diversity = run_query(conn, """
                SELECT COUNT(DISTINCT c.CropID) as count
                FROM Cultivates c
                JOIN Farms f ON c.FarmSeq = f.FarmSeq
                WHERE f.FarmerID=%s
            """, (st.session_state.farmer_id,))
            my_crops_count = my_diversity.iloc[0]['count'] if not my_diversity.empty else 0
            
            # National average
            national_diversity = run_query(conn, """
                SELECT AVG(crop_count) as avg_crops
                FROM (
                    SELECT f.FarmerID, COUNT(DISTINCT c.CropID) as crop_count
                    FROM Farms f
                    LEFT JOIN Cultivates c ON f.FarmSeq = c.FarmSeq
                    GROUP BY f.FarmerID
                ) as diversity_stats
            """)
            national_avg_crops = national_diversity.iloc[0]['avg_crops'] if not national_diversity.empty and national_diversity.iloc[0]['avg_crops'] else 0
            
            st.metric("🌱 My Crop Diversity", my_crops_count, 
                     delta=f"{(my_crops_count - national_avg_crops):.1f} vs national avg")
        
        st.markdown("---")
        
        # My ranking
        st.write("### 🏆 My National Ranking")
        
        ranking = run_query(conn, """
            SELECT fa.FarmerID, fa.Name, SUM(f.Area_acres) as Total_Area,
                   RANK() OVER (ORDER BY SUM(f.Area_acres) DESC) as Rank_Position
            FROM Farmers fa
            JOIN Farms f ON fa.FarmerID = f.FarmerID
            GROUP BY fa.FarmerID, fa.Name
        """)
        
        if not ranking.empty:
            my_rank = ranking[ranking['FarmerID'] == st.session_state.farmer_id]
            if not my_rank.empty:
                rank_pos = my_rank.iloc[0]['Rank_Position']
                total_farmers = len(ranking)
                st.success(f"🏅 You rank #{rank_pos} out of {total_farmers} farmers nationally!")
                
                # Show top 5
                st.write("#### Top 5 Farmers by Total Farm Area")
                top5 = ranking.head(5)[['Rank_Position', 'Name', 'Total_Area']]
                st.dataframe(top5, use_container_width=True, hide_index=True)
            else:
                st.info("Start adding farms to see your ranking")
        else:
            st.info("No ranking data available yet")
    
    elif choice == "💡 Recommendations":
        st.subheader("💡 Crop Recommendations for You")
        
        st.write("### 🌟 Best Crops for Current Conditions")
        st.info("Based on sustainability scores and seasonal data")
        
        # Get current season
        current_season = run_query(conn, """
            SELECT SeasonID, Season_Name 
            FROM Crop_Seasons 
            WHERE CURDATE() BETWEEN Start_Date AND End_Date
            LIMIT 1
        """)
        
        if current_season.empty:
            st.warning("No active season found. Showing general recommendations.")
            # Show top crops overall
            recommendations = run_query(conn, """
                SELECT c.Crop_Name, AVG(sa.Assessment_Score) as Avg_Score
                FROM Suitability_Assessment sa
                JOIN Crops c ON sa.CropID = c.CropID
                GROUP BY c.Crop_Name
                ORDER BY Avg_Score DESC
                LIMIT 10
            """)
        else:
            season_id = int(current_season.iloc[0]['SeasonID'])  # Convert to native Python int
            season_name = current_season.iloc[0]['Season_Name']
            st.success(f"📅 Current Season: **{season_name}**")
            
            # Get recommendations for current season
            recommendations = run_query(conn, """
                SELECT c.Crop_Name, AVG(sa.Assessment_Score) as Avg_Score, 
                       COUNT(*) as Assessment_Count
                FROM Suitability_Assessment sa
                JOIN Crops c ON sa.CropID = c.CropID
                WHERE sa.SeasonID=%s
                GROUP BY c.Crop_Name
                ORDER BY Avg_Score DESC
                LIMIT 10
            """, (season_id,))
        
        if not recommendations.empty:
            # Highlight top recommendations
            num_crops = min(len(recommendations), 3)
            st.write(f"### 🌟 Top {num_crops} Recommended Crops")
            
            top_crops = recommendations.head(num_crops)
            
            cols = st.columns(num_crops)
            for idx, (_, crop) in enumerate(top_crops.iterrows()):
                with cols[idx]:
                    rank_emoji = ["🥇", "🥈", "🥉"][idx]
                    score = crop['Avg_Score']
                    
                    # Color based on score
                    if score >= 8:
                        color = "#2e7d32"  # Dark green
                    elif score >= 6:
                        color = "#558b2f"  # Medium green
                    else:
                        color = "#827717"  # Olive
                    
                    st.markdown(f"""
                    <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center; color: white;">
                        <h2>{rank_emoji}</h2>
                        <h3>{crop['Crop_Name']}</h3>
                        <h1>{score:.1f}/10</h1>
                        <p>Sustainability Score</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Show all recommendations in table
            st.write(f"### 📊 All Recommended Crops ({len(recommendations)} total)")
            st.dataframe(recommendations, use_container_width=True, hide_index=True)
            
            # Visualize
            fig = px.bar(recommendations, x="Crop_Name", y="Avg_Score", 
                        title="Crop Sustainability Comparison", 
                        labels={"Avg_Score": "Sustainability Score", "Crop_Name": "Crop"},
                        color="Avg_Score",
                        color_continuous_scale=["#ffeb3b", "#8bc34a", "#2e7d32"])
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("No recommendations available. Check back after sustainability assessments are added.")
    
    elif choice == "👤 My Profile":
        st.subheader("👤 My Profile")
        
        # Get farmer details
        farmer_details = run_query(conn, """
            SELECT FarmerID, Name, Phone_No, DOB 
            FROM Farmers 
            WHERE FarmerID=%s
        """, (st.session_state.farmer_id,))
        
        if not farmer_details.empty:
            farmer = farmer_details.iloc[0]
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.write("### 📋 Profile Details")
                st.write(f"**Farmer ID:** {farmer['FarmerID']}")
                st.write(f"**Name:** {farmer['Name']}")
                st.write(f"**Phone:** {farmer['Phone_No']}")
                st.write(f"**Date of Birth:** {farmer['DOB']}")
            
            with col2:
                st.write("### ✏️ Update Your Information")
                st.info("You can update your name and phone number here")
                
                with st.form("update_contact"):
                    new_name = st.text_input("Name", value=farmer['Name'])
                    new_phone = st.text_input("Phone Number", value=farmer['Phone_No'])
                    submitted = st.form_submit_button("Update Information")
                    
                    if submitted:
                        try:
                            cur = conn.cursor()
                            cur.execute("UPDATE Farmers SET Name=%s, Phone_No=%s WHERE FarmerID=%s", 
                                       (new_name, new_phone, st.session_state.farmer_id))
                            conn.commit()
                            cur.close()
                            # Update session state with new name
                            st.session_state.farmer_name = new_name
                            st.success("✅ Information updated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
        
        st.markdown("---")
        
        # Account information
        st.write("### 🔐 Account Information")
        user_info = run_query(conn, "SELECT Username, Role FROM Users WHERE FarmerID=%s", (st.session_state.farmer_id,))
        if not user_info.empty:
            st.write(f"**Username:** {user_info.iloc[0]['Username']}")
            st.write(f"**Role:** {user_info.iloc[0]['Role']}")
            st.info("💡 Contact Reporter to change your password")

# Clean up
conn.close()
