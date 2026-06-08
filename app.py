# ========================
# IMPORT LIBRARIES
# ========================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ===========================
# PAGE CONFIG
# ===========================

st.set_page_config(
    page_title="Employee Attrition Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# GLOBAL STYLES
# ================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Root & Page ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.main {
    background-color: #0d1117;
}
.block-container {
    padding: 2rem 2.5rem 3rem 2.5rem;
    max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stMultiSelect label {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #8b949e !important;
}

/* ── Page title area ── */
h1 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.85rem !important;
    font-weight: 700 !important;
    color: #f0f6fc !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0 !important;
}
h2, h3 {
    font-family: 'DM Sans', sans-serif !important;
    color: #f0f6fc !important;
}
p, li {
    color: #8b949e;
}

/* ── KPI Cards ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.4rem 1.6rem !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: border-color 0.2s;
}
[data-testid="metric-container"]:hover {
    border-color: #388bfd;
}
[data-testid="metric-container"] label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #8b949e !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #f0f6fc !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Divider ── */
hr {
    border: none;
    border-top: 1px solid #21262d;
    margin: 1.5rem 0;
}

/* ── Section subheader ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #388bfd;
    margin-bottom: 0.3rem;
    margin-top: 1.5rem;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f0f6fc;
    margin-bottom: 0.15rem;
}
.section-desc {
    font-size: 0.83rem;
    color: #8b949e;
    margin-bottom: 1.2rem;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background-color: #161b22;
    border: 1px solid #21262d !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem;
    overflow: hidden;
}
[data-testid="stExpander"]:hover {
    border-color: #388bfd !important;
}
[data-testid="stExpander"] summary {
    padding: 1rem 1.4rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: #f0f6fc !important;
    background-color: #161b22 !important;
}
[data-testid="stExpander"] summary:hover {
    background-color: #1c2128 !important;
}
[data-testid="stExpander"] > div > div {
    padding: 0 1rem 1rem 1rem;
    background-color: #0d1117;
}

/* ── Insight box ── */
.insight-box {
    background: linear-gradient(135deg, #0d2137 0%, #0d1b2a 100%);
    border: 1px solid #1f3a5f;
    border-left: 3px solid #388bfd;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-top: 2px;
    margin-bottom: 6px;
    font-size: 0.8rem;
    color: #8b949e;
    line-height: 1.65;
    font-family: 'DM Sans', sans-serif;
}
.insight-box strong {
    color: #c9d1d9;
    font-weight: 600;
}
.insight-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #388bfd;
    margin-bottom: 4px;
    display: block;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #21262d;
    border-radius: 10px;
    overflow: hidden;
}

