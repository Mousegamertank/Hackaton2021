from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Date, Float
from sqlalchemy.orm import scoped_session, sessionmaker,  relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
# from app import lm

engine = create_engine('sqlite:///atividades.db', convert_unicode=True, echo=True)

db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

#####################################################
class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key = True)
    chapaNumber = Column(Integer, nullable = True)
    name = Column(String(length = 50))
    email = Column(String(80), unique=True)
    password = Column(String(80))
    active = Column(Boolean(), default=False)
    admin_password = relationship('Password_Forgot', backref='passwordAdmin', lazy=True)

    def __repr__(self):
        return f'Numero de Chapa: {self.chapaNumber}, \nEmail: {self.email}, \nPassword: {self.password}'

    def active(self):
        self.active = True
        db_session.add(self)
        db_session.commit()

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        self.active = False
        db_session.add(self)
        db_session.commit()

#####################################################
class Citizen(Base):
    __tablename__ = 'citizen'
    id = Column(Integer, primary_key = True)
    email = Column(String(80), unique=True)
    password = Column(String(length = 80))
    fullname = Column(String(length = 80))
    cpf = Column(String(length = 11), unique=True)
    whatsapp = Column(String(length = 11), unique=True)
    active = Column(Boolean(), default=False)
    passwordforgot = relationship('Password_Forgot', backref="citizenPassword", lazy=True)
    citizenOccurrence = relationship('Occurrence', backref="citizen_ocurrence", lazy=True)

    # @property
    # def is_authenticated(self):
    #     return True

    # @property
    # def is_active(self):
    #     return False
    
    # @property
    # def is_anonymous(self):
    #     return True
    
    # def get_id(self):
    #     return str(self.id)


    def __repr__(self):
        return f'Nome Completo: {self.fullname}, \nEmail: {self.email}, \nPassword: {self.password}, \nCPF: {self.cpf}, \nWhatsapp: {self.whatsapp}'

    def active(self):
        self.active = True
        db_session.add(self)
        db_session.commit()

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        self.active = False
        db_session.add(self)
        db_session.commit()

##################################################### 
class Password_Forgot(Base):
    __tablename__ = 'password_forgot'
    id = Column(Integer, primary_key = True)
    citizen_id = Column(Integer(), ForeignKey('citizen.id'), nullable=True)
    admin_id = Column(Integer(), ForeignKey('admin.id'), nullable=True)
    token = Column(String(length = 80))
    active = Column(Boolean(), default=True)
    
    def __repr__(self):
        return f'token: {self.token}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

#####################################################
class Occurrence(Base):
    __tablename__ = 'occurrence'
    id = Column(Integer(), primary_key = True)
    date = Column(String(length = 10))
    hour = Column(String(length = 5))
    viewed = Column(Boolean(), default = False)
    auto_number = Column(Integer(), nullable = True)
    obs = Column(String(length = 250), nullable = True)
    proper = Column(String(length = 80), nullable = True)
    cellphone = Column(String(length = 11))
    active = Column(Boolean(), default=True)
    number = Column(String(length = 4), nullable=False)
    street = Column(String(length = 80), nullable=False)
    latitude = Column(Float(), nullable=True)
    longitude = Column(Float(), nullable=True)
    occurrenceNumber = Column(String(length = 9), nullable = True)

    problem = Column(Integer(), ForeignKey('problem_types.id'), nullable=True)
    status_ocorrence = Column(Integer(), ForeignKey('status.id'), nullable=False)
    citizenOcurrence = Column(Integer(), ForeignKey('citizen.id'), nullable=False)
    
    occurrence_photos = relationship('Photos', backref='photos', lazy=True)

    def __repr__(self):
        return f'date: {self.date}, viewed: {self.viewed}, auto_number: {self.auto_number}, cellphone: {self.cellphone}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

#####################################################
class ProblemTypes(Base):
    __tablename__ = 'problem_types'
    id = Column(Integer, primary_key=True)
    description = Column(String(length = 45))
    problemtype = relationship('Occurrence', backref='problem_occurrence', lazy=True)

    def __repr__(self):
        return f'description: {self.description}, occurrenceType: {self.occurrenceType}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

##################################################### 
class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key = True)
    description = Column(String(length = 60), nullable = False)
    occurrence_status = relationship('Occurrence', backref='statusOcorrence', lazy=True)

    def __repr__(self):
        return f'description: {self.description}, occurrence_status: {self.occurrence_status}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

##################################################### 
class Photos(Base):
    __tablename__ = 'occurrence_photo'
    id = Column(Integer(), primary_key = True)
    name = Column(String(length = 125))
    occurrence_id = Column(Integer(), ForeignKey('occurrence.id'), nullable=False)

    def __repr__(self):
        return f'name: {self.name}, occurrencce: {self.occurrence_id.auto_number}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

##################################################### 


def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()    

#conectar com postgres
# engine = create_engine(
#     "postgresql+pg8000://scott:tiger@localhost/test",
#     execution_options={
#         "isolation_level": "REPEATABLE READ"
#     }
# )
# 
# SEGUE O MODELO DE OCMO TEM QUE SER COMPLETADO AS INFORMAÇÕES
# engine = create_engine("postgresql://(Usuarioaseusar):(senha)@localhost/(nome do banco)")
