from utils.connect_db import execute_query
from datetime import datetime
from backend.user import User

class Manager(User):
    """
    A class representing a Manager in the system, allowing for actions like viewing all reported issues.

    Attributes:
    -
    """
    def __init__(self, user_name: str, password: str, email: str, phone: str, user_id=None):
        super().__init__(user_name, password, email, phone, user_id)

    def view_all_issues(self, issue=None, machine=None, type=None, description=None):
        """
        Fetches all reported issues from the database based on optional filters for issue, machine, type, and description.
        Returns a list of dictionaries representing the issues.
        """
        # Base query
        query = """
            SELECT report_id, user_id, machine_id, report_target, issue_type, description, status, created_at, resolved_at
            FROM User_Reports
            WHERE 1=1
        """
        
        # List to hold query parameters
        params = []

        # Apply filters if provided
        if issue:
            query += " AND report_id = %s"
            params.append(issue)
        
        if machine:
            query += " AND machine_id = %s"
            params.append(machine)
        
        if type:
            query += " AND issue_type = %s"
            params.append(type)
        
        if description:
            query += " AND description ILIKE %s"
            params.append(f'%{description}%')

        # Execute the query with the filters
        issues = execute_query(query, tuple(params))

        # Return a structured list of issues
        return [
            {
                'report_id': issue[0],
                'user_id': issue[1],
                'machine_id': issue[2],
                'report_target': issue[3],
                'issue_type': issue[4],
                'description': issue[5],
                'status': issue[6],
                'created_at': issue[7],
                'resolved_at': issue[8],
            } for issue in issues
        ]
