import pandas as pd

# df_colegiados (Baseado na Imagem 2)
colegiados_data = {
    'colegiado': [
        'Comitê de Integração de Políticas Ambientais (CIPAM)',
        'Comitê de mobilidade, habitação, infraestrutura econômica e urbana',
        'Conselho Nacional de Recursos Hídricos (CNRH)',
        'Comitê-Executivo do Programa de Proteção Integrada de Fronteiras (CEPPIF)',
        'Conselho Nacional de Turismo (CNT)',
        'Estratégia Brasil 2050',
        'Grupo de Trabalho - GT Calamidades e Situações de Emergências',
        'Grupo Técnico de Trabalho (GTT) sobre Territórios e Participação Social nas Políticas Públicas do Governo Federal',
        'Subcomitês de infraestrutura econômica e urbana (COARIDE)'
    ],
    'status': ['Ativo', 'Em estruturação', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo'],
    'numero_representantes': [8, 0, 20, 10, 4, 8, 2, 6, 8],
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9] # ID para seleção e detalhes
}
df_colegiados = pd.DataFrame(colegiados_data)

# Detalhes de um Colegiado (para simular o CNRH selecionado na Imagem 2)
cnrh_details = {
    'colegiado_nome': 'Conselho Nacional de Recursos Hídricos (CNRH)',
    'nivel': 'Principal',
    'funcao': 'Interministerial',
    'tema': 'Segurança Hídrica',
    'coordenacao': 'Ministério da Integração e do Desenvolvimento Regional',
    'link_normativo': 'https://www.planalto.gov.br/ccivil_03/_Ato2023-2026/2024/Decreto/D11960.htm#art12',
    'total_representantes': 20
}


# df_representantes (Baseado na Imagem 1)
representantes_data = {
    'nome': ['João', 'Marina', 'Cleber', 'Pedro', 'Maria', 'Clésio', 'Vagner', 'Sabrina'],
    'status': ['Ativo', 'Inativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Ativo', 'Inativo'],
    'total_representacoes': [3, 5, 2, 1, 6, 10, 2, 3],
    'id': [101, 102, 103, 104, 105, 106, 107, 108] # ID para ações
}
df_representantes = pd.DataFrame(representantes_data)

# Informações Gerais dos Representantes (Baseado na Imagem 1)
representantes_info_gerais = {
    'total_representacoes': 820,
    'total_titulares': 400,
    'total_suplentes': 400,
    'total_pontos_focais': 20
}