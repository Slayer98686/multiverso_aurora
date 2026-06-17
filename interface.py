import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (.env)
load_dotenv()

# Configuração da página do Streamlit
st.set_page_config(page_title="Multiverso Aurora", page_icon="✨", layout="centered")

# Inicializa o cliente do Gemini usando a nova biblioteca google-genai
@st.cache_resource
def obter_cliente_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Se não houver arquivo .env (como no site do Streamlit), tenta pegar dos Secrets do Streamlit
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key) if api_key else None

try:
    client = obter_cliente_gemini()
except Exception:
    client = None

# Função para carregar a persona do seu jeito configurado
def carregar_persona(nome_persona):
    # Procura na pasta 'persona' que você corrigiu no seu computador
    caminho = os.path.join("persona", f"{nome_persona}.txt")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    return "Você é um assistente prestativo."

# Interface Visual
st.title("👑 Multiverso Aurora")
st.caption("Escolha a sua persona e entre no núcleo cognitivo.")

# Descobrir quais personas existem na sua pasta 'persona' automaticamente
pasta_persona = "persona"
if os.path.exists(pasta_persona):
    arquivos_persona = [f.replace(".txt", "") for f in os.listdir(pasta_persona) if f.endswith(".txt")]
else:
    arquivos_persona = ["bolha", "luna"] # Forçando a Bolha e a Luna direto na lista para não ter erro

# Menu lateral para escolher a persona
persona_selecionada = st.sidebar.selectbox("🎭 Selecione a Persona:", arquivos_persona)
instrucao_sistema = carregar_persona(persona_selecionada)

# Exibe o status da conexão
if client:
    st.sidebar.success(f"⚡ Conectado à essência de: [{persona_selecionada.upper()}]")
else:
    st.sidebar.error("❌ Chave API do Gemini não configurada.")

# Inicializa o histórico de mensagens na tela se não existir
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

# Limpa o chat visual se mudar de persona para não misturar as conversas
if "persona_atual" not in st.session_state:
    st.session_state.persona_atual = persona_selecionada
elif st.session_state.persona_atual != persona_selecionada:
    st.session_state.historico_chat = []
    st.session_state.persona_atual = persona_selecionada

# Mostrar as mensagens anteriores na tela estilizada do Streamlit
for mensagem in st.session_state.historico_chat:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# Caixa de entrada para o usuário digitar
if prompt := st.chat_input("Envie uma mensagem para a inteligência..."):
    # Mostra a mensagem do usuário na tela
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.historico_chat.append({"role": "user", "content": prompt})

    if client:
        with st.chat_message("assistant"):
            placeholder_resposta = st.empty()
            try:
                # Prepara o contexto incluindo o histórico para a IA ter memória
                conteudos_para_envio = []
                # Passa a instrução do sistema no formato correto
                config_modelo = {"system_instruction": instrucao_sistema}
                
                # Alimenta o histórico na chamada
                for m in st.session_state.historico_chat:
                    conteudos_para_envio.append(m["content"])
                
                # Faz a chamada para o modelo flash estável do Gemini
                resposta = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=conteudos_para_envio,
                    config=config_modelo
                )
                
                texto_resposta = resposta.text
                placeholder_resposta.markdown(texto_resposta)
                st.session_state.historico_chat.append({"role": "assistant", "content": texto_resposta})
            except Exception as e:
                placeholder_resposta.error(f"Erro ao gerar resposta: {e}")
    else:
        st.error("Configure sua API Key para poder conversar.")