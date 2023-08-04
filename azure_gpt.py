import os

from src.gpt_accessor import GptAccessor
from src.jira_accessor import JiraAccessor

if __name__ == '__main__':
    jira_accessor = JiraAccessor()
    gpt_accessor = GptAccessor()
    issues = jira_accessor.get_issues()
    for issue in issues:
        messages = [{
            'role': 'system', 'content': 'You are a Customer Support entity helping customers of <Company Name>, '
                                         'You need to use only your knowledge in <Company Name> '
                                         'to help clients resolve the issue. '
                                         'If you don\'t know the answer refer to <Company Name> R&D for assistance',
        }, {
            'role': 'user', 'name': os.environ['JIRA_USER_NAME'], 'content': f"What should we tell the client on the following issue: {issue.get_field('description')}"
        }]
        print('Support question:')
        print(issue.get_field('description'))
        print('-----------------------------------------------------------------')
        response = gpt_accessor.send_message(messages)
        gpt_accessor.print_conversation(response)
        print('-----------------------------------------------------------------')
