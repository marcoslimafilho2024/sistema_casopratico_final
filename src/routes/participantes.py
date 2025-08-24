from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.participante import Participante

participantes_bp = Blueprint('participantes', __name__)

@participantes_bp.route('/participantes', methods=['GET'])
def listar_participantes():
    try:
        participantes = Participante.query.filter_by(ativo=True).all()
        return jsonify([p.to_dict() for p in participantes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@participantes_bp.route('/participantes', methods=['POST'])
def criar_participante():
    try:
        data = request.get_json()
        
        if not data or 'nome_completo' not in data:
            return jsonify({'error': 'Nome completo é obrigatório'}), 400
        
        # Verificar se já existem 10 participantes
        count = Participante.query.filter_by(ativo=True).count()
        if count >= 10:
            return jsonify({'error': 'Máximo de 10 participantes permitido'}), 400
        
        participante = Participante(nome_completo=data['nome_completo'])
        db.session.add(participante)
        db.session.commit()
        
        return jsonify(participante.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@participantes_bp.route('/participantes/<int:id>', methods=['PUT'])
def atualizar_participante(id):
    try:
        participante = Participante.query.get_or_404(id)
        data = request.get_json()
        
        if 'nome_completo' in data:
            participante.nome_completo = data['nome_completo']
        
        db.session.commit()
        return jsonify(participante.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@participantes_bp.route('/participantes/<int:id>', methods=['DELETE'])
def remover_participante(id):
    try:
        participante = Participante.query.get_or_404(id)
        participante.ativo = False
        db.session.commit()
        return jsonify({'message': 'Participante removido com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

