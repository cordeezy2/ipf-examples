import streamlit as st
from ipfabric import IPFClient
import pandas as pd
import json
st.title("Join Table")
st.write(
    "built using Streamlit [docs.streamlit.io](https://docs.streamlit.io/)."
)


ipf = IPFClient()

list_of_tables = list()
for table in ipf.oas:
    if table.startswith("table"):
        list_of_tables.append(table)

st.write("Join IP Fabric Data from two tables, defaults to $last snapshot.")
right_table_options = st.multiselect(
    "Select right table",
    list_of_tables,
    max_selections=1
    )
right_table_options_columns = ipf.get_columns(right_table_options[0])
right_table_options_columns.remove("id")
right_table_options_columns = st.multiselect("Select columns for right table", right_table_options_columns)
right_table_filter = st.text_input("Filter for right table", value="{}")

left_table_options = st.multiselect(
    "Select left table",
    list_of_tables,
    max_selections=1
)
left_table_options_columns = ipf.get_columns(left_table_options[0])
left_table_options_columns.remove("id")
left_table_options_columns = st.multiselect("Select columns for left table", left_table_options_columns)
left_table_filter = st.text_input("Filter for left table", value="{}", help='{"and": [{"mode": ["eq","trunk"]}]}')


columns = (
        set(column for column in ipf.get_columns(right_table_options[0]))
        &
        set(column for column in ipf.get_columns(left_table_options[0]))
        )

if not columns or len(right_table_options) == 0 or len(left_table_options) == 0:
    st.write(f"please select both tables to join and try again.")
else:
    columns = st.multiselect(f"Possible columns for join", columns)


table_data_left = ipf.fetch_all(left_table_options[0],
                                export="df",
                                columns=left_table_options_columns,
                                filters=json.loads(left_table_filter))
table_data_right = ipf.fetch_all(right_table_options[0],
                                export="df",
                                columns=right_table_options_columns,
                                filters=json.loads(right_table_filter))
joined_data = pd.merge(
    table_data_left,
    table_data_right,
    on=columns,
    how="outer",
    suffixes=(f"_{left_table_options[0]}", f"_{right_table_options[0]}")
)

st.markdown("### Joined Data")
st.write(joined_data)

snapshot_selection = [
    snap for snap in ipf.get_snapshots()
]
for snap_id in ["$last", ipf.snapshot_id]:
    if snap_id in snapshot_selection:
        snapshot_selection.remove(snap_id)

snapshot_selection = st.multiselect("Select IP Fabric Snapshot", snapshot_selection, max_selections=1)
compare_table_data_left = ipf.fetch_all(left_table_options[0], export="df", snapshot_id=snapshot_selection[0], columns=left_table_options_columns, filters=json.loads(left_table_filter))
compare_table_data_right = ipf.fetch_all(right_table_options[0], export="df", snapshot_id=snapshot_selection[0], columns=right_table_options_columns, filters=json.loads(right_table_filter))
compare_joined_data = pd.merge(compare_table_data_left, compare_table_data_right, on=columns, how="outer")
st.write("Fetch the same data from another snapshot to compare.")
st.markdown(f"### Joined Data from snapshot {snapshot_selection[0]}")
st.write(compare_joined_data)

st.markdown("### Compare the Data!")
st.write("Let's compare the data from the two snapshots!")
if joined_data.equals(compare_joined_data):
    st.write("Data is the same!")
else:
    compared_df = pd.merge(joined_data, compare_joined_data, on=columns, how="outer", suffixes=("_current", "_compare"))
    st.write(compared_df)
