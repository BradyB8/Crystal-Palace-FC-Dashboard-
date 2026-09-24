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
    "Crystal palace (10) (6).xlsx"
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

    attacking_df = pd.read_excel(FILE, sheet_name="Attacking")

    advanced_df = pd.read_excel(FILE, sheet_name="Efficiency stats")

    defending_df = pd.read_excel(FILE, sheet_name="Defending")

    general_df = pd.read_excel(FILE, sheet_name="General Play")

    tactical_df = pd.read_excel(FILE, sheet_name="Tactical Stats")

    preview_df = pd.read_excel(FILE, sheet_name="preview ")

except Exception as e:

    st.error(f"Excel Error: {e}")

    st.stop()


except Exception as e:
    st.error(f"Excel Error: {e}")
    st.stop()

# ==================================================
# TABS
# ==================================================

dashboard_tab, opponent_tab, comparison_tab, match_tab, advanced_tab, tactical_tab = st.tabs([
    "Dashboard",
    "Game Analysis",
    "Match Comparison",
    "Match Stats",
    "Efficiency Stats",
    "Tactical Stats"

])
# ==================================================
# DASHBOARD
# ==================================================

with dashboard_tab:

    st.header("Season Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Premier League",
            "16th"
        )

    with col2:
        st.metric(
            "Europa League",
            "2nd"
        )

    with col3:
        st.metric(
            "Next Opponent",
            "Nottingham Forest"
        )
        st.caption("Last meeting: Crystal Palace 1-1 Nottingham Forest")

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
    # MATCH COMPARISON
    # ==================================================

