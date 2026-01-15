In this article we want to build a fast, array-based **data structure** that supports:

- **Range add**: add a value `v` to every element in a contiguous interval `[l, r]`.
- **Range sum**: query the sum of all the elements inside a contiguous interval `[l, r]`.

The implementation is **iterative / bottom-up**, storing nodes in linear arrays, and uses **immediate per-node additions** that represent a *per-element* increment for that node’s whole segment. The code is designed for clarity and speed in competitive programming use.

The advantages of this implementation are that it is relatively quick to implement and also provides the speed of writing an iterative array-based segment tree with minimal memory manipulation. This data structure has been tested across several problems and has been proven to pass most time constraints where the traditional recursive node-based segment tree even with lazy propagation fails.

The complete implementation of this data structure can be found here: [github.com/BooleanCube/hackpack](https://github.com/BooleanCube/hackpack/blob/main/content/data-structures/FastLazy.h)

---

# Storage

![storage](https://i.imgur.com/RkrUov4.gif)

The structure stores data in contiguous arrays (vectors):

* `n` — number of elements in the array (constructor parameter).
* `tree` — a vector of length `2*n` that holds the **segment sums** (one entry per node). Node indices used are `1 .. 2*n-1`. Index `0` is unused.
* `lazy` — a vector of length `2*n` that stores **per-element pending additions** for the node’s whole segment. (`lazy[idx]` means “add this value to every element in `rng[idx]` when/if children are visited”.)
* `rng` — a `vector<pair<int,int>>` of length `2*n` mapping `idx -> [L, R]` (inclusive, array indices) for the node `idx`. This lets us compute segment length quickly: `len = R - L + 1`.
* `vt` alias — `using vt = vector<T>;` for convenience.

**Indexing rule (bottom-up layout):**

* Leaves are at indices `n .. 2*n-1`, and leaf `idx = n + i` maps to array element `i` (0-indexed).
* Internal nodes are `1 .. n-1`.
* Root is index `1`.

This design avoids recursion during updates/queries and is friendly to iterative algorithms.

---

# Construction

![construction](https://i.imgur.com/5MV42gM.gif)

The constructor must:

1. allocate `tree`, `lazy`, and `rng` vectors,
2. fill `rng` for all node indices so we can compute node lengths and map nodes back to array indices.

A safe and simple `rng` construction is recursive, starting at the root index `1`. For node `idx`:

* If `idx >= n` → it's a leaf; `rng[idx] = {idx - n, idx - n}`.
* Else → recursively build children and set `rng[idx] = { rng[left].first, rng[right].second }`.

**Corrected constructor & `_construct` snippet**

```cpp
template <class T>
struct segtree {
    using vt = vector<T>;
    const int n;
    constexpr static T def = 0;
    vt tree, lazy;
    vector<pair<int,int>> rng;

    segtree(int N) : n(N) {
        tree = vt(n<<1, def);
        lazy = vt(n<<1, def);
        rng  = vector<pair<int,int>>(n<<1);
        _construct(1);                     // fill rng[1..2*n-1]
    }

    pair<int,int> _construct(int idx) {
        if (idx >= n) return rng[idx] = { idx - n, idx - n };
        auto L = _construct(idx << 1);
        auto R = _construct((idx << 1) + 1);
        return rng[idx] = { L.first, R.second };
    }

    // ... rest of implementation follows ...
};
```

Notes:

* The implementation works for any `n >= 1` — `rng` stores exact ranges even when `n` is not a power of two.
* `tree` and `lazy` are initialized with `def` (0 for sums).

---

# Range update (how it works)

![range-update](https://i.imgur.com/zLFFfIa.gif)

**Public API:** `update(l, r, val)` with `0 <= l <= r < n`. Internally we transform to node indices `l += n; r += n;` and run `_incUpdate(l, r, val)`.

**High-level idea (bottom-up / iterative covering):**

* We pick a minimal set of whole nodes whose segments exactly cover the update interval `[l, r]` using the standard iterative segment-tree trick:

  * If `l` is a right child, we take node `l`.
  * If `r` is a left child, we take node `r`.
  * Then shift `l` and `r` to their parents (`l >>= 1; r >>= 1`) and repeat until they meet.
* For each chosen node `idx`:

  1. we apply the *total* addition to `tree[idx]` and *also* add that total to all ancestors so `tree` remains consistent; and
  2. we record the per-element lazy increment in `lazy[idx]` so that descendants (if read later) can compute ancestor contributions.

This two-step approach avoids eagerly pushing lazies down; it keeps `tree` consistent by updating ancestor totals, while `lazy` retains the information required to reconstruct ancestor contributions for partial queries.

**Important fix (avoid undefined behavior):** do **not** write `lazy[l++] = op(lazy[l], val);` — that uses `l` twice with side effects and is undefined in C++. Increment/decrement must be separate statements.

**Core update routines (corrected)**:

```cpp
void update(int l, int r, T val) { _incUpdate(l + n, r + n, val); }

void _incUpdate(int l, int r, T val) {
    for (; l < r; l >>= 1, r >>= 1) {
        if (l & 1) {
            _updateLazy(l, val);
            lazy[l] = op(lazy[l], val);   // safe: update lazy first, then advance
            ++l;
        }
        if (l == r) break;
        if (!(r & 1)) {
            _updateLazy(r, val);
            lazy[r] = op(lazy[r], val);
            --r;
        }
    }
    // final node (when l == r)
    _updateLazy(l, val);
    lazy[l] = op(lazy[l], val);
}

void _updateLazy(int idx, T val) {
    // convert per-element val to total for node idx,
    // then add that total into tree[idx] and all ancestors
    T total = value(idx, val); // val * node_length
    for (; idx; idx >>= 1) tree[idx] = op(tree[idx], total);
}
```

**Why update ancestors?**
Because `lazy[idx]` records a per-element increment for `idx` so we don't push it to children. But queries that use ancestor nodes must see the node sums updated. By adding the `total` to `tree[idx]` and all ancestors, we keep `tree[parent]` consistent.

**`value(idx, val)`** converts a per-element increment `val` into the total sum over the node:

```cpp
T value(int idx, T val) { return val * (rng[idx].second - rng[idx].first + 1); }
```

---

# Range query (how it works)

![range-query](https://i.imgur.com/gRpsJXP.gif)

**Public API:** `query(l, r)` with `0 <= l <= r < n`. Internally `l += n; r += n;` and we run `_queryTree(l, r)`.

**High-level idea:**

* As with updates, iterate bottom-up picking the minimal nodes that cover `[l, r]`.
* For each chosen node `idx`, the sum contribution is:

  * `tree[idx]` (which already contains updates applied *at* that node), **plus**
  * contributions from **ancestor** `lazy` values that apply to `idx` but were never pushed down to `idx` (those are collected with `_climbLazy` and converted to totals with `value`).

**Why climb ancestors?**
`_updateLazy` updates `tree` for the node’s total but *does not* push that node’s `lazy` value down to children. If we visit a descendant node later, its `tree[desc]` will **not** include lazy values from its ancestors. `_climbLazy(desc)` aggregates `lazy` values from all ancestors so we can add their effect for the descendant node.

**Core query routines**

```cpp
T query(int l, int r) { return _queryTree(l + n, r + n); }

T _queryTree(int l, int r, T t = def) {
    for (; l < r; l >>= 1, r >>= 1) {
        if (l & 1) {
            t = op(t, value(l, _climbLazy(l)), tree[l]);
            ++l;
        }
        if (l == r) break;
        if (!(r & 1)) {
            t = op(t, value(r, _climbLazy(r)), tree[r]);
            --r;
        }
    }
    return op(t, value(l, _climbLazy(l)), tree[l]);
}

T _climbLazy(int idx, T cnt = def) {
    for (idx >>= 1; idx; idx >>= 1) cnt = op(cnt, lazy[idx]);
    return cnt;
}
```

* `tree[idx]` already includes contributions from updates that were targeted at node `idx` directly.
* `value(idx, _climbLazy(idx))` computes totals produced by lazies on **ancestors** of `idx`.
* `op(a,b,c)` is provided as `a + (b + c)` (i.e., sum combination).

---

## API interface

Public methods and how to use them:

```cpp
segtree<int64_t> st(n);     // create segment tree for n elements (all zeros initially)
st.update(l, r, val);       // add `val` to every element in [l, r] (inclusive), 0-indexed
auto s = st.query(l, r);    // returns the sum of elements in [l, r] (inclusive)
```

Details & contracts:

* Inputs `l` and `r` are **inclusive** and **0-indexed**.
* `T` must support `+`, `*` with `int` lengths (or equivalent) and a zero default (`def`) — commonly `long long` is used for sums.
* `update` and `query` expect `0 <= l <= r < n`.
* `tree` and `lazy` are internal; do not modify them externally.

---

## Time and space complexity

**Space:** `O(n)` memory using arrays of size `2*n`:

* `tree` length `2*n`
* `lazy` length `2*n`
* `rng` length `2*n`

**Time per operation (practical / average):**

* Each `update` or `query` visits `O(log n)` nodes (the set of nodes partitioning the interval).
* However, this implementation performs an **ancestor walk** (`_updateLazy` or `_climbLazy`) for each visited node:

  * `_updateLazy` updates all ancestors (an `O(log n)` walk) whenever a chosen node is updated, and
  * `_climbLazy` walks upward to aggregate lazies for each visited node in a query (another `O(log n)` each).
* Therefore **worst-case** time per update or query can be `O((log n)^2)` in the current code.

**How to get strict `O(log n)` worst-case:**

* Use an iterative **push/pull** approach:

  * `push` lazies down along the path from root to the two target leaves before performing your operation, so per-node `_climbLazy` becomes unnecessary.
  * After modifying leaves, `pull` (recompute) parents upward once.
* That pattern is a standard iterative lazy tree optimization and yields `O(log n)` worst-case per operation. If you want, I can produce that optimized implementation.
* Downside to this approach is that it takes significantly more time to implement when not needed.

---

# Usage examples

![complexity](https://i.imgur.com/ZtMZzyk.gif)

Below are simple examples and expected results.

**Example 1 — small walkthrough**

```cpp
// Create tree over n = 8 elements, all initially 0
segtree<long long> st(8);

// Add 3 to indices [2, 5]
st.update(2, 5, 3);

// Queries:
auto total = st.query(0, 7); // sum over entire array
auto partial = st.query(2, 3);

// Expected values:
// indices 2,3,4,5 each increased by 3 -> 4 elements * 3 = 12
// total == 12
// partial (2..3) == 3 + 3 = 6
```

**Example 2 — sequence of updates**

```cpp
segtree<long long> st(6);
st.update(0, 2, 5);   // array: [5,5,5,0,0,0]
st.update(1, 4, 2);   // array: [5,7,7,2,2,0]

st.query(0, 5); // expected 5 + 7 + 7 + 2 + 2 + 0 = 23
st.query(2, 3); // expected 7 + 2 = 9
```

---

## Notes, caveats & suggestions

* **Undefined behavior fix:** the original compact form used `lazy[l++] = op(lazy[l], val);` — that’s undefined in C++ and must be split into separate operations (`lazy[l] = op(...); ++l;`).
* **Type `T` constraints:** `T` must behave like a numeric type supporting `+` and `*` by integer lengths. Use `long long` (or `int64_t`) if sums could be large.
* **Performance tradeoff:** the current code is clear and compact, and in many practical cases it runs fast; for guaranteed worst-case `O(log n)` operations, the iterative push/pull pattern is preferred.
* **Intervals:** the code uses inclusive intervals `[l, r]` (common for competitive programming). If you prefer half-open `[l, r)` semantics, the interface and some loop conditions simplify; I can convert it on request.
* **Testing:** test edge cases (small `n` like `n=1`, updates where `l==r`, and non-power-of-two `n`) — this implementation’s `rng` logic handles non-power-of-two `n` correctly.


