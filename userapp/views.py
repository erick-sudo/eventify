from django.shortcuts import render, redirect
from .serializers import UserRegistrationSerializer, LoginSerializer, ForgotPasswordSerializer, PasswordResetSerializer
from .models import User
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return render(request, 'register.html', {'status': {}, 'form_data': {}, 'success': True}) 
        else:
            errors = serializer.errors
            return render(request, 'register.html', {'errors': errors, 'form_data': serializer.data })

    return render(request, 'register.html')
    

def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            return redirect("/")
        else:
            errors = serializer.errors
            return render(request, 'login.html', {'errors': errors, 'form_data': serializer.data })

    return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('/')

def reset_password(request, uidb64, token):
    form_state = None
    if request.method == "POST":
        serializer = PasswordResetSerializer(data=request.POST, context={'request': request, 'uidb64': uidb64, 'token': token})
        if serializer.is_valid():
            form_state = {
                'posting': True,
                'success': True,
                'message': 'Password reset successfully',
                'errors': {},
                'form_data': {}
            }
        else:
            
            errors = serializer.errors
            form_state = {
                'posting': True,
                'success': False,
                'errors': errors,
                'form_data': serializer.data
            }
    else:
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            User.objects.get(id=user_id)
                
            try:
                AccessToken(token)
                form_state = {
                    'success': True,
                    'message': None,
                }
                    
            except TokenError as e:
                form_state = {
                    'success': False,
                    'message': f'{e}.'
                }
        except User.DoesNotExist:
            form_state = {
                'success': False,
                'message': f'invalid activation token'
            }
        except Exception as e:
            form_state = {
                'success': False,
                'message': f'link is invalid or has expired.'
            }
            
    return render(request, 'reset_password.html', {'form_state': form_state, 'uidb64': uidb64, 'token': token})

def forgot_password(request):
    if request.method == 'POST':
        serializer = ForgotPasswordSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            return render(request, 'forgot_password.html', {'errors': {}, 'form_data': {}, 'success': True })
        else:
            errors = serializer.errors
            return render(request, 'forgot_password.html', {'errors': errors, 'form_data': serializer.data })

    return render(request, 'forgot_password.html')

def activate_account(request, uidb64, token):
    message = None
    try:
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
        
        if request.method == "POST":
            try:
                AccessToken(token)
                user.is_verified = True
                user.save()
                message = {
                    'success': True,
                    'message': 'Your account has been activated.'
                }
            except TokenError as e:
                message = {
                    'success': False,
                    'message': f'{e}'
                }
        else:
            try:
                AccessToken(token)
                message = {
                    'success': True,
                    'message': None,
                    'get': True,
                }
            except TokenError as e:
                message = {
                    'success': False,
                    'message': f'{e}'
                }
    except User.DoesNotExist:
        message = {
            'success': False,
            'message': 'Sorry! User does not exist.'
        }
    except Exception as e:
            message = {
                'success': False,
                'message': f'link is invalid or has expired.'
            }
        
    return render(request, 'activate_account.html', {'message': message, 'uidb64': uidb64, 'token': token})
