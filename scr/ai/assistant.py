"""Обработчик запросов"""
from typing import Literal

import openai
from openai import OpenAI

from scr.config import LOGER
from scr.settings import OPENAI_TOKEN, OPENAI_MODEL

SQL_PROMPT = """
у меня есть таблица в sqlite: 
1. Freelancer_ID - Unique identifier for each freelancer in the dataset 
2. Job_Category - Primary classification of freelance work (Web Development, Data Entry, etc.) 
3. Platform - Freelance marketplace where work was performed (Fiverr, Upwork, etc.) 
4. Experience_Level - Freelancer's experience tier (Beginner, Intermediate, Expert) 
5. Client_Region - Geographical location of the client (Asia, Europe, USA, etc.) 
6. Payment_Method - Method used for financial transactions (Bank Transfer, PayPal, etc.) 
7. Job_Completed - Number of projects successfully completed by the freelancer 
8. Earnings_USD - Total earnings in US Dollars 
9. Hourly_Rate - Freelancer's hourly compensation rate in USD 
10. Job_Success_Rate - Percentage of successful job completions (50-100%) 
дай ответ в формате {"sql-query": "тут запрос", "description": "тут описание ответа"}
не надо никаких доплнительных пояснений и описаний, только строгий ответ.
Если запрос подразумевает обновление или удаление данных из таблицы замени его на
'select count(*) from freelancers' а в описании укажи, что запрос неккоректен.
"""

HUMAN_PROMPT = """
сделай этот ответ удобочитаемым, 
оставь только ответ на запрос, 
если надо произведи математические операции, что бы лучше ответить на поставленный вопрос. 
Ответ на запрос, должен максимально отвечать ему, не забудь про детали.
"""

class AssistantOpenAI:
    """обьект для взаимодействия с OpenAI"""
    #pylint: disable = too-few-public-methods
    def __init__(self):
        self._client = OpenAI(api_key=OPENAI_TOKEN)
        self._sql_prompt = SQL_PROMPT
        self._human_prompt = HUMAN_PROMPT
        self._model = OPENAI_MODEL

    @LOGER.catch
    def do_response(self, message: str, prompt: Literal['sql', 'human']) -> str | None:
        """ответ на сообщение пользователя из openai"""
        try:
            res = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "developer",
                        "content":
                            self._sql_prompt if prompt == 'sql' else self._human_prompt
                    },
                    {"role": "user", "content": message}
                ]
            )
            return res.choices[0].message.content
        except openai.PermissionDeniedError:
            LOGER.warning("Проверьте свой токен доступа к OpenAI или VPN")
            return None
