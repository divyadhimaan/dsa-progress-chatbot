# DSA Interview Patterns

## Sliding Window

The sliding window pattern maintains a contiguous subarray or substring as a "window" and slides it across the input. Use it when the problem asks for the longest, shortest, or best subarray/substring satisfying some condition.

**When to use:** Maximum subarray of size k, longest substring without repeating characters, smallest subarray with sum ≥ S, longest substring with at most K distinct characters, string anagram/permutation presence.

**Fixed-size window template:**
```python
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
# Time: O(n), Space: O(1)
```

**Dynamic window template (shrink when condition violated):**
```python
def longest_substring_k_distinct(s, k):
    char_count = {}
    left = max_len = 0
    for right, ch in enumerate(s):
        char_count[ch] = char_count.get(ch, 0) + 1
        while len(char_count) > k:
            left_ch = s[left]
            char_count[left_ch] -= 1
            if char_count[left_ch] == 0:
                del char_count[left_ch]
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len
# Time: O(n), Space: O(k)
```

**Key insight:** Expand right pointer freely; shrink left pointer only when the window becomes invalid.

---

## Two Pointers

Two pointers work on sorted arrays or linked lists. One pointer starts at the beginning, one at the end, and they move toward each other (or in the same direction for fast/slow variants).

**When to use:** Pair with target sum in sorted array, remove duplicates from sorted array, squaring a sorted array, triplet sum, Dutch National Flag (sort colors), comparing strings with backspaces.

**Opposite-direction template:**
```python
def pair_with_target_sum(arr, target):
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []
# Time: O(n), Space: O(1)
```

**Three Sum (extend two pointers):**
```python
def three_sum(arr):
    arr.sort()
    result = []
    for i in range(len(arr) - 2):
        if i > 0 and arr[i] == arr[i-1]:
            continue   # skip duplicates
        left, right = i + 1, len(arr) - 1
        while left < right:
            s = arr[i] + arr[left] + arr[right]
            if s == 0:
                result.append([arr[i], arr[left], arr[right]])
                while left < right and arr[left] == arr[left+1]: left += 1
                while left < right and arr[right] == arr[right-1]: right -= 1
                left += 1; right -= 1
            elif s < 0: left += 1
            else: right -= 1
    return result
# Time: O(n^2), Space: O(n) for output
```

---

## Fast & Slow Pointers (Floyd's Tortoise and Hare)

The fast pointer moves 2 steps, slow moves 1. Used to detect cycles in linked lists and arrays.

**When to use:** Linked list cycle detection, find cycle start, find middle of linked list, find duplicate in array where values are in range [1,n], happy number.

**Cycle detection:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
# Time: O(n), Space: O(1)

def find_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    # Reset one pointer to head
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    return slow  # cycle start
```

**Find middle of linked list:**
```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # middle node (left-middle for even length)
```

---

## Merge Intervals

Sort intervals by start time, then merge overlapping ones.

**When to use:** Merge overlapping intervals, insert interval, interval intersection, minimum meeting rooms, task scheduler.

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:              # overlap
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
# Time: O(n log n), Space: O(n)
```

**Minimum meeting rooms (use heap):**
```python
import heapq
def min_meeting_rooms(intervals):
    intervals.sort(key=lambda x: x[0])
    heap = []  # stores end times of active meetings
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)
        else:
            heapq.heappush(heap, end)
    return len(heap)
# Time: O(n log n), Space: O(n)
```

---

## Binary Search Variants

Beyond basic binary search: find first/last occurrence, search in rotated array, find peak element.

