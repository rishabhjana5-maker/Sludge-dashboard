import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & HEADER
# ---------------------------------------------------------
st.set_page_config(
    page_title="S³ – Smart Sludge Selection & Resource Recovery System",
    page_icon="♻️",
    layout="wide"
)

st.title("♻️ S³ – Smart Sludge Selection & Resource Recovery System")
st.markdown(
    "**Seva First Innovation Challenge (`SEVA57826`)** | *Digital Demonstrator using Illustrative Synthetic Data*"
)
st.info(
    "**Disclaimer:** This demonstrator uses clearly labelled synthetic/illustrative data for preliminary decision support. "
    "It does not certify sludge as safe, authorize treatment, or replace laboratory analysis, regulatory compliance, and qualified engineering approval."
)

# ---------------------------------------------------------
# 2. SYNTHETIC PRESET DATA & TREATMENT PATHWAY DATABASE
# ---------------------------------------------------------
SYNTHETIC_PRESETS = {
    "Custom Batch Entry": None,
    "Synthetic Batch A: High-Organic Municipal Primary Sludge": {
        "batch_id": "SLG-2026-001",
        "source": "Municipal Domestic STP",
        "quantity_tpd": 45.0,
        "moisture_pct": 88.0,
        "organic_matter_pct": 72.0,
        "contaminant_status": "Screened - Compliant",
        "heavy_metals_flag": False,
        "data_confidence": "High (Lab Verified Synthetic)",
        "missing_params": []
    },
    "Synthetic Batch B: Semi-Dried Digested Cake (Low Moisture)": {
        "batch_id": "SLG-2026-002",
        "source": "Secondary Biological WWTP",
        "quantity_tpd": 20.0,
        "moisture_pct": 58.0,
        "organic_matter_pct": 55.0,
        "contaminant_status": "Screened - Compliant",
        "heavy_metals_flag": False,
        "data_confidence": "Medium (Estimated Synthetic)",
        "missing_params": []
    },
    "Synthetic Batch C: Mixed Industrial-Municipal (Contaminated)": {
        "batch_id": "SLG-2026-003",
        "source": "Mixed Industrial-Municipal Inlet",
        "quantity_tpd": 30.0,
        "moisture_pct": 78.0,
        "organic_matter_pct": 48.0,
        "contaminant_status": "Non-Compliant / Elevated Contaminants",
        "heavy_metals_flag": True,
        "data_confidence": "High (Lab Verified Synthetic)",
        "missing_params": []
    },
    "Synthetic Batch D: Incomplete Characterization Stream": {
        "batch_id": "SLG-2026-004",
        "source": "Decentralized Community STP",
        "quantity_tpd": 10.0,
        "moisture_pct": 85.0,
        "organic_matter_pct": 60.0,
        "contaminant_status": "Pending / Missing Screening",
        "heavy_metals_flag": False,
        "data_confidence": "Low (Incomplete Data)",
        "missing_params": ["Contaminant Screening", "Pathogen Count"]
    }
}

# Modular Treatment Pathways & Residue Management Map (All braces properly closed!)
RESIDUE_MAP = {
    "Mechanical Dewatering": {
        "base_suitability": 8.5,
        "energy_efficiency": 8.5,
        "cost_efficiency": 8.5,
        "env_safeguard": 7.5,
        "resource_recovery": 4.0,
        "est_energy_kwh_t": 45,
        "est_cost_inr_t": 850,
        "primary_output": "Dewatered Sludge Cake (20–30% Solids)",
        "secondary_residue": "Filtrate/Centrate liquid (requires return to WWTP headworks)",
        "safeguard_note": "Volume reduction step; does not stabilize pathogens or organic odor.",
        "is_advanced": False
    },
    "Solar / Thermal Drying": {
        "base_suitability": 7.5,
        "energy_efficiency": 6.0,
        "cost_efficiency": 6.5,
        "env_safeguard": 7.5,
        "resource_recovery": 7.0,
        "est_energy_kwh_t": 180,
        "est_cost_inr_t": 1900,
        "primary_output": "Dried Biosolid Pellets (>85% Solids)",
        "secondary_residue": "Condensate water & exhaust vapor",
        "safeguard_note": "Requires odor control and dust explosion safeguards; solar hybrid lowers energy cost.",
        "is_advanced": False
    },
    "Aerobic Composting": {
        "base_suitability": 8.0,
        "energy_efficiency": 8.0,
        "cost_efficiency": 8.0,
        "env_safeguard": 8.0,
        "resource_recovery": 8.5,
        "est_energy_kwh_t": 60,
        "est_cost_inr_t": 1100,
        "primary_output": "Nutrient-Rich Soil Conditioner / Organic Fertilizer",
        "secondary_residue": "Leachate & screened rejects",
        "safeguard_note": "Strictly prohibited for land application if heavy metals or toxic contaminants are present.",
        "is_advanced": False
    },
    "Anaerobic Digestion (Biogas)": {
        "base_suitability": 9.0,
        "energy_efficiency": 9.0,
        "cost_efficiency": 7.5,
        "env_safeguard": 8.5,
        "resource_recovery": 9.5,
        "est_energy_kwh_t": 75,
        "est_cost_inr_t": 1450,
        "primary_output": "Biogas (Methane) + Stabilized Digestate",
        "secondary_residue": "Liquid digestate supernatant & H2S scrubber waste",
        "safeguard_note": "Ideal for high-moisture, high-organic sludge; requires gas-tight containment.",
        "is_advanced": False
    },
    "Selected Thermal Treatment (Pyrolysis / Incineration)": {
        "base_suitability": 7.0,
        "energy_efficiency": 5.5,
        "cost_efficiency": 5.0,
        "env_safeguard": 6.5,
        "resource_recovery": 7.5,
        "est_energy_kwh_t": 320,
        "est_cost_inr_t": 3400,
        "primary_output": "Biochar / Heat Recovery & Sterile Ash",
        "secondary_residue": "Fly ash, bottom ash & flue gas scrubber sludge",
        "safeguard_note": "Requires prior dewatering and strict air-pollution control (APC) compliance.",
        "is_advanced": False
    },
    "Vitrification (Optional Future Feasibility)": {
        "base_suitability": 5.5,
        "energy_efficiency": 3.0,
        "cost_efficiency": 2.5,
        "env_safeguard": 7.0,
        "resource_recovery": 6.5,
        "est_energy_kwh_t": 750,
        "est_cost_inr_t": 6800,
        "primary_output": "Inert Vitrified Slag / Glass Aggregate",
        "secondary_residue": "High-temperature off-gas & volatile heavy metal condensates",
        "safeguard_note": "OPTIONAL ADVANCED PATHWAY ONLY: Not a default solution. Requires independent feasibility, off-gas & cost evaluation.",
        "is_advanced": True
    }
}

