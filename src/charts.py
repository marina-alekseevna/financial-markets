import plotly.graph_objects as go
import pandas as pd
from typing import Tuple, List, Union
import plotly.express as px
from calendar import monthrange
from plotly.subplots import make_subplots



def makeChoropleth(df: pd.DataFrame, 
                  min_val: float, 
                  max_val: float, 
                  indicator: str, 
                  colorscale: str, 
                  colorbar_title: str, 
                  title: str, 
                  source: str) -> go.Figure:
    '''
        Return stylised plotly graph object choropleth
        
        Args:
            df (pd.DataFrame): filtered for specific date
            min_val (float): minimum value for the colorscale
            max_val (float): maximum values for the colorscale
            indicator (str): illustrated indicator
            colorscale (str): colorscale from plotly library
            colorbar_title (str): name of the indicator
            title (str): title of the choropleth
            source (str): citation, quote, or any other link to the source
        Returns:
            plotly.graph_objs._figure.Figure: stylised plotly choropleth
    '''
    if indicator in df.columns:
        pass
    else:
        print(f"Indicator {indicator} not found")
        return
    fig = go.Figure(data=go.Choropleth(
        locations=df['ISO3'],
        z=df[indicator].astype(float),
        zmin=min_val,
        zmax=max_val,
        colorscale= colorscale,
        autocolorscale=False,
        text=df[f'text_{indicator}'], 
        hovertemplate="%{text}",
        hoverlabel = dict(namelength=0),
        colorbar_title=colorbar_title,
        colorbar_orientation='h',
        colorbar_thickness = 15,
        colorbar_yanchor = "bottom",
        colorbar_y=-0.01))

    fig.update_layout(
        dragmode="zoom",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Sans-Serif"
        ),

        title={
            'text': title,
            'y':0.95,
            'x':0.5
        },
        title_font_color='#525252',
        title_font_size=20,
        font=dict(
            family="Sans-Serif", 
            size=12, 
            color='#525252'
        ),

        legend = dict(
            orientation="h"
        ),
        annotations = [dict(
            x=0,
            y=-1.25,
            xref='paper',
            yref='paper',
            text=source,
            showarrow = False,
        )],
        margin=dict(l=5, r=5, t=5, b=2)
    )
    return fig

