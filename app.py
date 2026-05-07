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

@app.route("/",methods=["GET","POST"])
def home():

    # 1. Store SAP user once
    if "sap_user" not in session:
        session["sap_user"] = request.args.get("user")

    sap_user = session.get("sap_user")

    if not sap_user:
        sap_user = request.form.get("emp_id")
        print(sap_user)

    # 2. Always call SAP
    if sap_user:
      result = conn.call(
        'Z_GET_EMPLOYEE',
        PERNR=str(sap_user)
        )

    EMPD = result.get("EMPD", {})
    print(EMPD)

    return render_template("form.html", empd=EMPD)


if __name__ == "__main__":
    app.run(debug=True)
