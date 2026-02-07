from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from library.models import BorrowRecord

class Command(BaseCommand):
    help = "Send an email to the person who is overdue on returning the book."

    def handle(self, *args, **kwargs):
        today = timezone.localdate()

        # 1) Đồng bộ trạng thái: borrowed nhưng đã quá hạn => đổi sang overdue
        updated = BorrowRecord.objects.filter(
            status="borrowed",
            due_date__lt=today
        ).update(status="overdue")

        # 2) Lấy danh sách quá hạn thực sự (chưa trả + due_date < today)
        overdue_qs = BorrowRecord.objects.filter(
            status__in=["borrowed", "overdue"],
            due_date__lt=today
        ).select_related("user__user", "book")

        sent = 0
        skipped_no_email = 0

        for record in overdue_qs:
            email = getattr(record.user.user, "email", None)
            if not email:
                skipped_no_email += 1
                continue

            # late_days của bạn chỉ đúng nếu status=overdue, nên đảm bảo như trên
            days = (today - record.due_date).days

            send_mail(
                subject="Overdue Book Return Reminder",
                message=(
                    f"Hello {record.user.user.username},\n\n"
                    f"You are overdue returning the book: {record.book.title}\n"
                    f"Return deadline: {record.due_date.strftime('%d/%m/%Y')}\n"
                    f"Overdue by: {days} days\n\n"
                    f"Please return or extend the loan (if you still have one) as soon as possible.\n\n"
                    f"Thank you for using our library!"
                ),
                from_email=None,
                recipient_list=[email],
            )

            sent += 1
            self.stdout.write(f"[OK] Sent overdue reminder email to {email} (Record #{record.record_id})")

        self.stdout.write(self.style.SUCCESS(
            f"[SUCCESS] Update borrowed->overdue: {updated} | total overdue: {overdue_qs.count()} | Sent emails: {sent} | Skipped (no email): {skipped_no_email}"
        ))
