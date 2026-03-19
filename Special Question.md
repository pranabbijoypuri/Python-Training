# 🤔 Comparison: list.sort() vs sorted()

| Feature | `list.sort()` | `sorted(iterable)` |
| :--- | :--- | :--- |
| **Type** | Method of the list class | Built-in Python function |
| **Modification** | **In-place**: Modifies the original list | **New Object**: Leaves original unchanged |
| **Return Value** | Returns `None` | Returns a **new sorted list** |
| **List Support** | Supported | Supported |
| **Tuple Support** | **Not supported** (Tuples are immutable) | Supported (Returns a new sorted list) |
| **Dict Support** | **Not supported** | Supported (Returns sorted list of **keys**) |
| **Performance** | Slightly faster (no copy made) | Slightly slower (requires extra memory) |
| **Use Case** | Use when you don't need the original order | Use when you need to keep the original data |
