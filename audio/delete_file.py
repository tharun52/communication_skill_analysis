import os

def delete_file(file_paths):
    # iterate through list of paths
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"File deleted successfully: {file_path}")
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")
