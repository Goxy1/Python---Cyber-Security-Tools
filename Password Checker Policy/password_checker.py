import re
import hashlib
import requests
import secrets
import string
from collections import Counter

class PasswordChecker:
    def __init__(self):
        self.common_passwords = [
            "123456","123456789","12345","12345678","password","qwerty","1234567","1234567890",
            "123123","abc123","qwerty123","111111","password1","admin","admin123","letmein",
            "welcome","iloveyou","monkey","dragon","football","sunshine","login","princess",
            "master","hello","freedom","whatever","trustno1","passw0rd","starwars","zaq1zaq1",
            "000000","654321","superman","batman","shadow","killer","flower","hottie","loveme",
            "secret","asdfgh","asdfghjkl","qazwsx","qwe123","internet","service","manager","root",
            "root123","system","user","user123","test","test123","guest","guest123","changeme",
            "temp123","access","admin1","adminadmin","welcome1","login123","password123","pass1234",
            "pass123","mypassword","mysecret","computer","desktop","laptop","mobile","android",
            "iphone","samsung","google","facebook","twitter","linkedin","instagram","youtube",
            "amazon","netflix","spotify","office","office123","company","company123","employee",
            "employee123","welcome123","admin2020","admin2021","admin2022","admin2023","admin2024",
            "qwertyuiop","asdf1234"
        ]
        # Password Policy Requirements
        self.min_length = 12
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_numbers = True
        self.require_special = True
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def check_length(self, password):
        return len(password) >= self.min_length
    
    def check_uppercase(self, password):
        return bool(re.search(r'[A-Z]', password))
    
    def check_lowercase(self, password):
        return bool(re.search(r'[a-z]', password))
    
    def check_numbers(self, password):
        return bool(re.search(r'\d', password))
    
    def check_special_chars(self, password):
        return any(char in self.special_chars for char in password)
    def check_common_passwords(self, password):
        return password.lower() not in [p.lower() for p in self.common_passwords]
    
    def check_sequential_chars(self, password):
        """Check for sequential characters (abc, 123, etc.)"""
        sequential_patterns = ['abc', 'bcd', 'cde', 'def', '123', '234', '345', '456', '789']
        password_lower = password.lower()
        
        for pattern in sequential_patterns:
            if pattern in password_lower:
                return False
        return True
    
    def check_repeated_chars(self, password):
        """Check for excessive repeated characters"""
        char_counts = Counter(password.lower())
        max_repeat = max(char_counts.values()) if char_counts else 0
        return max_repeat <= 3  # Allow max 3 repetitions
    
    def calculate_entropy(self, password):
        charset_size = 0

        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if any(char in self.special_chars for char in password):
            charset_size += len(self.special_chars)
        
        if charset_size == 0:
            return 0
        
        import math
        entropy = len(password) * math.log2(charset_size)
        return entropy
    
    def estimate_crack_time(self, password):
        entropy = self.calculate_entropy(password)

        guesses_per_second = 1_000_000_000
        combinations = 2 ** entropy
        seconds_to_crack = combinations / (2 * guesses_per_second) #Average case

        if seconds_to_crack < 60:
            return f"{seconds_to_cssack:.2f} seconds"
        elif seconds_to_crack < 3600:
            return f"{seconds_to_crack/60:.2f} minutes"
        elif seconds_to_crack < 86400:
            return f"{seconds_to_crack/3600:.2f} hours"
        elif seconds_to_crack < 31536000:
            return f"{seconds_to_crack/86400:.2f} days"
        else:
            return f"{seconds_to_crack/31536000:.2f} years"
        

    def check_haveibeenpwned(self, password):
        
        try:
            #hashing the password
            sha1_hash = hashlib.sha1(password.encode().hexdigest().upper())
            prefix = sha1_hash[:5]
            suffix = sha1_hash[:5]

            #Query HaveIbeenPawned API
            url = f"API"
            response = requests.get(url, timeout = 5)

            if response.status_code == 200:
                hashes = response.text.splitlines()
                for hash_line in hashes:
                    hash_suffix, count = hash_line.split(':')
                    if hash_suffix == suffix:
                        return int(count)
            return 0
        except Exception as e:
            print(f"Could not check data breach: {e}")
            return -1
    
    def assess_password(self, password):
        #Comprehensive password assessment
        results = {
            'password': password,
            'score' : 0,
            'max_score' : 100,
            'checks' : {},
            'recommendations' : [],
            'strength' : 'Very weak'
        }

        # Running all checks
        checks = {
            'length': (self.check_length(password), 15, f"At least {self.min_length} characters"),
            'uppercase': (self.check_uppercase(password), 10, "Contains uppercase letters"),
            'lowercase': (self.check_lowercase(password), 10, "Contains lowercase letters"),
            'numbers': (self.check_numbers(password), 10, "Contains numbers"),
            'special_chars': (self.check_special_chars(password), 15, "Contains special characters"),
            'not_common': (self.check_common_passwords(password), 20, "Not a common password"),
            'no_sequential': (self.check_sequential_chars(password), 10, "No sequential characters"),
            'no_repeated': (self.check_repeated_chars(password), 10, "Limited repeated characters")
        }
        # Calculate score and collect results
        for check_name, (passed, points, description) in checks.items():
            results['checks'][check_name] = {
                'passed': passed,
                'points': points if passed else 0,
                'description': description
            }
            if passed:
                results['score'] += points
            else:
                results['recommendations'].append(description)
        
        # Check breach database
        breach_count = self.check_haveibeenpwned(password)
        if breach_count > 0:
            results['checks']['breach_check'] = {
                'passed': False,
                'points': 0,
                'description': f"Found in {breach_count} data breaches"
            }
            results['recommendations'].append("This password has been compromised in data breaches")
        elif breach_count == 0:
            results['checks']['breach_check'] = {
                'passed': True,
                'points': 0,
                'description': "Not found in known breaches"
            }
        # Calculate entropy and crack time
        entropy = self.calculate_entropy(password)
        crack_time = self.estimate_crack_time(password)
        
        results['entropy'] = entropy
        results['estimated_crack_time'] = crack_time
        
        # Determine strength level
        if results['score'] >= 90:
            results['strength'] = 'Very Strong'
        elif results['score'] >= 70:
            results['strength'] = 'Strong'
        elif results['score'] >= 50:
            results['strength'] = 'Moderate'
        elif results['score'] >= 30:
            results['strength'] = 'Weak'
        else:
            results['strength'] = 'Very Weak'
        
        return results
    
    def generate_secure_password(self, length=16, include_symbols=True):
        """Generate a cryptographically secure password"""
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += self.special_chars
        
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password
    
    def generate_passphrase(self, num_words=4):
        """Generate a secure passphrase using common words"""
        # Simple word list for demonstration
        words = [
            'apple', 'beach', 'chair', 'dance', 'eagle', 'flame', 'grape', 'house',
            'island', 'jungle', 'knife', 'lemon', 'mouse', 'night', 'ocean', 'piano',
            'quiet', 'river', 'snake', 'tiger', 'uncle', 'voice', 'whale', 'zebra'
        ]
        
        selected_words = [secrets.choice(words) for _ in range(num_words)]
        # Add random number and capitalize random words
        passphrase = []
        for word in selected_words:
            if secrets.choice([True, False]):
                word = word.capitalize()
            passphrase.append(word)
        
        # Add a random number
        passphrase.append(str(secrets.randbelow(9999)).zfill(4))
        
        return '-'.join(passphrase)

