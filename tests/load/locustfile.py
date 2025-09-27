import requests
from locust import HttpUser, between, task


class ApiUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        login_data = {"username": "testuser", "password": "testpass"}
        try:
            response = self.client.post("/auth/login", json=login_data)
            print(
                f"on_start Login: Status {response.status_code}, Response {response.text}"
            )
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                print(f"Login successful: Token {self.access_token[:10]}...")
                # Create an initial expense
                headers = {"Authorization": f"Bearer {self.access_token}"}
                expense_data = {"description": "Test expense", "amount": 10.0}
                response = self.client.post(
                    "/expenses/", json=expense_data, headers=headers
                )
                print(
                    f"on_start Create expense: Status {response.status_code}, Response {response.text}"
                )
                if response.status_code == 200:
                    expense = response.json()
                    self.expense_id = expense["id"]
                    print(f"Created expense ID: {self.expense_id}")
                else:
                    self.expense_id = None
                    print("Failed to create expense for PUT/DELETE")
            else:
                self.access_token = None
                self.expense_id = None
                print(
                    f"Login failed: Status {response.status_code}, Response {response.text}"
                )
        except requests.exceptions.ConnectionError:
            self.access_token = None
            self.expense_id = None
            print("Login failed: Cannot connect to server at {self.host}")

    @task(1)
    def login(self):
        login_data = {"username": "testuser", "password": "testpass"}
        try:
            response = self.client.post("/auth/login", json=login_data)
            print(
                f"Login task: Status {response.status_code}, Response {response.text}"
            )
        except requests.exceptions.ConnectionError:
            print(
                "Login task failed: Cannot connect to server at {self.host}"
            )

    @task(3)
    def get_expenses(self):
        if self.access_token:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            try:
                response = self.client.get("/expenses/", headers=headers)
                print(
                    f"Get expenses: Status {response.status_code}, Response {response.text}"
                )
            except requests.exceptions.ConnectionError:
                print(
                    "Get expenses failed: Cannot connect to server at {self.host}"
                )
        else:
            print("No token, skip get expenses")

    @task(2)
    def create_expense(self):
        if self.access_token:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            expense_data = {"description": "Test expense", "amount": 10.0}
            try:
                response = self.client.post(
                    "/expenses/", json=expense_data, headers=headers
                )
                print(
                    f"Create expense: Status {response.status_code}, Response {response.text}"
                )
                if response.status_code == 200:
                    expense = response.json()
                    self.expense_id = expense["id"]
                    print(f"Created expense ID: {self.expense_id}")
            except requests.exceptions.ConnectionError:
                print(
                    "Create expense failed: Cannot connect to server at {self.host}"
                )
        else:
            print("No token, skip create expense")

    @task(2)
    def update_expense(self):
        if self.access_token:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            if not self.expense_id:
                expense_data = {"description": "Test expense", "amount": 10.0}
                try:
                    response = self.client.post(
                        "/expenses/", json=expense_data, headers=headers
                    )
                    print(
                        f"Update expense create: Status {response.status_code}, Response {response.text}"
                    )
                    if response.status_code == 200:
                        expense = response.json()
                        self.expense_id = expense["id"]
                        print(
                            f"Created expense ID for update: {self.expense_id}"
                        )
                    else:
                        print("Failed to create expense for update")
                        return
                except requests.exceptions.ConnectionError:
                    print(
                        "Update expense create failed: Cannot connect to server at {self.host}"
                    )
                    return
            update_data = {"description": "Updated expense", "amount": 15.0}
            try:
                response = self.client.put(
                    f"/expenses/{self.expense_id}",
                    json=update_data,
                    headers=headers,
                )
                print(
                    f"Update expense: Status {response.status_code}, Response {response.text}"
                )
            except requests.exceptions.ConnectionError:
                print(
                    "Update expense failed: Cannot connect to server at {self.host}"
                )
        else:
            print("No token, skip update expense")

    @task(1)
    def delete_expense(self):
        if self.access_token:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            if not self.expense_id:
                expense_data = {"description": "Test expense", "amount": 10.0}
                try:
                    response = self.client.post(
                        "/expenses/", json=expense_data, headers=headers
                    )
                    print(
                        f"Delete expense create: Status {response.status_code}, Response {response.text}"
                    )
                    if response.status_code == 200:
                        expense = response.json()
                        self.expense_id = expense["id"]
                        print(
                            f"Created expense ID for delete: {self.expense_id}"
                        )
                    else:
                        print("Failed to create expense for delete")
                        return
                except requests.exceptions.ConnectionError:
                    print(
                        "Delete expense create failed: Cannot connect to server at {self.host}"
                    )
                    return
            try:
                response = self.client.delete(
                    f"/expenses/{self.expense_id}", headers=headers
                )
                print(
                    f"Delete expense: Status {response.status_code}, Response {response.text}"
                )
                self.expense_id = None
            except requests.exceptions.ConnectionError:
                print(
                    "Delete expense failed: Cannot connect to server at {self.host}"
                )
        else:
            print("No token, skip delete expense")
