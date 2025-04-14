import random
import string
import requests
from datetime import datetime, timedelta

# Mailjet API credentials
API_KEY = 'db722316dc59f2215f167af4871d61c5'
API_SECRET = '68b0add277af5ded50d107895d3c59b3'

class OTPManager:
    def __init__(self):
        self.otps = {}  # Store OTPs with timestamps: {email: (otp, timestamp)}
    
    def generate_otp(self, length=6):
        """Generate a random OTP"""
        return ''.join(random.choices(string.digits, k=length))
    
    def save_otp(self, email, otp):
        """Save OTP with current timestamp"""
        self.otps[email] = (otp, datetime.now())
    
    def verify_otp(self, email, otp, expiry_minutes=5):
        """Verify if provided OTP matches and hasn't expired"""
        if email not in self.otps:
            return False
        
        stored_otp, timestamp = self.otps[email]
        if datetime.now() - timestamp > timedelta(minutes=expiry_minutes):
            del self.otps[email]  # Remove expired OTP
            return False
        
        if otp == stored_otp:
            del self.otps[email]  # Remove used OTP
            return True
            
        return False
    
    def send_otp_email(self, email, otp, purpose="verification"):
        """Send OTP via Mailjet"""
        url = 'https://api.mailjet.com/v3.1/send'
        
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "acadassistant8@gmail.com",
                        "Name": "AcadAssist"
                    },
                    "To": [
                        {
                            "Email": email,
                            "Name": "User"
                        }
                    ],
                    "Subject": f"Your AcadAssist OTP for {purpose}",
                    "TextPart": f"Your OTP for {purpose} is: {otp}\nThis OTP will expire in 5 minutes.",
                    "HTMLPart": f"""
                        <h3>AcadAssist OTP Verification</h3>
                        <p>Your OTP for {purpose} is: <strong>{otp}</strong></p>
                        <p>This OTP will expire in 5 minutes.</p>
                        <p>If you didn't request this, please ignore this email.</p>
                    """
                }
            ]
        }
        
        try:
            response = requests.post(
                url,
                auth=(API_KEY, API_SECRET),
                json=data
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send OTP: {str(e)}")
            return False

# Global OTP manager instance
otp_manager = OTPManager()