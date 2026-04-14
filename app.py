# Outfit Rewear Tracker
# A Streamlit app to help you track what you wear, upload outfit photos, manage your closet, and get outfit suggestions based on items you already own.

# Outfit Rewear Tracker
# A Streamlit app to help you track what you wear, upload outfit photos,
# manage your closet, and get outfit suggestions based on items you already own.

import os
import uuid
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Outfit Rewear Tracker", layout="wide")

# -----------------------------
# File paths
# -----------------------------
CLOSET_CSV = "closet.csv"
OUTFIT_LOG_CSV = "outfit_log.csv"
CLOSET_IMAGE_FOLDER = "closet_images"
OUTFIT_IMAGE_FOLDER = "outfit_images"

os.makedirs(CLOSET_IMAGE_FOLDER, exist_ok=True)
os.makedirs(OUTFIT_IMAGE_FOLDER, exist_ok=True)

# -----------------------------
# Custom styling
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f3ecfb;
    }

    .main-title {
        color: #7b4bb7;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #5f5f5f;
        font-size: 18px;
        margin-bottom: 20px;
    }

    .section-box {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# CSV helpers
# -----------------------------
def load_csv_data():
    """Load closet and outfit log from CSV files into session state."""
    if os.path.exists(CLOSET_CSV):
        closet_df = pd.read_csv(CLOSET_CSV)
        st.session_state.closet = closet_df.fillna("").to_dict(orient="records")
    else:
        st.session_state.closet = []

    if os.path.exists(OUTFIT_LOG_CSV):
        outfit_df = pd.read_csv(OUTFIT_LOG_CSV)
        st.session_state.outfit_log = outfit_df.fillna("").to_dict(orient="records")
    else:
        st.session_state.outfit_log = []


def save_closet_to_csv():
    """Save closet session state to CSV."""
    closet_df = pd.DataFrame(st.session_state.closet)
    closet_df.to_csv(CLOSET_CSV, index=False)


def save_outfit_log_to_csv():
    """Save outfit log session state to CSV."""
    outfit_df = pd.DataFrame(st.session_state.outfit_log)
    outfit_df.to_csv(OUTFIT_LOG_CSV, index=False)


def save_uploaded_file(uploaded_file, folder_name):
    """Save an uploaded file to disk and return the saved path."""
    if uploaded_file is None:
        return ""

    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(folder_name, unique_filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


# -----------------------------
# Session state
# -----------------------------
if "closet" not in st.session_state:
    st.session_state.closet = []

if "outfit_log" not in st.session_state:
    st.session_state.outfit_log = []

if "data_loaded" not in st.session_state:
    load_csv_data()
    st.session_state.data_loaded = True

# -----------------------------
# Helper functions
# -----------------------------
def add_closet_item(name, category, color, season, image):
    image_path = save_uploaded_file(image, CLOSET_IMAGE_FOLDER)

    st.session_state.closet.append(
        {
            "name": name,
            "category": category,
            "color": color,
            "season": season,
            "image": image_path,
        }
    )
    save_closet_to_csv()


def delete_closet_item(item_name):
    item_to_remove = None
    for item in st.session_state.closet:
        if item["name"] == item_name:
            item_to_remove = item
            break

    if item_to_remove is not None:
        image_path = item_to_remove.get("image", "")
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass

    st.session_state.closet = [
        item for item in st.session_state.closet if item["name"] != item_name
    ]
    save_closet_to_csv()


def log_outfit(log_date, top, bottom, shoes, occasion, rating, image):
    image_path = save_uploaded_file(image, OUTFIT_IMAGE_FOLDER)
    outfit_name = f"{top} + {bottom} + {shoes}"

    st.session_state.outfit_log.append(
        {
            "date": str(log_date),
            "outfit_name": outfit_name,
            "top": top,
            "bottom": bottom,
            "shoes": shoes,
            "occasion": occasion,
            "rating": rating,
            "image": image_path,
        }
    )
    save_outfit_log_to_csv()


def get_outfit_dataframe():
    if not st.session_state.outfit_log:
        return pd.DataFrame(
            columns=["date", "outfit_name", "top", "bottom", "shoes", "occasion", "rating", "image"]
        )

    df = pd.DataFrame(st.session_state.outfit_log)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date", ascending=False)


def get_closet_dataframe():
    if not st.session_state.closet:
        return pd.DataFrame(columns=["name", "category", "color", "season", "image"])

    return pd.DataFrame(st.session_state.closet)


def recommend_outfits(season_filter=None):
    closet_df = get_closet_dataframe()
    outfit_df = get_outfit_dataframe()

    if closet_df.empty:
        return []

    tops = closet_df[closet_df["category"] == "Top"]["name"].tolist()
    bottoms = closet_df[closet_df["category"] == "Bottom"]["name"].tolist()
    shoes = closet_df[closet_df["category"] == "Shoes"]["name"].tolist()

    if season_filter:
        filtered_tops = closet_df[
            (closet_df["category"] == "Top") &
            ((closet_df["season"] == season_filter) | (closet_df["season"] == "All"))
        ]["name"].tolist()

        filtered_bottoms = closet_df[
            (closet_df["category"] == "Bottom") &
            ((closet_df["season"] == season_filter) | (closet_df["season"] == "All"))
        ]["name"].tolist()

        filtered_shoes = closet_df[
            (closet_df["category"] == "Shoes") &
            ((closet_df["season"] == season_filter) | (closet_df["season"] == "All"))
        ]["name"].tolist()

        if filtered_tops:
            tops = filtered_tops
        if filtered_bottoms:
            bottoms = filtered_bottoms
        if filtered_shoes:
            shoes = filtered_shoes

    suggestions = []

    for top in tops[:6]:
        for bottom in bottoms[:6]:
            for shoe in shoes[:6]:
                combo = f"{top} + {bottom} + {shoe}"
                times_worn = 0
                if not outfit_df.empty:
                    times_worn = (outfit_df["outfit_name"] == combo).sum()

                suggestions.append(
                    {
                        "outfit": combo,
                        "times_worn": times_worn
                    }
                )

    suggestions = sorted(suggestions, key=lambda x: x["times_worn"])
    return suggestions[:5]

# -----------------------------
# Header
# -----------------------------
col1, col2 = st.columns([1, 6])

with col1:
    try:
        st.image("dress_logo.png", width=110)
    except Exception:
        st.write("👗")

with col2:
    st.markdown('<div class="main-title">Outfit Rewear Tracker</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Track your outfits, upload your closet, and get recommendations from clothes you already own.</div>',
        unsafe_allow_html=True
    )

# -----------------------------
# Sidebar
# -----------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Add Closet Item",
        "Closet Overview",
        "Log Daily Outfit",
        "Outfit History",
        "Recommendations"
    ]
)

