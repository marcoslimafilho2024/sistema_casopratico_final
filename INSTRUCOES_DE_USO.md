# Sistema de Cálculo Tributário - PIS/COFINS e CBS

## Instruções de Instalação e Uso

### Pré-requisitos
- Python 3.11+
- Node.js 18+ (para desenvolvimento do frontend)

### Instalação

1. **Clone ou baixe o projeto**
   ```bash
   cd sistema_tributario
   ```

2. **Ative o ambiente virtual e instale dependências**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Execute o sistema**
   ```bash
   python src/main.py
   ```

4. **Acesse o sistema**
   - Abra o navegador em: http://localhost:5000
   - O sistema estará disponível com tema dark

### Funcionalidades Implementadas

#### ✅ Cadastro de Participantes
- Cadastro de até 10 participantes da equipe
- Validação de limite máximo
- Interface intuitiva com tema dark

#### ✅ Etapa 1 - PIS e COFINS
- **Vendas**: Cadastro de produtos com NCM, CST e valores
- **Aquisições**: Cadastro de despesas e aquisições
- **Apuração**: Cálculo automático de débitos e créditos
- Geração de arquivo TXT com memória de cálculo

#### ✅ Etapa 2 - CBS
- **Preparação**: Lista de NCMs com checklist
- **Integração**: Link para calculadora oficial da reforma
- **Processamento XML**: Importação e processamento de XMLs
- **Apuração CBS**: Cálculo final da CBS

#### ✅ Consultas de Tabelas
- **Alíquota Zero**: Produtos com alíquota zero PIS/COFINS
- **CST**: Códigos de Situação Tributária
- **LC 214/2025**: Tabela da reforma tributária
- **Consulta NCM**: Busca específica por NCM

#### ✅ Parecer Técnico
- Geração automática com IA (OpenAI)
- Parecer dissertativo com introdução, desenvolvimento e conclusão
- Baseado nos cálculos realizados
- Download em formato TXT

### Fluxo de Uso

1. **Cadastre os participantes** (até 10)
2. **Etapa 1 - PIS/COFINS**:
   - Adicione produtos (vendas)
   - Adicione aquisições/despesas
   - Execute a apuração
3. **Etapa 2 - CBS**:
   - Acesse a calculadora da reforma
   - Processe os XMLs gerados
   - Execute a apuração CBS
4. **Gere o parecer técnico** final

### Arquivos de Dados Inclusos

- `ALIQUOTAZEROPISECOFINS.doc` - Tabela de alíquotas zero
- `TABELACSTPISECOFINS.doc` - Códigos CST
- `REFORMATRIBUTÁRIA-PRODUTOSLC214.xlsx` - Lei Complementar 214/2025
- `XML.txt` - Exemplo de XML CBS

### Tecnologias Utilizadas

**Backend:**
- Flask (Python)
- SQLAlchemy (ORM)
- Pandas (processamento de dados)
- OpenAI API (geração de parecer)

**Frontend:**
- React 18
- Tailwind CSS (tema dark)
- Axios (comunicação HTTP)
- Shadcn/UI (componentes)

### Suporte

O sistema foi desenvolvido conforme as especificações do PowerPoint fornecido, implementando todas as funcionalidades solicitadas com interface em tema dark profissional.

Para dúvidas ou suporte, consulte a documentação técnica ou entre em contato com a equipe de desenvolvimento.

---

**IPOG - Projeto do Caso Prático Final**
*Sistema Público da Escrituração Digital e os Impactos da Reforma Tributária*

