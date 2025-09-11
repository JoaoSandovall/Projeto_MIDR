from dash import dcc, html, dash_table
import pandas as pd
from data.data import df_colegiados, cnrh_details

layout = html.Div([
    html.Div([ # Cabeçalho da área de conteúdo principal para colegiados
        html.Div([
            html.H4("Informações Gerais", className="info-gerais-title"), # Título "Informações Gerais"
            html.H2(cnrh_details['colegiado_nome'], className="colegiado-main-title") # Nome do colegiado selecionado
        ], className="title-section-colegiados"),

        html.Div([
            html.Div([
                html.Span("Nível: ", className="info-label"),
                html.Span(cnrh_details['nivel'], className="info-value")
            ], className="info-item"),
            html.Div([
                html.Span("Função: ", className="info-label"),
                html.Span(cnrh_details['funcao'], className="info-value")
            ], className="info-item"),
            html.Div([
                html.Span("Tema: ", className="info-label"),
                html.Span(cnrh_details['tema'], className="info-value")
            ], className="info-item"),
            html.Div([
                html.Span("Coordenação: ", className="info-label"),
                html.Span(cnrh_details['coordenacao'], className="info-value")
            ], className="info-item"),
            html.Div([
                html.Span("Total Representantes: ", className="info-label"),
                html.Span(str(cnrh_details['total_representantes']), className="info-value")
            ], className="info-item"),
            html.A(
                "Link do Normativo",
                href=cnrh_details['link_normativo'],
                target="_blank", # Abre em nova aba
                className="link-normativo" # Classe para estilizar o link como um botão ou texto formatado
            )
        ], className="general-info-card-colegiados"),
    ], className="header-details-colegiado-page"), # Container para a seção de detalhes gerais

    # Tabela de Colegiados
    html.Div([
        dash_table.DataTable(
            id='table-colegiados',
            columns=[
                {"name": "Colegiado", "id": "colegiado"},
                {"name": "Status", "id": "status"},
                {"name": "Número de Representantes", "id": "numero_representantes"},
                {"name": "Ações", "id": "acoes", "presentation": "markdown"}
            ],
            data=df_colegiados.assign(
                acoes=[
                    # Comentário: Troque 'javascript:void(0)' por uma URL ou callback real para as ações
                    # Ícone de Olho (Visualizar)
                    f'[<i class="fas fa-eye"></i>](javascript:void(0)){{.view-btn}} '
                    # Ícone de Lápis (Editar)
                    f'[<i class="fas fa-edit"></i>](javascript:void(0)){{.edit-btn}} '
                    # Ícone de Lixeira (Deletar)
                    f'[<i class="fas fa-trash-alt"></i>](javascript:void(0)){{.delete-btn}}'
                    for _ in range(len(df_colegiados))
                ]
            ).to_dict('records'),
            filter_action="native", # Habilita filtros nativos por coluna
            sort_action="native",
            style_table={'overflowX': 'auto', 'marginTop': '20px'},
            style_header={
                'backgroundColor': '#e8edf3', # Cor de fundo mais clara para o cabeçalho
                'fontWeight': 'bold',
                'textAlign': 'left',
                'padding': '10px 18px',
                'borderBottom': '2px solid #ddd'
            },
            style_cell={
                'textAlign': 'left',
                'padding': '10px 18px',
                'borderBottom': '1px solid #eee'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(250, 250, 250)'
                }
            ],
            row_selectable="single" # Permite selecionar uma linha
        )
    ], className="content-table-colegiados")
])