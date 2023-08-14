import pymysql
import json
db = pymysql.connect(host='127.0.0.1', user='admin', database='flyliht_wordbook', charset='utf8',autocommit=True)
cur = db.cursor()

def get_tran(data):
    temp=[]
    temp2={}
    for i in data:
        try:
            temp2['pos'] = i['pos']
        except KeyError:
            temp2['pos'] = 'other'
        temp2['tran'] = i['tranCn']
        temp.append(temp2.copy())
    return temp

def get_synonyms(data):
    temp=[]
    temp2={}
    temp3=[]
    temp4={}
    for i in data:
        temp2['pos'] = i['pos']
        temp2['tran'] = i['tran']
        for j in i['hwds']:
            temp4['content'] = j['w']
            temp3.append(temp4.copy())
        temp2['words'] = temp3[:]
        temp3.clear()
        temp.append(temp2.copy())
    return temp

def get_rel(data):
    temp=[]
    temp2={}
    temp3=[]
    temp4={}
    for i in data:
        temp2['pos'] = i['pos']
        for j in i['words']:
            temp4['content'] = j['hwd']
            temp4['tran'] = j['tran']
            temp3.append(temp4.copy())
        temp2['words'] = temp3[:]
        temp3.clear()
        temp.append(temp2.copy())
    return temp

def get_sentence(data):
    temp=[]
    temp2={}
    for i in data:
        temp2['content'] = i['sContent']
        temp2['tran'] = i['sCn']
        temp.append(temp2.copy())
    return temp

def get_antonyms(data):
    temp=[]
    temp2={}
    for i in data:
        temp2['content'] = i['hwd']
        temp2['tran'] = ''
        temp.append(temp2.copy())
    return temp

def get_phrase(data):
    temp=[]
    temp2={}
    for i in data:
        temp2['content'] = i['pContent']
        temp2['tran'] = i['pCn']
        temp.append(temp2.copy())
    return temp

def replaceFran(str):
    fr_en = [['é', 'e'], ['ê', 'e'], ['è', 'e'], ['ë', 'e'], ['à', 'a'], ['â', 'a'], ['ç', 'c'], ['î', 'i'], ['ï', 'i'],
             ['ô', 'o'], ['ù', 'u'], ['û', 'u'], ['ü', 'u'], ['ÿ', 'y']
             ]
    for i in fr_en:
        str = str.replace(i[0], i[1])
    return str
filename = "temp.json";

def run():
    file = open(filename,'r',encoding='utf-8' );
    for line in file.readlines():
        words = replaceFran(line.strip())
        word_json = json.loads( words )
        print(word_json['content']['word']['wordHead'])
        main(word_json)
    file.close()
    
def main(parsed_data):
    data = parsed_data['content']['word']['content']
    word = parsed_data['content']['word']['wordHead']
    tran = get_tran(data['trans'])
    try:
        synonyms = get_synonyms(data['syno']['synos'])
    except KeyError:
        synonyms = []
    try:
        antonyms = get_antonyms(data['antos']['anto'])
    except KeyError:
        antonyms = []
    try:
        phone = data['phone']
    except KeyError:
        phone = ''
    try:
        usphone = data['usphone']
    except KeyError:
        usphone = ''
    try:
        ukphone = data['ukphone']
    except KeyError:
        ukphone = ''
    phone = {'phone': phone, 'usphone': usphone, 'ukphone': ukphone}
    try:
        phrase = get_phrase(data['phrase']['phrases'])
    except KeyError:
        phrase = []
    try:
        rel = get_rel(data['relWord']['rels'])
    except KeyError:
        rel = []
    try: 
        rem_method = data['remMethod']['val']
    except KeyError:
        rem_method = ''
    try:
        sentence = get_sentence(data['sentence']['sentences'])
    except KeyError:
        sentence = []


    sql = "INSERT INTO lib (word, phone, tran, syno, anto, rel, phrase, rem_method,sentence) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s)"
    values = (word, 
            json.dumps(phone, ensure_ascii=False),
            json.dumps(tran, ensure_ascii=False),
            json.dumps(synonyms, ensure_ascii=False),
            json.dumps(antonyms, ensure_ascii=False),
            json.dumps(rel, ensure_ascii=False),
            json.dumps(phrase, ensure_ascii=False),
            rem_method,
            json.dumps(sentence, ensure_ascii=False))
    try:
        cur.execute(sql,values)
    except pymysql.err.IntegrityError as msg:
        if msg.args[0] == 1062:
            pass
        else:
            print(msg)
    except pymysql.err.ProgrammingError as msg:
        print(sql % values)
        print(msg)
        exit()

run()
db.commit()
cur.close()
db.close()
