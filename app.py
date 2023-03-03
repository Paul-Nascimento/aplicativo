from flask import Flask,render_template,request,url_for,redirect,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField,IntegerField,SelectField
from wtforms.validators import DataRequired,NumberRange
import datetime
from forms import LiberacaoForm,ApuracaoForm,RegistrarEmpresaForm,AlteracaoForm,NotaFiscalForm,FiltrarForm,\
    FiltrarLiberacaoForm,FiltrarApuracaoForm,ConferenciaForm,FiltrarConferenciaForm,FiltrarEnvioDeEmailForm,\
    EnvioDeEmailForm
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///fiscal.db"
app.config['SECRET_KEY'] = "Ttestes"
#Instanciando um banco de dados
db = SQLAlchemy(app)



class Empresa(db.Model):
    __tablename__ = "empresas"
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(50),nullable=False)
    grupo = db.Column(db.String(4),nullable=False)
    macro = db.Column(db.String(3),nullable=True)
    regime = db.Column(db.String(15),nullable=True)
    cnpj = db.Column(db.String(14),nullable=False)

    #Infos Liberação
    liberacao = db.Column(db.Boolean,default=False,nullable=True)
    data_liberacao = db.Column(db.DateTime,nullable=True)
    responsavel_liberacao = db.Column(db.String(20),nullable=True)
    movimento_liberacao = db.Column(db.String(20),nullable=True)

    #Infos Apuracao
    apuracao = db.Column(db.Boolean, default=False, nullable=True)
    data_apuracao = db.Column(db.DateTime)
    responsavel_apuracao = db.Column(db.String(20))
    movimento_apuracao = db.Column(db.String(20))
    #
    #Infos conferência
    conferencia = db.Column(db.Boolean, default=False)
    data_conferencia = db.Column(db.DateTime)
    responsavel_conferencia = db.Column(db.String(20))
    movimento_conferencia = db.Column(db.String(20))
    #
    # #Infos envio de emails

    envio_email = db.Column(db.Boolean, default=False)
    data_envio_email = db.Column(db.DateTime)
    responsavel_envio_email = db.Column(db.String(20))


    def __init__(self,id,nome,grupo,macro,regime,cnpj,
                 liberacao=None,data_liberacao=None,responsavel_liberacao=None,movimento_liberacao=None,
                 apuracao=None,data_apuracao=None,responsavel_apuracao=None,movimento_apuracao=None,
                 conferencia=None,data_conferencia=None,responsavel_conferencia=None,movimento_conferencia=None,
                 envio_de_email=None,data_envio_de_email=None,responsavel_envio_de_email=None):

        self.id = id
        self.nome = nome
        self.grupo = grupo
        self.macro = macro
        self.regime = regime
        self.cnpj = cnpj

        #Liberacao
        self.liberacao = liberacao
        self.data_liberacao = data_liberacao
        self.responsavel_liberacao = responsavel_liberacao
        self.movimento_liberacao = movimento_liberacao

        #Apuracao
        self.apuracao = apuracao
        self.data_apuracao = data_apuracao
        self.responsavel_apuracao = responsavel_apuracao
        self.movimento_apuracao = movimento_apuracao

        #Conferencia
        self.conferencia = conferencia
        self.data_conferencia = data_conferencia
        self.responsavel_conferencia = responsavel_conferencia
        self.movimento_conferencia = movimento_conferencia

        #Envio de Email
        self.envio_de_email = envio_de_email
        self.data_envio_de_email = data_envio_de_email
        self.responsavel_envio_email = responsavel_envio_de_email

