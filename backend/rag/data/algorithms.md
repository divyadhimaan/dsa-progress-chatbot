# Core Algorithms & Complexity Reference

## Sorting Algorithms

| Algorithm      | Best     | Average  | Worst    | Space   | Stable |
|----------------|----------|----------|----------|---------|--------|
| Bubble Sort    | O(n)     | O(n²)    | O(n²)    | O(1)    | Yes    |
| Selection Sort | O(n²)    | O(n²)    | O(n²)    | O(1)    | No     |
| Insertion Sort | O(n)     | O(n²)    | O(n²)    | O(1)    | Yes    |
| Merge Sort     | O(n log n)| O(n log n)| O(n log n)| O(n) | Yes    |
| Quick Sort     | O(n log n)| O(n log n)| O(n²)   | O(log n)| No     |
| Heap Sort      | O(n log n)| O(n log n)| O(n log n)| O(1) | No     |
| Tim Sort       | O(n)     | O(n log n)| O(n log n)| O(n) | Yes    |
| Counting Sort  | O(n+k)   | O(n+k)   | O(n+k)   | O(k)    | Yes    |
| Radix Sort     | O(nk)    | O(nk)    | O(nk)    | O(n+k)  | Yes    |

**Quick Sort with Lomuto partition:**
```python
def quicksort(arr, low, high):
    if low < high:
        pivot = partition(arr, low, high)
        quicksort(arr, low, pivot - 1)
        quicksort(arr, pivot + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
```

**Merge Sort:**
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
```

**Counting Sort (for integers in range [0, k]):**
```python
def counting_sort(arr, k):
    count = [0] * (k + 1)
    for n in arr:
        count[n] += 1
    result = []
    for val, freq in enumerate(count):
        result.extend([val] * freq)
    return result
# Time: O(n + k), Space: O(k)
```

---

## Graph Algorithms

### Dijkstra's Shortest Path (weighted, non-negative edges)
```python
import heapq

def dijkstra(graph, src, n):
    """
    graph: dict[node] = list of (neighbor, weight)
    Returns: dist[node] = shortest distance from src
    """
    dist = [float('inf')] * n
    dist[src] = 0
    heap = [(0, src)]   # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue    # stale entry
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist
# Time: O((V + E) log V), Space: O(V)
```

### Bellman-Ford (handles negative edges, detects negative cycles)
```python
def bellman_ford(n, edges, src):
    """edges: list of (u, v, weight)"""
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(n - 1):           # relax all edges n-1 times
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Check for negative cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None              # negative cycle exists
    return dist
# Time: O(V * E), Space: O(V)
```

### Floyd-Warshall (all-pairs shortest path)
```python
def floyd_warshall(graph, n):
    """graph[i][j] = weight or inf if no edge"""
    dist = [row[:] for row in graph]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist
# Time: O(V^3), Space: O(V^2)
```

### Kruskal's MST (greedy + Union-Find)
```python
def kruskal(n, edges):
    """edges: list of (weight, u, v), sorted by weight"""
    edges.sort()
    uf = UnionFind(n)   # see patterns.md
    mst_cost, mst_edges = 0, []
    for w, u, v in edges:
        if uf.union(u, v):
            mst_cost += w
            mst_edges.append((u, v, w))
    return mst_cost, mst_edges
# Time: O(E log E), Space: O(V)
```

### Prim's MST (greedy + heap)
```python
def prims(graph, n):
    """graph[u] = list of (v, weight)"""
    visited = [False] * n
    heap = [(0, 0)]   # (cost, node), start at node 0
    total = 0
    while heap:
        cost, u = heapq.heappop(heap)
        if visited[u]: continue
        visited[u] = True
        total += cost
        for v, w in graph[u]:
            if not visited[v]:
                heapq.heappush(heap, (w, v))
    return total
# Time: O(E log V), Space: O(V)
```

---

## Tree Algorithms

### Tree Traversals (iterative)
```python
# Inorder (Left → Root → Right) — gives sorted order for BST
def inorder(root):
    result, stack, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        result.append(cur.val)
        cur = cur.right
    return result

# Level-order (BFS)
from collections import deque
def level_order(root):
    if not root: return []
    queue, result = deque([root]), []
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result

# Morris Traversal (inorder, O(1) space)
def morris_inorder(root):
    result, cur = [], root
    while cur:
        if not cur.left:
            result.append(cur.val); cur = cur.right
        else:
            pre = cur.left
            while pre.right and pre.right != cur:
                pre = pre.right
            if not pre.right:
                pre.right = cur; cur = cur.left
            else:
                pre.right = None; result.append(cur.val); cur = cur.right
    return result
```

### BST Operations
```python
def bst_insert(root, val):
    if not root: return TreeNode(val)
    if val < root.val: root.left  = bst_insert(root.left,  val)
    else:              root.right = bst_insert(root.right, val)
    return root

