from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.db import transaction
from django.template import loader

from apps.base.models import Member, EducationalYear


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('emails_file', nargs=1)

    def handle(self, *args, **options):
        emails_file = options.get('emails_file', [None])[0]

        if not emails_file:
            self.stdout.write(self.style.ERROR('File is required'))
            return

        had_error = False

        file = open(str(emails_file), 'r')
        l_number = 0
        edu_years = dict()
        try:
            for line in file.read().split('\n'):
                l_number += 1
                line = line.replace(';', '')
                if not line:
                    continue
                splitted_line = line.split(',')
                try:
                    new_std_id = splitted_line[0]
                    new_email = splitted_line[1].lower()
                    if new_std_id[:2] in edu_years:
                        new_start_year = edu_years[new_std_id[:2]]
                    else:
                        ey, created = EducationalYear.objects.get_or_create(year=1300 + int(new_std_id[:2]))
                        new_start_year = ey
                        edu_years[new_std_id[:2]] = ey
                except:
                    self.stdout.write(self.style.ERROR('line ' + str(l_number) + ' has some errors. [line=' + line + ']'))
                    had_error = True
                    continue

                new_password = Member.objects.make_random_password(length=7)
                if '@' in new_email:
                    new_username = new_email[:new_email.find('@')]
                else:
                    new_username = new_email
                    new_email = new_username + "@ce.sharif.edu"
                try:
                    member = Member.objects.get(username=new_username)
                except:
                    try:
                        with transaction.atomic():
                            context = {
                                'site': {
                                    'domain': 'shora.ce.sharif.edu'
                                },
                                'username': new_username,
                                'password': new_password,
                                'secure': False,
                            }
                            subject = loader.render_to_string("account_create/new_account_email_subject.txt",
                                                              context).strip()
                            text_body = loader.render_to_string("account_create/new_account_email.txt", context).strip()

                            msg = EmailMessage(subject=subject, from_email="shora.cesharif@gmail.com", to=[new_email],
                                               body=text_body)
                            msg.send()
                            member = Member.objects.create(username=new_username,
                                                           std_id=new_std_id,
                                                           email=new_email,
                                                           password=make_password(new_password),
                                                           start_year=new_start_year)
                            self.stdout.write(self.style.SUCCESS('Created account for ') + new_username + ' (' + new_std_id + ')')
                    except:
                        self.stdout.write(self.style.ERROR('Could not create account for ' + str(l_number) + 'th line. [line=' + line + ']'))
                        had_error = True

            if had_error:
                self.stdout.write("making account for this lines was impossible, please contact some developer!")
            else:
                self.stdout.write(self.style.SUCCESS('Success!'))
        finally:
            file.close()
