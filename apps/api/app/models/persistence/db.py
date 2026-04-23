from contextlib import contextmanager
import certifi
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import OperationFailure


class MongoDB:
    def __init__(
        self,
        mongo_uri: str,
        db_name: str,
        collection_name: str,
    ) -> None:
        self.client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
        self.database: Database = self.client[db_name]
        self.collection: Collection = self.database[collection_name]
        self._indexes_ready = False

    def ensure_indexes(self, indexes: list[dict]) -> None:
        if self._indexes_ready:
            return
        for spec in indexes:
            keys = spec.get("keys", [])
            options = spec.get("options", {})
            if not keys:
                continue
            index_name = options.get("name")
            try:
                self.collection.create_index(keys, **options)
            except OperationFailure as exc:
                # Handle stale index definitions with the same name but different keys.
                if exc.code == 86 and index_name:
                    existing = self.collection.index_information().get(index_name)
                    if existing:
                        existing_keys = list(existing.get("key", []))
                        requested_keys = list(keys)
                        if existing_keys != requested_keys:
                            self.collection.drop_index(index_name)
                            self.collection.create_index(keys, **options)
                            continue
                raise
        self._indexes_ready = True

    def ping(self) -> None:
        self.client.admin.command("ping")

    @contextmanager
    def session(self):
        session = None
        try:
            session = self.client.start_session()
            yield session
        except Exception:
            yield None
        finally:
            if session is not None:
                session.end_session()
