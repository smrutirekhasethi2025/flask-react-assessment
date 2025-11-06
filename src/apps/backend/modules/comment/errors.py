from modules.application.errors import AppError

class CommentErrorCode:
    NOT_FOUND = "COMMENT_NOT_FOUND"

class CommentNotFoundError(AppError):
    def __init__(self, comment_id: str) -> None:
        super().__init__(code=CommentErrorCode.NOT_FOUND, http_status_code=404, message=f"Comment with id {comment_id} not found.")

class CommentBadRequestError(AppError):
    def __init__(self, message: str = "Bad Request"):
        super().__init__(code="COMMENT_BAD_REQUEST", http_status_code=400, message=message)
