import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px
from autocorrect_module import run_function


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app  = dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.H1("CHARACTER AUTOCOMPLETE",style={'align':'center','marginLeft':450}),

    dcc.Input(id="input-word",type="text",placeholder='enter a word',autoComplete="off",
            style={'marginTop':100,'marginLeft':300,'width':500,'padding':20,'fontSize':25}),
    
    html.Div(id="output",style={'marginTop':100,'marginLeft':300,'fontSize':22})


])


@app.callback(
    Output("output","children"),
    Input("input-word","value"),
)

def get_words(input_word):
    
    if input_word is None:
        final_list=[]
        raise PreventUpdate
        
    
    else:
        final_list=[]
        
        if input_word == "":
            final_list=[]
            
            return ""

        elif input_word != "":

            for i in input_word.split():

                similar_words = run_function(i)

                sim_words=[]
                for w,prob in similar_words:
                    
                    sim_words.append(w)
                
                final_list.append(sim_words)

            return u"{}".format(final_list)
            
            
        print(final_list)

        



if __name__ =="__main__":
    app.run_server(debug=True)