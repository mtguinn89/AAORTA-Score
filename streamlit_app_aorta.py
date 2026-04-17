import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="AAORTA-1 Calculator", layout="centered")

# 2. Force Light Mode / White Background via CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }
    h1, h2, h3, p, span, label, .stCheckbox {
        color: #262730 !important;
    }
    [data-testid="stMetricValue"] {
        color: #1c83e1 !important;
    }
    /* Style checkboxes to be clearly visible on white */
    .stCheckbox > label > div {
        border: 1px solid #d3d3d3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title Section ---
st.title("AAORTA-1 Risk Calculator")
st.write("**Aortic Arch Operation Risk Tool for Assessment:** Preoperative 90-Day Mortality Prediction.")

# --- Scoring Logic ---
# HTAD: -1 | Prior CABG: 2 | Kidney Disease: 1 | Pulmonary Disease: 1 | Never Smoked: -1
points_map = {
    "nv_HTAD": -1,
    "nv_PriorCABG": 2,
    "nv_KidneyDisease": 1,
    "nv_PulmonaryDisease": 1,
    "nv_NoSmoke": -1
}

# --- Input Interface ---
st.subheader("Preoperative Patient Parameters")
st.info("Select variables present prior to the index procedure.")

col1, col2 = st.columns(2)

with col1:
    htad = st.checkbox("Heritable Thoracic Aortic Disease (HTAD)", 
                       help="e.g., Marfan, Loeys-Dietz, BAV with known genetic variant.")
    cabg = st.checkbox("Prior CABG", 
                       help="Previous coronary artery bypass grafting.")
    kidney = st.checkbox("Kidney Disease", 
                         help="Documented renal insufficiency or CKD.")

with col2:
    pulmonary = st.checkbox("Pulmonary Disease", 
                            help="COPD, emphysema, or severe restrictive lung disease.")
    nosmoke = st.checkbox("Never Used Tobacco", 
                          help="Patient has no history of tobacco use.")

# --- Calculation ---
score = 0
if htad: score += points_map["nv_HTAD"]
if cabg: score += points_map["nv_PriorCABG"]
if kidney: score += points_map["nv_KidneyDisease"]
if pulmonary: score += points_map["nv_PulmonaryDisease"]
if nosmoke: score += points_map["nv_NoSmoke"]

st.divider()

# --- Results Display ---
st.metric(label="Calculated AAORTA-1 Score", value=f"{score} Points")

# Threshold Logic based on validated brackets: Low (<=0), Medium (1), High (>1)
if score <= 0:
    st.success("✅ **RISK GROUP: LOW RISK**")
    st.write("**Observed 90-Day Mortality:** ~5.3%")
    st.info("**Clinical Guidance:** Standard postoperative surveillance and routine ICU care.")
elif score == 1:
    st.warning("⚠️ **RISK GROUP: MEDIUM RISK**")
    st.write("**Observed 90-Day Mortality:** ~26.5%")
    st.info("**Clinical Guidance:** Consider optimized ICU monitoring and early multidisciplinary involvement.")
else:
    st.error("🚨 **RISK GROUP: HIGH RISK**")
    st.write("**Observed 90-Day Mortality:** ~33.3%")
    st.warning("**Clinical Guidance:** High risk for early mortality. Evaluate for preoperative optimization or alternative surgical strategies.")

# --- Scientific Context ---
with st.expander("Model Performance & Definitions"):
    st.write(f"""
    **Scientific Validation:**
    - **Calibration:** Excellent agreement between predicted and observed mortality (R² = 0.83).
    - **Brier Score:** 0.1049 (Indicates high predictive accuracy).
    
    **Definitions:**
    - **HTAD:** Heritable Thoracic Aortic Disease.
    - **90-Day Mortality:** All-cause mortality within 90 days of the index procedure.
    """)

st.write("---")
st.caption("© 2026 AAORTA Score Project. For research and educational purposes only.")
