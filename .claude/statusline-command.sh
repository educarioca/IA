#!/usr/bin/env bash
input=$(cat)

# cwd
cwd=$(echo "$input" | grep -o '"current_dir":"[^"]*"' | head -1 | sed 's/"current_dir":"//;s/"//')
[ -z "$cwd" ] && cwd=$(echo "$input" | grep -o '"cwd":"[^"]*"' | head -1 | sed 's/"cwd":"//;s/"//')
cwd_basename=$(basename "$cwd")
[ -z "$cwd_basename" ] && cwd_basename="."

# Git branch (skip optional lock)
branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)
[ -z "$branch" ] && branch="no-branch"

# Model display name
model=$(echo "$input" | grep -o '"display_name":"[^"]*"' | head -1 | sed 's/"display_name":"//;s/"//')
[ -z "$model" ] && model=$(echo "$input" | grep -o '"id":"[^"]*"' | head -1 | sed 's/"id":"//;s/"//')
[ -z "$model" ] && model="unknown"

# Context used percentage (pre-calculated)
used=$(echo "$input" | grep -o '"used_percentage":[0-9.]*' | head -1 | sed 's/"used_percentage"://')
if [ -n "$used" ]; then
    ctx=$(printf '%.0f' "$used")
else
    ctx="?"
fi

# Cost: estimate from total tokens (input $3/M, output $15/M — Sonnet pricing)
total_in=$(echo "$input" | grep -o '"total_input_tokens":[0-9]*' | head -1 | sed 's/"total_input_tokens"://')
total_out=$(echo "$input" | grep -o '"total_output_tokens":[0-9]*' | head -1 | sed 's/"total_output_tokens"://')
if [ -n "$total_in" ] && [ -n "$total_out" ]; then
    cost=$(awk "BEGIN { printf \"%.3f\", ($total_in * 3 / 1000000) + ($total_out * 15 / 1000000) }")
else
    cost="0.000"
fi

# Compact count: not available in JSON — track via session file
session_id=$(echo "$input" | grep -o '"session_id":"[^"]*"' | head -1 | sed 's/"session_id":"//;s/"//')
compact_file="/tmp/claude_compacts_${session_id}.txt"
compact_count=0
[ -f "$compact_file" ] && compact_count=$(cat "$compact_file")

# Context color + phase label
if [ "$ctx" != "?" ]; then
    if [ "$ctx" -lt 30 ]; then
        ctx_color="\033[32m"   # green — early session
        ctx_phase="fresh"
    elif [ "$ctx" -lt 60 ]; then
        ctx_color="\033[32m"   # green — mid session
        ctx_phase="mid"
    elif [ "$ctx" -le 80 ]; then
        ctx_color="\033[33m"   # yellow — getting full
        ctx_phase="filling"
    else
        ctx_color="\033[31m"   # red — near limit
        ctx_phase="FULL"
    fi
    ctx_str=$(printf "%b%s%%\033[0m(%s)" "$ctx_color" "$ctx" "$ctx_phase")
else
    ctx_str="?(unknown)"
fi

# Compact indicator
if [ "$compact_count" -eq 0 ]; then
    compact_str="no-compact"
else
    compact_str=$(printf "\033[33mcompact x%s\033[0m" "$compact_count")
fi

printf "%s | %s | %s | ctx:%s | \$%s | %s" \
    "$cwd_basename" "$branch" "$model" "$ctx_str" "$cost" "$compact_str"
