"""
data_analytics.py
-----------------
Contains the DataAnalytics class, which wraps NumPy functionality
using Object-Oriented Programming principles:

* Constructor      -> __init__ initializes the array
* Encapsulation    -> the array is stored in a private attribute
* Private methods  -> internal checks/computations (name-mangled with __)
* @classmethod     -> alternative ways to build an object
* @staticmethod    -> utilities that do not need object data
"""

import operator

import numpy as np


class DataAnalytics:
    """Holds a NumPy array and exposes analysis operations as methods."""

    # Class-level data: supported filter operators (shared by all objects)
    OPERATORS = {
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
    }

    # ------------------------------------------------------------------ #
    # Constructor and alternative constructors
    # ------------------------------------------------------------------ #
    def __init__(self, data=None):
        """Initialize the analyzer with optional data (list or ndarray)."""
        self.__data = None if data is None else np.array(data)

    @classmethod
    def from_list(cls, values, shape=None):
        """Build an object from a flat list, optionally reshaped."""
        arr = np.array(values)
        if shape is not None:
            arr = arr.reshape(shape)
        return cls(arr)

    @classmethod
    def from_text(cls, text, shape=None):
        """Build an object from space-separated text like '10 20 30'."""
        return cls.from_list(cls.parse_numbers(text), shape)

    # ------------------------------------------------------------------ #
    # Static utilities (no object data needed)
    # ------------------------------------------------------------------ #
    @staticmethod
    def parse_numbers(text):
        """Convert 'a b c' into a list of numbers (ints if possible)."""
        parts = text.replace(",", " ").split()
        if not parts:
            raise ValueError("No numbers were entered.")
        try:
            return [int(p) for p in parts]
        except ValueError:
            try:
                return [float(p) for p in parts]
            except ValueError:
                raise ValueError("Please enter valid numbers only.")

    @staticmethod
    def parse_range(text):
        """Convert 'start:end' (e.g. '0:2', ':3', '1:') into a slice."""
        text = text.strip()
        if text in ("", ":"):
            return slice(None)
        if ":" not in text:
            raise ValueError("Use the start:end format, e.g. 0:2")
        start, end = text.split(":", 1)
        try:
            return slice(int(start) if start.strip() else None,
                         int(end) if end.strip() else None)
        except ValueError:
            raise ValueError("Range values must be whole numbers.")

    @staticmethod
    def parse_index(text):
        """Convert '1,2' into the tuple (1, 2)."""
        try:
            return tuple(int(p) for p in text.replace(" ", "").split(",") if p != "")
        except ValueError:
            raise ValueError("Index values must be whole numbers.")

    # ------------------------------------------------------------------ #
    # Private helpers (internal computations / validation)
    # ------------------------------------------------------------------ #
    def __ensure_loaded(self):
        if self.__data is None:
            raise ValueError("No array yet. Create an array first (option 1).")
        return self.__data

    def __same_shape(self, other):
        other = np.array(other)
        if other.shape != self.__ensure_loaded().shape:
            raise ValueError(
                f"Array sizes differ: {self.__data.shape} vs {other.shape}."
            )
        return other

    # ------------------------------------------------------------------ #
    # Array management
    # ------------------------------------------------------------------ #
    @property
    def data(self):
        """Read-only access to the stored array."""
        return self.__ensure_loaded()

    def has_data(self):
        return self.__data is not None

    def set_data(self, data):
        self.__data = np.array(data)

    def get_index(self, index):
        """Indexing: element, row, or sub-array selected by an index tuple."""
        return self.__ensure_loaded()[index]

    def get_slice(self, slices):
        """Slicing: slices is a list of slice objects, one per dimension."""
        return self.__ensure_loaded()[tuple(slices)]

    def combine(self, other, axis=0):
        """Concatenate with another array (vertical stack by default)."""
        other = self.__same_shape(other)
        return np.concatenate((self.__data, other), axis=axis)

    def split(self, parts, axis=0):
        """Split into `parts` smaller arrays (as evenly as possible)."""
        arr = self.__ensure_loaded()
        if parts < 1 or parts > arr.shape[axis]:
            raise ValueError(
                f"Parts must be between 1 and {arr.shape[axis]} for this array."
            )
        return np.array_split(arr, parts, axis=axis)

    # ------------------------------------------------------------------ #
    # Mathematical operations
    # ------------------------------------------------------------------ #
    def add(self, other):
        return self.__ensure_loaded() + self.__same_shape(other)

    def subtract(self, other):
        return self.__ensure_loaded() - self.__same_shape(other)

    def multiply(self, other):
        return self.__ensure_loaded() * self.__same_shape(other)

    def divide(self, other):
        other = self.__same_shape(other)
        if np.any(other == 0):
            raise ValueError("Division by zero is not allowed.")
        return self.__ensure_loaded() / other

    def dot_product(self, other):
        arr = self.__ensure_loaded()
        other = np.array(other)
        try:
            return np.dot(arr, other)
        except ValueError:
            raise ValueError("Shapes are not aligned for a dot product.")

    def matrix_multiply(self, other):
        arr = self.__ensure_loaded()
        other = np.array(other)
        if arr.ndim != 2 or other.ndim != 2:
            raise ValueError("Matrix multiplication needs two 2D arrays.")
        if arr.shape[1] != other.shape[0]:
            raise ValueError(
                f"Columns of first ({arr.shape[1]}) must equal rows of second ({other.shape[0]})."
            )
        return np.matmul(arr, other)

    # ------------------------------------------------------------------ #
    # Search, sort and filter
    # ------------------------------------------------------------------ #
    def search(self, value):
        """Return the positions (as a list of index tuples) of a value."""
        positions = np.argwhere(self.__ensure_loaded() == value)
        return [tuple(int(i) for i in pos) for pos in positions]

    def sort(self, descending=False):
        """Return a sorted copy (row-wise for 2D, last axis for 3D)."""
        result = np.sort(self.__ensure_loaded(), axis=-1)
        return np.flip(result, axis=-1) if descending else result

    def filter(self, op, value):
        """Return a 1D array of elements satisfying `element op value`."""
        arr = self.__ensure_loaded()
        if op not in self.OPERATORS:
            raise ValueError(f"Unsupported condition '{op}'.")
        return arr[self.OPERATORS[op](arr, value)]

    # ------------------------------------------------------------------ #
    # Aggregates and statistics
    # ------------------------------------------------------------------ #
    def sum(self):
        return np.sum(self.__ensure_loaded())

    def mean(self):
        return np.mean(self.__ensure_loaded())

    def median(self):
        return np.median(self.__ensure_loaded())

    def std(self):
        return np.std(self.__ensure_loaded())

    def variance(self):
        return np.var(self.__ensure_loaded())

    def minimum(self):
        return np.min(self.__ensure_loaded())

    def maximum(self):
        return np.max(self.__ensure_loaded())

    def percentile(self, q):
        if not 0 <= q <= 100:
            raise ValueError("Percentile must be between 0 and 100.")
        return np.percentile(self.__ensure_loaded(), q)

    def correlation(self, other):
        """Correlation coefficient between this array and another one."""
        other = self.__same_shape(other)
        flat = self.__data.flatten()
        if flat.size < 2:
            raise ValueError("Need at least 2 elements for correlation.")
        if np.std(flat) == 0 or np.std(other) == 0:
            raise ValueError("Correlation is undefined for constant data.")
        return np.corrcoef(flat, other.flatten())[0, 1]