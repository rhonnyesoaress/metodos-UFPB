from abc import ABC, abstractmethod

class IOutputImplementor(ABC):
    @abstractmethod
    def save(self, data: str):
        pass


class FileOutputImplementor(IOutputImplementor):
    def __init__(self, filename="report.txt"):
        self.filename = filename

    def save(self, data: str):
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(data)


class ConsoleOutputImplementor(IOutputImplementor):
    """Implementor que apenas imprime o relatório no console (útil para debug).

    Útil quando a UI quer exibir o relatório diretamente em vez de gravar em
    arquivo.
    """
    def save(self, data: str):
        print(data)