def bst_delete(root, val):
    if not root: return None
    if val < root.val:
        root.left = bst_delete(root.left, val)
    elif val > root.val:
        root.right = bst_delete(root.right, val)
    else:   # found
        if not root.left:  return root.right
        if not root.right: return root.left
        # Replace with inorder successor (smallest in right subtree)
        successor = root.right
        while successor.left: successor = successor.left
        root.val   = successor.val
        root.right = bst_delete(root.right, successor.val)
    return root

def validate_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root: return True
    if not (lo < root.val < hi): return False
    return (validate_bst(root.left,  lo, root.val) and
            validate_bst(root.right, root.val, hi))
```

### Lowest Common Ancestor (LCA)
```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left  = lca(root.left,  p, q)
    right = lca(root.right, p, q)
    if left and right: return root   # p and q are on different sides
    return left or right
# Time: O(n), Space: O(h) where h = tree height
```

### Diameter of Binary Tree
```python
def diameter(root):
    max_d = [0]
    def height(node):
        if not node: return 0
        l, r = height(node.left), height(node.right)
        max_d[0] = max(max_d[0], l + r)
        return max(l, r) + 1
    height(root)
    return max_d[0]
```

### Serialize / Deserialize Binary Tree
```python
def serialize(root):
    def dfs(node):
        if not node: return ['N']
        return [str(node.val)] + dfs(node.left) + dfs(node.right)
    return ','.join(dfs(root))

def deserialize(data):
    vals = iter(data.split(','))
    def dfs():
        v = next(vals)
        if v == 'N': return None
        node = TreeNode(int(v))
        node.left  = dfs()
        node.right = dfs()
        return node
    return dfs()
```

---

## String Algorithms

### KMP (Knuth-Morris-Pratt) Pattern Matching
```python
def kmp(text, pattern):
    def build_lps(p):
        lps = [0] * len(p)
        length = 0; i = 1
        while i < len(p):
            if p[i] == p[length]:
                length += 1; lps[i] = length; i += 1
            elif length:
                length = lps[length - 1]
            else:
                lps[i] = 0; i += 1
        return lps

    lps = build_lps(pattern)
    i = j = 0
    matches = []
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1; j += 1
        if j == len(pattern):
            matches.append(i - j); j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            j = lps[j - 1] if j else 0; i += (j == 0)
    return matches
# Time: O(n + m), Space: O(m)
```

### Rabin-Karp (rolling hash)
```python
def rabin_karp(text, pattern):
    BASE, MOD = 31, 10**9 + 7
    n, m = len(text), len(pattern)
    if m > n: return []

    def char_val(c): return ord(c) - ord('a') + 1

    high = pow(BASE, m - 1, MOD)
    ph = th = 0
    for i in range(m):
        ph = (ph * BASE + char_val(pattern[i])) % MOD
        th = (th * BASE + char_val(text[i]))    % MOD

    result = []
    for i in range(n - m + 1):
        if ph == th and text[i:i+m] == pattern:   # hash match + verify
            result.append(i)
        if i < n - m:
            th = (th - char_val(text[i]) * high) % MOD
            th = (th * BASE + char_val(text[i + m])) % MOD
    return result
# Time: O(n + m) avg, O(nm) worst
```

### Longest Palindromic Substring (Manacher's O(n))
```python
def longest_palindrome(s):
    # Expand around center — O(n^2) is usually sufficient for interviews
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l+1:r]
    result = ""
    for i in range(len(s)):
        odd  = expand(i, i)
        even = expand(i, i + 1)
        if len(odd)  > len(result): result = odd
        if len(even) > len(result): result = even
    return result
# Time: O(n^2), Space: O(1)
```

---

## Big-O Complexity Cheat Sheet

### Data Structure Operations
| Structure        | Access  | Search  | Insert  | Delete  |
|------------------|---------|---------|---------|---------|
| Array            | O(1)    | O(n)    | O(n)    | O(n)    |
| Stack/Queue      | O(n)    | O(n)    | O(1)    | O(1)    |
| Singly Linked List| O(n)   | O(n)    | O(1)*   | O(1)*   |
| Hash Table       | —       | O(1)**  | O(1)**  | O(1)**  |
| BST (balanced)   | O(log n)| O(log n)| O(log n)| O(log n)|
| Heap (binary)    | O(1)†   | O(n)    | O(log n)| O(log n)|
| Trie             | O(m)    | O(m)    | O(m)    | O(m)    |

*with pointer to node, **amortised, †min/max only

### Graph Algorithm Complexities
| Algorithm         | Time            | Space   |
|-------------------|-----------------|---------|
| BFS / DFS         | O(V + E)        | O(V)    |
| Dijkstra (heap)   | O((V+E) log V)  | O(V)    |
| Bellman-Ford      | O(V · E)        | O(V)    |
| Floyd-Warshall    | O(V³)           | O(V²)   |
| Kruskal           | O(E log E)      | O(V)    |
| Prim (heap)       | O(E log V)      | O(V)    |
| Topological Sort  | O(V + E)        | O(V)    |

---

## Common Bit Manipulation Tricks

```python
# Check if n is a power of 2
is_power_of_two = lambda n: n > 0 and (n & (n - 1)) == 0

