import datetime
import tkinter as tk
from collections import deque
from tkinter import ttk
import pygit2


# 커밋 히스토리 그래프 생성 함수
def draw_commit_history_ui(top_frame):
    ###########################################################################
    # UI / left, right, scrollbar_left, scrollbar_right, tree, canvas
    ###########################################################################

    # 프레임 생성
    left = tk.Frame(top_frame, border=1, relief="flat", bg="white")
    left.pack(side="left", fill="both", expand=True)

    right = tk.Frame(top_frame, border=1, relief="flat", bg="white", width='40')
    right.pack(side="right", fill="y")

    # 스크롤바
    scrollbar_left = ttk.Scrollbar(left, orient="vertical")
    scrollbar_left.pack(side="right", fill="y")

    # Treeview 생성
    tree = ttk.Treeview(right, columns=("#1"), selectmode="extended", show="tree headings")
    tree.heading("#0", text="configuration", anchor="w")
    tree.heading("#1", text="content", anchor="w")
    tree.column("#0", anchor="e", stretch=False, width=100)
    tree.column("#1", anchor="e", stretch=False, width=500)
    tree.pack(side="top", fill="y")

    # Branch Control View 생성
    branch_control_frame = tk.Frame(right, border=1, bg="#3c3c3c", width=300, height=500)
    branch_control_frame.pack(side="bottom", fill="both")

    # 캔버스
    canvas = tk.Canvas(left, bg="white", yscrollcommand=scrollbar_left.set)
    canvas.pack(fill="both", expand=True)

    # left 영역의 스크롤바와 캔버스 연결
    scrollbar_left.config(command=canvas.yview)

    # 내용 프레임
    content_frame = tk.Frame(canvas, bg="white")
    content_frame.pack(fill="both", expand=True)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # 스크롤 기능 구현해야함! wh/할일
    def configure_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", configure_canvas)

    return tree, canvas, branch_control_frame


def handle_text_click(commit, tree):
    for item in tree.get_children():
        tree.delete(item)

    commit_time = datetime.datetime.fromtimestamp(commit.commit_time)
    formatted_time = commit_time.strftime("%Y-%m-%d %H:%M:%S")

    tree.insert("", tk.END, text="ID", value=[str(commit.id)], open=False)
    tree.insert("", tk.END, text="TIME", value=[formatted_time], open=False)
    tree.insert("", tk.END, text="AUTHOR", value=[str(commit.author)], open=False)
    tree.insert("", tk.END, text="MESSAGE", value=[str(commit.message)], open=False)
    parent_ids = str()
    for n in commit.parent_ids:
        parent_ids += (str(n) + "\n")
    tree.insert("", tk.END, text="PARENT_ID", value=[parent_ids], open=False)
    tree.insert("", tk.END, text="TREE_ID", value=[str(commit.tree_id)], open=False)


