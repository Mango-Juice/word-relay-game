import os
import requests

OK, USED, INVALID, NOT_WORD = range(4)
ERROR_MESSAGE = {USED: "이미 사용된 단어입니다.",
                INVALID: "유효하지 않은 단어입니다.",
                NOT_WORD: "단어(명사)가 아닙니다."}
used = []


def print_computer_word(c: str) -> str:
  URL = "https://opendict.korean.go.kr/api/search"
  param = {"key": os.environ['API_KEY'],
          "req_type": "json",
          "q": c,
          "num": 10,
          "sort": "popular",
          "advanced": "y",
          "method": "start",
          "letter_s": 2,
          "letter_e": 80,
          "pos": [1, 2, 3, 9, 15, 17, 18, 19, 20, 25, 26, 27]}
  result = requests.get(URL, params=param)
  data = result.json()["channel"]["item"]

  for i in data:
    word = i["word"]
    mean = i['sense'][0]

    if not (word in used):
      used.append(word)
      print(f"{word} : ({mean['pos']}) {mean['definition']}")
      return word[-1]
  return ""


def check_user_word(word: str, c: str) -> int:
  if len(word) < 2 or (c and c != word[0]): return INVALID
  if word in used: return USED

  URL = "https://opendict.korean.go.kr/api/search"
  param = {"key": os.environ['API_KEY'],
          "req_type": "json",
          "q": word,
          "advanced": "y",
          "pos": [1, 2, 3, 9, 15, 17, 18, 19, 20, 25, 26, 27]}
  result = requests.get(URL, params=param)
  data = result.json()["channel"]

  if data["total"] == 0 or data["item"][0]["word"] != word:
    return NOT_WORD

  used.append(word)
  return OK

print("아무 단어나 입력하여 시작하세요.")
while True:
  c = ''

  while True:
    inp = input()
    checker = check_user_word(inp, c)
    if checker == OK: 
      c = inp[-1]
      break
    else: print(ERROR_MESSAGE[checker])
  
  computer = print_computer_word(c)
  if computer: c = computer
  else:
    print("당신이 이겼어요.")
    break