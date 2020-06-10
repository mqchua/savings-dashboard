import pandas as pd
import plotly.graph_objects as go
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

app = dash.Dash(__name__, assets_folder='./assets/', external_stylesheets=[BS])

app.title = 'Monthly Expenses'

server = app.server

# Reading data

xls = pd.ExcelFile("test_output.xlsx",)
df_history = pd.read_excel(xls, 'Sheet1', index_col=0)
df_expenses = pd.read_excel(xls, 'Sheet2', index_col=0)


month = df_expenses.Month.tolist()
savings = df_expenses.Savings.tolist()
wedding = df_expenses.Wedding.tolist()
renovation = df_expenses.Renovation.tolist()

spending_label = df_expenses.columns.tolist()[2:9]

# PLOT 2

fig_total = go.Figure()

# Add trace to the figure

fig_total.add_trace(go.Scatter(x=df_expenses['Month'], y=df_expenses['Wedding'], name='Wedding',
                               mode='lines+markers',
                               line_shape='spline',
                               line=dict(color='rgb(125, 164, 255)', width=2),
                               marker=dict(size=2, color='rgb(125, 164, 255)',
                                           line=dict(width=.5, color='rgb(125, 164, 255)')),
                               ))

fig_total.add_trace(go.Scatter(x=df_expenses['Month'], y=df_expenses['Renovation'], name='Renovation',
                               mode='lines+markers',
                               line_shape='spline',
                               line=dict(color='#f0953f', width=2),
                               marker=dict(size=2, color='#f0953f',
                                           line=dict(width=.5, color='#f0953f')),
                               ))

fig_total.update_layout(

    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),

    xaxis=dict(
        showline=True),


    xaxis_tickformat='%b %d',
    hovermode='x unified',
    legend_orientation="h",
    legend=dict(x=.27, y=-0.1),
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)


# APP LAYOUT

