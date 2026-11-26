"""
main.py
-------
Menu-driven console interface for the NumPy Analyzer.
Run with:  python main.py
"""

import numpy as np

from data_analytics import DataAnalytics

LINE = "=" * 40


# ---------------------------------------------------------------------- #
# Input helpers
# ---------------------------------------------------------------------- #
def ask_int(prompt, minimum=1):
    """Keep asking until the user enters a whole number >= minimum."""
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Please enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def ask_elements(count, prompt):
    """Ask for exactly `count` numbers separated by spaces."""
    while True:
        try:
            values = DataAnalytics.parse_numbers(input(prompt))
            if len(values) != count:
                print(f"You entered {len(values)} elements, but {count} are needed.")
                continue
            return values
        except ValueError as err:
            print(err)


def ask_second_array(analyzer, label="same-size array elements"):
    """Ask for a second array shaped like the current one."""
    shape = analyzer.data.shape
    count = int(np.prod(shape))
    values = ask_elements(
        count, f"Enter the {label} ({count} elements separated by space): "
    )
    return np.array(values).reshape(shape)


def show(title, array):
    print(f"\n{title}\n{array}")


# ---------------------------------------------------------------------- #
# 1. Create array (+ indexing / slicing)
# ---------------------------------------------------------------------- #
def create_array(analyzer):
    print("\nSelect the type of array to create:")
    print("1. 1D Array\n2. 2D Array\n3. 3D Array")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        shape = (ask_int("Enter the number of elements: "),)
    elif choice == "2":
        shape = (ask_int("Enter the number of rows: "),
                 ask_int("Enter the number of columns: "))
    elif choice == "3":
        shape = (ask_int("Enter the number of layers (depth): "),
                 ask_int("Enter the number of rows: "),
                 ask_int("Enter the number of columns: "))
    else:
        print("Invalid choice.")
        return

    count = int(np.prod(shape))
    values = ask_elements(
        count, f"Enter {count} elements for the array separated by space: "
    )
    analyzer.set_data(DataAnalytics.from_list(values, shape).data)
    show("Array created successfully:", analyzer.data)
    index_slice_menu(analyzer)


def index_slice_menu(analyzer):
    while True:
        print("\nChoose an operation:")
        print("1. Indexing\n2. Slicing\n3. Go Back")
        choice = input("Enter your choice: ").strip()
        try:
            if choice == "1":
                text = input(
                    f"Enter index separated by commas (array has {analyzer.data.ndim} "
                    "dimension(s), e.g. 1,2): "
                )
                show("Result:", analyzer.get_index(DataAnalytics.parse_index(text)))
            elif choice == "2":
                names = {1: ["element"],
                         2: ["row", "column"],
                         3: ["layer", "row", "column"]}.get(analyzer.data.ndim, ["element"])
                slices = [
                    DataAnalytics.parse_range(input(f"Enter the {n} range (start:end): "))
                    for n in names
                ]
                show("Sliced Array:", analyzer.get_slice(slices))
            elif choice == "3":
                return
            else:
                print("Invalid choice. Please try again.")
        except (ValueError, IndexError) as err:
            print(f"Error: {err}")


# ---------------------------------------------------------------------- #
# 2. Mathematical operations
# ---------------------------------------------------------------------- #
def math_operations(analyzer):
    print("\nChoose a mathematical operation:")
    print("1. Addition\n2. Subtraction\n3. Multiplication\n4. Division")
    print("5. Dot Product\n6. Matrix Multiplication")
    choice = input("Enter your choice: ").strip()
    names = {"1": "Addition", "2": "Subtraction", "3": "Multiplication",
             "4": "Division", "5": "Dot Product", "6": "Matrix Multiplication"}
    if choice not in names:
        print("Invalid choice.")
        return

    if choice in "1234":
        other = ask_second_array(analyzer)
        funcs = {"1": analyzer.add, "2": analyzer.subtract,
                 "3": analyzer.multiply, "4": analyzer.divide}
        result = funcs[choice](other)
        label = "Second Array:"
    else:
        rows = ask_int("Enter the number of rows for the second array: ")
        cols = ask_int("Enter the number of columns for the second array: ")
        values = ask_elements(
            rows * cols, f"Enter {rows * cols} elements separated by space: "
        )
        other = np.array(values).reshape(rows, cols)
        result = (analyzer.dot_product(other) if choice == "5"
                  else analyzer.matrix_multiply(other))
        label = "Second Array:"

    show("Original Array:", analyzer.data)
    show(label, other)
    show(f"Result of {names[choice]}:", result)


