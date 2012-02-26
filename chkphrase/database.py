from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import chkphrase.conf as conf

engineString = 'mysql://%s:%s@%s/%s' % (conf.db_user, conf.db_password,
                                        conf.db_host, conf.db_database)
engine = create_engine(engineString,
                       convert_unicode=True,
                       pool_recycle=3600)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import chkphrase.models
    Base.metadata.create_all(bind=engine)
