## Project 8 🎱<img width="480" height="358" alt="GirlBirthdayGIFbyMinkaComics" src="https://github.com/user-attachments/assets/6a53be45-74ce-4c24-add1-430cb92c6fcc" />

<img width="2400" height="720" alt="image" src="https://github.com/user-attachments/assets/7f6e9ae7-96fd-41f1-b824-fea5ee58de42" />
Crunch numbers, slice arrays and spot patterns, all from a friendly console menu.

Features · OOP Design · Structure · Quick Start · Demo · User Guide · Assumptions · Author

## ⭐About the Project

NumPy Analyzer is a Python console application that wraps the power of NumPy inside a clean Object-Oriented design. A single class, DataAnalytics, holds the data and exposes every operation as a method, so you can create arrays, do math, combine or split them, search, sort, filter, and compute statistics without writing any NumPy code yourself.

👌Goal: show how NumPy functionality and OOP principles (constructors, encapsulation, class methods and static methods) work together to solve real data tasks.

## ⭐Features
## Array Management
>> Create 1D, 2D and 3D arrays from user input
>> Indexing for single elements, rows and columns
>> Slicing with a simple start:end syntax
>> Combine arrays (stacking) or split an array into smaller ones

 <img width="1520" height="600" alt="image" src="https://github.com/user-attachments/assets/e2467e0e-df34-4dc7-a968-ca5e8a5511b6" />



## ⭐Mathematical Operations

>> Element-wise addition, subtraction, multiplication and division

>> Dot product and matrix multiplication for 2D arrays

## ⭐Search, Sort and Filter

>> Search for a specific value in an array
>> Sort in ascending or descending order
>> Filter using user-defined conditions
>> Aggregates and Statistics
>> Sum, mean, median, standard deviation and variance
>> Minimum and maximum values
>> Percentiles
>> Correlation coefficients between arrays
>>
>> class DataAnalytics:
    def __init__(self, data):
        self.__data = np.array(data)          # encapsulated array

    @classmethod
    def from_list(cls, values):               # class-level method
        return cls(values)

    @staticmethod
    def is_valid_number(text):                # static utility
        ...

    def _compute_median(self):                # private helper
        return np.median(self.__data)


## ⭐OOP Design

The whole toolkit lives in one class, built around core OOP ideas:

Constructor (__init__): initializes the array when a DataAnalytics object is created
Encapsulation: the array is stored privately, and internal calculations use private helper methods (named with a leading underscore)

@classmethod: alternative ways to build an object, for example from a list or from user input
@staticmethod: small utilities that do not need object data, such as input validation


class DataAnalytics:
    def __init__(self, data):
        self.__data = np.array(data)          # encapsulated array

    @classmethod
    def from_list(cls, values):               # class-level method
        return cls(values)

    @staticmethod
    def is_valid_number(text):                # static utility
        ...

    def _compute_median(self):                # private helper
        return np.median(self.__data)


## ⭐Quick Start

# 1. Clone the repository
git clone https://github.com/<your-username>/numpy-analyzer.git

# 2. Enter the folder
cd numpy-analyzer

# 3. Install NumPy
pip install numpy

# 4. Run the analyzer
python main.py

## ⭐Demo

<img width="1520" height="800" alt="image" src="https://github.com/user-attachments/assets/25c79f96-a852-4aba-a19d-a29641a9429f" />

## Array creation and slicing
Select the type of array to create:
1. 1D Array
2. 2D Array
3. 3D Array
Enter your choice: 2

Enter the number of rows: 2
Enter the number of columns: 3
Enter 6 elements for the array separated by space: 10 20 30 40 50 60

Array created successfully:
[[10 20 30]
 [40 50 60]]

Enter the row range (start:end): 0:2
Enter the column range (start:end): 1:3

Sliced Array:
[[20 30]
 [50 60]]

 <img width="1520" height="600" alt="image" src="https://github.com/user-attachments/assets/e2467e0e-df34-4dc7-a968-ca5e8a5511b6" />


## Mathematical operation (addition)

Original Array:
[[10 20 30]
 [40 50 60]]

Second Array:
[[5 5 5]
 [5 5 5]]

Result of Addition:
[[15 25 35]
 [45 55 65]]
 
 ## Combine arrays (vertical stack)

 Combined Array (Vertical Stack):
[[10 20 30]
 [40 50 60]
 [ 1  2  3]
 [ 4  5  6]]

 ## Sort

 Sorted Array:
[[10 20 30]
 [40 50 60]]
(Sorting applied row-wise.)

## Aggregates and statistics (median)

Median of Array: 35.0

## Exit

Thank you for using the NumPy Analyzer! Goodbye!

</details>

## ⭐User Guide

Run python main.py to open the main menu.
Choose 1 first to create an array. The other options work on the array you created.
Type the number of an option and press Enter, then follow the prompts.
Enter array elements separated by spaces, for example 10 20 30 40 50 60.
For slicing, use the start:end format, for example 0:2.
Choose 6 from the main menu to exit.

## Tips 

When you add, subtract, multiply or divide, the second array must be the same size as the first.
For the dot product and matrix multiplication, the shapes must be compatible (columns of the first equal rows of the second).
Division by zero is handled safely and reported instead of crashing the program.

## Concepts Demonstrated

NumPy arrays: creation, indexing, slicing, stacking and splitting
Vectorized math: element-wise operations, dot product, matrix multiplication
Statistics: sum, mean, median, standard deviation, variance, percentiles, correlation
Classes and objects: one DataAnalytics class that encapsulates all functionality
Constructors: array initialization in __init__
Encapsulation: private attribute and private helper methods
@classmethod and @staticmethod: alternative constructors and reusable utilities
Input validation: safe handling of wrong shapes, bad numbers and invalid choices

## Assumptions

Python 3.8 or newer and NumPy are installed.
Arrays are created from numbers entered by the user, separated by spaces.
The array created in option 1 stays active and is used by the other menu options.
A second array for math or combining must match the required size, and the program shows a clear message if it does not.
Sorting defaults to row-wise for 2D arrays, as shown in the sample output.
Combining arrays uses a vertical stack by default.
Median, mean and similar results are calculated over all elements of the array.
Percentiles use NumPy's default linear interpolation.

## Project Checklist

[x] DataAnalytics class that encapsulates all functionality
[x] 1D, 2D and 3D array creation, indexing and slicing
[x] Combine and split arrays
[x] Element-wise math, dot product and matrix multiplication
[x] Search, sort and filter
[x] Aggregates and statistical functions
[x] Constructors, private methods, @classmethod and @staticmethod
[x] Menu-driven interface with exit option
[x] README with documented assumptions

## ✨Author

Tejani Janvi CSE 3C, Computer Science Engineering
<div align="center">
Built with Python, NumPy and a lot of curiosity.

If you found this helpful, give the repo a star.✨✨✨✨

</div>
