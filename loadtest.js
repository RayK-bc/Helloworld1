import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';
import htmlReport from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

export const options = {
  stages: [
    { duration: '30s', target: 20 }, // 30 秒內 Ramp-up 到 20 users
    { duration: '1m', target: 20 },  // 壓測 1 分鐘
    { duration: '10s', target: 0 },   // Cool-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'], // 95% 請求需在 1 秒內完成 (因包含系統 ping 延遲)
  },
};

export default function () {
  // 打向你 main.py 裡面的 /api/v1/ping?host=127.0.0.1
  const res = http.get('http://localhost:8000/api/v1/ping?host=127.0.0.1');

  // 驗證 Response HTTP Code 係否 200
  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  // 1 至 5 秒隨機等待再發起下一次 Request
  sleep(randomIntBetween(1, 5));
}

export function handleSummary(data) {
  return {
    'summary.html': htmlReport(data),
  };
}