def makeScatterplot(df: pd.DataFrame, indicators: Union[Tuple[str, str], List[str]], 
                   hovertemplate: str="%{text}<br>interest rate: %{y:.2f}%,<br>inflation %{x:.2f}%", 
                   textposition:str="top right") -> go.Figure:
    '''
    Delivers a formatted go.figure scatterplot
    
    Args:
        df (pd.DataFrame): dataframe that contains data for visualisation
        indicators (Tuple[str, str] or List[str, str]): indicators to be visualised, in (x, y) format
        hovertemplate (str): template to format hovertemplate output
        textposition (str): placement of text around the datapoints
    Returns:
        go.Figure, a scatterplot with visualised data
    '''
    fig= go.Figure(go.Scatter(
        x=df[indicators[0]],
        y=df[indicators[1]],
        text=df["Country"],
        hovertemplate=hovertemplate,
        name="",  
        marker=dict(
                # color="#E57A88",
                color = px.colors.sequential.Sunsetdark,
                opacity=0.8,
                line=dict(
                    color='#525252',
                    width=1),
                size=20),

        textposition=textposition,
        mode="markers+text"
    ))

    fig.update_layout(
        template="none",
        grid=dict(xgap=0.05, ygap=0.05),
        font=dict(color='#525252'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Sans-Serif"
        ),
        title={
                'text': f"<b>{indicators[0]} vs {indicators[1]}</b>",
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
        title_font_color='#525252',
        title_font_size=20,
        margin=dict(l=15, r=15)
    )

    fig.update_xaxes(
            tickangle = 0,
            title_text = indicators[0],
            title_font = {"size": 15},
            title_standoff = 0)
    fig.update_yaxes(
            tickangle = 0,
            title_text = indicators[1],
            title_font = {"size": 15},
            title_standoff = 0)
    return fig


def makeLineplot(df: pd.DataFrame, 
                 indicator: str, 
                 interval: Tuple[int, int],
                 countries: List[str], 
                 colorscheme: List[str]) -> go.Figure:
    '''
    makes a formatted lineplot
    
    Args:
        df (pd.DataFrame) formatted dataframe with timeseries data for different countries
        indicator (str): targetted indicators, title of a column
        interval (Tuple[int, int]): year and month to be highlighted
        countries (List[str]): list of countries to be plotted
        colorscheme (List[str]) list of strings of colors, px.colors.sequential works 
    Returns:
        go.Figure lineplot
    '''
    counter = 0
    fig = go.Figure(layout=dict(hovermode = "x unified"))
    for country in countries:
        fig.add_trace(go.Scatter(x=df[df.Country == country]["date"], 
                            y=df[df.Country == country][indicator], mode='lines', name=country,
                            hovertemplate="%{y:.2f}%",
                            line = dict(color=colorscheme[counter%7])
                            ))
        counter += 1
    
    fig.update_layout(
        template="none",
        grid=dict(xgap=0.05, ygap=0.05),
        font=dict(color='#525252'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Sans-Serif"
        ),
        title={
                'text': f"<b>{indicator} over time</b>",
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
        title_font_color='#525252',
        title_font_size=26)
    
    fig.update_xaxes(
        tickangle = 0,
        title="date",
        title_font = {"size": 15},
        title_standoff = 0)
    
    fig.update_yaxes(
        tickangle = 0,
        title=indicator,
        title_text = indicator,
        title_font = {"size": 15},
        title_standoff = 0)
    
    fig.add_vrect(
        x0=f"{interval[0]}-{interval[1]}-01", 
        x1=f"{interval[0]}-{interval[1]}-{monthrange(interval[0],interval[1])[1]}",
        fillcolor="Blue", opacity=0.5,
        layer="below", line_width=0,
    )
    return fig



def addLineplot(df: pd.DataFrame, 
                fig: go.Figure,
                indicator: str,
                interval: Tuple[int, int],
                countries: List[str],
                pos: Tuple[int, int],
                colorscheme: List[str]) -> go.Figure:
    '''
    adds a formatted lineplot to a pre-existing go.Figure
    
    Args:
        df (pd.DataFrame): a formatted dataframe with timeseries data for different countries
        fig (go.Figure): a figure to add lineplot to
        indicator (str): targetted indicators, title of a column
        interval (Tuple[int, int]): year and month to be highlighted
        countries (List[str]): list of countries to be plotted
        pos (int): position in the subplot item
        colorscheme (List[str]) list of strings of colors, px.colors.sequential works 
    Returns:
        go.Figure with added lines to a subplot
    '''
    counter = 0
    
    for country in countries:
        fig.add_trace(go.Scatter(x=df[df.Country == country]["date"], 
                               y=df[df.Country == country][indicator], mode='lines', name=country,
                              hovertemplate="%{y:.2f}%",
                              line = dict(color=colorscheme[counter%7]),
                              
                              ),
                      row=pos[0], col=pos[1])
        counter += 1
    
    fig.add_vrect(
        x0=f"{interval[0]}-{interval[1]}-01", 
        x1=f"{interval[0]}-{interval[1]}-{monthrange(interval[0],interval[1])[1]}",
        fillcolor="Blue", opacity=0.5,
        layer="below", line_width=0,
        row=pos[0], col=pos[1]
    )

    return fig

def makeVerticalLineplots(df: pd.DataFrame,
                          indicators: Tuple[str],
                          countries: Tuple[str],
                          interval: Tuple[int],
                          subplot_titles: Tuple[str],
                          colorscheme: List[str]) -> go.Figure:
    '''
    makes vertical lineplots with titles

    Args:
        df (pd.DataFrame): a formatted dataframe with timeseries data for different countries
        fig (go.Figure): a figure to add lineplot to
        indicators (str): targetted indicators, title of a column
        countries (List[str]): list of countries to be plotted
        interval (Tuple[int, int]): year and month to be highlighted
        subplot_titles (Tuple[str]): titles to be used for the graphs
        colorscheme (List[str]) list of strings of colors, px.colors.sequential works 
    '''
    rows = len(indicators)
    fig = make_subplots(rows=rows, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.1,
                        subplot_titles=subplot_titles)
    pos = 1
    for indicator in indicators:
        addLineplot(df, fig, 
                    indicator, 
                    interval, 
                    countries,
                    (pos, 1), 
                    colorscheme)
        pos += 1

    fig.update_xaxes(
        tickangle = 0,
        title="date",
        title_text = "date",
        title_font = {"size": 15},
        title_standoff = 0)

    fig.update_yaxes(
        tickangle = 0,
        title="%",
        title_text = "%",
        title_font = {"size": 15},
        title_standoff = 0)

    fig.update_layout(
        # hovermode = "x unified",
        template="none",
        grid=dict(xgap=0.05, ygap=0.05),
        font=dict(color='#525252'),
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Sans-Serif"
        ),

        title_font_color='#525252',
        title_font_size=26,
        margin=dict(l=15, r=15))
    fig.layout.annotations[0].update(font_size=20)
    fig.layout.annotations[1].update(font_size=20)
    return fig