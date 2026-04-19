#!/bin/bash

set -e

IMAGE_NAME=$1

if [ -z "$IMAGE_NAME" ]; then
  echo "❌ Usage: ./trivy-scan.sh <image-name>"
  exit 1
fi

echo "🔍 Running Trivy scan on $IMAGE_NAME..."

docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image \
  --severity HIGH,CRITICAL \
  --exit-code 1 \
  --no-progress \
  "$IMAGE_NAME"

echo "✅ Trivy scan completed"