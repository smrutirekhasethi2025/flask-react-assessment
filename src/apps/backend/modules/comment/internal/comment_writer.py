from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.internal.store.comment_model import CommentModel

class CommentWriter:
    @staticmethod
    def create(account_id: str, task_id: str, content: str):
        model = CommentModel(account_id=account_id, task_id=task_id, content=content)
        return CommentRepository.insert_comment(model)

    @staticmethod
    def update(comment_id: str, content: str):
        return CommentRepository.update_comment(comment_id, content)

    @staticmethod
    def delete(comment_id: str):
        return CommentRepository.delete_comment(comment_id)
