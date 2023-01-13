from mainapp.models import Submission
from userauth.models import Account
from utils.email_sender import send_mail
import os
from dotenv import load_dotenv

status_dict = {
    'Accept':'Accepted',
    'Hold':'On Hold',
    'Reject':'Rejected',
}

def update_status(id, new_status_txt):
    submission = Submission.objects.get(id=id)
    old_status = submission.status
    new_status = status_dict[new_status_txt]

    if old_status == new_status:
        return -1
    else:
        submission.status = new_status
        submission.save()

        load_dotenv()
        send_mail(submission.ideator.email, f"Idea status updated to {new_status}", f"Hey {submission.ideator.fullname}! Your submission in the business unit {submission.business_unit.name} has been updated from {old_status} to {new_status}. Check it here {os.getenv('WEB_URL')}#YOUR_SUBMISSIONS")

        return 1