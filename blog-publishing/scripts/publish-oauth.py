#!/usr/bin/env python3
"""
Publish blog to Firebase using Google OAuth 2.0 token
"""

import os
import json
import base64
import subprocess
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Tuple

# Get credentials from environment
CLIENT_EMAIL = os.getenv('client_email', '')
PRIVATE_KEY_B64 = os.getenv('private_key', '')
PROJECT_ID = 'myblog-personal'

if not CLIENT_EMAIL or not PRIVATE_KEY_B64:
    print("❌ Missing credentials: client_email, private_key")
    exit(1)

# Convert base64 private key to PEM format
def format_private_key(key_b64: str) -> str:
    """Convert base64 key to PEM format"""
    # Add PEM headers
    pem = "-----BEGIN RSA PRIVATE KEY-----\n"
    
    # Add key in 64-char chunks (PEM standard)
    key_clean = key_b64.replace('\n', '').replace('\\n', '')
    for i in range(0, len(key_clean), 64):
        pem += key_clean[i:i+64] + "\n"
    
    pem += "-----END RSA PRIVATE KEY-----"
    return pem

def create_jwt_and_get_token(client_email: str, private_key: str) -> str:
    """Create JWT and exchange for access token"""
    
    # Write private key to temp file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as f:
        f.write(private_key)
        key_file = f.name
    
    try:
        # Create JWT
        header = {"alg": "RS256", "typ": "JWT"}
        
        now = int(time.time())
        payload = {
            "iss": client_email,
            "scope": "https://www.googleapis.com/auth/cloud-platform",
            "aud": "https://oauth2.googleapis.com/token",
            "exp": now + 3600,
            "iat": now
        }
        
        # Encode
        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        message = f"{header_b64}.{payload_b64}"
        
        # Sign with openssl
        cmd = ['openssl', 'dgst', '-sha256', '-sign', key_file]
        result = subprocess.run(
            cmd,
            input=message.encode(),
            capture_output=True
        )
        
        if result.returncode != 0:
            raise Exception(f"Signing failed: {result.stderr.decode()}")
        
        signature = base64.urlsafe_b64encode(result.stdout).decode().rstrip('=')
        jwt = f"{message}.{signature}"
        
        # Exchange for access token
        data = f'grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion={jwt}'
        
        cmd = [
            'curl', '-s', '-X', 'POST',
            'https://oauth2.googleapis.com/token',
            '-H', 'Content-Type: application/x-www-form-urlencoded',
            '-d', data
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        response = json.loads(result.stdout)
        
        if 'access_token' in response:
            return response['access_token']
        else:
            raise Exception(f"Token exchange failed: {response.get('error_description', response)}")
    
    finally:
        os.unlink(key_file)

def extract_frontmatter(mdx_content: str) -> Tuple[Dict[str, Any], str]:
    """Extract frontmatter and content"""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', mdx_content, re.DOTALL)
    
    if not match:
        raise ValueError("Invalid frontmatter format")
    
    frontmatter_str = match.group(1)
    content = match.group(2)
    
    frontmatter = {}
    for line in frontmatter_str.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            elif value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.startswith('[') and value.endswith(']'):
                value_str = value[1:-1]
                value = [v.strip().strip("'\"") for v in value_str.split(',')] if value_str else []
            
            frontmatter[key] = value
    
    return frontmatter, content

def create_slug(title: str) -> str:
    """Generate slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s]', '', slug)
    slug = slug.strip()
    slug = re.sub(r'\s+', '-', slug)
    
    if not slug or slug == '-':
        import random, string
        random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        slug = f'post-{random_id}'
    
    return slug

def publish_to_firestore(doc_id: str, blog_data: dict, access_token: str) -> bool:
    """Publish to Firebase using OAuth token"""
    
    API_KEY = 'AIzaSyBIFQnsOpMZ38H-KXQgaE1YCS5gxoYXBxw'
    url = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/bloglist/{doc_id}?key={API_KEY}"
    
    # Build Firestore format
    firestore_doc = {'fields': {}}
    for key, value in blog_data.items():
        if isinstance(value, str):
            firestore_doc['fields'][key] = {'stringValue': value}
        elif isinstance(value, bool):
            firestore_doc['fields'][key] = {'booleanValue': value}
        elif isinstance(value, list):
            firestore_doc['fields'][key] = {
                'arrayValue': {
                    'values': [{'stringValue': str(v)} for v in value]
                }
            }
    
    # Send request with OAuth token
    cmd = [
        'curl', '-s', '-X', 'PATCH',
        url,
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer {access_token}',
        '-d', json.dumps(firestore_doc)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        response = json.loads(result.stdout)
        if 'name' in response:
            return True
        elif 'error' in response:
            error = response['error'].get('message', 'Unknown error')
            print(f"  ❌ {error}")
            return False
    except:
        print(f"  ❌ Response parse error")
        return False

def main():
    mdx_file = Path('/home/node/clawd/clawdbot-workflow.mdx')
    
    if not mdx_file.exists():
        print(f"❌ File not found: {mdx_file}")
        return 1
    
    print("\n" + "="*50)
    print("  📝 Publishing to Firebase (OAuth 2.0)")
    print("="*50 + "\n")
    
    # Read file
    mdx_content = mdx_file.read_text(encoding='utf-8')
    
    # Parse
    try:
        frontmatter, content = extract_frontmatter(mdx_content)
    except Exception as e:
        print(f"❌ Parse error: {e}")
        return 1
    
    # Build document
    title = frontmatter.get('title', 'Untitled')
    slug = create_slug(title)
    
    blog_data = {
        'title': title,
        'slug': slug,
        'date': frontmatter.get('date', datetime.now().isoformat()),
        'tags': frontmatter.get('tags', []),
        'draft': frontmatter.get('draft', False),
        'summary': frontmatter.get('summary', ''),
        'content': content,
        'authors': frontmatter.get('authors', ['evanchen']),
        'lastmod': datetime.now().isoformat(),
        'fileName': mdx_file.name,
    }
    
    print(f"📖 Title: {title}")
    print(f"📝 Slug: {slug}")
    print(f"📋 Summary: {blog_data['summary'][:60]}...")
    print()
    
    # Get OAuth token
    print("🔐 Getting Google OAuth 2.0 token...")
    try:
        private_key = format_private_key(PRIVATE_KEY_B64)
        access_token = create_jwt_and_get_token(CLIENT_EMAIL, private_key)
        print("✅ Token obtained")
    except Exception as e:
        print(f"❌ Token generation failed: {e}")
        return 1
    
    print()
    print("🚀 Publishing to Firebase...")
    
    if publish_to_firestore(slug, blog_data, access_token):
        print(f"\n✅ Published successfully!")
        print(f"🔗 https://chenyefan.zeabur.app/blog/{slug}\n")
        return 0
    else:
        print(f"\n❌ Publish failed\n")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
