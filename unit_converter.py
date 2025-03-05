import streamlit as st
import plotly.graph_objects as go
import requests
import json

def length_conversion(value, from_unit, to_unit):
    # Base unit is meters
    length_units = {
        'Kilometer': 1000,
        'Meter': 1,
        'Centimeter': 0.01,
        'Millimeter': 0.001,
        'Mile': 1609.34,
        'Yard': 0.9144,
        'Foot': 0.3048,
        'Inch': 0.0254
    }
    # Convert to base unit first, then to target unit
    return value * length_units[from_unit] / length_units[to_unit]

def weight_conversion(value, from_unit, to_unit):
    # Base unit is kilograms
    weight_units = {
        'Tonne': 1000,
        'Kilogram': 1,
        'Gram': 0.001,
        'Milligram': 0.000001,
        'Pound': 0.453592,
        'Ounce': 0.0283495
    }
    return value * weight_units[from_unit] / weight_units[to_unit]

def temperature_conversion(value, from_unit, to_unit):
    if from_unit == 'Celsius':
        if to_unit == 'Fahrenheit':
            return (value * 9/5) + 32
        elif to_unit == 'Kelvin':
            return value + 273.15
    elif from_unit == 'Fahrenheit':
        if to_unit == 'Celsius':
            return (value - 32) * 5/9
        elif to_unit == 'Kelvin':
            return (value - 32) * 5/9 + 273.15
    elif from_unit == 'Kelvin':
        if to_unit == 'Celsius':
            return value - 273.15
        elif to_unit == 'Fahrenheit':
            return (value - 273.15) * 9/5 + 32
    return value

def create_conversion_graph(value, result, from_unit, to_unit):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[from_unit, to_unit],
        y=[value, result],
        text=[f'{value:.2f}', f'{result:.2f}'],
        textposition='auto',
        marker_color=['#1f77b4', '#2ecc71']
    ))
    
    fig.update_layout(
        title={
            'text': 'Conversion Visualization',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    return fig

def main():
    # Page configuration
    st.set_page_config(
        page_title="Unit Converter Pro",
        page_icon="🔄",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #2ecc71;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
        }
        .stSelectbox {
            margin-bottom: 20px;
        }
        .success-message {
            padding: 20px;
            border-radius: 10px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Professional Unit Converter")
        st.write("Convert between different units of measurement with real-time visualization")

    # Main content
    main_col1, main_col2 = st.columns([2, 3])

    with main_col1:
        st.markdown("### Input Parameters")
        conversion_type = st.selectbox(
            "Select Conversion Type",
            ["Length", "Weight", "Temperature"],
            key="conversion_type"
        )

        value = st.number_input("Enter Value", value=0.0, key="value_input")

        if conversion_type == "Length":
            units = ['Kilometer', 'Meter', 'Centimeter', 'Millimeter', 
                    'Mile', 'Yard', 'Foot', 'Inch']
        elif conversion_type == "Weight":
            units = ['Tonne', 'Kilogram', 'Gram', 'Milligram', 
                    'Pound', 'Ounce']
        else:
            units = ['Celsius', 'Fahrenheit', 'Kelvin']

        from_unit = st.selectbox("From Unit", units, key="from_unit")
        to_unit = st.selectbox("To Unit", units, key="to_unit")

        convert_button = st.button("Convert Units")

    with main_col2:
        st.markdown("### Results and Visualization")
        if convert_button:
            if conversion_type == "Length":
                result = length_conversion(value, from_unit, to_unit)
            elif conversion_type == "Weight":
                result = weight_conversion(value, from_unit, to_unit)
            else:
                result = temperature_conversion(value, from_unit, to_unit)

            # Display result
            st.markdown(f"""
                <div class='success-message'>
                    <h3>Conversion Result:</h3>
                    <p>{value} {from_unit} = {result:.4f} {to_unit}</p>
                </div>
            """, unsafe_allow_html=True)

            # Display graph
            fig = create_conversion_graph(value, result, from_unit, to_unit)
            st.plotly_chart(fig, use_container_width=True)

    # Add information cards
    st.markdown("### Additional Information")
    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4>🎯 Precision</h4>
                <p>All calculations are performed with high precision floating-point arithmetic.</p>
            </div>
        """, unsafe_allow_html=True)

    with info_col2:
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4>📊 Visualization</h4>
                <p>Interactive charts help you understand the conversion ratios better.</p>
            </div>
        """, unsafe_allow_html=True)

    with info_col3:
        st.markdown("""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4>🔄 Real-time</h4>
                <p>Get instant conversions with our real-time calculation engine.</p>
            </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Made with ❤️ using Streamlit | "
        "© 2024 Unit Converter Pro</p>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()