from flask import Flask, render_template, request, redirect, url_for, flash, abort
import sqlite3
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "chave-local-trocar-antes-de-producao"
DB = Path(__file__).with_name("chamados.db")
PRIORIDADES = {1: "Muito baixa", 2: "Baixa", 3: "Média", 4: "Alta", 5: "Urgente"}
STATUS = ("Aberto", "Em andamento", "Fechado")

def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def inicializar():
    with conectar() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL, descricao TEXT NOT NULL,
            prioridade INTEGER NOT NULL CHECK(prioridade BETWEEN 1 AND 5),
            status TEXT NOT NULL DEFAULT 'Aberto',
            criado_em TEXT NOT NULL)""")

@app.template_filter("data_br")
def data_br(valor):
    try:
        return datetime.fromisoformat(valor).strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return valor

@app.get("/")
def index():
    status = request.args.get("status", "")
    busca = request.args.get("busca", "").strip()
    sql = "SELECT * FROM chamados WHERE 1=1"
    args = []
    if status in STATUS:
        sql += " AND status=?"; args.append(status)
    if busca:
        sql += " AND (titulo LIKE ? OR descricao LIKE ?)"
        args += [f"%{busca}%", f"%{busca}%"]
    sql += """ ORDER BY CASE status WHEN 'Aberto' THEN 1
        WHEN 'Em andamento' THEN 2 ELSE 3 END, prioridade DESC, id DESC"""
    with conectar() as con:
        chamados = con.execute(sql, args).fetchall()
        total = con.execute("SELECT COUNT(*) FROM chamados").fetchone()[0]
        abertos = con.execute("SELECT COUNT(*) FROM chamados WHERE status='Aberto'").fetchone()[0]
        andamento = con.execute("SELECT COUNT(*) FROM chamados WHERE status='Em andamento'").fetchone()[0]
        fechados = con.execute("SELECT COUNT(*) FROM chamados WHERE status='Fechado'").fetchone()[0]
    return render_template("index.html", chamados=chamados, prioridades=PRIORIDADES,
        status_validos=STATUS, filtro_status=status, busca=busca, total=total,
        abertos=abertos, andamento=andamento, fechados=fechados)

@app.route("/chamados/novo", methods=["GET", "POST"])
def novo():
    chamado = {"titulo": "", "descricao": "", "prioridade": 3}
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        try:
            prioridade = int(request.form.get("prioridade", "3"))
        except ValueError:
            prioridade = 0
        erros = []
        if not titulo or len(titulo) > 120: erros.append("Informe um título de até 120 caracteres.")
        if not descricao or len(descricao) > 2000: erros.append("Informe uma descrição de até 2.000 caracteres.")
        if prioridade not in PRIORIDADES: erros.append("Selecione uma prioridade válida.")
        chamado = {"titulo": titulo, "descricao": descricao, "prioridade": prioridade if prioridade in PRIORIDADES else 3}
        if erros:
            for erro in erros: flash(erro, "erro")
            return render_template("form.html", chamado=chamado, prioridades=PRIORIDADES), 400
        data = datetime.now().astimezone().isoformat(timespec="seconds")
        with conectar() as con:
            cur = con.execute("INSERT INTO chamados(titulo,descricao,prioridade,status,criado_em) VALUES(?,?,?,'Aberto',?)",
                (titulo, descricao, prioridade, data))
            numero = cur.lastrowid
        flash(f"Chamado #{numero} cadastrado com sucesso.", "sucesso")
        return redirect(url_for("index"))
    return render_template("form.html", chamado=chamado, prioridades=PRIORIDADES)

@app.route("/chamados/<int:numero>/editar", methods=["GET", "POST"])
def editar(numero):
    with conectar() as con:
        chamado = con.execute("SELECT * FROM chamados WHERE id=?", (numero,)).fetchone()
    if chamado is None: abort(404)
    if request.method == "POST":
        status = request.form.get("status", "")
        try: prioridade = int(request.form.get("prioridade", "0"))
        except ValueError: prioridade = 0
        if status not in STATUS or prioridade not in PRIORIDADES:
            flash("Selecione um status e uma prioridade válidos.", "erro")
            return redirect(url_for("editar", numero=numero))
        with conectar() as con:
            con.execute("UPDATE chamados SET status=?, prioridade=? WHERE id=?", (status, prioridade, numero))
        flash(f"Chamado #{numero} atualizado com sucesso.", "sucesso")
        return redirect(url_for("index"))
    return render_template("editar.html", chamado=chamado, prioridades=PRIORIDADES, status_validos=STATUS)

@app.errorhandler(404)
def nao_encontrado(_):
    return render_template("404.html"), 404

inicializar()
if __name__ == "__main__":
    app.run(debug=True)
