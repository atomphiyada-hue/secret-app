import os
import random
from dash import Dash, html, dcc, Input, Output, State

app = Dash()

# สุ่มตัวเลข 1-100 ไว้
target_num = random.randint(1, 100)

app.layout = [
    html.H1("🎮 เกมทายตัวเลข (1-100)"),
    dcc.Input(id="user-guess", type="number", placeholder="พิมพ์ตัวเลขที่นี่..."),
    html.Button("ทายเลย!", id="btn-guess"),
    html.Div(id="game-output", style={"marginTop": "20px", "fontSize": "20px"})
]

@app.callback(
    Output("game-output", "children"),
    Input("btn-guess", "n_clicks"),
    State("user-guess", "value")
)
def play_game(n_clicks, guess):
    if not n_clicks or guess is None:
        return "กรุณาใส่ตัวเลขแล้วกดปุ่มทาย!"
    
    if guess == target_num:
        return "🎉 ถูกต้องแล้วครับ! คุณชนะแล้ว!"
    elif guess < target_num:
        return "📉 น้อยเกินไป! ลองทายเลขที่มากกว่านี้"
    else:
        return "📈 มากเกินไป! ลองทายเลขที่น้อยกว่านี้"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)