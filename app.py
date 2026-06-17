import sys
from cerebro.config import obter_cliente_gemini, carregar_instrucao_persona, criar_configuracao_chat

def iniciar_multiverso():
    print("="*50)
    print("👑 SISTEMA AURORA — ENTRANDO NO NÚCLEO COGNITIVO 👑")
    print("="*50)

    # 1. Define qual persona vai rodar (mude para 'bolha' ou 'luna')
    persona_ativa = "luna" 

    # 2. Carrega as configurações dos módulos
    instrucao = carregar_instrucao_persona(persona_ativa)
    if not instrucao:
        print("❌ Erro crítico: Não foi possível carregar a essência da persona.")
        return

    # 3. Inicializa o cliente e a configuração da IA
    client = obter_cliente_gemini()
    configuracao = criar_configuracao_chat(instrucao)

    # 4. Cria o chat usando o modelo mais recente e estável (gemini-2.5-flash)
    print(f"✨ Conectando ao filtro de linguagem de: [{persona_ativa.upper()}]...")
    chat = client.chats.create(model="gemini-2.5-flash", config=configuracao)
    print("🚀 Conexão estabelecida! Digite 'sair' para encerrar.\n")

    # 5. Loop de conversa
    while True:
        try:
            entrada = input("Você: ")
            if entrada.lower() in ["sair", "exit"]:
                print(f"\n🌙 Desconectando do multiverso de {persona_ativa.capitalize()}...")
                break
            
            if not entrada.strip():
                continue

            # Envia para a IA e exibe a resposta com a personalidade aplicada
            resposta = chat.send_message(entrada)
            print(f"\n{resposta.text}\n" + "-"*30)

        except KeyboardInterrupt:
            print("\n\n⚔️ Conexão interrompida pelo console.")
            sys.exit(0)

if __name__ == "__main__":
    iniciar_multiverso()