import numpy as np

class Calculator:
    """A basic calculator using NumPy arrays."""

    @staticmethod
    def add(a: list[float], b: list[float]) -> list[float]:
        """Element-wise addition of two lists."""
        arr_a = np.array(a)
        arr_b = np.array(b)
        return (arr_a + arr_b).tolist()

    @staticmethod
    def multiply(a: list[float], b: list[float]) -> list[float]:
        """Element-wise multiplication of two lists."""
        arr_a = np.array(a)
        arr_b = np.array(b)
        return (arr_a * arr_b).tolist()

    @staticmethod
    def mean(numbers: list[float]) -> float:
        """Calculates the mean of a list of numbers."""
        return float(np.mean(numbers))