from django.db import models

# Model to store Participant's data
class Participant(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(primary_key=True)
    verified = models.BooleanField()

    def __str__(self):
        return self.email

# Model to store Interview details
class Interview(models.Model):
    agenda = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    edited_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


# Model to store relationship between Participants and Interviews
class InterviewParticipants(models.Model):
    interview=models.ForeignKey(Interview,on_delete=models.CASCADE)
    participant=models.ForeignKey(Participant,on_delete=models.CASCADE)
    class Meta:
        unique_together=(('interview','participant'),)
