from rococo.repositories.postgresql import PostgreSQLRepository
from rococo.data.postgresql import PostgreSQLAdapter
from rococo.messaging.base import MessageAdapter
from typing import Optional


class BaseRepository(PostgreSQLRepository):
    MODEL = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.MODEL is None:
            raise TypeError(f"Subclasses of {cls.__name__} must define the MODEL attribute.")

    def __init__(
            self, db_adapter: PostgreSQLAdapter, message_adapter: Optional[MessageAdapter], 
            queue_name: str, user_id: str = None
    ):
        # Pass MODEL as the model to the BaseRepository
        super().__init__(db_adapter, self.MODEL, message_adapter, queue_name, user_id=user_id)


    def update(self, filters: dict, updates: dict):
        """
        Fetch a single object using filters, apply updates, and save.
        """
        obj = self.get_one(filters)
        if not obj:
            raise ValueError(f"{self.MODEL.__name__} not found with filters: {filters}")

        for key, value in updates.items():
            if hasattr(obj, key):
                setattr(obj, key, value)

        return self.save(obj)
    
    