import streamlit as st

from rhdzmota.ext.streamlit_webapps.page_view import PageView


class FrontendView(PageView):
    def view(self):
        st.markdown("# Hello, World!")
