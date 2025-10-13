from .ReportGenerator import ReportGenerator
class HTMLReportGenerator(ReportGenerator):
    def _format_header(self): return "<h1>Relatório</h1>"
    def _format_body(self, data): return f"<pre>{data}</pre>"
    def _format_footer(self): return "<hr/>"
