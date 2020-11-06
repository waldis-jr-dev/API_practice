import requests
import static

url_d = "https://systran-systran-platform-for-language-processing-v1.p.rapidapi.com/nlp/lid/detectLanguage/document"
url_t = "https://systran-systran-platform-for-language-processing-v1.p.rapidapi.com/translation/text/translate"
headers = static.translator_api()

def leng_detect(words):
    querystring = {"input": words}
    response = requests.request("GET", url_d, headers=headers, params=querystring)
    answ = response.json()
    lengs = []
    for i in answ['detectedLanguages']:
        lengs.append(i['lang'])
    return lengs


#print(leng_detect('Hello my friends'))


def translator(leng, transl, words):
    data = {
        "source": leng,
        "target": transl,
        "input": words
    }
    response = requests.request("GET", url_t, headers=headers, params=data)
    answ = response.json()
    return answ['outputs'][0]['output']


#print(translator('en', 'ru', 'Hello my friends'))


def auto_translator(words, leng):
    ret = []
    for i in leng_detect(words):
        data = {
            "source": i,
            "target": leng,
            "input": words
        }
        try:
            response = requests.request("GET", url_t, headers=headers, params=data)
            answ = response.json()
            ro = answ['outputs'][0]['output']
            ret.append(f'If you mean "{i}" => {ro}')
        except Exception:
            pass
    return ret

print(auto_translator('webhook', 'ru'))