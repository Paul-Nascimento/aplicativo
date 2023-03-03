from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField,IntegerField,SelectField
from wtforms.validators import DataRequired,NumberRange



responsaveis = ["","Sarah","Paulo","Larissa","Isabella","Josevane","Gabriela","Mario"]
grupos = ["","1.0","2.0","3.0","4.1","4.2","4.3","5.1","5.2","5.3","5.4","6.1","6.2","6.3","6.4","6.5","6.6","6.7","6.8","6.9","9.0","9.4","10.0","11.1"]
macros = ["","A.1","A.2","B.1","B.2","B.3","B.4","C.1"]
movimentos=["","Sem Movimento","Ativo","S/M Fixo de ISS","S/M Fixo ICMS", "S/M Fixo ICMS e ISS","Ativo com Fixo de ICMS","Ativo com Fixo de ISS"]
regimes = ["","SN","REAL","PRE"]
class LiberacaoForm(FlaskForm):

    empresas = StringField("Empresa",validators=[DataRequired()])
    responsavel_liberacao = SelectField("Responsável",choices=responsaveis,validators=[DataRequired()])
    movimento_liberacao = SelectField("Movimento",choices=movimentos,validators=[DataRequired()])

    liberar =SubmitField("Liberar")
    excluir_liberacao = SubmitField("Excluir Liberacao")

class ApuracaoForm(FlaskForm):
    empresas = StringField("Empresa", validators=[DataRequired()])
    responsavel_apuracao = SelectField("Responsável", choices=responsaveis,validators=[DataRequired()])
    movimento_apuracao = SelectField("Movimento", choices=movimentos, validators=[DataRequired()])

    apurar = SubmitField("Apurar")
    excluir_apuracao = SubmitField("Excluir Apuracao")

class ConferenciaForm(FlaskForm):
    empresas = StringField("Empresa", validators=[DataRequired()])
    responsavel_conferencia = SelectField("Responsável", choices=responsaveis,validators=[DataRequired()])


    conferir = SubmitField("Conferência")
    excluir_conferencia = SubmitField("Excluir Apuracao")
class EnvioDeEmailForm(FlaskForm):
    empresas = StringField("Empresa", validators=[DataRequired()])
    responsavel_envio_email = SelectField("Responsável", choices=responsaveis,validators=[DataRequired()])

    envio_de_email = SubmitField("Registrar Envio")
    excluir_envio_de_email = SubmitField("Excluir Envio")

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

class FiltrarLiberacaoForm(FlaskForm):
    id = IntegerField("ID")
    nome = StringField("Nome da empresa")
    grupo = SelectField("Grupo", choices=grupos)
    macro = SelectField("Macro", choices=macros)
    regime = SelectField("Regime", choices=regimes)

    liberacao = SelectField("Liberadas",choices=["","Sim","Não"])
    data_liberacao = StringField("Data")
    responsavel_liberacao = SelectField("Responsavel",choices=responsaveis)
    movimento_liberacao = SelectField("Movimento",choices=movimentos)
    filtrar = SubmitField("Filtrar")

class FiltrarApuracaoForm(FlaskForm):
    id = IntegerField("ID")
    nome = StringField("Nome da empresa")
    grupo = SelectField("Grupo", choices=grupos)
    macro = SelectField("Macro", choices=macros)
    regime = SelectField("Regime", choices=regimes)
    liberacao = SelectField("Liberada", choices=["", "Sim","Não"])
    movimento_liberacao = SelectField("Movimento liberacao",choices=movimentos)
    apuracao = SelectField("Apurada",choices=["","Sim","Não"])
    data_apuracao = StringField("Data")
    responsavel_apuracao = SelectField("Responsavel",choices=responsaveis)
    movimento_apuracao = SelectField("Movimento",choices=movimentos)
    filtrar = SubmitField("Filtrar")

class FiltrarConferenciaForm(FlaskForm):
    id = IntegerField("ID")
    nome = StringField("Nome da empresa")
    grupo = SelectField("Grupo", choices=grupos)
    macro = SelectField("Macro", choices=macros)
    regime = SelectField("Regime", choices=regimes)
    apuracao = SelectField("Apurada", choices=["", "Sim","Não"])
    movimento_apuracao = SelectField("Movimento Apuracao",choices=movimentos)
    conferencia = SelectField("Conferida", choices=["", "Sim","Não"])

    data_conferencia = StringField("Data")
    responsavel_conferencia = SelectField("Responsavel",choices=responsaveis)

    filtrar = SubmitField("Filtrar")

class FiltrarEnvioDeEmailForm(FlaskForm):
    id = IntegerField("ID")
    nome = StringField("Nome da empresa")
    grupo = SelectField("Grupo", choices=grupos)
    macro = SelectField("Macro", choices=macros)
    regime = SelectField("Regime", choices=regimes)
    conferencia = SelectField("Conferida", choices=["", "Sim","Não"])
    envio_de_email = SelectField("Enviado", choices=["", "Sim","Não"])

    data_envio_de_email = StringField("Data")
    responsavel_envio_email = SelectField("Responsavel",choices=responsaveis)

    filtrar = SubmitField("Filtrar")

# class FiltrarLiberacaoForm(FlaskForm):
#     id = IntegerField("ID")
#     nome = StringField("Nome da empresa")
#     grupo = SelectField("Grupo", choices=grupos)
#     macro = SelectField("Macro", choices=macros)
#     regime = SelectField("Regime", choices=regimes)
#     liberacao = SelectField("Liberada",choices=["","Sim"])
#     data_liberacao = StringField("Data")
#     responsavel_liberacao = SelectField("Responsavel",choices=responsaveis)
#     movimento_liberacao = SelectField("Movimento",choices=movimentos)
#     filtrar = SubmitField("Filtrar")