app.layout = html.Div(
    id='app-body',
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(
                    id='header-title',
                    children="June Expenses"),
                # html.H3(
                #     id="description",
                #     children=dcc.Markdown(
                #         children=(
                #             '''
                #             This is a monthly savings tracker.
                #             ''',
                #         )
                #     )
                # ),
                # html.Hr(
                # ),
            ]
        ),

        html.Div(
            className="number-plate",
            children=[
                html.Div(
                    className='number-plate-single',
                    style={'border-top': '#292929 solid .2rem', },
                    children=[
                        html.H5(
                            style={'color': '#292929', },
                            children="Expenses"
                        ),
                        html.H3(
                            style={'color': '#292929'},
                            children=[
                                '$1,200',
                                html.P(
                                    style={'color': '#ffffff', },
                                    children='xxxx xx xxx xxxx xxx xxxxx'
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-active',
                    style={'border-top': '#2ecc77 solid .2rem', },
                    children=[
                        html.H5(
                            style={'color': '#2ecc77'},
                            children="Savings"
                        ),
                        html.H3(
                            style={'color': '#2ecc77'},
                            children=[
                                '+$300',
                                html.P(
                                    # children='+ {:,d} in the past 24h ({:.1%})'.format(
                                    #     plusRemainNum, plusRemainNum3) if plusRemainNum > 0 else '{:,d} in the past 24h ({:.1%})'.format(plusRemainNum, plusRemainNum3)
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-confirm',
                    style={'border-top': 'rgb(125, 164, 255) solid .2rem', },
                    children=[
                        html.H5(
                            style={'color': 'rgb(125, 164, 255)'},
                            children="Wedding"
                        ),
                        html.H3(
                            style={'color': 'rgb(125, 164, 255)'},
                            children=[
                                '$10,500',
                                html.P(
                                    children='+ $4,500 from target'
                                ),
                                html.P(
                                    children='Months left: 5'
                                )

                            ]
                        ),

                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-recover',
                    style={'border-top': '#f0953f solid .2rem', },
                    children=[
                        html.H5(
                            style={'color': '#f0953f'},
                            children="Renovation"
                        ),
                        html.H3(
                            style={'color': '#f0953f'},
                            children=[
                                '$23,000',
                                html.P(
                                    children='+ $7,000 from target'
                                ),
                                html.P(
                                    children='Months left: 16'
                                )

                            ]
                        ),

                    ]
                ),
            ]
        ),  # number plate end

        html.Div(
            className='row dcc-plot',
            children=[
                html.Div(
                    className='dcc-sub-plot',
                    children=[
                        html.H5(
                            children='Spending History'
                        ),
                        dash_table.DataTable(
                            data=df_history.to_dict('records'),
                            columns=[{'id': c, 'name': c}
                                     for c in df_history.columns],
                            style_as_list_view=True,
                            style_cell={'padding': '5px'},
                            style_header={
                                'backgroundColor': '#ffffff',
                                'fontWeight': 'bold'
                            },
                            fixed_rows={
                                'headers': True, 'data': 0
                            },
                            sort_action='native',
                            filter_action='native',
                            style_table={
                                'minHeight': '475px',
                                'height': '475px',
                                'maxHeight': '475px',
                                'overflowX': 'auto',
                            },
                            style_cell_conditional=[
                                {'if': {'column_id': 'Month'}, 'width': '20%'},
                                {'if': {'column_id': 'Category'},
                                 'width': '20%'},
                                {'if': {'column_id': 'Cost'},
                                 'width': '20%'},
                                {'if': {'column_id': 'Comments'},
                                 'width': '40%'},
                                {'textAlign': 'center'}
                            ],
                        ),
                    ]
                ),
                html.Div(
                    className='dcc-sub-plot',
                    children=[
                        html.H5(
                            children='Spendings by Category'
                        ),
                        dcc.Dropdown(
                            id="dcc-dropdown",
                            placeholder="Select month",
                            value='Oct',
                            options=[
                                {'label': i, 'value': i}
                                for i in df_expenses.Month.tolist()
                            ],
                        ),
                        dcc.Graph(
                            id='categories-pie-plot',
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            className='row dcc-plot',
            children=[
                html.Div(
                    className='dcc-sub-plot',
                    children=[
                        html.Div(
                            id='case-timeline-log-button',
                            children=[
                                html.H5(
                                    children='Monthly Savings | Expenses'
                                ),

                            ],
                        ),
                        dcc.Graph(
                            id='expenses-bar-plot',
                            config={"displayModeBar": False,
                                    "scrollZoom": False},
                        ),
                        html.P([
                            # html.Label("Time Period"),
                            dcc.RangeSlider(id='slider',
                                            marks={i: month[i]
                                                   for i in range(0, 12)},
                                            min=0,
                                            max=11,
                                            value=[6, 11])
                        ], style={'width': '100%',
                                  'fontSize': '12px',
                                  'display': 'inline-block'
                                  })
                    ]
                ),
                html.Div(
                    className='dcc-sub-plot',
                    children=[
                        html.Div(
                            id='',
                            children=[
                                html.H5(
                                    children='Total Savings'
                                ),

                            ],
                        ),
                        dcc.Graph(
                            figure=fig_total,
                            config={"displayModeBar": False,
                                    "scrollZoom": False},

                        ),

                    ]
                ),
            ]
        ),
        html.Div(
            className='dcc-table',
            children=[
                html.H5(
                    id='dcc-table-header',
                    children='Summary'
                ),
                dash_table.DataTable(
                    data=df_expenses.to_dict('records'),
                    columns=[{'id': c, 'name': c}
                             for c in df_expenses.columns],
                    style_as_list_view=True,
                    style_cell={'padding': '5px'},
                    style_header={
                        'backgroundColor': '#ffffff',
                        'fontWeight': 'bold'
                    },
                    fixed_rows={
                        'headers': True, 'data': 0
                    },
                    sort_action='native',
                    style_table={
                                'minHeight': '475px',
                                'height': '475px',
                                'maxHeight': '475px',
                                'overflowX': 'auto',
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': 'Month'}, 'width': '6%'},
                        {'if': {'column_id': 'Food'}, 'width': '8%'},
                        {'if': {'column_id': 'Transport'}, 'width': '8%'},
                        {'if': {'column_id': 'Utilities'}, 'width': '8%'},
                        {'if': {'column_id': 'Insurance'}, 'width': '8%'},
                        {'if': {'column_id': 'Healthcare'}, 'width': '8%'},
                        {'if': {'column_id': 'Lifestyle'}, 'width': '8%'},
                        {'if': {'column_id': 'Savings'},
                            'width': '8%', 'color': '#2ecc77'},
                        {'if': {'column_id': 'Expenses'},
                            'width': '8%', 'color': '#f0953f'},
                        {'if': {'column_id': 'Wedding'},
                            'width': '8%', 'color': '#2ecc77'},
                        {'if': {'column_id': 'Renovation'},
                            'width': '8%', 'color': '#2ecc77'},
                        {'if': {'column_id': 'Comments'}, 'width': '14%'},
                        {'textAlign': 'center'}
                    ],
                ),
            ],
        ),


    ]
)  # end of main div


@app.callback(Output('expenses-bar-plot', 'figure'),
              [Input('slider', 'value')])
def render_combined_bar_plot(input1):

    # filtering the data

    month_index = month[input1[0]:input1[1] + 1]

    df2 = df_expenses[df_expenses['Month'].isin(month_index)]

    # Create empty figure canvas
    fig_combine = go.Figure()
    # Add trace to the figure

    trace_1 = go.Bar(x=df2['Month'], y=df2['Savings'], name='Savings',
                     marker_color='#85DE77', marker_line_color='rgb(8,48,107)')
    trace_2 = go.Bar(x=df2['Month'], y=df2['Expenses'], name='Expenses',
                     marker_color='#F9FFCB', marker_line_color='rgb(8,48,107)')

    fig_combine = go.Figure(data=[trace_1, trace_2])

    fig_combine.update_layout(barmode='group')
    fig_combine.update_layout(

        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
        ),

        xaxis=dict(
            showline=True),


        xaxis_tickformat='%b %d',
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=.385, y=-0.1),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

    return fig_combine


@app.callback(Output('categories-pie-plot', 'figure'),
              [Input('dcc-dropdown', 'value')])
def render_combined_bar_plot(input1):

    # filter input

    month_index = df_expenses[df_expenses['Month'].str.match(input1)].iloc[0].tolist()[
        2:]

    fig = go.Figure(data=[go.Pie(labels=spending_label,
                                 values=month_index)])

    fig.update_traces(hoverinfo='label+value+percent', textinfo='label+value', textfont_size=12,
                      marker=dict(line=dict(color='#FFFFFF', width=1.2)))

    fig.update_layout(

        margin=go.layout.Margin(
            l=10,
            r=10,
            b=50,
            t=50,
            pad=0
        ),

        # legend_orientation="",
        showlegend=False,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
