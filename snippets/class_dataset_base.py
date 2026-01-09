import threading

import pandas as pd
from pandas.api.types import is_float_dtype, is_integer_dtype, is_string_dtype


class DatasetBase:
    # REQUIRED_COLUMNS = {"open", "high", "low", "close"}
    # EXPECTED_TYPES = {"open": float, "high": float, "low": float, "close": float}
    
    REQUIRED_COLUMNS = {"x"}
    EXPECTED_TYPES = {"x": ["int64", "float64"]}

    def __init__(self, dataset: pd.DataFrame = None):
        self._lock = threading.Lock()

        # Validate immediately if data is provided
        if dataset is not None:
            self._validate_schema(dataset)

        self._data = dataset

    def _check_type(self, series: pd.Series, expected: str) -> bool:
        """Helper to match a single expected type or abstract category."""
        if expected == "any_int":
            return is_integer_dtype(series)
        elif expected == "any_float":
            return is_float_dtype(series)
        elif expected == "string":
            # Handles both 'object' and 'string' dtypes
            return is_string_dtype(series)
        else:
            # Fallback for specific strings like 'int64' or 'datetime64[ns]'
            return str(series.dtype) == expected

    def _repair_column(self, series: pd.Series, target: str) -> pd.Series:
        """Attempts to convert a series to the target abstract or specific type."""
        try:
            if target == "any_int":
                # pd.to_numeric with downcast='integer' is safer than .astype(int)
                return pd.to_numeric(series, errors="raise", downcast="integer")
            elif target == "any_float":
                return pd.to_numeric(series, errors="raise")
            elif target == "string":
                return series.astype("string")
            else:
                # Specific types like 'int64'
                return series.astype(target)
        except (ValueError, TypeError):
            # If repair fails, the original validation will catch it
            return series

    def _validate_schema(self, df: pd.DataFrame, repair: bool = True):
        for col, expected in self.EXPECTED_TYPES.items():
            # Ensure column exists
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

            # Support for lists: Check if any of the allowed types match
            allowed_list = expected if isinstance(expected, list) else [expected]

            # if not any(self._check_type(df[col], t) for t in allowed_list):
            #     raise TypeError(f"Column '{col}' expected {expected}, but got {df[col].dtype}")

            # Initial check: Is it already valid?
            if not any(self._check_type(df[col], t) for t in allowed_list):
                if repair:
                    print(f"Repairing column '{col}' to match {allowed_list[0]}...")
                    # Attempt repair using the FIRST item in the allowed list
                    df[col] = self._repair_column(df[col], allowed_list[0])

                    # Final check after repair
                    if not any(self._check_type(df[col], t) for t in allowed_list):
                        raise TypeError(f"Could not repair column '{col}' to {expected}")
                else:
                    raise TypeError(f"Column '{col}' expected {expected}, got {df[col].dtype}")

    @property
    def data(self) -> pd.DataFrame:
        # First check (no lock) for high performance after initialization
        if self._data is None:
            with self._lock:
                # Second check (with lock) to prevent race conditions
                if self._data is None:
                    # "Thread-safe loading...
                    self._data = pd.DataFrame({"a": [1, 2, 3]})
        return self._data

    @data.setter
    def data(self, value: pd.DataFrame):
        with self._lock:
            if not isinstance(value, pd.DataFrame):
                raise TypeError("Must be a pandas DataFrame")
            self._data = value


class MyClass(DatasetBase):
    # Subclasses can override the schema requirements
    REQUIRED_COLUMNS = {"x"}

    def __init__(self, dataset: pd.DataFrame = None):
        super().__init__(dataset)
        pass


x = MyClass(dataset=pd.DataFrame({"x": [5.3, 7.0, 9, 1]}))
x = MyClass(dataset=pd.DataFrame({"x": ["1", "2"]}))
x = MyClass()

print(x.data)