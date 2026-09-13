import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Crystal Palace Analytics",
    page_icon="⚽",
    layout="wide"
)

# ==================================================
# CRYSTAL PALACE THEME
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #07142B;
}

h1, h2, h3 {
    color: white !important;
}

div[data-testid="metric-container"] {
    background-color: #12315C;
    border-left: 6px solid #E41B23;
    border-radius: 12px;
    padding: 10px;
}

button[data-baseweb="tab"] {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# EXCEL FILE LOCATION
# ==================================================

FILE = os.path.join(
    os.path.expanduser("~"),
    "Downloads",
    "Crystal palace (9).xlsx"
)

# ==================================================
# HEADER
# ==================================================

col1, col2 = st.columns([1, 5])

with col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/en/a/a2/Crystal_Palace_FC_logo_%282022%29.svg",
        width=100
    )

with col2:
    st.title("Crystal Palace Analytics Dashboard")

# ==================================================
# CHECK FILE EXISTS
# ==================================================

if not os.path.exists(FILE):
    st.error(f"Excel file not found at:\n{FILE}")
    st.stop()

# ==================================================
# LOAD SHEETS
# ==================================================

try:

    attacking_df = pd.read_excel(
        FILE,
        sheet_name="Attacking"
    )

    advanced_df = pd.read_excel(
        FILE,
        sheet_name="Efficiency stats"
    )

    defending_df = pd.read_excel(
        FILE,
        sheet_name="Defending"
    )

    general_df = pd.read_excel(
        FILE,
        sheet_name="General Play"
    )

except Exception as e:
    st.error(f"Excel Error: {e}")
    st.stop()

# ==================================================
# TABS
# ==================================================

dashboard_tab, match_tab, advanced_tab, opponent_tab = st.tabs([
    "Dashboard",
    "Match Stats",
    "Efficiency Stats",
    "Opponent Analysis"
])

# ==================================================
# DASHBOARD
# ==================================================

