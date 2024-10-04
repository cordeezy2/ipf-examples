import streamlit

from .base_extension import IPFExtension
from ipfabric_reports import IPFabricReportGenerator
from ipfabric_reports.report_registry import ReportRegistry
import os
from os import listdir
from os.path import isfile, join


class IPFReport(IPFExtension):
    name: str = "IPF Report"
    version: str = "0.0.0a"
    report_generator: IPFabricReportGenerator = IPFabricReportGenerator

    def __init__(self):
        super().__init__()

    def input_form(self):
        try:
            ipf_client = self.get_ipf_client()
            self.st.write(
                """
                # IP Fabric Report
                This extension allows you to generate reports from the IP Fabric API.
                You can customize the report by providing a custom css file.
                \n
                The following reports are available: \n
                """
            )

            report_options = ReportRegistry.list_reports()
            for report, report_info in report_options.items():
                self.st.write(f"##### {report.upper()}\n"
                              f"{report_info}")
            report = self.st.selectbox("Select Report", report_options)
            self.st.write(f"{report} selected")
            self.st.write("Please provide the following information to generate the report.")
            if not ipf_client:
                self.st.write("IP Fabric Client not initialized. Please initialize in the sidebar.")
                return
            self.st.write(self.st.session_state)
            server_url = f"https://{ipf_client.base_url.host}"
            os.environ['IPF_URL'] = server_url
            token = self.st.session_state.get("auth")
            os.environ['IPF_TOKEN'] = token if token else ''
            snapshot_id = ipf_client.snapshot_id
            os.environ['IPF_SNAPSHOT_ID'] = snapshot_id
            report_type = report
            os.environ['REPORT_TYPE'] = report_type

            with self.st.form(key="Report Form"):
                site_filter = self.st.text_input("Site Filter", value="")
                report_style = self.st.text_input("Report Style", value="default_style.css")
                submit = self.st.form_submit_button("Generate Report")
                if submit:
                    if ipf_client:
                        self.get_report()
                    else:
                        self.st.write("IP Fabric Client not initialized. Please initialize in the sidebar.")
            self.display_file()

        except Exception as e:
            self.st.write(f"Error: {e}")
            self.logger.error(f"Error: {e}")

    @staticmethod
    def get_report():
        report_generator = IPFabricReportGenerator()
        report_generator.generate_report()

    def display_file(self):
        mypath = os.path.join(os.getcwd(), 'export')
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        self.st.write("Please select the report file to download. or view")
        report_file = self.st.selectbox("Select Report File", onlyfiles)

        with open(os.path.join(mypath, report_file), 'rb') as f:
            btn = self.st.download_button(label="Download Report", data=f, file_name=report_file, )
        view = self.st.button("View Report")
        if view:
            if report_file.endswith('.html'):
                with open(os.path.join(mypath, report_file), 'r') as f:
                    self.st.html(f.read())
            else:
                self.st.write("Only HTML files can be viewed.")
