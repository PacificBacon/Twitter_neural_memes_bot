from transformers import BertTokenizer, BertModel

from word2vec_utils import *
from tg_utils import *

class MemeBot:
  def __init__(self, tg_token):
    self.tg_token = tg_token
    self.offset = 0

    self.tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased-sentence')
    self.embed = (BertModel.from_pretrained('DeepPavlov/rubert-base-cased-sentence')).embeddings.word_embeddings
  
  def do_action_on_message(self, chat_id, message):
    BOUND = 0.725
    examples_one = [
      'покажи одну новость',
      'хочу последнее объявление',
      'хочу новость'
    ]
    examples_several = [
      'покажи все новости',
      'выведи последние объявления',
      'хочу увидеть новости',
      'хочу новости'
    ]

    print("Input message:", message)

    scores_one = []
    for example in examples_one:
      scores_one.append(get_similarity(self.tokenizer, self.embed, example, message))
    score_one = sum(scores_one) / len(scores_one)
    print("Score to one:", score_one)

    scores_several = []
    for example in examples_several:
      scores_several.append(get_similarity(self.tokenizer, self.embed, example, message))
    score_several = sum(scores_several) / len(scores_several)
    print("Score to several:", score_several)

    score_mean = (score_one + score_several) / 2.0
    print("Mean score:", score_mean)
    if (score_mean < BOUND):
      print("Incorrect message")
      tg_sendMessage(self.tg_token, chat_id, "Не понятен запрос.")
    else:
      has_num = 0
      if ('1' in message) or ('одн' in message):
        has_num = 1  
      if ('2' in message) or ('две' in message) or ('два' in message):
        has_num = 2
      if ('3' in message) or ('три' in message):
        has_num = 3 
      if ('4' in message) or ('четыре' in message):
        has_num = 4 
      if ('5' in message) or ('пять' in message):
        has_num = 5 
      if ('6' in message) or ('шесть' in message):
        has_num = 6 
      if ('7' in message) or ('семь' in message):
        has_num = 7 
      if ('8' in message) or ('восемь' in message):
        has_num = 8 
      if ('9' in message) or ('девять' in message):
        has_num = 9 

      print("Find num:", has_num)

      cnt = 0
      if (score_one > score_several and (has_num == 0 or has_num == 1)):
        print("One article.")
        cnt = 1
      else:
        print("Lots of articles:")
        if (has_num > 0):
          cnt = has_num
        else:
          cnt = 9
        print(cnt, "articles")
      
      tg_sendNews(self.tg_token, chat_id, cnt)
    print()



  def do_step(self):
    updates = tg_getUpdates(self.tg_token, self.offset)
    if len(updates['result']) == 0:
            return
    first_update = updates['result'][0]

    if 'message' in first_update:
      message = first_update['message']
      chat_id = message['chat']['id']
      if 'text' in message:
        text = message['text']
        print(text)
        self.do_action_on_message(chat_id, text)
      else:
        print('Not text:')
        print(message)
    else:
      print('Not message:')
      print(first_update)

    self.offset = int(first_update['update_id']) + 1


  def do_steps(self):
    print('Bot started')
    while (True):
      self.do_step()
     
import argparse

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--tg_token', required=True, help='Telegram token')
  args = parser.parse_args()
  bot = MemeBot(args.tg_token)
  bot.do_steps()
