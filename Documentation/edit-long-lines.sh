
  #!/bin/bash

  locations=$(git show HEAD | grep -n '.\{79\}' | grep ':+' | while IFS=: read line_num plus_and_content; do
      content="${plus_and_content#+}"
      grep -rn --fixed-strings "$content" . | cut -d: -f1,2
  done)

  echo "$locations" | while IFS=: read filename line_number; do
      hx "$filename:$line_number"
  done
