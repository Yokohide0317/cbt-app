# -*- coding: utf-8 -*-
from flask import Flask, session,render_template, request, redirect
import os
import pandas as pd
import pathlib
import make_question

app = Flask(__name__)

def get_datalist(search="./data/"):
    under_dir = pathlib.Path(search)
    dir_list = [str(d.stem) for d in under_dir.iterdir() if d.is_dir()]
    data_list = [str(d.name) for d in under_dir.iterdir() if d.is_file(

    )]
    return dir_list, data_list

def read_csv(csv_path):
    with open(csv_path) as f:
        lines = f.readlines()

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
    """
    req = request.args
    file_id = None

    try:
        file_id = req.get("file_id")
    except:
        pass
    if file_id != None:
    """
    dir_list, data_list = get_datalist(f"./data/{path}")
    if "main.csv" in data_list:
        return redirect(f"/questions/{path}/?status=1")

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
    status = int(req.get("status"))
    status = 1 if status == None else status

    ans = req.get("ans")
    ans = 0 if ans == None else int(ans)

    file_dir = pathlib.Path("./data") / path
    main_csv = file_dir / "main.csv"

    # indexファイルから、順番に情報を取得し、それぞれのcsvファイルを呼び出す
    q_info_list = read_csv(main_csv)
    if status >= len(q_info_list):
        return render_template("done.html")

    q_info = q_info_list[status]
    q_infoDic = {
        "big_num": q_info[0],
        "small_num": q_info[1],
        "type": q_info[2],
        "id": q_info[3]
    }

    # 外部スクリプト
    q_type, question = get_question(file_dir, q_infoDic)
    html, inp_dict = make_question.main(q_type, question, ans, status)

    return render_template(html, python=inp_dict)

def get_question(dir_path, q_infoDic):
    q_type = q_infoDic["type"]
    file = dir_path / f"{q_type}.csv"
    lines = read_csv(file)
    row = 0
    for index, data in enumerate(lines):
        if q_infoDic["id"] == data[0]:
            row = index
            break
    q_line = lines[row]
    return q_infoDic["type"], q_line

if __name__ == "__main__":
    port = int(os.getenv("PORT", 12345))
    app.run(host="0.0.0.0", port=port, debug=True)

