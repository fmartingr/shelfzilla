# coding: utf-8

from django.template import Context, Template
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class Email(object):
    template = ''
    context = {}

    subject = ''
    from_email = None
    recipients = []
    text = ''

    def __init__(self, context={}):
        self.form_email = getattr(settings, 'FROM_EMAIL', 'root@localhost')
        self.context = context
        self.prepare()

    def prepare(self):
        pass

    def compile_template(self):
        tmpl = get_template(self.template)
        self.html = tmpl.render(Context(self.context))
        print(self.html.encode('utf-8'))
        self.text = strip_tags(self.html)
        print(self.text.encode('utf-8'))

    def send(self):
        if self.template:
            self.compile_template()

        message = EmailMultiAlternatives(self.subject,
                                         self.text,
                                         self.from_email,
                                         self.recipients)

        if self.template:
            message.attach_alternative(self.html, "text/html")

        message.send()


# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'
# html_content = '<p>This is an <strong>important</strong> message.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()
