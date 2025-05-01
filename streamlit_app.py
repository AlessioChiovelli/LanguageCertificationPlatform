from __future__ import annotations
from PIL import Image
from time import sleep
from typing import Tuple
import streamlit as st
import io

from Utils.parse_command import parse_command

class ChatLLM:

    def __init__(self, api_key: str, model: str):
        """
        Inizializza i messaggi e mostra la cronologia e l'input.
        """
        self.api_key = api_key
        self.model = model
        if "messages" not in st.session_state:
            st.session_state.messages = []
        self.display_history()
        self.new_msg()

    @staticmethod
    def display_sidebar() -> Tuple[str | None, str]:
        """Prende la api key e il modello da user input."""
        st.sidebar.title("Impostazioni")
        api_key = st.sidebar.text_input("Inserisci la tua API Key", type="password")
        model = st.sidebar.selectbox("Seleziona il modello", ["gpt-4", "gpt-3.5-turbo", "altro"])
        if st.sidebar.button("Pulisci chat"):
            ChatLLM.clear_chat()
            st.rerun()
        return api_key, model
    
    def display_history(self):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if "attachments" in msg:
                    for att in msg["attachments"]:
                        if att["type"] == "image":
                            st.image(att["data"], caption=att["name"])
                        else:
                            st.download_button(
                                label=f"Scarica {att['name']}",
                                data=att["data"],
                                file_name=att["name"]
                            )

    @staticmethod
    def handle_attachments(uploaded_files):
        attachments = []
        for file in uploaded_files:
            file_type = "image" if file.type.startswith("image") else "file"
            data = file.read()
            if file_type == "image":
                img = Image.open(io.BytesIO(data))
                attachments.append({"type": "image", "data": img, "name": file.name})
            else:
                attachments.append({"type": "file", "data": data, "name": file.name})
        return attachments



    def new_msg(self):
        # Nuovo input chat con file
        message = st.chat_input(
            "Scrivi il tuo messaggio",
            accept_file=True,
            file_type=["png", "jpg", "jpeg", "pdf", "txt"]
        )

        if message:
            command = parse_command(message["text"])
            print(f'{command = }')
            if command:
                st.toast(f"Rilevato comando: {command}")
                sleep(1)
                
            user_input = message["text"]
            uploaded_files = message.get("files", [])
            attachments = self.handle_attachments(uploaded_files)

            self.add_message_to_history("user", user_input, attachments)

            llm_response = f"Input> {user_input}\n(Modello: {self.model})"
            if attachments:
                llm_response += f"\nHai allegato {len(attachments)} file."

            self.add_message_to_history("assistant", llm_response)
            st.rerun()

    def add_message_to_history(self, role, content, attachments=None):
        msg = {"role": role, "content": content}
        if attachments:
            msg["attachments"] = attachments
        st.session_state.messages.append(msg)

    @staticmethod
    def display_chat() -> None | ChatLLM:
        api_key, model = ChatLLM.display_sidebar()
        if not api_key:
            st.warning("Devi fornire un'Api key")
            return
        return ChatLLM(api_key, model)

    @staticmethod
    def clear_chat():
        st.session_state.messages = []

st.set_page_config(page_title="Chat LLM con Allegati", layout="wide")
st.title("Chat con LLM e Allegati")
ChatLLM.display_chat()