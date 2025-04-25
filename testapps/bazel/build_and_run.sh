#!/bin/bash
# Build and Run Script for Bazel Example

set -e

# Step 1: Build the project
echo "Building the project..."
bazel build //:my_project

# Step 2: Run the compiled binary
echo "Running the program..."
./bazel-bin/my_project

echo "Done!"

