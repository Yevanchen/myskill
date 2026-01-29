#!/bin/bash

##############################################################################
# Blog Publishing Script
# 
# Usage: ./publish.sh [mdx-file]
# Example: ./publish.sh my-article.mdx
#
# This script publishes an MDX blog post to Firebase Firestore.
# Requires: BLOG_AUTH_TOKEN environment variable
##############################################################################

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if file argument provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}📝 Blog Publishing Script${NC}"
    echo
    echo "Usage: $0 <mdx-file>"
    echo
    echo "Examples:"
    echo "  $0 my-article.mdx"
    echo "  $0 ~/Desktop/draft.mdx"
    echo
    echo "Environment:"
    echo "  BLOG_AUTH_TOKEN - Set to your publishing token"
    echo
    exit 1
fi

MDX_FILE="$1"

# Validate file exists
if [ ! -f "$MDX_FILE" ]; then
    echo -e "${RED}❌ File not found: $MDX_FILE${NC}"
    exit 1
fi

# Validate auth token is set
if [ -z "$BLOG_AUTH_TOKEN" ]; then
    echo -e "${RED}❌ BLOG_AUTH_TOKEN not set${NC}"
    echo
    echo "Set it with:"
    echo "  export BLOG_AUTH_TOKEN=\"sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c\""
    echo
    exit 1
fi

echo -e "${GREEN}🚀 Publishing blog post...${NC}"
echo "📄 File: $MDX_FILE"
echo

# Run Python script
python3 "$(dirname "$0")/publish.py" "$MDX_FILE"

exit $?
