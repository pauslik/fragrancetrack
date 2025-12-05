import os

class TempFiles():
    def __init__(self) -> None:
        self.files = []

    def add_file(self, file):
        self.files.append(file)
        return self.files

    def cleanup(self):
        for file in self.files:
            print("Cleaning up test files:")
            if os.path.exists(file):
                os.remove(file)
                print(f'Removed: {file}')
            else:
                print(f'Not Found: {file}')
        if len(self.files) > 0:
            print("Cleanup done.")
        self.files = []
        return True