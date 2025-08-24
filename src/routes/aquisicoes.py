from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.aquisicao import Aquisicao

aquisicoes_bp = Blueprint('aquisicoes', __name__)

@aquisicoes_bp.route('/aquisicoes', methods=['GET'])
def listar_aquisicoes():
    try:
        aquisicoes = Aquisicao.query.all()
        return jsonify([a.to_dict() for a in aquisicoes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@aquisicoes_bp.route('/aquisicoes', methods=['POST'])
def criar_aquisicao():
    try:
        data = request.get_json()
        
        required_fields = ['nome_despesa', 'valor']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        valor = float(data['valor'])
        
        # Calcular créditos PIS e COFINS (alíquotas padrão)
        pis_credito = valor * 0.0165  # 1,65%
        cofins_credito = valor * 0.076  # 7,6%
        
        # CBS crédito será calculado posteriormente
        cbs_credito = data.get('cbs_credito', 0)
        
        aquisicao = Aquisicao(
            nome_despesa=data['nome_despesa'],
            valor=valor,
            pis_credito=pis_credito,
            cofins_credito=cofins_credito,
            cbs_credito=cbs_credito
        )
        
        db.session.add(aquisicao)
        db.session.commit()
        
        return jsonify(aquisicao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@aquisicoes_bp.route('/aquisicoes/<int:id>', methods=['PUT'])
def atualizar_aquisicao(id):
    try:
        aquisicao = Aquisicao.query.get_or_404(id)
        data = request.get_json()
        
        if 'nome_despesa' in data:
            aquisicao.nome_despesa = data['nome_despesa']
        
        if 'valor' in data:
            aquisicao.valor = float(data['valor'])
            # Recalcular créditos
            aquisicao.pis_credito = aquisicao.valor * 0.0165
            aquisicao.cofins_credito = aquisicao.valor * 0.076
        
        if 'cbs_credito' in data:
            aquisicao.cbs_credito = float(data['cbs_credito'])
        
        db.session.commit()
        return jsonify(aquisicao.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@aquisicoes_bp.route('/aquisicoes/<int:id>', methods=['DELETE'])
def remover_aquisicao(id):
    try:
        aquisicao = Aquisicao.query.get_or_404(id)
        db.session.delete(aquisicao)
        db.session.commit()
        return jsonify({'message': 'Aquisição removida com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@aquisicoes_bp.route('/aquisicoes/totais', methods=['GET'])
def calcular_totais():
    try:
        aquisicoes = Aquisicao.query.all()
        
        total_aquisicoes = sum(float(a.valor) for a in aquisicoes)
        total_pis_credito = sum(float(a.pis_credito) for a in aquisicoes)
        total_cofins_credito = sum(float(a.cofins_credito) for a in aquisicoes)
        total_cbs_credito = sum(float(a.cbs_credito) for a in aquisicoes)
        
        return jsonify({
            'total_aquisicoes': total_aquisicoes,
            'total_pis_credito': total_pis_credito,
            'total_cofins_credito': total_cofins_credito,
            'total_cbs_credito': total_cbs_credito,
            'quantidade_aquisicoes': len(aquisicoes)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

