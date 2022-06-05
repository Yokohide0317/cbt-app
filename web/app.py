# -*- coding: utf-8 -*-
from flask import Flask, session,render_template, request, redirect
import os
import pandas as pd
import pathlib

app = Flask(__name__)

def get_datalist(search="./data/"):
    under_dir = pathlib.Path(search)
    dir_list = [str(d.stem) for d in under_dir.iterdir() if d.is_dir()]
    data_list = [str(d.name) for d in under_dir.iterdir() if d.is_file()]
    return dir_list, data_list

def read_csv(csv_path):
    #df = pd.read_csv(csv_path, sep="\t")
    with open(csv_path) as f:
        lines = f.readlines()

    # 大問, 小問, 問題, 答え
    question_list = [l.strip().split(",") for l in lines]
    return question_list

# 最初
@app.route('/')
def main():
    dir_list, data_list = get_datalist()
    inp_dict = {
        "dir_list": dir_list,
        "data_list": data_list,
        "title": "年度",
        "current": "/data"
                }
    return render_template("index.html", python=inp_dict)

# サーチング
@app.route('/data/<path:path>', methods=["GET", "POST"])
def second(path):
    req = request.args
    file_id = None

    try:
        file_id = req.get("file_id")
    except:
        pass
    if file_id != None:
        return redirect(f"/questions/{path}/?file_id={file_id}")

    dir_list, data_list = get_datalist(f"./data/{path}")
    inp_dict = {
        "dir_list": dir_list,
        "data_list": data_list,
        "title": "教科",
        "current": f"/data/{path}"
                }
    return render_template("index.html", python=inp_dict)

@app.route('/questions/<path:path>', methods=['GET'])
def question(path):
    req = request.args
    file_id = None
    try:
        file_id = req.get("file_id")
    except:
        pass
    q_id = req.get("q_id")
    q_id = 1 if q_id == None else q_id

    file_path = pathlib.Path("./data") / path / file_id
    if not file_path.is_file():
        return

    question_list = read_csv(file_path)
    question = question_list[q_id]
    inp_dict = {
        "big_num": question[0],
        "small_num": question[1],
        "question": question[2]
    }
    return render_template("question.html", python=inp_dict)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 12345))
    app.run(host="0.0.0.0", port=port, debug=True)

