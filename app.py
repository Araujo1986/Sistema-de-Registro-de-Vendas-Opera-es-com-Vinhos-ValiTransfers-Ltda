from flask import Flask, render_template, request, redirect, send_file
from flask_mysqldb import MySQL
import csv
import os
import config

app = Flask(__name__)

app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)

@app.route("/")
def index():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM vendas")

    vendas = cursor.fetchall()

    cursor.close()

    return render_template("index.html", vendas=vendas)


@app.route("/salvar", methods=["POST"])
def salvar():

    tipo = request.form["tipo"]

    marca = request.form["marca"]

    preco = request.form["preco"]

    quantidade = request.form["quantidade"]

    cursor = mysql.connection.cursor()

    cursor.execute("""
        INSERT INTO vendas
        (tipo_vinho, marca, preco, quantidade_vendida)
        VALUES(%s,%s,%s,%s)
    """, (tipo, marca, preco, quantidade))

    mysql.connection.commit()

    cursor.close()

    return redirect("/")


@app.route("/csv")
def csv_export():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM vendas")

    dados = cursor.fetchall()

    cursor.close()

    if not os.path.exists("exports"):
        os.makedirs("exports")

    arquivo = "exports/vendas.csv"

    with open(arquivo, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "ID",
            "Tipo de vinho",
            "Marca",
            "Preço",
            "Quantidade Vendida"
        ])

        for venda in dados:
            writer.writerow(venda)

    return send_file(
        arquivo,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)