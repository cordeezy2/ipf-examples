import streamlit as st


def service_now_page():
    with st.form(key="snow_inputs"):
        show_diff = st.checkbox("Show Diff")
        diff_source = st.text_input("Diff Source")
        write_diff = st.checkbox("Write Diff")
        dry_run = st.checkbox("Dry Run")
        ipf_snapshot = st.text_input("IPF Snapshot")
        timeout = st.number_input("Timeout")
        record_limit = st.number_input("Record Limit")
        output_verbose = st.checkbox("Output Verbose")
        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            st.write("show_diff", show_diff)
            st.write("diff_source", diff_source)
            st.write("write_diff", write_diff)
            st.write("dry_run", dry_run)
            st.write("ipf_snapshot", ipf_snapshot)
            st.write("timeout", timeout)
            st.write("record_limit", record_limit)
            st.write("output_verbose", output_verbose)
    st.title("Service Now")
    st.write("built using Streamlit [docs.streamlit.io](https://docs.streamlit.io/).")
    st.write("This page is under construction.")
    st.write("Please select a different page from the sidebar.")
    st.write("Thank you for your patience.")