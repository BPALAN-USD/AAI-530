import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Parking Sessions Analytics",
    page_icon="🅿️",
    layout="wide"
)

st.title("🅿️ Parking Sessions Analytics & AI Assistant")


@st.cache_data
def load_data():
    """Load and preprocess parking sessions data."""
    df = pd.read_csv("parking_sessions.csv")
    # Parse datetime columns
    df['IN_TIME'] = pd.to_datetime(df['IN_TIME'], format='mixed', utc=True)
    df['OUT_TIME'] = pd.to_datetime(df['OUT_TIME'], format='mixed', utc=True)
    # Extract hour for analysis
    df['HOUR'] = df['IN_TIME'].dt.hour
    return df


@st.cache_resource
def get_agent(_df):
    """Create LangChain pandas agent."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return None
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key
    )
    
    agent = create_pandas_dataframe_agent(
        llm,
        _df,
        verbose=True,
        agent_type="openai-tools",
        allow_dangerous_code=True,
        prefix="""You are a data analyst assistant helping users understand parking session data.
The dataframe contains parking sessions with columns:
- SESSION_ID: Unique session identifier
- LICENSE_PLATE: Vehicle license plate
- FACILITY_ID, FACILITY_NAME: Parking facility info
- DISTRICT: NYC district (Manhattan, Brooklyn, Queens, Bronx, Staten_Island, Airport)
- IN_TIME, OUT_TIME: Entry and exit timestamps
- ACTUAL_DURATION_HOURS: Parking duration in hours
- RATE_PER_HOUR: Hourly rate in dollars
- COST: Total cost for the session
- STATUS: Session status (completed, etc.)
- LICENSE_PLATE_STATE: State of the license plate

Always provide clear, concise answers. When showing numbers, format them appropriately (e.g., currency with $, percentages with %)."""
    )
    return agent


# Load data
df = load_data()

# Create layout: Dashboard (left) | Chatbot (right)
left_col, right_col = st.columns([2, 1])

# ============ LEFT COLUMN: DASHBOARD ============
with left_col:
    st.header("📊 Dashboard")
    
    # KPI Metrics Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        total_revenue = df['COST'].sum()
        st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    
    with kpi2:
        total_sessions = len(df)
        st.metric("🚗 Total Sessions", f"{total_sessions:,}")
    
    with kpi3:
        avg_duration = df['ACTUAL_DURATION_HOURS'].mean()
        st.metric("⏱️ Avg Duration", f"{avg_duration:.2f} hrs")
    
    with kpi4:
        unique_vehicles = df['LICENSE_PLATE'].nunique()
        st.metric("🔢 Unique Vehicles", f"{unique_vehicles:,}")
    
    st.divider()
    
    # Charts Row 1
    chart1, chart2 = st.columns(2)
    
    with chart1:
        st.subheader("Revenue by District")
        district_revenue = df.groupby('DISTRICT')['COST'].sum().reset_index()
        district_revenue = district_revenue.sort_values('COST', ascending=True)
        fig1 = px.bar(
            district_revenue,
            x='COST',
            y='DISTRICT',
            orientation='h',
            color='COST',
            color_continuous_scale='Blues'
        )
        fig1.update_layout(
            showlegend=False,
            xaxis_title="Revenue ($)",
            yaxis_title="",
            height=300,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig1.update_traces(texttemplate='$%{x:,.0f}', textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)
    
    with chart2:
        st.subheader("Sessions by Hour")
        hourly_sessions = df.groupby('HOUR').size().reset_index(name='COUNT')
        fig2 = px.line(
            hourly_sessions,
            x='HOUR',
            y='COUNT',
            markers=True
        )
        fig2.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Number of Sessions",
            height=300,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        fig2.update_traces(line_color='#1f77b4', fill='tozeroy', fillcolor='rgba(31,119,180,0.2)')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Charts Row 2
    chart3, chart4 = st.columns(2)
    
    with chart3:
        st.subheader("Top 10 Facilities by Revenue")
        facility_revenue = df.groupby('FACILITY_NAME')['COST'].sum().reset_index()
        facility_revenue = facility_revenue.nlargest(10, 'COST')
        fig3 = px.bar(
            facility_revenue,
            x='FACILITY_NAME',
            y='COST',
            color='COST',
            color_continuous_scale='Greens'
        )
        fig3.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="Revenue ($)",
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with chart4:
        st.subheader("Sessions by State (Top 10)")
        state_sessions = df.groupby('LICENSE_PLATE_STATE').size().reset_index(name='COUNT')
        state_sessions = state_sessions.nlargest(10, 'COUNT')
        fig4 = px.pie(
            state_sessions,
            values='COUNT',
            names='LICENSE_PLATE_STATE',
            hole=0.4
        )
        fig4.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig4, use_container_width=True)

# ============ RIGHT COLUMN: CHATBOT ============
with right_col:
    st.header("🤖 AI Assistant")
    st.caption("Ask questions about the parking data")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    chat_container = st.container(height=500)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about parking data..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        # Get agent response
        agent = get_agent(df)
        
        if agent is None:
            response = "⚠️ Please set your OpenAI API key in the .env file to use the AI assistant."
        else:
            with st.spinner("Thinking..."):
                try:
                    result = agent.invoke({"input": prompt})
                    response = result["output"]
                except Exception as e:
                    response = f"❌ Error: {str(e)}"
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(response)
        
        # Rerun to update the chat display
        st.rerun()
    
    # Sample questions
    st.divider()
    st.subheader("💡 Sample Questions")
    sample_questions = [
        "What is the total revenue?",
        "Which district has the most sessions?",
        "What's the average cost per session in Manhattan?",
        "Top 5 facilities by number of sessions?",
        "How many NJ plates parked here?",
        "What's the busiest hour for parking?"
    ]
    
    for q in sample_questions:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()
