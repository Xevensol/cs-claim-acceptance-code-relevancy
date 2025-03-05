import streamlit as st
import re
# Custom function to display success messages with black text
def subheader_func(message):
    st.markdown(
        f"""
        <div style="color: black; background-color: #DFF2BF; border: 0.5px solid #4CAF50; padding: 5px; border-radius: 5px;">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )

def warning_message(message):
    st.markdown(
        f"""
        <div style="color: white; background-color: #FF0000; border: 0.5px solid #4CAF50; padding: 5px; border-radius: 5px;">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )
    
def output_message(message):
    color = "#EF4444" if "Irrelevant" in message else "black"  # Red for Irrelevant, black for others
    st.markdown(
        f"""
        <div style="color: {color}; padding: 5px; border-radius: 5px; font-size: 25px;">
            <b>{message}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

def output_final(message):
    st.markdown(
        f"""
        <div style="color: black; padding: 15px; border-radius: 10px; font-size: 15px; background-color: #f0f0f0; border: 1px solid #ddd;">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )

def reformat_bullet_points(text):
    reformatted = re.sub(r"- (\d+)", r"\n- \1", text.strip())
    reformatted = re.sub(r"\s*\.\s*$", "", reformatted)
    return reformatted

def reformat_output(output):
    reformatted_text = ""
    relevant_codes = output.relevant_sbs_codes
    irrelevant_codes = output.irrelevant_sbs_codes
    reason_for_irrelevancy = output.reason_for_irrelevancy

    # Relevant SBS Codes
    if relevant_codes:
        reformatted_text += "<p><span style='color: red; font-size: 16px;'><strong>Relevant SBS Codes:</strong></span></p>"
        reformatted_text += "<ul>"
        for relevant_code in relevant_codes:
            reformatted_text += f"<li>{relevant_code}</li>"
        reformatted_text += "</ul>"
    else:
        reformatted_text += "<p><span style='color: red; font-size: 16px;'><strong>Relevant SBS Codes: None</strong></span></p>"

    # Irrelevant SBS Codes
    if irrelevant_codes:
        reformatted_text += "<p><span style='color: red; font-size: 16px;'><strong>Irrelevant SBS Codes:</strong></span></p>"
        reformatted_text += "<ul>"
        for irrelevant_code in irrelevant_codes:
            reformatted_text += f"<li>{irrelevant_code}</li>"
        reformatted_text += "</ul>"
    else:
        reformatted_text += "<p><span style='color: red; font-size: 16px;'><strong>Irrelevant SBS Codes: None</strong></span></p>"

    # Reason for Irrelevancy
    if reason_for_irrelevancy:
        reformatted_text += f"<p><span style='color: red; font-size: 16px;'><strong>Reason of Irrelevancy:</strong></span> {reason_for_irrelevancy}</p>"

    return reformatted_text

