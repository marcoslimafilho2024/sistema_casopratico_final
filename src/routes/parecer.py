from flask import Blueprint, request, jsonify
from src.models.calculo import Calculo
import openai
import os

parecer_bp = Blueprint('parecer', __name__)

@parecer_bp.route('/parecer/gerar', methods=['POST'])
def gerar_parecer():
    try:
        # Buscar os dois cálculos mais recentes
        calculo_pis_cofins = Calculo.query.filter_by(tipo='PIS_COFINS').order_by(Calculo.data_calculo.desc()).first()
        calculo_cbs = Calculo.query.filter_by(tipo='CBS').order_by(Calculo.data_calculo.desc()).first()
        
        if not calculo_pis_cofins or not calculo_cbs:
            return jsonify({'error': 'É necessário ter os cálculos de PIS/COFINS e CBS realizados'}), 400
        
        # Preparar prompt para IA
        prompt = f"""Gostaria de elaborar um parecer técnico dissertativo e em parágrafos com Introdução, desenvolvimento dos cálculos apresentados em anexo e conclusão.

DADOS DOS CÁLCULOS:

=== CÁLCULO PIS/COFINS ===
{calculo_pis_cofins.arquivo_txt}

=== CÁLCULO CBS ===
{calculo_cbs.arquivo_txt}

Por favor, elabore um parecer técnico profissional que:
1. Faça uma introdução sobre o contexto da reforma tributária e a transição do PIS/COFINS para CBS
2. Desenvolva uma análise comparativa dos cálculos apresentados
3. Apresente as principais diferenças e impactos identificados
4. Conclua com recomendações técnicas

O parecer deve ser formal, técnico e adequado para apresentação em ambiente acadêmico ou profissional."""

        # Chamar API OpenAI
        client = openai.OpenAI()
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um especialista em tributação brasileira, com conhecimento profundo sobre PIS, COFINS e a nova CBS (Contribuição sobre Bens e Serviços). Elabore pareceres técnicos profissionais e detalhados."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        parecer_texto = response.choices[0].message.content
        
        return jsonify({
            'parecer': parecer_texto,
            'data_geracao': calculo_pis_cofins.data_calculo.isoformat(),
            'calculos_utilizados': {
                'pis_cofins_id': calculo_pis_cofins.id,
                'cbs_id': calculo_cbs.id
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar parecer: {str(e)}'}), 500

@parecer_bp.route('/parecer/exemplo', methods=['GET'])
def gerar_parecer_exemplo():
    """Endpoint para gerar um parecer de exemplo sem usar IA"""
    try:
        # Buscar os dois cálculos mais recentes
        calculo_pis_cofins = Calculo.query.filter_by(tipo='PIS_COFINS').order_by(Calculo.data_calculo.desc()).first()
        calculo_cbs = Calculo.query.filter_by(tipo='CBS').order_by(Calculo.data_calculo.desc()).first()
        
        if not calculo_pis_cofins or not calculo_cbs:
            return jsonify({'error': 'É necessário ter os cálculos de PIS/COFINS e CBS realizados'}), 400
        
        parecer_exemplo = f"""PARECER TÉCNICO COMPARATIVO
ANÁLISE DOS IMPACTOS DA REFORMA TRIBUTÁRIA: PIS/COFINS vs CBS

INTRODUÇÃO

A reforma tributária brasileira, instituída pela Lei Complementar nº 214/2025, representa uma das mais significativas mudanças no sistema tributário nacional das últimas décadas. A substituição gradual do PIS (Programa de Integração Social) e da COFINS (Contribuição para o Financiamento da Seguridade Social) pela CBS (Contribuição sobre Bens e Serviços) visa simplificar a tributação sobre o consumo e reduzir a complexidade do sistema tributário brasileiro.

O presente parecer técnico tem por objetivo analisar comparativamente os cálculos realizados sob o regime atual (PIS/COFINS) e o novo regime (CBS), identificando os principais impactos e diferenças para a empresa em análise.

DESENVOLVIMENTO DOS CÁLCULOS

Análise do Regime Atual (PIS/COFINS):
- Total de débitos apurados: R$ {calculo_pis_cofins.total_debito:,.2f}
- Total de créditos apurados: R$ {calculo_pis_cofins.total_credito:,.2f}
- Valor líquido a recolher: R$ {calculo_pis_cofins.resultado:,.2f}

Análise do Novo Regime (CBS):
- Total de débitos CBS: R$ {calculo_cbs.total_debito:,.2f}
- Total de créditos CBS: R$ {calculo_cbs.total_credito:,.2f}
- Valor líquido CBS a recolher: R$ {calculo_cbs.resultado:,.2f}

Comparativo dos Regimes:
A diferença entre os regimes representa um impacto de R$ {abs(calculo_cbs.resultado - calculo_pis_cofins.resultado):,.2f}, sendo {'favorável' if calculo_cbs.resultado < calculo_pis_cofins.resultado else 'desfavorável'} ao contribuinte no novo regime CBS.

CONCLUSÃO

Com base na análise comparativa realizada, observa-se que a transição do regime PIS/COFINS para CBS apresenta impactos significativos na tributação da empresa. A nova sistemática da CBS, com sua base de cálculo e alíquotas diferenciadas, resulta em uma carga tributária {'menor' if calculo_cbs.resultado < calculo_pis_cofins.resultado else 'maior'} em relação ao regime atual.

Recomenda-se:
1. Acompanhamento contínuo da evolução da legislação da CBS;
2. Revisão dos processos internos para adequação ao novo regime;
3. Análise periódica dos impactos tributários;
4. Planejamento tributário considerando a transição gradual entre os regimes.

Este parecer foi elaborado com base nos dados fornecidos e na legislação vigente, devendo ser revisado periodicamente conforme a evolução normativa da reforma tributária.

Data: {calculo_pis_cofins.data_calculo.strftime('%d/%m/%Y')}"""

        return jsonify({
            'parecer': parecer_exemplo,
            'data_geracao': calculo_pis_cofins.data_calculo.isoformat(),
            'calculos_utilizados': {
                'pis_cofins_id': calculo_pis_cofins.id,
                'cbs_id': calculo_cbs.id
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao gerar parecer: {str(e)}'}), 500

