import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';
// ✅ 加了花括號 { htmlReport } 修正語法錯誤
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

export const options = {
  stages: [
    { duration: '30s', target: 2 }, // 30 秒內 Ramp-up 至 2 users
    { duration: '15s', target: 2 },  // 壓測 15 秒
    { duration: '10s', target: 0 },   // Cool-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
  },
};

export default function () {
  const res = http.get('http://localhost:8000/api/v1/ping?host=127.0.0.1');

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(randomIntBetween(1, 5));
}

// 自動生成 HTML 報告
export function handleSummary(data) {
  return {
    'summary.html': htmlReport(data),
  };
}