# -----------------------------
# Home
# -----------------------------
if page == "Home":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.header("Welcome to the app")
    st.write(
        """
        This app helps you track what you wear and make better use of your closet.

        **Where to find everything:**
        - **Add Closet Item**: add clothes, shoes, and upload pictures of them
        - **Closet Overview**: see all your closet items and delete items
        - **Log Daily Outfit**: record what you wore and upload a picture of your outfit
        - **Outfit History**: see how many times you wore outfits and on which dates
        - **Recommendations**: get outfit ideas from your own closet, especially items you wear less often
        """
    )

    st.subheader("Main features")
    st.write(
        """
        - Upload closet items with pictures
        - Upload daily outfit pictures
        - Track wear count
        - Track when you wore each outfit
        - Get outfit recommendations from your own closet
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Add Closet Item
# -----------------------------
elif page == "Add Closet Item":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.header("Add an item to your closet")

    with st.form("closet_form"):
        item_name = st.text_input("Item name")
        category = st.selectbox("Category", ["Top", "Bottom", "Shoes", "Jacket", "Accessory"])
        color = st.text_input("Color")
        season = st.selectbox("Season", ["All", "Spring", "Summer", "Fall", "Winter"])
        item_image = st.file_uploader("Upload a picture of the item", type=["png", "jpg", "jpeg"])
        submit_item = st.form_submit_button("Add item")

    if submit_item:
        if item_name.strip():
            add_closet_item(item_name, category, color, season, item_image)
            st.success(f"{item_name} added to your closet.")
        else:
            st.warning("Please enter an item name.")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Closet Overview
# -----------------------------
elif page == "Closet Overview":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.header("Your closet")

    closet_df = get_closet_dataframe()

    if closet_df.empty:
        st.info("Your closet is empty. Add some items first.")
    else:
        st.dataframe(
            closet_df[["name", "category", "color", "season"]],
            use_container_width=True
        )

        st.subheader("Delete an item")
        item_to_delete = st.selectbox("Select an item to delete", closet_df["name"].tolist())
        if st.button("Delete selected item"):
            delete_closet_item(item_to_delete)
            st.success(f"{item_to_delete} was deleted.")
            st.rerun()

        st.subheader("Closet items")
        cols = st.columns(3)

        for i, item in enumerate(st.session_state.closet):
            with cols[i % 3]:
                st.markdown(f"**{item['name']}**")
                st.write(f"Category: {item['category']}")
                st.write(f"Color: {item['color']}")
                st.write(f"Season: {item['season']}")
                if item.get("image", ""):
                    st.image(item["image"], use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Log Daily Outfit
# -----------------------------
elif page == "Log Daily Outfit":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.header("Log your outfit of the day")

    closet_df = get_closet_dataframe()

    tops = closet_df[closet_df["category"] == "Top"]["name"].tolist()
    bottoms = closet_df[closet_df["category"] == "Bottom"]["name"].tolist()
    shoes_list = closet_df[closet_df["category"] == "Shoes"]["name"].tolist()

    if not tops or not bottoms or not shoes_list:
        st.warning("Please add at least one top, one bottom, and one pair of shoes first.")
    else:
        with st.form("outfit_form"):
            outfit_date = st.date_input("Date", value=date.today())
            top_choice = st.selectbox("Top", tops)
            bottom_choice = st.selectbox("Bottom", bottoms)
            shoes_choice = st.selectbox("Shoes", shoes_list)
            occasion = st.selectbox("Occasion", ["Casual", "School", "Work", "Party", "Formal"])
            rating = st.slider("How much did you like this outfit?", 1, 10, 7)
            outfit_image = st.file_uploader("Upload a picture of today's outfit", type=["png", "jpg", "jpeg"])
            submit_outfit = st.form_submit_button("Save outfit")

        if submit_outfit:
            log_outfit(outfit_date, top_choice, bottom_choice, shoes_choice, occasion, rating, outfit_image)
            st.success("Outfit logged successfully.")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Outfit History
# -----------------------------
elif page == "Outfit History":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.header("Outfit history")

    df = get_outfit_dataframe()

    if df.empty:
        st.info("No outfits logged yet.")
    else:
        st.subheader("All logged outfits")
        show_df = df.copy()
        show_df["date"] = show_df["date"].dt.strftime("%Y-%m-%d")
        st.dataframe(
            show_df[["date", "outfit_name", "occasion", "rating"]],
            use_container_width=True
        )

        st.subheader("How many times each outfit was worn")
        wear_counts = df["outfit_name"].value_counts().reset_index()
        wear_counts.columns = ["Outfit", "Times Worn"]
        st.dataframe(wear_counts, use_container_width=True)

        chart_df = wear_counts.copy()
        chart_df["Display Outfit"] = chart_df["Outfit"].apply(
            lambda x: x if len(x) <= 45 else x[:45] + "..."
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(chart_df["Display Outfit"], chart_df["Times Worn"])
        ax.set_xlabel("Times Worn")
        ax.set_ylabel("Outfit")
        ax.set_title("How many times each outfit was worn")
        ax.set_xticks(range(0, int(chart_df["Times Worn"].max()) + 1))
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("When did I wear each outfit?")
        selected_outfit = st.selectbox(
            "Select an outfit to view wear dates",
            df["outfit_name"].unique()
        )

        selected_dates = df[df["outfit_name"] == selected_outfit][["date", "occasion", "rating"]].sort_values("date")
        selected_dates["date"] = selected_dates["date"].dt.strftime("%Y-%m-%d")
        st.dataframe(selected_dates, use_container_width=True)

        st.subheader("Outfit photos")
        for _, row in df.iterrows():
            st.markdown(f"**{row['outfit_name']}** on {row['date'].strftime('%Y-%m-%d')}")
            if row.get("image", ""):
                st.image(row["image"], width=250)
            else:
                st.write("No photo uploaded.")
            st.divider()

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Recommendations
# -----------------------------
elif page == "Recommendations":
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.header("Outfit recommendations")

    season_choice = st.selectbox("Choose season", ["All", "Spring", "Summer", "Fall", "Winter"])
    season_filter = None if season_choice == "All" else season_choice

    suggestions = recommend_outfits(season_filter=season_filter)

    if not suggestions:
        st.info("Add more closet items first to get recommendations.")
    else:
        st.subheader("Recommended outfits you have worn the least")
        for suggestion in suggestions:
            st.markdown(f"**{suggestion['outfit']}**")
            st.write(f"Times worn: {suggestion['times_worn']}")
            st.write("This recommendation is based on items from your own closet and lower wear frequency.")
            st.divider()

    st.markdown('</div>', unsafe_allow_html=True)