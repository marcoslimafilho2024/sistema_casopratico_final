# 🚀 Guia de Deploy - Sistema Tributário

## 📋 Checklist de Deploy

### ✅ Pré-requisitos Verificados
- [x] Projeto configurado com Git
- [x] Arquivos de configuração criados
- [x] Dependências atualizadas
- [x] Configuração para produção

### 🔧 Arquivos Criados/Modificados
- [x] `render.yaml` - Configuração do Render.com
- [x] `Procfile` - Configuração para deploy
- [x] `runtime.txt` - Versão Python
- [x] `requirements.txt` - Com gunicorn
- [x] `.gitignore` - Exclusões do Git
- [x] `src/config.py` - Configuração de ambiente
- [x] `src/main.py` - Atualizado para produção
- [x] `README.md` - Documentação completa

## 🚀 Passos para Deploy

### 1. Commit das Mudanças
```bash
cd "C:\Users\marko\OneDrive\Documentos\Caso Prático SPED\PROJETO_CASO_PRATICO\sistema_tributario_essencial\home\ubuntu\sistema_tributario"

# Verificar status
git status

# Adicionar todos os arquivos
git add .

# Commit das mudanças
git commit -m "Configuração para deploy no Render.com"

# Push para GitHub
git push origin main
```

### 2. Configuração no Render.com

1. **Acesse**: https://render.com
2. **Login** com suas credenciais
3. **Clique**: "New +" → "Web Service"
4. **Conecte**: Sua conta GitHub
5. **Selecione**: Repositório `sistema_tributario`

### 3. Configurações do Serviço

```
Name: sistema-tributario
Environment: Python 3
Region: Frankfurt (EU Central) [Recomendado]
Branch: main
Build Command: pip install -r requirements.txt
Start Command: gunicorn src.main:app --bind 0.0.0.0:$PORT
Plan: Free
```

### 4. Variáveis de Ambiente (Opcional)

```
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### 5. Deploy Automático

- ✅ Render detectará mudanças no GitHub
- ✅ Build automático em alguns minutos
- ✅ URL: `https://sistema-tributario.onrender.com`

## 🔍 Verificação do Deploy

### Status do Build
- Acompanhe o progresso no dashboard do Render
- Verifique logs de build e runtime
- Teste a URL gerada

### Testes Pós-Deploy
- [ ] Acesse a URL do sistema
- [ ] Teste funcionalidades principais
- [ ] Verifique responsividade
- [ ] Teste em diferentes navegadores

## 🛠️ Solução de Problemas

### Erro de Build
- Verifique versão Python (3.11+)
- Confirme dependências no `requirements.txt`
- Verifique logs de erro

### Erro de Runtime
- Confirme comando de start
- Verifique variáveis de ambiente
- Analise logs de aplicação

### Problemas de CORS
- CORS já configurado no código
- Verifique configurações do Render

## 📱 URLs de Acesso

- **Desenvolvimento**: http://localhost:5000
- **Produção**: https://sistema-tributario.onrender.com

## 🔄 Atualizações Futuras

```bash
# Para atualizar o sistema
git add .
git commit -m "Descrição da atualização"
git push origin main

# Deploy automático em ~5 minutos
```

## 📞 Suporte

- **Render.com**: Dashboard de serviços
- **GitHub**: Issues e documentação
- **Logs**: Dashboard do Render para debug

---

**Status**: ✅ Pronto para Deploy  
**Última Atualização**: Configuração completa para Render.com
