import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Importar layouts das páginas
from pages import colegiados, representantes

# --- Configuração do App Dash ---
# Para ícones do Font Awesome, você precisa de um link CSS externo.
# A classe 'active' para a sidebar será controlada por CSS e callbacks.
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css', # Ícones Font Awesome
    # Comentário: Adicione outras folhas de estilo CSS se necessário (ex: Bootstrap)
]
# Você também pode usar um arquivo CSS local na pasta 'assets'
# app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

# --- Componentes Comuns (Header e Footer) ---
# Cabeçalho - Replicando o visual das suas imagens
header = html.Div([
    html.Div([
        # Comentário: Coloque a imagem do logo gov.br aqui se tiver
        # html.Img(src="/assets/govbr-logo.png", className="logo-govbr"),
        html.Span("gov.br", className="logo-text"),
        html.Span("Sistema", className="sistema-text") # "Sistema de Colegiados e Participantes"
    ], className="header-left"),
    html.Div([
        # Comentário: Coloque os ícones de engrenagem e usuário aqui
        html.I(className="fas fa-cog header-icon"), # Ícone de engrenagem
        html.I(className="fas fa-user-circle header-icon"), # Ícone de usuário
        html.Span("João.Vera", className="user-name")
    ], className="header-right")
], className="app-header")

# Rodapé - O texto que aparece nas suas imagens
footer = html.Div([
    html.P("Texto destinado a exibição das informações relacionadas a licença de uso.", className="footer-text")
], className="app-footer")

# --- Layout Principal do Aplicativo ---
app.layout = html.Div([
    header, # Cabeçalho fixo

    html.Div([ # Container principal para Sidebar e Conteúdo
        # Sidebar Esquerda
        html.Div([
            html.Button([html.I(className="fas fa-sitemap"), html.Span(" Colegiados")], id='nav-colegiados', n_clicks=0, className="sidebar-button active"),
            html.Button([html.I(className="fas fa-users"), html.Span(" Representantes")], id='nav-representantes', n_clicks=0, className="sidebar-button"),
            # Comentário: Adicione mais botões de navegação aqui se precisar
        ], className="sidebar"),

        # Conteúdo Principal Dinâmico
        html.Div(id='page-content', className="content-area")
    ], className="main-content-container"), # Fechamento do main-content-container

    footer # Rodapé fixo
])

# --- Callbacks para Navegação e Interatividade ---

# Callback para mudar o conteúdo da página com base nos botões da sidebar
@app.callback(
    [Output('page-content', 'children'),
     Output('nav-colegiados', 'className'),
     Output('nav-representantes', 'className')],
    [Input('nav-colegiados', 'n_clicks'),
     Input('nav-representantes', 'n_clicks')]
)
def display_page(n_colegiados, n_representantes):
    ctx = dash.callback_context

    # Define as classes padrão para os botões (inativos)
    colegiados_btn_class = "sidebar-button"
    representantes_btn_class = "sidebar-button"

    # Determina qual botão foi clicado
    if not ctx.triggered:
        # Se nenhum botão foi clicado (primeira carga), exibe a página de colegiados
        colegiados_btn_class += " active"
        return colegiados.layout, colegiados_btn_class, representantes_btn_class
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'nav-colegiados':
            colegiados_btn_class += " active"
            return colegiados.layout, colegiados_btn_class, representantes_btn_class
        elif button_id == 'nav-representantes':
            representantes_btn_class += " active"
            return representantes.layout, colegiados_btn_class, representantes_btn_class
    
    # Fallback caso algo dê errado (deve ser rara com a lógica acima)
    colegiados_btn_class += " active"
    return colegiados.layout, colegiados_btn_class, representantes_btn_class

# Comentário: Adicione outros callbacks aqui para interações dentro das páginas
# Ex: Filtrar tabelas, ações de botões (editar/deletar), etc.

# --- Rodar o Aplicativo ---
if __name__ == '__main__':
    app.run(debug=True)