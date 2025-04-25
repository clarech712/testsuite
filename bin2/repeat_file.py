import sys
import os

def repeat_file_content(filename: str, count: int):
    try:
        # Read original file content
        with open(filename, 'r') as file:
            content = file.read()

        # Multiply the content
        repeated_content = content * count

        # Create the new filename with '.multiplied' suffix
        new_filename = f"{filename}.multiplied"

        # Write to the new file
        with open(new_filename, 'w') as file:
            file.write(repeated_content)

        print(f"New file '{new_filename}' created with {count} copies of the original content.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage from command line: python script.py filename.txt 3
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <filename> <count>")
    else:
        file_name = sys.argv[1]
        try:
            repeat_count = int(sys.argv[2])
            repeat_file_content(file_name, repeat_count)
        except ValueError:
            print("Error: <count> must be an integer.")

