import streamlit as st
from st_pages import join_table_page, service_now_page

pg = st.navigation([
    st.Page(join_table_page.join_table_page, title="Join Table", icon="🔗"),
    st.Page(service_now_page.service_now_page, title="Service Now", icon="🔧"),
]
)
pg.run()
