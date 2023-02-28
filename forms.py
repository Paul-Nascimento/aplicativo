from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField,IntegerField,SelectField
from wtforms.validators import DataRequired,NumberRange



responsaveis = ["Sarah","Paulo","Larissa","Isabella","Josevane","Gabriela","Mario"]
grupos = ["","1.0","2.0","3.0","4.1","4.2","4.3","5.1","5.2","5.3","5.4","6.1","6.2","6.3","6.4","6.5","6.6","6.7","6.8","6.9","9.0","9.4","10.0","11.1"]
macros = ["","A.1","A.2","B.1","B.2","B.3","B.4","C.1"]
movimentos=["","Sem Movimento","Ativo"]
regimes = ["","SN","Real","PRE"]
class LiberacaoForm(FlaskForm):

    empresas = StringField("Empresa",validators=[DataRequired()])
    responsavel_liberacao = SelectField("Responsável",choices=responsaveis,validators=[DataRequired()])
    movimento_liberacao = SelectField("Movimento",choices=movimentos,validators=[DataRequired()])

    liberar =SubmitField("Liberar")
    excluir_liberacao = SubmitField("Excluir Liberacao")

class ApuracaoForm(FlaskForm):
    empresas = StringField("Empresa", validators=[DataRequired()])
    responsavel_apuracao = SelectField("Responsável", choices=responsaveis,validators=[DataRequired()])
    movimento_apuracao = SelectField("Movimento", choices=["Sem Movimento", "Ativo"], validators=[DataRequired()])

    apurar = SubmitField("Apurar")
    excluir_apuracao = SubmitField("Excluir Apuracao")

class RegistrarEmpresaForm(FlaskForm):

    id=IntegerField("ID",validators=[DataRequired()])
    nome=StringField("Nome da empresa",validators=[DataRequired()])
    grupo=SelectField("Grupo",choices=grupos,validators=[DataRequired()])
    macro=SelectField("Grupo",choices=macros,validators=[DataRequired()])
    cnpj=StringField("CNPJ",validators=[DataRequired()])
    regime=SelectField("Regime",choices=regimes,validators=[DataRequired()])
    registrar=SubmitField("Registrar")


class AlteracaoForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    nome = StringField("Nome da empresa", validators=[DataRequired()])
    grupo = SelectField("Grupo", choices=grupos, validators=[DataRequired()])
    macro = SelectField("Macro", choices=macros, validators=[DataRequired()])
    cnpj = StringField("CNPJ", validators=[DataRequired()])
    regime = SelectField("Regime", choices=regimes, validators=[DataRequired()])

    alterar = SubmitField("Registrar")
    deletar = SubmitField("Excluir")

class NotaFiscalForm(FlaskForm):
    id = IntegerField("ID", validators=[DataRequired()])
    demanda = SelectField("Demanda",choices=["Nota","Nota de Devolução"], validators=[DataRequired()])
    meio = SelectField("Meio",choices=["Email","Whatsapp","Telefone"], validators=[DataRequired()])
    responsavel = SelectField("Responsavel",choices=["Larissa","Sarah"], validators=[DataRequired()])

    quantidade = IntegerField("Quantidade", validators=[DataRequired()])
    numero_da_nota = StringField("Numero das notas", validators=[DataRequired()])
    obs = StringField("Observações:")
    fazer_nota = SubmitField("Fazer")


class FiltrarForm(FlaskForm):
    id = IntegerField("ID")
    nome = StringField("Nome da empresa")
    grupo = SelectField("Grupo", choices=grupos)
    macro = SelectField("Macro", choices=macros)
    cnpj = StringField("CNPJ")
    regime = SelectField("Regime", choices=regimes)

    filtrar = SubmitField("Filtrar")