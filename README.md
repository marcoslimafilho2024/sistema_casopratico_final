# Sistema de Cálculo Tributário - PIS/COFINS e CBS

## 📋 Descrição

Sistema web completo para cálculo tributário, implementando PIS/COFINS e CBS (Contribuição sobre Bens e Serviços) conforme a reforma tributária. Desenvolvido como projeto final do IPOG.

## 🚀 Deploy no Render.com

### Pré-requisitos
- Conta no [GitHub](https://github.com)
- Conta no [Render.com](https://render.com)
- Projeto já configurado com Git

### Passo a Passo para Deploy

#### 1. Preparar o Repositório GitHub

```bash
# No diretório do projeto
git add .
git commit -m "Configuração para deploy no Render.com"
git push origin main
```

#### 2. Conectar ao Render.com

1. Acesse [render.com](https://render.com) e faça login
2. Clique em **"New +"** → **"Web Service"**
3. Conecte sua conta GitHub
4. Selecione o repositório `sistema_tributario`
5. Configure o serviço:
   - **Name**: `sistema-tributario`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn src.main:app --bind 0.0.0.0:$PORT`
   - **Plan**: `Free`

#### 3. Variáveis de Ambiente (Opcional)

Se precisar configurar variáveis específicas:
- **SECRET_KEY**: Chave secreta para Flask
- **OPENAI_API_KEY**: Sua chave da API OpenAI (para parecer técnico)

#### 4. Deploy Automático

- O Render detectará mudanças no GitHub
- Deploy automático a cada push para `main`
- URL será: `https://sistema-tributario.onrender.com`

## 🛠️ Tecnologias

- **Backend**: Flask (Python 3.11+)
- **Frontend**: React 18 + Tailwind CSS
- **Database**: SQLite
- **Deploy**: Render.com
- **CI/CD**: GitHub + Render

## 📁 Estrutura do Projeto

```
sistema_tributario/
├── src/
│   ├── main.py              # Aplicação Flask principal
│   ├── models/              # Modelos do banco de dados
│   ├── routes/              # Rotas da API
│   └── static/              # Frontend buildado
├── data/                    # Arquivos de dados
├── requirements.txt         # Dependências Python
├── render.yaml             # Configuração Render.com
├── Procfile               # Configuração para deploy
└── runtime.txt            # Versão Python
```

## 🔧 Funcionalidades

- ✅ Cadastro de participantes
- ✅ Cálculo PIS/COFINS
- ✅ Processamento CBS
- ✅ Consultas de tabelas
- ✅ Geração de parecer técnico
- ✅ Interface dark theme

## 📱 Acesso

- **Local**: http://localhost:5000
- **Produção**: https://sistema-tributario.onrender.com

## 🔄 Atualizações

Para atualizar o sistema em produção:

```bash
git add .
git commit -m "Atualização do sistema"
git push origin main
```

O Render.com fará deploy automático em alguns minutos.

## 📞 Suporte

- **Documentação**: Este README
- **Issues**: GitHub Issues
- **Deploy**: Render.com Dashboard

---

**IPOG - Projeto do Caso Prático Final**  
*Sistema Público da Escrituração Digital e os Impactos da Reforma Tributária*
