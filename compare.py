import time
from scipy.optimize import linear_sum_assignment
import numpy as np
import random

# 設定のパラメータ
num_students = 40
num_courses = 10
course_capacity = 4

# 学生のデータ生成
students_preferences = {i: random.sample(
    range(num_courses), 3) for i in range(num_students)}

# コースの空き状況
course_slots = {i: course_capacity for i in range(num_courses)}


# ハンガリアンアルゴリズム用のコスト行列を作成
num_total_course_slots = num_courses * course_capacity
cost_matrix = np.full(
    (num_students, num_total_course_slots), 1000)  # 高いコストで初期化

# 希望度をコストに変換（低い希望度が低いコストになるように）
preference_to_cost = {0: 0, 1: 1, 2: 2}  # 希望度をコストに変換（0:最高希望, 2:最低希望）

# コスト行列の更新
for student, preferences in students_preferences.items():
    for i, course in enumerate(preferences):
        for slot in range(course_capacity):
            course_slot_index = course * course_capacity + slot
            cost_matrix[student, course_slot_index] = preference_to_cost[i]


# 計算時間と解の精度の評価

# Greedyアルゴリズムの計算時間測定
start_time = time.time()
# Greedyアルゴリズムの実行（再度実行して計算時間を測定）
greedy_assignments = {}
for student in students_preferences:
    assigned = False
    for preference in students_preferences[student]:
        if course_slots[preference] > 0:
            greedy_assignments[student] = preference
            course_slots[preference] -= 1
            assigned = True
            break
    if not assigned:
        greedy_assignments[student] = None
greedy_time = time.time() - start_time


# ハンガリアンアルゴリズムの計算時間測定
start_time = time.time()
# ハンガリアンアルゴリズムの実行
row_ind, col_ind = linear_sum_assignment(cost_matrix)
hungarian_assignments = {student: course_slot //
                         course_capacity for student, course_slot in zip(row_ind, col_ind)}
hungarian_time = time.time() - start_time


# 解の精度の評価
def calculate_accuracy(assignments, preferences):
    satisfied = 0
    for student, assigned_course in assignments.items():
        if assigned_course is not None and assigned_course in preferences[student]:
            satisfied += 1
    return satisfied / len(assignments)


greedy_accuracy = calculate_accuracy(greedy_assignments, students_preferences)
hungarian_accuracy = calculate_accuracy(
    hungarian_assignments, students_preferences)

# 結果の表示
print("Greedy Algorithm")
print("Time: ", greedy_time)
print("Accuracy: ", greedy_accuracy)
print()
print("Hungarian Algorithm")
print("Time: ", hungarian_time)
print("Accuracy: ", hungarian_accuracy)
print()
print("Hungarian Algorithm is {:.2f} times faster than Greedy Algorithm".format(
    greedy_time / hungarian_time))
print("Hungarian Algorithm is {:.2f} times more accurate than Greedy Algorithm".format(
    hungarian_accuracy / greedy_accuracy))
