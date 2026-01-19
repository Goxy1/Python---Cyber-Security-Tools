import psutil
import time
import socket
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

class SystemMonitor:
    def __init__(self, cpu_threshold=80, memory_threshold=85, disk_threshold=90):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.alerts = []

    def check_cpu_usage(self):
        #Monitor CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > self.cpu_threshold:
            alert = {
                'type': 'CPU_HIGH',
                'value': cpu_percent,
                'threshold': self.cpu_threshold,
                'timestamp': datetime.now().isoformat(),
                'message': f'High CPU usage detected: {cpu_percent}%'
            }
            self.alerts.append(alert)
            return alert
        return None
    
    def check_memory_usage(self):
        #Monitor memory usage
        memory = psutil.virtual_memory()
        if memory.percent > self.memory_threshold:
            alert = {
                'type': 'MEMORY_HIGH',
                'value': memory.percent,
                'threshold': self.memory_threshold,
                'timestamp': datetime.now().isoformat(),
                'message': f'High memory usage detected: {memory.percent}%'
            }
            self.alerts.append(alert)
            return alert
        return None
    
    def check_disk_usage(self):
        #Monitor disk usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > self.disk_threshold:
            alert = {
                'type': 'DISK_USAGE_HIGH',
                'value': disk.percent,
                'threshold': self.disk_threshold,
                'timestamp': datetime.now().isoformat(),
                'message': f'High DISK usage detected: {disk.percent}%'
            }

    def check_network_connections(self):
        #Monitor network connections for suspicious activity
        connections = psutil.net_connections(kind = 'inet')
        suspicious_ports = [22, 23, 135, 139, 445, 3389] #Common attack targets

        alerts = []
        for conn in connections:
            if conn.laddr and conn.laddr.port in suspicious_ports and conn.status == "LISTEN":
                alert = {
                    'type': 'SUSPICIOUS_PORT',
                    'port': conn.laddr.port,
                    'status': conn.status,
                    'timestamp': datetime.now().isoformat(),
                    'message': f'Suspicious port {conn.laddr.port} is listening'
                }
                alerts.append(alert)
                self.alerts.append(alert)

        return alerts
    
    def check_running_processes(self):
        #Monitor for suspicious processes
        suspicious_names = ['nc', 'netcat', 'nmap', 'metasploit'] #Example suspicious process names
        alerts = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if any(sus in proc.info['name'].lower() for sus in suspicious_names):
                    alert = {
                        'type': 'SUSPICIOUS_PROCESS',
                        'process': proc.info['name'],
                        'pid': proc.info['pid'],
                        'cpu': proc.info['cpu_percent'],
                        'timestamp': datetime.now().isoformat(),
                        'message': f'Suspicious process detected: {proc.info["name"]} (PID: {proc.info["pid"]})'
                    }
                    alerts.append(alert)
                    self.alerts.append(alert)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return alerts
    
    def get_system_info(self):
        #Get current system information
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100,
            'network_connections': len(psutil.net_connections()),
            'running_processes': len(psutil.pids())
        }
    
    def log_to_file(self, data, filename='system_monitor.log'):
        #Log system information and alerts to file
        with open(filename, 'a') as f:
            f.write(json.dumps(data) + '\n')
    
    def send_email_alert(self, alert, smtp_server='localhost', from_email='monitor@localhost'):
        #Send email alert (requires SMTP configuration)
        try:
            msg = MIMEText(f"SECURITY ALERT: {alert['message']}\n\nTimestamp: {alert['timestamp']}")
            msg['Subject'] = f"System Alert: {alert['type']}"
            msg['From'] = from_email
            msg['To'] = 'admin@localhost'
            
            #This is a placeholder - configure your SMTP settings
            #server = smtplib.SMTP(smtp_server)
            #server.send_message(msg)
            #server.quit()
            print(f"Email alert would be sent: {alert['message']}")
        except Exception as e:
            print(f"Failed to send email alert: {e}")
    
    def run_monitoring_cycle(self):
        #Run one complete monitoring cycle
        print(f"\n=== System Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        
        # Check all metrics
        cpu_alert = self.check_cpu_usage()
        memory_alert = self.check_memory_usage()
        disk_alert = self.check_disk_usage()
        network_alerts = self.check_network_connections()
        process_alerts = self.check_running_processes()
        
        # Get system info
        sys_info = self.get_system_info()
        print(f"CPU: {sys_info['cpu_percent']}% | Memory: {sys_info['memory_percent']}% | Disk: {sys_info['disk_percent']:.1f}%")
        
        # Handle alerts
        all_alerts = [cpu_alert, memory_alert, disk_alert] + network_alerts + process_alerts
        active_alerts = [alert for alert in all_alerts if alert is not None]
        
        if active_alerts:
            print(f"\n🚨 ALERTS DETECTED ({len(active_alerts)}):")
            for alert in active_alerts:
                print(f"  - {alert['message']}")
                self.send_email_alert(alert)
        else:
            print("✅ All systems normal")
        
        # Log everything
        log_entry = {
            'system_info': sys_info,
            'alerts': active_alerts
        }
        self.log_to_file(log_entry)
        
        return active_alerts

def main():
    #Main monitoring loop
    monitor = SystemMonitor()
    
    print("🛡️  System Health Monitor Starting...")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        while True:
            monitor.run_monitoring_cycle()
            time.sleep(30)  # Check every 30 seconds
    except KeyboardInterrupt:
        print("\n\n📊 Monitoring stopped. Final report:")
        print(f"Total alerts generated: {len(monitor.alerts)}")
        
        # Show alert summary
        alert_types = {}
        for alert in monitor.alerts:
            alert_types[alert['type']] = alert_types.get(alert['type'], 0) + 1
        
        for alert_type, count in alert_types.items():
            print(f"  - {alert_type}: {count}")

if __name__ == "__main__":
    main()
