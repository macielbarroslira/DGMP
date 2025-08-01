# Nome do arquivo: app.py

import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.express as px
import pandas as pd

# --- 1. Carregamento e Tratamento dos Dados ---
try:
    df = pd.read_csv('PERNAMBUCO.csv', sep=';', encoding='utf-8-sig', on_bad_lines='skip')
except FileNotFoundError:
    print("ERRO: O arquivo 'PERNAMBUCO.csv' não foi encontrado.")
    exit()

df.columns = df.columns.str.strip()
df.rename(columns={
    'TIPO_INSTRUMENTO': 'instrumento', 'ESFERA': 'esfera', 'REGIAO': 'regiao_saude',
    'MACRORREGIAO': 'macrorregiao', 'MUNICIPIO': 'municipio', 'EXERCICIO': 'exercicio',
    'FASE': 'fase', 'SITUACAO': 'situacao'
}, inplace=True)

for col in ['instrumento', 'esfera', 'regiao_saude', 'macrorregiao', 'municipio', 'fase', 'situacao']:
    if col in df.columns:
        df[col] = df[col].str.strip()

options_instrumento = [{'label': i, 'value': i} for i in sorted(df['instrumento'].dropna().unique())]
options_esfera = [{'label': i, 'value': i} for i in sorted(df['esfera'].dropna().unique())]
options_regiao_saude = [{'label': i, 'value': i} for i in sorted(df['regiao_saude'].dropna().unique()) if i]
options_macrorregiao = [{'label': i, 'value': i} for i in sorted(df['macrorregiao'].dropna().unique()) if i]
options_municipio = [{'label': i, 'value': i} for i in sorted(df['municipio'].dropna().unique()) if i]
options_exercicio = [{'label': str(int(i)), 'value': i} for i in sorted(df['exercicio'].dropna().unique())]
options_fase = [{'label': i, 'value': i} for i in sorted(df['fase'].dropna().unique())]
options_situacao = [{'label': i, 'value': i} for i in sorted(df['situacao'].dropna().unique())]

# --- 2. Inicialização e Estilos ---
app = dash.Dash(__name__)

card_style = {
    'backgroundColor': 'white', 'borderRadius': '8px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
    'padding': '20px', 'margin': '10px', 'position': 'relative'
}
filter_style = {'flex': '1 1 23%', 'padding': '5px'}

