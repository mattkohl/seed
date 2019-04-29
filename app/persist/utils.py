from app import db


class PersistUtils:

    @staticmethod
    def get_or_create(session, model, **kwargs) -> db.Model:
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

