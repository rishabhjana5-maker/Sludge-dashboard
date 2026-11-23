import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="S³ – Smart Sludge Selection System", page_icon="♻️", layout="wide")

st.title("♻️ S³ – Smart Sludge Selection & Resource Recovery System")
st.caption("Preliminary Decision-Support Framework | Track 1: Sustainable Technologies | Idea ID: SEVA57826")
st.info(
    "**Illustrative Demonstrator Disclaimer:** This MVP uses **clearly labelled synthetic criteria** for early-stage planning. "
    "It does not certify sludge safety, replace certified laboratory analysis, or substitute statutory engineering approvals."
)

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Batch Registration & Profile")

preset = st.sidebar.selectbox(
    "Load Illustrative Synthetic Preset:",
    [
        "Custom Entry",
        "Preset A: High-Organic Municipal Sludge (Clean)",
        "Preset B: High-Moisture Raw Sludge (Missing Data)",
        "Preset C: Industrial-Mixed Sludge (Contaminated)"
    ]
)

if preset == "Preset A: High-Organic Municipal Sludge (Clean)":
    def_id, def_src, def_qty = "SLG-2026-001", "Municipal STP - Zone A", 25.0
    def_moist, def_org = 78, 68
    def_contam, def_conf = "Screened - Compliant (Low Heavy Metals)", "High (Lab Verified)"
elif preset == "Preset B: High-Moisture Raw Sludge (Missing Data)":
    def_id, def_src, def_qty = "SLG-2026-002", "Primary Clarifier - North", 40.0
    def_moist, def_org = 92, 55
    def_contam, def_conf = "Pending / Incomplete Screening", "Low (Estimated)"
elif preset == "Preset C: Industrial-Mixed Sludge (Contaminated)":
    def_id, def_src, def_qty = "SLG-2026-003", "CETP / Mixed Industrial Line", 15.0
    def_moist, def_org = 65, 42
    def_contam, def_conf = "Flagged - Exceeds Contaminant Limits", "Medium (Partial Lab)"
else:
    def_id, def_src, def_qty = "SLG-2026-004", "Municipal STP", 20.0
    def_moist, def_org = 80, 60
    def_contam, def_conf = "Screened - Compliant (Low Heavy Metals)", "High (Lab Verified)"

batch_id = st.sidebar.text_input("Batch Unique ID", value=def_id)
source = st.sidebar.text_input("Sludge Source / Origin", value=def_src)
quantity = st.sidebar.number_input("Batch Quantity (Tonnes/Day)", min_value=1.0, max_value=1000.0, value=def_qty)

st.sidebar.subheader("2. Characterization Data")
moisture = st.sidebar.slider("Moisture Content (%)", 10, 98, def_moist)
organic_matter = st.sidebar.slider("Organic Matter (% Dry Solids)", 10, 90, def_org)

contam_options = [
    "Screened - Compliant (Low Heavy Metals)",
    "Pending / Incomplete Screening",
    "Flagged - Exceeds Contaminant Limits"
]
contaminant_status = st.sidebar.selectbox(
    "Contaminant-Screening Status",
    contam_options,
    index=contam_options.index(def_contam)
)

conf_options = ["High (Lab Verified)", "Medium (Partial Lab)", "Low (Estimated)"]
data_confidence = st.sidebar.selectbox(
    "Data Confidence Level",
    conf_options,
    index=conf_options.index(def_conf)
)

st.sidebar.subheader("3. Adjustable Scoring Weights")
w_suitability = st.sidebar.slider("Technical Suitability", 1, 10, 8)
w_energy = st.sidebar.slider("Low Energy Demand", 1, 10, 7)
w_cost = st.sidebar.slider("Low Operating Cost", 1, 10, 7)
w_env = st.sidebar.slider("Environmental & Residue Safety", 1, 10, 9)
w_recovery = st.sidebar.slider("Resource Recovery Potential", 1, 10, 8)
total_weight = w_suitability + w_energy + w_cost + w_env + w_recovery

# --- NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs([
    "🧪 Single Batch Assessment (Steps 1–8)",
    "📂 Bulk Lab CSV Screener",
    "📊 Plant-Scale Impact Estimator"
])

