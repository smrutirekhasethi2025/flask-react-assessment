from flask import jsonify, request
from flask.views import MethodView
from modules.comment.comment_service import CommentService
from modules.comment.types import CreateCommentParams, UpdateCommentParams, DeleteCommentParams
from modules.comment.errors import CommentBadRequestError
from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware

class CommentView(MethodView):
    @access_auth_middleware
    def post(self, account_id: str, task_id: str):
        data = request.get_json()
        if data is None or not data.get("content"):
            raise CommentBadRequestError("content is required")
        params = CreateCommentParams(account_id=account_id, task_id=task_id, content=data["content"])
        comment = CommentService.create_comment(params=params)
        return jsonify({"data": comment.__dict__}), 201

    @access_auth_middleware
    def get(self, account_id: str, task_id: str):
        comments = CommentService.get_comments_for_task(account_id=account_id, task_id=task_id)
        return jsonify({"data": [c.__dict__ for c in comments]}), 200

class CommentByIdView(MethodView):
    @access_auth_middleware
    def patch(self, comment_id: str):
        data = request.get_json()
        if data is None or not data.get("content"):
            raise CommentBadRequestError("content is required")
        params = UpdateCommentParams(account_id="", comment_id=comment_id, content=data["content"])
        comment = CommentService.update_comment(params=params)
        return jsonify({"data": comment.__dict__}), 200

    @access_auth_middleware
    def delete(self, comment_id: str):
        params = DeleteCommentParams(account_id="", comment_id=comment_id)
        CommentService.delete_comment(params=params)
        return jsonify({}), 204
