import streamlit as st

# Configuração da página web
st.set_page_config(page_title="Fluxo de Caixa", page_icon="💰", layout="centered")

st.title("💰 Sistema de Fluxo de Caixa")
st.write("Insira os produtos para calcular os custos e lucros automaticamente.")

# Inicializa a lista de produtos na memória da página, se não existir
if 'lista_produtos' not in st.session_state:
    st.session_state.lista_produtos = []

# Formulário para entrada de dados (organizado de forma simples para celular)
with st.form(key="form_produto", clear_on_submit=True):
    nome = st.text_input("Nome do Produto:").strip()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        custo_pacote = st.number_input("Valor do Pacote (R$):", min_value=0.0, step=0.10, format="%.2f")
    with col2:
        unidades = st.number_input("Unidades no Pacote:", min_value=1, step=1)
    with col3:
        venda_un = st.number_input("Venda da Unidade (R$):", min_value=0.0, step=0.10, format="%.2f")
        
    botao_adicionar = st.form_submit_button(label="Adicionar Produto")

# Lógica para salvar o produto quando clicar no botão
if botao_adicionar and nome:
    custo_un = custo_pacote / unidades
    faturamento_pacote = venda_un * unidades
    lucro_total_produto = faturamento_pacote - custo_pacote
    lucro_un = venda_un - custo_un
    
    st.session_state.lista_produtos.append({
        'PRODUTO': nome.upper(),
        'CUSTO UN.': f"R$ {custo_un:.2f}",
        'VENDA UN.': f"R$ {venda_un:.2f}",
        'LUCRO UN.': f"R$ {lucro_un:.2f}",
        'LUCRO TOTAL': f"R$ {lucro_total_produto:.2f}",
        'custo_raw': custo_pacote,          # guardado para a soma final
        'lucro_raw': lucro_total_produto     # guardado para a soma final
    })
    st.success(f"{nome.upper()} adicionado com sucesso!")

# Se já houver produtos na lista, mostra a tabela e os totais
if st.session_state.lista_produtos:
    st.write("### 📊 Tabela de Produtos")
    
    # Exibe os dados em formato de tabela web com a nova coluna de Lucro Unitário
    st.dataframe(
        st.session_state.lista_produtos, 
        column_order=['PRODUTO', 'CUSTO UN.', 'VENDA UN.', 'LUCRO UN.', 'LUCRO TOTAL']
    )
    
    # Calcula os totais acumulados
    investimento_geral = sum(p['custo_raw'] for p in st.session_state.lista_produtos)
    lucro_geral = sum(p['lucro_raw'] for p in st.session_state.lista_produtos)
    
    st.markdown("---")
    col_tot1, col_tot2 = st.columns(2)
    col_tot1.metric(label="INVESTIMENTO TOTAL", value=f"R$ {investimento_geral:.2f}")
    col_tot2.metric(label="LUCRO TOTAL ACUMULADO", value=f"R$ {lucro_geral:.2f}")
    
    st.markdown("---")
    
    # --- LÓGICA DO BOTÃO DE COPIAR TUDO ---
    # Criando o texto formatado para o WhatsApp ou Bloco de Notas
    texto_copiar = "📋 *RELATÓRIO DE FLUXO DE CAIXA*\n\n"
    for p in st.session_state.lista_produtos:
        texto_copiar += f"🔹 *{p['PRODUTO']}*\n"
        texto_copiar += f"  - Custo Un: {p['CUSTO UN.']}\n"
        texto_copiar += f"  - Venda Un: {p['VENDA UN.']}\n"
        texto_copiar += f"  - Lucro Un: {p['LUCRO UN.']}\n"
        texto_copiar += f"  - Lucro Lote: {p['LUCRO TOTAL']}\n\n"
    
    texto_copiar += f"💰 *INVESTIMENTO TOTAL:* R$ {investimento_geral:.2f}\n"
    texto_copiar += f"📈 *LUCRO TOTAL ACUMULADO:* R$ {lucro_geral:.2f}"
    
    # Botões de ação lado a lado (Copiar e Limpar)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        st.copy_to_clipboard(texto_copiar, text="📋 Copiar Relatório")
    with col_btn2:
        if st.button("🗑️ Limpar Tudo"):
            st.session_state.lista_produtos = []
            st.rerun()
            
