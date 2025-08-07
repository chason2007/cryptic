import string
import secrets
import qrcode
import io
import base64
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import PasswordHistory  # Import our model

def home(request):
    """Render the main page with the password generator form"""
    # Optional: Get the 5 most recent passwords for display
    recent_passwords = PasswordHistory.objects.all().order_by('-created_at')[:5]
    return render(request, 'generator/home.html', {'recent_passwords': recent_passwords})

@csrf_exempt
def generate_password(request):
    """Generate a password based on parameters from POST request"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            length = int(data.get('length', 12))
            use_upper = data.get('upper', True)
            use_lower = data.get('lower', True)
            use_digits = data.get('digits', True)
            use_special = data.get('special', False)
            
            characters = ''
            if use_upper:
                characters += string.ascii_uppercase
            if use_lower:
                characters += string.ascii_lowercase
            if use_digits:
                characters += string.digits
            if use_special:
                characters += string.punctuation
                
            if not characters:
                return JsonResponse({'error': 'Select at least one character type!'}, status=400)
                
            password = ''.join(secrets.choice(characters) for _ in range(length))
            
            # Save to MongoDB (optional - include save_history flag in request)
            if data.get('save_history', False):
                PasswordHistory.objects.create(
                    password=password,
                    length=length,
                    has_uppercase=use_upper,
                    has_lowercase=use_lower,
                    has_digits=use_digits,
                    has_special=use_special
                )
            
            return JsonResponse({'password': password})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def generate_qr_code(request):
    """Generate a QR code for the password"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            password = data.get('password', '')
            
            if not password:
                return JsonResponse({'error': 'No password provided!'}, status=400)
                
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(password)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR code to memory buffer
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Convert to base64 for embedding in HTML
            img_str = base64.b64encode(buffer.getvalue()).decode('ascii')
            
            return JsonResponse({'qr_code': img_str})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Add a new view to display password history
def password_history(request):
    """View to display password history"""
    passwords = PasswordHistory.objects.all().order_by('-created_at')
    return render(request, 'generator/history.html', {'passwords': passwords})