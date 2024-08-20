import streamlit as st
from ipfabric_snow.apps.sync_devices import sync_devices_func
import os
import dotenv


def service_now_page():
    dotenv.load_dotenv(dotenv.find_dotenv())
    with st.form(key="snow_inputs"):
        show_diff = st.checkbox("Show Diff", value=True)
        diff_source = st.multiselect("Diff Source", options=["SNOW", "IPF"])
        write_diff = st.checkbox("Write Diff")
        dry_run = st.checkbox("Dry Run", value=True)
        ipf_snapshot = st.text_input("IPF Snapshot", value="$last")
        timeout = st.number_input("Timeout", value=10)
        record_limit = int(st.number_input("Record Limit", value=1000))
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

        etl_utility, diff = sync_devices_func(
            show_diff=show_diff,
            diff_source=diff_source[0],
            write_diff=write_diff,
            dry_run=dry_run,
            ipf_snapshot=ipf_snapshot,
            timeout=timeout,
            record_limit=record_limit,
            output_verbose=output_verbose,
        )

    st.write(diff)
    choices = list(diff.keys())
    choice = st.multiselect("Service Now Diff", choices)
    if choice:
        st.write(diff[choice[0]])

service_now_page()