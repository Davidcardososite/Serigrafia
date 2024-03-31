from flask import Flask, render_template, request, Blueprint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Cria um Blueprint para os arquivos estáticos
static_bp = Blueprint('static', __name__, static_folder='static', static_url_path='/static')

# Cria a aplicação Flask
app = Flask(__name__)
app.register_blueprint(static_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')
    
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Obter dados do formulário
    image = request.files['imageUpload']
    quantity = request.form['quantity']
    colors = request.form.getlist('color')  # Obter uma lista de todas as cores selecionadas
    material = request.form['material']  # Obter o tipo de material selecionado
    email = request.form['email']  # Obter o email do cliente
    phone = request.form['phone']  # Obter o número de telefone do cliente

    # Processar os dados e enviar um e-mail ao cliente
    enviar_email(image, quantity, colors, material, email, phone)

    return 'Pedido recebido com sucesso!'

def enviar_email(image, quantity, colors, material, email, phone):
    # Configurar informações de e-mail
    remetente = 'serigrafiatrabalhos@gmail.com'  # Seu e-mail
    senha = 'p w v h t e j p t y z l h m u z'  # Sua senha específica do aplicativo
    destinatario = 'davidcardososites@gmail.com'  # E-mail do cliente

    # Converter os códigos hexadecimais em nomes de cores
    cores_selecionadas = [obter_nome_cor(cor) for cor in colors]

    # Configurar mensagem de e-mail
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = 'Novo Pedido de Impressão'

    # Construir o corpo do e-mail com todas as cores selecionadas, o tipo de material e as informações de contato
    corpo_email = f"""
    Olá,

    Um novo pedido de orçamento foi recebido com as seguintes informações:

    Quantidade de Cores: {quantity}
    Cores Selecionadas:"""

    for i, cor in enumerate(cores_selecionadas, start=1):
        corpo_email += f"\nCor {i}: {cor}"

    corpo_email += f"""
    Tipo de Material: {material}
    Email para Contato: {email}
    Número de Telefone para Contato: {phone}
    Anexo: Imagem para impressão

    Atenciosamente,
    cliente
    """

    mensagem.attach(MIMEText(corpo_email, 'plain'))

    # Anexar a imagem ao e-mail
    anexo = MIMEBase('application', 'octet-stream')
    anexo.set_payload(image.read())
    encoders.encode_base64(anexo)  # Corrigido para usar o módulo encoders
    anexo.add_header('Content-Disposition', f'attachment; filename= {image.filename}')

    mensagem.attach(anexo)

    # Enviar e-mail
    servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(remetente, senha)
    servidor_smtp.sendmail(remetente, destinatario, mensagem.as_string())
    servidor_smtp.quit()

def obter_nome_cor(cor_hexadecimal):
    cores = {
        '#ff0000': 'Vermelho',
        '#ff7f00': 'Laranja',
        '#ffff00': 'Amarelo',
        '#00ff00': 'Verde',
        '#008000': 'Verde Escuro',
        '#0000ff': 'Azul',
        '#4b0082': 'Índigo',
        '#9400d3': 'Violeta',
        '#ff00ff': 'Magenta',
        '#ffc0cb': 'Rosa',
        '#a52a2a': 'Marrom',
        '#ffffff': 'Branco',
        '#000000': 'Preto',
        '#808080': 'Cinza',
        '#800080': 'Roxo',
        '#00ffff': 'Ciano',
        '#ffff80': 'Lima',
        '#ffd700': 'Dourado',
        '#8b4513': 'Marrom Sela',
        '#ff4500': 'Laranja Vermelho',
        '#ffe4b5': 'Amêndoa',
        '#7fffd4': 'Aquamarina',
        '#b0e0e6': 'Azul Pólvora',
        '#dda0dd': 'Violeta Médio',
        '#ff6347': 'Vermelho Tomate',
        # Adicione mais cores conforme necessário
    }
    # Retorna o nome da cor se estiver na lista, caso contrário retorna o próprio código hexadecimal
    return cores.get(cor_hexadecimal.lower(), cor_hexadecimal)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
