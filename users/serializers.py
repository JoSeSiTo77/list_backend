from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password as django_validated_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# JWT Settings
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        data = super().validate(attrs)

        user_data = {
            'first_name': self.user.first_name
        }

        data['user'] = user_data

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        
    # Custom fields validations
    def validate_first_name(self, value):
        # Value copy and elimination of spaces
        value_copy = value
        value_copy = value_copy.replace(" ", "")

        # Characters validation
        if not value_copy.isalpha():
            raise serializers.ValidationError('The name most contain only letters')

        # Processing of two names
        name_list = value.split()
        name = []
        if len(name_list) >= 2:
            name = [name_list[0].capitalize(), name_list[1].capitalize()]

            # Two names processed
            value = ' '.join(name)
        else: 
            value = name_list[0]
        return value

    def validate_password(self, value):
        if self.instance is not None:
            user = self.instance
        else:
            email = self.initial_data.get('email')
            name = self.initial_data.get('first_name')
            user = User(email=email, first_name=name)     
        try:
            django_validated_password(value, user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))

        return value

    # Custom methods to save on db
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
        