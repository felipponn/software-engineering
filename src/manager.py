from ..utils.connect_db import execute_query, execute_query_fetchone
from datetime import datetime

class Manager(User):
    def __init__(self, name: str, email: str, password: str, phone_number: str, user_id=None):
        super().__init__(name, email, password, phone_number, user_id)

    def view_all_issues(self):
        """
        Fetches all reported issues from the database and returns a list of formatted issues.
        """
        query = """
                SELECT issue_id, machine_id, issue_type, description
                FROM User_Reports;
                """
        
        # Fetch all issues from the database
        issues = execute_query(query)
        
        if issues:
            return [f"Issue ID: {issue[0]}, Machine ID: {issue[1]}, Type: {issue[2]}, Description: {issue[3]}" for issue in issues]
        else:
            print("No issues found.")
            return []

    def view_issues_by_machine(self, machine_id):
        """
        Fetches all reported issues for a specific machine from the database.
        """
        query = """
                SELECT issue_id, machine_id, issue_type, description
                FROM User_Reports
                WHERE machine_id = %s;
                """
        
        # Fetch issues related to a specific machine
        issues = execute_query(query, (machine_id,))
        
        if issues:
            return [f"Issue ID: {issue[0]}, Machine ID: {issue[1]}, Type: {issue[2]}, Description: {issue[3]}" for issue in issues]
        else:
            print(f"No issues found for machine {machine_id}.")
            return []