**Universal template (find leftmost position where condition is true):**
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2   # avoids overflow
        if arr[mid] == target:
            result = mid
            right = mid - 1  # or left = mid + 1 for rightmost
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result
```

**Search in rotated sorted array:**
```python
def search_rotated(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[left] <= arr[mid]:           # left half sorted
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:                               # right half sorted
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
# Time: O(log n), Space: O(1)
```

---

## BFS (Breadth-First Search)

BFS explores layer by layer using a queue. Always finds shortest path in unweighted graphs.

**When to use:** Shortest path in unweighted graph/grid, level-order tree traversal, word ladder, rotting oranges, 0-1 matrix distances, bipartite check.

**Graph BFS template:**
```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    distance = {start: 0}
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance
# Time: O(V + E), Space: O(V)
```

**Grid BFS (4-directional):**
```python
def bfs_grid(grid, start_r, start_c):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start_r, start_c, 0)])  # row, col, steps
    visited = {(start_r, start_c)}
    dirs = [(0,1),(0,-1),(1,0),(-1,0)]
    while queue:
        r, c, steps = queue.popleft()
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid[nr][nc] != '#':   # passable cell
                    visited.add((nr, nc))
                    queue.append((nr, nc, steps + 1))
```

---

## DFS (Depth-First Search)

DFS uses recursion or an explicit stack. Best for exhaustive search, connectivity, and tree/graph structure problems.

**When to use:** Number of islands, path sum in tree, all paths, generate permutations/combinations/subsets, detect cycle in directed graph, topological sort, clone graph.

**Recursive DFS on graph:**
```python
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

**Number of islands:**
```python
def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    def sink(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'   # mark visited by sinking
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            sink(r+dr, c+dc)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                sink(r, c)
                count += 1
    return count
# Time: O(m*n), Space: O(m*n) stack
```

---

## Backtracking

Backtracking builds a solution incrementally and abandons a branch as soon as it violates constraints. Always think: make choice → recurse → undo choice.

**Template:**
```python
def backtrack(state, choices, result):
    if is_complete(state):
        result.append(list(state))
        return
    for choice in choices:
        if is_valid(state, choice):
            state.append(choice)       # make
            backtrack(state, next_choices(state, choices), result)
            state.pop()                # undo
```

**Subsets (power set):**
```python
def subsets(nums):
    result, subset = [], []
    def dfs(start):
        result.append(list(subset))
        for i in range(start, len(nums)):
            subset.append(nums[i])
            dfs(i + 1)
            subset.pop()
    dfs(0)
    return result
# Time: O(2^n * n), Space: O(n)
```

**Permutations:**
```python
def permute(nums):
    result = []
    def dfs(current, remaining):
        if not remaining:
            result.append(list(current))
            return
        for i, num in enumerate(remaining):
            dfs(current + [num], remaining[:i] + remaining[i+1:])
    dfs([], nums)
    return result
# Time: O(n! * n), Space: O(n)
```

**N-Queens pruning with sets:**
```python
def solve_n_queens(n):
    cols, diag1, diag2, result, board = set(), set(), set(), [], [['.']*n for _ in range(n)]
    def dfs(r):
        if r == n:
            result.append(["".join(row) for row in board])
            return
        for c in range(n):
            if c in cols or (r-c) in diag1 or (r+c) in diag2:
                continue
            board[r][c] = 'Q'; cols.add(c); diag1.add(r-c); diag2.add(r+c)
            dfs(r + 1)
            board[r][c] = '.'; cols.discard(c); diag1.discard(r-c); diag2.discard(r+c)
    dfs(0)
    return result
```

---

## Dynamic Programming Patterns

### 0/1 Knapsack
Each item can be used at most once. Classic DP on items × capacity.

```python
def knapsack_01(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]                            # skip item
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
    return dp[n][capacity]
# Time: O(n * capacity), Space: O(n * capacity) → optimise to O(capacity) with 1D DP
```

**Space-optimised (iterate capacity in reverse):**
```python
def knapsack_01_opt(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):   # reverse to avoid reuse
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]
```

### Unbounded Knapsack / Coin Change
Items can be reused unlimited times.

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for a in range(coin, amount + 1):       # forward = allow reuse
            dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