# Count set bits (Brian Kernighan)
def count_bits(n):
    count = 0
    while n:
        n &= n - 1   # clears lowest set bit
        count += 1
    return count

# Get / Set / Clear / Flip bit at position i
get   = lambda n, i: (n >> i) & 1
set_b = lambda n, i: n | (1 << i)
clear = lambda n, i: n & ~(1 << i)
flip  = lambda n, i: n ^ (1 << i)

# XOR trick: find single non-duplicate in array where all others appear twice
def single_number(nums):
    result = 0
    for n in nums: result ^= n
    return result

# Find two non-duplicates in an array where all others appear twice
def single_number_ii(nums):
    xor = 0
    for n in nums: xor ^= n
    diff_bit = xor & (-xor)   # isolate rightmost set bit
    a = b = 0
    for n in nums:
        if n & diff_bit: a ^= n
        else:            b ^= n
    return [a, b]

# Reverse bits of a 32-bit integer
def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

---

## Two Classic Hard Problems

### Median of Two Sorted Arrays — Binary Search O(log(min(m,n)))
```python
def find_median_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2
        j = (m + n + 1) // 2 - i
        max_l1 = float('-inf') if i == 0 else nums1[i-1]
        min_r1 = float('inf')  if i == m else nums1[i]
        max_l2 = float('-inf') if j == 0 else nums2[j-1]
        min_r2 = float('inf')  if j == n else nums2[j]
        if max_l1 <= min_r2 and max_l2 <= min_r1:
            if (m + n) % 2 == 1:
                return max(max_l1, max_l2)
            return (max(max_l1, max_l2) + min(min_r1, min_r2)) / 2
        elif max_l1 > min_r2:
            hi = i - 1
        else:
            lo = i + 1
```

### Trapping Rain Water — Two Pointers O(n)
```python
def trap(height):
    left, right = 0, len(height) - 1
    max_l = max_r = water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= max_l: max_l = height[left]
            else: water += max_l - height[left]
            left += 1
        else:
            if height[right] >= max_r: max_r = height[right]
            else: water += max_r - height[right]
            right -= 1
    return water
# Time: O(n), Space: O(1)
```

---

## System Design Fundamentals (SDE-2 / SDE-3)

### CAP Theorem
A distributed system can guarantee at most 2 of 3: **Consistency** (every read gets the latest write), **Availability** (every request gets a response), **Partition Tolerance** (system works despite network splits). Since partitions are unavoidable in practice, choose CP (e.g. HBase, ZooKeeper) or AP (e.g. Cassandra, DynamoDB).

### Rate Limiting Algorithms
- **Token Bucket**: refill tokens at rate r, burst up to capacity c. Allows short bursts. Good for APIs.
- **Leaky Bucket**: requests drain at fixed rate. Smooths traffic. Good for output shaping.
- **Fixed Window Counter**: count requests per window (e.g. per minute). Simple but edge-case spike at window boundary.
- **Sliding Window Log**: keep timestamps of each request. Accurate but memory-intensive.
- **Sliding Window Counter**: blend of fixed window accuracy with lower memory. Most common in production.

### Caching Strategies
- **Cache-aside (Lazy)**: app reads cache first, on miss reads DB and writes to cache. Most common. Risk: cold start.
- **Write-through**: write to cache and DB synchronously. Always consistent, write latency doubles.
- **Write-behind (Write-back)**: write to cache, async to DB. Fast writes, risk of data loss.
- **Read-through**: cache sits in front of DB, auto-populates on miss. Transparent to app.

**Eviction policies**: LRU (most common), LFU (frequency-based), FIFO, TTL-based.

### Database Sharding
Horizontal partitioning of data across multiple nodes. Shard key choice is critical.
- **Range sharding**: simple, but can cause hotspots.
- **Hash sharding**: even distribution, but hard to range query.
- **Directory sharding**: flexible lookup table, but single point of failure.

**Consistent hashing** (used in Cassandra, DynamoDB): nodes and keys mapped to a ring. Adding/removing a node only remaps ~1/n keys. Supports virtual nodes for better load balance.

### Common Interview System Design Questions
- Design URL shortener: base62 encoding, KV store (Redis/DynamoDB), CDN for redirects
- Design Twitter timeline: fanout-on-write vs fanout-on-read, celebrity problem
- Design distributed rate limiter: Redis with sliding window counter + Lua scripts
- Design file storage (Dropbox/S3): chunking, deduplication, metadata service, CDN
- Design ride-sharing (Uber/Lyft): geospatial indexing (geohash/quadtree), real-time location tracking, matching
- Design notification system: event queue (Kafka), delivery workers per channel (push/email/SMS), retry with exponential backoff

### Back-of-Envelope Estimates
| Metric | Value |
|--------|-------|
| SSD sequential read | ~500 MB/s |
| Network (1Gbps) | ~125 MB/s |
| RAM read | ~10 GB/s |
| 1M ops/sec Redis | needs ~1 CPU core |
| Average webpage | ~2 MB |
| 100M DAU × 10 req/day | ~12,000 req/s peak |
