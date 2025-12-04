  echo "Checking for differences from master..."
  cd Documentation
  for manpage in *.1 *.5 *.7; do
      if [ -f "/tmp/master-man-pages/$manpage" ] && [ -f "$manpage" ]; then
          if ! diff -q "/tmp/master-man-pages/$manpage" "$manpage" >/dev/null; then
              echo "CHANGED: $manpage"
          fi
      fi
  done
