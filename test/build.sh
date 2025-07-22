#!/bin/bash
echo "🛠 Building image..."
docker build -t bot-runner:latest .
echo "✅ Done."