with dashboard_tab:

    st.header("Season Dashboard")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Record",
            "2-0-3"
        )

    with col2:
        st.metric(
            "Goals",
            9
        )

    with col3:
        st.metric(
            "xG",
            6.62
        )

    with col4:
        st.metric(
            "Goals Against",
            11
        )

    with col5:
        st.metric(
            "xG Against",
            9.74
        )

    st.markdown("---")

    numeric_cols = attacking_df.select_dtypes(
        include="number"
    ).columns.tolist()

    numeric_cols = [
        col for col in numeric_cols
        if "total" not in col.lower()
    ]

    selected_metric = st.selectbox(
        "Select Trend Metric",
        numeric_cols
    )

    chart_df = attacking_df[
        attacking_df["Team"] != "Totals"
    ]

    fig = px.line(
        chart_df,
        x="Team",
        y=selected_metric,
        markers=True,
        title=f"{selected_metric} Trend"
    )

    fig.update_traces(
        line_color="#E41B23"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# MATCH STATS
# ==================================================

with match_tab:

    st.header("Match Statistics")

    stat_type = st.selectbox(
        "Select Statistic Category",
        [
            "Attacking",
            "Defending",
            "General Play"
        ]
    )

    if stat_type == "Attacking":
        current_df = attacking_df

    elif stat_type == "Defending":
        current_df = defending_df

    else:
        current_df = general_df

    st.dataframe(
        current_df,
        height=700,
        use_container_width=True
    )

    numeric_cols = current_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if len(numeric_cols) > 0:

        selected_stat = st.selectbox(
            "Chart Statistic",
            numeric_cols
        )

        chart_df = current_df[
            current_df["Team"] != "Totals"
        ]

        fig = px.bar(
            chart_df,
            x="Team",
            y=selected_stat,
            color=selected_stat,
            title=f"{selected_stat} by Match"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==================================================
# ADVANCED STATS
# ==================================================

with advanced_tab:

    st.header("Efficiency Stats")

    advanced_display = advanced_df.copy()

    for col in advanced_display.columns:

        if col != "Team":

            advanced_display[col] = (
                advanced_display[col]
                .astype(float)
                .mul(100)
                .round(1)
                .astype(str)
                + "%"
            )

    st.dataframe(
        advanced_display,
        height=700,
        use_container_width=True
    )

    advanced_numeric = advanced_df.select_dtypes(
        include="number"
    ).columns.tolist()

    if len(advanced_numeric) > 0:

        selected_metric = st.selectbox(
            "Advanced Metric",
            advanced_numeric
        )

        chart_df = advanced_df.copy()

        chart_df[selected_metric] = (
            chart_df[selected_metric] * 100
        )

        fig = px.bar(
            chart_df,
            x="Team",
            y=selected_metric,
            color=selected_metric,
            title=f"{selected_metric} (%) by Match"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if len(advanced_numeric) >= 6:

        radar_metrics = advanced_numeric[:6]

        radar = go.Figure()

        radar.add_trace(
            go.Scatterpolar(
                r=[
                    advanced_df[col].mean() * 100
                    for col in radar_metrics
                ],
                theta=radar_metrics,
                fill="toself",
                name="Crystal Palace"
            )
        )

        radar.update_layout(
            title="Efficient Statistical Profile",
            polar=dict(
                radialaxis=dict(
                    visible=True
                )
            )
        )

        st.plotly_chart(
            radar,
            use_container_width=True
        )

# ==================================================
# OPPONENT ANALYSIS
# ==================================================

with opponent_tab:

    st.header("Opponent Analysis")

    opponent_column = attacking_df.columns[0]

    selected_team = st.selectbox(
        "Select Opponent",
        attacking_df[opponent_column]
        .astype(str)
        .unique()
    )

    st.subheader(f"Statistics vs {selected_team}")

    attacking_match = attacking_df[
        attacking_df[opponent_column]
        .astype(str)
        == selected_team
    ]

    st.write("### Attacking")

    st.dataframe(
        attacking_match,
        use_container_width=True
    )

    defending_match = defending_df[
        defending_df.iloc[:, 0]
        .astype(str)
        == selected_team
    ]

    if not defending_match.empty:

        st.write("### Defending")

        st.dataframe(
            defending_match,
            use_container_width=True
        )

    general_match = general_df[
        general_df.iloc[:, 0]
        .astype(str)
        == selected_team
    ]

    if not general_match.empty:

        st.write("### General Play")

        st.dataframe(
            general_match,
            use_container_width=True
        )

    advanced_match = advanced_df[
        advanced_df.iloc[:, 0]
        .astype(str)
        == selected_team
    ]

    if not advanced_match.empty:

        st.write("### Efficiency Stats")

        advanced_match_display = advanced_match.copy()

        for col in advanced_match_display.columns:

            if col != "Team":

                advanced_match_display[col] = (
                    advanced_match_display[col]
                    .astype(float)
                    .mul(100)
                    .round(1)
                    .astype(str)
                    + "%"
                )

        st.dataframe(
            advanced_match_display,
            use_container_width=True
        )

        # ==========================================
        # MATCH COMPARISON RADAR
        # Crystal Palace vs Opponent
        # ==========================================
        radar_metrics = [
            ("shots ", "shots/A", attacking_match),
            ("shots on goal", "shots on goal/A", attacking_match),
            ("shots in box", "shots in box/A", attacking_match),
            ("XG", "XG/A", attacking_match),
            ("goals ", "Goals/A", attacking_match)
        ]




        labels = []
        palace_values = []
        opponent_values = []

        for palace_stat, opponent_stat, source_df in radar_metrics:

            try:

                if (
                    palace_stat in source_df.columns
                    and opponent_stat in source_df.columns
                ):

                    labels.append(palace_stat)

                    palace_values.append(
                        float(
                            source_df[
                                palace_stat
                            ].iloc[0]
                        )
                    )

                    opponent_values.append(
                        float(
                            source_df[
                                opponent_stat
                            ].iloc[0]
                        )
                    )

            except:
                continue

        if len(labels) > 0:

            fig = go.Figure()

            fig.add_trace(
                go.Scatterpolar(
                    r=palace_values,
                    theta=labels,
                    fill="toself",
                    name="Crystal Palace",
                    line=dict(
                        color="#E41B23",
                        width=4
                    ),
                    fillcolor="rgba(228,27,35,0.30)"
                )
            )

            fig.add_trace(
                go.Scatterpolar(
                    r=opponent_values,
                    theta=labels,
                    fill="toself",
                    name=selected_team,
                    line=dict(
                        color="#1E90FF",
                        width=4
                    ),
                    fillcolor="rgba(30,144,255,0.30)"
                )
            )

            fig.update_layout(
                title=f"Crystal Palace vs {selected_team}",
                template="plotly_dark",
                paper_bgcolor="#07142B",
                plot_bgcolor="#07142B",
                font_color="white",
                height=750,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.05,
                    xanchor="center",
                    x=0.5
                ),
                polar=dict(
                    bgcolor="#07142B",
                    radialaxis=dict(
                        visible=True,
                        gridcolor="gray",
                        linecolor="gray"
                    ),
                    angularaxis=dict(
                        tickfont=dict(
                            color="white",
                            size=12
                        )
                    )
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
