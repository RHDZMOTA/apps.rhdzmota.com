import enum
import textwrap
from typing import Optional

import streamlit as st

from rhdzmota.ext.streamlit_webapps.page_view import PageView
from rhdzmota.ext.streamlit_webapps.page_view_switcher import PageViewSwitcher
from rhdzmota.ext.streamlit_webapps.backend import BackendRequestHandler
from rhdzmota.apps.hello_world.utils import Salutation


class FrontendView(PageView):

    def view(self):
        st.markdown("# Example App: hello-world")
    
        st.markdown(
            textwrap.dedent(
                """
                Example hello-world application designed by 
                [Rodrigo H. Mota](https://rhdzmota.com).
                """
            )
        )
    
        with st.form("form-hello-world"):
            recipient = st.text_input(label="Recipient", value="World")
            salutation = st.selectbox(
                label="Salutation",
                options=[
                    salutation
                    for salutation in Salutation
                ],
                format_func=lambda salutation: salutation.name.title()
            )
            submitted = st.form_submit_button("Submit")
        if not submitted:
            return
        st.markdown(f"> {salutation.value}, {recipient}!")


def get_frontend(
        page_start_key: Optional[str] = None,
        attach_handler: Optional[BackendRequestHandler] = None,
        **shared_page_configs,
    ):
    # Define the views
    main = Main(page_title="Hello", **shared_page_configs)
    # Set the default starting page
    page_start_key = page_start_key or main.refname
    # Create switcher instance
    switcher = PageViewSwitcher.from_page_views(
        switcher_name="hello-world",
        page_views=[main]
    )
    return switcher.run(initial_page_key=page_start_key, backend_request_handler=attach_handler)

