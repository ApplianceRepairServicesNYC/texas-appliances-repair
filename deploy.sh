#!/bin/bash

PROJECT_NAME="texas-appliances-repair"
DEPLOY_FOLDER="."
ATTEMPT=1

export PATH=~/.npm-global/bin:$PATH

echo "=== Cloudflare Pages Deployment Script ==="
echo "Project: $PROJECT_NAME"
echo "Folder: $DEPLOY_FOLDER"
echo ""

while true; do
    echo "=========================================="
    echo "ATTEMPT #$ATTEMPT - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="

    wrangler pages deploy "$DEPLOY_FOLDER" \
        --project-name "$PROJECT_NAME" \
        --commit-dirty=true

    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "SUCCESS on attempt #$ATTEMPT"
        echo "=========================================="
        exit 0
    fi

    echo ""
    echo "Attempt #$ATTEMPT failed (exit code: $EXIT_CODE)"
    echo "Waiting 10 seconds before retry..."
    echo ""

    sleep 10
    ATTEMPT=$((ATTEMPT + 1))
done
