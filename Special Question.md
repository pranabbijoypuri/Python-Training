# Special Questions

## 🤔 Comparison: list.sort() vs sorted()

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

## 🤔 Inheritence vs composition

## 🤔 Map vs Reduce vs Lamda

| Feature | **Map** | **Reduce** | **Lambda** |
| :--- | :--- | :--- | :--- |
| **What is it?** | A built-in function to transform data. | A function for aggregating/combining data. | An anonymous, one-line "throwaway" function. |
| **Purpose** | Applies a function to **every item** in a list individually. | Reduces a list to a **single value** by applying a rolling computation. | Provides the **logic** for functions like `map` or `reduce` without a full definition. |
| **Output** | A map object (list of the same length as input). | A single value (e.g., a sum, product, or string). | A function object. |
| **Module** | Built-in (no import needed). | Must import from `functools`. | Built-in keyword. |
| **Analogy** | **The Assembly Line:** Every item gets painted a new color. | **The Snowball:** Every flake is packed into one big ball. | **The Quick Instruction:** A post-it note saying "multiply by 2." |
| **Example Code** | `map(lambda x: x*2, [1, 2])` | `reduce(lambda x, y: x+y, [1, 2])` | `lambda x: x + 10` |
| **Result of Ex.** | `[2, 4]` | `3` | *(Returns a function)* |

### ⚙️ Map run sequentially. Here is how you man can make parallely

```from multiprocessing import Pool

def heavy_task(x):
    return x * x

if __name__ == '__main__':
    with Pool(4) as p:  # Uses 4 CPU cores at once
        results = p.map(heavy_task, [1, 2, 3, 4])
    print(results)```
