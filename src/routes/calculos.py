from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.calculo import Calculo, XmlCbs
from src.models.produto import Produto
from src.models.aquisicao import Aquisicao
import xml.etree.ElementTree as ET
from datetime import datetime
import os

calculos_bp = Blueprint('calculos', __name__)

@calculos_bp.route('/calculos/pis-cofins', methods=['POST'])
def calcular_pis_cofins():
    try:
        # Buscar totais de produtos (débitos)
        produtos = Produto.query.all()
        total_pis_debito = sum(float(p.pis_debito) for p in produtos)
        total_cofins_debito = sum(float(p.cofins_debito) for p in produtos)
        
        # Buscar totais de aquisições (créditos)
        aquisicoes = Aquisicao.query.all()
        total_pis_credito = sum(float(a.pis_credito) for a in aquisicoes)
        total_cofins_credito = sum(float(a.cofins_credito) for a in aquisicoes)
        
        # Calcular resultados
        resultado_pis = total_pis_debito - total_pis_credito
        resultado_cofins = total_cofins_debito - total_cofins_credito
        resultado_total = resultado_pis + resultado_cofins
        
        # Gerar memória de cálculo
        memoria_calculo = f"""MEMÓRIA DE CÁLCULO - PIS E COFINS
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

=== DÉBITOS (VENDAS) ===
PIS Total do Débito: R$ {total_pis_debito:,.2f}
COFINS Total do Débito: R$ {total_cofins_debito:,.2f}

Produtos:
"""
        for produto in produtos:
            memoria_calculo += f"NCM: {produto.ncm} - Valor: R$ {produto.valor_venda:,.2f} - PIS: R$ {produto.pis_debito:,.2f} - COFINS: R$ {produto.cofins_debito:,.2f}\n"
        
        memoria_calculo += f"""
=== CRÉDITOS (AQUISIÇÕES) ===
PIS Total do Crédito: R$ {total_pis_credito:,.2f}
COFINS Total do Crédito: R$ {total_cofins_credito:,.2f}

Aquisições:
"""
        for aquisicao in aquisicoes:
            memoria_calculo += f"{aquisicao.nome_despesa} - Valor: R$ {aquisicao.valor:,.2f} - PIS: R$ {aquisicao.pis_credito:,.2f} - COFINS: R$ {aquisicao.cofins_credito:,.2f}\n"
        
        memoria_calculo += f"""
=== APURAÇÃO ===
PIS = R$ {total_pis_debito:,.2f} - R$ {total_pis_credito:,.2f} = R$ {resultado_pis:,.2f}
COFINS = R$ {total_cofins_debito:,.2f} - R$ {total_cofins_credito:,.2f} = R$ {resultado_cofins:,.2f}

TOTAL A RECOLHER: R$ {resultado_total:,.2f}
"""
        
        # Salvar no banco
        calculo = Calculo(
            tipo='PIS_COFINS',
            total_debito=total_pis_debito + total_cofins_debito,
            total_credito=total_pis_credito + total_cofins_credito,
            resultado=resultado_total,
            arquivo_txt=memoria_calculo
        )
        
        db.session.add(calculo)
        db.session.commit()
        
        return jsonify({
            'id': calculo.id,
            'total_pis_debito': total_pis_debito,
            'total_cofins_debito': total_cofins_debito,
            'total_pis_credito': total_pis_credito,
            'total_cofins_credito': total_cofins_credito,
            'resultado_pis': resultado_pis,
            'resultado_cofins': resultado_cofins,
            'resultado_total': resultado_total,
            'memoria_calculo': memoria_calculo
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@calculos_bp.route('/calculos/cbs', methods=['POST'])
def calcular_cbs():
    try:
        # Buscar XMLs processados
        xmls = XmlCbs.query.filter_by(processado=True).all()
        total_base_calculo = sum(float(x.base_calculo) for x in xmls)
        total_cbs_debito = sum(float(x.valor_cbs) for x in xmls)
        
        # Buscar créditos CBS das aquisições
        aquisicoes = Aquisicao.query.all()
        total_cbs_credito = sum(float(a.cbs_credito) for a in aquisicoes)
        
        # Calcular resultado
        resultado_cbs = total_cbs_debito - total_cbs_credito
        
        # Gerar memória de cálculo
        memoria_calculo = f"""MEMÓRIA DE CÁLCULO - CBS
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

=== DÉBITOS (VENDAS CBS) ===
Base de Cálculo Total: R$ {total_base_calculo:,.2f}
CBS Total do Débito: R$ {total_cbs_debito:,.2f}

XMLs Processados:
"""
        for xml in xmls:
            memoria_calculo += f"NCM: {xml.ncm} - Base: R$ {xml.base_calculo:,.2f} - CBS: R$ {xml.valor_cbs:,.2f}\n"
        
        memoria_calculo += f"""
=== CRÉDITOS (AQUISIÇÕES CBS) ===
CBS Total do Crédito: R$ {total_cbs_credito:,.2f}

Aquisições:
"""
        for aquisicao in aquisicoes:
            memoria_calculo += f"{aquisicao.nome_despesa} - CBS Crédito: R$ {aquisicao.cbs_credito:,.2f}\n"
        
        memoria_calculo += f"""
=== APURAÇÃO CBS ===
CBS = R$ {total_cbs_debito:,.2f} - R$ {total_cbs_credito:,.2f} = R$ {resultado_cbs:,.2f}

TOTAL CBS A RECOLHER: R$ {resultado_cbs:,.2f}
"""
        
        # Salvar no banco
        calculo = Calculo(
            tipo='CBS',
            total_debito=total_cbs_debito,
            total_credito=total_cbs_credito,
            resultado=resultado_cbs,
            arquivo_txt=memoria_calculo
        )
        
        db.session.add(calculo)
        db.session.commit()
        
        return jsonify({
            'id': calculo.id,
            'total_base_calculo': total_base_calculo,
            'total_cbs_debito': total_cbs_debito,
            'total_cbs_credito': total_cbs_credito,
            'resultado_cbs': resultado_cbs,
            'memoria_calculo': memoria_calculo
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@calculos_bp.route('/calculos/<int:id>/txt', methods=['GET'])
def baixar_txt(id):
    try:
        calculo = Calculo.query.get_or_404(id)
        
        # Criar arquivo temporário
        filename = f"memoria_calculo_{calculo.tipo}_{calculo.id}.txt"
        filepath = os.path.join('/tmp', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(calculo.arquivo_txt)
        
        return jsonify({
            'filename': filename,
            'content': calculo.arquivo_txt
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@calculos_bp.route('/calculos', methods=['GET'])
def listar_calculos():
    try:
        calculos = Calculo.query.order_by(Calculo.data_calculo.desc()).all()
        return jsonify([c.to_dict() for c in calculos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

