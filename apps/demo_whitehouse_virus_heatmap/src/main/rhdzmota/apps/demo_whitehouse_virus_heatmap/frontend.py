import os

import pandas as pd
import streamlit as st
import plotly.express as px

from rhdzmota.ext.streamlit_webapps.page_view import PageView


class FrontendView(PageView):

    def get_virus_data(self):
        if "virus" not in st.session_state:
            # Initialize everything with zeros
            st.session_state["virus"] = [[0 for i in range(5)] for j in range(4)]
        return st.session_state["virus"]
    def get_whitehouse(self):
        import PIL
        whitehouse_path = os.path.join(os.path.dirname(__file__), "whitehouse.png")
        return PIL.Image.open(whitehouse_path)

    def get_virus_dataframe(self):
        df = pd.DataFrame(self.get_virus_data())
        df.columns = df.columns + 1
        df.index = df.index + 1
        return df

    def update_virus(self, xpos: int, ypos: int, num: int):
        data = self.get_virus_data()
        data[ypos][xpos] += num
        st.session_state["virus"] = data

    def display_virus_tabular(self):
        df = self.get_virus_dataframe()
        # Display tabular data
        st.table(df)

    def display_virus_heatmap(self):
        import plotly.graph_objects as go

        hm = go.Heatmap(
            z=self.get_virus_data(),
            x=[i+1 for i in range(5)],
            y=[i+1 for i in range(4)],
            hoverongaps = False,
            opacity=0.5,
            xgap=1.5, 
            ygap=1.5,
            dx = 10,
            dy = 1,
        )
        fig = go.Figure(
            data=hm,
        )
        fig.add_layout_image(
            source=self.get_whitehouse(),
            xref="x",
            yref="y",
            x=-0.4+1,
            y=3.4+1,
            sizex=5,
            sizey=4,
            opacity=1,
            layer="below",
            sizing="contain",
        )
        num_rows, num_cols = 4, 5
        # set some margins and padding
        margin = 50
        colorbar_width = 10
        
        # fix the width, scale the height
        fig_width = 800
        fig_height = 0.901*(fig_width - margin - colorbar_width) * num_rows / num_cols + margin
        
        fig.update_layout(
            width=fig_width,
            height=fig_height + 20,
            margin=dict(t=margin, b=margin, l=margin + colorbar_width, r=margin + colorbar_width),
            xaxis=dict(tickmode="linear", constrain="domain"),
            yaxis = dict(tickmode="linear", constrain="domain")
        )
        
        fig.update_layout(
            clickmode='event+select',
        )
        st.plotly_chart(fig)
        
        
    def view(self):
        st.markdown("# Demo: Whitehouse Virus Heatmap")
        with st.form("virus-update-form"):
            df = self.get_virus_dataframe()
            ypos = st.selectbox("Y Coord (Row)", df.index.tolist()) - 1
            xpos = st.selectbox("X Coord (Col)", df.columns.tolist()) - 1
            num = st.slider(
                "Virus Indicator",
                min_value=1,
                max_value=50,
                value=1,
                step=1
            )
            reduce = st.checkbox("Reduce")
            include_table = st.toggle("Display Table")
            submitted = st.form_submit_button("Register")

        if not submitted:
            self.display_virus_tabular() if include_table else None
            self.display_virus_heatmap()
            return
        factor = -1 if reduce else 1
        self.update_virus(xpos=xpos, ypos=ypos, num=num * factor)
        self.display_virus_tabular() if include_table else None
        self.display_virus_heatmap()
