import schedule
import settings

from .poll_pull_requests import poll_pull_requests as poll_pull_requests
from .poll_read_issue_comments import poll_read_issue_comments
from .poll_issue_close_stale import poll_issue_close_stale


def schedule_jobs(api):
    schedule.every(settings.PULL_REQUEST_POLLING_INTERVAL_SECONDS).seconds.do(
            lambda: poll_pull_requests(api))
    schedule.every(settings.ISSUE_COMMENT_POLLING_INTERVAL_SECONDS).seconds.do(
            lambda: poll_read_issue_comments(api))
    schedule.every(settings.ISSUE_CLOSE_STALE_INTERVAL_SECONDS).seconds.do(
            lambda: poll_issue_close_stale(api))