class Emails(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()




@app.route("/registrar_empresa",methods=["GET","POST"])
def registrar_empresas():
    formulario_de_registro = RegistrarEmpresaForm()
    if request.method == "POST":
        id = request.form["id"]
        nome = request.form["nome"]
        grupo = request.form["grupo"]
        macro = request.form["macro"]
        cnpj = request.form["cnpj"]
        regime = request.form["regime"]

        #Verifica se todas estão feitas corretamente

        empresa = Empresa(id,nome,grupo,macro,regime,cnpj)
        db.session.add(empresa)
        db.session.commit()
        flash("Usuario registrado com sucesso")


    return render_template("registrar_empresas.html",form=formulario_de_registro)

@app.route("/visualizar_dados",methods=["GET","POST"])
@app.route("/",methods=["GET","POST"])
def visualizar_dados():
    # dados=Empresa.query.all()
    form=FiltrarForm()

    if request.method == "POST":
        filtrar = []

        id = form.id.data
        nome = form.nome.data
        grupo = form.nome.data
        macro=form.nome.data
        regime=form.regime.data
        cnpj = form.cnpj.data
        dados = {"id" :form.id.data,
                 "nome":form.nome.data,
                 "grupo":form.grupo.data,
                 "macro":form.macro.data,
                 "regime":form.regime.data,
                 "cnpj":form.cnpj.data}

        for k,v in dados.items():
            if v not in ["", None]:
                filtrar.append(k)

        texto = ''
        for index,filtro in enumerate(filtrar):

            if index + 1 == len(filtrar):
                texto += f"{filtro}='{dados[filtro]}'"
            else:
                texto += f"{filtro}='{dados[filtro]}' AND "

        print(texto)


        if texto == "":
            dados = Empresa.query.order_by(Empresa.grupo).all()
        else:
            sql = text(f"select * from empresas where {texto}")
            dados = db.engine.execute(sql)



        return render_template("visualizar_dados.html", dados=dados, form=form)

        # quantidade_liberada_total = db.session.query(Empresa).filter_by(grupo=grupo).filter_by(envio_email=True).count()

    dados=Empresa.query.order_by(Empresa.grupo).all()
    return render_template("visualizar_dados.html",dados=dados,form=form)

@app.route("/atualizar_dados/<id>",methods=["GET","POST"])
def atualizar_dados(id):
    alteracao_form = AlteracaoForm()
    empresa = Empresa.query.filter_by(id=id).first()
    if request.method == "POST":
        if alteracao_form.alterar.data:

            empresa.id = request.form["id"]
            empresa.nome = request.form["nome"]
            empresa.grupo = request.form["grupo"]
            empresa.cnpj = request.form["cnpj"]
            empresa.macro = request.form["macro"]
            empresa.regime = request.form["regime"]
            'db.session.delete(empresa)'
            try:
                db.session.commit()

                flash("Update feito com sucesso")
                return render_template("atualizar_dados.html",
                                       form=alteracao_form,
                                       empresa=empresa)
        #
            except:
                return render_template("atualizar_dados.html",
                                       form=alteracao_form,
                                       empresa=empresa)
        if alteracao_form.deletar.data:
            print('Deletad')
            db.session.delete(empresa)
            db.session.commit()
            flash("Empresa deletada com sucesso")
            return render_template("atualizar_dados.html",
                                   form=alteracao_form,
                                   empresa=empresa)
    else:
        return render_template("atualizar_dados.html",
                           form=alteracao_form,
                           empresa=empresa
                           )

@app.route("/liberar_empresas",methods=["GET","POST"])
def liberar_empresas():
    formulario_de_liberacao = LiberacaoForm()
    form = FiltrarLiberacaoForm()
    dados = Empresa.query.order_by(Empresa.grupo).all()
    if request.method == "POST":


        if form.filtrar.data:
            if request.method == "POST":
                filtrar = []

                id = form.id.data
                nome = form.nome.data
                grupo = form.nome.data
                macro = form.nome.data
                regime = form.regime.data
                liberacao = form.liberacao.data
                if liberacao == "Sim":
                    liberacao = 1


                if liberacao == "Não":
                    liberacao = 0


                dados = {"id": form.id.data,
                         "nome": form.nome.data,
                         "grupo": form.grupo.data,
                         "macro": form.macro.data,
                         "regime": form.regime.data,
                         "liberacao": liberacao,
                         "data_liberacao":form.data_liberacao.data,
                         "responsavel_liberacao":form.responsavel_liberacao.data,
                         "movimento_liberacao":form.movimento_liberacao.data}

                for k, v in dados.items():
                    if v not in ["", None]:
                        filtrar.append(k)

                texto = ''
                for index, filtro in enumerate(filtrar):

                    if index + 1 == len(filtrar) and (filtro == "liberacao"):
                        texto += f"{filtro}={dados[filtro]}"

                    elif index + 1 == len(filtrar):
                        texto += f"{filtro}='{dados[filtro]}'"

                    elif filtro == "liberacao":
                        texto += f"{filtro}={dados[filtro]} AND "

                    else:
                        texto += f"{filtro}='{dados[filtro]}' AND "


                print(texto)

                if texto == "":
                    query = Empresa.query.order_by(Empresa.grupo).all()
                else:
                    sql = text(f"select * from empresas where {texto} ORDER BY grupo")
                    query = db.engine.execute(sql)

                print(query)

                return render_template("liberadas.html",form=formulario_de_liberacao,dados=query,filtro=form)

        id = request.form["empresas"]
        ids = id.split(",")
        status_de_liberacao = False
        data = None
        responsavel_liberacao = None
        movimento_liberacao = None

        if formulario_de_liberacao.liberar.data:
            status_de_liberacao = True
            data = datetime.datetime.now()
            responsavel_liberacao = request.form["responsavel_liberacao"]
            movimento_liberacao = request.form["movimento_liberacao"]
            flash(f"Empresas {ids} liberadas com sucesso")
        if formulario_de_liberacao.excluir_liberacao.data:
            status_de_liberacao = False
            data = None
            responsavel_liberacao = None
            movimento_liberacao = None
            flash(f"Liberação das empresas {ids} cancelado com sucesso")
        for codigo in ids:
            try:
                update = Empresa.query.filter_by(id=codigo).first()
                update.liberacao = status_de_liberacao
                update.data_liberacao = data
                update.responsavel_liberacao = responsavel_liberacao
                update.movimento_liberacao = movimento_liberacao
                db.session.commit()
            except AttributeError:
                print(f"Empresa {codigo} não compõe a base de dados")

    return render_template("liberadas.html",form=formulario_de_liberacao,dados=dados,filtro=form)

@app.route("/apurar_empresas",methods=["GET","POST"])
def apurar_empresas():
    formulario_de_apuracao = ApuracaoForm()
    form = FiltrarApuracaoForm()
    dados = Empresa.query.order_by(Empresa.grupo).all()
    if request.method == "POST":

        if form.filtrar.data:
            if request.method == "POST":
                filtrar = []


                liberacao = form.liberacao.data
                if liberacao == "Sim":
                    liberacao = 1

                if liberacao == "Não":
                    liberacao = 0
                apuracao = form.apuracao.data
                if apuracao == "Sim":
                    apuracao = 1
                if apuracao == "Não":
                    apuracao = 0

                movimento_liberacao = form.movimento_liberacao.data


                dados = {"id": form.id.data,
                         "nome": form.nome.data,
                         "grupo": form.grupo.data,
                         "macro": form.macro.data,
                         "regime": form.regime.data,
                         "liberacao": liberacao,
                         "movimento_liberacao":movimento_liberacao,
                         "apuracao": apuracao,
                         "data_apuracao": form.data_apuracao.data,
                         "responsavel_apuracao": form.responsavel_apuracao.data,
                         "movimento_apuracao": form.movimento_apuracao.data}

                for k, v in dados.items():
                    if v not in ["", None]:
                        filtrar.append(k)

                texto = ''
                for index, filtro in enumerate(filtrar):


                    if index + 1 == len(filtrar) and (filtro == "liberacao" or filtro == "apuracao"):
                        texto += f"{filtro}={dados[filtro]}"

                    elif index + 1 == len(filtrar):
                        texto += f"{filtro}='{dados[filtro]}'"

                    elif filtro == "liberacao" or filtro == "apuracao":
                        texto += f"{filtro}={dados[filtro]} AND "

                    else:
                        texto += f"{filtro}='{dados[filtro]}' AND "

                print(texto)

                if texto == "":
                    query = Empresa.query.order_by(Empresa.grupo).all()
                else:
                    sql = text(f"select * from empresas where {texto} ORDER BY grupo")
                    query = db.engine.execute(sql)

                print(query)

                return render_template("apuradas.html", form=formulario_de_apuracao, dados=query, filtro=form)

        id = request.form["empresas"]
        ids = id.split(",")
        status_de_apuracao = False
        data = None
        responsavel_apuracao= None
        movimento_apuracao = None

        if formulario_de_apuracao.apurar.data:
            status_de_apuracao = True
            data = datetime.datetime.now()
            responsavel_apuracao = request.form["responsavel_apuracao"]
            movimento_apuracao = request.form["movimento_apuracao"]
            flash(f"Empresas {ids} apuradas com sucesso")
        if formulario_de_apuracao.excluir_apuracao.data:
            status_de_apuracao = False
            data = None
            responsavel_apuracao = None
            movimento_apuracao = None
            flash(f"Apuracao das empresas {ids} cancelado com sucesso")
        for codigo in ids:
            try:
                update = Empresa.query.filter_by(id=codigo).first()
                update.apuracao = status_de_apuracao
                update.data_apuracao = data
                update.responsavel_apuracao = responsavel_apuracao
                update.movimento_apuracao = movimento_apuracao
                db.session.commit()
            except AttributeError:
                print(f"Empresa {codigo} não compõe a base de dados")

    return render_template("apuradas.html", form=formulario_de_apuracao, dados=dados, filtro=form)


@app.route("/notas_fiscais",methods=["GET","POST"])
def notas_fiscais():
    formulario_de_notas = NotaFiscalForm()
    if request.method=="POST":
        print("Nota registrada com sucesso")
    return render_template('notas_fiscais.html',form=formulario_de_notas)

@app.route("/visualizar_emails",methods=["GET","POST"])
def visualizar_emails():
    return render_template("visualizar_emails.html")

@app.route("/resumo")
def resumo():
    return render_template("resumo.html")

@app.route("/conferir_empresas",methods=["GET","POST"])
def conferir_empresas():
    formulario_de_conferencia = ConferenciaForm()
    form = FiltrarConferenciaForm()
    dados = Empresa.query.order_by(Empresa.grupo).all()
    if request.method == "POST":

        if form.filtrar.data:
            if request.method == "POST":
                filtrar = []


                apuracao = form.apuracao.data
                if apuracao == "Sim":
                    apuracao = 1
                if apuracao == "Não":
                    apuracao= 0

                conferencia = form.conferencia.data
                if conferencia == "Sim":
                    conferencia = 1
                if conferencia == "Não":
                    conferencia = 0



                dados = {"id": form.id.data,
                         "nome": form.nome.data,
                         "grupo": form.grupo.data,
                         "macro": form.macro.data,
                         "regime": form.regime.data,
                         "apuracao": apuracao,
                         "movimento_apuracao":form.movimento_apuracao.data,
                         "conferencia": conferencia,
                         "data_apuracao": form.data_conferencia.data,
                         "responsavel_apuracao": form.responsavel_conferencia.data
                         }

                for k, v in dados.items():
                    if v not in ["", None]:
                        filtrar.append(k)

                texto = ''
                for index, filtro in enumerate(filtrar):


                    if index + 1 == len(filtrar) and (filtro == "conferencia" or filtro == "apuracao"):
                        texto += f"{filtro}={dados[filtro]}"

                    elif index + 1 == len(filtrar):
                        texto += f"{filtro}='{dados[filtro]}'"

                    elif filtro == "conferencia" or filtro == "apuracao":
                        texto += f"{filtro}={dados[filtro]} AND "

                    else:
                        texto += f"{filtro}='{dados[filtro]}' AND "

                print(texto)

                if texto == "":
                    query = Empresa.query.order_by(Empresa.grupo).all()
                else:
                    sql = text(f"select * from empresas where {texto} ORDER BY grupo")
                    query = db.engine.execute(sql)

                print(query)

                return render_template("conferencia.html", form=formulario_de_conferencia, dados=query, filtro=form)

        id = request.form["empresas"]
        ids = id.split(",")
        status_de_conferencia = False
        data = None
        responsavel_conferencia= None


        if formulario_de_conferencia.conferir.data:
            status_de_conferencia = True
            data = datetime.datetime.now()
            responsavel_conferencia = request.form["responsavel_conferencia"]

            flash(f"Empresas {ids} apuradas com sucesso")
        if formulario_de_conferencia.excluir_conferencia.data:
            status_de_conferencia = False
            data = None


            flash(f"Apuracao das empresas {ids} cancelado com sucesso")
        for codigo in ids:
            try:
                update = Empresa.query.filter_by(id=codigo).first()
                update.conferencia = status_de_conferencia
                update.data_conferencia = data
                update.responsavel_conferencia = responsavel_conferencia

                db.session.commit()
            except AttributeError:
                print(f"Empresa {codigo} não compõe a base de dados")

    return render_template("conferencia.html", form=formulario_de_conferencia, dados=dados, filtro=form)

@app.route("/enviar_emails_das_empresas",methods=["GET","POST"])
def enviar_emails_das_empresas():
    formulario_de_envio_email = EnvioDeEmailForm()
    form = FiltrarEnvioDeEmailForm()
    dados = Empresa.query.order_by(Empresa.grupo).all()
    if request.method == "POST":

        if form.filtrar.data:
            if request.method == "POST":
                filtrar = []

                envio_email = form.envio_de_email.data
                print(envio_email)
                if envio_email == "Sim":
                    envio_email= 1
                if envio_email == "Não":
                    envio_email= 0
                print(envio_email)
                conferencia = form.conferencia.data
                if conferencia == "Sim":
                    conferencia = 1
                if conferencia == "Não":
                    conferencia = 0

                dados = {"id": form.id.data,
                         "nome": form.nome.data,
                         "grupo": form.grupo.data,
                         "macro": form.macro.data,
                         "regime": form.regime.data,
                         "conferencia": conferencia,
                         "envio_email": envio_email,

                         "data_envio_email": form.data_envio_de_email.data,
                         "responsavel_envio_email": form.responsavel_envio_email.data
                         }

                for k, v in dados.items():
                    if v not in ["", None]:
                        filtrar.append(k)

                texto = ''
                print(filtrar)
                for index, filtro in enumerate(filtrar):

                    if index + 1 == len(filtrar) and (filtro == "envio_email" or filtro == "conferencia"):
                        texto += f"{filtro}={dados[filtro]}"
                        print(texto)

                    elif index + 1 == len(filtrar):
                        texto += f"{filtro}='{dados[filtro]}'"

                    elif filtro == "conferencia" or filtro == "envio_email":
                        texto += f"{filtro}={dados[filtro]} AND "

                    else:
                        texto += f"{filtro}='{dados[filtro]}' AND "

                print(texto)

                if texto == "":
                    query = Empresa.query.order_by(Empresa.grupo).all()
                else:
                    sql = text(f"select * from empresas where {texto} ORDER BY grupo")
                    query = db.engine.execute(sql)

                print(query)

                return render_template("envio_de_email.html", form=formulario_de_envio_email, dados=query, filtro=form)

        id = request.form["empresas"]
        ids = id.split(",")
        status_de_envio_email = False
        data_envio_email = None
        responsavel_envio_email = None

        if formulario_de_envio_email.envio_de_email.data:
            status_de_envio_email = True
            data_envio_email = datetime.datetime.now()
            responsavel_envio_email = request.form["responsavel_envio_email"]

            flash(f"Empresas {ids} apuradas com sucesso")
        if formulario_de_envio_email.excluir_envio_de_email.data:
            status_de_envio_email= False
            data_envio_email = None

            flash(f"Apuracao das empresas {ids} cancelado com sucesso")
        for codigo in ids:
            try:
                update = Empresa.query.filter_by(id=codigo).first()
                update.envio_email = status_de_envio_email
                update.data_envio_email = data_envio_email
                update.responsavel_envio_email = responsavel_envio_email

                db.session.commit()
                print('Comitado')
            except AttributeError:
                print(f"Empresa {codigo} não compõe a base de dados")

    return render_template("envio_de_email.html", form=formulario_de_envio_email, dados=dados, filtro=form)

@app.errorhandler(404)
def error_page(e):
    return render_template("error_page.html"),404
@app.errorhandler(500)
def error_page(e):
    return render_template("error_page.html"),500
@app.errorhandler(403)
def error_page(e):
    return render_template("error_page.html"),403
@app.errorhandler(410)
def error_page(e):
    return render_template("error_page.html"),410

if __name__ == "__main__":
    app.run(debug=True)

