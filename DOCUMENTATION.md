## Pernambuco SUS Planning Dashboard — API, Components, and Usage Documentation

This repository contains two Dash applications that visualize and monitor health planning instruments for Pernambuco. The apps read a semicolon-separated CSV, provide interactive filters, KPIs, charts, a details table, and (in `app2.py`) an export-to-CSV feature.

### Quickstart

- **Requirements**: Python 3.9+ recommended.
- **Install dependencies**:
```bash
pip install dash plotly pandas
```
- **Place data**: Put `PERNAMBUCO.csv` in the project root (`/workspace`). It must be UTF-8 with BOM or UTF-8 and use `;` as a separator.
- **Run**:
  - Base dashboard: `python app.py`
  - Dashboard with CSV export: `python app2.py`
- **Open**: Visit `http://127.0.0.1:8050` in your browser.

### Data requirements

The application expects `PERNAMBUCO.csv` with at least the following columns (Portuguese headers):
- **TIPO_INSTRUMENTO**, **ESFERA**, **REGIAO**, **MACRORREGIAO**, **MUNICIPIO**, **EXERCICIO**, **FASE**, **SITUACAO**

At runtime, columns are trimmed and renamed to snake-case keys used throughout the app:
- `instrumento`, `esfera`, `regiao_saude`, `macrorregiao`, `municipio`, `exercicio`, `fase`, `situacao`

Minimal example header and two rows (note `;` separator):
```csv
TIPO_INSTRUMENTO;ESFERA;REGIAO;MACRORREGIAO;MUNICIPIO;EXERCICIO;FASE;SITUACAO
Plano Municipal;MUNICIPAL;IV;METROPOLITANA;Recife;2024;Elaboração;Aprovado
Relatório Anual;ESTADUAL;I;SERTAO;Arcoverde;2023;Avaliação;Em Análise
```

### Modules

- **`app.py`**: Base dashboard with filters, KPIs, 8 bar charts, and a details table.
- **`app2.py`**: Everything in `app.py` plus a CSV export button and download callback.

### UI components (IDs and purpose)

- **Filters (Dropdowns)**
  - `filtro-instrumento`: instrument type
  - `filtro-esfera`: government sphere
  - `filtro-regiao_saude`: health region
  - `filtro-macrorregiao`: macroregion
  - `filtro-municipio`: municipality
  - `filtro-exercicio`: exercise/year
  - `filtro-fase`: phase
  - `filtro-situacao`: status

- **KPIs**
  - `kpi-container`: container for 4 KPI cards

- **Charts (Bar charts)**
  - `graph-situacao`: by status
  - `graph-instrumento`: by instrument type
  - `graph-fase`: by phase
  - `graph-exercicio`: by exercise/year
  - `graph-esfera`: by sphere
  - `graph-macro`: by macroregion
  - `graph-regiao`: by health region (Top 15)
  - `graph-municipio`: by municipality (Top 15)

- **Table**
  - `tabela-detalhes`: details DataTable with columns `municipio`, `exercicio`, `fase`, `instrumento`, `situacao`, `regiao_saude`, `macrorregiao`

- **Export (only `app2.py`)**
  - `btn-exportar-csv`: button to export filtered data
  - `download-dataframe-csv`: hidden download target used by the export callback

### Public functions

- **`create_bar_chart(dff, column, title_base, top_n=None)`**
  - **Module**: `app.py`, `app2.py`
  - **Parameters**:
    - `dff` (pandas.DataFrame): filtered dataset
    - `column` (str): column to aggregate
    - `title_base` (str): plot title prefix
    - `top_n` (int | None): if provided, limit to top N categories
  - **Returns**: Plotly Figure dict; returns an annotated "Sem dados" placeholder when input is empty
  - **Behavior**: Counts non-null values, computes percent of valid values, shows count and percent as bar labels, sorts ascending, horizontal bars

