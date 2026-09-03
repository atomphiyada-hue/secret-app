import os
from dash import Dash, html
from dotenv import load_dotenv
from dash import Dash, dcc, html, Input, Output, State

# โหลดค่าจากไฟล์ .env
load_dotenv()
APP_PASSWORD = os.getenv("APP_PASSWORD")
SECRET_MESSAGE = os.getenv("SECRET_MESSAGE")

app = Dash()

# หน้าตาเว็บ: มีช่องกรอกรหัสผ่าน ปุ่มกด และพื้นที่แสดงผล
app.layout = [
    html.Div(children="Hello, Dash!")
    dcc.Input(id="password", type="password"),
    html.Button("Submit", id="btn-submit"),
    html.Div(id="output"),
]

# ระบบเช็กรหัสผ่าน
@app.callback(
    Output("output", "children"),
    Input("btn-submit", "n_clicks"),
    State("password", "value"),
)
def check_password(n_clicks, pw):
    if not n_clicks:
        return ""
    if pw == APP_PASSWORD:
        return SECRET_MESSAGE
    return "Wrong password"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)