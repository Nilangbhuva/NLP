import pickle
import sys
import os

def inspect_pickle(path):
    print(f"\nInspecting: {path}")
    if not os.path.exists(path):
        print("File not found.")
        return
    try:
        with open(path, "rb") as f:
            obj = pickle.load(f)
        print("Top-level type:", type(obj))
        if hasattr(obj, "__len__"):
            print("Length:", len(obj))
        else:
            print("No length (not a container)")

        # try to peek at one key/value safely
        if isinstance(obj, dict):
            try:
                k = next(iter(obj.keys()))
                v = obj[k]
                print("Sample key:", k, "| type:", type(k))
                print("Sample value:", v, "| type:", type(v))
            except StopIteration:
                print("Dict is empty.")
        elif hasattr(obj, "__iter__"):
            it = iter(obj)
            try:
                first = next(it)
                print("Sample element:", first, "| type:", type(first))
            except StopIteration:
                print("Empty iterable.")
    except Exception as e:
        print("Error while loading:", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_pickle.py path_to_pickle.pkl")
    else:
        inspect_pickle(sys.argv[1])
