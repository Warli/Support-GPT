import os

from src.gpt_accessor import GptAccessor
from src.jira_accessor import JiraAccessor

if __name__ == '__main__':
    jira_accessor = JiraAccessor()
    gpt_accessor = GptAccessor()
    issues = jira_accessor.get_issues()
    for issue in issues:
        messages = [{
            'role': 'user', 'name': os.environ['JIRA_USER_NAME'], 'content': issue.get_field('description')
        }]
        print('Support question:')
        print(issue.get_field('description'))
        print('-----------------------------------------------------------------')
        response = gpt_accessor.send_message(messages)
        gpt_accessor.print_conversation(response)
        print('-----------------------------------------------------------------')
