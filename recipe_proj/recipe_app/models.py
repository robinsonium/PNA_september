from django.db import models
from datetime import datetime
import re

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postdata):
        errors = {}

        # NAMES MUST BE LONGER THAN 2 CHARACTERS
        if len(postdata['first_name']) < 3:
            errors['first_name_length'] = "First name must be longer than 2 characters"
        if len(postdata['last_name']) < 3:
            errors['last_name_length'] = "First name must be longer than 2 characters"

        # EMAIL IS A VALID REGEX
        email_pattern = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_pattern.match(postdata['email']):
            errors['email_pattern'] = "Invalid email address"

        # EMAIL MUST BE UNIQUE
        all_users = User.objects.all()
        emails = [x.email for x in all_users]
        if postdata['email'] in emails:
            errors['unique_email'] = "This email is already registered"

        passwd=postdata['password']
        passwd_conf=postdata['confirm']
        # PASSWORD MUST MATCH CONFIRMATION
        if passwd != passwd_conf:
            errors['confirmation']="Password did not match confirmation"
        # PASSWORD MUST BE AT LEAST 8 CHARACTERS
        if len(passwd) < 8:
            errors['pwlength']="Password must be at least 8 characters"

        # PASSWORD NEEDS AT LEAST 1 UPPERCASE CHARACTER
        if not any(n.isupper() for  n in passwd): 
            errors['uppercase']="Password must have at least one upper case character"
        
        return errors

class RecipeManager(models.Manager):
    def validate(self, postdata):
        errors = {}

        # NAMES MUST BE LONGER THAN 2 CHARACTERS
        if len(postdata['title']) < 3:
            errors['title_length'] = "title must be longer than 2 characters"
        if len(postdata['last_name']) < 3:
            errors['last_name_length'] = "First name must be longer than 2 characters"

        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username=models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class Recipe(models.Model):
    title=models.CharField(max_length=255)
    creator=models.ForeignKey(User,related_name="recipe",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Review(models.Model):
    content=models.TextField()
    poster=models.ForeignKey(User,related_name="review",on_delete=models.CASCADE, null=True)
    recipe=models.ForeignKey(Recipe,related_name="review",on_delete=models.CASCADE, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Tag(models.Model):
    content=models.TextField()
    recipe=models.ForeignKey(Recipe,related_name="tags",on_delete=models.CASCADE, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content=models.TextField()
    poster=models.ForeignKey(User,related_name="comment",on_delete=models.CASCADE, null=True)
    review=models.ForeignKey(Review,related_name="comment",on_delete=models.CASCADE, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Ingredient(models.Model):
    content=models.TextField()
    recipe=models.ForeignKey(Recipe,related_name="ingredient",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Step(models.Model):
    content=models.TextField()
    recipe=models.ForeignKey(Recipe,related_name="step",on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