/* ── Sidebar title ── */
.sidebar-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #388bfd;
    padding: 0.5rem 0 0.75rem 0;
    border-bottom: 1px solid #21262d;
    margin-bottom: 1rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-size: 0.75rem;
    color: #484f58;
    padding: 1.5rem 0 0.5rem 0;
    letter-spacing: 0.03em;
}
</style>
""", unsafe_allow_html=True)

# ================================
# LOAD DATA
# ================================

@st.cache_data
def load_data():
    df = pd.read_csv("EDA DANIEL PRO.csv")
    df.columns = df.columns.str.strip().str.lower()
    df['status'] = df['left'].map({0: 'Stayed', 1: 'Left'})
    df['promoted']  = df['promotion_last_5years'].map({0: 'Not Promoted', 1: 'Promoted'})
    df['accident']  = df['work_accident'].map({0: 'No Accident', 1: 'Had Accident'})
    return df

df = load_data()

# ================================
# PLOTLY DARK THEME DEFAULTS
# ================================

PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#8b949e', size=11),
    title_font=dict(family='DM Sans', color='#c9d1d9', size=13, weight=600 if False else None),
    legend=dict(
        bgcolor='rgba(22,27,34,0.8)',
        bordercolor='#21262d',
        borderwidth=1,
        font=dict(color='#c9d1d9', size=10)
    ),
    xaxis=dict(
        gridcolor='#21262d',
        linecolor='#21262d',
        tickfont=dict(color='#8b949e', size=10),
        title_font=dict(color='#8b949e', size=11)
    ),
    yaxis=dict(
        gridcolor='#21262d',
        linecolor='#21262d',
        tickfont=dict(color='#8b949e', size=10),
        title_font=dict(color='#8b949e', size=11)
    ),
    margin=dict(l=16, r=16, t=44, b=16),
)

COLORS = {'Stayed': '#388bfd', 'Left': '#f85149'}
HEIGHT  = 360

# ================================
# SIDEBAR FILTERS
# ================================

with st.sidebar:
    st.markdown('<div class="sidebar-title">Dashboard Filters</div>', unsafe_allow_html=True)

    department_filter = st.multiselect(
        "Department",
        options=sorted(df['department'].unique()),
        default=sorted(df['department'].unique())
    )

    salary_filter = st.multiselect(
        "Salary Level",
        options=sorted(df['salary'].unique()),
        default=sorted(df['salary'].unique())
    )

    attrition_filter = st.selectbox(
        "Employee Status",
        options=["All", "Stayed", "Left"]
    )

    sat_min = float(df['satisfaction_level'].min())
    sat_max = float(df['satisfaction_level'].max())
    satisfaction_filter = st.slider(
        "Satisfaction Level",
        min_value=sat_min, max_value=sat_max,
        value=(sat_min, sat_max), step=0.01
    )

    tenure_filter = st.slider(
        "Years in Company",
        int(df['time_spend_company'].min()),
        int(df['time_spend_company'].max()),
        (int(df['time_spend_company'].min()), int(df['time_spend_company'].max()))
    )

# ================================
# FILTER DATA
# ================================

filtered_df = df.copy()
if department_filter:
    filtered_df = filtered_df[filtered_df['department'].isin(department_filter)]
if salary_filter:
    filtered_df = filtered_df[filtered_df['salary'].isin(salary_filter)]
filtered_df = filtered_df[filtered_df['satisfaction_level'].between(*satisfaction_filter)]
filtered_df = filtered_df[filtered_df['time_spend_company'].between(*tenure_filter)]
if attrition_filter == "Left":
    filtered_df = filtered_df[filtered_df['left'] == 1]
elif attrition_filter == "Stayed":
    filtered_df = filtered_df[filtered_df['left'] == 0]

# ================================
# HEADER
# ================================

st.markdown('<div class="section-label">Human Resources Intelligence</div>', unsafe_allow_html=True)
st.title("Employee Attrition Analytics")
st.markdown(
    '<p style="color:#8b949e; font-size:0.9rem; margin-top:0.25rem; margin-bottom:1.5rem;">'
    'Diagnostic insights into workforce behaviour, workload patterns, satisfaction drivers, '
    'and attrition risk across the organisation.'
    '</p>',
    unsafe_allow_html=True
)

# ================================
# KPI METRICS
# ================================

if len(filtered_df) > 0:
    total_employees = len(filtered_df)
    attrition_rate  = filtered_df['left'].mean() * 100
    avg_satisfaction= filtered_df['satisfaction_level'].mean()
    avg_hours       = filtered_df['average_montly_hours'].mean()
    stayed_pct      = (filtered_df['left'] == 0).mean() * 100
else:
    total_employees = attrition_rate = avg_satisfaction = avg_hours = stayed_pct = 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Employees",   f"{total_employees:,}")
k2.metric("Attrition Rate",    f"{attrition_rate:.1f}%")
k3.metric("Retention Rate",    f"{stayed_pct:.1f}%")
k4.metric("Avg Satisfaction",  f"{avg_satisfaction:.2f}")
k5.metric("Avg Monthly Hours", f"{avg_hours:.0f} hrs")

st.markdown("<hr>", unsafe_allow_html=True)

# ================================
# HELPERS
# ================================

def apply_theme(fig, height=HEIGHT, hide_yaxis=False):
    fig.update_layout(**PLOT_LAYOUT, height=height)
    if hide_yaxis:
        fig.update_yaxes(showgrid=False, visible=False)
    return fig

def insight(label, text):
    st.markdown(
        f'<div class="insight-box">'
        f'<span class="insight-label">📌 {label}</span>'
        f'{text}'
        f'</div>',
        unsafe_allow_html=True
    )

# ================================
# BUILD ALL FIGURES
# ================================

# ── Fig 1: Attrition Composition ──
attrition_data = filtered_df['status'].value_counts().reset_index()
attrition_data.columns = ['Status', 'Count']
fig1 = px.pie(
    attrition_data, names='Status', values='Count', hole=0.6,
    color='Status', color_discrete_map=COLORS
)
fig1.update_traces(
    textposition='inside', textinfo='percent+label',
    textfont=dict(color='white', size=11),
    marker=dict(line=dict(color='#0d1117', width=2))
)
fig1.update_layout(title='Attrition Composition', showlegend=True)
apply_theme(fig1, hide_yaxis=True)

# ── Fig 2: Salary vs Attrition ──
fig2 = px.histogram(
    filtered_df, x='salary', color='status', barmode='group', text_auto=True,
    color_discrete_map=COLORS,
    labels={'status': 'Status', 'salary': 'Salary Level'},
    category_orders={'salary': ['low', 'medium', 'high']}
)
fig2.update_traces(marker_line_width=0, textfont=dict(size=9, color='#8b949e'))
fig2.update_layout(title='Salary Level vs Attrition', bargap=0.25)
apply_theme(fig2)

# ── Fig 3: Satisfaction vs Attrition ──
fig3 = px.box(
    filtered_df, x='status', y='satisfaction_level', color='status',
    color_discrete_map=COLORS,
    labels={'status': 'Status', 'satisfaction_level': 'Satisfaction'}
)
fig3.update_traces(marker=dict(size=3, opacity=0.5), line=dict(width=1.5))
fig3.update_layout(title='Satisfaction vs Attrition', showlegend=False)
apply_theme(fig3)

# ── Fig 4: Tenure Distribution ──
fig4 = px.violin(
    filtered_df, x='status', y='time_spend_company', color='status', box=True,
    color_discrete_map=COLORS,
    labels={'status': 'Status', 'time_spend_company': 'Years at Company'}
)
fig4.update_traces(meanline_visible=True, line=dict(width=1.5))
fig4.update_layout(title='Tenure Distribution vs Attrition', showlegend=False)
apply_theme(fig4)

# ── Fig 5: Monthly Hours by Projects ──
line_data = (
    filtered_df
    .groupby(['number_project', 'status'])['average_montly_hours']
    .mean().reset_index()
    .rename(columns={'average_montly_hours': 'Avg Monthly Hours', 'number_project': 'Projects'})
)
fig5 = px.line(
    line_data, x='Projects', y='Avg Monthly Hours', color='status', markers=True,
    color_discrete_map=COLORS, labels={'status': 'Status'}
)
fig5.update_traces(line=dict(width=2.5), marker=dict(size=6))
fig5.update_layout(title='Monthly Hours by Project Count')
apply_theme(fig5)

# ── Fig 6: Performance Evaluation ──
fig6 = px.box(
    filtered_df, x='status', y='last_evaluation', color='status',
    color_discrete_map=COLORS,
    labels={'status': 'Status', 'last_evaluation': 'Evaluation Score'}
)
fig6.update_traces(marker=dict(size=3, opacity=0.5), line=dict(width=1.5))
fig6.update_layout(title='Performance Evaluation vs Attrition', showlegend=False)
apply_theme(fig6)

# ── Fig 7: Promotion Distribution ──
promo_data = filtered_df['promoted'].value_counts().reset_index()
promo_data.columns = ['Promotion Status', 'Count']
fig7 = px.pie(
    promo_data, names='Promotion Status', values='Count', hole=0.6,
    color_discrete_sequence=['#388bfd', '#e3b341']
)
fig7.update_traces(
    textposition='inside', textinfo='percent+label',
    textfont=dict(color='white', size=11),
    marker=dict(line=dict(color='#0d1117', width=2))
)
fig7.update_layout(title='Promotion Distribution')
apply_theme(fig7, hide_yaxis=True)

# ── Fig 8: Work Accident vs Attrition ──
fig8 = px.histogram(
    filtered_df, x='accident', color='status', barmode='stack',
    color_discrete_map=COLORS,
    labels={'accident': 'Accident History', 'status': 'Status'}
)
fig8.update_traces(marker_line_width=0)
fig8.update_layout(title='Work Accident vs Attrition', bargap=0.3)
apply_theme(fig8)

# ── Fig 9: Correlation Heatmap ──
numeric_df = filtered_df.select_dtypes(include=np.number)
corr = numeric_df.corr()
fig9 = go.Figure(go.Heatmap(
    z=corr.values,
    x=corr.columns, y=corr.columns,
    colorscale='RdBu', zmin=-1, zmax=1,
    text=corr.values.round(2), texttemplate='%{text}',
    textfont=dict(size=9),
    showscale=True,
    colorbar=dict(
        tickfont=dict(color='#8b949e', size=9),
        outlinewidth=0,
        bgcolor='rgba(0,0,0,0)'
    )
))
fig9.update_layout(title='Variable Correlation Matrix')
apply_theme(fig9, height=520)

# ── Fig 10: Turnover — Workload vs Projects ──
turnover_data = (
    filtered_df
    .groupby('number_project')
    .agg(
        Avg_Monthly_Hours=('average_montly_hours', 'mean'),
        Attrition_Rate=('left', lambda x: x.mean() * 100)
    )
    .reset_index()
    .rename(columns={'number_project': 'Number of Projects'})
)
fig10 = go.Figure()
fig10.add_trace(go.Scatter(
    x=turnover_data['Number of Projects'], y=turnover_data['Avg_Monthly_Hours'],
    mode='lines+markers', name='Avg Monthly Hours',
    line=dict(color='#388bfd', width=2.5), marker=dict(size=7)
))
fig10.add_trace(go.Scatter(
    x=turnover_data['Number of Projects'], y=turnover_data['Attrition_Rate'],
    mode='lines+markers', name='Attrition Rate (%)',
    line=dict(color='#f85149', width=2.5, dash='dash'),
    marker=dict(size=7), yaxis='y2'
))
fig10.update_layout(
    title='Workload vs Projects vs Attrition Rate',
    xaxis=dict(title='Number of Projects', gridcolor='#21262d', linecolor='#21262d',
               tickfont=dict(color='#8b949e'), title_font=dict(color='#8b949e')),
    yaxis=dict(title='Avg Monthly Hours', color='#388bfd',
               gridcolor='#21262d', linecolor='#21262d',
               tickfont=dict(color='#8b949e'), title_font=dict(color='#8b949e')),
    yaxis2=dict(title='Attrition Rate (%)', overlaying='y', side='right',
                color='#f85149', tickfont=dict(color='#8b949e'),
                title_font=dict(color='#8b949e')),
    legend=dict(bgcolor='rgba(22,27,34,0.8)', bordercolor='#21262d',
                borderwidth=1, font=dict(color='#c9d1d9', size=10)),
)
apply_theme(fig10, height=400)

# ================================
# SECTION: THREE EXPANDERS
# ================================

st.markdown('<div class="section-label">Diagnostic Charts</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Analysis Sections</div>', unsafe_allow_html=True)

# ── EXPANDER 1: Attrition ──────────────────────────────────────────────────
with st.expander("📊  Attrition", expanded=False):

    # Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(fig1, use_container_width=True)
        insight("What this shows",
            "<strong>~24% of employees left</strong> the organisation. This is above the healthy "
            "industry benchmark of 10–15%, signalling a systemic retention issue rather than "
            "isolated turnover. Every other chart in this dashboard helps explain the 'why'.")

    with c2:
        st.plotly_chart(fig2, use_container_width=True)
        insight("What this shows",
            "<strong>Low-salary employees leave at the highest rate.</strong> The gap between "
            "'Stayed' and 'Left' bars is widest at the low salary band — compensation "
            "dissatisfaction is a primary flight risk driver. Medium earners also churn but "
            "at a lower rate.")

    with c3:
        st.plotly_chart(fig3, use_container_width=True)
        insight("What this shows",
            "<strong>Leavers have a significantly lower median satisfaction.</strong> But notice "
            "the spread — some leavers had high satisfaction, pointing to a secondary group of "
            "high performers who left due to overwork or lack of growth, not pure dissatisfaction.")

    # Row 2
    c4, c5, c6 = st.columns(3)
    with c4:
        st.plotly_chart(fig4, use_container_width=True)
        insight("What this shows",
            "<strong>Mid-career employees (3–5 years) exit most.</strong> They have built enough "
            "skills and experience to become externally marketable, but haven't received "
            "promotions or recognition to make staying worthwhile — a classic retention gap.")

    with c5:
        st.plotly_chart(fig5, use_container_width=True)
        insight("What this shows",
            "<strong>Leavers consistently log more hours per project level.</strong> As project "
            "count grows, the working-hour gap between leavers and stayers widens sharply — "
            "a clear burnout signature. Overloaded employees are choosing to exit rather than "
            "endure unsustainable workloads.")

    with c6:
        st.plotly_chart(fig6, use_container_width=True)
        insight("What this shows",
            "<strong>High performers are leaving too.</strong> The evaluation scores of leavers "
            "are not significantly lower than stayers — many received strong reviews. This rules "
            "out poor performance as the driver; instead, growth ceilings and pay gaps are "
            "pushing out the organisation's best talent.")

    # Row 3
    c7, c8, _ = st.columns(3)
    with c7:
        st.plotly_chart(fig7, use_container_width=True)
        insight("What this shows",
            "<strong>Barely anyone has been promoted in 5 years.</strong> Over 94% of employees "
            "sit in the 'Not Promoted' slice. Career stagnation kills engagement — employees "
            "with no visible path forward disengage and eventually exit, regardless of "
            "other satisfaction factors.")

    with c8:
        st.plotly_chart(fig8, use_container_width=True)
        insight("What this shows",
            "<strong>Attrition is not safety-driven.</strong> Employees without accidents "
            "represent the vast majority of leavers, confirming that physical safety is not "
            "the concern. Organisational factors — pay, recognition, workload — are the "
            "dominant forces behind the turnover.")

# ── EXPANDER 2: Correlation Heatmap ───────────────────────────────────────
with st.expander("🔥  Correlation Heatmap", expanded=False):
    st.plotly_chart(fig9, use_container_width=True)
    insight("How to read this",
        "<strong>Red = strong positive correlation, Blue = strong negative correlation.</strong> "
        "Key signals: <strong>satisfaction_level</strong> has a meaningful negative correlation "
        "with 'left' — the less satisfied, the higher the exit probability. "
        "<strong>average_montly_hours</strong> and <strong>number_project</strong> both show "
        "positive correlations with attrition — overworked employees leave more. "
        "<strong>last_evaluation</strong> shows a weak or mixed relationship, reinforcing that "
        "strong performers are not immune to leaving.")

# ── EXPANDER 3: Turnover ──────────────────────────────────────────────────
with st.expander("📉  Turnover", expanded=False):
    st.plotly_chart(fig10, use_container_width=True)
    insight("What this shows",
        "<strong>Attrition follows a U-shaped curve across project count.</strong> Employees "
        "with very few projects leave due to disengagement; those with too many leave due to "
        "burnout. The attrition rate (red dashed) spikes at both extremes while monthly hours "
        "(blue) climb steeply with project count. <strong>The retention sweet spot is 3–4 "
        "projects</strong> — where workload is balanced and employees feel purposeful without "
        "being overwhelmed. HR should flag anyone outside this band as a high flight risk.")

st.markdown("<hr>", unsafe_allow_html=True)

# ================================
# DATA PREVIEW
# ================================

st.markdown('<div class="section-label">Raw Data</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Dataset Preview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-desc">Showing the first 20 records from the filtered dataset.</div>', unsafe_allow_html=True)

display_cols = [c for c in df.columns if c not in ['status', 'promoted', 'accident']]
st.dataframe(
    filtered_df[display_cols].head(20),
    use_container_width=True,
    hide_index=True
)

# ================================
# KEY INSIGHTS
# ================================

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Key Diagnostic Insights</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
<div style="background:#161b22; border:1px solid #21262d; border-radius:12px; padding:1.4rem 1.6rem; margin-bottom:1rem;">
<p style="font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#388bfd; margin:0 0 0.75rem 0;">Key Findings</p>
<ul style="color:#8b949e; font-size:0.84rem; line-height:1.8; margin:0; padding-left:1.2rem;">
<li>Employees with <strong style="color:#c9d1d9;">low satisfaction</strong> are significantly more likely to leave.</li>
<li><strong style="color:#c9d1d9;">High workload and excessive hours</strong> drive burnout and attrition.</li>
<li><strong style="color:#c9d1d9;">Low-salary employees</strong> demonstrate the highest turnover rates.</li>
<li><strong style="color:#c9d1d9;">Lack of promotion</strong> leads to disengagement and exit decisions.</li>
<li>Employees between <strong style="color:#c9d1d9;">3–5 years tenure</strong> are the highest flight risk group.</li>
<li>High performers are leaving — performance score alone does not predict retention.</li>
<li>Attrition peaks at both extremes of the project workload spectrum.</li>
</ul>
</div>
""", unsafe_allow_html=True)

