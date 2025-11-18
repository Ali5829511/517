#!/bin/bash

# Script to execute the PR completion plan
# نص تنفيذ خطة إكمال طلبات السحب
# Usage: ./EXECUTE_PR_PLAN.sh

set -e

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║         🚀 PR Completion Execution Script                         ║"
echo "║         نص تنفيذ إكمال طلبات السحب                               ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}❌ Not authenticated with GitHub CLI${NC}"
    echo "Run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Function to execute action with confirmation
execute_action() {
    local action="$1"
    local pr_number="$2"
    local description="$3"
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}Action: $action${NC}"
    echo -e "PR #$pr_number: $description"
    echo ""
    read -p "Execute this action? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        case $action in
            "MERGE")
                echo "Merging PR #$pr_number..."
                gh pr merge $pr_number --squash --delete-branch || echo -e "${RED}Failed to merge PR #$pr_number${NC}"
                ;;
            "CLOSE")
                echo "Closing PR #$pr_number..."
                gh pr close $pr_number --comment "Closing as recommended by PR analysis" || echo -e "${RED}Failed to close PR #$pr_number${NC}"
                ;;
            "READY")
                echo "Marking PR #$pr_number as ready..."
                gh pr ready $pr_number || echo -e "${RED}Failed to mark PR #$pr_number as ready${NC}"
                ;;
            *)
                echo -e "${RED}Unknown action: $action${NC}"
                ;;
        esac
        echo -e "${GREEN}✅ Action completed${NC}"
    else
        echo -e "${YELLOW}⏭️  Skipped${NC}"
    fi
    echo ""
}

# Function to show PR details
show_pr_details() {
    local pr_number="$1"
    echo -e "${BLUE}Viewing PR #$pr_number details...${NC}"
    gh pr view $pr_number
    echo ""
}

echo "═══════════════════════════════════════════════════════════════════"
echo "                    WEEK 1: IMMEDIATE ACTIONS"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Priority 1: Close duplicate
echo -e "${YELLOW}═══ Priority 1: Close Duplicate PR ═══${NC}"
show_pr_details 70
execute_action "CLOSE" 70 "Duplicate of PR #69 - Complete Pull Requests"

# Priority 2: Merge PR #62
echo -e "${YELLOW}═══ Priority 2: Merge Plate Recognizer ═══${NC}"
show_pr_details 62
execute_action "MERGE" 62 "Plate Recognizer & Takamul Integration (13/13 tests passing)"

# Priority 3: Merge PR #37
echo -e "${YELLOW}═══ Priority 3: Merge Homepage Redesign ═══${NC}"
show_pr_details 37
execute_action "READY" 37 "Mark as ready (remove draft status)"
execute_action "MERGE" 37 "Homepage Redesign (22/22 tasks complete)"

# Priority 4: Merge PR #33
echo -e "${YELLOW}═══ Priority 4: Merge Deployment Verification ═══${NC}"
show_pr_details 33
execute_action "MERGE" 33 "Deployment Verification & AI Improvements"

# Decision point: XAMPP
echo -e "${YELLOW}═══ Decision: XAMPP Support (PR #46) ═══${NC}"
show_pr_details 46
echo "This PR removes XAMPP deployment support (7,046 lines deleted)"
echo "Do you want to keep or remove XAMPP support?"
echo "1) Remove XAMPP (merge PR #46)"
echo "2) Keep XAMPP (close PR #46)"
read -p "Enter choice (1 or 2): " -n 1 -r
echo ""
if [[ $REPLY == "1" ]]; then
    execute_action "MERGE" 46 "Revert XAMPP deployment"
elif [[ $REPLY == "2" ]]; then
    execute_action "CLOSE" 46 "Keep XAMPP support"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "                  WEEK 2: QUALITY IMPROVEMENTS"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Quality improvements
execute_action "MERGE" 32 "PEP 8 Compliance fixes (91 violations)"
execute_action "MERGE" 25 "OpenAI initialization fix (security)"
execute_action "MERGE" 42 "GitHub issue/PR labeling system"
execute_action "MERGE" 43 "Deployment reflection fix (CI/CD)"

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "               WEEK 3: AUTHENTICATION CONSOLIDATION"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

echo "Four PRs work on authentication systems: #21, #24, #31, #39"
echo "PR #31 is recommended (7/8 tasks complete, most comprehensive)"
echo ""
echo "Review each authentication PR:"
echo ""

for pr in 21 24 31 39; do
    echo -e "${BLUE}─────────────────────────────────────────────────────────────────${NC}"
    show_pr_details $pr
    echo ""
done

echo "Which authentication PR do you want to keep?"
echo "1) PR #21 - Implement Secure Authentication"
echo "2) PR #24 - Security & Safety System"
echo "3) PR #31 - Complete Authentication (RECOMMENDED)"
echo "4) PR #39 - Authentication & Image Sorting"
read -p "Enter choice (1-4): " -n 1 -r
echo ""

chosen_pr=0
case $REPLY in
    1) chosen_pr=21 ;;
    2) chosen_pr=24 ;;
    3) chosen_pr=31 ;;
    4) chosen_pr=39 ;;
esac

if [ $chosen_pr -ne 0 ]; then
    execute_action "MERGE" $chosen_pr "Authentication system (chosen implementation)"
    
    # Close the others
    for pr in 21 24 31 39; do
        if [ $pr -ne $chosen_pr ]; then
            execute_action "CLOSE" $pr "Superseded by PR #$chosen_pr"
        fi
    done
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "                    WEEK 4: FINAL CLEANUP"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Review remaining PRs
echo "Remaining PRs to review:"
show_pr_details 45
execute_action "MERGE" 45 "Complete commits and production deployment"

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                    🎉 EXECUTION COMPLETE                          ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Summary of actions:"
gh pr list --state all --limit 20
echo ""
echo -e "${GREEN}✅ PR completion execution finished${NC}"
echo "Review the merged changes and verify everything works as expected."
