from app.extensions import db


class Constructor(db.Model):
    __tablename__ = 'constructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Constructor {self.name}>'
