from flask import Flask, request, render_template, session
from pyrfc import Connection

conn = Connection(
    user='TST_ABAP_PN',
    passwd='Dec@123',
    ashost='172.17.4.18',
    sysnr='00',
    client='320',
    lang='EN'
)

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/")
def home():

    # 1. Store SAP user once
    if "sap_user" not in session:
        session["sap_user"] = request.args.get("user")

    sap_user = session.get("sap_user")

    if not sap_user:
        sap_user = '1070510'

    # 2. Always call SAP
    result = conn.call(
        'Z_GET_EMPLOYEE',
        PERNR=str(sap_user)
    )

    EMPD = result.get("EMPD", {})

    return render_template("form.html", empd=EMPD)


if __name__ == "__main__":
    app.run(debug=True)
