import requests
import base64
import cv2
from string import ascii_uppercase as alc
import pickle

lucky_dict = {
    "13":4, "31":4, "68":3, "86":3, "49":2, "94":2, "27":1, "72":1,
    "19":4, "91":4, "78":3, "87":3, "34":2, "43":2, "26":1, "62":1,
    "14":4, "41":4, "67":3, "76":3, "39":2, "93":2, "28":1, "82":1,
    "11":4, "22":4, "88":3, "99":3, "66":2, "77":2, "33":1, "44":1
}

bad_dict = {
    "12":-4,"21":-4,"69":-3,"96":-3,"48":-2,"84":-2,"37":-1,"73":-1,
    "17":-4,"71":-4,"89":-3,"98":-3,"46":-2,"64":-2,"23":-1,"32":-1,
    "18":-4,"81":-4,"79":-3,"97":-3,"36":-2,"63":-2,"24":-1,"42":-1,
    "16":-4,"61":-4,"47":-3,"74":-3,"38":-2,"83":-2,"29":-1,"92":-1
}

def get_ocr_res(filename):
    client_id = <your client_id>
    client_secret = <your client_secret>
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    response = requests.get(host)
    access_token = response.json()['access_token']

    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
    f = open(filename, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        words_result = response.json()['words_result']
        return words_result

def draw_rec(image, plate_num,plate_dic,color=(0, 255, 0),text=""):
    location = plate_dic[plate_num]
    x = location['left']
    y = location['top']
    p1 = (location['left'],location['top'])
    p2 = (location['left']+location['width'],location['top']+location['height'])
    cv2.rectangle(image, p1, p2, color, 1)
    cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)


def draw_line(image, plate_num,plate_dic,color=(0, 255, 0),text=""):
    location = plate_dic[plate_num]
    x = location['left']
    y = location['top']
    p1 = (location['left'],location['top']+location['height']+10)
    p2 = (location['left']+location['width'],location['top']+location['height']+10)
    cv2.line(image, p1, p2, color, 5)
    #cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)


def covnert_num_str(s1):
    cnt = 1
    alpha_to_num = {}
    for i in alc:
        alpha_to_num[i] = str(cnt)
        cnt += 1
    res = ""
    for i in s1:
        if i in alc:
            res += alpha_to_num[i]
        else :
            res += i
    return res

def scores(s):
    s_list = []
    res = 0
    for i in range(len(s)-1):
        s_list.append(s[i]+s[i+1])
    for subs in s_list:
        if subs in lucky_dict.keys():
            res += lucky_dict[subs]
        elif subs in bad_dict.keys():
            res += bad_dict[subs]
    return res

def all_safe(s):
    s_list = []
    res = 0
    for i in range(len(s)-1):
        s_list.append(s[i]+s[i+1])
    for subs in s_list:
        if subs in bad_dict.keys():
            return False
    return True

def triple_same(s):
    import re
    regex = r"(.)\1{2,}"
    maches = re.findall(regex, s)
    if len(maches) > 0:
        return True
    return False

def workflow(filename):
    image = cv2.imread(filename)
    words_result = get_ocr_res(filename)
    plate_dic = {}
    for word in words_result:
        location = word['location']
        content = word['words']
        if len(content) == 6 and content.isalnum():
            plate_dic[word['words']] = location
    plate_nums_scores = {}
    for key in plate_dic.keys():
        plate_nums_scores[key] = scores(covnert_num_str(key))
    
    plate_nums_scores = sorted(plate_nums_scores.items(), key = lambda kv:(kv[1], kv[0]))
    plate_nums_scores.reverse()
    max_cnt = 1

    #画出前三吉利的车牌
    lucky_num = []
    for pair in plate_nums_scores:
        if max_cnt <= 3:
            lucky_num.append(pair[0])
            draw_rec(image,pair[0],plate_dic,color=(0,0,255),text=str(max_cnt))
            max_cnt += 1
        else:
            break
    
    #画出毫无凶兆的车牌
    for pair in plate_nums_scores:
        tmp_num = covnert_num_str(pair[0])
        if all_safe(tmp_num):
            draw_line(image,pair[0],plate_dic,color=(0,255,0),text="安全")
        if triple_same(pair[0]):
            draw_line(image,pair[0],plate_dic,color=(255,0,0),text="连号")

    # print(plate_nums)
    cv2.imwrite(filename, image)

    