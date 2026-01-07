"""
Sorting Algorithm Visualizer - Algorithm complexity visualization
Visualize different sorting algorithms with step-by-step animation
"""
import streamlit as st
from typing import List, Tuple, Generator
import random
import time

def render_sorting_visualizer(learn_mode: bool = True):
    """Main render function for Sorting Visualizer"""
    
    st.header("📊 Sorting Algorithm Visualizer")
    st.markdown("""
    **Goal:** Watch different sorting algorithms in action and understand their complexity!
    
    Compare algorithms side-by-side and see how they perform on different data.
    """)
    
    # Initialize state
    if 'sort_array' not in st.session_state:
        st.session_state.sort_array = generate_array(20)
    if 'sort_steps' not in st.session_state:
        st.session_state.sort_steps = []
    if 'sort_current_step' not in st.session_state:
        st.session_state.sort_current_step = 0
    if 'sort_comparisons' not in st.session_state:
        st.session_state.sort_comparisons = 0
    if 'sort_swaps' not in st.session_state:
        st.session_state.sort_swaps = 0
    if 'sort_algorithm' not in st.session_state:
        st.session_state.sort_algorithm = "Bubble Sort"
    
    # Configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        array_size = st.slider("Array Size", 5, 50, 20)
    
    with col2:
        data_type = st.selectbox("Data Pattern", [
            "Random",
            "Nearly Sorted",
            "Reversed",
            "Few Unique"
        ])
    
    with col3:
        if st.button("🔄 Generate New Array", use_container_width=True):
            st.session_state.sort_array = generate_array(array_size, data_type)
            st.session_state.sort_steps = []
            st.session_state.sort_current_step = 0
            st.session_state.sort_comparisons = 0
            st.session_state.sort_swaps = 0
            st.rerun()
    
    st.markdown("---")
    
    # Algorithm selection
    algorithms = {
        "Bubble Sort": ("O(n²)", "O(1)", bubble_sort_steps),
        "Selection Sort": ("O(n²)", "O(1)", selection_sort_steps),
        "Insertion Sort": ("O(n²)", "O(1)", insertion_sort_steps),
        "Merge Sort": ("O(n log n)", "O(n)", merge_sort_steps),
        "Quick Sort": ("O(n log n)*", "O(log n)", quick_sort_steps),
    }
    
    selected_algo = st.selectbox(
        "Choose Algorithm",
        list(algorithms.keys()),
        index=list(algorithms.keys()).index(st.session_state.sort_algorithm)
    )
    st.session_state.sort_algorithm = selected_algo
    
    time_complexity, space_complexity, sort_func = algorithms[selected_algo]
    
    # Complexity info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Time Complexity", time_complexity)
    with col2:
        st.metric("Space Complexity", space_complexity)
    with col3:
        st.metric("Array Size", len(st.session_state.sort_array))
    
    st.markdown("---")
    
    # Visualization
    st.subheader("📈 Array Visualization")
    
    arr = st.session_state.sort_array
    if st.session_state.sort_steps and st.session_state.sort_current_step < len(st.session_state.sort_steps):
        step = st.session_state.sort_steps[st.session_state.sort_current_step]
        arr = step['array']
        comparing = step.get('comparing', [])
        swapping = step.get('swapping', [])
        sorted_indices = step.get('sorted', [])
    else:
        comparing = []
        swapping = []
        sorted_indices = []
    
    render_array_bars(arr, comparing, swapping, sorted_indices)
    
    # Legend
    st.markdown("""
    <small>🟦 Normal | 🟨 Comparing | 🟥 Swapping | 🟩 Sorted</small>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Start Sorting", use_container_width=True):
            original = st.session_state.sort_array[:]
            steps = list(sort_func(original))
            st.session_state.sort_steps = steps
            st.session_state.sort_current_step = 0
            
            # Count operations
            comparisons = sum(1 for s in steps if s.get('comparing'))
            swaps = sum(1 for s in steps if s.get('swapping'))
            st.session_state.sort_comparisons = comparisons
            st.session_state.sort_swaps = swaps
            st.rerun()
    
    with col2:
        if st.button("⏮️ Previous", disabled=not st.session_state.sort_steps or st.session_state.sort_current_step == 0):
            st.session_state.sort_current_step -= 1
            st.rerun()
    
    with col3:
        if st.button("⏭️ Next", disabled=not st.session_state.sort_steps or 
                     st.session_state.sort_current_step >= len(st.session_state.sort_steps) - 1):
            st.session_state.sort_current_step += 1
            st.rerun()
    
    with col4:
        if st.button("⏩ Skip to End", disabled=not st.session_state.sort_steps):
            st.session_state.sort_current_step = len(st.session_state.sort_steps) - 1
            st.rerun()
    
    # Progress
    if st.session_state.sort_steps:
        progress = (st.session_state.sort_current_step + 1) / len(st.session_state.sort_steps)
        st.progress(progress)
        st.caption(f"Step {st.session_state.sort_current_step + 1} of {len(st.session_state.sort_steps)}")
    
    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Comparisons", st.session_state.sort_comparisons)
    with col2:
        st.metric("Swaps/Operations", st.session_state.sort_swaps)
    
    # Learn mode
    if learn_mode:
        st.markdown("---")
        st.subheader("🎓 Algorithm Details")
        
        tab1, tab2, tab3 = st.tabs(["📝 Pseudocode", "📊 Comparison", "🧠 Explanation"])
        
        with tab1:
            render_pseudocode(selected_algo)
        
        with tab2:
            render_algorithm_comparison()
        
        with tab3:
            render_algorithm_explanation(selected_algo)

def generate_array(size: int, pattern: str = "Random") -> List[int]:
    """Generate array with specified pattern"""
    if pattern == "Random":
        return [random.randint(1, 100) for _ in range(size)]
    elif pattern == "Nearly Sorted":
        arr = list(range(1, size + 1))
        # Swap a few random pairs
        for _ in range(size // 10 + 1):
            i, j = random.sample(range(size), 2)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif pattern == "Reversed":
        return list(range(size, 0, -1))
    elif pattern == "Few Unique":
        return [random.choice([10, 30, 50, 70, 90]) for _ in range(size)]
    return [random.randint(1, 100) for _ in range(size)]

def render_array_bars(arr: List[int], comparing: List[int] = None, 
                      swapping: List[int] = None, sorted_indices: List[int] = None):
    """Render array as vertical bars using Streamlit"""
    comparing = comparing or []
    swapping = swapping or []
    sorted_indices = sorted_indices or []
    
    max_val = max(arr) if arr else 1
    
    # Create bar chart representation
    bar_html = '<div style="display: flex; align-items: end; height: 200px; gap: 2px;">'
    
    for i, val in enumerate(arr):
        height = int((val / max_val) * 180)
        
        if i in swapping:
            color = "#e74c3c"  # Red
        elif i in comparing:
            color = "#f1c40f"  # Yellow
        elif i in sorted_indices:
            color = "#27ae60"  # Green
        else:
            color = "#3498db"  # Blue
        
        bar_html += f'''
        <div style="
            width: {max(100 // len(arr), 8)}px;
            height: {height}px;
            background-color: {color};
            border-radius: 2px 2px 0 0;
        " title="{val}"></div>
        '''
    
    bar_html += '</div>'
    st.markdown(bar_html, unsafe_allow_html=True)

def bubble_sort_steps(arr: List[int]) -> Generator:
    """Bubble sort with step tracking"""
    arr = arr[:]
    n = len(arr)
    sorted_indices = []
    
    for i in range(n):
        for j in range(0, n - i - 1):
            yield {'array': arr[:], 'comparing': [j, j + 1], 'sorted': sorted_indices[:]}
            
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield {'array': arr[:], 'swapping': [j, j + 1], 'sorted': sorted_indices[:]}
        
        sorted_indices.append(n - i - 1)
    
    yield {'array': arr[:], 'sorted': list(range(n))}

def selection_sort_steps(arr: List[int]) -> Generator:
    """Selection sort with step tracking"""
    arr = arr[:]
    n = len(arr)
    sorted_indices = []
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield {'array': arr[:], 'comparing': [min_idx, j], 'sorted': sorted_indices[:]}
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield {'array': arr[:], 'swapping': [i, min_idx], 'sorted': sorted_indices[:]}
        
        sorted_indices.append(i)
    
    yield {'array': arr[:], 'sorted': list(range(n))}

def insertion_sort_steps(arr: List[int]) -> Generator:
    """Insertion sort with step tracking"""
    arr = arr[:]
    n = len(arr)
    
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            yield {'array': arr[:], 'comparing': [j, j + 1], 'sorted': list(range(i))}
            arr[j + 1] = arr[j]
            yield {'array': arr[:], 'swapping': [j, j + 1], 'sorted': list(range(i))}
            j -= 1
        
        arr[j + 1] = key
        yield {'array': arr[:], 'sorted': list(range(i + 1))}
    
    yield {'array': arr[:], 'sorted': list(range(n))}

def merge_sort_steps(arr: List[int]) -> Generator:
    """Merge sort with step tracking (iterative for visualization)"""
    arr = arr[:]
    n = len(arr)
    
    # Bottom-up merge sort
    size = 1
    while size < n:
        for start in range(0, n, 2 * size):
            mid = min(start + size, n)
            end = min(start + 2 * size, n)
            
            # Merge arr[start:mid] and arr[mid:end]
            left = arr[start:mid]
            right = arr[mid:end]
            
            i = j = 0
            k = start
            
            while i < len(left) and j < len(right):
                yield {'array': arr[:], 'comparing': [start + i, mid + j] if mid + j < n else [start + i]}
                
                if left[i] <= right[j]:
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                yield {'array': arr[:], 'swapping': [k]}
                k += 1
            
            while i < len(left):
                arr[k] = left[i]
                i += 1
                k += 1
                yield {'array': arr[:], 'swapping': [k - 1]}
            
            while j < len(right):
                arr[k] = right[j]
                j += 1
                k += 1
                yield {'array': arr[:], 'swapping': [k - 1]}
        
        size *= 2
    
    yield {'array': arr[:], 'sorted': list(range(n))}

def quick_sort_steps(arr: List[int]) -> Generator:
    """Quick sort with step tracking"""
    arr = arr[:]
    n = len(arr)
    sorted_indices = set()
    
    def partition(low: int, high: int):
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            yield {'array': arr[:], 'comparing': [j, high], 'sorted': list(sorted_indices)}
            
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield {'array': arr[:], 'swapping': [i, j], 'sorted': list(sorted_indices)}
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield {'array': arr[:], 'swapping': [i + 1, high], 'sorted': list(sorted_indices)}
        
        return i + 1
    
    stack = [(0, n - 1)]
    
    while stack:
        low, high = stack.pop()
        
        if low < high:
            # Partition
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                yield {'array': arr[:], 'comparing': [j, high], 'sorted': list(sorted_indices)}
                
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    if i != j:
                        yield {'array': arr[:], 'swapping': [i, j], 'sorted': list(sorted_indices)}
            
            pi = i + 1
            arr[pi], arr[high] = arr[high], arr[pi]
            yield {'array': arr[:], 'swapping': [pi, high], 'sorted': list(sorted_indices)}
            
            sorted_indices.add(pi)
            
            stack.append((pi + 1, high))
            stack.append((low, pi - 1))
    
    yield {'array': arr[:], 'sorted': list(range(n))}

def render_pseudocode(algorithm: str):
    """Render pseudocode for selected algorithm"""
    pseudocodes = {
        "Bubble Sort": """
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # Flag for optimization
        swapped = False
        
        for j in range(0, n - i - 1):
            # Compare adjacent elements
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps, array is sorted
        if not swapped:
            break
    
    return arr
```
        """,
        "Selection Sort": """
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # Find minimum in unsorted portion
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap minimum with first unsorted
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr
```
        """,
        "Insertion Sort": """
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Shift elements greater than key
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insert key at correct position
        arr[j + 1] = key
    
    return arr
```
        """,
        "Merge Sort": """
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```
        """,
        "Quick Sort": """
```python
def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    
    return arr

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```
        """
    }
    
    st.markdown(pseudocodes.get(algorithm, "Pseudocode not available"))

def render_algorithm_comparison():
    """Render comparison table of all algorithms"""
    st.markdown("""
    | Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Stable |
    |-----------|-------------|------------|--------------|-------|--------|
    | Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
    | Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
    | Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
    | Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | ✅ |
    | Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | ❌ |
    
    **When to use which:**
    - **Bubble/Selection/Insertion:** Small arrays, educational purposes
    - **Insertion:** Nearly sorted data, online sorting
    - **Merge Sort:** Need stable sort, linked lists, external sorting
    - **Quick Sort:** General purpose, in-place sorting, average case matters
    """)

def render_algorithm_explanation(algorithm: str):
    """Render detailed explanation of algorithm"""
    explanations = {
        "Bubble Sort": """
**Bubble Sort** repeatedly steps through the list, compares adjacent elements, 
and swaps them if they're in the wrong order.

**Key Properties:**
- Simple to understand and implement
- Inefficient for large datasets
- Adaptive: O(n) when nearly sorted (with optimization)
- Stable: Equal elements maintain relative order

**Best for:** Educational purposes, very small arrays
        """,
        "Selection Sort": """
**Selection Sort** divides the array into sorted and unsorted portions, 
repeatedly finding the minimum from unsorted and adding it to sorted.

**Key Properties:**
- Simple implementation
- Performs well on small lists
- Makes minimum number of swaps: O(n)
- Not stable: May change relative order of equal elements

**Best for:** When memory writes are expensive, small arrays
        """,
        "Insertion Sort": """
**Insertion Sort** builds the sorted array one element at a time by 
inserting each element into its correct position.

**Key Properties:**
- Efficient for small datasets
- Adaptive: O(n) for nearly sorted data
- Online: Can sort as data arrives
- Stable: Maintains relative order

**Best for:** Small arrays, nearly sorted data, online sorting
        """,
        "Merge Sort": """
**Merge Sort** divides the array in half, recursively sorts each half, 
then merges the sorted halves.

**Key Properties:**
- Guaranteed O(n log n) in all cases
- Stable sorting algorithm
- Not in-place: Requires O(n) extra space
- Parallelizable: Independent subproblems

**Best for:** Linked lists, external sorting, when stability matters
        """,
        "Quick Sort": """
**Quick Sort** picks a pivot, partitions the array around it, 
then recursively sorts the partitions.

**Key Properties:**
- Average case O(n log n), very fast in practice
- In-place: O(log n) stack space
- Not stable: May reorder equal elements
- Pivot choice affects performance

**Best for:** General purpose sorting, when average case matters
        """
    }
    
    st.markdown(explanations.get(algorithm, "Explanation not available"))
