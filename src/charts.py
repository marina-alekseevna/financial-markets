import plotly.graph_objects as go
import pandas as pd



def makeChoropleth(df: pd.DataFrame, 
                  min_val: float, 
                  max_val: float, 
                  target_indicator: str, 
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
            target_indicator (str): illustrated indicator
            colorscale (str): colorscale from plotly library
            colorbar_title (str): name of the indicator
            title (str): title of the choropleth
            source (str): citation, quote, or any other link to the source
        Returns:
            plotly.graph_objs._figure.Figure: stylised plotly choropleth
    '''
    fig = go.Figure(data=go.Choropleth(
        locations=df['ISO3'],
        z=df['interest rate'].astype(float),
        zmin=min_val,
        zmax=max_val,
        colorscale= colorscale,
        autocolorscale=False,
        text=df['text'], 
        hovertemplate="%{text}",
        hoverlabel = dict(namelength=0),
        colorbar_title=colorbar_title))

    fig.update_layout(
        dragmode=False,
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


        annotations = [dict(
            x=0,
            y=-0.05,
            xref='paper',
            yref='paper',
            text=source,
            showarrow = False,
        )]
    )


    return fig