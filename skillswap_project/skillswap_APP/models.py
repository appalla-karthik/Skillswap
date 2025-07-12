from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    skills_offered = models.TextField(blank=True)
    skills_wanted = models.TextField(blank=True)
    availability = models.CharField(max_length=50, default='Weekends')
    visibility = models.CharField(max_length=10, choices=[('Public', 'Public'), ('Private', 'Private')], default='Public')
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default-avatar.png')

    def __str__(self):
        return f"{self.user.username}'s Profile"


class SkillSwapRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    offered_skill = models.CharField(max_length=100)
    requested_skill = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.username} ➝ {self.receiver.username} [{self.offered_skill} ⇄ {self.requested_skill}]"
    

