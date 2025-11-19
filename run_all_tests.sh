#!/bin/bash

fail_count=0

for dir in */
do
    echo "TESTING EXAMPLE PACKAGE $dir"
    (cd "$dir" && uv run pytest) || ((fail_count++))
done

if ((fail_count > 0))
then
    echo "SOME EXAMPLE TESTS FAILED; SEE ABOVE"
    exit 1
fi

exit 0
