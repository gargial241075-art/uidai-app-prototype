import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# 1. PAGE CONFIG (Government Portal Theme)
# ======================================================
st.set_page_config(
    page_title="UIDAI Smart Queue Management System",
    page_icon="🆔",
    layout="wide"
)

# Custom CSS for Government Portal Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 4px;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #003366;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #003366;
    }
    </style>
    """, unsafe_allow_html=True)

# ======================================================
# 2. LANGUAGE DICTIONARY
# ======================================================
t = {
    "English": {
        "nav_title": "🏛️ UIDAI Official",
        "nav_page": "Service Selection",
        "role_sel": "Portal Access",
        "pages": ["Overview", "Citizen Portal", "Center Locator Map", "Admin Strategic Dashboard", "Forecast & Insights"],
        "header_main": "🆔 Aadhaar Service Saturation Dashboard",
        "subheader_main": "Official Smart Governance Portal - Resource Optimization Engine",
        "triggers_head": "📅 Real-time Demand Triggers",
        "trigger_scheme": "Govt Scheme Active (+20%)",
        "trigger_holiday": "Public Holiday (+10%)",
        "trigger_bank": "Bank Deadline (+15%)",
        "kpi_total": "Total Centers",
        "kpi_wait": "Avg Wait Time",
        "kpi_red": "Critical Centers",
        "kpi_boost": "Active Boost",
        "matrix_head": "Live Saturation Status Matrix",
        "heatmap_head": "Regional Load Heatmap",
        "token_head": "🎟️ Generate E-Token",
        "token_btn": "Book Appointment",
        "insight_head": "💡 Center Statistics",
        "nearest_head": "🗺 GIS Center Locator",
        "admin_head": "🛡️ Administrative Command Center",
        "forecast_head": "📈 Analytics & Strategic Projections",
        "tabs": ["📊 Weekly Trends", "📉 Monthly Projections"],
        "nearest_found": "📍 Nearest ASK located:",
        "km_away": "KM away",
        "admin_lock": "🔒 Access Restricted. Official Login Required.",
        "shift_btn": "Execute Resource Shifting",
        "shift_msg": "Order dispatched to UIDAI Regional Office."
    },
    "Hindi": {
        "nav_title": "🏛️ यूआईडीएआई आधिकारिक",
        "nav_page": "सेवा चयन",
        "role_sel": "पोर्टल एक्सेस",
        "pages": ["ओवरव्यू", "नागरिक पोर्टल", "केंद्र लोकेटर मैप", "एडमिन डैशबोर्ड", "पूर्वानुमान और इनसाइट्स"],
        "header_main": "🆔 आधार सेवा संतृप्ति डैशबोर्ड",
        "subheader_main": "आधिकारिक स्मार्ट गवर्नेंस पोर्टल - संसाधन अनुकूलन इंजन",
        "triggers_head": "📅 रीयल-टाइम डिमांड ट्रिगर्स",
        "trigger_scheme": "सरकारी योजना सक्रिय (+20%)",
        "trigger_holiday": "सार्वजनिक अवकाश (+10%)",
        "trigger_bank": "बैंक समय सीमा (+15%)",
        "kpi_total": "कुल केंद्र",
        "kpi_wait": "औसत प्रतीक्षा समय",
        "kpi_red": "गंभीर केंद्र",
        "kpi_boost": "सक्रिय बूस्ट",
        "matrix_head": "लाइव स्टेटस मैट्रिक्स",
        "heatmap_head": "क्षेत्रीय लोड हीटमैप",
        "token_head": "🎟️ ई-टोकन जेनरेट करें",
        "token_btn": "अपॉइंटमेंट बुक करें",
        "insight_head": "💡 केंद्र सांख्यिकी",
        "nearest_head": "🗺 जीआईएस केंद्र लोकेटर",
        "admin_head": "🛡️ प्रशासनिक कमांड सेंटर",
        "forecast_head": "📈 एनालिटिक्स और रणनीतिक अनुमान",
        "tabs": ["📊 साप्ताहिक रुझान", "📉 मासिक अनुमान"],
        "nearest_found": "📍 निकटतम एएसके मिला:",
        "km_away": "किमी दूर",
        "admin_lock": "🔒 एक्सेस प्रतिबंधित। आधिकारिक लॉगिन आवश्यक है।",
        "shift_btn": "संसाधन स्थानांतरण निष्पादित करें",
        "shift_msg": "यूआईडीएआई क्षेत्रीय कार्यालय को आदेश भेजा गया।"
    }
}

# ======================================================
# 3. SIDEBAR & LOGIC
# ======================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/cf/Aadhaar_Logo.svg/1200px-Aadhaar_Logo.svg.png", width=100)
st.sidebar.title("🌐 Language")
lang = st.sidebar.selectbox("Select Language", ["English", "Hindi"], label_visibility="collapsed")
cur = t[lang]

st.sidebar.divider()
st.sidebar.title(cur["nav_title"])
user_role = st.sidebar.selectbox(cur["role_sel"], ["Citizen", "Administrator"])

page_idx = st.sidebar.radio(cur["nav_page"], range(len(cur["pages"])), format_func=lambda x: cur["pages"][x])
page = t["English"]["pages"][page_idx]

def calculate_distance(lat1, lon1, lat2, lon2):
    radius = 6371 
    dlat = math.radians(lat2 - lat1); dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2)
    return radius * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

if "tokens" not in st.session_state: st.session_state.tokens = []

data = {
    "Center Name": ["ASK - Napier Town", "ASK - Wright Town", "ASK - Vijay Nagar", "ASK - Ranjhi", "ASK - GCF Jabalpur"],
    "Historical Load": [65, 40, 85, 50, 30], "Real-Time Queue": [80, 35, 95, 55, 20],
    "Active Counters": [5, 3, 6, 4, 2], "Staff Efficiency": [0.9, 0.85, 0.95, 0.7, 0.8],
    "Latitude": [23.168, 23.163, 23.201, 23.185, 23.190], "Longitude": [79.932, 79.928, 79.895, 79.980, 79.960]
}
df_base = pd.DataFrame(data)

# ======================================================
# 4. DYNAMIC TRIGGER FUNCTION
# ======================================================
def apply_triggers(dataframe):
    st.markdown(f"### {cur['triggers_head']}")
    t1, t2, t3 = st.columns(3)
    with t1: scheme = st.toggle(cur["trigger_scheme"])
    with t2: holiday = st.toggle(cur["trigger_holiday"])
    with t3: deadline = st.toggle(cur["trigger_bank"])
    
    boost = (20 if scheme else 0) + (10 if holiday else 0) + (15 if deadline else 0)
    temp_df = dataframe.copy()
    temp_df["Saturation Score"] = (0.4 * temp_df["Historical Load"] + 0.4 * (temp_df["Historical Load"] + boost) + 0.2 * temp_df["Real-Time Queue"]).clip(0, 100).astype(int)
    temp_df["Wait Time (min)"] = ((temp_df["Real-Time Queue"] * 5) / (temp_df["Active Counters"] * temp_df["Staff Efficiency"])).astype(int)
    
    l_red = "🔴 Red" if lang == "English" else "🔴 लाल (गंभीर)"
    l_yellow = "🟡 Yellow" if lang == "English" else "🟡 पीला (चेतावनी)"
    l_green = "🟢 Green" if lang == "English" else "🟢 हरा (सामान्य)"
    temp_df["Zone Status"] = temp_df["Saturation Score"].apply(lambda s: l_red if s > 80 else (l_yellow if s > 50 else l_green))
    return temp_df, boost

# ======================================================
# 5. MAIN LOGIC
# ======================================================
st.title(cur["header_main"])
st.caption(cur["subheader_main"])

# --- OVERVIEW ---
if page == "Overview":
    df, b_val = apply_triggers(df_base)
    st.divider()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(cur["kpi_total"], len(df))
    k2.metric(cur["kpi_wait"], f"{int(df['Wait Time (min)'].mean())} m")
    k3.metric(cur["kpi_red"], len(df[df["Saturation Score"] > 80]))
    k4.metric(cur["kpi_boost"], f"+{b_val}%")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(cur["matrix_head"])
        st.dataframe(df.style.applymap(lambda x: 'background-color: #f8d7da' if 'Red' in str(x) or 'लाल' in str(x) else '', subset=['Zone Status']), use_container_width=True)
    with col2:
        st.subheader(cur["heatmap_head"])
        fig, ax = plt.subplots(); sns.heatmap(df[["Historical Load", "Real-Time Queue", "Saturation Score"]], annot=True, cmap="YlOrRd", ax=ax)
        st.pyplot(fig)

# --- CITIZEN PORTAL ---
elif page == "Citizen Portal":
    df, _ = apply_triggers(df_base)
    st.divider()
    t1, t2 = st.columns(2)
    with t1:
        st.subheader(cur["token_head"])
        sel_c = st.selectbox("Select Center", df["Center Name"])
        u_name = st.text_input("Full Name as per Aadhaar")
        if st.button(cur["token_btn"]):
            if u_name:
                wait = df[df["Center Name"] == sel_c]["Wait Time (min)"].values[0]
                t_id = f"UID-{np.random.randint(1000, 9999)}"
                st.session_state.tokens.append({"ID": t_id, "Name": u_name, "Center": sel_c, "Wait": f"{wait}m", "Time": (datetime.now() + timedelta(minutes=int(wait))).strftime("%H:%M")})
                st.success(f"Official E-Token {t_id} Generated!")
    with t2:
        st.subheader(cur["insight_head"])
        c_stats = df[df["Center Name"] == sel_c].iloc[0]
        st.metric("Center Saturation", f"{c_stats['Saturation Score']}%")
        st.progress(int(c_stats["Saturation Score"]) / 100)

# --- CENTER LOCATOR ---
elif page == "Center Locator Map":
    st.header(cur["nearest_head"])
    u_lat = st.sidebar.number_input("Mock GPS Lat", value=23.170); u_lon = st.sidebar.number_input("Mock GPS Lon", value=79.950)
    df_base["Dist"] = df_base.apply(lambda r: calculate_distance(u_lat, u_lon, r["Latitude"], r["Longitude"]), axis=1)
    st.success(f"{cur['nearest_found']} {df_base.sort_values('Dist').iloc[0]['Center Name']} ({df_base.sort_values('Dist').iloc[0]['Dist']:.2f} {cur['km_away']})")
    st.map(df_base.rename(columns={"Latitude": "lat", "Longitude": "lon"}))

# --- ADMIN DASHBOARD ---
elif page == "Admin Strategic Dashboard":
    if user_role != "Administrator":
        st.error(cur["admin_lock"])
    else:
        st.header(cur["admin_head"])
        df_admin = df_base.copy()
        df_admin["Saturation Score"] = (0.4 * df_admin["Historical Load"] + 0.4 * df_admin["Historical Load"] + 0.2 * df_admin["Real-Time Queue"]).astype(int)
        
        reds = df_admin[df_admin["Saturation Score"] > 70]; greens = df_admin[df_admin["Saturation Score"] < 50]
        if not reds.empty and not greens.empty:
            st.warning(f"🚨 STRATEGIC ALERT: {reds.iloc[0]['Center Name']} Capacity Breached.")
            if st.button(cur["shift_btn"]): st.success(cur["shift_msg"])
        st.plotly_chart(px.area(pd.DataFrame({"Time": [f"{i}:00" for i in range(9, 19)], "Load": [30, 45, 75, 95, 80, 60, 40, 35, 30, 25]}), x="Time", y="Load", title="Regional Demand Prediction"), use_container_width=True)

# --- FORECAST & INSIGHTS ---
elif page == "Forecast & Insights":
    st.header(cur["forecast_head"])
    
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📅 Service Demand Projections")
        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1: sel_date = st.date_input("Date", datetime.now())
        with d_col2: sel_month = st.selectbox("Month", ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], index=datetime.now().month-1)
        with d_col3: sel_week = st.selectbox("Week Number", ["Week 1", "Week 2", "Week 3", "Week 4"])
        
        sel_time_str = st.selectbox("Target Time Slot", [f"{h:02d}:00" for h in range(9, 19)], index=3)
        sel_time_int = int(sel_time_str.split(":")[0])

        day_name = sel_date.strftime("%A")
        mult = 1.35 if day_name in ["Saturday", "Sunday"] else 1.0
        h_list = list(range(9, 19))
        daily_vals = [max(15, min(98, (95 - abs(13 - h)*12) * mult)) for h in h_list]
        daily_df = pd.DataFrame({"Hour": h_list, "Load": daily_vals})

        fig_daily = px.area(daily_df, x="Hour", y="Load", title=f"Demand Curve: {sel_date} ({sel_week})", color_discrete_sequence=['#003366'])
        fig_daily.add_vline(x=sel_time_int, line_dash="dash", line_color="#ff0000")
        st.plotly_chart(fig_daily, use_container_width=True)
        
        st.info(f"**Analysis:** Load for {sel_week} of {sel_month} at {sel_time_str} is projected to be **{int(daily_vals[h_list.index(sel_time_int)])}%**.")

    with col_right:
        st.subheader("📊 Analytical Macro Trends")
        tab_w, tab_m = st.tabs(cur["tabs"])
        
        with tab_w:
            week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            week_load = [45, 52, 60, 85, 55, 92, 88]
            st.plotly_chart(px.bar(x=week_days, y=week_load, color=week_load, color_continuous_scale="Blues", labels={'x':'Day','y':'Load %'}), use_container_width=True)
            st.write(f"**Insight:** Historical data for {sel_week} indicates a surge during weekends.")

        with tab_m:
            month_weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
            month_load = [55, 72, 68, 80]
            st.plotly_chart(px.line(x=month_weeks, y=month_load, markers=True, title=f"Projected Trend for {sel_month}").update_traces(line_color="#003366"), use_container_width=True)
            st.write(f"**Monthly projection:** {sel_month} anticipates a 12% rise in address update requests.")

# ============= FOOTER =============
st.sidebar.markdown("---")
st.sidebar.caption("Digital India Initiative | UIDAI Command Dashboard")
st.sidebar.write(f"Server Status: Online | {datetime.now().strftime('%d-%m-%Y %H:%M')}")
