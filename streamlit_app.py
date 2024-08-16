import streamlit as st
from st_pages import join_table_page

pg = st.navigation([
    st.Page(join_table_page.join_table_page, title="Join Table", icon="🔗"),
]
)
pg.run()
