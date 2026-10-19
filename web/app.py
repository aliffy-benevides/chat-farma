from __future__ import annotations

import time

import streamlit as st

from src.api_client import chat, health
from src.config import get_api_url


st.set_page_config(
    page_title="Chat Farma",
    page_icon="💊",
    layout="centered",
)


def _init_state() -> None:
    if "messages" not in st.session_state:
        # Each item: {"role": "user"|"assistant", "content": str, "sources": list[...], "refused": bool}
        st.session_state.messages = []


def _render_header() -> None:
    st.title("Chat Farma — MVP")
    st.caption(
        "Chat de consulta/validação farmacoterapêutica com respostas baseadas exclusivamente nas fontes do MVP."
    )


def _render_sidebar() -> None:
    st.sidebar.header("Configuração")
    st.sidebar.write(f"**API:** {get_api_url()}")

    with st.sidebar.expander("Status da API", expanded=False):
        if st.sidebar.button("Checar /health"):
            try:
                info = health()
                st.sidebar.success("API OK")
                st.sidebar.json(info)
            except Exception as e:  # noqa: BLE001
                st.sidebar.error("Falha ao acessar a API")
                st.sidebar.write(str(e))

    st.sidebar.divider()
    st.sidebar.subheader("Boas práticas (LGPD)")
    st.sidebar.write(
        "Não insira dados identificáveis de pacientes (nome, CPF, prontuário, telefone, endereço)."
    )

    st.sidebar.divider()
    if st.sidebar.button("Limpar conversa"):
        st.session_state.messages = []
        st.rerun()


def _render_message(role: str, content: str, *, sources=None, refused: bool = False) -> None:
    with st.chat_message(role):
        st.markdown(content)

        if role == "assistant":
            if refused:
                st.info(
                    "Não encontrei evidência suficiente nas fontes do MVP para responder com segurança. "
                    "Tente reformular a pergunta com termos mais específicos."
                )

            if sources:
                with st.expander("Fontes usadas", expanded=False):
                    for i, s in enumerate(sources, start=1):
                        st.markdown(f"**{i}.** `{s['source_id']}`")
                        st.code(s["snippet"], language="text")


def main() -> None:
    _init_state()
    _render_header()
    _render_sidebar()

    # Replay chat history
    for m in st.session_state.messages:
        _render_message(
            m["role"],
            m["content"],
            sources=m.get("sources"),
            refused=bool(m.get("refused", False)),
        )

    user_text = st.chat_input("Digite sua pergunta clínica/farmacoterapêutica...")
    if not user_text:
        return

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_text})
    _render_message("user", user_text)

    # Call API and show assistant message
    with st.chat_message("assistant"):
        with st.spinner("Consultando fontes e gerando resposta..."):
            t0 = time.time()
            try:
                resp = chat(user_text)
                elapsed = time.time() - t0

                st.markdown(resp.answer)
                st.caption(f"Tempo: {elapsed:.2f}s")

                sources_payload = [s.model_dump() for s in resp.sources]

                if resp.refused:
                    st.info(
                        "Não encontrei evidência suficiente nas fontes do MVP para responder com segurança. "
                        "Tente reformular a pergunta com termos mais específicos."
                    )

                if sources_payload:
                    with st.expander("Fontes usadas", expanded=False):
                        for i, s in enumerate(sources_payload, start=1):
                            st.markdown(f"**{i}.** `{s['source_id']}`")
                            st.code(s["snippet"], language="text")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": resp.answer,
                        "sources": sources_payload,
                        "refused": resp.refused,
                    }
                )

            except Exception as e:  # noqa: BLE001
                st.error("Erro ao chamar a API /chat")
                st.write(str(e))


if __name__ == "__main__":
    main()
