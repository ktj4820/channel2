import os

from django.contrib import messages
from django.forms.formsets import formset_factory
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from channel2.core.views import StaffTemplateView
from channel2.settings import VIDEO_DIR
from channel2.staff.forms import StaffAccountCreateForm, StaffVideoAddForm, StaffVideoAddFormSet
from channel2.tag.models import Tag
from channel2.video.utils import extract_name, guess_tag


class StaffUserAddView(StaffTemplateView):

    template_name = 'staff/staff-user-add.html'

    def get(self, request):
        return self.render_to_response({
            'form': StaffAccountCreateForm()
        })

    def post(self, request):
        form = StaffAccountCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _('An activation email has been sent to {}').format(user.email))
            return redirect('staff.user.add')

        return self.render_to_response({
            'form': form,
        })


class StaffVideoAddView(StaffTemplateView):

    template_name = 'staff/staff-video-add.html'

    @classmethod
    def get_formset_cls(cls):
        return formset_factory(
            form=StaffVideoAddForm,
            formset=StaffVideoAddFormSet,
            extra=0,
            can_order=False,
            max_num=1000,
        )

    def get_context_data(self):
        tag_list = Tag.objects.order_by('slug').values_list('name', flat=True)
        return {'tag_list': tag_list}

    def get(self, request):
        context = self.get_context_data()

        initial = []
        for filename in os.listdir(VIDEO_DIR):
            if os.path.isdir(os.path.join(VIDEO_DIR, filename)):
                continue
            if not filename.endswith('mp4'):
                continue

            name = extract_name(filename)
            tag = name and guess_tag(name, context['tag_list'])

            initial.append({
                'filename': filename,
                'name': name,
                'tag': tag,
            })

        formset = self.get_formset_cls()(initial=initial)
        context['formset'] = formset
        return self.render_to_response(context)

    def post(self, request):
        formset = self.get_formset_cls()(data=request.POST)
        if formset.is_valid():
            count = formset.save()
            messages.success(request, _('{} videos have been added successfully.'.format(count)))
            return redirect('staff.video.add')

        context = self.get_context_data()
        context['formset'] = formset
        return self.render_to_response(context)
