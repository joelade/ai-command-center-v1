
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import random

# Set page config
st.set_page_config(
    page_title="QA Confidence Dashboard",
    page_icon="📊",
    layout="wide"
)

# API Configuration
ORCHESTRATOR_URL = "http://qa-orchestrator:8000"

# Title
st.title("🎯 QA Confidence Dashboard")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    time_range = st.selectbox("Time Range", ["Last 24h", "Last 7d", "Last 30d", "All Time"])
    refresh_rate = st.slider("Refresh Rate (seconds)", 5, 60, 30)
    st.markdown("---")
    
    # LLM Models Section
    st.subheader("🤖 LLM Models")
    available_models = ["mistral:latest", "neural-chat", "orca-mini", "Qwen2.5", "nomic-embed-text:latest", "deepseek-coder", "llama3"]
    selected_models = st.multiselect(
        "Select Models for QA Testing",
        available_models,
        default=["mistral:latest"]
    )
    
    if st.button("Update Model Configuration"):
        st.success(f"Models updated: {', '.join(selected_models)}")
    
    st.markdown("---")
    st.info("Dashboard auto-refreshes based on selected rate")

# Main tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 Models", "📋 Tests"])

with tab1:
    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Completeness Score", "92%", "+2%")
    with col2:
        st.metric("Risk Level", "High", "-5%")
    with col3:
        st.metric("Test Coverage", "87%", "+3%")
    with col4:
        st.metric("Avg Response Time", "245ms", "-12ms")

    st.markdown("---")

    # Charts row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Test Case Distribution")
        chart_data = {
            "Positive": 70,
            "Negative": 20,
            "Edge Cases": 10
        }
        st.bar_chart(chart_data)

    with col2:
        st.subheader("Success Rate Trend")
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D')
        success_rates = [85, 87, 86, 89, 88, 90, 92]
        trend_data = pd.DataFrame({
            'Date': dates,
            'Success Rate': success_rates
        })
        st.line_chart(trend_data.set_index('Date'))

    st.markdown("---")

    # Detailed metrics
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Test Results Summary")
        results_data = {
            'Status': ['Passed', 'Failed', 'Skipped', 'Pending'],
            'Count': [145, 12, 8, 5]
        }
        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, width='stretch')

    with col2:
        st.subheader("Risk Categories")
        risk_data = {
            'Category': ['Critical', 'High', 'Medium', 'Low'],
        'Issues': [3, 12, 28, 45]
    }
    risk_df = pd.DataFrame(risk_data)
    st.dataframe(risk_df, width='stretch')

    st.markdown("---")

    # Recent activity
    st.subheader("📋 Recent Test Executions")
    execution_data = {
        'Test ID': ['TEST_001', 'TEST_002', 'TEST_003', 'TEST_004', 'TEST_005'],
        'Test Name': ['Login Flow', 'Data Validation', 'API Response', 'UI Rendering', 'Error Handling'],
        'Status': ['✅ Passed', '✅ Passed', '❌ Failed', '✅ Passed', '⚠️ Skipped'],
        'Duration': ['1.2s', '0.8s', '2.1s', '1.5s', '0s'],
        'Timestamp': [
            datetime.now() - timedelta(minutes=5),
            datetime.now() - timedelta(minutes=8),
            datetime.now() - timedelta(minutes=12),
            datetime.now() - timedelta(minutes=15),
            datetime.now() - timedelta(minutes=20)
        ]
    }
    execution_df = pd.DataFrame(execution_data)
    st.dataframe(execution_df, width='stretch')

with tab2:
    st.header("🤖 LLM Models Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Available Models")
        st.write("Models ready to pull:")
        available_models_list = ["mistral:latest", "neural-chat", "orca-mini", "Qwen2.5", "nomic-embed-text:latest", "deepseek-coder", "llama3"]
        for model in available_models_list:
            st.write(f"• {model}")
    
    with col2:
        st.subheader("Active Models")
        active_data = {
            'Model': ['mistral:latest', 'neural-chat', 'Qwen2.5', 'llama3'],
            'Size': ['7GB', '4GB', '6GB', '8GB'],
            'Status': ['Running', 'Running', 'Running', 'Running']
        }
        active_df = pd.DataFrame(active_data)
        st.dataframe(active_df, width='stretch')
    
    st.markdown("---")
    
    st.subheader("Pull New Model")
    col1, col2 = st.columns([3, 1])
    with col1:
        model_to_pull = st.selectbox("Select model to download", available_models_list)
    with col2:
        if st.button("📥 Pull Model"):
            st.info(f"Pulling {model_to_pull}... This may take a few minutes.")
    
    st.markdown("---")
    
    st.subheader("Model Performance")
    perf_data = {
        'Model': ['mistral:latest', 'neural-chat', 'orca-mini', 'Qwen2.5', 'llama3', 'deepseek-coder'],
        'Avg Response Time': ['245ms', '180ms', '320ms', '210ms', '290ms', '350ms'],
        'Success Rate': ['94%', '91%', '89%', '95%', '92%', '88%'],
        'Latency': [245, 180, 320, 210, 290, 350]
    }
    perf_df = pd.DataFrame(perf_data)
    st.dataframe(perf_df, width='stretch')

with tab3:
    st.header("📋 Test Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Test Configuration")
        st.selectbox("Select Test Suite", ["Login Tests", "API Tests", "UI Tests", "Integration Tests"])
        st.multiselect("Models to Test With", ["mistral:latest", "neural-chat", "orca-mini", "Qwen2.5", "nomic-embed-text:latest", "deepseek-coder", "llama3"])
        if st.button("▶️ Run Tests"):
            st.success("Tests started! Monitor progress below.")
    
    with col2:
        st.subheader("Test Statistics")
        stats_data = {
            'Metric': ['Total Tests', 'Passed', 'Failed', 'Success Rate'],
            'Value': [170, 157, 13, '92.4%']
        }
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, width='stretch')
    
    st.markdown("---")
    
    st.subheader("Test Execution History")
    history_data = {
        'Test Suite': ['Login Tests', 'API Tests', 'UI Tests', 'Integration Tests'],
        'Last Run': ['2 hours ago', '1 hour ago', '30 mins ago', '45 mins ago'],
        'Status': ['✅ Passed', '✅ Passed', '⚠️ Mixed', '✅ Passed'],
        'Duration': ['2m 15s', '3m 45s', '5m 20s', '7m 10s']
    }
    history_df = pd.DataFrame(history_data)
    st.dataframe(history_df, width='stretch')

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; margin-top: 30px;'>
    Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
    <br>
    <small>QA Confidence Dashboard v2.0 - Multi-LLM Support</small>
</div>
""", unsafe_allow_html=True)
