
def main(q_type, question, ans, status):
    # 共通して、正解は3行目に配置
    answer = ""
    if ans == 1:
        answer = question[2]

    tmp_dict = {
            "next": f"?status={int(status)+1}",
            "ans": f"?status={int(status)}&ans=1",
            "question": question[1],
            "answer": answer,
            "choices": None
        }

    # 4択問題の場合
    if q_type == "multi":
        inp_dict = tmp_dict.copy()
        inp_dict["choices"] = question[3:]

        return "multi.html", inp_dict

    # 標準入力問題
    elif q_type == "input":
        inp_dict = tmp_dict.copy()

        return "input.html", inp_dict
