from django.shortcuts import render_to_response, get_object_or_404
from SampleISP.models import Router, Switch, RAS, Customer, RouterPort, SwitchPort, IPaddress
from django.views import generic
from SampleISP.forms import RouterForm, RouterPortForm, RouterPortFormSetWithExtra, RouterPortFormSet, \
                            RASForm, IPaddressInlineFormSet
from SampleISP.AjaxableResponseMixin import AjaxableResponseMixin, JSONResponseMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from extra_views import ModelFormSetView, FormSetView
from SampleISP.serializers import RouterPortSerializer
from django.views.decorators.csrf import csrf_protect
from django.db import transaction

# index
def index(request):
    #### set all table view's anchor url to customers, because I just made the customer table view only
    table_list = ({'url':'customers','table_name':'Customers'},
                  {'url':'routers','table_name':'Routers'},
                  {'url':'routerports','table_name':'RouterPorts'},
                  {'url':'routerports/manage','table_name':'Manage RouterPorts'},
                  {'url':'routerports/new_manage','table_name':'Manage RouterPorts using Class-based Formset'},
                  {'url':'customers','table_name':'Switches'},
                  {'url':'ras','table_name':'Remote Access Servers'})
    return render_to_response('SampleISP/index.html',{'table_list': table_list, 
                                                      'user': request.user,
                                                      'title': 'Table List'})

# customers
@login_required()
def customer_list(request):
    # get current request sort column
    order_column = request.REQUEST.get('o', 'customerID')
    # check previous sort column and sort order
    prev_order_column = request.REQUEST.get('po', '')
    prev_ascending = request.REQUEST.get('asc', '-')
    #decide current sort order
    if order_column == prev_order_column:
        # when previous sort column is same with current sort column
        if prev_ascending == '':
            # and if previous sort order is ascending, set descending order
            ascending = '-' 
        else:
            # if previous sort column is different with current one, set ascending order
            ascending = ''
    else:
        # otherwise ascending order
        ascending = ''
    #get customers with requested sort column and order
    customer_list = Customer.objects.all().order_by(ascending + order_column)
    return render_to_response('SampleISP/customer_list.html',{'customer_list': customer_list, 
                                                              'user': request.user,
                                                              'order_column': order_column,
                                                              'ascending': ascending,
                                                              'title': 'Customer List'})

@login_required()
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render_to_response('SampleISP/customer_detail.html',{'customer': customer, 
                                                                'user': request.user,
                                                                'title': customer.full_name})

# routers
@login_required()
def router_list(request):
    router_list = Router.objects.all().order_by('router_name')
    return render_to_response('SampleISP/router_list.html',{'router_list': router_list,
                                                            'user': request.user,
                                                            'title': 'Router List'})

class RouterListView(generic.ListView):
    context_object_name = "router_list"
    model = Router
    # queryset = Router.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RouterListView, self).get_context_data(**kwargs)
        # Add extra context as you want
        context['title'] = 'Router List'
        return context

    def get_queryset(self):
        '''
        Dynamic Filtering : http://127.0.0.1:8000/SampleISP/routers/AL/
        '''
        router_objects = super(RouterListView, self).get_queryset()
        if self.args:
            #model = get_object_or_404(Router, router_model__iexact=self.args[0])
            model = self.args[0]
            return router_objects.filter(router_model=model)
        else:
            return router_objects

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RouterListView, self).dispatch(*args, **kwargs)

