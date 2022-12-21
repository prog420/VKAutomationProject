import sqlalchemy
from sqlalchemy.orm import sessionmaker
from app.sql.models.user import User


class MySQLClient:
    def __init__(self, db_name, user="root", password="root", host="127.0.0.1", port=3306):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        # SQLAlchemy
        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}"
        self.engine = sqlalchemy.create_engine(url=url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def add_all(self, objects):
        self.session.add_all(objects)
        self.session.commit()

    def execute_query(self, query, fetch=False):
        response = self.connection.execute(query)
        if fetch:
            return response.fetchall()

    def add_user(self, name, surname, password, email, middle_name=None,
                 username=None, access=None, active=None):
        instance = self.session.query(User).filter_by(username=username).first()
        if instance:
            return instance
        else:
            new_user = User(name=name, surname=surname, middle_name=middle_name, username=username,
                            password=password, email=email, access=access, active=active)
            self.session.add(new_user)
            self.session.commit()
            return new_user

    def get_user(self, **kwargs):
        return self.session.query(User).filter_by(**kwargs).first()

    def delete_user(self, value, filter_by="username", table="test_users"):
        self.connect(db_created=True)
        self.execute_query(f'DELETE FROM {table} WHERE {filter_by}="{value}"')

    def truncate(self, table="test_users"):
        self.connect(db_created=True)
        self.execute_query(f'TRUNCATE TABLE {table}')
