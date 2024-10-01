import streamlit as st
from ipfabric import IPFClient
from ipfabric.models.global_search import GlobalSearch, RANKED
import pandas as pd


def display_global_search(results):
    st.write("# Results of Global Search")
    for result in results:
        st.write(f"Menu: {result['menu']}")
        st.write(f"Path: {result['path']}")
        st.write(f"URL: {result['url']}")
        st.write(pd.DataFrame.from_records(result["data"]))


def global_search():
    results = None
    st.set_page_config(page_title="IP Fabric Global Search", page_icon=":mag:", layout="centered")
    st.title("Global Search")
    with st.form(key="Global Search Args"):
        snapshot = st.text_input(label="IPF Snapshot UUID", value="$last")
        ipf = IPFClient(snapshot_id=snapshot)
        ipf._client.headers["user-agent"] += "; IPF Extensions "
        gs = GlobalSearch(client=ipf)
        address = st.text_input(label="IP or MAC Address to search")
        regex = st.text_input(label="Regex to use in search")
        if regex:
            search_type = st.multiselect(label="Search Type", options=["ipv4", "ipv6", "mac"], default=["ipv4"], max_selections=1)
        full_scan = st.checkbox(label="Full Scan")
        break_on_match = st.checkbox(label="Break on Match?")
        submitted = st.form_submit_button("Run Global Search")
        if submitted:
            if regex:
                results = gs.search_regex(
                    search_type=search_type[0], address=address, full_scan=full_scan, first_match=break_on_match
                )
            else:
                results = gs.search(address=address, full_scan=full_scan, first_match=break_on_match)
    if results:
        display_global_search(results.values())


global_search()
