from underthesea import word_tokenize
import pandas as pd

VIETNAMESE_STOPWORDS = {
    'và', 'của', 'là', 'có', 'được', 'trong', 'với', 'đã', 'này',
    'cho', 'từ', 'nhưng', 'các', 'khi', 'về', 'một', 'những', 'tại',
    'sẽ', 'không', 'cũng', 'theo', 'như', 'thì', 'hay', 'để', 'vào',
    'bởi', 'nên', 'mà', 'đây', 'đó', 'rằng', 'vì', 'sau', 'trên'
}

def tokenize_vi(text):
  try:
    tokens = word_tokenize(text, format='text')
    token_list = tokens.split()
    cleaned = [
        t.lower() for t in token_list
        if t.lower() not in VIETNAMESE_STOPWORDS
        and len(t) > 1
        and not t.isdigit()   
    ]
    return ' '.join(cleaned)
  except Exception as e:
      return ''
