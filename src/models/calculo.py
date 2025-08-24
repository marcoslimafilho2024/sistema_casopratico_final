from src.models.user import db
from datetime import datetime

class Calculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'PIS_COFINS' ou 'CBS'
    total_debito = db.Column(db.Numeric(15, 2), default=0)
    total_credito = db.Column(db.Numeric(15, 2), default=0)
    resultado = db.Column(db.Numeric(15, 2), default=0)
    arquivo_txt = db.Column(db.Text)
    data_calculo = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Calculo {self.tipo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'total_debito': float(self.total_debito),
            'total_credito': float(self.total_credito),
            'resultado': float(self.resultado),
            'arquivo_txt': self.arquivo_txt,
            'data_calculo': self.data_calculo.isoformat() if self.data_calculo else None
        }

class XmlCbs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ncm = db.Column(db.String(8), nullable=False)
    xml_content = db.Column(db.Text, nullable=False)
    base_calculo = db.Column(db.Numeric(15, 2), default=0)
    valor_cbs = db.Column(db.Numeric(15, 2), default=0)
    processado = db.Column(db.Boolean, default=False)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<XmlCbs NCM:{self.ncm}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ncm': self.ncm,
            'xml_content': self.xml_content,
            'base_calculo': float(self.base_calculo),
            'valor_cbs': float(self.valor_cbs),
            'processado': self.processado,
            'data_upload': self.data_upload.isoformat() if self.data_upload else None
        }

