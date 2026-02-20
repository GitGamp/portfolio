"""
9-BOX TALENT CLASSIFICATION DASHBOARD
Visualization of promotion model outputs

Author: Tanya Gampert, PHR, CAPM
"""


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="9-Box Talent Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stAlert {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================


@st.cache_data
def load_data():
    ## Fix path issues for deployment!!
    # Get the directory where streamlit_app.py lives
    current_dir = Path(__file__).parent
    
    # Locate the CSV relative to that directory
    file_path = current_dir / "final_data.csv"
    
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found. Path checked: {file_path}")
        st.stop()

def get_box_color(box_category):
    """Return color based on 9-box category"""
    color_map = {
        'High Potential / High Performance': '#2ecc71',      # Green - Stars
        'High Potential / Moderate Performance': '#3498db',  # Blue - Development Ready
        'High Potential / Low Performance': '#f39c12',       # Orange - Emerging Talent
        'Moderate Potential / High Performance': '#16a085',  # Teal - Core Contributors
        'Moderate Potential / Moderate Performance': '#95a5a6', # Gray - Solid Performers
        'Moderate Potential / Low Performance': '#e67e22',   # Dark Orange - At Risk
        'Low Potential / High Performance': '#9b59b6',       # Purple - Technical Experts
        'Low Potential / Moderate Performance': '#7f8c8d',   # Dark Gray - Limited Growth
        'Low Potential / Low Performance': '#e74c3c'         # Red - Underperformers
    }
    return color_map.get(box_category, '#95a5a6')

def create_9box_grid(df_filtered):
    """Create 9-box heatmap grid using existing box_category column"""
    
    # Count existing categories
    category_counts = df_filtered['box_category'].value_counts()
    total = len(df_filtered)
    
    # Define grid structure (row = potential, col = performance)
    potential_levels = ['Low Potential', 'Moderate Potential', 'High Potential']
    performance_levels = ['Low Performance', 'Moderate Performance', 'High Performance']

    # Create grid data and annotations
    annotations = []
    z_values = []
    
    for i, potential in enumerate(potential_levels):
        row_z = []
        for j, performance in enumerate(performance_levels):
            category_name = f"{potential} / {performance}"
            count = category_counts.get(category_name, 0)
            pct = int((count / total * 100)) if total > 0 else 0
            
            # Create annotation text
            text = f"<b>{count:,}</b><br>({pct}%)<br><br>{potential} /<br>{performance}"
            
            annotations.append(dict(
                x=j, y=i, text=text, showarrow=False,
                font=dict(size=14, color='black')  # Increased font size
            ))
            
            # Color score based on grid position (top-right = best)
            color_score = i * 3 + j  # Inverts so top-right is highest
            row_z.append(color_score)
        
        z_values.append(row_z)
    
    # High/High = darkest green, Low/Low = darkest red
    colorscale = [
        [0.0, '#e74c3c'],   # Red (worst)
        [0.3, '#f39c12'],   # Orange
        [0.5, '#f1c40f'],   # Yellow
        [0.7, '#a9dfbf'],   # Light green
        [1.0, '#27ae60']    # Dark green (best)
    ]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=['Low Rating', 'Moderate Rating', 'High Rating'],
        y=potential_levels,
        colorscale=colorscale,
        showscale=False,
        hoverinfo='skip'
    ))
    
    # Add annotations
    for annotation in annotations:
        fig.add_annotation(annotation)
    
    # Update layout
    fig.update_layout(
        # title={'text': '9 Box Grid', 'x': 0.5, 'font': {'size': 18}},
        xaxis=dict(title='Performance Rating', tickfont=dict(size=14)),
        yaxis=dict(title='Potential Score', tickfont=dict(size=14)),
        height=500,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

def create_box_distribution(df_filtered):
    """Create bar chart with consistent colors and legend labels""" 
    
    box_counts = df_filtered['box_category'].value_counts().reset_index()
    box_counts.columns = ['Category', 'Count']
    
    # Use gradient colors consistent with 9-box grid
    color_map = {
        'High Potential / High Performance': '#27ae60',      # Dark green (best)
        'High Potential / Moderate Performance': '#a9dfbf',  # Light green
        'High Potential / Low Performance': '#f1c40f',       # Yellow
        'Moderate Potential / High Performance': '#a9dfbf',  # Light green
        'Moderate Potential / Moderate Performance': '#f39c12', # Orange
        'Moderate Potential / Low Performance': '#f39c12',   # Orange
        'Low Potential / High Performance': '#f1c40f',       # Yellow
        'Low Potential / Moderate Performance': '#f39c12',   # Orange
        'Low Potential / Low Performance': '#e74c3c'         # Red (worst)
    }
    
    # Short legend labels (Stars, etc.)
    legend_map = {
        'High Potential / High Performance': 'Consistent Stars',
        'High Potential / Moderate Performance': 'High Potential', 
        'High Potential / Low Performance': 'Potential Gems',
        'Moderate Potential / High Performance': 'High Performers',
        'Moderate Potential / Moderate Performance': 'Key Players',
        'Moderate Potential / Low Performance': 'Inconsistent Performers',
        'Low Potential / High Performance': 'Strong Performers',
        'Low Potential / Moderate Performance': 'Effective Employees', 
        'Low Potential / Low Performance': 'Under Performers'
    }
    
    box_counts['Color'] = box_counts['Category'].map(color_map)
    box_counts['Legend'] = box_counts['Category'].map(legend_map)
    
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=box_counts['Count'],
        y=box_counts['Category'],
        orientation='h',
        marker=dict(color=box_counts['Color']),
        text=box_counts['Count'],
        textposition='auto',
        showlegend=False,
    ))
    
    # Add legend text on right side
    max_count = box_counts['Count'].max()
    fig.add_trace(go.Scatter(
        x=[max_count * 1.15] * len(box_counts),  # Position further right
        y=box_counts['Category'],  # Use same y values as bars
        text=box_counts['Legend'],
        mode='text',
        textposition='middle left',
        showlegend=False,
        textfont=dict(size=14, color='#333')
    ))
        
    fig.update_layout(
        title='',
        xaxis_title='Number of Employees',
        yaxis_title='',
        height=500,
        showlegend=False,
        margin=dict(r=200),  # CHANGE THIS LINE
        xaxis=dict(
            title_font=dict(size=16, family='Arial Black'),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=14)
        )
    )
    
    fig.update_traces(hoverinfo='skip')
    return fig



