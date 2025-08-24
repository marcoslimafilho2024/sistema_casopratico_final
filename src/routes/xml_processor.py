from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.calculo import XmlCbs
from src.models.produto import Produto
import xml.etree.ElementTree as ET
import re

xml_bp = Blueprint('xml', __name__)

@xml_bp.route('/xml/processar', methods=['POST'])
def processar_xml():
    try:
        data = request.get_json()
        
        if 'xml_content' not in data or 'ncm' not in data:
            return jsonify({'error': 'XML content e NCM são obrigatórios'}), 400
        
        xml_content = data['xml_content']
        ncm = data['ncm']
        
        # Validar se o NCM existe nos produtos cadastrados
        produto = Produto.query.filter_by(ncm=ncm).first()
        if not produto:
            return jsonify({'error': f'NCM {ncm} não encontrado nos produtos cadastrados'}), 400
        
        # Processar XML
        try:
            # Limpar e preparar XML
            xml_clean = xml_content.strip()
            if not xml_clean.startswith('<?xml'):
                xml_clean = '<?xml version="1.0" encoding="UTF-8"?>' + xml_clean
            
            root = ET.fromstring(xml_clean)
            
            # Extrair valores do XML
            base_calculo = 0
            valor_cbs = 0
            
            # Buscar vBC (base de cálculo)
            vbc_elements = root.findall('.//vBC')
            for vbc in vbc_elements:
                if vbc.text:
                    base_calculo += float(vbc.text)
            
            # Buscar vCBS (valor CBS)
            vcbs_elements = root.findall('.//vCBS')
            for vcbs in vcbs_elements:
                if vcbs.text:
                    valor_cbs += float(vcbs.text)
            
            # Verificar se já existe XML para este NCM
            xml_existente = XmlCbs.query.filter_by(ncm=ncm).first()
            if xml_existente:
                # Atualizar existente
                xml_existente.xml_content = xml_content
                xml_existente.base_calculo = base_calculo
                xml_existente.valor_cbs = valor_cbs
                xml_existente.processado = True
                xml_obj = xml_existente
            else:
                # Criar novo
                xml_obj = XmlCbs(
                    ncm=ncm,
                    xml_content=xml_content,
                    base_calculo=base_calculo,
                    valor_cbs=valor_cbs,
                    processado=True
                )
                db.session.add(xml_obj)
            
            db.session.commit()
            
            return jsonify({
                'id': xml_obj.id,
                'ncm': ncm,
                'base_calculo': base_calculo,
                'valor_cbs': valor_cbs,
                'message': 'XML processado com sucesso'
            }), 200
            
        except ET.ParseError as e:
            return jsonify({'error': f'Erro ao processar XML: {str(e)}'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@xml_bp.route('/xml/ncms-produtos', methods=['GET'])
def listar_ncms_produtos():
    try:
        produtos = Produto.query.all()
        ncms = []
        
        for produto in produtos:
            # Verificar se já tem XML processado
            xml_processado = XmlCbs.query.filter_by(ncm=produto.ncm, processado=True).first()
            
            ncms.append({
                'ncm': produto.ncm,
                'valor_venda': float(produto.valor_venda),
                'xml_processado': xml_processado is not None,
                'xml_id': xml_processado.id if xml_processado else None
            })
        
        return jsonify(ncms), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@xml_bp.route('/xml/totais', methods=['GET'])
def calcular_totais_xml():
    try:
        xmls = XmlCbs.query.filter_by(processado=True).all()
        
        total_base_calculo = sum(float(x.base_calculo) for x in xmls)
        total_valor_cbs = sum(float(x.valor_cbs) for x in xmls)
        
        return jsonify({
            'total_base_calculo': total_base_calculo,
            'total_valor_cbs': total_valor_cbs,
            'quantidade_xmls': len(xmls),
            'xmls': [x.to_dict() for x in xmls]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@xml_bp.route('/xml/<int:id>', methods=['DELETE'])
def remover_xml(id):
    try:
        xml_obj = XmlCbs.query.get_or_404(id)
        db.session.delete(xml_obj)
        db.session.commit()
        return jsonify({'message': 'XML removido com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