# class RouterDetailView(generic.FormView):
#     model = Router
#     template_name = 'SampleISP/router_detail.html'
#     form_class = RouterForm
#
#     def get_context_data(self, **kwargs):
#         context = super(RouterDetailView, self).get_context_data(**kwargs)
#         if(self.kwargs['pk']):
#             pk = self.kwargs['pk']
#             router = Router.objects.get(id = pk)
#             form = RouterForm(router)
#         # Add extra context as you want
#         context['title'] = 'Router Detail'
#         return context
class RouterDetailView(AjaxableResponseMixin, generic.UpdateView):
    context_object_name = "router"
    model = Router
    template_name = 'SampleISP/router_detail.html'
    form_class = RouterForm
    success_url = reverse_lazy('SampleISP:router_list')

    def post(self, request, *args, **kwargs):
        return super(RouterDetailView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(RouterDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RouterDetailView, self).get_context_data(**kwargs)
        # Add extra context as you want
        context['title'] = context['router'].router_name()
        context['form'].fields['router_name'].initial = 'ISP-R-{0}-{1:08d}'.format(self.object.router_model, self.object.id)
        return context

    # def get_success_url(self):
    #     return reverse('SampleISP:router_list')

    def get_queryset(self):
        return super(RouterDetailView, self).get_queryset()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RouterDetailView, self).dispatch(*args, **kwargs)

class RouterPortListView(generic.ListView):
    model = RouterPort
    # optional (the default is app_name/modelNameInLowerCase_list.html; which will look into your templates folder for that path and file)
    template_name = 'SampleISP/routerport_list.html'
    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class
    context_object_name = "routerport_list"
    paginate_by = 5  #and that's it !!

    def get_context_data(self, **kwargs):
        context = super(RouterPortListView, self).get_context_data(**kwargs)
        # Add extra context as you want
        context['title'] = 'Router Port List'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RouterPortListView, self).dispatch(*args, **kwargs)

