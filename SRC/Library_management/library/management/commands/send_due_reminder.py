from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from library.models import BorrowRecord

class Command(BaseCommand):
    help = 'Gửi mail nhắc hạn trả sách (trước 1 ngày)'

    def handle(self, *args, **kwargs):
        records = BorrowRecord.objects.filter(status='borrowed')

        for record in records:
            if record.days_left == 1:
                send_mail(
                    subject='📚 Nhắc hạn trả sách',
                    message=(
                        f"Xin chào {record.user.user.username},\n\n"
                        f"Bạn đang mượn sách: {record.book.title}\n"
                        f"Hạn trả: {record.due_date.strftime('%d/%m/%Y')}\n\n"
                        f"Vui lòng trả sách đúng hạn hoặc gia hạn nếu cần.\n\n"
                        f"Thư viện xin cảm ơn!"
                    ),
                    from_email=None,
                    recipient_list=[record.user.user.email],
                )

                self.stdout.write(
                    f"✔ Đã gửi mail cho {record.user.user.email}"
                )
