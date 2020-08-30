from django.shortcuts import render
from django.http import HttpResponse
import datetime, pytz
from .models import Participant, Interview, InterviewParticipants

# Get the list of interviews scheduled for a particular participants
def getInterviews(participant):
    interview_details=[]
    relations=InterviewParticipants.objects.filter(participant=participant)
    for relation in relations:
        interview_details.append(relation.interview)
    return interview_details

# To get a list of participants along with their scheduled interviews
def getParticipantsDetailedData():
    participants=Participant.objects.all()
    detailed_list=[]
    for participant in participants:
        data={}
        data['participant']=participant
        data['interviews']=getInterviews(participant)
        detailed_list.append(data)
    return detailed_list

# Get the list of participants scheduled for a particular interview
def getParticipants(interview):
    participant_details=[]
    relations=InterviewParticipants.objects.filter(interview=interview)
    for relation in relations:
        participant_details.append(relation.participant)
    return participant_details

# To get a list of participants along with their scheduled interviews
def getInterviewsDetailedData():
    interviews=Interview.objects.all().order_by('start_time')
    detailed_list=[]
    for interview in interviews:
        data={}
        data['interview']=interview
        data['participants']=getParticipants(interview)
        detailed_list.append(data)
    return detailed_list

# Function to check if the time for current interview overlaps with any of its Participants
def checkConflict(participant_list,start_time,end_time):
    for participant in participant_list:
        interviews=getInterviews(participant)
        for interview in interviews:
            if ((end_time > interview.start_time and end_time < interview.end_time) or
                (start_time > interview.start_time and start_time < interview.end_time) or
                (interview.start_time > start_time and interview.start_time < end_time) or
                (interview.end_time > start_time and interview.end_time < end_time)):
                return True
    return False

# Function to check if the time for current interview(which is edited version of a previous interview) overlaps with any of its Participants(excluing the current interview)
def checkConflictEdit(participant_list,start_time,end_time,curr_interview):
    for participant in participant_list:
        interviews=getInterviews(participant)
        for interview in interviews:
            if interview.id == curr_interview.id:
                continue
            if ((end_time > interview.start_time and end_time < interview.end_time) or
                (start_time > interview.start_time and start_time < interview.end_time) or
                (interview.start_time > start_time and interview.start_time < end_time) or
                (interview.end_time > start_time and interview.end_time < end_time)):
                return True
    return False

# Get data from POST request
def getFormData(request):
    count=int(request.POST['count'])
    agenda=request.POST['agenda']
    start_time=pytz.timezone('Asia/Kolkata').localize(datetime.datetime.strptime(request.POST['start_time'], '%Y-%m-%dT%H:%M'))
    end_time=pytz.timezone('Asia/Kolkata').localize(datetime.datetime.strptime(request.POST['end_time'], '%Y-%m-%dT%H:%M'))
    participant_list=[]
    for i in range(0,count):
        id="participant"+str(i+1)
        participant_list.append(Participant.objects.get(email=request.POST[id]))

    return count, agenda, start_time, end_time, participant_list

# View for displaying the landing page
def home(request):
    return render(request,'home.html',{})

# View for displaying the create page
def createInterview(request):
    # Handle POST requests
    if request.method=='POST':

        # Get all the post data in required variables
        count, agenda, start_time, end_time, participant_list = getFormData(request)
        # Check if the current timings of the interview overlap with any of the participant's schedule
        flag=checkConflict(participant_list,start_time,end_time)
        # If no conflict, create the interview object and required relationship objects
        if flag==False:
            interview=Interview(agenda=agenda,start_time=start_time,end_time=end_time)
            interview.save()
            for participant in participant_list:
                relation=InterviewParticipants(participant=participant,interview=interview)
                relation.save()
            return render(request,'show_message.html',{'status':'success','message':'Interview was successfully created.'})

        # If there are conflicts then return required message
        else:
            return render(request,'show_message.html',{'status':'failure','message':'Unable to schedule interview. There was a conflict with one or more participants schedule.'})

    # Handle GET requests
    else:
        participants=list(Participant.objects.all().values('name','email'))
        return render(request,'create.html',{'num':0,'participants':participants,'participants_selected':[],'nextURL':'createInterview'})

def editParticipant(request,id):
    # Check whether interview obkect with given id exists or not
    try:
        interview=Interview.objects.get(id=id)
    # If it does not exist return required message
    except:
        return render(request,'show_message.html',{'status':'failure','message':'404 Not Found. Interview with given details does not exist.'})
    # Handling POST requests for the edit page
    if request.method=='POST':
        # Get all the post data in required variables
        count, agenda, start_time, end_time, participant_list_edit = getFormData(request)
        # participant_list_edit contains partcipants selected in the edit page whereas participant_list_original contains participants of the current unedited interview object
        participant_list_original=getParticipants(interview)
        # Check if the current timings of the interview overlap with any of the participant's schedule
        flag=checkConflictEdit(participant_list_edit,start_time,end_time,interview)
        # if no conflict edit the interview object and add/delete required relationship objects
        if flag==False:
            interview.start_time=start_time
            interview.end_time=end_time
            interview.agenda=agenda
            interview.save()
            edit_set=set(participant_list_edit)
            original_set=set(participant_list_original)
            #delete participants which are in original list but not in edit list
            for participant in original_set:
                if participant in edit_set:
                    continue
                relation=InterviewParticipants.objects.get(participant=participant,interview=interview)
                relation.delete()
            #add participants which are in edit list but not in original list
            for participant in edit_set:
                if participant in original_set:
                    continue
                relation=InterviewParticipants(participant=participant,interview=interview)
                relation.save()
            return render(request,'show_message.html',{'status':'success','message':'Interview was successfully edited.'})

        # If there are conflicts then return required message
        else:
            return render(request,'show_message.html',{'status':'failure','message':'Unable to edit interview. There was a conflict with one or more participants schedule.'})

    #Handling GET requests for the edit page
    else:
        participants=list(Participant.objects.all().values('name','email'))
        participants_selected=getParticipants(interview)
        return render(request,'create.html',{'num':len(participants_selected),'participants':participants,'participants_selected':participants_selected,'interview':interview,'nextURL':'editParticipant','interview_id':interview.id})

# View for displaying the created interviews
def viewInterviews(request):
    data=getInterviewsDetailedData()
    return render(request,'interviews.html',{'data':data})

# View for displaying the list of participants along with their scheduled interviews
def viewParticipants(request):
    data=getParticipantsDetailedData()
    return render(request,'participants.html',{'data':data})
