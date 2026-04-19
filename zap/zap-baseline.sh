#!/bin/bash

set -e

TARGET_URL=$1

if [ -z "$TARGET_URL" ]; then
  echo "❌ Usage: ./zap-baseline.sh <target-url>"
  exit 1
fi

echo "🛡️ Running ZAP baseline scan on $TARGET_URL..."

docker run --rm \
  -v $(pwd):/zap/wrk:rw \
  --user $(id -u):$(id -g) \
  owasp/zap2docker-stable \
  zap-baseline.py \
  -t "$TARGET_URL" \
  -r zap-report.html \
  -I

echo "✅ ZAP scan completed. Report generated: zap-report.html"