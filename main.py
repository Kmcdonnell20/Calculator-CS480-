from calculator import evaluateInput

import streamlit as st

# Set page title for web app
st.set_page_config(page_title="Calculator")

# Start setting a title for the app
st.markdown("""
        # Web Scientific Calculator
        This calculator allows the user to input any expression and it returns the result
        Allowed operations:
        * All basic math operations
        * Trigonometric operations (sin, cos, tan, cot, arcsin, ...)
        * Power operations using ^
        * Logarithms (log and ln)

        *Note: The valid parenthesis are (), [] and {}*
        """)


# Create a text field that allows the user to give input
expression = st.text_input("Input your expression here:")

# Create a button that triggers the calculation if an input is given
col1, col2, col3 = st.columns([1, 1, 1])
if col2.button("Evaluate"):
    # Validate expression if given
    if expression != "":
        result = evaluateInput(expression)
        if isinstance(result, str):
            col2.error(result)
        else:
            col2.success(result)
