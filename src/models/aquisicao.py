from src.models.user import db
from datetime import datetime

class Aquisicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_despesa = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Numeric(15, 2), nullable=False)
    pis_credito = db.Column(db.Numeric(15, 2), default=0)
    cofins_credito = db.Column(db.Numeric(15, 2), default=0)
    cbs_credito = db.Column(db.Numeric(15, 2), default=0)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Aquisicao {self.nome_despesa}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome_despesa': self.nome_despesa,
            'valor': float(self.valor),
            'pis_credito': float(self.pis_credito),
            'cofins_credito': float(self.cofins_credito),
            'cbs_credito': float(self.cbs_credito),
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        }

