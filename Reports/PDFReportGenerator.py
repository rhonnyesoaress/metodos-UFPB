from .ReportGenerator import ReportGenerator

class PDFReportGenerator(ReportGenerator):
    def _format_header(self) -> str:
        return "=== RELATÓRIO ===\n"

    def _format_body(self, data: dict) -> str:
        linhas = "\n".join(f"{k}: {v}" for k, v in data.items())
        return linhas + "\n"

    def _format_footer(self) -> str:
        return "=== FIM ===\n"