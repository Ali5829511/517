#!/bin/bash
# تنفيذ تلقائي كامل لإكمال جميع طلبات السحب
# Full Automatic Execution to Complete All Pull Requests
# 
# Usage: ./AUTO_COMPLETE_PRS.sh
#
# This script will automatically execute all PR operations
# without requiring manual confirmation for each step.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Logging function
log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_action() {
    echo -e "${CYAN}🚀 $1${NC}"
}

# Banner
echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║                                                                   ║${NC}"
echo -e "${MAGENTA}║         🚀 التنفيذ التلقائي لإكمال طلبات السحب 🚀               ║${NC}"
echo -e "${MAGENTA}║         Automatic PR Completion Execution                        ║${NC}"
echo -e "${MAGENTA}║                                                                   ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check prerequisites
log_info "Checking prerequisites..."

if ! command -v gh &> /dev/null; then
    log_error "GitHub CLI (gh) is not installed"
    echo "Install from: https://cli.github.com/"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    log_error "Not authenticated with GitHub CLI"
    echo "Run: gh auth login"
    exit 1
fi

log_success "Prerequisites check passed"
echo ""

# Counter for tracking
MERGED_COUNT=0
CLOSED_COUNT=0
FAILED_COUNT=0

# Function to merge PR
merge_pr() {
    local pr_num=$1
    local description=$2
    
    log_action "Merging PR #$pr_num: $description"
    
    if gh pr merge $pr_num --squash --delete-branch 2>&1; then
        log_success "PR #$pr_num merged successfully"
        ((MERGED_COUNT++))
        return 0
    else
        log_error "Failed to merge PR #$pr_num"
        ((FAILED_COUNT++))
        return 1
    fi
}

# Function to close PR
close_pr() {
    local pr_num=$1
    local reason=$2
    
    log_action "Closing PR #$pr_num: $reason"
    
    if gh pr close $pr_num --comment "$reason" 2>&1; then
        log_success "PR #$pr_num closed successfully"
        ((CLOSED_COUNT++))
        return 0
    else
        log_error "Failed to close PR #$pr_num"
        ((FAILED_COUNT++))
        return 1
    fi
}

# Function to mark PR as ready
ready_pr() {
    local pr_num=$1
    
    log_action "Marking PR #$pr_num as ready (removing draft status)"
    
    if gh pr ready $pr_num 2>&1; then
        log_success "PR #$pr_num marked as ready"
        return 0
    else
        log_warning "Could not mark PR #$pr_num as ready (may already be ready)"
        return 1
    fi
}

echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                   المرحلة 1: الإجراءات الفورية                     ${NC}"
echo -e "${YELLOW}                   Phase 1: Immediate Actions                       ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Step 1: Close duplicate PR #70
close_pr 70 "Duplicate of PR #69. All functionality is covered in PR #69."

sleep 2

# Step 2: Merge PR #62 - Plate Recognizer
merge_pr 62 "Plate Recognizer & Takamul Integration"

sleep 2

# Step 3: Merge PR #37 - Homepage Redesign
ready_pr 37  # Remove draft status first
sleep 1
merge_pr 37 "Homepage Redesign"

sleep 2

# Step 4: Merge PR #33 - Deployment Verification
merge_pr 33 "Deployment Verification & AI Improvements"

sleep 2

echo ""
log_info "المرحلة 1 مكتملة | Phase 1 Complete"
echo ""

echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                  المرحلة 2: تحسينات الجودة                        ${NC}"
echo -e "${YELLOW}                  Phase 2: Quality Improvements                     ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Step 5: Merge PR #32 - PEP 8
merge_pr 32 "PEP 8 Compliance fixes"

sleep 2

# Step 6: Merge PR #25 - OpenAI Init
merge_pr 25 "OpenAI initialization security fix"

sleep 2

# Step 7: Merge PR #42 - Labeling System
merge_pr 42 "GitHub issue/PR labeling system"

sleep 2

# Step 8: Merge PR #43 - Deployment Automation
merge_pr 43 "Deployment reflection fix (CI/CD)"

sleep 2

echo ""
log_info "المرحلة 2 مكتملة | Phase 2 Complete"
echo ""

echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                المرحلة 3: حل تداخل المصادقة                       ${NC}"
echo -e "${YELLOW}                Phase 3: Authentication Resolution                  ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo ""

log_info "Consolidating 4 authentication PRs into PR #31 (most complete)"

# Step 9: Merge PR #31 - Authentication (the chosen one)
merge_pr 31 "Complete Authentication System (consolidated)"

sleep 2

# Step 10-12: Close the other authentication PRs
close_pr 21 "Superseded by PR #31. Authentication functionality consolidated in PR #31."

sleep 1

close_pr 24 "Superseded by PR #31. Security features consolidated in PR #31."

sleep 1

close_pr 39 "Superseded by PR #31. Authentication and image sorting consolidated in PR #31."

sleep 2

echo ""
log_info "المرحلة 3 مكتملة | Phase 3 Complete"
echo ""

echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                      قرار XAMPP                                    ${NC}"
echo -e "${YELLOW}                      XAMPP Decision                                 ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo ""

log_info "PR #46 removes XAMPP support (7,046 lines)"
log_warning "Skipping XAMPP decision - requires manual review"
log_info "To handle PR #46 later, run:"
echo "  - To remove XAMPP: gh pr merge 46 --squash --delete-branch"
echo "  - To keep XAMPP: gh pr close 46 --comment 'Keeping XAMPP support'"
echo ""

sleep 2

echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                   المرحلة 4: التنظيف النهائي                      ${NC}"
echo -e "${YELLOW}                   Phase 4: Final Cleanup                          ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════════${NC}"
echo ""

# Step 13: Merge PR #45 - Production Deployment
merge_pr 45 "Complete commits and production deployment"

sleep 2

echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║                                                                   ║${NC}"
echo -e "${MAGENTA}║                    🎉 التنفيذ مكتمل! 🎉                          ║${NC}"
echo -e "${MAGENTA}║                    Execution Complete!                           ║${NC}"
echo -e "${MAGENTA}║                                                                   ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Final summary
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}                         الملخص النهائي                             ${NC}"
echo -e "${GREEN}                         Final Summary                               ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════════${NC}"
echo ""

log_success "PRs Merged: $MERGED_COUNT"
log_success "PRs Closed: $CLOSED_COUNT"

if [ $FAILED_COUNT -gt 0 ]; then
    log_error "Failed Operations: $FAILED_COUNT"
fi

TOTAL_PROCESSED=$((MERGED_COUNT + CLOSED_COUNT))
echo ""
log_info "Total PRs Processed: $TOTAL_PROCESSED out of 15"

if [ $TOTAL_PROCESSED -ge 13 ]; then
    log_success "Excellent! Almost all PRs have been resolved! 🎊"
elif [ $TOTAL_PROCESSED -ge 10 ]; then
    log_success "Great progress! Most PRs resolved! 👍"
elif [ $TOTAL_PROCESSED -ge 5 ]; then
    log_info "Good start! Continue with remaining PRs."
else
    log_warning "Some issues occurred. Review the log above."
fi

echo ""
log_info "Remaining open PRs:"
gh pr list --state open

echo ""
log_action "Next steps:"
echo "  1. Review merged changes: git log --oneline -20"
echo "  2. Test the application: make test"
echo "  3. Deploy to production if tests pass"
echo "  4. Handle PR #46 (XAMPP) decision manually"
echo ""

log_success "✨ PR completion process finished! ✨"
