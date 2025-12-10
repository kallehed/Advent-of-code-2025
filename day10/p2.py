import pulp, numpy as np, sys

# This solution works great!
# Constraints: Ax = b. Minimize 1-norm of x. x is in set N^n (>= 0)
total_presses = 0;
for l in sys.stdin.read().strip().split("\n"):
    to_get_str, r2 = l[1:].split("]")
    buttons_str, r = r2.split("{");
    # turn them into bool-vector, that can be added later
    b = np.array([int(x) for x in r[:-1].split(",")])

    # horrible python list 'comprehension' (incomprehensible)
    buttons_idx = [[int(x) for x in b[1:-1].split(",")] for b in buttons_str.strip().split(" ")];
    buttons_idx.sort(key=len) # sort to be greedy
    buttons_idx.reverse()
    # Ax = b, A: nxm, x:m, b:n
    n = len(b)
    m = len(buttons_idx)
    A = np.zeros((n, m), dtype=int)
    for i in range(n):
        for j in range(m):
            if (i in buttons_idx[j]):
                A[i][j] = 1
    print("A:",A);
    print("b:",b);

    model = pulp.LpProblem("min_l1", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x{j}", lowBound=0, cat="Integer") for j in range(m)]
    model += pulp.lpSum(x)
    for i in range(n):
        model += pulp.lpSum(A[i, j] * x[j] for j in range(m)) == b[i]
    model.solve()

    total_presses += int(pulp.value(model.objective))

print("TOTAL: ", total_presses);
