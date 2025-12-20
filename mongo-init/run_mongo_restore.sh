#!/bin/bash
set -e

echo "Looking for .bson files in /dump_staging..."

files=(/dump_staging/*.bson)
if [ ${#files[@]} -eq 0 ] || [ "${files[0]}" = '/dump_staging/*.bson' ]; then
  echo "No .bson files found in /dump_staging"
  exit 0
fi

for f in /dump_staging/*.bson; do
  bn=$(basename "$f" .bson)
  echo "Restoring $bn from $f"
  mongorestore --host db_mongo --port 27017 --verbose --drop --db "$bn" --collection "$bn" "$f"
done

echo "RESTORE_COMPLETE"