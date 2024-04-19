from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.contrib.auth import authenticate, login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.utils.encoding import smart_str, force_bytes
from .utils import send_email_via_template, generate_scheme_and_domain

class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Check if passwords match and email is unique.
        """
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("Email is already taken.")
        
        return data

    def create(self, validated_data):
        """
        Create and return a new user instance.
        """
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        request=self.context.get('request')
        token = AccessToken.for_user(user)
        token_string = str(token)
        
        # Encoding the user's ID for use in the URL
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Activation URL with the token in the query string
        scheme, domain = generate_scheme_and_domain(request)
            
        absolute_link = f"{scheme}://{domain}{reverse('activate_account', kwargs={ 'uidb64': uidb64, 'token': token_string })}"
        
        try:
            send_email_via_template("Account Activation", [user.email], "account_activation_mailer.html", { 'link': absolute_link, 'first_name': user.first_name })
        except Exception as e:
            User.objects.delete(user=user)
            raise serializers.ValidationError(f"An internal server error occurred. We could not save your details. Please try again later.")
        
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=6, write_only=True)
    password=serializers.CharField(max_length=68, write_only=True)
    
    class Meta:
        model=User
        fields=['email', 'password']
        
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        
        request=self.context.get('request')
        user=authenticate(request, email=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid username or password', code=401)
        
        if not user.is_verified:
            raise serializers.ValidationError("account not verified, please verify your account", code=403)
        
        login(request, user)
        
        return attrs
        
class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255, min_length=6)
    
    class Meta:
        fields=['email']
        
    def validate(self, attrs):
        email=attrs.get('email')
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            
            if not user.is_verified:
                raise serializers.ValidationError("account not verified, please verify your account", code=403)
            
            request = self.context.get('request')
            
            token = AccessToken.for_user(user)
            token_string = str(token)
            
            # Encoding the user's ID for use in the URL
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Activation URL with the token in the query string
            scheme, domain = generate_scheme_and_domain(request)
                
            absolute_link = f"{scheme}://{domain}{reverse('reset_password', kwargs={ 'uidb64': uidb64, 'token': token_string })}"
            
            try:
                send_email_via_template("Password Reset", [user.email], 'forgot_password_mailer.html', { 'link': absolute_link,'first_name': user.first_name })
            except Exception as e:
                raise serializers.ValidationError(f"an internal server error occurred. Please try again later.")
            return attrs
        else:
            raise serializers.ValidationError(f"User by email {email} does not exist", code=404)
        
    
class PasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        fields=['password', 'confirm_password', 'uidb64', 'token']
        
    def validate(self, attrs):
        token = self.context.get('token')
        uidb64 = self.context.get('uidb64')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password!= confirm_password:
            raise serializers.ValidationError("passwords do not match", code=422)
        
        user = None
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
        except Exception as e:
            raise serializers.ValidationError("link is invalid or has expired", 401)
        
        try:
            AccessToken(token)
        except TokenError as e:
            raise serializers.ValidationError(f"{e}", 401)
        
        
        user.set_password(password)
        user.save()
        return user