class RouterPortDetailView(AjaxableResponseMixin, generic.UpdateView):
    model = RouterPort
    template_name = 'SampleISP/routerport_detail.html'
    form_class = RouterPortForm
    success_url = reverse_lazy('SampleISP:routerport_list')
    serializer = RouterPortSerializer

    @transaction.commit_on_success
    def post(self, request, *args, **kwargs):
        return super(RouterPortDetailView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super(RouterPortDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RouterPortDetailView, self).get_context_data(**kwargs)
        # Add extra context as you want
        context['title'] = context['routerport'].port_name
        context['css'] = context['form'].media['css']
        context['js'] = context['form'].media['js']
        # context['js']._js.append(settings.STATIC_URL + "js/SampleISP/routerport_detail.js")
        return context

    def form_valid(self, form):
        return super(RouterPortDetailView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RouterPortDetailView, self).dispatch(*args, **kwargs)

@login_required()
def manage_routerport(request, port_name_filter=None):
    if request.method == 'POST':
        formset = RouterPortFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
            return HttpResponseRedirect(reverse('SampleISP:routerport_list'))
        else:
            return render_to_response("SampleISP/manage_routerport.html", {
                "formset": formset,
                "title": 'Manage',
            }, context_instance = RequestContext(request))
    else:
        if port_name_filter:
            formset = RouterPortFormSet(queryset=RouterPort.objects.filter(port_name__contains=port_name_filter))
        else:
            formset = RouterPortFormSet(queryset=RouterPort.objects.all())
        return render_to_response("SampleISP/manage_routerport.html", {
            "formset": formset,
            "title": 'Manage',
        }, context_instance = RequestContext(request))

class RouterPortManageView(AjaxableResponseMixin, FormSetView):
    template_name = 'SampleISP/manage_routerport.html'
    form_class = RouterPortForm
    success_url = reverse_lazy('SampleISP:routerport_list')

    def post(self, request, *args, **kwargs):
        formset = RouterPortFormSetWithExtra(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        #     # do something.
        #     return HttpResponseRedirect(reverse('SampleISP:routerport_list'))
        # else:
        #     return render_to_response("SampleISP/manage_routerport.html", {
        #         "formset": formset,
        #         "title": 'Manage',
        #     }, context_instance = RequestContext(request))
        return super(RouterPortManageView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if args:
            self.formset = RouterPortFormSetWithExtra(queryset=RouterPort.objects.filter(port_name__contains=args[0]))
        else:
            self.formset = RouterPortFormSetWithExtra(queryset=RouterPort.objects.all())
        # return render_to_response("SampleISP/manage_routerport.html", {
        #     "formset": self.formset,
        #     "title": 'Manage',
        # }, context_instance = RequestContext(request))
        return super(RouterPortManageView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RouterPortManageView, self).get_context_data(**kwargs)
        # Add extra context as you want
        context['formset'] = self.formset
        context['title'] = 'Manage'
        return context

    def form_valid(self, form):
        return super(RouterPortManageView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RouterPortManageView, self).dispatch(*args, **kwargs)

@login_required()
def add_routerport(request):
    if request.method == 'POST':
        formset = RouterPortFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            # do something.
    else:
        formset = RouterPortFormSet(queryset=RouterPort.objects.none())
    return render_to_response("SampleISP/manage_routerport.html", {
        "formset": formset,
        "title": 'Add',
    }, context_instance = RequestContext(request))


# switches
@login_required()
def switch_list(request):
    switch_list = Switch.objects.all().order_by('switch_name')
    return render_to_response('SampleISP/switch_list.html',{'switch_list': switch_list, 
                                                            'user': request.user,
                                                            'title': 'Switch List'})

# Remote Access Servers
@login_required()
def ras_list(request):
    ras_list = RAS.objects.all().order_by('ras_name')
    return render_to_response('SampleISP/ras_list.html',{'ras_list': ras_list, 
                                                         'user': request.user,
                                                         'title': 'Remote Access Server List'})
class RASListView(generic.ListView):
    model = RAS
    # optional (the default is app_name/modelNameInLowerCase_list.html; which will look into your templates folder for that path and file)
    template_name = 'SampleISP/ras_list.html'
    #default is object_list as well as model's_verbose_name_list and/or model's_verbose_name_plural_list, if defined in the model's inner Meta class
    context_object_name = "ras_list"
    paginate_by = 5  #and that's it !!

    def get_context_data(self, **kwargs):
        context = super(RASListView, self).get_context_data(**kwargs)
        # Add extra context as you want
        context['title'] = 'Remote Access Servers'
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RASListView, self).dispatch(*args, **kwargs)


class RasManageView(AjaxableResponseMixin, generic.CreateView):
    template_name = 'SampleISP/ras_and_ipaddress.html'
    form_class = RASForm
    second_form_class = IPaddressInlineFormSet
    success_url = reverse_lazy('SampleISP:ras_list')

    def post(self, request, *args, **kwargs):
        # # get the user instance
        # self.object = self.get_object()
        # # determine which form is being submitted
        # # uses the name of the form's submit button
        # if 'ras_form' in request.POST:
        #     # get the primary form
        #     form_class = self.get_form_class()
        #     form_name = 'ras_form'
        # else:
        #     # get the secondary form
        #     form_class = self.second_form_class
        #     form_name = 'ipaddress_form'
        #
        # # get the form
        # form = self.get_form(form_class)
        #
        # # validate
        # if form.is_valid():
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(**{form_name: form})
        return super(RasManageView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RasManageView, self).get_context_data(**kwargs)
        instance = None
        ipaddress_pk = self.kwargs.get('pk')
        if ipaddress_pk:
            instance = get_object_or_404(RAS, pk=ipaddress_pk)
        if self.request.POST:
            context['ras_form'] = RASForm(self.request.POST, instance=instance)
            context['ipaddress_formset'] = IPaddressInlineFormSet(self.request.POST, instance=instance)
        else:
            context['ras_form'] = RASForm(instance=instance)
            context['ipaddress_formset'] = IPaddressInlineFormSet(instance=instance)
        # Add extra context as you want
        context['title'] = instance.ras_name
        context['ras_form'].fields['ras_name'].initial = 'ISP-R-{0}-{1:08d}'.format(instance.ras_model, instance.id)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['ras_form']
        formset = context['ipaddress_formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
        #     return HttpResponseRedirect(reverse('SampleISP:ras_list'))
        # else:
        #     return self.render_to_response(self.get_context_data(form=form))
        return super(RasManageView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RasManageView, self).dispatch(*args, **kwargs)

