from random import randint 

def random_integer():
    min_ = 100
    max_ = 1000000000
    rand = randint(min_, max_)

    # possibility of same random number is very low.
    # but if you want to make sure, here you can check id exists in database.
    from sqlalchemy.orm import sessionmaker
    db_session_maker = sessionmaker(bind=sqlite:///ppdb.sqlite)
    db_session = db_session_maker()
    while db_session.query(Table).filter(uuid == rand).limit(1).first() is not None:
        rand = randint(min_, max_)

    return rand

random_integer()
