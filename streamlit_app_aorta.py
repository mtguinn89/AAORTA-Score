import streamlit as st
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="AAORTA-1 Calculator", layout="centered")


# 2. Page Configuration & Styling (TOTAL STATE LOCK)
st.markdown(
    """
    <style>
    .stApp {
        background-color: white;
    }

    /* 1. Force all text and list items to absolute black */
    h1, h2, h3, h4, h5, h6, p, li, span, label {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        opacity: 1 !important;
    }

    /* 2. THE NUCLEAR OPTION: Lock the background for the entire expander tree */
    /* This targets the outer box, the header, and the internal hover container */
    [data-testid="stExpander"], 
    [data-testid="stExpanderDetails"],
    .streamlit-expanderHeader,
    .streamlit-expanderHeader > div,
    .streamlit-expanderHeader:hover,
    .streamlit-expanderHeader:active {
        background-color: #e7f3fe !important; /* Persistent Light Blue */
        color: #000000 !important;
        border-color: #b6d4fe !important;
    }

    /* 3. Disable the Streamlit "Transition" that causes the flash/fade to black */
    .streamlit-expanderHeader {
        transition: none !important;
        border: 1px solid #b6d4fe !important;
        border-radius: 8px !important;
    }

    /* 4. Bold the Header Text */
    .streamlit-expanderHeader p {
        font-weight: bold !important;
    }

    /* 5. Force the Arrow to stay black */
    .streamlit-expanderHeader svg {
        fill: #000000 !important;
    }

    /* 6. Keep Metrics Blue */
    [data-testid="stMetricValue"] {
        color: #1c83e1 !important;
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
