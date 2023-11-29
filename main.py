import streamlit as st
from bridge import Bridge

# Create bridge instance
bridge = Bridge()

# Create input prompt field
prompt = st.text_area("Input prompt", height=100)

# Create dropdowns for ply types
main_ply_type = st.selectbox("Main model ply type", ["None", "1", "2", "3", "4"])
sub_ply_type = st.selectbox("Sub model ply type", ["None", "1", "2", "3", "4"])

# Define main and sub prompts
main_prompt = f"{prompt}"
sub_prompt = f"{prompt}"

# Get main and sub output using bridge
if main_ply_type != "None":
    main_prompt = f"{bridge.a}+{bridge.b}:{main_prompt}"
    main_prompt = bridge.transform(main_prompt, main_ply_type)

if sub_ply_type != "None":
    sub_prompt = f"{bridge.c}:{bridge.D}"
    sub_prompt = bridge.transform(sub_prompt, sub_ply_type)

# Display main and sub output
st.text_area("Main model output", value=main_prompt, height=300)
st.text_area("Sub model output", value=sub_prompt, height=300)

