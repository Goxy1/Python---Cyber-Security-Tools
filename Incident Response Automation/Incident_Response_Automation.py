import subprocess
import platform
import sqlite3
from datetime import datetime, timedelta
import hashlib


class IncidentResponseTool:
    def __init__(self, db_path='incident_response_db.db'):
        self.db_path = db_path
        self.init_database()
        self.system_info = self.collect_system_info()
        
    def init_database(self):
        """Initialize incident response database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                incident_type TEXT,
                severity TEXT,
                description TEXT,
                evidence_collected TEXT,
                status TEXT DEFAULT 'OPEN'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id INTEGER,
                evidence_type TEXT,
                file_path TEXT,
                hash_value TEXT,
                timestamp TEXT,
                FOREIGN KEY (incident_id) REFERENCES incidents (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def collect_system_info(self):
        """Collect basic system information"""
        return {
            'hostname': platform.node(),
            'os': platform.system(),
            'os_version': platform.release(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'timestamp': datetime.now().isoformat()
        }
    
    def create_incident(self, incident_type, severity, description):
        """Create new incident record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO incidents (timestamp, incident_type, severity, description)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), incident_type, severity, description))
        
        incident_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"📋 Created incident #{incident_id}: {incident_type}")
        return incident_id
    
    def collect_network_evidence(self, incident_id):
        """Collect network-related evidence"""
        evidence_files = []
        
        try:
            # Collect netstat information
            if platform.system() == 'Windows':
                netstat_cmd = ['netstat', '-an']
            else:
                netstat_cmd = ['netstat', '-tuln']
            
            result = subprocess.run(netstat_cmd, capture_output=True, text=True)
            
            # Save netstat output
            netstat_file = f'evidence_netstat_{incident_id}_{int(datetime.now().timestamp())}.txt'
            with open(netstat_file, 'w') as f:
                f.write(f"Network connections at {datetime.now()}\n")
                f.write("="*50 + "\n")
                f.write(result.stdout)
            
            evidence_files.append(('network_connections', netstat_file))
            
            # Collect ARP table
            if platform.system() == 'Windows':
                arp_cmd = ['arp', '-a']
            else:
                arp_cmd = ['arp', '-a']
            
            result = subprocess.run(arp_cmd, capture_output=True, text=True)
            
            arp_file = f'evidence_arp_{incident_id}_{int(datetime.now().timestamp())}.txt'
            with open(arp_file, 'w') as f:
                f.write(f"ARP table at {datetime.now()}\n")
                f.write("="*50 + "\n")
                f.write(result.stdout)
            
            evidence_files.append(('arp_table', arp_file))
            
        except Exception as e:
            print(f"Error collecting network evidence: {e}")
        
        # Record evidence in database
        self.record_evidence(incident_id, evidence_files)
        return evidence_files
    
    def collect_process_evidence(self, incident_id):
        """Collect process-related evidence"""
        evidence_files = []
        
        try:
            # Get running processes
            if platform.system() == 'Windows':
                ps_cmd = ['tasklist', '/v']
            else:
                ps_cmd = ['ps', 'aux']
            
            result = subprocess.run(ps_cmd, capture_output=True, text=True)
            
            ps_file = f'evidence_processes_{incident_id}_{int(datetime.now().timestamp())}.txt'
            with open(ps_file, 'w') as f:
                f.write(f"Running processes at {datetime.now()}\n")
                f.write("="*50 + "\n")
                f.write(result.stdout)
            
            evidence_files.append(('running_processes', ps_file))
            
        except Exception as e:
            print(f"Error collecting process evidence: {e}")
        
        self.record_evidence(incident_id, evidence_files)
        return evidence_files
    
    def collect_system_logs(self, incident_id, hours_back=24):
        """Collect relevant system logs"""
        evidence_files = []
        
        try:
            if platform.system() == 'Linux':
                # Collect recent auth logs
                auth_log_file = f'evidence_auth_logs_{incident_id}_{int(datetime.now().timestamp())}.txt'
                
                # Get logs from last N hours
                since_time = datetime.now() - timedelta(hours=hours_back)
                
                with open('/var/log/auth.log', 'r') as source:
                    with open(auth_log_file, 'w') as dest:
                        dest.write(f"Authentication logs from last {hours_back} hours\n")
                        dest.write("="*50 + "\n")
                        
                        for line in source:
                            dest.write(line)
                
                evidence_files.append(('auth_logs', auth_log_file))
                
            elif platform.system() == 'Windows':
                # Collect Windows event logs (simplified)
                event_log_file = f'evidence_event_logs_{incident_id}_{int(datetime.now().timestamp())}.txt'
                
                with open(event_log_file, 'w') as f:
                    f.write(f"Event log collection attempted at {datetime.now()}\n")
                    f.write("Note: Full Windows event log collection requires elevated privileges\n")
                
                evidence_files.append(('event_logs', event_log_file))
                
        except Exception as e:
            print(f"Error collecting system logs: {e}")
        
        self.record_evidence(incident_id, evidence_files)
        return evidence_files
    
    def record_evidence(self, incident_id, evidence_files):
        """Record evidence files in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for evidence_type, file_path in evidence_files:
            # Calculate file hash
            try:
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
            except:
                file_hash = 'unknown'
            
            cursor.execute('''
                INSERT INTO evidence (incident_id, evidence_type, file_path, hash_value, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (incident_id, evidence_type, file_path, file_hash, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        print(f"📁 Recorded {len(evidence_files)} evidence files for incident #{incident_id}")
    
    def generate_incident_report(self, incident_id):
        """Generate comprehensive incident report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get incident details
        cursor.execute('SELECT * FROM incidents WHERE id = ?', (incident_id,))
        incident = cursor.fetchone()
        
        if not incident:
            print(f"Incident #{incident_id} not found")
            return None
        
        # Get evidence files
        cursor.execute('SELECT * FROM evidence WHERE incident_id = ?', (incident_id,))
        evidence = cursor.fetchall()
        
        conn.close()
        
        # Generate report
        report_file = f'incident_report_{incident_id}_{int(datetime.now().timestamp())}.txt'
        
        with open(report_file, 'w') as f:
            f.write("INCIDENT RESPONSE REPORT\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Incident ID: {incident[0]}\n")
            f.write(f"Timestamp: {incident[1]}\n")
            f.write(f"Type: {incident[2]}\n")
            f.write(f"Severity: {incident[3]}\n")
            f.write(f"Description: {incident[4]}\n")
            f.write(f"Status: {incident[6]}\n\n")
            
            f.write("SYSTEM INFORMATION\n")
            f.write("-"*30 + "\n")
            for key, value in self.system_info.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            f.write("EVIDENCE COLLECTED\n")
            f.write("-"*30 + "\n")
            if evidence:
                for ev in evidence:
                    f.write(f"Type: {ev[2]}\n")
                    f.write(f"File: {ev[3]}\n")
                    f.write(f"Hash: {ev[4]}\n")
                    f.write(f"Collected: {ev[5]}\n\n")
            else:
                f.write("No evidence collected\n")
            
            f.write("RECOMMENDATIONS\n")
            f.write("-"*30 + "\n")
            f.write("1. Review all collected evidence files\n")
            f.write("2. Implement containment measures if threat is active\n")
            f.write("3. Update security policies based on findings\n")
            f.write("4. Consider additional monitoring for similar incidents\n")
        
        print(f"📊 Generated incident report: {report_file}")
        return report_file
    
if __name__ == "__main__":
    tool = IncidentResponseTool()

    incident_id = tool.create_incident(
        incident_type="Suspicious Activity",
        severity = "High",
        description="Investigation started due to alerts."
    )
    # 2) Collect evidence
    tool.collect_network_evidence(incident_id)
    tool.collect_process_evidence(incident_id)
    tool.collect_system_logs(incident_id, hours_back=24)

    # 3) Generate report
    tool.generate_incident_report(incident_id)