# ---------------------------------------------------------
# 3. SIDEBAR: STEP 1 & 2 - BATCH ENTRY & ADJUSTABLE WEIGHTS
# ---------------------------------------------------------
st.sidebar.header("Step 1 & 2: Sludge Batch Profile")
preset_choice = st.sidebar.selectbox("Load Synthetic Demonstrator Preset", list(SYNTHETIC_PRESETS.keys()))
preset = SYNTHETIC_PRESETS[preset_choice]

batch_id = st.sidebar.text_input("Batch Unique ID", value=preset["batch_id"] if preset else "SLG-2026-005")
source = st.sidebar.selectbox(
    "Sludge Source",
    ["Municipal Domestic STP", "Secondary Biological WWTP", "Mixed Industrial-Municipal Inlet", "Decentralized Community STP"],
    index=0 if not preset else ["Municipal Domestic STP", "Secondary Biological WWTP", "Mixed Industrial-Municipal Inlet", "Decentralized Community STP"].index(preset["source"])
)
quantity_tpd = st.sidebar.number_input("Batch Quantity (Tonnes/Day)", min_value=1.0, max_value=500.0, value=preset["quantity_tpd"] if preset else 25.0)
moisture_pct = st.sidebar.slider("Moisture Content (%)", min_value=30.0, max_value=99.0, value=preset["moisture_pct"] if preset else 82.0)
organic_matter_pct = st.sidebar.slider("Volatile / Organic Matter (% of Dry Solids)", min_value=10.0, max_value=90.0, value=preset["organic_matter_pct"] if preset else 65.0)

contaminant_options = ["Screened - Compliant", "Pending / Missing Screening", "Non-Compliant / Elevated Contaminants"]
contaminant_status = st.sidebar.selectbox(
    "Contaminant-Screening Status",
    contaminant_options,
    index=0 if not preset else contaminant_options.index(preset["contaminant_status"])
)
heavy_metals_flag = st.sidebar.checkbox("Elevated Heavy Metals / Toxic Restriction Flag", value=preset["heavy_metals_flag"] if preset else False)

confidence_options = ["High (Lab Verified Synthetic)", "Medium (Estimated Synthetic)", "Low (Incomplete Data)"]
data_confidence = st.sidebar.selectbox(
    "Data Confidence Level",
    confidence_options,
    index=0 if not preset else confidence_options.index(preset["data_confidence"])
)

missing_params = st.sidebar.multiselect(
    "Flagged Missing Parameters",
    ["Contaminant Screening", "Pathogen Count", "Calorific Value", "Heavy Metal Assay"],
    default=preset["missing_params"] if preset else []
)

include_vitrification = st.sidebar.checkbox("Include Vitrification (Optional Future Feasibility)", value=False)

st.sidebar.divider()
st.sidebar.header("Disclosed Scoring Weights (%)")
w_suitability = st.sidebar.slider("Technical Suitability", 0, 50, 30)
w_energy = st.sidebar.slider("Energy Efficiency", 0, 50, 20)
w_cost = st.sidebar.slider("Operating Cost Efficiency", 0, 50, 20)
w_env = st.sidebar.slider("Environmental & Residue Safeguards", 0, 50, 15)
w_recovery = st.sidebar.slider("Resource Recovery Potential", 0, 50, 15)

total_weight = w_suitability + w_energy + w_cost + w_env + w_recovery
if total_weight != 100:
    st.sidebar.warning(f"Weights sum to {total_weight}%. Scores will be normalized to 100%.")

# ---------------------------------------------------------
# 4. STEP 3 & 4: DATA COMPLETENESS & MANDATORY REVIEW GATE
# ---------------------------------------------------------
st.subheader("1. Batch Summary, Data Confidence & Mandatory Review Gate")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Batch ID", batch_id)
m2.metric("Quantity", f"{quantity_tpd:.1f} TPD")
m3.metric("Moisture / Organics", f"{moisture_pct:.0f}% / {organic_matter_pct:.0f}%")
m4.metric("Data Confidence", data_confidence.split(" ")[0])

# Mandatory Compliance & Data-Quality Gate Logic
