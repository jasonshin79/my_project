from flask import Flask, render_template, jsonify, request
import requests, re
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
# client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbproject  # 'dbproject'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')


@app.route('/keep')
def keep():
    return render_template('keep.html')


@app.route('/meme', methods=['POST'])
def post_Meme():
    # 1. 클라이언트로부터 정보 받아오기
    title_receive = request.form['title_give']
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    # 2. 영상 url을 업로드하기 위해 적절하게 수정하기
    # 주소를 그대로 공유하는 경우
    if 'watch?v=' in url_receive:
        url_receive = url_receive.replace('watch?v=', 'embed/')

    # 공유하기 링크로 공유하는 경우
    if url_receive.startswith('https://youtu.be/'):
        url_receive = url_receive.replace('https://youtu.be/', 'https://www.youtube.com/embed/')

    # 링크에서 &key=value 형태 모두 삭제하여 재생 오류 방지
    url_receive = re.sub('\&.*', '', url_receive)

    # 3. mongoDB에 데이터 넣기
    doc = {'title': title_receive, 'url': url_receive, 'comment': comment_receive, 'like': 0}
    db.memes.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '밈 업로드 완료!'})


@app.route('/meme', methods=['GET'])
def show_likes():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    like_list = object_id_decoder(list(db.memes.find().sort('like', -1)))

    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'data': like_list})

def read_Memes():
    keyword_receive = request.args.get('keyword_give', '')
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    meme_list = list(db.memes.find(
        {'$or': [{'title': {'$regex': keyword_receive}},
                 {'comment': {'$regex': keyword_receive}}]}, {'_id': False}))

    # 2. memes라는 키 값으로 memes 정보 보내주기
    return jsonify({'result': 'success', 'data': meme_list})


@app.route('/like', methods=['POST'])
def like_Memes():
    url_receive = request.form['url_give']
    db.memes.update_one({'url': url_receive}, {'$inc': {'like': 1}})
    return jsonify({'result': 'success', 'msg': '여러분의 <좋아요>가 더 나은 세상을 만듭니다!'})

def object_id_decoder(data_list):
    results = []
    for data in data_list:
        data['_id'] = str(data['_id'])
        results.append(data)
    return results


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
