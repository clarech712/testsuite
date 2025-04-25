#!/bin/bash

# Check if the input file is provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <module_file>"
  exit 1
fi

module_file="$1"

# Check if the input file exists and is readable
if [ ! -f "$module_file" ]; then
  echo "Error: File '$module_file' not found."
  exit 1
fi

if [ ! -r "$module_file" ]; then
  echo "Error: Cannot read file '$module_file'. Check permissions."
  exit 1
fi

# Check if ./testapp exists and is executable
if [ ! -f "./testapp" ]; then
  echo "Error: The executable './testapp' not found in the current directory."
  exit 1
fi

if [ ! -x "./testapp" ]; then
  echo "Error: The file './testapp' is not executable. Check permissions."
  exit 1
fi

# Read each line from the module file
while IFS= read -r module_name; do
  # Run ./testapp with the current module name as an argument
  echo "Running: ./testapp \"$module_name\""
  ./testapp "$module_name"
  # You can add error handling or logging here if needed
done < "$module_file"

echo "Finished processing all modules."

exit 0
