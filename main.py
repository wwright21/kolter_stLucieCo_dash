import streamlit as st
import pandas as pd
import plotly.express as px

# set page configurations
st.set_page_config(
    page_title=f"Migration Explorer",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"  # 'collapsed' or 'expanded'
)

# whole page variables
county_var = "St. Lucie"
state_var = "Florida"
stateAbbrev_var = "FL"

# set the dashboard title
title_font_size = 30
title_margin_top = 0
title_margin_bottom = 0

# Dashboard title
st.markdown(
    f"""
    <div style='margin-top: {title_margin_top}px; margin-bottom: {title_margin_bottom}px;'>
        <span style='font-size: {title_font_size}px; font-weight: 700; color: #36454F;'>
            {county_var} County ({stateAbbrev_var}) Migration Dashboard
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
st.write('---')

st.write("")

col1, col2 = st.columns(2)

# Radio label
col1.markdown(
    """
    <div style='text-align: right; padding-top: 0px;'>
        <span style='font-size: 20px; font-style: italic; color: #36454F;'>
            Select migration variable:
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Radio buttons
dash_variable = col2.radio(
    "",
    ["People", "Dollars"],
    horizontal=True,
    label_visibility='collapsed'
)

dash_variable_dict = {
    "People": [
        "people_net",  # dataframe column
        ",.0f",       # y-axis formatting
        "%{y:,.0f}",  # hover label formatting
        1000          # y-axis dtick
    ],
    "Dollars": [
        "agi_net",
        "$~s",
        "%{y:$,.0f}",
        50000000
    ]
}

# read in data
df = pd.read_csv('Assets/migration_data.csv')
line_chart_data = df[df['migration_type'] == 'total']

# create fig object
fig = px.line(
    line_chart_data,
    x='year',
    y=dash_variable_dict[dash_variable][0],
    title=f'Net Migration of {dash_variable} into {county_var} County Since 2016',
    height=440,
)

# update fig layout
fig.update_layout(
    margin=dict(l=20, r=20, t=50, b=0),
    hovermode='x unified',
    hoverlabel=dict(
        font_size=16,
        bgcolor='#36454F',
        font_color='#fffaf6'
    ),
    title={
        'font': {
            'color': '#000',
            'weight': 'normal'
        },
        'x': 0.5,
        'y': 0.97,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis=dict(
        title='',
        tickfont=dict(
            size=16,
            color='#000'
        ),
        gridcolor='#000'
    ),
    yaxis=dict(
        title='',
        tickfont=dict(
            size=16,
            color='#000'
        ),
        tickformat=dash_variable_dict[dash_variable][1],
        dtick=dash_variable_dict[dash_variable][3]
    ),
    plot_bgcolor='#fffaf6',
    paper_bgcolor='#fffaf6'
)

# customize line trace
line_color = '#FF6F61'
fig.update_traces(
    hovertemplate=dash_variable_dict[dash_variable][2],
    mode='lines+markers',
    line=dict(
        color=line_color,
        width=3,
        dash='solid'
    ),
    marker=dict(
        size=8
    )
)

fig.update_xaxes(
    showline=True,
    linewidth=1,
    linecolor='#000'
)
fig.update_yaxes(
    showline=True,
    linewidth=1,
    linecolor='#000',
    showgrid=False
)

config = {'displayModeBar': False}
st.plotly_chart(
    fig,
    config=config,
    theme='streamlit',
    use_container_width=True
)

# KPI readout
var_KPI = line_chart_data[dash_variable_dict[dash_variable][0]].sum()

if dash_variable == 'People':
    kpi_formatter = ''
else:
    kpi_formatter = '$'

st.markdown(
    f"""
    <div style='margin-top: 5px; margin-bottom: 0px; text-align: center'>
        <span style='font-size: 16px; font-weight: 100; color: #36454F;'>
            Cumulative Total Since 2016: <b>{kpi_formatter}{var_KPI:,}</b>
            <br><i>Note: 2023 data scheduled for release in June 2025.</i>
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
st.write('---')

# Top metros KPIs
metro_rollup = df.groupby('aux_GeoRollup')[
    dash_variable_dict[dash_variable][0]].sum().nlargest(5)

st.markdown(
    f""" 
    <div style='margin-top: 0px; margin-bottom: 10px; text-align: center'>
        <span style='font-size: 16px; font-weight: 200; color: #36454F;'>
            Metro Areas (and Cumulative Total) Sending <br/>the Most {dash_variable} Into {county_var} County Since 2016: 
        </span>
    </div>
    """,
    unsafe_allow_html=True)

# Define 5 Streamlit columns
col1, col2, col3, col4, col5 = st.columns(5)

# Iterate over the columns and top 5 cities
for col, (metro, migration_total) in zip([col1, col2, col3, col4, col5], metro_rollup.items()):
    with col:
        # Display the metro name
        st.markdown(
            f""" 
            <div style='margin-top: 0px; margin-bottom: -20px; text-align: center'>
                <span style='font-size: 15px; font-weight: 200; color: #36454F;'>
                    <b>{metro}</b>
                </span>
            </div>
            """,
            unsafe_allow_html=True)

        # Display migration variable under metro name
        st.markdown(
            f"""
            <div style='margin-top: 0px; margin-bottom: 0px; text-align: center'>
                <span style='font-size: 14px; font-weight: 200; color: #36454F;'>
                    ({kpi_formatter}{migration_total:,})
                </span>
            </div>
            """,
            unsafe_allow_html=True)

# finally, show the whole source data
st.write('---')
st.write("")
st.markdown(
    f"""
    <div style='margin-top: -30px; margin-bottom: 20px; text-align: left'>
        <span style='font-size: 16px; font-weight: 200; color: #36454F;'>
            See below table for migration source data from the 
            <a href="https://www.irs.gov/statistics/soi-tax-stats-migration-data" 
               target="_blank" 
               style="color: #FF6F61; 
               text-decoration: none;">
               <b>IRS Statistics of Income.</b>
            </a>
            Each row represents the flow of people, adjusted gross income (AGI), and AGI per capita into and out of {county_var} County, {state_var} relative to the other county for the given year. 
            <br/><br/>Click on any of the column headers to sort the data ascending and then descending. A third click on the column header will remove the sort. Finally, hover over the table to reveal control buttons in the top-right corner of the table to download a copy of the data to CSV, search within the table, or expand the table to fullscreen.
        </span>
    </div>
    """,
    unsafe_allow_html=True)

df_display = df[df['migration_type'] != 'total']
df_display['year'] = df_display['year'].astype(str)
df_display = df_display.drop(
    columns=['migration_type', 'primary_FIPS', 'aux_FIPS'])
df_display = df_display.rename(columns={
    'year': 'Year',
    'aux_county': 'County',
    'aux_state': 'State',
    'aux_GeoRollup': 'Metro Area',
    'agi_capita_inflow': f'AGI Per Capita into {county_var} County',
    'agi_capita_outflow': f'AGI Per Capita leaving {county_var} County',
    'agi_inflow': f'AGI into {county_var} County',
    'agi_outflow': f'AGI leaving {county_var} County',
    'people_inflow': f'Persons into {county_var} County',
    'people_outflow': f'Persons leaving {county_var} County'
})
df_display = df_display[[
    'Year',
    'County',
    'State',
    'Metro Area',
    f'AGI into {county_var} County',
    f'Persons into {county_var} County',
    f'AGI Per Capita into {county_var} County',
    f'AGI leaving {county_var} County',
    f'Persons leaving {county_var} County',
    f'AGI Per Capita leaving {county_var} County'
]]

# Format the "GDP" column as currency
formatted_df = df_display.style.format({
    f"AGI Per Capita into {county_var} County": "${:,.0f}",
    f"AGI Per Capita leaving {county_var} County": "${:,.0f}",
    f"AGI into {county_var} County": "${:,.0f}",
    f"AGI leaving {county_var} County": "${:,.0f}",
    f"Persons into {county_var} County": "{:,.0f}",
    f"Persons leaving {county_var} County": "{:,.0f}",
})

st.dataframe(formatted_df)

st.write("")
st.write("")
st.write("")
col1, col2 = st.columns([4, 1])
col1.markdown(
    f"""
    For questions about this data explorer or the source data, please contact Will Wright by clicking <a href="mailto:williamcwrightjr@gmail.com?subject=Question about Baldwin Migration Dashboard" style="text-decoration: none; color: #FF6F61;"><b>here</b>.</a> 
    """,
    unsafe_allow_html=True)
col2.image('Assets/kolter2.png', width=100)

# the custom CSS lives here:
hide_default_format = """
    <style>
        .reportview-container .main {visibility: hidden;}
        #MainMenu, header, footer {visibility: hidden;}
        div.stActionButton{visibility: hidden;}
        [class="stAppDeployButton"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none
        }
        .stRadio [role=radiogroup] {
            justify-content: left;
            background-color: #fffaf6;
            border-radius: 7px;
            padding-top: 0px;
            padding-bottom: 10px;
            padding-left: 0px;
        }
        .stRadio [role=radiogroup] p {
            font-size: 20px;
        }
    </style>
"""

# inject the CSS
st.markdown(hide_default_format, unsafe_allow_html=True)
