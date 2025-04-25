#!/bin/bash
# Build Script for Autoconf Example

set -e

# Step 1: Generate configuration scripts
echo "Generating configuration scripts..."
autoreconf --install

# Step 2: Run the configure script
echo "Running configure..."
./configure

# Step 3: Compile the program
echo "Building the program..."
make

echo "Build complete!"