# ==============================================================================
# TAB 1: SINGLE BATCH WORKFLOW
# ==============================================================================
with tab1:
    st.subheader("Step 1–4: Batch Summary, Data Quality & Mandatory Review Gate")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Batch ID", batch_id)
    col2.metric("Quantity", f"{quantity} T/day")
    col3.metric("Moisture / Organics", f"{moisture}% / {organic_matter}%")
    col4.metric("Data Confidence", data_confidence.split(" ")[0])

    gate_blocked = False
    if contaminant_status == "Flagged - Exceeds Contaminant Limits":
        gate_blocked = True
        st.error(
            "🚨 **MANDATORY REVIEW GATE TRIGGERED (NON-COMPLIANT):** "
            "Biological & agricultural pathways (Composting, Anaerobic Digestion) are **BLOCKED** regardless of weighted score."
        )
    elif contaminant_status == "Pending / Incomplete Screening" or data_confidence == "Low (Estimated)":
        st.warning(
            "⚠️ **DATA QUALITY CAUTION:** Screening is incomplete or confidence is low. "
            "Laboratory verification is mandatory before finalizing treatment selection."
        )
    else:
        st.success("✅ **COMPLIANCE GATE PASSED:** Batch meets preliminary screening thresholds for multi-pathway comparison.")

    st.divider()

    # --- STEP 5-7: SCORING & MATRIX ---
    st.subheader("Step 5–7: Candidate Pathway Comparison & Weighted Scoring")

    dewater_suit = 9.5 if moisture > 75 else 4.0
    drying_suit = 8.0 if moisture <= 80 else 5.0
    compost_suit = 8.5 if (organic_matter >= 50 and moisture <= 80) else 4.5
    ad_suit = 9.0 if (organic_matter >= 55 and moisture >= 70) else 5.0
    thermal_suit = 8.0 if (moisture <= 65 and organic_matter >= 45) else 4.5
    vitrif_suit = 7.5 if moisture <= 50 else 3.5

    pathways = [
        {
            "Pathway": "Mechanical Dewatering",
            "Suitability": dewater_suit,
            "Energy": 8.5,
            "Cost": 8.5,
            "Env_Safety": 7.5,
            "Recovery": 4.0,
            "Status": "Eligible",
            "Caution": "Produces wet sludge cake requiring secondary treatment/disposal."
        },
        {
            "Pathway": "Thermal Drying",
            "Suitability": drying_suit,
            "Energy": 4.0,
            "Cost": 5.0,
            "Env_Safety": 7.5,
            "Recovery": 7.0,
            "Status": "Eligible",
            "Caution": "High thermal energy demand; requires odor and dust controls."
        },
        {
            "Pathway": "Composting (Aerobic)",
            "Suitability": compost_suit,
            "Energy": 8.0,
            "Cost": 8.0,
            "Env_Safety": 1.0 if gate_blocked else 7.0,
            "Recovery": 8.5,
            "Status": "BLOCKED (Contamination)" if gate_blocked else "Eligible",
            "Caution": "Requires bulking agents, land area, and heavy-metal compliance."
        },
        {
            "Pathway": "Anaerobic Digestion",
            "Suitability": ad_suit,
            "Energy": 7.5,
            "Cost": 6.0,
            "Env_Safety": 1.0 if gate_blocked else 8.0,
            "Recovery": 9.5,
            "Status": "BLOCKED (Contamination)" if gate_blocked else "Eligible",
            "Caution": "Sensitive to toxic shock loads; requires biogas handling."
        },
        {
            "Pathway": "Thermal Treatment (Incineration/Pyrolysis)",
            "Suitability": thermal_suit,
            "Energy": 4.5,
            "Cost": 4.0,
            "Env_Safety": 6.5,
            "Recovery": 7.5,
            "Status": "Eligible (Review Required)",
            "Caution": "Requires pre-drying, flue-gas scrubbing, and ash disposal."
        },
        {
            "Pathway": "Vitrification (Optional Advanced)",
            "Suitability": vitrif_suit,
            "Energy": 2.0,
            "Cost": 2.5,
            "Env_Safety": 8.5,
            "Recovery": 8.0,
            "Status": "Optional Feasibility Only",
            "Caution": "Not a default solution; extreme energy demand requires independent study."
        }
    ]

    df = pd.DataFrame(pathways)
    df["Weighted Score (/100)"] = (
        (df["Suitability"] * w_suitability)
        + (df["Energy"] * w_energy)
        + (df["Cost"] * w_cost)
        + (df["Env_Safety"] * w_env)
        + (df["Recovery"] * w_recovery)
    ) / (total_weight * 10) * 100
    df["Weighted Score (/100)"] = df["Weighted Score (/100)"].round(1)

    df["Sort_Key"] = df.apply(lambda r: -1 if "BLOCKED" in r["Status"] else r["Weighted Score (/100)"], axis=1)
    df = df.sort_values(by="Sort_Key", ascending=False).drop(columns=["Sort_Key"]).reset_index(drop=True)

    chart_col, table_col = st.columns([1, 1.4])
    with chart_col:
        st.markdown("**Preliminary Weighted Score Comparison**")
        st.bar_chart(df.set_index("Pathway")["Weighted Score (/100)"])

    with table_col:
        st.markdown("**Decision Matrix & Key Cautions**")
        st.dataframe(df[["Pathway", "Status", "Weighted Score (/100)", "Caution"]], use_container_width=True, hide_index=True)

    st.divider()

    # --- STEP 8: SUMMARY, RESIDUE PROFILE & DOWNLOAD ---
    st.subheader("Step 8: Batch Assessment Summary & Expert Hand-off")

    eligible_df = df[~df["Status"].str.contains("BLOCKED")].reset_index(drop=True)
    top_pathway = eligible_df.loc[0, "Pathway"]
    top_score = eligible_df.loc[0, "Weighted Score (/100)"]
    gate_msg = "BLOCKED - Non-compliant contaminant levels detected." if gate_blocked else "PASSED / PROVISIONAL - Eligible for technical review."

    residue_map = {
        "Mechanical Dewatering": (
            "Dewatered Sludge Cake (~25–30% solids)",
            "Filtrate water returned to STP headworks; cake requires secondary stabilization."
        ),
        "Thermal Drying": (
            "Dried Biosolid Pellets (>90% solids)",
            "Condensate & exhaust air require scrubbers; pellets usable as fuel/soil conditioner if compliant."
        ),
        "Composting (Aerobic)": (
            "Nutrient-Rich Organic Compost",
            "Leachate collection required; must pass CPCB heavy-metal limits before agricultural application."
        ),
        "Anaerobic Digestion": (
            "Biogas (Methane) + Stabilized Digestate",
