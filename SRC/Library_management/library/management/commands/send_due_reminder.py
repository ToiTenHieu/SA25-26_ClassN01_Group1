from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from library.models import BorrowRecord

class Command(BaseCommand):
    help = 'sent a reminder email about the book return deadline (one day in advance).'

    def handle(self, *args, **kwargs):
        records = BorrowRecord.objects.filter(status='borrowed')

        for record in records:
            if record.days_left == 1:
                send_mail(
                    subject='Reminder of book return deadline',
                    message=(
                        f"Hello {record.user.user.username},\n\n"
                        f"You are borrowing the book: {record.book.title}\n"
                        f"Return deadline: {record.due_date.strftime('%d/%m/%Y')}\n\n"
                        f"Please return the book on time or extend the loan if needed.\n\n"
                        f"Thank you for using our library!"
                    ),
                    from_email=None,
                    recipient_list=[record.user.user.email],
                )

                self.stdout.write(
                    f"[OK] Sent reminder email to {record.user.user.email}"
                )
