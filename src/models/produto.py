from src.models.user import db
from datetime import datetime

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ncm = db.Column(db.String(8), nullable=False)
    cst_pis = db.Column(db.String(2), nullable=False)
    cst_cofins = db.Column(db.String(2), nullable=False)
    valor_venda = db.Column(db.Numeric(15, 2), nullable=False)
    pis_debito = db.Column(db.Numeric(15, 2), default=0)
    cofins_debito = db.Column(db.Numeric(15, 2), default=0)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Produto NCM:{self.ncm}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ncm': self.ncm,
            'cst_pis': self.cst_pis,
            'cst_cofins': self.cst_cofins,
            'valor_venda': float(self.valor_venda),
            'pis_debito': float(self.pis_debito),
            'cofins_debito': float(self.cofins_debito),
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        }