# ---------------------------------------------------------------------- #
# 3. Combine or split
# ---------------------------------------------------------------------- #
def combine_or_split(analyzer):
    print("\nChoose an option:\n1. Combine Arrays\n2. Split Array")
    choice = input("Enter your choice: ").strip()
    if choice == "1":
        other = ask_second_array(analyzer, "elements of another array to combine")
        show("Original Array:", analyzer.data)
        show("Second Array:", other)
        show("Combined Array (Vertical Stack):", analyzer.combine(other))
    elif choice == "2":
        parts = ask_int("Enter the number of parts to split into: ")
        show("Original Array:", analyzer.data)
        for i, part in enumerate(analyzer.split(parts), start=1):
            show(f"Part {i}:", part)
    else:
        print("Invalid choice.")


# ---------------------------------------------------------------------- #
# 4. Search, sort, filter
# ---------------------------------------------------------------------- #
def search_sort_filter(analyzer):
    print("\nChoose an option:\n1. Search a value\n2. Sort the array\n3. Filter values")
    choice = input("Enter your choice: ").strip()
    show("Original Array:", analyzer.data)

    if choice == "1":
        try:
            value = float(input("Enter the value to search: "))
        except ValueError:
            print("Please enter a valid number.")
            return
        positions = analyzer.search(value)
        if positions:
            print(f"\nValue {value:g} found at position(s): {positions}")
        else:
            print(f"\nValue {value:g} was not found.")
    elif choice == "2":
        order = input("Sort order - 1. Ascending  2. Descending: ").strip()
        show("Sorted Array:", analyzer.sort(descending=(order == "2")))
        print("(Sorting applied row-wise.)")
    elif choice == "3":
        op = input("Enter condition (>, <, >=, <=, ==, !=): ").strip()
        try:
            value = float(input("Enter the value to compare with: "))
        except ValueError:
            print("Please enter a valid number.")
            return
        show(f"Elements where value {op} {value:g}:", analyzer.filter(op, value))
    else:
        print("Invalid choice.")


# ---------------------------------------------------------------------- #
# 5. Aggregates and statistics
# ---------------------------------------------------------------------- #
def aggregates(analyzer):
    print("\nChoose an aggregate/statistical operation:")
    print("1. Sum\n2. Mean\n3. Median\n4. Standard Deviation\n5. Variance")
    print("6. Minimum\n7. Maximum\n8. Percentile\n9. Correlation Coefficient")
    choice = input("Enter your choice: ").strip()
    show("Original Array:", analyzer.data)
    print()

    if choice == "1":
        print(f"Sum of Array: {analyzer.sum()}")
    elif choice == "2":
        print(f"Mean of Array: {analyzer.mean()}")
    elif choice == "3":
        print(f"Median of Array: {analyzer.median()}")
    elif choice == "4":
        print(f"Standard Deviation of Array: {analyzer.std():.4f}")
    elif choice == "5":
        print(f"Variance of Array: {analyzer.variance():.4f}")
    elif choice == "6":
        print(f"Minimum of Array: {analyzer.minimum()}")
    elif choice == "7":
        print(f"Maximum of Array: {analyzer.maximum()}")
    elif choice == "8":
        try:
            q = float(input("Enter percentile (0-100): "))
        except ValueError:
            print("Please enter a valid number.")
            return
        print(f"{q:g}th Percentile: {analyzer.percentile(q)}")
    elif choice == "9":
        other = ask_second_array(analyzer, "elements of the second array")
        print(f"Correlation Coefficient: {analyzer.correlation(other):.4f}")
    else:
        print("Invalid choice.")


# ---------------------------------------------------------------------- #
# Main menu
# ---------------------------------------------------------------------- #
def main():
    analyzer = DataAnalytics()
    print("Welcome to the NumPy Analyzer!")
    print(LINE)

    actions = {
        "2": math_operations,
        "3": combine_or_split,
        "4": search_sort_filter,
        "5": aggregates,
    }

    while True:
        print("\nChoose an option:")
        print("1. Create a Numpy Array")
        print("2. Perform Mathematical Operations")
        print("3. Combine or Split Arrays")
        print("4. Search, Sort, or Filter Arrays")
        print("5. Compute Aggregates and Statistics")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "6":
            print("\nThank you for using the NumPy Analyzer! Goodbye!")
            break
        if choice == "1":
            create_array(analyzer)
        elif choice in actions:
            if not analyzer.has_data():
                print("\nNo array yet. Please create an array first (option 1).")
                continue
            try:
                actions[choice](analyzer)
            except ValueError as err:
                print(f"\nError: {err}")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
    