# Time: O(amount * len(coins)), Space: O(amount)
```

### Longest Common Subsequence (LCS)
```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
# Time: O(m*n), Space: O(m*n)
```

### Longest Increasing Subsequence (LIS)
```python
# O(n^2) DP
def lis_dp(nums):
    dp = [1] * len(nums)
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# O(n log n) with patience sorting + binary search
import bisect
def lis_nlogn(nums):
    tails = []
    for n in nums:
        pos = bisect.bisect_left(tails, n)
        if pos == len(tails): tails.append(n)
        else: tails[pos] = n
    return len(tails)
```

### Edit Distance
```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[:]
        dp[0] = i
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[j] = prev[j-1]
            else:
                dp[j] = 1 + min(prev[j], dp[j-1], prev[j-1])
    return dp[n]
# Time: O(m*n), Space: O(n)
```

---

## Heap / Priority Queue Patterns

### Top K Elements
```python
import heapq

def top_k_frequent(nums, k):
    freq = {}
    for n in nums:
        freq[n] = freq.get(n, 0) + 1
    # min-heap of size k
    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for _, num in heap]
# Time: O(n log k), Space: O(n)
```

### Kth Largest Element
```python
def find_kth_largest(nums, k):
    # min-heap of size k → top is kth largest
    heap = nums[:k]
    heapq.heapify(heap)
    for n in nums[k:]:
        if n > heap[0]:
            heapq.heapreplace(heap, n)
    return heap[0]
# Time: O(n log k), Space: O(k)
```

### Merge K Sorted Lists
```python
def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = cur = ListNode(0)
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node; cur = cur.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
# Time: O(n log k), Space: O(k)
```

---

## Monotonic Stack

A stack that is kept strictly increasing or decreasing. Used to find the next/previous greater/smaller element in O(n).

```python
def next_greater_element(nums):
    result = [-1] * len(nums)
    stack = []  # stores indices, stack values are decreasing
    for i, n in enumerate(nums):
        while stack and nums[stack[-1]] < n:
            result[stack.pop()] = n
        stack.append(i)
    return result
# Time: O(n), Space: O(n)
```

**Largest rectangle in histogram:**
```python
def largest_rectangle(heights):
    stack, max_area = [], 0
    for i, h in enumerate(heights + [0]):   # sentinel 0 to flush stack
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area
# Time: O(n), Space: O(n)
```

---

## Union-Find (Disjoint Set Union)

Used for dynamic connectivity problems: group nodes into components, detect cycles in undirected graphs, count connected components.

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank   = [0] * n
        self.count  = n     # number of components

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False   # already connected
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.count -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
# find/union: O(α(n)) ≈ O(1) amortised
```

---

## Trie (Prefix Tree)

Efficient for prefix lookups, autocomplete, and word search.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end   = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children: return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children: return False
            node = node.children[ch]
        return True
# insert/search/starts_with: O(m) where m = word length
```

---

## Topological Sort

For DAGs: find a valid ordering of nodes such that every edge u→v has u before v. Two approaches: Kahn's algorithm (BFS with in-degree) and DFS post-order.

**Kahn's Algorithm (BFS):**
```python
from collections import deque

def topo_sort_kahn(num_nodes, edges):
    graph    = [[] for _ in range(num_nodes)]
    in_degree = [0] * num_nodes
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque(n for n in range(num_nodes) if in_degree[n] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            in_degree[nei] -= 1
            if in_degree[nei] == 0:
                queue.append(nei)
    return order if len(order) == num_nodes else []   # empty = cycle detected
# Time: O(V + E), Space: O(V + E)
```

**Cycle detection in directed graph (DFS with 3 colours):**
```python
def has_cycle_directed(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    # 0=unvisited, 1=in-stack, 2=done
    color = [0] * n
    def dfs(node):
        color[node] = 1
        for nei in graph[node]:
            if color[nei] == 1: return True   # back edge = cycle
            if color[nei] == 0 and dfs(nei): return True
        color[node] = 2
        return False
    return any(color[i] == 0 and dfs(i) for i in range(n))
```
