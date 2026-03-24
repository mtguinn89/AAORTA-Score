import streamlit as st

# Set page configuration
st.set_page_config(page_title="AAORTA Score Calculator", layout="centered")

st.title("AAORTA-1 Risk Calculator")
st.write("Aortic Arch Operation Risk Tool for Assessment: Preoperative 90-Day Mortality Prediction.")

# --- Scoring Logic ---
# Points based on your validated model:
# HTAD: -1 | Prior CABG: 2 | Kidney Disease: 1 | Pulmonary Disease: 1 | Never Smoked: -1
points_map = {
    "nv_HTAD": -1,
    "nv_PriorCABG": 2,
    "nv_KidneyDisease": 1,
    "nv_PulmonaryDisease": 1,
    "nv_NoSmoke": -1
}

st.subheader("Preoperative Parameters")
st.info("Select all that apply to the patient prior to the incision.")

# --- Input Interface ---
col1, col2 = st.columns(2)

with col1:
    htad = st.checkbox("Heritable Thoracic Aortic Disease (HTAD)", help="e.g., Marfan, Loeys-Dietz, BAV with known genetic variant.")
    cabg = st.checkbox("Prior CABG", help="Previous coronary artery bypass grafting.")
    kidney = st.checkbox("Kidney Disease", help="Documented renal insufficiency or CKD.")

with col2:
    pulmonary = st.checkbox("Pulmonary Disease", help="COPD, emphysema, or severe restrictive lung disease.")
    nosmoke = st.checkbox("Never Used Tobacco", help="Patient has no history of tobacco use.")

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

# Threshold Logic based on your validated brackets:
# Low: <= 0 | Medium: 1 | High: > 1
if score <= 0:
    st.success("✅ **RISK GROUP: LOW RISK**")
    st.write("**Observed 90-Day Mortality:** ~5.3%")
    st.info("**Clinical Guidance:** Standard postoperative surveillance.")
elif score == 1:
    st.warning("⚠️ **RISK GROUP: MEDIUM RISK**")
    st.write("**Observed 90-Day Mortality:** ~26.5%")
    st.info("**Clinical Guidance:** Consider optimized ICU monitoring and early involvement of multidisciplinary teams.")
else:
    st.error("🚨 **RISK GROUP: HIGH RISK**")
    st.write("**Observed 90-Day Mortality:** ~33.3%")
    st.warning("**Clinical Guidance:** High risk for early mortality. Evaluate for preoperative optimization or alternative surgical strategies.")

# --- Scientific Context ---
with st.expander("Model Performance & Definitions"):
    st.write(f"""
    **Scientific Validation:**
    - **C-Statistic (AUC):** High predictive accuracy for 90-day mortality.
    - **Calibration:** Excellent agreement between predicted and observed mortality (R² = 0.83).
    - **Brier Score:** {0.1049} (Lower values indicate better predictive performance).
    
    **Definitions:**
    - **HTAD:** Heritable Thoracic Aortic Disease.
    - **90-Day Mortality:** Includes all-cause mortality within 90 days of the index aortic procedure.
    """)

st.caption("Disclaimer: This tool is for research and educational purposes only and should not replace clinical judgment.")
