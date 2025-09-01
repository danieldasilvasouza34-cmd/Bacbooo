import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

class BacBoAI:
    def __init__(self, aposta_unidade=1, banca_inicial=100, stop_win=None, stop_loss=None):
        self.historico = []
        self.aposta_unidade = aposta_unidade
        self.banca = banca_inicial
        self.banca_inicial = banca_inicial
        self.lucro_prejuizo = []
        self.stop_win = stop_win
        self.stop_loss = stop_loss
        self.parou = False
        self.resultados_apostas = []  # guarda win/loss

    def jogar_rodada(self):
        if self.parou:
            return "Jogo parado pelo gerenciamento de stop."

        # Dois dados para cada lado
        player = random.randint(1,6) + random.randint(1,6)
        banker = random.randint(1,6) + random.randint(1,6)

        if player > banker:
            resultado = "Player"
        elif banker > player:
            resultado = "Banker"
        else:
            resultado = f"Tie-{player}"  # Empate com número específico

        self.historico.append(resultado)
        return resultado

    def aplicar_aposta(self, resultado, estrategia="misto"):
        if self.parou:
            return 0

        aposta = self.aposta_unidade
        ganho = 0
        win = False

        if estrategia == "so_tie":
            if "Tie" in resultado:
                ganho = aposta * 4  # payout Tie
                win = True
            else:
                ganho = -aposta

        elif estrategia == "so_player":
            if resultado == "Player":
                ganho = aposta
                win = True
            else:
                ganho = -aposta

        elif estrategia == "so_banker":
            if resultado == "Banker":
                ganho = aposta
                win = True
            else:
                ganho = -aposta

        else:  # Estratégia mista simples
            if "Tie" in resultado:
                ganho = aposta * 4
                win = True
            elif resultado in ["Player", "Banker"]:
                ganho = aposta
                win = True
            else:
                ganho = -aposta

        self.banca += ganho
        self.lucro_prejuizo.append(self.banca - self.banca_inicial)
        self.resultados_apostas.append(win)

        # Checa stop win / stop loss
        if self.stop_win is not None and self.banca >= self.banca_inicial + self.stop_win:
            self.parou = True
            st.warning(f"🚀 Stop Win atingido! Lucro de {self.banca - self.banca_inicial}.")
        elif self.stop_loss is not None and self.banca <= self.banca_inicial - self.stop_loss:
            self.parou = True
            st.error(f"⚠️ Stop Loss atingido! Prejuízo de {self.banca - self.banca_inicial}.")

        return ganho

    def relatorio_final(self):
        total_rodadas = len(self.resultados_apostas)
        acertos = sum(self.resultados_apostas)
        taxa_acerto = (acertos / total_rodadas * 100) if total_rodadas > 0 else 0
        lucro_total = self.banca - self.banca_inicial
        roi = (lucro_total / (self.aposta_unidade * total_rodadas) * 100) if total_rodadas > 0 else 0

        st.subheader("📊 RELATÓRIO FINAL")
        st.write(f"Rodadas jogadas: {total_rodadas}")
        st.write(f"Acertos: {acertos} ({taxa_acerto:.2f}%)")
        st.write(f"Lucro/Prejuízo final: {lucro_total}")
        st.write(f"Banca final: {self.banca}")
        st.write(f"ROI: {roi:.2f}%")

    def mostrar_dashboard(self):
        if not self.historico:
            st.info("Sem histórico para exibir.")
            return

        df = pd.Series(self.historico)
        contagem = df.value_counts()

        st.subheader("📊 Estatísticas de Resultados")
        st.bar_chart(contagem)

        st.subheader("💰 Evolução do Lucro/Prejuízo")
        st.line_chart(self.lucro_prejuizo)


# Interface Streamlit
st.title("🎲 Bac Bo AI - Simulador com Gestão de Banca")

aposta_unidade = st.sidebar.number_input("Valor da aposta (unidade)", min_value=1, value=5)
banca_inicial = st.sidebar.number_input("Banca inicial", min_value=50, value=200)
stop_win = st.sidebar.number_input("Stop Win (meta de lucro)", min_value=0, value=50)
stop_loss = st.sidebar.number_input("Stop Loss (limite de perda)", min_value=0, value=30)
rodadas = st.sidebar.number_input("Número de rodadas", min_value=10, value=50)

estrategia = st.sidebar.selectbox(
    "Estratégia de aposta",
    ["misto", "so_tie", "so_player", "so_banker"]
)

if st.button("Iniciar Simulação"):
    bacbo = BacBoAI(aposta_unidade=aposta_unidade, banca_inicial=banca_inicial,
                    stop_win=stop_win, stop_loss=stop_loss)

    for i in range(rodadas):
        resultado = bacbo.jogar_rodada()
        ganho = bacbo.aplicar_aposta(resultado, estrategia=estrategia)
        if bacbo.parou:
            break

    bacbo.mostrar_dashboard()
    bacbo.relatorio_final()
  
app.py app.py
