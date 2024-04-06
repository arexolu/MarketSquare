from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, SchemaOpts, pre_load, post_dump
from sqlalchemy import Integer, DateTime, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


class __Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=__Base, engine_options={ 'pool_pre_ping': True})


class _NamespaceOpts(SchemaOpts):
    """
    Same as the default class Meta options, but adds 'name' and
    'plural_name' options for enveloping.
    """

    def __init__(self, meta, **kwargs):
        SchemaOpts.__init__(self, meta, **kwargs)
        self.name = getattr(meta, "name", None)
        self.plural_name = getattr(meta, "plural_name", self.name)


class BaseSchema(Schema):
    OPTIONS_CLASS = _NamespaceOpts

    class Meta:
        ordered = True

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many, **kwargs):
        key = self.opts.plural_name if many else self.opts.name
        return data[key]

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        key = self.opts.plural_name if many else self.opts.name
        return {key: data}


class BaseModel:
    __schema__ = BaseSchema
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.current_timestamp(), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        index=True,
    )

    def __init__(self, *args, **kwargs):
        cols = [c.name for c in self.__table__.columns]
        for k, v in kwargs.items():
            if k in cols:
                setattr(self, k, v)

    def __repr__(self):
        return (
            "<%r with id %r created at %r>" % self.__class__.__name__,
            self.id,
            self.created_at,
        )
    
    def to_json(self, **kwargs):
        """Serializes an instance of model to a JSON object

        Returns:
            json: JSON object representation of the instance
        """
        return self.__schema__(**kwargs).dump(self)

    def to_dict(self):
        """Serializes an instance of model to python dictionary

        Returns:
            dict: Python dict representation of the instance
        """
        return { c.name: getattr(self, c.name) for c in self.__table__.columns }


    @classmethod
    def create(cls, *args, **kwargs):
        try:
            resource = cls(*args, **kwargs)
            db.session.add(resource)
            db.session.commit()
            return resource
        except IntegrityError as e:
            db.session.rollback()
            db.session.close()
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            raise e
        except Exception as e:
            db.session.rollback()
            db.session.close()
            raise e

    def add(self, resource):
        try:
            db.session.add(resource)
            db.session.commit()
            return resource
        except IntegrityError as e:
            db.session.rollback()
            db.session.close()
            raise e
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            raise e
        except Exception as e:
            db.session.rollback()
            db.session.close()
            raise e

    def update(self, resource: dict):
        [
            setattr(self, attr, resource[attr])
            for attr in resource.keys()
            if attr in self.__dict__.keys()
        ]
        db.session.commit()
        return self

    def save(self):
        db.session.commit()
        return self

    def destroy(self):
        db.session.delete(self)
        db.session.commit()
        return self

