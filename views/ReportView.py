import streamlit as st
import streamlit as st
from Business.Bridge.abstractions import ActivityReport
from Business.Bridge.implementors import FileOutputImplementor

class ReportView:
    def __init__(self, atividades):
        self.manager = atividades

    def render(self):
        st.title("📊 Geração de Relatórios")

        st.markdown("Gere um relatório com estatísticas sobre as atividades registradas.")

        if st.button("Gerar Relatório"):
            implementor = FileOutputImplementor("report.txt")
            report = ActivityReport(implementor, self.manager)
            report.export()
            st.success("✅ Relatório salvo como **report.txt** na pasta do projeto.")
