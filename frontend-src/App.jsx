import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('cadastro');
  const [participantes, setParticipantes] = useState([]);
  const [produtos, setProdutos] = useState([]);
  const [csts, setCsts] = useState([]);
  const [apuracao, setApuracao] = useState(null);
  const [loading, setLoading] = useState(false);

  // Estados para formulários
  const [novoParticipante, setNovoParticipante] = useState('');
  const [novoProduto, setNovoProduto] = useState({
    ncm: '',
    cst: '',
    valor_venda: '',
    tributado: true
  });

  // Carregar CSTs ao iniciar
  useEffect(() => {
    carregarCSTs();
  }, []);

  const carregarCSTs = async () => {
    try {
      const response = await fetch('/api/csts');
      if (response.ok) {
        const data = await response.json();
        setCsts(data);
      }
    } catch (error) {
      console.error('Erro ao carregar CSTs:', error);
    }
  };

  const adicionarParticipante = () => {
    if (novoParticipante.trim() && participantes.length < 10) {
      setParticipantes([...participantes, novoParticipante.trim()]);
      setNovoParticipante('');
    }
  };

  const adicionarProduto = async () => {
    if (novoProduto.ncm && novoProduto.cst && novoProduto.valor_venda) {
      try {
        const response = await fetch('/api/produtos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(novoProduto)
        });
        
        if (response.ok) {
          const produto = await response.json();
          setProdutos([...produtos, produto]);
          setNovoProduto({ ncm: '', cst: '', valor_venda: '', tributado: true });
        }
      } catch (error) {
        console.error('Erro ao adicionar produto:', error);
      }
    }
  };

  const calcularApuracao = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/calculos/pis-cofins', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (response.ok) {
        const resultado = await response.json();
        setApuracao(resultado);
      }
    } catch (error) {
      console.error('Erro ao calcular apuração:', error);
    } finally {
      setLoading(false);
    }
  };

  const baixarMemoriaCalculo = async (id) => {
    try {
      const response = await fetch(`/api/calculos/${id}/txt`);
      if (response.ok) {
        const data = await response.json();
        
        // Criar e baixar arquivo
        const blob = new Blob([data.content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename;
        a.click();
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Erro ao baixar arquivo:', error);
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="header">
        <h1>Sistema de Cálculo Tributário</h1>
        <p>Simulações com Comparação Entre SPED Contribuições e a Calculadora da Reforma</p>
        <p>Empresa do Lucro Real - PIS/COFINS vs CBS</p>
      </header>

      {/* Navigation */}
      <nav className="navigation">
        <button 
          className={activeTab === 'cadastro' ? 'active' : ''} 
          onClick={() => setActiveTab('cadastro')}
        >
          Cadastro
        </button>
        <button 
          className={activeTab === 'etapa1' ? 'active' : ''} 
          onClick={() => setActiveTab('etapa1')}
        >
          Etapa 1 - PIS/COFINS
        </button>
        <button 
          className={activeTab === 'etapa2' ? 'active' : ''} 
          onClick={() => setActiveTab('etapa2')}
        >
          Etapa 2 - CBS
        </button>
        <button 
          className={activeTab === 'consultas' ? 'active' : ''} 
          onClick={() => setActiveTab('consultas')}
        >
          Consultas
        </button>
        <button 
          className={activeTab === 'parecer' ? 'active' : ''} 
          onClick={() => setActiveTab('parecer')}
        >
          Parecer
        </button>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {activeTab === 'cadastro' && (
          <div className="card">
            <h2>👥 Cadastro dos Participantes da Equipe</h2>
            <p>Inserir o nome completo dos participantes (até 10 participantes). Precisamos armazenar até concluir o CASO PRÁTICO.</p>
            
            <div className="form-group">
              <label>Nome Completo:</label>
              <div className="input-group">
                <input
                  type="text"
                  value={novoParticipante}
                  onChange={(e) => setNovoParticipante(e.target.value)}
                  placeholder="Digite o nome completo do participante"
                  maxLength={100}
                />
                <button onClick={adicionarParticipante} disabled={participantes.length >= 10}>
                  ➕ Adicionar
                </button>
              </div>
            </div>

            {participantes.length > 0 && (
              <div className="participantes-list">
                <h3>Participantes ({participantes.length}/10):</h3>
                <ul>
                  {participantes.map((nome, index) => (
                    <li key={index}>{nome}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {activeTab === 'etapa1' && (
          <div className="card">
            <h2>📊 Etapa 1 - PIS e COFINS</h2>
            <p>Simulação do Cálculo do PIS e COFINS</p>
            
            {/* Sub-navigation */}
            <div className="sub-nav">
              <button className="sub-active">Vendas</button>
              <button>Aquisições</button>
              <button>Apuração</button>
            </div>

            {/* Formulário de Produto */}
            <div className="form-section">
              <h3>Adicionar Produto</h3>
              
              <div className="form-grid">
                <div className="form-group">
                  <label>NCM (8 dígitos):</label>
                  <input
                    type="text"
                    value={novoProduto.ncm}
                    onChange={(e) => setNovoProduto({...novoProduto, ncm: e.target.value})}
                    placeholder="12345678"
                    maxLength={8}
                  />
                </div>

                <div className="form-group">
                  <label>CST:</label>
                  <select
                    value={novoProduto.cst}
                    onChange={(e) => setNovoProduto({...novoProduto, cst: e.target.value})}
                  >
                    <option value="">Selecione CST</option>
                    {csts.map((cst) => (
                      <option key={cst.codigo} value={cst.codigo}>
                        {cst.codigo} - {cst.descricao}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Valor da Venda:</label>
                  <input
                    type="number"
                    step="0.01"
                    value={novoProduto.valor_venda}
                    onChange={(e) => setNovoProduto({...novoProduto, valor_venda: e.target.value})}
                    placeholder="0,00"
                  />
                </div>

                <div className="form-group checkbox-group">
                  <label>
                    <input
                      type="checkbox"
                      checked={novoProduto.tributado}
                      onChange={(e) => setNovoProduto({...novoProduto, tributado: e.target.checked})}
                    />
                    Tributado (PIS/COFINS)
                  </label>
                </div>
              </div>

              <button className="btn-primary" onClick={adicionarProduto}>
                ➕ Adicionar Produto na Lista
              </button>
            </div>

            {/* Lista de Produtos */}
            {produtos.length > 0 && (
              <div className="produtos-list">
                <h3>Produtos Cadastrados ({produtos.length}):</h3>
                <div className="table-container">
                  <table>
                    <thead>
                      <tr>
                        <th>NCM</th>
                        <th>CST</th>
                        <th>Valor</th>
                        <th>Tributado</th>
                        <th>PIS Débito</th>
                        <th>COFINS Débito</th>
                      </tr>
                    </thead>
                    <tbody>
                      {produtos.map((produto) => (
                        <tr key={produto.id}>
                          <td>{produto.ncm}</td>
                          <td>{produto.cst}</td>
                          <td>R$ {produto.valor_venda}</td>
                          <td>{produto.tributado ? 'Sim' : 'Não'}</td>
                          <td>R$ {produto.pis_debito}</td>
                          <td>R$ {produto.cofins_debito}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Botão de Apuração */}
            <div className="apuração-section">
              <button 
                className="btn-success" 
                onClick={calcularApuracao}
                disabled={loading || produtos.length === 0}
              >
                {loading ? '🔄 Calculando...' : '📊 Calcular Apuração'}
              </button>
            </div>

            {/* Resultados da Apuração */}
            {apuracao && (
              <div className="resultado-apuracao">
                <h3>Resultado da Apuração</h3>
                
                <div className="resultado-grid">
                  <div className="resultado-item">
                    <span className="label">PIS Débito:</span>
                    <span className="value">R$ {apuracao.total_pis_debito}</span>
                  </div>
                  <div className="resultado-item">
                    <span className="label">PIS Crédito:</span>
                    <span className="value">R$ {apuracao.total_pis_credito}</span>
                  </div>
                  <div className="resultado-item">
                    <span className="label">COFINS Débito:</span>
                    <span className="value">R$ {apuracao.total_cofins_debito}</span>
                  </div>
                  <div className="resultado-item">
                    <span className="label">COFINS Crédito:</span>
                    <span className="value">R$ {apuracao.total_cofins_credito}</span>
                  </div>
                </div>

                <div className="resultado-total">
                  <div className="resultado-item">
                    <span className="label">PIS a Recolher:</span>
                    <span className="value success">R$ {apuracao.resultado_pis}</span>
                  </div>
                  <div className="resultado-item">
                    <span className="label">COFINS a Recolher:</span>
                    <span className="value success">R$ {apuracao.resultado_cofins}</span>
                  </div>
                  <div className="resultado-item">
                    <span className="label">Total a Recolher:</span>
                    <span className="value success total">R$ {apuracao.resultado_total}</span>
                  </div>
                </div>

                <button 
                  className="btn-download"
                  onClick={() => baixarMemoriaCalculo(apuracao.id)}
                >
                  📄 Baixar Memória de Cálculo (TXT)
                </button>
              </div>
            )}

            {/* Botão Avançar */}
            <div className="btn-avancar">
              <button className="btn-purple">
                Avançar para Etapa 2 - CBS
              </button>
            </div>
          </div>
        )}

        {activeTab === 'etapa2' && (
          <div className="card">
            <h2>🔄 Etapa 2 - CBS</h2>
            <p>Processamento da Contribuição sobre Bens e Serviços</p>
            <p>Funcionalidade em desenvolvimento...</p>
          </div>
        )}

        {activeTab === 'consultas' && (
          <div className="card">
            <h2>🔍 Consultas</h2>
            <p>Sistema de consultas em desenvolvimento...</p>
          </div>
        )}

        {activeTab === 'parecer' && (
          <div className="card">
            <h2>📝 Parecer Técnico</h2>
            <p>Geração de parecer técnico em desenvolvimento...</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p>Sistema Público da Escrituração Digital e os Impactos da Reforma Tributária</p>
        <p>IPOG - Projeto do Caso Prático Final</p>
      </footer>
    </div>
  );
}

export default App;
