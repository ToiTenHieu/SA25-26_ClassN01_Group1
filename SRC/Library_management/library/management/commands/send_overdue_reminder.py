from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from library.models import BorrowRecord

class Command(BaseCommand):
    help = "Gửi mail cho người quá hạn trả sách"

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
                subject="⏰ Thông báo quá hạn trả sách",
                message=(
                    f"Xin chào {record.user.user.username},\n\n"
                    f"Bạn đang quá hạn trả sách: {record.book.title}\n"
                    f"Hạn trả: {record.due_date.strftime('%d/%m/%Y')}\n"
                    f"Quá hạn: {days} ngày\n\n"
                    f"Vui lòng hoàn trả hoặc gia hạn (nếu còn lượt) sớm nhất.\n\n"
                    f"Thư viện xin cảm ơn!"
                ),
                from_email=None,
                recipient_list=[email],
            )

            sent += 1
            self.stdout.write(f"✔ Đã gửi mail quá hạn cho {email} (Record #{record.record_id})")

        self.stdout.write(self.style.SUCCESS(
            f"✅ Update borrowed->overdue: {updated} | Tổng quá hạn: {overdue_qs.count()} | Đã gửi: {sent} | Bỏ qua (không email): {skipped_no_email}"
        ))
