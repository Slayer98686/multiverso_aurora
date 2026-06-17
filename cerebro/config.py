import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carrega a chave do .env
load_dotenv()

def obter_cliente_gemini():
    """Inicializa o cliente oficial da API."""
    return genai.Client()

def carregar_instrucao_persona(nome_persona):
    """Lê o arquivo de texto da persona na pasta correspondente."""
    caminho = os.path.join("personas", f"{nome_persona}.txt")
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"⚠️ Alerta: Arquivo de persona não encontrado em {caminho}")
        return ""

def criar_configuracao_chat(texto_instrucao):
    """Monta a configuração do sistema do Gemini com a persona escolhida."""
    return types.GenerateContentConfig(
        system_instruction=texto_instrucao,
        temperature=0.7
    )