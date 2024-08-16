import pandas as pd
import streamlit as st
import plotly.express as px

from rhdzmota.ext.streamlit_webapps.page_view import PageView


class FrontendView(PageView):

    def get_medals_data(self):
        if "medals" not in st.session_state:
            st.session_state["medals"] = [
                row
                for _, row in px.data.medals_wide(indexed=False).T.to_dict().items()
            ]
        return st.session_state["medals"]

    def get_medals_dataframe(self):
        return pd.DataFrame(self.get_medals_data())

    def update_medals(self, nation: str, medal: str, num: int):
        data = self.get_medals_data()
        for row in data:
            if row["nation"] == nation:
                row[medal] += num
        st.session_state["medals"] = data


    def display_medals(self):
        df = self.get_medals_dataframe()
        # Display tabular data
        st.table(df)
        # Display plotly viz
        fig = px.imshow(df.set_index("nation"), labels={"x": "medals"})
        st.plotly_chart(fig)

    def view(self):
        st.markdown("# Demo: Medals Heatmap")
        with st.form("medal-update-form"):
            df = self.get_medals_dataframe()
            nation = st.selectbox("nation", df.nation.unique().tolist())
            medal_type = st.selectbox("medal", df.set_index("nation").columns.tolist())
            medal_nums = st.slider(
                "Number of medals",
                min_value=1,
                max_value=10,
                value=1,
                step=1
            )
            reduce = st.checkbox("Reduce")
            submitted = st.form_submit_button("Register")

        if not submitted:
            return self.display_medals()
        factor = -1 if reduce else 1
        self.update_medals(nation=nation, medal=medal_type, num=medal_nums * factor)
        self.display_medals()
