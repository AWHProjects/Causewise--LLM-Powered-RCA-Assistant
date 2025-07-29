import psutil
import time
from threading import Thread
import json

class SystemMonitor:
    def __init__(self):
        self.monitoring = False
        self.stats = {
            'cpu_percent': 0,
            'memory_percent': 0,
            'memory_used_mb': 0,
            'memory_total_mb': 0,
            'disk_usage_percent': 0,
            'network_sent_mb': 0,
            'network_recv_mb': 0
        }
    
    def get_current_stats(self):
        """Get current system statistics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = round(memory.used / (1024 * 1024), 2)
            memory_total_mb = round(memory.total / (1024 * 1024), 2)
            
            # Disk usage (root directory)
            disk = psutil.disk_usage('/')
            disk_usage_percent = round((disk.used / disk.total) * 100, 2)
            
            # Network I/O
            network = psutil.net_io_counters()
            network_sent_mb = round(network.bytes_sent / (1024 * 1024), 2)
            network_recv_mb = round(network.bytes_recv / (1024 * 1024), 2)
            
            self.stats = {
                'cpu_percent': round(cpu_percent, 1),
                'memory_percent': round(memory_percent, 1),
                'memory_used_mb': memory_used_mb,
                'memory_total_mb': memory_total_mb,
                'disk_usage_percent': disk_usage_percent,
                'network_sent_mb': network_sent_mb,
                'network_recv_mb': network_recv_mb,
                'timestamp': time.time()
            }
            
            return self.stats
        except Exception as e:
            return {
                'error': f"Failed to get system stats: {str(e)}",
                'cpu_percent': 0,
                'memory_percent': 0,
                'memory_used_mb': 0,
                'memory_total_mb': 0,
                'disk_usage_percent': 0,
                'network_sent_mb': 0,
                'network_recv_mb': 0,
                'timestamp': time.time()
            }
    
    def get_process_info(self):
        """Get information about the current Python process"""
        try:
            process = psutil.Process()
            return {
                'pid': process.pid,
                'cpu_percent': round(process.cpu_percent(), 2),
                'memory_mb': round(process.memory_info().rss / (1024 * 1024), 2),
                'memory_percent': round(process.memory_percent(), 2),
                'threads': process.num_threads(),
                'status': process.status()
            }
        except Exception as e:
            return {'error': f"Failed to get process info: {str(e)}"}

# Global monitor instance
monitor = SystemMonitor()