# ============================================================
# MAIN APPLICATION
# ============================================================

def main():
    # Header
    st.markdown('<div class="main-header">9-Box Talent Classification Dashboard</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
**Interactive tool for exploring promotion model outputs and talent segmentation**

This dashboard visualizes the results of a logistic regression model that predicts 
promotion probability based on merit-based performance metrics. Employees are classified 
into a 9-box grid based on **Performance Rating** (x-axis) and **Promotion Potential** (y-axis).
""")

    # METHODOLOGY SECTION:
    st.markdown("---")
    st.markdown("### Methodology")
    st.markdown("""
**9-Box Classification:** Employees are positioned based on their performance ratings (1-5 scale) 
and model-predicted promotion potential scores. The grid identifies succession candidates, 
development priorities, and retention risks across nine distinct talent segments.

**Succession Planning Framework:** This tool enables data-driven succession decisions by 
highlighting high-potential talent, identifying skill gaps, and prioritizing development 
investments based on both current performance and future leadership potential.
""")

    st.markdown("---")

    st.markdown("### Business Impact")
    st.markdown("""
This dashboard enables HR leaders and executives to make data-driven succession planning decisions by:

**🎯 Identifying Leadership Gaps:** Quickly spot critical roles lacking ready successors and prioritize development investments where they matter most.

**📈 Optimizing Talent Development:** Focus coaching and training resources on high-potential employees who will deliver the greatest organizational impact.

**⚠️ Mitigating Succession Risk:** Proactively address potential leadership shortfalls before they become critical business disruptions.

**💡 Strategic Workforce Planning:** Use objective performance and potential data to build robust succession pipelines across all organizational levels.
""")

    st.markdown("---")
    
    # Load data
    df = load_data()
    
    # ============================================================
    # SIDEBAR FILTERS
    # ============================================================
    st.sidebar.header("Core Filters")
        
    # Promotion status filter
    st.sidebar.markdown("#### Promotion Status")
    promotion_status = st.sidebar.radio(
        'Select Promotion Status',
        ['All', 'Promoted', 'Not Promoted'],
        help='Filter by actual promotion outcome'
    )

    # Potential score range
    st.sidebar.markdown("#### Potential Score Range (model probabilities)")
    potential_range = st.sidebar.slider(
        'Select range',
        float(df['potential'].min()),
        float(df['potential'].max()),
        (float(df['potential'].min()), float(df['potential'].max())),
        step=0.01,
        help='Filter by model-predicted promotion potential'
    )

    # 9-Box Category filter
    st.sidebar.markdown("#### 9-Box Category")
    selected_boxes = st.sidebar.multiselect(
        'Categories:', 
        options=sorted(df['box_category'].unique().tolist()),
        default=[],
        help='Select one or more categories'
    )

    # Employee ID filter
    st.sidebar.header("Additional Filters")
    selected_ids = st.sidebar.multiselect(
        "Employee IDs:",
        options=sorted(df['employee_id'].unique()),
        default=[],
        help='Select one or more employee IDs'

    )

    # Manager ID filter
    selected_ids = st.sidebar.multiselect(
        "Manager IDs:",
        options=sorted(df['manager_id'].unique()),
        default=[],
        help='Select one or more manager IDs'

    )

    # Department filter
    departments = ['All'] + sorted(df['department'].unique().tolist())
    selected_dept = st.sidebar.selectbox(
        'Department',
        departments,
        help='Filter employees by department'
    )
    
    # Role level filter
    role_levels = ['All'] + sorted(df['role_level'].unique().tolist())
    selected_role = st.sidebar.selectbox(
        'Role Level',
        role_levels,
        help='Filter employees by organizational level'
    )
    
    # Education level filter
    education_levels = ['All'] + sorted(df['education_level'].unique().tolist())
    selected_edu = st.sidebar.selectbox(
        'Education Level',
        education_levels,
        help='Filter employees by education background'
    )
    
    st.sidebar.markdown("---")
    
    # Apply filters
    df_filtered = df.copy()
    
    if selected_dept != 'All':
        df_filtered = df_filtered[df_filtered['department'] == selected_dept]
    
    if selected_role != 'All':
        df_filtered = df_filtered[df_filtered['role_level'] == selected_role]
    
    if selected_edu != 'All':
        df_filtered = df_filtered[df_filtered['education_level'] == selected_edu]
    
    if promotion_status == 'Promoted':
        df_filtered = df_filtered[df_filtered['promoted'] == 1]
    elif promotion_status == 'Not Promoted':
        df_filtered = df_filtered[df_filtered['promoted'] == 0]
    
    df_filtered = df_filtered[
        (df_filtered['potential'] >= potential_range[0]) & 
        (df_filtered['potential'] <= potential_range[1])
    ]
    
    if selected_ids:
        df_filtered = df_filtered[df_filtered['employee_id'].isin(selected_ids)]

    if selected_ids:
        df_filtered = df_filtered[df_filtered['manager_id'].isin(selected_ids)]

    if selected_boxes:
        df_filtered = df_filtered[df_filtered['box_category'].isin(selected_boxes)]

    # ============================================================
    # SUMMARY METRICS
    # ============================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
        label="Total Employees",
        value=f"{len(df_filtered):,}"
        )
        st.caption(f"{len(df_filtered)/len(df)*100:.1f}% of Eligible EEs")

    with col2:
        promoted_count = df_filtered['promoted'].sum()
        st.metric(
            label="Actually Promoted",
            value=f"{promoted_count:,}"            
        )
        st.caption(f"{promoted_count/len(df)*100:.1f}% of Selected EEs")

    with col3:
        high_pot_count = df_filtered[df_filtered['box_category'].str.contains('High Potential')].shape[0]
        st.metric(
            label="High Potential Talent",
            value=f"{high_pot_count:,}"
        )
        st.caption(f"{high_pot_count/len(df_filtered)*100:.1f}% of Selected EEs")

    with col4:
        stars_count = df_filtered[df_filtered['box_category'] == 'High Potential / High Performance'].shape[0]
        st.metric(
            label="Stars (High/High)",
            value=f"{stars_count:,}"
        )
        st.caption(f"{stars_count/len(df_filtered)*100:.1f}% of Selected EEs")

    st.markdown("---")
    # ============================================================
    # VISUALIZATIONS
    # ============================================================
    
    if len(df_filtered) > 0:
        st.subheader("9-Box Grid")
        fig_grid = create_9box_grid(df_filtered)
        st.plotly_chart(fig_grid, use_container_width=True)
    
    # Distribution chart - full width
        st.subheader("9-Box Category Distribution")
        fig_dist = create_box_distribution(df_filtered)
        st.plotly_chart(fig_dist, use_container_width=True)

    # Salary Distribution Visualization
        st.subheader("Salary Distribution")
        if not df_filtered.empty and 'salary' in df_filtered.columns:
            fig_salary = px.box(df_filtered, x='salary', title="Salary Distribution", color_discrete_sequence=['#27ae60'])
            fig_salary.update_traces(hoverinfo='skip')
            st.plotly_chart(fig_salary, use_container_width=True)
        else:
            st.write("No salary data available for current filters.")

    
        # ============================================================
        # DETAILED DATA TABLE
        # ============================================================
        st.markdown("---")
        st.subheader("Detailed Employee Data")
        
        # Select columns to display
        display_cols = ['employee_id','promoted',
        'prediction_promoted',
        'manager_id',
        'department',
        'role_level',
        'education_level',
        'years_in_company',
        'years_in_role',
        'performance_rating',
        'awards',
        'kpis_count',
        'kpis_achieved_pct',
        'peer_review_score',
        'training_courses_completed',
        'certification_count',
        'mentorship_participation',
        'projects_delivered',
        'salary',
        'performance_intervention',
        'box_category',
        'potential']
        
        df_display = df_filtered[display_cols].copy()
        df_display['promoted'] = df_display['promoted'].map({0: 'No', 1: 'Yes'})
        df_display['prediction_promoted'] = df_display['prediction_promoted'].map({0: 'No', 1: 'Yes'})
        df_display = df_display.rename(columns={
            'employee_id': 'Employee ID',
            'manager_id' : 'Manager ID',
            'department': 'Department',
            'role_level': 'Role Level',
            'education_level': 'Education',
            'years_in_company' : 'Company Tenure',
            'years_in_role' : 'Role Tenure',
            'performance_rating': 'Performance',
            'potential': 'Potential Score',
            'awards': 'Awards',
            'kpis_count' : 'KPIs Ct',
            'kpis_achieved_pct': "KPIs Achieved",
            'peer_review_score' : 'Peer Score',
            'training_courses_completed' : 'Training Courses',
            'certification_count' : 'Certifications',
            'mentorship_participation' : 'Mentorship',
            'projects_delivered' : 'Projects',
            'salary': 'Salary',
            'box_category': '9-Box Category',
            'promoted': 'Actually Promoted',
            'prediction_promoted': 'Model Prediction'
        })
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        # ============================================================
        # EXPORT FUNCTIONALITY
        # ============================================================
        st.markdown("---")
        st.subheader("Export Data")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            # Export filtered data as CSV
            csv = df_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Filtered Data (CSV)",
                data=csv,
                file_name=f"9box_filtered_data_{selected_dept}_{selected_role}.csv",
                mime="text/csv",
                help="Download the currently filtered employee data"
            )
        
        with col_export2:
            # Export summary statistics
            summary_stats = df_filtered.groupby('box_category').agg({
                'employee_id': 'count',
                'promoted': 'sum',
                'potential': 'mean',
                'performance_rating': 'mean'
            }).reset_index()
            summary_stats.columns = ['Category', 'Count', 'Promoted', 'Avg Potential', 'Avg Performance']
            
            csv_summary = summary_stats.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Summary Stats (CSV)",
                data=csv_summary,
                file_name="9box_summary_statistics.csv",
                mime="text/csv",
                help="Download aggregated statistics by 9-box category"
            )
    
        
    
    # ============================================================
    # FOOTER
    # ============================================================
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 2rem 0;'>
        <p><strong>9-Box Talent Classification Dashboard</strong></p>
        <p>Built with Streamlit | Data powered by logistic regression model</p>
        <p>Author: Tanya Gampert, PHR, CAPM | MSDA Capstone Project</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# RUN APPLICATION
# ============================================================
if __name__ == "__main__":
    main()