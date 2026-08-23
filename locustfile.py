from locust import HttpUser, task, between

class APIUser(HttpUser):
    # 每個模擬使用者發送 Request 之間隨機等待 0.1 ~ 0.5 秒
    wait_time = between(0.1, 0.5)

    @task(3) # 權重為 3，較常觸發
    def test_health(self):
        self.client.get("/api/v1/health")

    @task(1) # 權重為 1
    def test_get_item(self):
        self.client.get("/api/v1/items/100")