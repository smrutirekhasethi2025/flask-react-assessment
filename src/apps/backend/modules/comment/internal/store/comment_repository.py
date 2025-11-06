from pymongo.collection import Collection
from datetime import datetime
from bson import ObjectId
from pymongo.errors import OperationFailure

from modules.application.repository import ApplicationRepository
from modules.comment.internal.store.comment_model import CommentModel
from modules.logger.logger_manager import Logger

COMMENT_VALIDATION_SCHEMA = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["account_id", "task_id", "content", "created_at"],
        "properties": {
            "account_id": {"bsonType": "string"},
            "task_id": {"bsonType": "string"},
            "content": {"bsonType": "string"},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"},
        },
    }
}

class CommentRepository(ApplicationRepository):
    collection_name = CommentModel.get_collection_name()

    @classmethod
    def on_init_collection(cls, collection: Collection) -> bool:
        # create index on task_id + account_id
        collection.create_index([("task_id", 1), ("account_id", 1)], name="task_account_index")
        add_validation_command = {
            "collMod": cls.collection_name,
            "validator": COMMENT_VALIDATION_SCHEMA,
            "validationLevel": "strict",
        }
        try:
            collection.database.command(add_validation_command)
        except OperationFailure as e:
            if e.code == 26:
                collection.database.create_collection(cls.collection_name, validator=COMMENT_VALIDATION_SCHEMA)
            else:
                Logger.error(message=f"Unable to ensure collection validation for {cls.collection_name} - {e}")
        return True

    @classmethod
    def collection(cls) -> Collection:
        return ApplicationRepository.db()[cls.collection_name]

    @classmethod
    def insert_comment(cls, comment: CommentModel) -> CommentModel:
        doc = {
            "account_id": comment.account_id,
            "task_id": comment.task_id,
            "content": comment.content,
            "created_at": comment.created_at or datetime.utcnow(),
            "updated_at": comment.updated_at,
        }
        res = cls.collection().insert_one(doc)
        doc["_id"] = res.inserted_id
        return CommentModel.from_bson(doc)

    @classmethod
    def find_by_task(cls, account_id: str, task_id: str):
        cursor = cls.collection().find({"account_id": account_id, "task_id": task_id}).sort("created_at", -1)
        return [CommentModel.from_bson(doc) for doc in cursor]

    @classmethod
    def find_by_id(cls, comment_id: str):
        try:
            doc = cls.collection().find_one({"_id": ObjectId(comment_id)})
        except Exception:
            return None
        if not doc:
            return None
        return CommentModel.from_bson(doc)

    @classmethod
    def update_comment(cls, comment_id: str, content: str):
        try:
            res = cls.collection().find_one_and_update(
                {"_id": ObjectId(comment_id)},
                {"$set": {"content": content, "updated_at": datetime.utcnow()}},
                return_document=True,
            )
        except Exception:
            return None
        if not res:
            return None
        return CommentModel.from_bson(res)

    @classmethod
    def delete_comment(cls, comment_id: str):
        try:
            res = cls.collection().find_one_and_delete({"_id": ObjectId(comment_id)})
        except Exception:
            return None
        if not res:
            return None
        return CommentModel.from_bson(res)
