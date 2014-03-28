from django.views.generic import View as DjangoView


class View(DjangoView):
    section = None

    def get_context(self, context):
        if self.section:
            context['navigation'] = {
                'section': self.section
            }

        return context
