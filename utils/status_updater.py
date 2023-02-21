from mainapp.models import Submission
from userauth.models import Account
from utils.email_sender import send_mail
import os
from dotenv import load_dotenv
from django.utils.timezone import localtime

status_dict = {
    'Accept':'Accepted',
    'Hold':'On Hold',
    'Reject':'Rejected',
}

def update_status(id, new_status_txt, remark):
    submission = Submission.objects.get(id=id)
    old_status = submission.status
    if new_status_txt:
        new_status = status_dict[new_status_txt]
    else:
        new_status = old_status

    if remark != "" and submission.remark != remark:
            submission.remark = remark


    if old_status == new_status:
        return -1
    else:
        submission.status = new_status
        submission.modified_on = localtime()

        submission.save()

        load_dotenv()
        # send_mail(submission.ideator.email, f"Idea status updated to {new_status}", f"Hey {submission.ideator.fullname}! Your submission in the business unit {submission.business_unit.name} has been updated from {old_status} to {new_status}. Check it here {os.getenv('WEB_URL')}#YOUR_SUBMISSIONS")

        return 1