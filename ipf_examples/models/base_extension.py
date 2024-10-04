from loguru import logger
import ipfabric
import streamlit as st


class IPFExtension:
    """
    Base Extension for IP Fabric Extensions
        Override the input_form method to create a custom input form. The input form should handle user inputs. Input
        forms should be created using the Streamlit form method. Please see the Streamlit documentation for more.

        The input_form method is called when the extension is initialized. This starts the process of the extension. Flow is
        controlled by the input form.
    """
    name: str = "IPF Extension"
    version: str = "0.0.0a"
    logger: logger = logger
    ipf: ipfabric = ipfabric
    st: st = st

    def __init__(self):
        """
        Start the extension by calling the input form method
        """
        self.logger.info(f"Initializing {self.name} - {self.version}")
        self.input_form()
        self.manage_sidebar()

    def input_form(self):
        """
        Override this method to create a custom input form for your extension. The input form should handle user inputs.
        Input forms should be created using the Streamlit form method. Please see the Streamlit documentation for more.
        """
        ipf = None
        self.st.write("# Base Extension")
        with self.st.form(key=f"{self.name}_inputs"):
            self.st.write("This is the base extension input form. Please override this method in your extension.")
            self.st.code(
                """
                # override the input_form method in your extension
                def input_form(self):
                    with self.st.form(key=f"{self.name}_inputs"):
                        self.st.write("My Awesome Extension Input Form")
                        # Handle user inputs 
                        foo = self.st.text_input("foo", value="foo")
                        bar = self.st.text_input("bar", value="bar")
                        
                        submit_button = self.st.form_submit_button(label="Submit")
                        if submit_button:
                            # Do something with the user inputs
                            self.st.write(f"foo: {foo}")
                            self.st.write(f"bar: {bar}")
                """
            )
            self.st.write("My Awesome Extension Input Form")
            # Handle user inputs
            foo = self.st.text_input("foo", value="foo")
            bar = self.st.text_input("bar", value="bar")

            submit_button = self.st.form_submit_button(label="Submit")
            if submit_button:
                # Do something with the user inputs
                self.st.write("## You pressed the submit button")
                self.st.write(f"foo: {foo}")
                self.st.write(f"bar: {bar}")
        self.display_example_info()

    def display_example_info(self):
        self.st.write("# Demo of the IP Fabric Python SDK")
        ipf_client = self.get_key_from_session("ipf_client")
        if ipf_client:
            device_count = len(ipf_client.devices.all)
            self.st.write(f"IPF Snapshot: {ipf_client.snapshot_id}")
            self.st.write(f"Device Count: {device_count}")
        else:
            self.st.write("IP Fabric Client not initialized. Add Credentials in the Side Bar.")

    def build_ipf_client_input_form(self):
        """
        Common method to build an IP Fabric Client input form. This method will return an IP Fabric Client object if the
        form is submitted.
        """
        if not self.get_ipf_client():
            self.st.sidebar.write("Fill out the form below and press submit to initialize the IP Fabric Client")
            ipf_url = self.st.sidebar.text_input("IPF URL", help="IP Fabric URL")
            ipf_token = self.st.sidebar.text_input("IPF API Token", help="IP Fabric API Token", type="password")
            ipf_snapshot = self.st.sidebar.text_input("IPF Snapshot", help="IP Fabric Snapshot UUID")
            if self.st.sidebar.button(label="Submit"):
                ipf_client = self.ipf.IPFClient(base_url=ipf_url, auth=ipf_token, snapshot_id=ipf_snapshot)
                self.add_key_to_session("ipf_client", ipf_client)
                self.st.sidebar.write("IPF Client Initialized")
                self.add_key_to_session("base_url", ipf_url)
                self.add_key_to_session("auth", ipf_token)
                self.add_key_to_session("snapshot_id", ipf_snapshot)
                self.st.rerun()

    def manage_sidebar(self):
        """
        Manage the sidebar for the extension
        """
        if self.get_key_from_session("ipf_client"):
            self.st.sidebar.write("IP Fabric Client Initialized")
            if self.st.sidebar.button("Reinitialize IP Fabric Client"):
                del self.st.session_state["ipf_client"]
                self.st.rerun()
        else:
            self.build_ipf_client_input_form()

    def add_key_to_session(self, key, value):
        """
        Add a key value pair to the session state
        """
        session_state = self.st.session_state
        session_state[key] = value
        return

    def get_key_from_session(self, key):
        """
        Get a key value pair from the session state
        """
        session_state = self.st.session_state
        return session_state.get(key)

    def get_ipf_client(self):
        """
        Get the IP Fabric Client from the session state
        """
        return self.get_key_from_session("ipf_client")