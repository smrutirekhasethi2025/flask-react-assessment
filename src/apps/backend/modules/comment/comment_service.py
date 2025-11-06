from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import CreateCommentParams, UpdateCommentParams, DeleteCommentParams
from modules.comment.errors import CommentNotFoundError

class CommentService:
    @staticmethod
    def create_comment(params: CreateCommentParams):
        from modules.comment.internal.store.comment_model import CommentModel
        model = CommentModel(account_id=params.account_id, task_id=params.task_id, content=params.content)
        inserted = CommentRepository.insert_comment(model)
        return inserted

    @staticmethod
    def get_comments_for_task(account_id: str, task_id: str):
        return CommentRepository.find_by_task(account_id=account_id, task_id=task_id)

    @staticmethod
    def update_comment(params: UpdateCommentParams):
        updated = CommentRepository.update_comment(params.comment_id, params.content)
        if not updated:
            raise CommentNotFoundError(params.comment_id)
        return updated

    @staticmethod
    def delete_comment(params: DeleteCommentParams):
        deleted = CommentRepository.delete_comment(params.comment_id)
        if not deleted:
            raise CommentNotFoundError(params.comment_id)
        return deleted
