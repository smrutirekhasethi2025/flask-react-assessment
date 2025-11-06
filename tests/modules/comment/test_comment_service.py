import unittest
from tests.modules.comment.base_test_comment import BaseTestComment
from modules.comment.comment_service import CommentService
from modules.comment.types import CreateCommentParams, UpdateCommentParams, DeleteCommentParams

class TestCommentService(BaseTestComment):
    def test_create_comment(self):
        params = CreateCommentParams(account_id=self.account.id, task_id=str(self.task.id), content="Hello")
        comment = CommentService.create_comment(params=params)
        self.assertIsNotNone(comment.id)
        self.assertEqual(comment.content, "Hello")

    def test_update_comment(self):
        create = CreateCommentParams(account_id=self.account.id, task_id=str(self.task.id), content="Initial")
        comment = CommentService.create_comment(params=create)
        update = UpdateCommentParams(account_id=self.account.id, comment_id=str(comment.id), content="Updated")
        updated = CommentService.update_comment(params=update)
        self.assertEqual(updated.content, "Updated")

    def test_delete_comment(self):
        create = CreateCommentParams(account_id=self.account.id, task_id=str(self.task.id), content="ToDelete")
        comment = CommentService.create_comment(params=create)
        delete = DeleteCommentParams(account_id=self.account.id, comment_id=str(comment.id))
        CommentService.delete_comment(params=delete)
        from modules.comment.internal.store.comment_repository import CommentRepository
        self.assertIsNone(CommentRepository.find_by_id(str(comment.id)))
