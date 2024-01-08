import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

url = "https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv"
df = pd.read_csv(url, low_memory=False, on_bad_lines='skip')

app = dash.Dash(__name__)

# Choisir les 10 premiers livres qui apparaissent
top_10_books = df.head(10)

# Créer un graph en bar avec Plotly Express
fig = px.bar(top_10_books, x='title', y='  num_pages', title='Number of Pages for Top 10 Books')

app.layout = html.Div(children=[
    html.H1(children='Book Analysis Dashboard'),

    dcc.Graph(
        id='book-pages-bar-chart',
        figure=fig
    ),

    html.Label('Select Author:'),
    dcc.Dropdown(
        id='author-dropdown',
        options=[
            {'label': author, 'value': author} for author in df['authors'].unique()
        ],
        multi=True
    ),

    html.Label('Enter Maximum Pages:'),
    dcc.Input(
        id='max-pages-input',
        type='number',
        value=df['  num_pages'].max()
    )
])

# Callback pour le filtre par auteur et nombre de pages
@app.callback(
    Output('book-pages-bar-chart', 'figure'),
    [Input('author-dropdown', 'value'),
     Input('max-pages-input', 'value')]
)
def update_chart(selected_authors, max_pages):
    filtered_df = df

    if selected_authors:
        filtered_df = filtered_df[filtered_df['authors'].isin(selected_authors)]

    if max_pages is not None:
        filtered_df = filtered_df[filtered_df['  num_pages'] <= max_pages]

    fig = px.bar(filtered_df, x='title', y='  num_pages', title='Filtered Books')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)