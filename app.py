import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd # Para lidar com a planilha

# Inicializa o aplicativo Dash
app = dash.Dash(__name__)

# --- Dados de Exemplo (Imagine que isso viria da sua planilha) ---
# Colegiados
colegiados_data = {
    'id': [1, 2, 3, 4, 5],
    'nome': ['Conselho de Inovação', 'Comitê de Sustentabilidade', 'Grupo de Trabalho Digital', 'Câmara Técnica de Infraestrutura', 'Conselho de Políticas Públicas'],
    'sigla': ['CI', 'CS', 'GTD', 'CTI', 'CPP'],
    'tipo': ['Conselho', 'Comitê', 'Grupo de Trabalho', 'Câmara Técnica', 'Conselho'],
    'status': ['Ativo', 'Ativo', 'Ativo', 'Inativo', 'Ativo']
}
df_colegiados = pd.DataFrame(colegiados_data)

# Participantes (Exemplo: Cada colegiado tem alguns participantes)
participantes_data = [
    {'colegiado_id': 1, 'nome': 'Maria Silva', 'cpf': '111.111.111-11', 'orgao': 'Min. X', 'cargo': 'Presidente', 'mandato': '2023-2025'},
    {'colegiado_id': 1, 'nome': 'João Pereira', 'cpf': '222.222.222-22', 'orgao': 'Min. Y', 'cargo': 'Membro', 'mandato': '2023-2025'},
    {'colegiado_id': 2, 'nome': 'Ana Costa', 'cpf': '333.333.333-33', 'orgao': 'Min. Z', 'cargo': 'Secretário', 'mandato': '2024-2026'},
    {'colegiado_id': 3, 'nome': 'Carlos Souza', 'cpf': '444.444.444-44', 'orgao': 'Org. K', 'cargo': 'Coordenador', 'mandato': '2023-2024'},
    {'colegiado_id': 3, 'nome': 'Paula Lima', 'cpf': '555.555.555-55', 'orgao': 'Org. L', 'cargo': 'Membro', 'mandato': '2023-2024'},
    {'colegiado_id': 5, 'nome': 'Roberto Santos', 'cpf': '666.666.666-66', 'orgao': 'Min. W', 'cargo': 'Membro', 'mandato': '2024-2026'},
]
df_participantes = pd.DataFrame(participantes_data)

# --- Layout do Aplicativo ---
app.layout = html.Div([
    # TOP HEADER (Similar ao da imagem)
    html.Div([
        html.Div("Assinatura", className="logo-placeholder"),
        html.Div("Título do Header", className="header-title"),
        html.Div([
            html.Div("O que você procura?", className="search-input-header"),
            html.Button("🔎", className="search-button-header")
        ], className="header-search-container")
    ], className="top-header"),

    # MAIN CONTENT AREA (Divisão lateral)
    html.Div([
        # LEFT SIDEBAR (Colegiados List)
        html.Div([
            html.H3("Colegiados", style={'padding': '15px 10px', 'margin': '0', 'color': 'white', 'background-color': '#0056b3'}),
            dcc.Input(
                id='search-colegiado-input',
                type='text',
                placeholder='🔎 Buscar colegiado...',
                style={'width': 'calc(100% - 20px)', 'padding': '8px', 'margin': '10px', 'border-radius': '5px', 'border': '1px solid #ccc'}
            ),
            html.Div(id='colegiados-list-container', style={'overflow-y': 'auto', 'height': 'calc(100% - 120px)'}),
        ], className="sidebar-left"), # Estilos seriam aplicados via CSS

        # RIGHT CONTENT AREA (Details of selected Colegiado)
        html.Div([
            html.Div(id='colegiado-details-content', style={'padding': '20px'})
        ], className="content-right") # Estilos seriam aplicados via CSS
    ], className="main-container"),

    # FOOTER (Similar ao da imagem)
    html.Div([
        html.Div([
            html.Div(".Img", className="footer-logo"),
            html.Div("TITULO", className="footer-title"),
            html.Div([
                html.Div("Imagem", className="footer-img-placeholder"),
                html.Div("Imagem", className="footer-img-placeholder")
            ], className="footer-images")
        ], className="footer-content"),
        html.P("Texto destinado a exibição das informações relacionadas a licença de uso.", className="footer-text")
    ], className="footer")
])

# --- Callbacks para interatividade ---

