from modules.comment.internal.store.comment_repository import CommentRepository

class CommentReader:
    @staticmethod
    def get_comments_for_task(account_id: str, task_id: str):
        return CommentRepository.find_by_task(account_id=account_id, task_id=task_id)

    @staticmethod
    def get_comment_by_id(comment_id: str):
        return CommentRepository.find_by_id(comment_id)
