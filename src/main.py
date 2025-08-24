import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.participantes import participantes_bp
from src.routes.produtos import produtos_bp
from src.routes.aquisicoes import aquisicoes_bp
from src.routes.calculos import calculos_bp
from src.routes.xml_processor import xml_bp
from src.routes.consultas import consultas_bp
from src.routes.parecer import parecer_bp
from src.config import get_config

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuração baseada no ambiente
# No Render, forçar ambiente de produção
if os.environ.get('RENDER'):
    app.config['FLASK_ENV'] = 'production'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/app.db"
else:
    config = get_config()
    app.config.from_object(config)

# Habilitar CORS para todas as rotas
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(participantes_bp, url_prefix='/api')
app.register_blueprint(produtos_bp, url_prefix='/api')
app.register_blueprint(aquisicoes_bp, url_prefix='/api')
app.register_blueprint(calculos_bp, url_prefix='/api')
app.register_blueprint(xml_bp, url_prefix='/api')
app.register_blueprint(consultas_bp, url_prefix='/api')
app.register_blueprint(parecer_bp, url_prefix='/api')

# Configuração do banco de dados
db.init_app(app)

# Importar todos os modelos para criar as tabelas
from src.models.participante import Participante
from src.models.produto import Produto
from src.models.aquisicao import Aquisicao
from src.models.calculo import Calculo, XmlCbs

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config.get('DEBUG', False))
