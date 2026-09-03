import os
import random
from dash import Dash, dcc, html, Input, Output, State, ctx

app = Dash()

app.layout = html.Div(
    style={"textAlign": "center", "fontFamily": "sans-serif", "marginTop": "20px"},
    children=[
        html.H1("🐤 Flappy Bird (Dash Python)"),
        html.Div(id="score-board", children="Score: 0", style={"fontSize": "24px", "fontWeight": "bold"}),
        html.Br(),
        
        html.Div(
            id="game-screen",
            style={
                "width": "300px",
                "height": "400px",
                "backgroundColor": "#70c5ce",
                "margin": "0 auto",
                "position": "relative",
                "overflow": "hidden",
                "border": "3px solid #333",
                "borderRadius": "8px",
            },
            children=[
                html.Div(
                    id="bird",
                    style={
                        "width": "24px",
                        "height": "24px",
                        "backgroundColor": "#f4c430",
                        "borderRadius": "50%",
                        "position": "absolute",
                        "left": "50px",
                    },
                ),
                html.Div(
                    id="pipe-top",
                    style={
                        "width": "50px",
                        "backgroundColor": "#73bf2e",
                        "position": "absolute",
                        "border": "2px solid #222",
                    },
                ),
                html.Div(
                    id="pipe-bottom",
                    style={
                        "width": "50px",
                        "backgroundColor": "#73bf2e",
                        "position": "absolute",
                        "border": "2px solid #222",
                    },
                ),
                html.Div(
                    id="game-over-msg",
                    style={
                        "color": "white",
                        "fontSize": "22px",
                        "fontWeight": "bold",
                        "marginTop": "150px",
                        "display": "none",
                        "textShadow": "2px 2px #000",
                    },
                ),
            ],
        ),
        html.Br(),
        html.Button("🚀 กระโดด / เริ่มใหม่", id="btn-jump", n_clicks=0, style={"padding": "12px 24px", "fontSize": "18px", "cursor": "pointer"}),
        
        dcc.Interval(id="game-timer", interval=150, n_clicks=0),
        dcc.Store(id="game-store", data={"bird_y": 150, "velocity": 0, "pipe_x": 300, "pipe_gap_y": 150, "score": 0, "game_over": False}),
    ],
)

@app.callback(
    [
        Output("game-store", "data"),
        Output("bird", "style"),
        Output("pipe-top", "style"),
        Output("pipe-bottom", "style"),
        Output("score-board", "children"),
        Output("game-over-msg", "style"),
        Output("game-over-msg", "children"),
    ],
    [Input("game-timer", "n_intervals"), Input("btn-jump", "n_clicks")],
    [State("game-store", "data")],
)
def update_game(n_intervals, jump_clicks, data):
    triggered_id = ctx.triggered_id

    if data["game_over"]:
        if triggered_id == "btn-jump":
            data = {"bird_y": 150, "velocity": -6, "pipe_x": 300, "pipe_gap_y": 150, "score": 0, "game_over": False}
        else:
            msg_style = {"color": "red", "fontSize": "22px", "fontWeight": "bold", "marginTop": "150px", "display": "block"}
            return data, {}, {}, {}, f"Score: {data['score']}", msg_style, "GAME OVER! กดปุ่มเพื่อเล่นใหม่"

    if triggered_id == "btn-jump":
        data["velocity"] = -8

    data["velocity"] += 1.8
    data["bird_y"] += data["velocity"]

    data["pipe_x"] -= 12
    if data["pipe_x"] < -50:
        data["pipe_x"] = 300
        data["pipe_gap_y"] = random.randint(80, 220)
        data["score"] += 1

    gap_height = 110
    if (
        data["bird_y"] <= 0
        or data["bird_y"] >= 376
        or (data["pipe_x"] <= 74 and data["pipe_x"] + 50 >= 50 and (data["bird_y"] < data["pipe_gap_y"] or data["bird_y"] + 24 > data["pipe_gap_y"] + gap_height))
    ):
        data["game_over"] = True

    bird_style = {
        "width": "24px",
        "height": "24px",
        "backgroundColor": "#f4c430",
        "borderRadius": "50%",
        "position": "absolute",
        "left": "50px",
        "top": f"{data['bird_y']}px",
    }

    pipe_top_style = {
        "width": "50px",
        "height": f"{data['pipe_gap_y']}px",
        "backgroundColor": "#73bf2e",
        "position": "absolute",
        "left": f"{data['pipe_x']}px",
        "top": "0px",
    }
    pipe_bottom_style = {
        "width": "50px",
        "height": f"{400 - data['pipe_gap_y'] - gap_height}px",
        "backgroundColor": "#73bf2e",
        "position": "absolute",
        "left": f"{data['pipe_x']}px",
        "bottom": "0px",
    }

    msg_style = {"display": "none"}
    return data, bird_style, pipe_top_style, pipe_bottom_style, f"Score: {data['score']}", msg_style, ""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)