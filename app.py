# outfit_rewear_tracker/app.py
import streamlit as st
import pandas as pd

# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(page_title="Outfit Rewear Tracker", page_icon="👗", layout="centered")

# -----------------------------
# Custom styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F3E8FF;
    }

    .main-title {
        text-align: center;
        color: #5B3B73;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6E4B87;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .logo-wrap {
        display: flex;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .logo-circle {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        background-color: #E6D6F3;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        box-shadow: 0 4px 12px rgba(91, 59, 115, 0.18);
        border: 3px solid white;
    }

    .section-box {
        background-color: rgba(255, 255, 255, 0.55);
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 18px;
    }

    h2, h3 {
        color: #5B3B73 !important;
    }

    .recommendation-box {
        background-color: #ffffff;
        padding: 16px;
        border-radius: 14px;
        border-left: 6px solid #B57EDC;
        color: #4A335A;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# App logo + title
# -----------------------------
st.markdown('<div class="logo-wrap"><div class="logo-circle">👗</div></div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Outfit Rewear Tracker</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Track how often you rewear outfits and get fresh styling ideas.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Inputs
# -----------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Enter Your Outfit Details")

category = st.selectbox(
    "Choose an outfit category:",
    ["Casual", "School", "Work", "Going Out"]
)

wear_count = st.slider(
    "How many times have you worn this outfit in the last 3 weeks?",
    1, 10, 3
)

favorite_item = st.text_input(
    "What item do you wear the most?",
    "Black jeans"
)

colors = st.multiselect(
    "Choose the colors in your outfit:",
    ["Black", "White", "Blue", "Pink", "Beige", "Gray", "Green", "Purple"],
    default=["Black"]
)

show_recommendation = st.checkbox("Show styling recommendation", value=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Summary output
# -----------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Your Outfit Summary")
st.write(f"**Category:** {category}")
st.write(f"**Most-worn item:** {favorite_item}")
st.write(f"**Wear count:** {wear_count}")
st.write(f"**Colors:** {', '.join(colors) if colors else 'No colors selected'}")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Feedback based on wear count
# -----------------------------
if wear_count >= 7:
    st.warning("You wear this outfit a lot. Try switching one main piece to create a fresh look.")
elif wear_count >= 4:
    st.info("You wear this outfit fairly often. Small changes can help it feel new again.")
else:
    st.success("Nice variety — you are rotating your outfits well.")

# -----------------------------
# Recommendation logic
# -----------------------------
recommendation = ""

if category == "Casual":
    recommendation = "Try pairing your usual item with a different top, a light jacket, and sneakers for an easy refreshed casual look."
elif category == "School":
    recommendation = "Try layering with a cardigan or hoodie and switching to different shoes or accessories to change the vibe."
elif category == "Work":
    recommendation = "Try combining your outfit with trousers, a neutral blouse, and one polished accessory like a tote or loafers."
elif category == "Going Out":
    recommendation = "Try a new color combination or add one statement piece, like boots, jewelry, or a dressier jacket."

if "Black" in colors and len(colors) == 1:
    recommendation += " Since you mostly wear black, try adding one lighter accent color for contrast."

if wear_count >= 7:
    recommendation += " Because you wear this often, changing either the top, shoes, or outer layer would make the biggest difference."

# -----------------------------
# Recommendation output
# -----------------------------
if show_recommendation:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Recommendation")
    st.markdown(f'<div class="recommendation-box">{recommendation}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Outfit ideas table
# -----------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Suggested Outfit Ideas")

data = pd.DataFrame({
    "Outfit Idea": [
        "Black jeans + white top + denim jacket",
        "Beige pants + sweater + boots",
        "Skirt + blouse + flats",
        "Wide-leg pants + blazer + loafers"
    ],
    "Style": ["Casual", "School", "Going Out", "Work"]
})

filtered_data = data[data["Style"] == category]
st.dataframe(filtered_data, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.caption("Fashion tip: Rewearing is great — styling the same pieces in new ways keeps your wardrobe feeling fresh.")