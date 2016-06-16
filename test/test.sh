#!/bin/bash

# This is the test runner for the bashbeautify tests.
# All test input files are located under test/input.
# All expected output files are under test/output.
#
# To remain consistent, these files should not be executable (this is also the
# reason they have a .txt file extension). The input files do also not have to
# be valid Bash (e.g. they do not have to be executable, as long as they serve
# to check the formatting).

# Descend to the script location.
cd "$(dirname "$0")"

# Copy all input files to a temporary output directory.
mkdir tmp
cp input/* tmp
cd tmp

# Run bashbeautify for each .sh.txt file in the temporary directory.
for file in *.sh.txt
do
  # Format file.
  python ../../bashbeautify.py $file

  # Compare the formatted file with the expected formatting.
  diffout=$(diff -q "$file" "../output/$file")

  if [ -n "$diffout" ]; then
    echo "$file was not formatted as expected."
    diff "$file" "../output/$file"

    # Terminate.
    cd ../
    rm -rf tmp
    exit 1
  else
    echo "$file was formatted as expected!"
  fi
done

# Clean up.
cd ../
rm -rf tmp
