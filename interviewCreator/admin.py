from django.contrib import admin
from .models import Participant, Interview, InterviewParticipants

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'verified',)
    list_filter = ('verified',)
    search_fields = ('name', 'email',)

class InterviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'agenda', 'start_time', 'end_time', 'edited_on',)
    search_fields = ('id', 'agenda',)

class InterviewParticipantsAdmin(admin.ModelAdmin):
    list_display = ('interview', 'participant',)
    search_fields = ('interview__id', 'participant__email',)

admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(InterviewParticipants, InterviewParticipantsAdmin)