with col_b:
    st.markdown("""
<div style="background:#161b22; border:1px solid #21262d; border-radius:12px; padding:1.4rem 1.6rem; margin-bottom:1rem;">
<p style="font-size:0.7rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#f85149; margin:0 0 0.75rem 0;">Recommendations</p>
<ul style="color:#8b949e; font-size:0.84rem; line-height:1.8; margin:0; padding-left:1.2rem;">
<li>Introduce <strong style="color:#c9d1d9;">structured compensation reviews</strong> for low and medium salary bands.</li>
<li>Implement <strong style="color:#c9d1d9;">workload monitoring</strong> — flag employees exceeding sustainable hour thresholds.</li>
<li>Create clear <strong style="color:#c9d1d9;">promotion and career development pathways</strong> to retain mid-tenure talent.</li>
<li>Run <strong style="color:#c9d1d9;">stay interviews</strong> with employees at the 3-year mark before attrition risk peaks.</li>
<li>Invest in <strong style="color:#c9d1d9;">recognition programmes</strong> for high performers to prevent silent attrition.</li>
<li>Review <strong style="color:#c9d1d9;">project allocation</strong> — target 3–4 projects per employee as the retention sweet spot.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ================================
# FOOTER
# ================================

st.markdown(
    '<div class="footer">Developed by <strong>Adeniran Daniel</strong> &nbsp;·&nbsp; '
    'Employee Attrition Diagnostic Analytics Project</div>',
    unsafe_allow_html=True
)