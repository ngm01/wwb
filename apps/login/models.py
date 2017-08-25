from __future__ import unicode_literals

from django.db import models

import bcrypt


class userManager(models.Manager):
	def regValidator(self, postData):
		errors = {}
		if User.objects.filter(user_name = postData['user_name']):
		 	errors['user_name_exists'] = "Sorry, that user name has been taken."
		if len(postData['user_name']) < 3:
			errors['user_name'] = "User name must be at least 3 characters long."
		if len(postData['password']) < 8:
			errors['pword_length'] = "Password must be at least 8 characters long."
		if postData['password'] != postData['pwconf']:
			errors['pwconf'] = "Password confirmation must match password."
		print errors
		return errors
		
	def loginValidator(self, postData):
		user = User.objects.filter(user_name = postData['user_name'])
		errors = {}
		if not user:
			errors['user_name'] = "Please enter a valid username."
		if user and not bcrypt.checkpw(postData['password'].encode('utf8'), user[0].password.encode('utf8')):
			errors['password'] = "Invalid password."
		return errors

# Create your models here.
class User(models.Model):
	user_name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = userManager()
