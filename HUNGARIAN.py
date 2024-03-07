# ハンガリアンアルゴリズムの実装
def reduce_rows(matrix):
    for i in range(len(matrix)):
        min_val = min(matrix[i])
        for j in range(len(matrix[i])):
            matrix[i][j] -= min_val


def reduce_cols(matrix):
    for j in range(len(matrix[0])):
        col = [matrix[i][j] for i in range(len(matrix))]
        min_val = min(col)
        for i in range(len(matrix)):
            matrix[i][j] -= min_val


def cover_zeros(matrix):
    covered_rows = set()
    covered_cols = set()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0 and i not in covered_rows and j not in covered_cols:
                covered_rows.add(i)
                covered_cols.add(j)
    return covered_rows, covered_cols


def create_additional_zeros(matrix, covered_rows, covered_cols):
    uncovered_values = [matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix[i]))
                        if i not in covered_rows and j not in covered_cols]
    min_val = min(uncovered_values) if uncovered_values else 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if i not in covered_rows and j not in covered_cols:
                matrix[i][j] -= min_val
            elif i in covered_rows and j in covered_cols:
                matrix[i][j] += min_val


def hungarian_algorithm(cost_matrix):
    matrix = [row[:] for row in cost_matrix]  # コスト行列のコピーを作成
    reduce_rows(matrix)
    reduce_cols(matrix)

    while True:
        covered_rows, covered_cols = cover_zeros(matrix)
        if len(covered_rows) + len(covered_cols) == len(matrix):
            break
        create_additional_zeros(matrix, covered_rows, covered_cols)

    # マッチングの作成 (ここでは簡単な実装を行います)
    matches = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                matches.append((i, j))
                break  # 1つの行に対して1つのマッチングのみを許可
    return matches


# サンプルデータ
cost_matrix = [
    [3, 8, 9, 1, 6],
    [1, 4, 1, 5, 5],
    [7, 2, 7, 9, 2],
    [3, 1, 6, 8, 8],
    [2, 6, 3, 6, 2]
]

# ハンガリアンアルゴリズムを使用して最適なマッチングを計算
matches = hungarian_algorithm(cost_matrix)

# 結果の表示
for match in matches:
    print(f"S{match[0] + 1} は T{match[1] + 1} にマッチング")
