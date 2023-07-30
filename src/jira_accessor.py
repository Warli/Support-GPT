import os

from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue

JIRA_TOKEN = os.environ['JIRA_TOKEN']
JIRA_SERVER = os.environ['JIRA_SERVER']
JIRA_USER_EMAIL = os.environ['JIRA_USER_EMAIL']


class JiraAccessor:
    def __init__(self):
        self.__client = None

    @property
    def _client(self):
        if self.__client is None:
            self.__client = JIRA(
                server=JIRA_SERVER,
                basic_auth=(JIRA_USER_EMAIL, JIRA_TOKEN)
            )
        return self.__client

    def get_issues(self) -> ResultList[Issue]:
        jql_query = f'' # JQL query to select incoming new support tickets
        issues = self._client.search_issues(jql_query)
        return issues
