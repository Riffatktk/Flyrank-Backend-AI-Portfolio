from abc import ABC, abstractmethod
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor


class ItemRepository(ABC):
    @abstractmethod
    def create(self, name: str, description: str):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, item_id: int):
        pass


class InMemoryRepository(ItemRepository):
    def __init__(self):
        self.items = []
        self.next_id = 1

    def create(self, name: str, description: str):
        item = {
            "id": self.next_id,
            "name": name,
            "description": description,
        }
        self.items.append(item)
        self.next_id += 1
        return item

    def get_all(self):
        return self.items

    def get_by_id(self, item_id: int):
        for item in self.items:
            if item["id"] == item_id:
                return item
        return None


class PostgresRepository(ItemRepository):
    def __init__(self, database_url: str):
        self.conn = psycopg2.connect(
            database_url,
            cursor_factory=RealDictCursor
        )

    def create(self, name: str, description: str):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO items (name, description)
                VALUES (%s, %s)
                RETURNING id, name, description;
                """,
                (name, description),
            )
            item = cur.fetchone()
            self.conn.commit()
            return dict(item)

    def get_all(self):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, description
                FROM items
                ORDER BY id;
                """
            )
            items = cur.fetchall()
            return [dict(item) for item in items]

    def get_by_id(self, item_id: int):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, description
                FROM items
                WHERE id = %s;
                """,
                (item_id,),
            )
            item = cur.fetchone()
            if item:
                return dict(item)
            return None