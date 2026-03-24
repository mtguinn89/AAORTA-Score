import streamlit as st

# Set page configuration for mobile responsiveness
st.set_page_config(page_title="CDRI Calculator", layout="centered")

st.title("Cardiac Diuretic-Responsiveness Index (CDRI)")
st.write("A standardized tool for real-time renal risk assessment following cardiac surgery.")

# --- Calculator Interface ---
st.subheader("Patient Parameters")
col1, col2 = st.columns(2)

with col1:
    weight = st.number_input("Patient Weight (kg)", min_value=1.0, value=70.0, step=0.1, help="Actual body weight at time of surgery.")
    dose = st.number_input("Diuretic Dose (mg Furosemide Eq)", min_value=1.0, value=20.0, step=1.0, help="IV Furosemide equivalent dose.")

with col2:
    uop = st.number_input("1-Hour Urine Output (mL)", min_value=0.0, step=1.0, help="Total urine volume produced in the first hour post-dose.")

# CDRI Formula: UOP / (Weight * Dose)
cdri = uop / (weight * dose)

st.divider()

# Results Display
st.metric(label="Calculated CDRI", value=f"{cdri:.4f} cc/kg/hr/mg")

# Threshold Logic based on segmental regression
if cdri < 0.075:
    st.error("🚨 **RESULT: NON-RESPONDER**")
    st.warning("**Clinical Action:** High risk for CSA-AKI. Consider early renal protective interventions.")
else:
    st.success("✅ **RESULT: ADEQUATE RESPONDER**")
    st.info("**Clinical Action:** Low risk for CSA-AKI development. Continue standard postoperative care.")

# --- Scientific Context ---
with st.expander("About this Metric"):
    st.write("""
    **Evidence Base:**
    - **Threshold:** 0.075 cc/kg/hr/mg (derived via segmental regression).
    - **Predictive Power:** CDRI < 0.075 is associated with an 8.37 Adjusted Odds Ratio for AKI development.
    - **Performance:** Outperforms traditional oliguria (C-stat 0.85 vs 0.77).
    """)
