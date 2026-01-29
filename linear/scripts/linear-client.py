#!/usr/bin/env python3
"""
Linear API client for common operations
"""

import os
import json
import subprocess
import sys
from typing import Dict, Any, Optional

class LinearClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('LINEARAPIKEY', '')
        self.endpoint = 'https://api.linear.app/graphql'
        
        if not self.api_key:
            raise ValueError("Missing LINEARAPIKEY environment variable")
    
    def query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute GraphQL query or mutation"""
        
        payload = {
            "query": query
        }
        
        if variables:
            payload["variables"] = variables
        
        cmd = [
            'curl', '-s', '-X', 'POST',
            self.endpoint,
            '-H', f'Authorization: {self.api_key}',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(payload, ensure_ascii=False)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        response = json.loads(result.stdout)
        
        return response
    
    def get_viewer(self) -> Dict[str, Any]:
        """Get authenticated user info"""
        query = """
        query {
          viewer {
            id
            name
            email
          }
        }
        """
        return self.query(query)
    
    def get_teams(self) -> Dict[str, Any]:
        """List all teams"""
        query = """
        query {
          teams {
            nodes {
              id
              name
              projects {
                nodes {
                  id
                  name
                }
              }
            }
          }
        }
        """
        return self.query(query)
    
    def create_issue(self, team_id: str, project_id: str, title: str, 
                     description: str = "") -> Dict[str, Any]:
        """Create a new issue"""
        mutation = """
        mutation CreateIssue($input: IssueCreateInput!) {
          issueCreate(input: $input) {
            issue {
              id
              identifier
              title
              url
            }
          }
        }
        """
        
        variables = {
            "input": {
                "teamId": team_id,
                "projectId": project_id,
                "title": title,
                "description": description
            }
        }
        
        return self.query(mutation, variables)
    
    def update_issue(self, issue_id: str, **updates) -> Dict[str, Any]:
        """Update an issue"""
        mutation = """
        mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
          issueUpdate(id: $id, input: $input) {
            issue {
              id
              identifier
              title
              state { id name }
            }
          }
        }
        """
        
        variables = {
            "id": issue_id,
            "input": updates
        }
        
        return self.query(mutation, variables)
    
    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """Get issue details"""
        query = """
        query GetIssue($id: String!) {
          issue(id: $id) {
            id
            identifier
            title
            description
            state { id name }
            assignee { id name }
            createdAt
            url
          }
        }
        """
        
        variables = {"id": issue_id}
        return self.query(query, variables)
    
    def get_team_issues(self, team_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get issues for a team"""
        query = """
        query GetTeamIssues($teamId: String!, $first: Int!) {
          team(id: $teamId) {
            id
            name
            issues(first: $first) {
              nodes {
                id
                identifier
                title
                state { name }
                assignee { name }
              }
            }
          }
        }
        """
        
        variables = {
            "teamId": team_id,
            "first": limit
        }
        
        return self.query(query, variables)

def main():
    """Demo CLI"""
    
    try:
        client = LinearClient()
        
        # Test connection
        print("🔐 Testing authentication...")
        viewer = client.get_viewer()
        
        if 'data' in viewer and viewer['data'].get('viewer'):
            user = viewer['data']['viewer']
            print(f"✅ Authenticated as: {user['name']} ({user['email']})")
        else:
            print(f"❌ Auth failed: {viewer}")
            sys.exit(1)
        
        # List teams
        print("\n📋 Teams available:")
        teams = client.get_teams()
        
        if 'data' in teams and teams['data'].get('teams'):
            for team in teams['data']['teams']['nodes']:
                print(f"  • {team['name']} (id: {team['id']})")
                for project in team['projects']['nodes']:
                    print(f"    - {project['name']}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
