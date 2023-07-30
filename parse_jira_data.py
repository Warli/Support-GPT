from src.jira_ticket_parser import JiraTicketParser

if __name__ == '__main__':
    jira_ticket_parser = JiraTicketParser()
    jira_ticket_parser.parse('data/<your_data_file_here>')
