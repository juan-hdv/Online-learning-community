'''
a ForeignKey (b) <=> b "ManyToOne relationship" with a
Example: 
	<order> ForeignKey (<user>) <=> <user> "ManyToOne relatinship" with <order>
								One <order> is related with One <user>
								One <user> could place Many <orders>
'''
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	pass
