import time
from typing import Callable, Any
from functools import wraps


class PerformanceMonitor:
    """Monitor and track performance metrics."""

    def __init__(self):
        self.metrics = {}
        self.call_counts = {}

    def track(self, name: str):
        """Decorator to track function performance."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start_time

                if name not in self.metrics:
                    self.metrics[name] = []
                    self.call_counts[name] = 0

                self.metrics[name].append(elapsed)
                self.call_counts[name] += 1

                return result
            return wrapper
        return decorator

    def get_stats(self, name: str) -> dict:
        """Get statistics for a tracked function."""
        if name not in self.metrics or not self.metrics[name]:
            return {}

        times = self.metrics[name]
        return {
            'name': name,
            'calls': self.call_counts[name],
            'total_time': sum(times),
            'average_time': sum(times) / len(times),
            'min_time': min(times),
            'max_time': max(times)
        }

    def print_report(self):
        """Print performance report."""
        print("\n" + "="*60)
        print("PERFORMANCE REPORT")
        print("="*60)

        for name in sorted(self.metrics.keys()):
            stats = self.get_stats(name)
            print(f"\n{name}:")
            print(f"  Calls: {stats['calls']}")
            print(f"  Total: {stats['total_time']:.4f}s")
            print(f"  Average: {stats['average_time']:.6f}s")
            print(f"  Min: {stats['min_time']:.6f}s")
            print(f"  Max: {stats['max_time']:.6f}s")

    def clear(self):
        """Clear all metrics."""
        self.metrics.clear()
        self.call_counts.clear()


# Global performance monitor
perf_monitor = PerformanceMonitor()
