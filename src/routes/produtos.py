from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.produto import Produto

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    try:
        produtos = Produto.query.all()
        return jsonify([p.to_dict() for p in produtos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/produtos', methods=['POST'])
def criar_produto():
    try:
        data = request.get_json()
        
        required_fields = ['ncm', 'cst', 'valor_venda', 'tributado']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} é obrigatório'}), 400
        
        # Verificar se já existem 10 produtos
        count = Produto.query.count()
        if count >= 10:
            return jsonify({'error': 'Máximo de 10 produtos permitido'}), 400
        
        # Validar NCM (8 dígitos)
        if len(data['ncm']) != 8 or not data['ncm'].isdigit():
            return jsonify({'error': 'NCM deve conter exatamente 8 dígitos'}), 400
        
        # Calcular PIS e COFINS apenas se tributado
        valor_venda = float(data['valor_venda'])
        tributado = data['tributado']
        
        if tributado:
            pis_debito = valor_venda * 0.0165  # 1,65%
            cofins_debito = valor_venda * 0.076  # 7,6%
        else:
            pis_debito = 0
            cofins_debito = 0
        
        produto = Produto(
            ncm=data['ncm'],
            cst=data['cst'],
            valor_venda=valor_venda,
            tributado=tributado,
            pis_debito=pis_debito,
            cofins_debito=cofins_debito
        )
        
        db.session.add(produto)
        db.session.commit()
        
        return jsonify(produto.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    try:
        produto = Produto.query.get_or_404(id)
        data = request.get_json()
        
        if 'valor_venda' in data:
            produto.valor_venda = float(data['valor_venda'])
            # Recalcular PIS e COFINS se tributado
            if produto.tributado:
                produto.pis_debito = produto.valor_venda * 0.0165
                produto.cofins_debito = produto.valor_venda * 0.076
            else:
                produto.pis_debito = 0
                produto.cofins_debito = 0
        
        if 'ncm' in data:
            if len(data['ncm']) != 8 or not data['ncm'].isdigit():
                return jsonify({'error': 'NCM deve conter exatamente 8 dígitos'}), 400
            produto.ncm = data['ncm']
        
        if 'cst' in data:
            produto.cst = data['cst']
        
        if 'tributado' in data:
            produto.tributado = data['tributado']
            # Recalcular PIS e COFINS baseado no novo status de tributação
            if produto.tributado:
                produto.pis_debito = produto.valor_venda * 0.0165
                produto.cofins_debito = produto.valor_venda * 0.076
            else:
                produto.pis_debito = 0
                produto.cofins_debito = 0
        
        db.session.commit()
        return jsonify(produto.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/produtos/<int:id>', methods=['DELETE'])
def remover_produto(id):
    try:
        produto = Produto.query.get_or_404(id)
        db.session.delete(produto)
        db.session.commit()
        return jsonify({'message': 'Produto removido com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/produtos/totais', methods=['GET'])
def calcular_totais():
    try:
        produtos = Produto.query.all()
        
        total_vendas = sum(float(p.valor_venda) for p in produtos)
        total_pis_debito = sum(float(p.pis_debito) for p in produtos)
        total_cofins_debito = sum(float(p.cofins_debito) for p in produtos)
        
        return jsonify({
            'total_vendas': total_vendas,
            'total_pis_debito': total_pis_debito,
            'total_cofins_debito': total_cofins_debito,
            'quantidade_produtos': len(produtos)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