# Callback para filtrar a lista de colegiados
@app.callback(
    Output('colegiados-list-container', 'children'),
    Input('search-colegiado-input', 'value')
)
def update_colegiados_list(search_term):
    if not search_term:
        filtered_df = df_colegiados
    else:
        filtered_df = df_colegiados[
            df_colegiados['nome'].str.contains(search_term, case=False) |
            df_colegiados['sigla'].str.contains(search_term, case=False)
        ]

    # Cria uma lista de botões/links para cada colegiado
    list_items = []
    for index, row in filtered_df.iterrows():
        list_items.append(
            html.Button(
                f"{row['nome']} ({row['sigla']})",
                id={'type': 'colegiado-button', 'index': row['id']},
                className="colegiado-list-item", # Classe para estilização
                style={'width': '100%', 'padding': '10px', 'margin-bottom': '5px', 'border': 'none', 'background-color': 'transparent', 'text-align': 'left', 'cursor': 'pointer'}
            )
        )
    return list_items

# Callback para exibir os detalhes do colegiado selecionado
@app.callback(
    Output('colegiado-details-content', 'children'),
    Input({'type': 'colegiado-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'colegiado-button', 'index': dash.dependencies.ALL}, 'id')
)
def display_colegiado_details(n_clicks, button_ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.P("Selecione um colegiado na lista à esquerda para ver os detalhes.")

    # Descobre qual botão foi clicado
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    colegiado_id = eval(button_id)['index'] # Converte a string de volta para dicionário e pega o id

    colegiado_selecionado = df_colegiados[df_colegiados['id'] == colegiado_id].iloc[0]
    participantes_do_colegiado = df_participantes[df_participantes['colegiado_id'] == colegiado_id]

    return html.Div([
        html.H2(f"{colegiado_selecionado['nome']} ({colegiado_selecionado['sigla']})"),
        html.Div([
            html.Button("Editar Colegiado", id='edit-colegiado-btn', className="action-button"),
            html.Button("+ Adicionar Participante", id='add-participante-btn', className="action-button primary")
        ], style={'margin-bottom': '20px', 'display': 'flex', 'gap': '10px'}),

        html.H3("Informações Gerais"),
        html.P(f"Tipo: {colegiado_selecionado['tipo']}"),
        html.P(f"Status: {colegiado_selecionado['status']}"),
        # Adicione mais informações aqui conforme sua planilha

        html.H3("Participantes do Colegiado"),
        dash_table.DataTable(
            id='participantes-table',
            columns=[{"name": i, "id": i} for i in participantes_do_colegiado.drop(columns=['colegiado_id'], errors='ignore').columns],
            data=participantes_do_colegiado.drop(columns=['colegiado_id'], errors='ignore').to_dict('records'),
            style_table={'overflowX': 'auto', 'margin-top': '10px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'left', 'padding': '8px'}
        )
    ])


# --- CSS Básico para o visual GOV.BR (Embutido para simplicidade) ---
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%Metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body { font-family: 'Open Sans', sans-serif; margin: 0; background-color: #f0f2f5; }
            .top-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background-color: #004a8f; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .logo-placeholder { font-size: 1.5em; font-weight: bold; }
            .header-title { font-size: 1.2em; flex-grow: 1; text-align: center; }
            .header-search-container { display: flex; align-items: center; }
            .search-input-header { padding: 5px; border: none; border-radius: 3px; margin-right: 5px; }
            .search-button-header { background-color: #007bff; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer; }

            .main-container { display: flex; height: calc(100vh - 120px); } /* Ajuste altura considerando header e footer */
            .sidebar-left { width: 300px; background-color: #0056b3; color: white; padding-top: 0px; box-shadow: 2px 0 5px rgba(0,0,0,0.1); flex-shrink: 0; }
            .content-right { flex-grow: 1; padding: 20px; background-color: white; overflow-y: auto; }

            .colegiado-list-item {
                background-color: #0056b3; /* Cor padrão */
                color: white;
                border: none;
                padding: 12px 15px;
                text-align: left;
                width: 100%;
                cursor: pointer;
                border-bottom: 1px solid rgba(255,255,255,0.1);
                font-size: 1em;
                transition: background-color 0.2s ease-in-out;
            }
            .colegiado-list-item:hover {
                background-color: #0069d9; /* Mais claro no hover */
            }
            /* Adicionar classe para item selecionado via callback, se necessário */

            .action-button { background-color: #007bff; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; font-size: 0.9em; }
            .action-button.primary { background-color: #28a745; } /* Verde para adicionar */

            .footer { background-color: #004a8f; color: white; padding: 20px; text-align: center; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;}
            .footer-content { display: flex; align-items: center; gap: 20px; }
            .footer-logo { font-size: 1.2em; font-weight: bold; }
            .footer-title { font-size: 1em; }
            .footer-img-placeholder { width: 80px; height: 40px; background-color: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 0.8em; }
            .footer-images { display: flex; gap: 10px;}
            .footer-text { font-size: 0.8em; margin-top: 10px;}
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


# --- Rodar o aplicativo ---
if __name__ == '__main__':
    app.run(debug=True)