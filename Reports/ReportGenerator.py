from abc import ABC, abstractmethod
class ReportGenerator(ABC):
    def generate_report(self, data: dict) -> str:
        return self._format_header() + self._format_body(data) + self._format_footer()
    @abstractmethod
    def _format_header(self) -> str: ...
    @abstractmethod
    def _format_body(self, data: dict) -> str: ...
    @abstractmethod
    def _format_footer(self) -> str: ...