- **`generate_dynamic_title_suffix(filters)`**
  - **Module**: `app.py`, `app2.py`
  - **Parameters**: `filters` (dict[str, list|scalar]) — keys among `instrumentos`, `esferas`, `regioes`, `macros`, `municipios`, `exercicios`, `fases`, `situacoes`
  - **Returns**: HTML string snippet like `<br><sub>(Instrumento: Plano, Esfera: MUNICIPAL)</sub>` summarizing active filters

- **`update_all_outputs(...)`**
  - **Module**: `app.py`, `app2.py`
  - **Dash callback**: Updates KPIs, table data, and 8 figures based on all filters
  - **Inputs**: values from all 8 dropdowns
  - **Outputs** (in order): `kpi-container.children`, `tabela-detalhes.data`, and 8 chart figures
  - **Behavior**: Applies filtering, computes KPIs (total, entities monitored, pending count, most frequent critical status), builds figures via `create_bar_chart`, formats `exercicio` as 4-digit string in table

- **`exportar_dados(...)`** (only `app2.py`)
  - **Dash callback**: Exports the currently filtered dataset to CSV
  - **Input**: `btn-exportar-csv.n_clicks`
  - **State**: same 8 filter values as `update_all_outputs`
  - **Output**: `dcc.send_data_frame` download payload named `dados_filtrados.csv` with `;` separator and UTF-8 BOM

### API summary table

| Symbol | Module | Type | Signature | Returns |
|---|---|---|---|---|
| `create_bar_chart` | `app.py`/`app2.py` | function | `(dff: DataFrame, column: str, title_base: str, top_n: int|None=None)` | Plotly Figure dict |
| `generate_dynamic_title_suffix` | `app.py`/`app2.py` | function | `(filters: dict)` | HTML string suffix |
| `update_all_outputs` | `app.py`/`app2.py` | Dash callback | Inputs: 8 filter values; Outputs: KPIs, table data, 8 figures | List + figures |
| `exportar_dados` | `app2.py` | Dash callback | Input: button clicks; State: 8 filter values | CSV download payload |

### Usage examples

- **Programmatic: build a chart from a DataFrame**
```python
import pandas as pd
from app import create_bar_chart

sample = pd.DataFrame({
    'municipio': ['Recife', 'Olinda', 'Recife', 'Caruaru'],
    'situacao': ['Aprovado', 'Em Análise', 'Aprovado', 'Aprovado'],
})
fig = create_bar_chart(sample, 'situacao', 'Por Situação')
# In a Dash context: dcc.Graph(figure=fig)
```

- **Running with your own CSV**
```bash
export PYTHONUNBUFFERED=1
python app2.py
# Open http://127.0.0.1:8050
```

- **CSV export (UI)**
  - Apply filters using the dropdowns.
  - Click "Exportar para CSV".
  - A file `dados_filtrados.csv` will be downloaded with current filters applied.

### Extending the app

- **Add a new filter**
  1. Build an `options_*` list from the DataFrame unique values.
  2. Add a `dcc.Dropdown` to the filters area with a unique ID (e.g., `filtro-novo_campo`).
  3. Add the new dropdown ID to the callback Inputs and replicate the corresponding `dff = dff[dff['novo_campo'].isin(values)]` line.

- **Add a new chart**
  1. Add `dcc.Graph(id='graph-novo')` to the layout.
  2. Add a new Output to the callback for that graph ID.
  3. Inside the callback, compute `fig_novo = create_bar_chart(dff, 'novo_campo', f'Por Novo Campo{title_suffix}')` and return it in order.

- **Change chart behavior**
  - Adjust `create_bar_chart` to modify labels, template, orientation, or sorting globally.

### Behavior and edge cases

- If the CSV is missing, the app prints `ERRO: O arquivo 'PERNAMBUCO.csv' não foi encontrado.` and exits.
- If filters result in no data, charts display a centered "Sem dados" message and KPIs show zeros.
- The details table formats `exercicio` as a four-digit string when possible.

### Notes

- UI text is in Portuguese to match the domain data; the API names (function and IDs) use English-friendly snake_case.
- `app.py` and `app2.py` share the same public functions; prefer `app2.py` if you need CSV export from the UI.