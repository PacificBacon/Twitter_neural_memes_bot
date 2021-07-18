def message2vec(tokenizer_model, embedding_model, message):
  tokenizer_out = tokenizer_model(message, return_tensors='pt')
  tokens = tokenizer_out['input_ids'][0]
  #print(tokens)
  vec_list = embedding_model(tokens)
  #print(vec_list.shape)
  vec = vec_list.mean(dim = 0)
  #print(vec.shape)
  return vec

from torch import nn
def get_similarity(tokenizer_model, embedding_model, message1, message2):
  vec1 = message2vec(tokenizer_model, embedding_model, message1)
  vec2 = message2vec(tokenizer_model, embedding_model, message2)
  similarity = nn.CosineSimilarity(dim=0)
  score = similarity(vec1, vec2)
  return score.item()
