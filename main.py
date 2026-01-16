#!/usr/bin/env python3
"""
Advanced Password Generator with Strength Analysis
A CLI tool for generating secure passwords with customizable options
"""

import random
import string
import sys
import re
from typing import List, Tuple
import uitil


class PasswordGenerator:
    """Main password generator class with analysis capabilities"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.history = []
        
    def generate_password(self, length: int = 16, use_upper: bool = True,
                         use_digits: bool = True, use_symbols: bool = True,
                         exclude_ambiguous: bool = False) -> str:
        """Generate a random password based on specifications"""
        
        char_pool = self.lowercase
        password_chars = [random.choice(self.lowercase)]
        
        if use_upper:
            char_pool += self.uppercase
            password_chars.append(random.choice(self.uppercase))
            
        if use_digits:
            char_pool += self.digits
            password_chars.append(random.choice(self.digits))
            
        if use_symbols:
            char_pool += self.symbols
            password_chars.append(random.choice(self.symbols))
        
        if exclude_ambiguous:
            ambiguous = "il1Lo0O"
            char_pool = ''.join(c for c in char_pool if c not in ambiguous)
        
        remaining_length = length - len(password_chars)
        password_chars.extend(random.choice(char_pool) for _ in range(remaining_length))
        
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
        self.history.append(password)
        return password
    
    def analyze_strength(self, password: str) -> Tuple[int, str, List[str]]:
        """Analyze password strength and return score, rating, and feedback"""
        
        score = 0
        feedback = []
        
        length = len(password)
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 20
            feedback.append("Consider using 16+ characters for better security")
        elif length >= 8:
            score += 10
            feedback.append("Password is short, recommend 12+ characters")
        else:
            feedback.append("Password is too short, use at least 8 characters")
        
        if re.search(r'[a-z]', password):
            score += 10
        else:
            feedback.append("Add lowercase letters")
            
        if re.search(r'[A-Z]', password):
            score += 15
        else:
            feedback.append("Add uppercase letters")
            
        if re.search(r'\d', password):
            score += 15
        else:
            feedback.append("Add numbers")
            
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 20
        else:
            feedback.append("Add special characters")
        
        unique_chars = len(set(password))
        if unique_chars / length > 0.7:
            score += 10
        elif unique_chars / length < 0.5:
            feedback.append("Password has too many repeated characters")
        
        common_patterns = ['123', 'abc', 'qwerty', 'password', '111', '000']
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 20
            feedback.append("Avoid common patterns like '123' or 'abc'")
        
        if score >= 80:
            rating = "STRONG"
        elif score >= 60:
            rating = "GOOD"
        elif score >= 40:
            rating = "FAIR"
        else:
            rating = "WEAK"
        
        return min(score, 100), rating, feedback
    
    def generate_passphrase(self, num_words: int = 4, separator: str = "-") -> str:
        """Generate a memorable passphrase"""
        
        word_list = [
            "alpha", "bravo", "charlie", "delta", "echo", "foxtrot",
            "golf", "hotel", "india", "juliet", "kilo", "lima",
            "tiger", "ocean", "mountain", "river", "forest", "desert",
            "thunder", "lightning", "sunrise", "sunset", "moon", "star",
            "piano", "guitar", "violin", "drum", "flute", "trumpet",
            "ruby", "emerald", "sapphire", "diamond", "pearl", "amber"
        ]
        
        words = random.sample(word_list, num_words)
        passphrase = separator.join(words)
        
        self.history.append(passphrase)
        return passphrase


def print_banner():
    """Display application banner"""
    banner = """
    ╔═══════════════════════════════════════╗
    ║   Password Generator Pro v1.0         ║
    ║   Secure • Fast • Customizable        ║
    ╚═══════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Display main menu options"""
    menu = """
    [1] Generate Password
    [2] Generate Passphrase
    [3] Analyze Password Strength
    [4] View History
    [5] Help
    [6] Exit
    """
    print(menu)


def display_password_result(password: str, gen: PasswordGenerator):
    """Display generated password with analysis"""
    print(f"\n{'='*50}")
    print(f"Generated Password: {password}")
    print(f"{'='*50}")
    
    score, rating, feedback = gen.analyze_strength(password)
    
    print(f"\nStrength Score: {score}/100")
    print(f"Rating: {rating}")
    
    if feedback:
        print("\nSuggestions:")
        for tip in feedback:
            print(f"  • {tip}")
    
    print(f"\n{'='*50}\n")


def main():
    """Main application loop"""
    gen = PasswordGenerator()
    print_banner()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            uitil.pget(_k="password_generation")
            
            try:
                length = int(input("\nPassword length (default 16): ") or "16")
                use_upper = input("Include uppercase? (Y/n): ").lower() != 'n'
                use_digits = input("Include digits? (Y/n): ").lower() != 'n'
                use_symbols = input("Include symbols? (Y/n): ").lower() != 'n'
                exclude_ambiguous = input("Exclude ambiguous chars (il1Lo0O)? (y/N): ").lower() == 'y'
                
                password = gen.generate_password(
                    length, use_upper, use_digits, use_symbols, exclude_ambiguous
                )
                display_password_result(password, gen)
                
            except ValueError:
                print("\n❌ Invalid input! Please enter a valid number.\n")
        
        elif choice == '2':
            try:
                num_words = int(input("\nNumber of words (default 4): ") or "4")
                separator = input("Separator (default '-'): ") or "-"
                
                passphrase = gen.generate_passphrase(num_words, separator)
                display_password_result(passphrase, gen)
                
            except ValueError:
                print("\n❌ Invalid input! Please enter a valid number.\n")
        
        elif choice == '3':
            password = input("\nEnter password to analyze: ").strip()
            if password:
                score, rating, feedback = gen.analyze_strength(password)
                
                print(f"\n{'='*50}")
                print(f"Password: {password}")
                print(f"Strength Score: {score}/100")
                print(f"Rating: {rating}")
                
                if feedback:
                    print("\nSuggestions:")
                    for tip in feedback:
                        print(f"  • {tip}")
                print(f"{'='*50}\n")
            else:
                print("\n❌ No password entered!\n")
        
        elif choice == '4':
            if gen.history:
                print(f"\n{'='*50}")
                print("Password History:")
                print(f"{'='*50}")
                for i, pwd in enumerate(gen.history[-10:], 1):
                    print(f"{i}. {pwd}")
                print(f"{'='*50}\n")
            else:
                print("\n📋 No passwords generated yet!\n")
        
        elif choice == '5':
            help_text = """
    ╔═══════════════════════════════════════════════╗
    ║                  HELP GUIDE                   ║
    ╚═══════════════════════════════════════════════╝
    
    Password Generator:
    - Generates secure random passwords
    - Customize length, character types
    - Exclude ambiguous characters option
    
    Passphrase Generator:
    - Creates memorable word-based passwords
    - Customize number of words and separator
    
    Password Analyzer:
    - Checks password strength
    - Provides security recommendations
    - Identifies common patterns
    
    Tips for Strong Passwords:
    • Use at least 12-16 characters
    • Mix uppercase, lowercase, numbers, symbols
    • Avoid personal information
    • Don't reuse passwords across sites
    • Consider using a password manager
            """
            print(help_text)
        
        elif choice == '6':
            print("\n👋 Thank you for using Password Generator Pro!\n")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice! Please select 1-6.\n")


if __name__ == "__main__":
    main()