def main():
    """Main password checker interface"""
    checker = PasswordChecker()
    
    print("🔐 Password Security Checker")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Check password strength")
        print("2. Generate secure password")
        print("3. Generate secure passphrase")
        print("4. Batch check passwords from file")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            password = input("Enter password to check: ")
            if not password:
                print("Please enter a password.")
                continue
                
            print("\nAnalyzing password...")
            results = checker.assess_password(password)
            
            print(f"\n📊 Password Analysis Results")
            print(f"Strength: {results['strength']}")
            print(f"Score: {results['score']}/{results['max_score']}")
            print(f"Entropy: {results['entropy']:.1f} bits")
            print(f"Estimated crack time: {results['estimated_crack_time']}")
            
            print(f"\n✅ Passed Checks:")
            for check_name, check_result in results['checks'].items():
                if check_result['passed']:
                    print(f"  - {check_result['description']}")
            
            if results['recommendations']:
                print(f"\n❌ Recommendations:")
                for rec in results['recommendations']:
                    print(f"  - {rec}")
        
        elif choice == '2':
            length = input("Password length (default 16): ").strip()
            length = int(length) if length.isdigit() else 16
            
            include_symbols = input("Include symbols? (y/n, default y): ").strip().lower()
            include_symbols = include_symbols != 'n'
            
            password = checker.generate_secure_password(length, include_symbols)
            print(f"\nGenerated password: {password}")
            
            # Auto-analyze the generated password
            results = checker.assess_password(password)
            print(f"Strength: {results['strength']} (Score: {results['score']}/{results['max_score']})")
        
        elif choice == '3':
            num_words = input("Number of words (default 4): ").strip()
            num_words = int(num_words) if num_words.isdigit() else 4
            
            passphrase = checker.generate_passphrase(num_words)
            print(f"\nGenerated passphrase: {passphrase}")
            
            # Auto-analyze the generated passphrase
            results = checker.assess_password(passphrase)
            print(f"Strength: {results['strength']} (Score: {results['score']}/{results['max_score']})")
        
        elif choice == '4':
            filename = input("Enter filename containing passwords (one per line): ").strip()
            try:
                with open(filename, 'r') as f:
                    passwords = [line.strip() for line in f if line.strip()]
                
                print(f"\nAnalyzing {len(passwords)} passwords...")
                weak_passwords = []
                
                for i, password in enumerate(passwords, 1):
                    results = checker.assess_password(password)
                    print(f"{i:3d}. Score: {results['score']:3d}/100 | {results['strength']:12s} | {password}")
                    
                    if results['score'] < 50:
                        weak_passwords.append(password)
                
                print(f"\nSummary: {len(weak_passwords)} out of {len(passwords)} passwords are weak")
                
            except FileNotFoundError:
                print(f"File '{filename}' not found.")
            except Exception as e:
                print(f"Error reading file: {e}")
        
        elif choice == '5':
            print("Thank you for using Password Security Checker!")
            break
        
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
 