# --- 3. Layout do Dashboard de Visão Única ---
app.layout = html.Div(style={'backgroundColor': '#f4f6f9', 'fontFamily': 'Segoe UI, Arial, sans-serif'}, children=[
    html.Div([
        html.H1("Planejamento no SUS: Pernambuco", style={'color': '#003366'}),
        html.P("Monitoramento dos Instrumentos de Gestão", style={'color': '#555'})
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': 'white', 'marginBottom': '10px'}),

    html.Div(id='kpi-container', style={'display': 'flex', 'flexWrap': 'wrap'}),
    
    html.Div([
        html.H4("Filtros de Análise", style={'width': '100%', 'textAlign': 'center', 'marginBottom': '10px'}),
        html.Div([
            html.Div(dcc.Dropdown(id='filtro-instrumento', options=options_instrumento, multi=True, placeholder="Instrumento"), style=filter_style),
            html.Div(dcc.Dropdown(id='filtro-esfera', options=options_esfera, multi=True, placeholder="Esfera"), style=filter_style),
            html.Div(dcc.Dropdown(id='filtro-regiao_saude', options=options_regiao_saude, multi=True, placeholder="Região de Saúde"), style=filter_style),
            html.Div(dcc.Dropdown(id='filtro-macrorregiao', options=options_macrorregiao, multi=True, placeholder="Macrorregião"), style=filter_style),
        ], style={'display': 'flex', 'width': '100%'}),
        html.Div([
            html.Div(dcc.Dropdown(id='filtro-municipio', options=options_municipio, multi=True, placeholder="Município"), style=filter_style),
            html.Div(dcc.Dropdown(id='filtro-exercicio', options=options_exercicio, multi=True, placeholder="Exercício (Ano)"), style=filter_style),
            html.Div(dcc.Dropdown(id='filtro-fase', options=options_fase, multi=True, placeholder="Fase"), style=filter_style),
            html.Div(dcc.Dropdown(id='filtro-situacao', options=options_situacao, multi=True, placeholder="Situação"), style=filter_style),
        ], style={'display': 'flex', 'width': '100%'}),
    ], style={**card_style, 'display': 'flex', 'flexWrap': 'wrap'}),

    html.Div([
        html.Div([
            html.Div(dcc.Graph(id='graph-situacao'), style=card_style),
            html.Div(dcc.Graph(id='graph-instrumento'), style=card_style),
            html.Div(dcc.Graph(id='graph-fase'), style=card_style),
            html.Div(dcc.Graph(id='graph-exercicio'), style=card_style),
        ], style={'flex': '1'}),
        html.Div([
            html.Div(dcc.Graph(id='graph-esfera'), style=card_style),
            html.Div(dcc.Graph(id='graph-macro'), style=card_style),
            html.Div(dcc.Graph(id='graph-regiao'), style=card_style),
            html.Div(dcc.Graph(id='graph-municipio'), style=card_style),
        ], style={'flex': '1'}),
    ], style={'display': 'flex', 'flexWrap': 'wrap'}),

    html.Div([
        html.Div([
            html.H4("Tabela de Detalhes", style={'textAlign': 'center', 'flex': '1'}),
            # BOTÃO DE EXPORTAÇÃO ADICIONADO AQUI
            html.Button("Exportar para CSV", id="btn-exportar-csv", style={'margin-bottom': '10px'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),
        
        dash_table.DataTable(
            id='tabela-detalhes',
            columns=[{'name': col.replace('_', ' ').title(), 'id': col} for col in ['municipio', 'exercicio', 'fase', 'instrumento', 'situacao', 'regiao_saude', 'macrorregiao']],
            page_size=20, sort_action="native", filter_action="native",
            style_cell={'textAlign': 'left'}, style_header={'fontWeight': 'bold'},
        ),
        # COMPONENTE DE DOWNLOAD INVISÍVEL
        dcc.Download(id="download-dataframe-csv"),
    ], style=card_style)
])

# --- 4. Função Auxiliar para criar gráficos ---
def create_bar_chart(dff, column, title_base, top_n=None):
    fig_vazia = {"layout": {"annotations": [{"text": "Sem dados", "showarrow": False, "font": {"size": 20}}]}}
    if dff.empty or column not in dff.columns or dff[column].dropna().empty:
        return fig_vazia

    counts = dff[column].dropna().value_counts()
    if top_n:
        counts = counts.nlargest(top_n)

    data_to_plot = counts.reset_index()
    data_to_plot.columns = [column, 'count']
    total_valid = len(dff.dropna(subset=[column]))
    data_to_plot['percent'] = (data_to_plot['count'] / total_valid) * 100
    data_to_plot['text'] = data_to_plot.apply(lambda row: f" {row['count']} ({row['percent']:.1f}%)", axis=1)

    fig = px.bar(data_to_plot.sort_values(by='count'), y=column, x='count', text='text', title=title_base, template='plotly_white', orientation='h')
    
    max_val = data_to_plot['count'].max()
    fig.update_layout(
        title_x=0.5, margin=dict(l=20, r=20, t=60, b=20), yaxis={'categoryorder':'total ascending'}, 
        xaxis_title=None, yaxis_title=None, xaxis_range=[0, max_val * 1.25]
    )
    fig.update_traces(textposition='outside', textfont_size=10)
    return fig

def generate_dynamic_title_suffix(filters):
    parts = []
    max_items_to_list = 2
    filter_labels = {
        'instrumentos': 'Instrumento', 'esferas': 'Esfera', 'regioes': 'Região de Saúde',
        'macros': 'Macrorregião', 'municipios': 'Município', 'exercicios': 'Exercício',
        'fases': 'Fase', 'situacoes': 'Situação'
    }
    for name, value in filters.items():
        if value:
            label = filter_labels.get(name, name.title())
            if isinstance(value, list):
                if len(value) > max_items_to_list:
                    parts.append(f"{len(value)} {label}s")
                else:
                    str_values = [str(v) for v in value]
                    parts.append(f"{label}: {', '.join(str_values)}")
            else:
                parts.append(f"{label}: {value}")
    if not parts:
        return ""
    return f"<br><sub>({', '.join(parts)})</sub>"

# --- 5. Callback Principal (Atualiza Gráficos, KPIs e Tabela) ---
@app.callback(
    [Output('kpi-container', 'children'), Output('tabela-detalhes', 'data'),
     Output('graph-situacao', 'figure'), Output('graph-instrumento', 'figure'),
     Output('graph-fase', 'figure'), Output('graph-exercicio', 'figure'),
     Output('graph-esfera', 'figure'), Output('graph-macro', 'figure'),
     Output('graph-regiao', 'figure'), Output('graph-municipio', 'figure')],
    [Input(f'filtro-{col}', 'value') for col in ['instrumento', 'esfera', 'regiao_saude', 'macrorregiao', 'municipio', 'exercicio', 'fase', 'situacao']]
)
def update_all_outputs(instrumentos, esferas, regioes, macros, municipios, exercicios, fases, situacoes):
    dff = df.copy()

    if instrumentos: dff = dff[dff['instrumento'].isin(instrumentos)]
    if esferas: dff = dff[dff['esfera'].isin(esferas)]
    if regioes: dff = dff[dff['regiao_saude'].isin(regioes)]
    if macros: dff = dff[dff['macrorregiao'].isin(macros)]
    if municipios: dff = dff[dff['municipio'].isin(municipios)]
    if exercicios: dff = dff[dff['exercicio'].isin(exercicios)]
    if fases: dff = dff[dff['fase'].isin(fases)]
    if situacoes: dff = dff[dff['situacao'].isin(situacoes)]

    fig_vazia = {"layout": {"annotations": [{"text": "Sem dados para esta seleção", "showarrow": False, "font": {"size": 20}}]}}
    if dff.empty:
        kpis = [
            html.Div([html.H3("Total de Instrumentos"), html.H4(0)], style={**card_style, 'textAlign': 'center', 'flex': 1}),
            html.Div([html.H3("Entidades Monitoradas"), html.H4(0)], style={**card_style, 'textAlign': 'center', 'flex': 1}),
            html.Div([html.H3("Instrumentos Pendentes"), html.H4(0, style={'color': '#d9534f'})], style={**card_style, 'textAlign': 'center', 'flex': 1}),
            html.Div([html.H3("Situação Crítica"), html.H4("N/A", style={'color': '#f0ad4e'})], style={**card_style, 'textAlign': 'center', 'flex': 1}),
        ]
        return kpis, [], fig_vazia, fig_vazia, fig_vazia, fig_vazia, fig_vazia, fig_vazia, fig_vazia, fig_vazia

    total_instrumentos = len(dff)
    entidades_monitoradas = dff['municipio'].nunique() + dff[dff['esfera'] == 'ESTADUAL']['esfera'].nunique()
    situacoes_ok = ["Aprovado", "Avaliado", "Homologado pelo Gestor Estadual", "Aprovado com Ressalvas"]
    pendentes_df = dff[~dff['situacao'].isin(situacoes_ok)]
    total_pendentes = len(pendentes_df)
    situacao_critica = pendentes_df['situacao'].mode()[0] if not pendentes_df.empty else "Nenhuma"
    kpis = [
        html.Div([html.H3("Total de Instrumentos"), html.H4(total_instrumentos)], style={**card_style, 'textAlign': 'center', 'flex': 1}),
        html.Div([html.H3("Entidades Monitoradas"), html.H4(entidades_monitoradas)], style={**card_style, 'textAlign': 'center', 'flex': 1}),
        html.Div([html.H3("Instrumentos Pendentes"), html.H4(total_pendentes, style={'color': '#d9534f'})], style={**card_style, 'textAlign': 'center', 'flex': 1}),
        html.Div([html.H3("Situação Crítica"), html.H4(situacao_critica, style={'color': '#f0ad4e'})], style={**card_style, 'textAlign': 'center', 'flex': 1}),
    ]

    active_filters = {'instrumentos': instrumentos, 'esferas': esferas, 'regioes': regioes, 'macros': macros, 'municipios': municipios, 'exercicios': exercicios, 'fases': fases, 'situacoes': situacoes}
    title_suffix = generate_dynamic_title_suffix(active_filters)

    fig_situacao = create_bar_chart(dff, 'situacao', f'Por Situação{title_suffix}')
    fig_instrumento = create_bar_chart(dff, 'instrumento', f'Por Instrumento{title_suffix}')
    fig_fase = create_bar_chart(dff, 'fase', f'Por Fase{title_suffix}')
    fig_exercicio = create_bar_chart(dff, 'exercicio', f'Por Exercício{title_suffix}')
    fig_esfera = create_bar_chart(dff, 'esfera', f'Por Esfera{title_suffix}')
    fig_macro = create_bar_chart(dff, 'macrorregiao', f'Por Macrorregião{title_suffix}')
    fig_regiao = create_bar_chart(dff, 'regiao_saude', f'Por Região de Saúde (Top 15){title_suffix}', top_n=15)
    fig_municipio = create_bar_chart(dff, 'municipio', f'Por Município (Top 15){title_suffix}', top_n=15)
    
    tabela_df = dff[['municipio', 'exercicio', 'fase', 'instrumento', 'situacao', 'regiao_saude', 'macrorregiao']].copy()
    tabela_df['exercicio'] = tabela_df['exercicio'].apply(lambda x: str(int(x)) if pd.notna(x) else 'N/A')
    tabela_data = tabela_df.to_dict('records')

    return kpis, tabela_data, fig_situacao, fig_instrumento, fig_fase, fig_exercicio, fig_esfera, fig_macro, fig_regiao, fig_municipio

# --- 6. Novo Callback para o Botão de Exportação ---
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-exportar-csv", "n_clicks"),
    [State(f'filtro-{col}', 'value') for col in ['instrumento', 'esfera', 'regiao_saude', 'macrorregiao', 'municipio', 'exercicio', 'fase', 'situacao']],
    prevent_initial_call=True,
)
def exportar_dados(n_clicks, instrumentos, esferas, regioes, macros, municipios, exercicios, fases, situacoes):
    dff = df.copy()

    # Aplica a mesma lógica de filtragem do callback principal
    if instrumentos: dff = dff[dff['instrumento'].isin(instrumentos)]
    if esferas: dff = dff[dff['esfera'].isin(esferas)]
    if regioes: dff = dff[dff['regiao_saude'].isin(regioes)]
    if macros: dff = dff[dff['macrorregiao'].isin(macros)]
    if municipios: dff = dff[dff['municipio'].isin(municipios)]
    if exercicios: dff = dff[dff['exercicio'].isin(exercicios)]
    if fases: dff = dff[dff['fase'].isin(fases)]
    if situacoes: dff = dff[dff['situacao'].isin(situacoes)]

    # Converte o DataFrame filtrado para CSV e envia para download
    return dcc.send_data_frame(dff.to_csv, "dados_filtrados.csv", index=False, sep=';', encoding='utf-8-sig')


# --- 7. Execução do Servidor ---
if __name__ == '__main__':
    app.run(debug=True)
