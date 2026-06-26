#!/bin/bash
# Status line customizado: git branch + model + contexto + custo

set -e

# Parse stdin (JSON com contexto da sessão)
BRANCH=$(echo "$ARGV_statusline" 2>/dev/null | jq -r '.git_branch // "detached"' 2>/dev/null || echo "?")
MODEL=$(echo "$ARGV_statusline" 2>/dev/null | jq -r '.model // "unknown"' 2>/dev/null || echo "?")
CONTEXT=$(echo "$ARGV_statusline" 2>/dev/null | jq -r '.context_usage // "0%"' 2>/dev/null || echo "0%")
COST=$(echo "$ARGV_statusline" 2>/dev/null | jq -r '.session_cost // "$0.00"' 2>/dev/null || echo "$0.00")

# Formato: [branch] model | context | cost
echo "[$BRANCH] $MODEL | $CONTEXT | $COST"
