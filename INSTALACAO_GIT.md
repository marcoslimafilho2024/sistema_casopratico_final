# 🔧 Instalação do Git e Configuração do Repositório

## 📥 Instalação do Git no Windows

### Opção 1: Download Direto
1. Acesse: https://git-scm.com/download/win
2. Baixe a versão para Windows
3. Execute o instalador
4. **Importante**: Durante a instalação, selecione "Git from the command line and also from 3rd-party software"

### Opção 2: Via Chocolatey (se tiver)
```powershell
choco install git
```

### Opção 3: Via Winget
```powershell
winget install --id Git.Git -e --source winget
```

## ✅ Verificação da Instalação

Após instalar, abra um **novo** PowerShell e execute:
```powershell
git --version
```

Deve retornar algo como: `git version 2.40.0.windows.1`

## 🔧 Configuração Inicial do Git

```powershell
# Configurar seu nome
git config --global user.name "Seu Nome"

# Configurar seu email
git config --global user.email "seu.email@exemplo.com"

# Verificar configurações
git config --list
```

## 📁 Navegação para o Projeto

```powershell
# Navegar para o diretório do projeto
cd "C:\Users\marko\OneDrive\Documentos\Caso Prático SPED\PROJETO_CASO_PRATICO\sistema_tributario_essencial\home\ubuntu\sistema_tributario"

# Verificar se está no diretório correto
dir
```

## 🔍 Verificação do Status do Git

```powershell
# Verificar status do repositório
git status

# Verificar se há commits
git log --oneline
```

## 🚀 Primeiro Commit e Push

```powershell
# Adicionar todos os arquivos
git add .

# Fazer o primeiro commit
git commit -m "Configuração inicial para deploy no Render.com"

# Verificar se há um repositório remoto
git remote -v

# Se não houver, adicionar o repositório GitHub
git remote add origin https://github.com/SEU_USUARIO/sistema_tributario.git

# Fazer push para o GitHub
git push -u origin main
```

## 🔗 Conectar ao GitHub

1. **Crie um repositório** no GitHub:
   - Nome: `sistema_tributario`
   - Descrição: "Sistema de Cálculo Tributário - PIS/COFINS e CBS"
   - Público ou Privado (sua escolha)

2. **Copie a URL** do repositório

3. **Adicione como remote**:
```powershell
git remote add origin https://github.com/SEU_USUARIO/sistema_tributario.git
```

## 📋 Checklist de Verificação

- [ ] Git instalado e funcionando
- [ ] Configuração de usuário feita
- [ ] Diretório do projeto acessado
- [ ] Status do Git verificado
- [ ] Repositório GitHub criado
- [ ] Remote adicionado
- [ ] Primeiro commit feito
- [ ] Push para GitHub realizado

## 🆘 Solução de Problemas

### Git não reconhecido
- Reinicie o PowerShell após instalação
- Verifique se Git está no PATH do sistema

### Erro de autenticação
- Use GitHub CLI ou configure credenciais
- Ou use token de acesso pessoal

### Erro de push
- Verifique se o repositório existe
- Confirme se o remote está correto

---

**Próximo Passo**: Após configurar o Git, seguir o guia `DEPLOY.md`
