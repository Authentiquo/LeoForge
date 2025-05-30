import streamlit as st
import subprocess
import sys

def run_leoforge_generate(query: str):
    """Runs the leoforge generate command with the given query."""
    # Use subprocess to run the launch.sh script
    # We need to ensure the script is executable and correctly finds main.py
    # Using the full command including python and main.py might be more robust
    command = ["./launch.sh", "generate", query, "--no-interactive"]
    
    process = subprocess.Popen(
        command,
        cwd=".", # Run from the project root directory
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, # Capture stderr as well
        text=True # Decode stdout/stderr as text
    )
    
    # Stream output line by line
    output = []
    for line in process.stdout:
        output.append(line)
        # Optional: display output in real-time in Streamlit (requires more complex handling)
        # For simplicity, we'll capture and display after completion
        # st.text(line, anchor=False)

    process.wait()
    
    return "".join(output)

st.set_page_config(layout="wide") # Use wide layout

st.title("🔥 LeoForge")

st.markdown("Enter your project description below and click 'Forge' to generate code.")

# Input field for the user query
user_query = st.text_area(
    "Describe your Leo project:",
    "Create a simple token with mint and transfer functions", # Default value
    height=150
)

# Button to trigger the generation
if st.button("Forge"):
    if not user_query:
        st.warning("Please enter a project description.")
    else:
        with st.spinner("Forging your project... Please wait, this might take a few minutes."):
            # Run the LeoForge generation
            output = run_leoforge_generate(user_query)
            
            # Display the output
            st.subheader("Output:")
            # Use a markdown code block for better formatting of stdout
            st.code(output, language='bash')

st.markdown("---")
st.markdown("Powered by [LeoForge](https://github.com/yourusername/LeoForge)") 