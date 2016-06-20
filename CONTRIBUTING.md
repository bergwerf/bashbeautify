Contributing guidelines
=======================
Pull requests are very welcome! But please also add tests for your fix or
feature. To do so, put an incorrectly formatted Bash file in
`test/input/{PR or issue number}.sh.txt` and a correctly formatted one in
`test/output/{PR or issue number}.sh.txt`. Running `make check` will format
the input file with the updated `bashbeautify.py` and match it with the output
file.
