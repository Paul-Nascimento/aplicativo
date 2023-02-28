from flask import Flask,render_template,request,url_for,redirect,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField,IntegerField,SelectField
from wtforms.validators import DataRequired,NumberRange
import datetime
from forms import LiberacaoForm,ApuracaoForm,RegistrarEmpresaForm,AlteracaoForm,NotaFiscalForm,FiltrarForm

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
        self.responsavel_envio_de_email = responsavel_envio_de_email


# class Emails(db.Model):
#     __tablename__ = "emails"
#     id = db.Column(db.Integer,nullable=False,primary_key=True)
#     nome = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     cnpj = db.Column(db.String(14), nullable=False)

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
        remover = []

        dados = {"id" :form.id.data,
                 "nome":form.nome.data,
                 "grupo":form.grupo.data,
                 "macro":form.macro.data,
                 "regime":form.regime.data,
                 "cnpj":form.cnpj.data}

        for k,v in dados.items():
            if v in ["",None]:
                remover.append(k)

        for k in remover:
            del dados[k]
        print(dados)



        # quantidade_liberada_total = db.session.query(Empresa).filter_by(grupo=grupo).filter_by(envio_email=True).count()

    dados=Empresa.query.order_by(Empresa.grupo).all()
    return render_template("visualizar_dados.html",dados=dados,form=form,filtro=dados)

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
    dados = Empresa.query.all()
    if request.method == "POST":
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

    return render_template("liberadas.html",form=formulario_de_liberacao,dados=dados)

@app.route("/apurar_empresas",methods=["GET","POST"])
def apurar_empresas():
    formulario_de_apuracao = ApuracaoForm()
    dados = Empresa.query.all()
    if request.method == "POST":
        id = request.form["empresas"]
        ids = id.split(",")

        status_de_apuracao = False
        data = None
        responsavel_apuracao = None
        movimento_apuracao = None

        if formulario_de_apuracao.apurar.data:
            status_de_apuracao = True
            data = datetime.datetime.now()
            responsavel_apuracao = request.form["responsavel_apuracao"]
            movimento_apuracao = request.form["movimento_apuracao"]
        if formulario_de_apuracao.excluir_apuracao.data:
            status_de_apuracao = False
            data = None
            responsavel_apuracao = None
            movimento_apuracao = None
        for codigo in ids:
            try:
                update = Empresa.query.filter_by(id=codigo).first()
                liberacao = update.liberacao
                if liberacao == None:
                    # flash("Empresa não liberada ainda")
                    pass

                else:
                    # flash("Apurada com sucesso")
                    update.apuracao = status_de_apuracao
                    update.data_apuracao = data
                    update.responsavel_apuracao = responsavel_apuracao
                    update.movimento_apuracao = movimento_apuracao
                # db.session.commit()
            except AttributeError:
                # flash(f"Empresa {codigo} não compõe a base de dados")
                pass

    return render_template("apuradas.html",form=formulario_de_apuracao,dados=dados)

@app.route("/notas_fiscais",methods=["GET","POST"])
def notas_fiscais():
    formulario_de_notas = NotaFiscalForm()
    if request.method=="POST":
        print("Nota registrada com sucesso")
    return render_template('notas_fiscais.html',form=formulario_de_notas)


@app.route("/resumo")
def resumo():

    return render_template("resumo.html")


def emails():

    return render_template("emails.html")


def querys():
    # quantidade_liberada_total = db.session.query(Empresa).filter_by(grupo=grupo).filter_by(envio_email=True).count()
    #
    # quantidade_total = db.session.query(Empresa).filter_by(grupo=grupo).count()

    pass




# def totais():
#     grupos_e_quantidades_totais = {}
#     for grupo in grupos:
#         quantidade_total = db.session.query(Empresa).filter_by(grupo=grupo).count()
#         grupos_e_quantidades_totais[f"{grupo}"] = quantidade_total
#     return grupos_e_quantidades_totais


if __name__ == "__main__":
    app.run(debug=True)
