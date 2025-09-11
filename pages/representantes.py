from dash import dcc, html, dash_table
import pandas as pd
from data.data import df_representantes, representantes_info_gerais

layout = html.Div([
    html.Div([ # Cabeçalho da área de conteúdo principal para Representantes
        html.H4("Representantes", className="main-content-title"), # Título "Representantes"
        html.Div([
            html.H5("Informações Gerais", className="info-gerais-representantes-title"), # Subtítulo
            html.Div([
                html.Div([
                    html.Span("Total de Representações: ", className="info-label-rep"),
                    html.Span(str(representantes_info_gerais['total_representacoes']), className="info-value-rep")
                ], className="info-item-rep"),
                html.Div([
                    html.Span("Total de Titulares: ", className="info-label-rep"),
                    html.Span(str(representantes_info_gerais['total_titulares']), className="info-value-rep")
                ], className="info-item-rep"),
                html.Div([
                    html.Span("Total de Suplentes: ", className="info-label-rep"),
                    html.Span(str(representantes_info_gerais['total_suplentes']), className="info-value-rep")
                ], className="info-item-rep"),
                html.Div([
                    html.Span("Total de Pontos Focais: ", className="info-label-rep"),
                    html.Span(str(representantes_info_gerais['total_pontos_focais']), className="info-value-rep")
                ], className="info-item-rep"),
            ], className="general-info-card-representantes") # Card para informações gerais
        ], className="header-details-representantes-page")
    ], className="header-representantes-section"),


    html.Div([ # Barra de busca e botão "Adicionar"
        dcc.Input(
            id='search-representante-input',
            type='text',
            placeholder='Pesquisar representante...',
            className="form-control search-input"
        ),
        html.Button([html.I(className="fas fa-plus"), " Adicionar Participante"], id='add-participante-btn', className="btn btn-success add-button") # Ícone de +
    ], className="search-bar-representantes"),

    # Tabela de Representantes
    dash_table.DataTable(
        id='table-representantes',
        columns=[
            {"name": "Representante", "id": "nome"},
            {"name": "Status", "id": "status"},
            {"name": "Total de Representações", "id": "total_representacoes"},
            {"name": "Ações", "id": "acoes", "presentation": "markdown"}
        ],
        data=df_representantes.assign(
            acoes=[
                # Comentário: Troque 'javascript:void(0)' por uma URL ou callback real para as ações
                # Ícone de Lápis (Editar)
                f'[<i class="fas fa-edit"></i>](javascript:void(0)){{.edit-btn}} '
                # Ícone de Lixeira (Deletar)
                f'[<i class="fas fa-trash-alt"></i>](javascript:void(0)){{.delete-btn}}'
                for _ in range(len(df_representantes))
            ]
        ).to_dict('records'),
        filter_action="native",
        sort_action="native",
        style_table={'overflowX': 'auto', 'marginTop': '20px'},
        style_header={
            'backgroundColor': '#e8edf3',
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
        ]
    )
])