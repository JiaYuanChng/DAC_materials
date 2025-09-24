import pandas as pd
import streamlit as st
import plotly.express as px

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="CO2 Capture Materials Explorer",
    page_icon="🔬",
    layout="wide"
)

st.title("Interactive CO2 Capture Materials Database")

# --- 2. Data Loading and Caching ---
@st.cache_data
def load_data(csv_path):
    """Loads data from CSV and sorts it by capacity."""
    df = pd.read_csv(csv_path)
    df_sorted = df.sort_values(by='capacity').reset_index(drop=True)
    return df_sorted

try:
    df = load_data('data.csv')
except FileNotFoundError:
    st.error("Error: `data.csv` not found. Please make sure the file is in the same directory.")
    st.stop()

# --- 3. Layout Definition ---
# Create two columns: one for the plot, one for the details
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Material Capacity")
    
    # --- 4. Interactive Plot ---
    fig = px.scatter(
        df,
        x=df.index,
        y='capacity',
        custom_data=['material'], # Pass material name for identification
        labels={'x': 'Material Index (sorted by capacity)', 'y': 'Capacity (mmol/g)'},
        height=600
    )
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Capacity: %{y}<extra></extra>"
    )
    
    # Use streamlit-plotly-events to capture clicks
    # This requires a separate library installation: pip install streamlit-plotly-events
    from streamlit_plotly_events import plotly_events

    # The key argument is essential for session state
    selected_points = plotly_events(fig, click_event=True, key="plot_click")

with col2:
    st.header("Material Details")
    
    # --- 5. Display Information on Click ---
    if selected_points:
        # Get the index of the clicked point
        point_index = selected_points[0]['pointNumber']
        material_info = df.iloc[point_index]
        
        st.subheader(material_info['material'])
        
        for key, value in material_info.items():
            if key != 'material':
                label = key.replace('_', ' ').capitalize()
                if key == 'doi':
                    st.markdown(f"**{label}:** [{value}](https://doi.org/{value})")
                else:
                    st.write(f"**{label}:** {value}")
    else:
        st.info("Click on a data point in the plot to see its details here.")
