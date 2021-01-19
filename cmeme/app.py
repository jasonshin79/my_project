from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

# client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
client = MongoClient('mongodb://test:test@localhost', 27017)
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

    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # title = soup.select_one('meta[property="og:title"]')['content']
    # url = soup.select_one('meta[property="og:url"]')['content']
    # comment = soup.select_one('meta[property="og:comment"]')['content']

    # youtube watch -> embed
    if 'watch?v=' in url_receive:
        url_receive = url_receive.replace('watch?v=', 'embed/')

    # 3. mongoDB에 데이터 넣기
    doc = {'title': title_receive, 'url': url_receive, 'comment': comment_receive, 'like': 0, 'dislike': 0}
    db.memes.insert_one(doc)

    return jsonify({'result': 'success', 'msg': '밈 업로드 완료!'})


@app.route('/meme', methods=['GET'])
def read_Memes():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    meme_list = list(db.memes.find({}, {'_id': False}))

    # 2. memes라는 키 값으로 memes 정보 보내주기
    return jsonify({'result': 'success', 'data': meme_list})


@app.route('/like', methods=['POST'])
def like_Memes():
    url_receive = request.form['url_give']
    db.memes.update_one({'url': url_receive}, {'$inc': {'like': 1}})
    return jsonify({'result': 'success', 'msg': '여러분의 <좋아요>가 더 나은 세상을 만듭니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
