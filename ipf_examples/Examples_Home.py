import streamlit as st
from models.base_extension import IPFExtension
from models.ipf_report import IPFReport
from models.ipf_dora_example import IPFDoraExample


def build_home_page():
    st.markdown("# IP Fabric Plugin Home Page")

    st.write(
        """
        Welcome to the IP Fabric Examples page.
        This page hopes to give you an overview of the what is possible with the IP Fabric API.
    
        The navigation bar on the left while guide you through the default "Extension" installed with IP Fabric.
        """
    )


st.set_page_config(page_title="IP Fabric Plugins", page_icon=":electric_plug:", layout="centered")
pages = st.navigation(
    {
        "Example Extensions": [
            st.Page(build_home_page, title="Home", icon='🏠'),
            st.Page("models/pages/Global_Search.py", title="Global Search", icon='🔍'),
            st.Page(IPFReport, title="Built in Reporting", icon="📤"),
            st.Page(IPFDoraExample, title="Dora Example", icon="💶" ),
        ],
        "Base Extension": [
            st.Page(IPFExtension, title="Base Extension", ),
        ],
    }
)
pages.run()
