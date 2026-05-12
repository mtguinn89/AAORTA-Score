import streamlit as st
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="AAORTA-1 Calculator", layout="centered")

st.markdown(
    """
    <style>
    /* Force main background to white */
    .stApp {
        background-color: white;
    }
    
    /* Force ALL text to pure black, including headers and list items */
    h1, h2, h3, h4, h5, h6, p, li, span, label {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }

    /* Target the Expander Header specifically */
    .streamlit-expanderHeader {
        color: #000000 !important;
        background-color: #f0f2f6 !important; /* Light gray background for contrast */
        border-radius: 5px;
    }

    /* Fix for the expander icon (arrow) color */
    .streamlit-expanderHeader svg {
        fill: #000000 !important;
    }

    /* Target the text inside the expander content specifically */
    [data-testid="stExpander"] div {
        color: #000000 !important;
    }

    /* Keep the metric values (scores) in the blue accent color */
    [data-testid="stMetricValue"] {
        color: #1c83e1 !important;
    }

    /* Ensure checkboxes are visible */
    .stCheckbox > label > div[role="checkbox"] {
        border-color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title Section ---
st.title("AAORTA-1 Risk Calculator")
st.write("**Aortic Arch Operation Risk Tool for Assessment:** Preoperative 90-Day Mortality Prediction.")

# --- Scoring Logic (Synced with R script calculate_points) ---
points_map = {
    "nv_HTAD": -1,
    "nv_PriorCABG": 2,
    "nv_KidneyDisease": 1,
    "nv_PulmonaryDisease": 1,
    "nv_NoSmoke": -1
}

# --- Input Interface ---
st.subheader("Preoperative Patient Parameters")
st.info("Select clinical variables present prior to the index procedure.")

col1, col2 = st.columns(2)

with col1:
    htad = st.checkbox("Heritable Thoracic Aortic Disease (HTAD)", 
                       help="Marfan, Loeys-Dietz, BAV with known genetic variant, or other heritable aortopathy.")
    cabg = st.checkbox("Prior CABG", 
                       help="History of coronary artery bypass grafting.")
    kidney = st.checkbox("Kidney Disease", 
                         help="Documented preoperative renal insufficiency or CKD.")

with col2:
    pulmonary = st.checkbox("Pulmonary Disease", 
                            help="Documented COPD, emphysema, or restrictive lung disease (STS Definition).")
    nosmoke = st.checkbox("Never Used Tobacco", 
                          help="Patient has no clinical history of tobacco use.")

# --- Calculation ---
score = 0
if htad: score += points_map["nv_HTAD"]
if cabg: score += points_map["nv_PriorCABG"]
if kidney: score += points_map["nv_KidneyDisease"]
if pulmonary: score += points_map["nv_PulmonaryDisease"]
if nosmoke: score += points_map["nv_NoSmoke"]


# --- REGRESSION-BASED PROBABILITY ---
# Exact values from institutional model: summary(my_mod)
intercept = -2.062013 
beta_score = 0.5391404 

# Logit calculation and Logistic Transformation
logit = intercept + (beta_score * score)
probability = (1 / (1 + np.exp(-logit))) * 100

st.divider()

# --- Results Display ---
c1, c2 = st.columns(2)
with c1:
    st.metric(label="Calculated AAORTA-1 Score", value=f"{score} Points")
with c2:
    st.metric(label="Predicted 90-Day Mortality", value=f"{round(probability, 1)}%")

# --- Risk Stratification & Clinical Guidance ---
if score <= 0:
    st.success("✅ **RISK GROUP: LOW RISK**")
    st.info("**Guidance:** Standard postoperative surveillance and routine ICU care.")
elif score == 1:
    st.warning("⚠️ **RISK GROUP: MEDIUM RISK**")
    st.info("**Guidance:** Consider optimized ICU monitoring and early multidisciplinary involvement.")
else:
    st.error("🚨 **RISK GROUP: HIGH RISK**")
    st.warning("**Guidance:** Significant risk for early mortality. Evaluate for preoperative optimization or alternative surgical strategies.")

# --- Scientific Context ---
with st.expander("Model Performance & Definitions"):
    st.write(f"""
    **Model Calibration:**
    The AAORTA-1 score utilizes a logistic regression model.
    
    **Definitions:**
    - **HTAD:** Heritable Thoracic Aortic Disease.
    - **Pulmonary Disease:** Includes asthma, chronic obstructive pulmonary disease, obstructive sleep apnea, 
    prior lung transplant, tuberculosis, pneumothorax, and other documented chronic pulmonary conditions.
    - **90-Day Mortality:** All-cause mortality within 90 days of the index procedure.
    """)

st.write("---")
st.caption("© 2026 AAORTA Score Project. For research and educational purposes only.")
