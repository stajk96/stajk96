import pandas as pd
import streamlit as st

from utils.session_state import init_state

init_state()
st.title("Change Log")
if st.session_state.change_log:
    df = pd.DataFrame([vars(x) for x in st.session_state.change_log])
    st.dataframe(df)
    st.download_button("download csv", df.to_csv(index=False).encode("utf-8"), file_name="change_log.csv")
else:
    st.info("No changes logged yet.")
