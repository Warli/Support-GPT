import json
import math
import os.path
import re
import shutil
from copy import deepcopy
from datetime import datetime

import pandas


class JiraTicketParser:
    __RESULT_DIR = 'data_set'
    __RESULT_FILE_PATTERN = 'data_set/analyzed_jira_tickets_{date_time}.jsonl'
    __PARSED_LINE_FORMAT = {
        'prompt': '',
        'completion': ''
    }

    def __init__(self):
        if os.path.exists(self.__RESULT_DIR):
            shutil.rmtree(self.__RESULT_DIR)
        os.mkdir(self.__RESULT_DIR)

    def parse(self, jira_report_file_path):
        jira_report_df = pandas.read_csv(jira_report_file_path)
        max_comment_index = int(re.search(r'\d+', jira_report_df.columns[-2]).group(0))
        file_name = self.__RESULT_FILE_PATTERN.format(date_time=datetime.today().date())
        comments = []
        for index, jira_ticket in jira_report_df.iterrows():
            jira_ticket_description = jira_ticket['Description']
            if isinstance(jira_ticket_description, float) and math.isnan(jira_ticket_description):
                continue
            prompt, completion_comment = self._parse_comment(jira_ticket, jira_ticket_description, max_comment_index)
            comments.append(self._create_prompt(prompt, completion_comment))
        self._write_to_dataset(file_name, comments)

    def _parse_comment(self, jira_ticket, jira_ticket_description, max_comment_index):
        completion_comment = None
        jira_ticket_description = self._clean_text(jira_ticket_description)
        prompt = jira_ticket_description
        for comment_index in reversed(range(max_comment_index + 1)):
            column_name = 'Comment'
            if comment_index > 0:
                column_name += f'.{comment_index}'
            comment = jira_ticket[column_name]

            if isinstance(comment, float) and math.isnan(comment):
                continue
            comment = self._clean_text(comment)
            if completion_comment is None:
                completion_comment = comment + ' END' # Mark end of discussion for GPT
            else:
                prompt += '\n\n###\n\n' + comment # Chain any comment in a way GPT will understand this is a continuous comment
        return prompt, completion_comment

    def _clean_text(self, text):
        text = re.sub(r'\[\~accountid:[^\]]+\]', '', text)
        text = re.sub(r'\b[0-9a-fA-F]{24}\b;', '', text)# Cleaning JIRA entities from the text
        text = text.replace('\n', ' ')
        text = text.replace('\r', '')
        text = text.replace('  ', ' ')
        # add here any other cleaning you might need
        return text

    def _create_prompt(self, prompt, completion):
        parsed_line = deepcopy(self.__PARSED_LINE_FORMAT)
        parsed_line['prompt'] = prompt
        parsed_line['completion'] = completion
        return parsed_line

    def _write_to_dataset(self, file_name, comments):
        with open(file_name, 'a+') as result_file:
            for comment in comments:
                result_file.write(json.dumps(comment) + '\n')
