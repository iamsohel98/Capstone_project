"""
In-memory metrics store for query count, latency, errors, and token usage.
"""

import threading
from dataclasses import dataclass, field


@dataclass
class MetricsStore:
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    total_queries: int = 0
    total_errors: int = 0
    total_latency_ms: float = 0.0
    token_usage_estimate: int = 0

    def record(self, latency_ms: float, tokens: int = 0) -> None:
        with self._lock:
            self.total_queries += 1
            self.total_latency_ms += latency_ms
            self.token_usage_estimate += tokens

    def record_error(self) -> None:
        with self._lock:
            self.total_errors += 1

    def summary(self) -> dict:
        with self._lock:
            avg_latency = (
                self.total_latency_ms / self.total_queries
                if self.total_queries > 0
                else 0.0
            )
            return {
                "total_queries": self.total_queries,
                "total_errors": self.total_errors,
                "avg_latency_ms": round(avg_latency, 2),
                "token_usage_estimate": self.token_usage_estimate,
                "estimated_cost_usd_concept": round(self.token_usage_estimate * 0.000002, 6),
            }


metrics_store = MetricsStore()