def draw_commit_history(tree, canvas, repo_path):
    ###########################################################################
    # LOGIG / tree, canvas, repo -> clear + draw -> update
    ###########################################################################

    # tree, canvas 초기화
    for item in tree.get_children():
        tree.delete(item)
    canvas.delete("all")

    # Git 리포지토리 열기 path를 전달받아 객체 생성
    #
    try:
        repo = pygit2.Repository(repo_path)
        walk_object = repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL | pygit2.GIT_SORT_TIME)
    except pygit2.GitError:
        return

    # 각 행의 높이
    row_height = 20

    # 좌측 여백
    margin_left = 10

    commits = []  # 커밋 객체 리스트
    for row, commit in enumerate(walk_object):
        commits.append(commit)  # 커밋 ID를 행 번호로 등록

    parent_list = deque()

    for i in range(0, len(commits)):
        next_commit_id = str()
        row = i + 1
        if i != 0:
            col = parent_list.index(str(commits[i].id)[0:7])
        elif i == 0:
            col = 0
            parent_list.append(str(commits[0].id)[0:7])

        print("--------------loop-------------------------")
        print("현재 커밋 아이디 : ", commits[i].id)
        print("현재 커밋의 패런트 아이디 : ", commits[i].parent_ids)
        print("현재 parent 데크 목록 : ", parent_list)
        print("현재 column : ", col)
        print("현재 row : ", row)
        # 여기에 점 찍기

        node_width = 50
        node_height = 15
        node_x = 60
        node_y = row_height + (row_height - node_height) // 2
        canvas.create_rectangle(margin_left + node_x * col, node_y * row, margin_left + node_x * col + node_width,
                                node_y * row + node_height,
                                fill="lightblue",
                                outline="black")

        text_id = canvas.create_text(margin_left + node_x * col + node_width // 2, node_y * row + node_height // 2,
                                     text=str(commits[i].id)[0:7], font=("Helvetica", 10, "bold"), fill="black")
        # 텍스트에 태그 할당
        canvas.itemconfig(text_id, tags=str(i))
        canvas.tag_bind(text_id, "<Button-1>",
                        lambda event, c=commits[i], t=tree: handle_text_click(c, t))

        # 처음 화면 생성시 첫번째 노드 정보 띄우기
        if i == 0:
            handle_text_click(commits[i], tree)

        if i < len(commits) - 1:
            next_commit_id = str(commits[i + 1].id)[0:7]

        # parent_list 업데이트
        temp_list = reversed(commits[i].parent_ids)
        for j in temp_list:
            parent_list.insert(col, str(j)[0:7])
        print(parent_list)
        count = 0
        while True:
            try:
                parent_list.remove(str(commits[i].id)[0:7])
                print("[", str(commits[i].id)[0:7], "] removed!!!!!!!!!!!")
                count += 1
            except ValueError:
                break
        print("다음 parent 데크 목록 (선긋기): ", parent_list)

        # 다음거 체크
        alive_parent = len(parent_list)
        branch_pair = []
        next_col = str()
        check_next = 0
        temp_cnt = 0

        #col보다 큰 위치에서 브랜치 분기로 인한 parent_list 감소시 증가
        col_cnt = 0

        #parent_list_str = []
        #for j in commits[i].parent_ids:
        #    parent_list_str.append(str(j)[0:7])

        if i < len(commits) - 1:
            next_col = parent_list.index(str(commits[i + 1].id)[0:7])

        for j in range(len(parent_list)):
            if len(commits[i].parents) >= 2:
                if parent_list[j] == next_commit_id:
                    # 여기 페어에 연결
                    if j == parent_list.index(str(commits[i].parent_ids[0])[0:7]) + 1:
                        branch_pair.append([col, next_col])
                        temp_cnt += 1

                        print("a, 페런트 2개이상, 다음연결될게 다음 커밋, 진짜부모 인덱스 + 1 일경우")
                    else:
                        branch_pair.append([j - temp_cnt, next_col])
                        print("b, 페런트 2개이상, 다음연결될게 다음 커밋, 진짜부모 인덱스 + 1 X")
                    check_next += 1
                    if j > next_col:
                        col_cnt += 1
                else:
                    if parent_list[j] == str(commits[i].parent_ids[1])[0:7]:
                        print("c, 페런트 2개이상, 다음연결될게 다음 커밋 X, 다음 연결될게 가짜부모일대")
                        temp_cnt += 1
                        branch_pair.append([j - temp_cnt, j])
                    else:
                        branch_pair.append([j - temp_cnt, j - col_cnt])

                        print("d,페런트 2개이상, 다음연결될게 다음 커밋 X, 다음 연결될게 가짜부모 X")
                    # 그냥 일직선
            else:
                if parent_list[j] == next_commit_id:
                    print("e, 페런트 1개, 다음 연결될게 다음 커밋")
                    branch_pair.append([j, next_col])
                    check_next += 1
                else:
                    if check_next > 1:
                        branch_pair.append([j, j - check_next + 1])
                        print("f, 페런트 1개, 다음연결될게 당므 커밋이 아님, 그런데 하나이상 합쳐졌다면")
                    else:
                        branch_pair.append([j, j])
                        print("g, 페런트 1개, 다음연결될게 당므 커밋이 아님, 그런데 하나이상 합쳐지지않음")
                    # 그냥 일직선
        temp_index = 0
        count = 0
        if check_next > 1:
            while True:
                try:
                    if count == 0:
                        temp_index = parent_list.index(str(commits[i + 1].id)[0:7])
                    parent_list.remove(str(commits[i + 1].id)[0:7])
                    count += 1
                except ValueError:
                    parent_list.insert(temp_index, str(commits[i + 1].id)[0:7])
                    break
            for x, y in branch_pair:
                # branch pair row, x -> row + 1 , y 로 선긋기
                # 좌표 정보 node_x * col, node_y * row
                canvas.create_line(margin_left + node_x * x, node_y * row, margin_left + node_x * y, node_y * (row + 1),
                                   fill="black")
        else:
            cur_parent_num = len(commits[i].parents)
            if cur_parent_num >= 2:
                for j in range(col + 1):
                    canvas.create_line(margin_left + node_x * j, node_y * row, margin_left + node_x * j,
                                       node_y * (row + 1), fill="black")
                    print("a")
                for j in range(col, col + cur_parent_num - 1):
                    canvas.create_line(margin_left + node_x * col, node_y * row, margin_left + node_x * (j + 1),
                                       node_y * (row + 1), fill="black")
                    print("b")
                for j in range(col + 1, alive_parent + 1 - cur_parent_num):
                    canvas.create_line(margin_left + node_x * j, node_y * row, margin_left + node_x * (j + cur_parent_num - 1),
                                       node_y * (row + 1), fill="black")
                    print(col + 1, alive_parent, 1, cur_parent_num)
                    print("c")
            elif len(commits[i].parents) == 1:
                for j in range(alive_parent):
                    canvas.create_line(margin_left + node_x * j, node_y * row, margin_left + node_x * j,
                                       node_y * (row + 1), fill="black")

        # 커밋 데이터를 행마다 그리기
        # tree.insert("", tk.END, text=str(commits[i].id)[0:7], values=[
        #    row], open=False)
