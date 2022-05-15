import plotly.graph_objects as go
import pandas as pd
from typing import Tuple, List, Union



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
        colorbar_y=-0.2))

    fig.update_layout(
        dragmode="zoom",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Sans-Serif"
        ),

        title={
            'text': title,
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        title_font_color='#525252',
        title_font_size=26,
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
            y=-0.21,
            xref='paper',
            yref='paper',
            text=source,
            showarrow = False,
        )]
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
        text=df["name"],
        hovertemplate=hovertemplate,
        name="",  
        marker=dict(
                color="#E57A88",
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
        title_font_size=26
    )

    fig.update_xaxes(
            tickangle = 0,
            title_text = indicators[0],
            title_font = {"size": 20},
            title_standoff = 15)
    fig.update_yaxes(
            tickangle = 0,
            title_text = indicators[1],
            title_font = {"size": 20},
            title_standoff = 15)
    return fig