from flask import Flask, render_template, request, json, flash
import requests, json
from datetime import datetime
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '0fb59abbe2bb39814d80f1d1'

@app.route('/', methods=['GET', 'POST'])
def grade():
    url = 'https://epg-api.video.globo.com/programmes/1337?date={}'
    programacao = []
    str_date = request.form.get('data')
    if str_date is None or str_date == '':
        str_date_atual = datetime.today()
        data_correta = datetime.strftime(str_date_atual, '%Y-%m-%d')
    else:
        data_correta = str_date
    if request.method == 'POST' or data_correta != '':
        try: 
            requisicao = requests.get(url.format(data_correta)).json()['programme']['entries'] 
        except json.JSONDecodeError:
            str_date_atual = datetime.today()
            data_correta = datetime.strftime(str_date_atual, '%Y-%m-%d')
            requisicao = requests.get(url.format(data_correta)).json()['programme']['entries']
            flash('Data escolhida está indisponível. Mostrando a grade de horários de hoje.', category='danger')

        b = 0
        for i in requisicao:
            programa = requests.get(url.format(data_correta)).json()['programme']['entries'][b]['title']
            hora_inicio = str(
                requests.get(url.format(data_correta)).json()['programme']['entries'][b]['human_start_time'])[:5]
            hora_fim = str(requests.get(url.format(data_correta)).json()['programme']['entries'][b]['human_end_time'])[
                       :5]
            programacao_diaria = {
                'programa': programa,
                'hora_inicio': hora_inicio,
                'hora_fim': hora_fim,
            }
            b += 1

            programacao.append(programacao_diaria)

    context = json.dumps(programacao, ensure_ascii=False)
    df = pd.read_json(context)
    df = df.rename(columns={'programa': 'Programa', 'hora_inicio': 'Início', 'hora_fim': 'Fim'})
    dados = df.to_dict('records')
    colunas = df.columns.values
    str_date_hoje = datetime.today()
    str_date_hoje = datetime.strftime(str_date_hoje, '%d/%m/%Y')
    str_date = datetime.strptime(data_correta, '%Y-%m-%d')
    str_date = datetime.strftime(str_date, '%d/%m/%Y')
    return render_template('index.html', dados=dados, colunas=colunas, str_date=str_date, str_date_hoje=str_date_hoje)


@app.route("/404")
def error_404():
    return render_template('404.html')



if __name__ == '__main':
    app.run()
