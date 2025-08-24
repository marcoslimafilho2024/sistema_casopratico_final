from flask import Blueprint, request, jsonify
import os
import pandas as pd
from docx import Document
from src.models.user import db
from src.models.participante import Participante

consultas_bp = Blueprint('consultas', __name__)

@consultas_bp.route('/consultas/aliquotas-zero', methods=['GET'])
def consultar_aliquotas_zero():
    try:
        # Ler arquivo DOC de alíquotas zero
        doc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'ALIQUOTAZEROPISECOFINS.doc')
        
        # Para simplificar, vamos retornar dados estruturados baseados no que lemos
        # Em uma implementação real, seria necessário processar o documento DOC
        
        aliquotas_zero = [
            {
                'codigo': '100',
                'descricao': 'INSUMOS E PRODUTOS AGROPECUÁRIOS',
                'ncm': '',
                'inicio': '01/2011',
                'termino': ''
            },
            {
                'codigo': '101',
                'descricao': 'Adubos ou fertilizantes classificados no Capítulo 31',
                'ncm': '',
                'inicio': '01/2011',
                'termino': ''
            },
            {
                'codigo': '113',
                'descricao': 'Farinha de trigo',
                'ncm': '1101.00.10',
                'inicio': '01/2011',
                'termino': ''
            },
            {
                'codigo': '114',
                'descricao': 'Trigo',
                'ncm': '10.01',
                'inicio': '01/2011',
                'termino': ''
            },
            {
                'codigo': '124',
                'descricao': 'Açúcar classificado nos códigos 1701.14.00 e 1701.99.00',
                'ncm': '1701.14.00, 1701.99.00',
                'inicio': '08/03/2013',
                'termino': ''
            }
        ]
        
        return jsonify({
            'message': 'Consulta de produtos com alíquota zero de PIS e COFINS',
            'aviso': 'IMPORTANTE: Produtos constantes na tabela possuem ALÍQUOTA ZERO para PIS e COFINS',
            'produtos': aliquotas_zero
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@consultas_bp.route('/csts', methods=['GET'])
def listar_csts():
    """Lista os CSTs disponíveis para PIS/COFINS"""
    csts = [
        {"codigo": "01", "descricao": "Operação Tributável (base de cálculo = valor da operação (alíquota normal (cumulativo/não cumulativo)))"},
        {"codigo": "02", "descricao": "Operação Tributável (base de cálculo = valor da operação (alíquota diferenciada))"},
        {"codigo": "03", "descricao": "Operação Tributável (base de cálculo = quantidade vendida por alíquota por unidade de produto)"},
        {"codigo": "04", "descricao": "Tributação monofásica (alíquota zero)"},
        {"codigo": "05", "descricao": "Operação Tributável (ST)"},
        {"codigo": "06", "descricao": "Operação Tributável (alíquota zero)"},
        {"codigo": "07", "descricao": "Operação Isenta da Contribuição"},
        {"codigo": "08", "descricao": "Operação Sem Incidência da Contribuição"},
        {"codigo": "09", "descricao": "Operação com Suspensão da Contribuição"},
        {"codigo": "49", "descricao": "Outras Operações de Saída"},
        {"codigo": "50", "descricao": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno"},
        {"codigo": "51", "descricao": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno"},
        {"codigo": "52", "descricao": "Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação"},
        {"codigo": "53", "descricao": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno"},
        {"codigo": "54", "descricao": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação"},
        {"codigo": "55", "descricao": "Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação"},
        {"codigo": "56", "descricao": "Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno e de Exportação"},
        {"codigo": "60", "descricao": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno"},
        {"codigo": "61", "descricao": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno"},
        {"codigo": "62", "descricao": "Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação"},
        {"codigo": "63", "descricao": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno"},
        {"codigo": "64", "descricao": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação"},
        {"codigo": "65", "descricao": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação"},
        {"codigo": "66", "descricao": "Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno e de Exportação"},
        {"codigo": "67", "descricao": "Crédito Presumido - Outras Operações"},
        {"codigo": "70", "descricao": "Operação de Aquisição sem Direito a Crédito"},
        {"codigo": "71", "descricao": "Operação de Aquisição com Isenção"},
        {"codigo": "72", "descricao": "Operação de Aquisição com Suspensão"},
        {"codigo": "73", "descricao": "Operação de Aquisição a Alíquota Zero"},
        {"codigo": "74", "descricao": "Operação de Aquisição sem Incidência da Contribuição"},
        {"codigo": "75", "descricao": "Operação de Aquisição por ST"},
        {"codigo": "98", "descricao": "Outras Operações de Entrada"},
        {"codigo": "99", "descricao": "Outras Operações"}
    ]
    return jsonify(csts), 200

@consultas_bp.route('/consultas/reforma-tributaria', methods=['GET'])
def consultar_reforma_tributaria():
    try:
        # Ler arquivo CSV da reforma tributária
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'reforma_tributaria.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # Converter para lista de dicionários
            produtos_lc214 = []
            for _, row in df.head(50).iterrows():  # Limitar a 50 primeiros para performance
                produtos_lc214.append({
                    'anexo': str(row.get('ANEXO', '')),
                    'item': str(row.get('ITEM', '')),
                    'descricao': str(row.get('DESCRIÇÃO DO PRODUTO', '')),
                    'ncm': str(row.get('NBS / NCM/SH', '')),
                    'tipo_reducao': str(row.get('REDUÇÃO/ALÍQUOTA', '')),
                    'percentual': float(row.get('% RED/ALIQ', 0)) if pd.notna(row.get('% RED/ALIQ')) else 0
                })
            
            return jsonify({
                'message': 'Produtos da Lei Complementar 214/2025 - Reforma Tributária',
                'total_registros': len(df),
                'registros_exibidos': len(produtos_lc214),
                'produtos': produtos_lc214
            }), 200
        else:
            return jsonify({'error': 'Arquivo da reforma tributária não encontrado'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@consultas_bp.route('/consultas/ncm/<ncm>', methods=['GET'])
def consultar_ncm(ncm):
    try:
        # Buscar NCM na tabela da reforma tributária
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'reforma_tributaria.csv')
        
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            
            # Filtrar por NCM
            resultado = df[df['NBS / NCM/SH'].astype(str).str.contains(ncm, na=False)]
            
            if not resultado.empty:
                produtos_encontrados = []
                for _, row in resultado.iterrows():
                    produtos_encontrados.append({
                        'anexo': str(row.get('ANEXO', '')),
                        'item': str(row.get('ITEM', '')),
                        'descricao': str(row.get('DESCRIÇÃO DO PRODUTO', '')),
                        'ncm': str(row.get('NBS / NCM/SH', '')),
                        'tipo_reducao': str(row.get('REDUÇÃO/ALÍQUOTA', '')),
                        'percentual': float(row.get('% RED/ALIQ', 0)) if pd.notna(row.get('% RED/ALIQ')) else 0
                    })
                
                return jsonify({
                    'ncm_consultado': ncm,
                    'encontrados': len(produtos_encontrados),
                    'produtos': produtos_encontrados
                }), 200
            else:
                return jsonify({
                    'ncm_consultado': ncm,
                    'encontrados': 0,
                    'message': 'NCM não encontrado na tabela da reforma tributária'
                }), 404
        else:
            return jsonify({'error': 'Arquivo da reforma tributária não encontrado'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

