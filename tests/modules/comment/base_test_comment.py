import unittest
from modules.logger.logger_manager import LoggerManager
from modules.task.task_service import TaskService
from modules.task.types import CreateTaskParams
from modules.account.account_service import AccountService
from modules.comment.rest_api.comment_rest_api_server import CommentRestApiServer
from modules.task.rest_api.task_rest_api_server import TaskRestApiServer

class BaseTestComment(unittest.TestCase):
    DEFAULT_TASK_TITLE = "Test Task"
    DEFAULT_TASK_DESCRIPTION = "Task description"

    def setUp(self) -> None:
        LoggerManager.mount_logger()
        # ensure routers registered similarly to other tests
        TaskRestApiServer.create()
        CommentRestApiServer.create()
        # create test account
        self.account = AccountService.create_account_by_username_and_password(
            username="testuser@example.com", password="testpassword"
        )
        # create a task
        task_params = CreateTaskParams(account_id=self.account.id, title=self.DEFAULT_TASK_TITLE, description=self.DEFAULT_TASK_DESCRIPTION)
        self.task = TaskService.create_task(params=task_params)

    def tearDown(self) -> None:
        from modules.task.internal.store.task_repository import TaskRepository
        from modules.comment.internal.store.comment_repository import CommentRepository
        TaskRepository.collection().delete_many({})
        CommentRepository.collection().delete_many({})
