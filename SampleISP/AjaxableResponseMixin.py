__author__ = 'austin_45B_Kerkhoff'

import json
from rest_framework.renderers import JSONRenderer, XMLRenderer, BrowsableAPIRenderer, JSONPRenderer

from django.http import HttpResponse
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        # data = json.dumps(context)
        data = JSONRenderer().render(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def render_to_jsonp_response(self, context, **response_kwargs):
        # data = json.dumps(context)
        callback = self.request.REQUEST['callback']
        data = JSONRenderer().render(context)
        response_kwargs['content_type'] = 'application/javascript'
        jsonp = callback + b'(' + data + b');'
        return HttpResponse(jsonp, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            # return self.render_to_json_response(form.errors, status=400)
            form_error_html = str(form.errors)
            response_dict = {'errors_html': form_error_html,}
            response_dict = dict(response_dict, **form.errors)
            return self.render_to_json_response(response_dict, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            # if self.request.META['HTTP_ACCEPT'] == 'application/json':
            if 'application/json' in self.request.META['HTTP_ACCEPT']:
                serializer = self.serializer(self.object)
                data = serializer.data
                data['api'] = self.request.path
                return self.render_to_json_response(data)
            elif 'application/javascript' in self.request.META['HTTP_ACCEPT']:
                serializer = self.serializer(self.object)
                data = serializer.data
                data['api'] = self.request.path
                return self.render_to_jsonp_response(data)
        # if self.request.is_ajax():
        #     if 'accept' in self.request.POST.keys():
        #         if self.request.POST['accept']=='json':
        #             # data = {
        #             #     # 'pk': self.object.pk,
        #             # }
        #             # for field in self.object._meta.fields:
        #             #     data[field.name] = field.value_to_string(self.object)
        #             serializer = self.serializer(self.object)
        #             data = serializer.data
        #             data['api'] = self.request.path
        #             return self.render_to_json_response(data)
        return response

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

class HybridDetailView(JSONResponseMixin,SingleObjectTemplateResponseMixin, BaseDetailView):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format','html') == 'json':
            return JSONResponseMixin.render_to_response(self, context)
        else:
            return SingleObjectTemplateResponseMixin.render_to_response(self, context)

