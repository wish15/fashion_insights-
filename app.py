from flask import Flask, request, jsonify,render_template

import json
        
import pandas as pd

df=pd.read_csv("df.csv")


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')
@app.route('/query',methods=['POST'])
def call_query():
    # print("bhai",request.form)
    # # print(jsonify(request.form['text']))
    # req=request.form
    # req=(req[0][1]).json
    # print(req)
    #request.json
    req=json.loads(request.form["text"])

    print("bhai",req)
    if req['query_type'] == "discounted_products_list":
        return query(req)
    elif req["query_type"] == "discounted_products_count|avg_discount":
        return q2(req)
    elif req["query_type"] == "expensive_list":
        if len(req.keys())==1:
            t=list(df.loc[df['competition'] != "0"]['_id'])
            return jsonify({'expensive_list' : t})
        else:
            return q3(req)
    else:
        return q4(req)
def query(req):
    op1=req['filters'][0]['operand1']
    op2=req['filters'][0]['operand2']
    op=req['filters'][0]['operator']
    if op =='>':
        t=list(df.loc[df[op1] > op2]['_id'])
        
    elif op == '==':
        t=list(df.loc[df[op1] == op2]['_id'])
    else:
        t=list(df.loc[df[op1] < op2]['_id'])
    return jsonify({'discounted_products_list' : t})
def q2(req):
    op1=req['filters'][0]['operand1']
    op2=req['filters'][0]['operand2']
    op=req['filters'][0]['operator']
    if op =='>':
        t=list(df.loc[df[op1] > op2]['discount'])
    elif op == '==':
        t=list(df.loc[df[op1] == op2]['discount'])
    else:
        t=list(df.loc[df[op1] < op2]['discount'])
    t1=len(t)
    t2=sum(t)/len(t)
    return jsonify({'discounted_products_count':t1 , 'avg_discount':t2})
def q3(req):
    op1 = req['filters'][0]['operand1']
    op2 = req['filters'][0]['operand2']
    op = req['filters'][0]['operator']
    if op == '>':
        t = list(df.loc[(df[op1] > op2)&(df['competition'] != "0")]['_id'])
    elif op == '==':
        t = list(df.loc[(df[op1] == op2)&(df['competition'] != "0")]['_id'])
    else:
        t = list(df.loc[(df[op1] < op2)&(df['competition'] != "0")]['_id'])
    return jsonify({'expensive_list': t})
def q4(req):
    op1 = req['filters'][0]['operand1']
    op2 = req['filters'][0]['operand2']
    op = req['filters'][0]['operator']
    op3 = req['filters'][1]['operand1']
    op4 = req['filters'][1]['operand2']
    ope = req['filters'][1]['operator']
    if op == '>':
        x=df[op1] > op2
    elif op == '==':
        x=df[op1] == op2
    else:
        x=df[op1] < op2
    if ope == '>':
        x1=df[op3] > op4
    elif ope == '==':
        x1=df[op3] == op4
    else:
        x1=df[op3] < op4
    t = list(df.loc[(x)&(x1)&(df['competition'] != "0")]['_id'])
    return jsonify({'competition_discount_diff_list' : t})
if __name__=='__main__':
    app.run(debug=True, port=5500)