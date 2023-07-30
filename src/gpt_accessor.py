import os
from time import sleep

import openai
from openai import cli

openai.api_type = "azure"
openai.api_key = os.environ['AZURE_OPEN_AI_API_KEY']
openai.api_base = os.environ['AZURE_OPEN_AI_PROJECT_NAME'] # format "https://<project_name>.openai.azure.com/"
openai.api_version = "2023-03-15-preview"

chatgpt_model_name = os.environ['AZURE_OPEN_AI_MODEL_NAME']


class GptAccessor:

    def send_message(self, messages, max_response_tokens=500):
        response = openai.ChatCompletion.create(
            engine=chatgpt_model_name,
            messages=messages,
            temperature=0.5,
            max_tokens=max_response_tokens,
            top_p=0.9,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response['choices'][0]['message']['content']

    def print_conversation(self, message):
        print('Automated response:')
        print(message)

    def upload_training_data(self, training_dir):
        training_ids = []
        for index, training_file_path in enumerate(os.listdir(training_dir)):
            training_id = cli.FineTune._get_or_upload(os.path.join(training_dir, training_file_path), True)
            print(f'{training_file_path=}, {training_id=}')
            training_ids.append(training_id)
            if index == 100:
                break

        self.check_status(training_ids)

    def check_status(self, training_ids):
        for training_id in training_ids:
            failure_rate = 0
            while failure_rate < 5:
                try:
                    train_status = openai.File.retrieve(training_id)["status"]
                    print(f'Status {train_status=}')
                    if train_status not in ["succeeded", "failed"]:
                        sleep(1)
                    else:
                         break
                except Exception:
                    sleep(2)
                    failure_rate += 1