install:
	# Create symlink for pre-commit hook.
	ln -sf ../../test/pre-commit.sh .git/hooks/pre-commit

check:
	./test/test.sh