with comparison_tab:
    st.header("Crystal Palace Match Comparison")

    teams = attacking_df["Team"].dropna().unique()

    col1, col2 = st.columns(2)

    with col1:
        match1 = st.selectbox(
            "Match 1",
            teams,
            key="comparison_match1"
        )

    with col2:
        match2 = st.selectbox(
            "Match 2",
            teams,
            key="comparison_match2"
        )

    # ==========================================
    # TEAM / AGAINST STATS
    # ==========================================

    stat_view = st.radio(
        "Stat Type",
        [
            "Team Stats",
            "Against Stats"
        ],
        horizontal=True
    )

    # ==========================================
    # CATEGORY
    # ==========================================

    category = st.selectbox(
        "Statistic Category",
        [
            "Attacking",
            "Defending",
            "General Play",
            "Efficiency Stats",
            "Tactical Stats"
        ]
    )

    # ==========================================
    # DATAFRAME
    # ==========================================

    if category == "Attacking":
        selected_df = attacking_df

    elif category == "Defending":
        selected_df = defending_df

    elif category == "General Play":
        selected_df = general_df

    elif category == "Efficiency Stats":
        selected_df = advanced_df

    else:
        selected_df = tactical_df

    # ==========================================
    # MATCH ROWS
    # ==========================================

    row1 = selected_df[
        selected_df.iloc[:, 0].astype(str) == match1
        ]

    row2 = selected_df[
        selected_df.iloc[:, 0].astype(str) == match2
        ]

    if row1.empty or row2.empty:

        st.error("Match not found.")

    else:

        row1 = row1.iloc[0]
        row2 = row2.iloc[0]

        st.markdown(
            f"## {match1} vs {match2}"
        )

        # ==========================================
        # AVAILABLE STATS
        # ==========================================

        all_stats = selected_df.select_dtypes(
            include="number"
        ).columns.tolist()

        if stat_view == "Team Stats":

            stats = [
                col
                for col in all_stats
                if "/A" not in col
            ]

        else:

            stats = [
                col
                for col in all_stats
                if "/A" in col
            ]

        selected_stats = st.multiselect(
            "Choose Statistics",
            stats,
            default=stats[:10] if len(stats) > 10 else stats
        )

        # ==========================================
        # BUILD CHART DATA
        # ==========================================

        comparison_data = []

        match1_wins = 0
        match2_wins = 0

        for stat in selected_stats:

            try:

                val1 = float(row1[stat])
                val2 = float(row2[stat])

                comparison_data.append({
                    "Statistic": stat,
                    "Match": match1,
                    "Value": val1
                })

                comparison_data.append({
                    "Statistic": stat,
                    "Match": match2,
                    "Value": val2
                })

                if val1 > val2:
                    match1_wins += 1

                elif val2 > val1:
                    match2_wins += 1

            except:
                pass

        comparison_df = pd.DataFrame(
            comparison_data
        )

        # ==========================================
        # LARGE COMPARISON CHART
        # ==========================================

        if not comparison_df.empty:
            fig = go.Figure()

            match1_df = comparison_df[
                comparison_df["Match"] == match1
                ]

            match2_df = comparison_df[
                comparison_df["Match"] == match2
                ]

            fig.add_trace(
                go.Bar(
                    y=match1_df["Statistic"],
                    x=match1_df["Value"],
                    name=match1,
                    orientation="h",
                    marker_color="#E41B23",
                    text=match1_df["Value"].round(2),
                    textposition="outside"
                )
            )

            fig.add_trace(
                go.Bar(
                    y=match2_df["Statistic"],
                    x=match2_df["Value"],
                    name=match2,
                    orientation="h",
                    marker_color="#1E90FF",
                    text=match2_df["Value"].round(2),
                    textposition="outside"
                )
            )

            fig.update_layout(
                title=f"{match1} vs {match2}",
                barmode="group",
                height=max(
                    600,
                    len(selected_stats) * 50
                ),
                paper_bgcolor="#07142B",
                plot_bgcolor="#07142B",
                font_color="white",
                legend_title="",
                xaxis_title="Value",
                yaxis_title="",
                yaxis=dict(
                    autorange="reversed"
                ),
                margin=dict(
                    l=20,
                    r=80,
                    t=60,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ==========================================
        # OVERALL RESULT
        # ==========================================

        st.markdown("---")

        st.subheader("Overall Comparison")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                match1,
                match1_wins
            )

        with c2:
            st.metric(
                match2,
                match2_wins
            )

        total_stats = match1_wins + match2_wins

        if match1_wins > match2_wins:

            st.success(
                f"🏆 {match1} won "
                f"{match1_wins} of {total_stats} stats"
            )

        elif match2_wins > match1_wins:

            st.success(
                f"🏆 {match2} won "
                f"{match2_wins} of {total_stats} stats"
            )

        else:

            st.info(
                f"Level comparison ({match1_wins}-{match2_wins})"
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
        # TACTICAL STATS
        # ==================================================

        with tactical_tab:

            st.header("Tactical Analysis")

            tactical_display = tactical_df.copy()

            percent_cols = [
                col for col in tactical_display.columns
                if col != "Team"
            ]

            for col in percent_cols:
                tactical_display[col] = (
                        tactical_display[col]
                        .astype(float)
                        .mul(100)
                        .round(1)
                        .astype(str)
                        + "%"
                )

            st.dataframe(
                tactical_display,
                use_container_width=True,
                height=600
            )

            selected_team = st.selectbox(
                "Select Team",
                tactical_df["Team"]
            )

            team_data = tactical_df[
                tactical_df["Team"] == selected_team
                ].iloc[0]

            attack_labels = [
                "Right",
                "Middle",
                "Left"
            ]

            attack_values = [
                team_data["% of attacks from the right "] * 100,
                team_data["% of attacks from the middle"] * 100,
                team_data["% of attacks from the left"] * 100
            ]

            fig = px.pie(
                values=attack_values,
                names=attack_labels,
                title=f"{selected_team} Attack Direction"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            shot_values = [
                team_data["% of shots from the right "] * 100,
                team_data["% of shots from the middle "] * 100,
                team_data["% of shots from the left"] * 100
            ]

            fig2 = px.pie(
                values=shot_values,
                names=attack_labels,
                title=f"{selected_team} Shot Location Distribution"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )
# ==================================================
# OPPONENT ANALYSIS
# ==================================================
        with opponent_tab:

            st.header("Game Analysis")

            team_stats_tab, against_stats_tab = st.tabs([
                "Team Stats",
                "Against Stats"
            ])

            # ==========================================
            # TEAM STATS TAB
            # ==========================================

            with team_stats_tab:

                opponent_column = attacking_df.columns[0]

                selected_team = st.selectbox(
                    "Select Opponent",
                    attacking_df[opponent_column]
                    .astype(str)
                    .unique()
                )

                st.subheader(f"Statistics vs {selected_team}")

                # ==========================================
                # MATCH PREVIEW
                # ==========================================

                preview_match = preview_df[
                    preview_df.iloc[:, 0].astype(str).str.strip() == selected_team.strip()
                    ]

                if not preview_match.empty:

                    preview_row = preview_match.iloc[0]

                    st.markdown("### Match Preview")

                    # Formations side-by-side
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(
                            f"**Crystal Palace Formation:** {preview_row['Formation']}"
                        )

                    with col2:
                        st.markdown(
                            f"**{selected_team} Formation:** {preview_row['Formation/A']}"
                        )

                    st.markdown("#### What Went Right")

                    right_items = [
                        item.strip()
                        for item in str(
                            preview_row["What Went right "]
                        ).split(",")
                        if item.strip()
                    ]

                    for item in right_items:
                        st.markdown(f"• {item}")

                    st.markdown("#### What Went Wrong")

                    wrong_items = [
                        item.strip()
                        for item in str(
                            preview_row["What went wrong "]
                        ).split(",")
                        if item.strip()
                    ]

                    for item in wrong_items:
                        st.markdown(f"• {item}")

                    st.markdown("---")



                attacking_match = attacking_df[
                    attacking_df[opponent_column]
                    .astype(str) == selected_team
                    ]

                st.write("### Attacking")

                attacking_team = attacking_match[
                    [c for c in attacking_match.columns if "/A" not in c]
                ]

                st.dataframe(
                    attacking_team,
                    use_container_width=True
                )
                defending_match = defending_df[
                    defending_df.iloc[:, 0]
                    .astype(str) == selected_team
                    ]

                if not defending_match.empty:
                    st.write("### Defending")

                    defending_team = defending_match[
                        [c for c in defending_match.columns if "/A" not in c]
                    ]

                    st.dataframe(
                        defending_team,
                        use_container_width=True
                    )

                general_match = general_df[
                    general_df.iloc[:, 0]
                    .astype(str) == selected_team
                    ]

                if not general_match.empty:
                    st.write("### General Play")

                    general_team = general_match[
                        [c for c in general_match.columns if "/A" not in c]
                    ]

                    st.dataframe(
                        general_team,
                        use_container_width=True
                    )
                advanced_match = advanced_df[
                    advanced_df.iloc[:, 0]
                    .astype(str) == selected_team
                    ]

                if not advanced_match.empty:

                    st.write("### Efficiency Stats")

                    advanced_display = advanced_match[
                        [c for c in advanced_match.columns if "/A" not in c]
                    ].copy()

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
                        use_container_width=True
                    )

                tactical_match = tactical_df[
                    tactical_df.iloc[:, 0]
                    .astype(str) == selected_team
                    ]

                if not tactical_match.empty:

                    st.write("### Tactical Stats")

                    tactical_display = tactical_match[
                        [c for c in tactical_match.columns if "/A" not in c]
                    ].copy()

                    for col in tactical_display.columns:

                        if col != "Team":
                            tactical_display[col] = (
                                    pd.to_numeric(
                                        tactical_display[col],
                                        errors="coerce"
                                    )
                                    .mul(100)
                                    .round(1)
                                    .astype(str)
                                    + "%"
                            )

                    st.dataframe(
                        tactical_display,
                        use_container_width=True
                    )




                radar_metrics = [
                    ("shots ", "shots/A"),
                    ("shots on goal", "shots on goal/A"),
                    ("shots in box", "shots in box/A"),
                    ("XG", "XG/A"),
                    ("goals ", "Goals/A")
                ]

                labels = []
                palace_values = []
                opponent_values = []

                for palace_stat, opponent_stat in radar_metrics:

                    try:

                        if (
                                palace_stat in attacking_match.columns
                                and opponent_stat in attacking_match.columns
                        ):
                            labels.append(palace_stat)

                            palace_values.append(
                                float(
                                    attacking_match[
                                        palace_stat
                                    ].iloc[0]
                                )
                            )

                            opponent_values.append(
                                float(
                                    attacking_match[
                                        opponent_stat
                                    ].iloc[0]
                                )
                            )

                    except:
                        pass

                if labels:
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
                            )
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
                            )
                        )
                    )

                    fig.update_layout(
                        template="plotly_dark",
                        height=700,
                        title=f"Crystal Palace vs {selected_team}"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # ==========================================
            # AGAINST STATS TAB
            # ==========================================

            with against_stats_tab:

                selected_team_against = st.selectbox(
                    "Select Opponent",
                    attacking_df["Team"].astype(str).unique(),
                    key="against_select"
                )


                def against_only(df, team):
                    row = df[
                        df.iloc[:, 0]
                        .astype(str) == team
                        ]

                    cols = [
                        c for c in df.columns
                        if "/A" in c
                           or c == df.columns[0]
                    ]

                    return row[cols]


                st.write("### Attacking Against")

                st.dataframe(
                    against_only(
                        attacking_df,
                        selected_team_against
                    ),
                    use_container_width=True
                )

                st.write("### Defending Against")

                st.dataframe(
                    against_only(
                        defending_df,
                        selected_team_against
                    ),
                    use_container_width=True
                )

                st.write("### General Play Against")

                st.dataframe(
                    against_only(
                        general_df,
                        selected_team_against
                    ),
                    use_container_width=True
                )

                st.write("### Efficiency Stats Against")

                advanced_against = against_only(
                    advanced_df,
                    selected_team_against
                ).copy()

                for col in advanced_against.columns[1:]:
                    advanced_against[col] = (
                            pd.to_numeric(
                                advanced_against[col],
                                errors="coerce"
                            )
                            .mul(100)
                            .round(0)
                            .astype("Int64")
                            .astype(str)
                            + "%"
                    )

                st.dataframe(
                    advanced_against,
                    use_container_width=True
                )

            st.write("### Tactical Against")

            tactical_against = against_only(
                tactical_df,
                selected_team_against
            ).copy()

            for col in tactical_against.columns[1:]:
                tactical_against[col] = (
                        pd.to_numeric(
                            tactical_against[col],
                            errors="coerce"
                        )
                        .mul(100)
                        .round(0)
                        .astype("Int64")
                        .astype(str)
                        + "%"
                )

            st.dataframe(
                tactical_against,
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
