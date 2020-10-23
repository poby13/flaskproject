#-*- coding:utf-8 -*-
import mariadb
import configparser
import sys
from flask import Flask, request, render_template
 
app = Flask(__name__)

config = configparser.ConfigParser()
config.read('app.ini')


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
@app.route("/user")
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
        # action=request.args.get('cmd'),
        data = html,
        err = error
    )
 
# get 방식 입력
@app.route("/newuser")
def user_insert():
    # http://localhost:5000/user?name=f
    # 참고: https://tinyurl.com/y47eyszw
    new_name = request.args.get('name') # f
    conn = get_conn()
    sql = "INSERT INTO mytest (name) VALUES ('{}')".format(new_name)
 
    cur = conn.cursor()
    cur.execute(sql)
    
    conn.commit()
 
    if conn:
        conn.close()
    
    return "입력성공"
 
def get_sql():
    msg = ""
    err = ""
    # 처리 방식을 구분
    cmd = request.args.get('cmd')
    # 파라미터가 없으면 None이 반환된다.
    # print(cmd)
    try:
        # 추가
        if cmd == 'insert':
            name = request.args.get('name')
            # name == ""
            # not name(거짓) ==> 참 ==> if 코드블록 실행
            if not name:
                raise Exception('이름을 확인해 주세요.')
            sql = "INSERT INTO mytest (name) VALUES ('{}')".format(name)
        # 삭제
        elif cmd == 'delete':
            id = request.args.get('id')
            sql = 'DELETE FROM mytest WHERE id={}'.format(int(id))
 
        # 수정
        elif cmd == 'update':
            name = request.args.get('name')
            if name == None:
                raise Exception('이름을 확인해 주세요.')
            id = request.args.get('id')
            sql = "UPDATE mytest SET name='{}' WHERE id={}".format(name, int(id))
        else:
            # 기타는 모두 목록보기
            sql = err
    except TypeError as err:
        sql = "ERROR: {0}".format(err)
    except Exception as err:
        sql = "ERROR: {0}".format(err)
 
    return sql
 
 
 
 
if __name__ == "__main__":
    app.run(host='0.0.0.0')