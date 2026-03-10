export function formatDateTime(value) {
  if (!value) {
    return '-';
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString('zh-CN', { hour12: false });
}


export function formatMetricSummary(metric) {
  if (!metric) {
    return '-';
  }
  const map50 = metric.map50 ?? '-';
  const map5095 = metric.map50_95 ?? '-';
  return `mAP50 ${map50} / mAP50-95 ${map5095}`;
}
