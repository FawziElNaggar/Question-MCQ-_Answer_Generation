# -*- coding: utf-8 -*-
"""BDG(Distractor Generation).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kHLsn3aUtsTJ_n4EgK_et2A1_Z0Q8dpQ
"""

from nlgeval import NLGEval

nlgeval = NLGEval(
    metrics_to_omit=['METEOR', 'EmbeddingAverageCosineSimilairty', 'SkipThoughtCS', 'VectorExtremaCosineSimilarity',
                     'GreedyMatchingScore', 'CIDEr'])

!wget https://github.com/voidful/BDG/releases/download/v2.0/BDG.pt
!wget https://github.com/voidful/BDG/releases/download/v2.0/BDG_ANPM.pt
!wget https://github.com/voidful/BDG/releases/download/v2.0/BDG_PM.pt

from transformers import RobertaTokenizer
from transformers import RobertaForMultipleChoice
import torch
from torch.distributions import Categorical
import itertools as it
import nlp2go

tokenizer = RobertaTokenizer.from_pretrained("LIAMF-USP/roberta-large-finetuned-race")
model = RobertaForMultipleChoice.from_pretrained("LIAMF-USP/roberta-large-finetuned-race")
model.eval()
model.to("cuda")

dg_model = nlp2go.Model('./BDG.pt')
dg_model_pm = nlp2go.Model('./BDG_PM.pt')
dg_model_both = nlp2go.Model('./BDG_ANPM.pt')

def get_all_Options(context, question, answer):
  d_input = context + '</s>' + question + '</s>' + answer
  choices = dg_model.predict(d_input, decodenum=3)['result']
  choices_pm = dg_model_pm.predict(d_input, decodenum=3)['result']
  choices_both = dg_model_both.predict(d_input, decodenum=3)['result']
  all_options = choices + choices_pm + choices_both
  return all_options

def selection(context, question, answer, all_options):
    max_combin = [0, []]
    for combin in set(it.combinations(all_options, 3)):
        options = list(combin) + [answer]
        keep = True
        for i in set(it.combinations(options, 2)):
            a = "".join([char if char.isalpha() or char == " " else " " + char + " " for char in i[0]])
            b = "".join([char if char.isalpha() or char == " " else " " + char + " " for char in i[1]])
            metrics_dict = nlgeval.compute_individual_metrics([a], b)
            if metrics_dict['Bleu_1'] > 0.5:
                keep = False
                break
        if keep:
            prompt = context + tokenizer.sep_token + question
            encoding_input = []
            for choice in options:
                encoding_input.append([prompt, choice])
            encoding_input.append([prompt, answer])
            labels = torch.tensor(len(options) - 1).unsqueeze(0)
            encoding = tokenizer(encoding_input, return_tensors='pt', padding=True, truncation='only_first')
            outputs = model(**{k: v.unsqueeze(0).to('cuda') for k, v in encoding.items()},
                            labels=labels.to('cuda'))  # batch size is 1
            entropy = Categorical(probs=torch.softmax(outputs.logits, -1)).entropy().tolist()[0]
            if entropy >= max_combin[0]:
                max_combin = [entropy, options]
    return max_combin[1][:-1]

