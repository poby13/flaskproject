# -*- coding:utf-8 -*-
import mariadb
import configparser
import sys
import bcrypt
import os
from flask import Flask, request, render_template

# file upload https://tinyurl.com/yxkr95gr

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/flask-proj/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
config = configparser.ConfigParser()
config.read('app.ini')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_conn():
    cfg = config['db']
    conn = mariadb.connect(
        user=cfg['user'],
        password=cfg['password'],
        host=cfg['host'],
        port=int(cfg['port']),
        database=cfg['database']
    )
    return conn


@app.route("/")
def hello():
    return "<h1 style='color:blue'>플라스크 프로젝트</h1>"

# get 방식 호출


@app.route("/user", methods=['GET', 'POST'])
def user():
    html = ""
    error = ""

    sql = get_sql()
    # 삭제에러가 발생하면

    print("sql = ", sql)

    conn = get_conn()
    # 삭제, 수정, 추가
    cur = conn.cursor()

    # 입력, 수정, 삭제인 경우
    sql_head = sql[:3]
    print("="*10, sql_head)
    if sql_head == 'INS' or sql_head == 'DEL' or sql_head == 'UPD':
        cur.execute(sql)
        # 이전 작업을 반영한다.
        conn.commit()
    elif sql_head == 'ERR':
        # 에러인 경우
        error = sql
    # else:
    #     error = "예상되지 않은 오류가 발생했습니다."

    # 적용결과

    if sql[:6] != 'SELECT':
        # 반영결과를 추출한다.
        sql = 'SELECT id, name FROM mytest ORDER BY id desc'
        cur.execute(sql)

    for (id, name) in cur:
        html += "{name} <button onclick=\"updateForm({id})\">Edit</button> <a href=\"/user?cmd=delete&id={id}\">Del</a><br>\n".format(
            id=id,
            name=name
        )

    if conn:
        conn.close()

    # request.args의 데이터타입은 {"cmd": "insert"}

    # return html
    return render_template(
        "user.html",
        # action=request_param.get('cmd'),
        data=html,
        err=error
    )


def get_sql():
    err = ""
    request_param = request.args

    if request.method == 'POST':
        request_param = request.form

    # 처리 방식을 구분
    cmd = request_param.get('cmd')
    # 파라미터가 없으면 None이 반환된다.
    # print(cmd)
    try:
        # 추가
        if cmd == 'insert':
            name = request_param.get('name')
            password = request_param.get('password')
            filename = ""
            
            # 해시코드 https://tinyurl.com/yb3bq6c6
            hashed = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt(14))
            # name == ""
            # not name(거짓) ==> 참 ==> if 코드블록 실행
            if not name:
                raise Exception('이름을 확인해 주세요.')

            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if filename:
                sql = "INSERT INTO mytest (name, password, file) VALUES ('%s', '%s', '%s')" % (name, hashed.decode(), filename)
            else:
                sql = "INSERT INTO mytest (name, password) VALUES ('%s', '%s')" % (
                    name, hashed.decode())
        # 삭제
        elif cmd == 'delete':
            id = request_param.get('id')
            sql = 'DELETE FROM mytest WHERE id=%d' % int(id)

        # 수정
        elif cmd == 'update':
            name = request_param.get('name')
            if name == None:
                raise Exception('이름을 확인해 주세요.')
            id = request_param.get('id')
            sql = "UPDATE mytest SET name='%s' WHERE id=%d" % (name, int(id))
        else:
            # 기타는 모두 목록보기
            sql = err
    except TypeError as err:
        print(err)
        sql = "ERROR: %s" % err
    except Exception as err:
        print(err)
        sql = "ERROR: %s" % err

    return sql


if __name__ == "__main__":
    app.run(host='0.0.0.0')
