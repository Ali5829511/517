#!/bin/bash

# Script to check for merge conflicts in open pull requests
# Usage: ./check_pr_conflicts.sh

echo "========================================="
echo "فحص تعارضات طلبات السحب | PR Conflict Checker"
echo "========================================="
echo ""

# Array of branch names from open PRs
branches=(
    "copilot/link-image-analysis-system"
    "revert-44-copilot/run-project-on-xampp-server"
    "copilot/complete-commit-and-publish-update"
    "copilot/fix-update-reflection-issue"
    "copilot/complete-naming-requirements"
    "copilot/complete-and-verify-commitments"
    "copilot/redesign-homepage-layout"
    "copilot/check-for-new-updates"
    "copilot/fix-issue-identified"
    "copilot/update-unknown-issue"
    "copilot/fix-module-not-found-error"
    "copilot/fix-unknown-issue"
    "copilot/complete-all-commitments"
)

# PR numbers corresponding to branches
pr_numbers=(
    "62"
    "46"
    "45"
    "43"
    "42"
    "39"
    "37"
    "33"
    "32"
    "31"
    "25"
    "24"
    "21"
)

# Fetch all branches
echo "جاري جلب جميع الفروع... | Fetching all branches..."
git fetch --all --quiet
echo "✅ تم جلب الفروع | Branches fetched"
echo ""

# Check each branch for conflicts
for i in "${!branches[@]}"; do
    branch="${branches[$i]}"
    pr="${pr_numbers[$i]}"
    
    echo "----------------------------------------"
    echo "فحص PR #$pr | Checking PR #$pr"
    echo "الفرع | Branch: $branch"
    echo "----------------------------------------"
    
    # Check if branch exists
    if ! git rev-parse --verify "origin/$branch" &>/dev/null; then
        echo "⚠️  الفرع غير موجود | Branch not found"
        echo ""
        continue
    fi
    
    # Get merge base
    merge_base=$(git merge-base main "origin/$branch" 2>/dev/null)
    
    if [ -z "$merge_base" ]; then
        echo "⚠️  لا يمكن إيجاد نقطة التفرع | Cannot find merge base"
        echo ""
        continue
    fi
    
    # Check for conflicts using merge-tree
    conflict_output=$(git merge-tree "$merge_base" main "origin/$branch" 2>&1)
    
    # Count conflicts
    conflict_count=$(echo "$conflict_output" | grep -c "^changed in both" || true)
    
    if [ "$conflict_count" -gt 0 ]; then
        echo "❌ تعارضات موجودة | CONFLICTS DETECTED: $conflict_count"
        echo "الملفات المتعارضة | Conflicting files:"
        echo "$conflict_output" | grep "^changed in both" | head -5
        if [ "$conflict_count" -gt 5 ]; then
            echo "... و $((conflict_count - 5)) ملفات أخرى | and $((conflict_count - 5)) more files"
        fi
    else
        echo "✅ لا توجد تعارضات | No conflicts detected"
    fi
    
    # Check if branch is behind main
    commits_behind=$(git rev-list --count "origin/$branch..main" 2>/dev/null || echo "0")
    commits_ahead=$(git rev-list --count "main..origin/$branch" 2>/dev/null || echo "0")
    
    echo "📊 الحالة | Status:"
    echo "  - متأخر عن main بـ | Behind main by: $commits_behind commits"
    echo "  - متقدم عن main بـ | Ahead of main by: $commits_ahead commits"
    
    if [ "$commits_behind" -gt 0 ]; then
        echo "  ⚠️  يحتاج تحديث | Needs rebase/merge from main"
    fi
    
    echo ""
done

echo "========================================="
echo "انتهى الفحص | Check Complete"
echo "========================================="
echo ""
echo "📝 للمزيد من المعلومات، راجع: | For more info, see:"
echo "   PR_MANAGEMENT_GUIDE.md"
