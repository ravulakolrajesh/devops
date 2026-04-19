#!/bin/bash

set -e

if [ -z "$SONAR_AUTH_TOKEN" ] || [ -z "$SONAR_HOST_URL" ]; then
  echo "❌ Required environment variables not set"
  exit 1
fi

echo "📊 Running SonarQube scan..."

docker run --rm \
  --network devops-net \
  -e SONAR_HOST_URL=$SONAR_HOST_URL \
  -v $(pwd):/usr/src \
  sonarsource/sonar-scanner-cli \
  -Dsonar.projectKey=my-app \
  -Dsonar.sources=. \
  -Dsonar.host.url=$SONAR_HOST_URL \
  -Dsonar.login=$SONAR_AUTH_TOKEN

echo "✅ SonarQube scan completed"