'''

@author: rtermondt
'''
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.simplejson import dumps
from manager.constants import RECORDS_PER_PAGE, INITIATIVE_LAUNCH
from manager.dao import inbox_dao, initiative_dao
from manager.forms import InitiativeForm
from manager.models import Initiative, Service, Initiative_Service, \
    Initiative_Service_Offer, Milestone, Milestones, Initiative_Rating, Profile, \
    Profile_Rating, Payment_Receipt
import stripe


@login_required()
def initiative_contributors(request, uuid=None):
    system_message = None
    my_pid = request.session['profile_id']
    if request.method == 'POST':
        # need security around this: check user owns initiative, and the
        # contrib is assocaited with this initiative
        contributor_id = request.POST['contributor_id']
        uuid = request.POST['uuid']
        try:
            initiative = Initiative.objects.get(uuid=uuid, profile_id=my_pid)
        except Initiative.DoesNotExist:
            return render_to_response('system.html', {
                                      'system_message': 'Invalid data. Error code: D001',
                                      }, context_instance=RequestContext(request))
        try:
            i = Initiative_Service_Offer.objects.get(
                id=contributor_id, initiative_id=initiative.id)
            i.is_accepted = False
            i.save()
        except Initiative_Service_Offer.DoesNotExist:
            return render_to_response('system.html', {
                                      'system_message': 'Invalid data. Error code: D002',
                                      }, context_instance=RequestContext(request))
        system_message = 'Update complete'
    else:
        try:
            initiative = Initiative.objects.get(uuid=uuid)
        except Initiative.DoesNotExist:
            return render_to_response('system.html', {
                                      'system_message': 'Initiative Key not recognized.',
                                      }, context_instance=RequestContext(request))

    initiative_id = initiative.id
    contributors = Initiative_Service_Offer.objects.filter(
        initiative_id=initiative_id,
        is_accepted=True).values(
        'id',
        'service__short_desc',
        'profile__first_name',
        'profile__last_name',
        'profile__confirm_key')
    paginator = Paginator(contributors, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        contributor_list = paginator.page(page)
    except PageNotAnInteger:
        contributor_list = paginator.page(1)
    except EmptyPage:
        contributor_list = paginator.page(paginator.num_pages)
    offer_list = inbox_dao.get_offer_list(my_pid)
    return render_to_response('initiative_contributor.html', {
                              'initiative': initiative,
                              'contributor_list': contributor_list,
                              'offer_list': offer_list,
                              'system_message': system_message
                              }, RequestContext(request))


@login_required()
def contributor_offers(request, uuid=None):
    my_pid = request.session['profile_id']
    system_message = None
    if request.POST:
        offer_id = request.POST['offer_id']
        uuid = request.POST['uuid']
        try:
            initiative = Initiative.objects.get(uuid=uuid, profile_id=my_pid)
        except Initiative.DoesNotExist:
            return render_to_response('system.html', {
                                      'system_message': 'Invalid data. Error code: D001',
                                      }, context_instance=RequestContext(request))
        cmd = request.POST['cmd']
        if cmd == 'accept':
            is_accepted = True
        else:
            is_accepted = False
        try:
            i = Initiative_Service_Offer.objects.get(
                id=offer_id, initiative_id=initiative.id)
            i.is_accepted = is_accepted
            i.save()
            system_message = "Updated"
        except Initiative_Service_Offer.DoesNotExist:
            return render_to_response('system.html', {
                                      'system_message': 'Invalid data. Error code: D002',
                                      }, context_instance=RequestContext(request))
    else:
        try:
            initiative = Initiative.objects.get(uuid=uuid, profile_id=my_pid)
        except Initiative.DoesNotExist:
            return render_to_response('system.html', {
                                      'system_message': 'Initiative Key not recognized.',
                                      }, context_instance=RequestContext(request))

    offer_list = Initiative_Service_Offer.objects.filter(
        initiative_id=initiative.id,
        is_accepted=None).values(
        'id',
        'is_accepted',
        'service__short_desc',
        'profile__first_name',
        'profile__last_name',
        'profile__confirm_key',
        'initiative__id',
        'initiative__short_desc')

    paginator = Paginator(offer_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        offers = paginator.page(page)
    except PageNotAnInteger:
        offers = paginator.page(1)
    except EmptyPage:
        offers = paginator.page(paginator.num_pages)
    #service_selected = Service.objects.filter(initiative_service__initiative_id=initiative_id)
    #iso = Initiative_Service_Offer.objects.filter(initiative__profile_id=my_pid, service__service_id=initiative__).values('short_desc', 'milestones__is_completed')
    return render_to_response('contributor_offer.html', {
                              'offer_list': offers,
                              'initiative': initiative,
                              'system_message': system_message
                              }, RequestContext(request))


@login_required()
def initiatives(request):
    initiative_list = Initiative.objects.all().filter(is_public=True).values(
        'uuid',
        'short_desc',
        'profile__confirm_key',
        'profile__first_name',
        'profile__last_name'
    ).annotate(Avg('initiative_rating__rating')).order_by('-create_date')
    paginator = Paginator(initiative_list, RECORDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        initiatives = paginator.page(page)
    except PageNotAnInteger:
        initiatives = paginator.page(1)
    except EmptyPage:
        initiatives = paginator.page(paginator.num_pages)
    return render_to_response(
        'initiatives.html', {
            'initiative_list': initiatives}, RequestContext(request))


@login_required()
def my_initiatives(request):
    initiative_list = initiative_dao.initiative_list_by_profile_id(
        request.session['profile_id'])
    return render_to_response(
        'initiatives_personal.html', {
            'initiative_list': initiative_list}, RequestContext(request))


@login_required()
def initiative_view_rating(request, uuid):
    try:
        initiative = Initiative.objects.get(uuid=uuid, is_public=True)

        rating_list = Initiative_Rating.objects.filter(
            initiative_id=initiative.id).values(
            'initiative_id',
            'rating',
            'comments',
            'profile_id',
            'profile__first_name',
            'profile__last_name')
        num_ratings = rating_list.count()
        average_rating = Initiative_Rating.objects.filter(
            initiative_id=initiative.id).aggregate(
            Avg('rating')).values()[0]

        paginator = Paginator(rating_list, RECORDS_PER_PAGE)
        page = request.GET.get('page')
        try:
            rating = paginator.page(page)
        except PageNotAnInteger:
            rating = paginator.page(1)
        except EmptyPage:
            rating = paginator.page(paginator.num_pages)
        #average_rating = rating.aggregate(Avg('rating')).values()[0]

        return render_to_response('initiative_view_ratings.html', {
                                  'initiative': initiative,
                                  'average_rating': average_rating,
                                  'num_ratings': num_ratings,
                                  'rating_list': rating
                                  }, RequestContext(request))
    except Initiative.DoesNotExist:
        return render_to_response('system.html', {
                                  'system_message': 'Initiative Key not recognized.',
                                  }, context_instance=RequestContext(request))


@login_required()
def initiative_detail(request, uuid):
    try:
        #initiative_id = utils.decode_id(long(encoded_id))
        initiative = Initiative.objects.get(uuid=uuid, is_public=True)
        initiative_id = initiative.id
        sponsor_profile_id = initiative.profile_id
        my_profile_id = request.session['profile_id']
        if my_profile_id == sponsor_profile_id:
            can_rate = False
        else:
            can_rate = True
        sponsor_profile = Profile.objects.get(pk=sponsor_profile_id)
        sponsor_rating = Profile_Rating.objects.filter(
            profile_id=sponsor_profile_id)
        sponsor_avg_rating = sponsor_rating.aggregate(
            Avg('rating')).values()[0]
        service_selected = Service.objects.filter(
            initiative_service__initiative_id=initiative_id)

        rating = Initiative_Rating.objects.filter(initiative_id=initiative_id)
        num_ratings = rating.count()
        average_rating = rating.aggregate(Avg('rating')).values()[0]
        milestones_selected = Milestone.objects.filter(
            milestones__initiative_id=initiative_id).values(
            'short_desc',
            'milestones__is_completed')
        offer_list = Initiative_Service_Offer.objects.filter(
            initiative_id=initiative_id,
            is_accepted=True).values(
            'service__short_desc',
            'profile__first_name',
            'profile__last_name',
            'profile__confirm_key')

        return render_to_response('initiative_detail.html', {
                                  'initiative': initiative,
                                  'service_selected': service_selected,
                                  'milestones_selected': milestones_selected,
                                  'offer_list': offer_list,
                                  'rating': average_rating,
                                  'num_ratings': num_ratings,
                                  'sponsor_profile': sponsor_profile,
                                  'sponsor_avg_rating': sponsor_avg_rating,
                                  'can_rate': can_rate
                                  }, RequestContext(request))
    except (Initiative.DoesNotExist, ValueError):
        return render_to_response('system.html', {
                                  'system_message': 'Initiative Key not recognized.',
                                  }, context_instance=RequestContext(request))


@login_required()
def initiative_add(request):
    if request.method == 'POST':
        form = InitiativeForm(request.POST)
        if form.is_valid():
            short_desc = form.cleaned_data['short_desc']
            long_desc = form.cleaned_data['long_desc']
            is_public = form.cleaned_data['is_public']
            publish_date = None
            if is_public:
                if settings.INITIATIVE_LAUNCH_FEE == 0:
                    is_public = is_public
                    publish_date = datetime.now()
                else:
                    is_public = False
            i = Initiative.objects.create(
                profile_id=request.session['profile_id'],
                short_desc=short_desc,
                long_desc=long_desc,
                is_public=is_public,
                publish_date=publish_date)

            if settings.INITIATIVE_LAUNCH_FEE > 0 and is_public:
                system_message = 'Initiative added, payment required.'
                raw_fee = settings.INITIATIVE_LAUNCH_FEE
                display_fee = raw_fee[-2:] + '.' + raw_fee[:-2]
                return render_to_response('initiative_payment.html', {
                                          'system_message': system_message,
                                          'uuid': i.uuid,
                                          'display_fee': display_fee,
                                          'raw_fee': raw_fee,
                                          }, context_instance=RequestContext(request))
            # load data for next step
            #s = Service.objects.all().order_by('short_desc', )
            return render_to_response('initiative_add.html', {
                                      'system_message': 'Initiative created!.',
                                      'return_code': '0',
                                      'uuid': i.uuid
                                      }, RequestContext(request))
        else:
            #form = InitiativeForm()
            return render_to_response('initiative_add.html', {
                                      'form': form,
                                      }, RequestContext(request))
    else:
        form = InitiativeForm()
        return render_to_response('initiative_add.html', {
                                  'form': form,
                                  }, RequestContext(request))
        #t = loader.get_template('initiative_add.html')
        # return HttpResponse(t.render(RequestContext(request)))


@login_required()
def initiative_edit(request, uuid):
    try:

        initiative = Initiative.objects.get(
            uuid=uuid,
            profile_id=request.session['profile_id'])
        initiative_id = initiative.id

        form = InitiativeForm({
                              'short_desc': initiative.short_desc,
                              'long_desc': initiative.long_desc,
                              'is_public': initiative.is_public
                              })
        return render_to_response(
            'initiative_edit.html', {
                'form': form, 'uuid': uuid}, RequestContext(request))
    except (Initiative.DoesNotExist, ValueError):
        return render_to_response('system.html', {
                                  'system_message': 'Initiative Key not recognized.',
                                  }, context_instance=RequestContext(request))


@login_required()
def initiative_edit_save(request):
    system_message = None
    if request.method == 'POST':
        uuid = request.POST['uuid']
        initiative_id = initiative_dao.get_intitiative_id(uuid)
        form = InitiativeForm(request.POST)
        if form.is_valid():
            is_public = form.cleaned_data['is_public']
            initiative = Initiative.objects.get(pk=initiative_id)
            initiative.short_desc = form.cleaned_data['short_desc']
            initiative.long_desc = form.cleaned_data['long_desc']
            if is_public:
                if settings.INITIATIVE_LAUNCH_FEE == 0:
                    initiative.is_public = is_public
                    if initiative.publish_date is None:
                        initiative.publish_date = datetime.now()
            else:
                initiative.is_public = is_public

            initiative.save()
            if settings.INITIATIVE_LAUNCH_FEE > 0 and is_public and initiative.publish_date is None:
                raw_fee = settings.INITIATIVE_LAUNCH_FEE
                display_fee = str(raw_fee)[:-2] + '.' + str(raw_fee)[-2:]
                return render_to_response('initiative_payment.html', {
                                          'system_message': system_message,
                                          'uuid': uuid,
                                          'display_fee': display_fee,
                                          'raw_fee': raw_fee,
                                          }, context_instance=RequestContext(request))
            else:
                system_message = 'Initiative updated!'
            return render_to_response('initiative_edit.html', {
                                      'system_message': system_message,
                                      'form': None,
                                      'uuid': uuid,
                                      }, context_instance=RequestContext(request))
        else:
            system_message = 'Error'

        return render_to_response('initiative_edit.html', {
                                  'system_message': system_message,
                                  'uuid': uuid,
                                  'form': form,
                                  }, context_instance=RequestContext(request))

    else:
        system_message = 'Invalid request'
        return render_to_response('system.html', {
                                  'system_message': system_message,
                                  }, context_instance=RequestContext(request))


@login_required()
def initiative_service(request, uuid, system_message=None):
    try:
        initiative = Initiative.objects.get(
            uuid=uuid,
            profile_id=request.session['profile_id'])
        s = Service.objects.all().order_by('short_desc', )
        service_selected = Initiative_Service.objects.get_query_set(
        ).filter(initiative_id=initiative.id)
        return render_to_response('initiative_add_service.html', {
                                  'service_list': s,
                                  'service_selected': service_selected,
                                  'initiative': initiative,
                                  'system_message': system_message,
                                  }, RequestContext(request))
    except Initiative.DoesNotExist:
        return render_to_response('system.html', {
                                  'system_message': 'Initiative Key not recognized.',
                                  }, context_instance=RequestContext(request))


@login_required()
def initiative_service_add(request):
    system_message = None
    if request.POST:
        sl = request.POST.getlist('service_list')
        uuid = request.POST['uuid']
        initiative_id = initiative_dao.get_intitiative_id(uuid)
        Initiative_Service.objects.filter(initiative_id=initiative_id).delete()
        for service in sl:
            Initiative_Service.objects.create(initiative_id=initiative_id,
                                              service_id=service)
        system_message = 'Services updated'

    return initiative_service(request, uuid, system_message)
# TODO: fix html page


@login_required()
def initiative_milestones(request, uuid, system_message=None):
    try:
        initiative = Initiative.objects.get(
            uuid=uuid,
            profile_id=request.session['profile_id'])
        milestone_list = Milestone.objects.all().order_by('short_desc', )
        milestones_selected = Milestones.objects.get_query_set(
        ).filter(initiative_id=initiative.id)
        return render_to_response('initiative_milestones.html', {
                                  'milestone_list': milestone_list,
                                  "milestones_selected": milestones_selected,
                                  'initiative': initiative,
                                  'system_message': system_message
                                  }, RequestContext(request))
    except Initiative.DoesNotExist:
        return render_to_response('system.html', {
                                  'system_message': 'Initiative Key not recognized.',
                                  }, context_instance=RequestContext(request))


@login_required()
def initiative_milestones_add(request):
    system_message = None
    if request.POST:
        ml = request.POST.getlist('milestone_list')
        uuid = request.POST['uuid']
        initiative_id = initiative_dao.get_intitiative_id(uuid)
        Milestones.objects.filter(initiative_id=initiative_id).delete()
        for milestone in ml:
            Milestones.objects.create(initiative_id=initiative_id,
                                      milestone_id=milestone)
        system_message = 'Milestones updated'
        return initiative_milestones(request, uuid, system_message)


@login_required()
def initiative_service_offer(request, uuid=None):
    my_profile_id = request.session['profile_id']
    if request.POST:
        sl = request.POST.getlist('service_list')
        uuid = request.POST['uuid']
        initiative_id = initiative_dao.get_pulic_intitiative_id(uuid)

        # Initiative_Service_Offer.objects.filter(initiative_id=initiative_id,
        #                                        profile_id=my_profile_id).delete()
        existing_offers = Initiative_Service_Offer.objects.filter(
            initiative_id=initiative_id,
            profile_id=my_profile_id)

        existing_service_ids = []
        for existing_service in existing_offers:
            existing_service_ids.append(existing_service.service_id)
            if str(existing_service.service_id) not in sl:
                Initiative_Service_Offer.objects.get(
                    pk=existing_service.id).delete()

        for service in sl:
            if int(service) not in existing_service_ids:
                Initiative_Service_Offer.objects.create(
                    profile_id=request.session['profile_id'],
                    initiative_id=initiative_id,
                    service_id=service)
        system_message = 'Update complete'
    else:
        system_message = None

    s = Service.objects.all().order_by('short_desc', )
    service_selected = Initiative_Service_Offer.objects.get_query_set().filter(
        initiative_id=initiative_dao.get_pulic_intitiative_id(uuid),
        profile_id=my_profile_id)
    return render_to_response('initiative_service_offer.html', {
                              'service_list': s,
                              'service_selected': service_selected,
                              'uuid': uuid,
                              'system_message': system_message,
                              }, RequestContext(request))


@login_required()
def initiative_rate(request, uuid=None):
    system_message = None
    my_profile_id = request.session['profile_id']

    if request.POST:
        initiative_id = initiative_dao.get_pulic_intitiative_id(
            request.POST['uuid'])
        initiative = Initiative.objects.get(pk=initiative_id)
        if my_profile_id == initiative.profile_id:
            system_message = 'You can not rate your own Initiative!'
            return render_to_response(
                'system.html', {
                    'system_message': system_message, }, context_instance=RequestContext(request))
        if 'star' in request.POST:
            rating = Decimal(request.POST['star'])
        else:
            system_message = "Error, you must select a rating."
            if 'initiative_rating_id' in request.POST:
                init_rating = Initiative_Rating.objects.get(
                    pk=request.POST['initiative_rating_id'])
            else:
                init_rating = None

            return render_to_response('initiative_rate.html', {
                                      'system_message': system_message,
                                      'initiative_id': initiative_id,
                                      'init_rating': init_rating,
                                      }, RequestContext(request))

        comments = request.POST['comments']
        if 'initiative_rating_id' in request.POST:
            initiative_rating_id = request.POST['initiative_rating_id']
            system_message = "Your rating has been updated"
            init_rating = Initiative_Rating.objects.get(
                pk=initiative_rating_id)
            init_rating.rating = rating
            init_rating.comments = comments
            init_rating.save()
        else:
            system_message = "Your rating has been added"
            init_rating = Initiative_Rating.objects.create(
                initiative_id=initiative_id,
                profile_id=my_profile_id,
                rating=rating,
                comments=comments
            )
    else:
        try:
            init_rating = Initiative_Rating.objects.get(
                initiative_id=Initiative.objects.get(
                    uuid=uuid).id,
                profile_id=my_profile_id)
            system_message = "Update rating"
        except Initiative_Rating.DoesNotExist:
            init_rating = None

    return render_to_response('initiative_rate.html', {
                              'system_message': system_message,
                              'uuid': uuid,
                              'init_rating': init_rating,
                              }, RequestContext(request))


@login_required()
def initiative_auto(request):
    initiatives = Initiative.objects.filter(
        short_desc__startswith=request.GET['term'], is_public=True)
    results = []
    for initiative in initiatives:
        i_dict = {'id': initiative.id, 'label':
                  initiative.short_desc, 'value': initiative.short_desc}
        results.append(i_dict)

    return HttpResponse(dumps(results), mimetype='application/json')


@login_required()
def initiative_search(request):
    system_message = None
    if request.POST:
        if not request.POST.get('search', ''):
            system_message = 'Search term required'
            initiative_list = None
        else:
            search = request.POST['search']
            initiative_list = Initiative.objects.filter(
                short_desc__startswith=search,
                is_public=True).values(
                'uuid',
                'short_desc',
                'profile_id',
                'profile__first_name',
                'profile__last_name').annotate(
                Avg('initiative_rating__rating'))
            paginator = Paginator(initiative_list, RECORDS_PER_PAGE)
            page = request.GET.get('page')
            try:
                initiatives = paginator.page(page)
            except PageNotAnInteger:
                initiatives = paginator.page(1)
            except EmptyPage:
                initiatives = paginator.page(paginator.num_pages)

            return render_to_response('initiative_search.html', {
                                      'system_message': system_message,
                                      'initiative_list': initiatives,
                                      }, RequestContext(request))

    else:
        initiative_list = None

    return render_to_response('initiative_search.html', {
                              'system_message': system_message,
                              'initiative_list': initiative_list,
                              }, RequestContext(request))


@login_required()
def initiative_milestone_date(request, uuid=None):
    system_message = None
    if request.POST:
        system_message = 'post'
        uuid = request.POST['uuid']
        milestone_id = request.POST['milestone_id']
        target_date = request.POST['target_date']
        complete_date = request.POST['complete_date']
        if target_date != '' or complete_date != '':
            milestone = Milestones.objects.get(pk=milestone_id)
            if target_date != '':
                milestone.target_date = datetime.strptime(
                    target_date,
                    "%m/%d/%Y").strftime("%Y-%m-%d")
            if complete_date != '':
                milestone.complete_date = datetime.strptime(
                    complete_date,
                    "%m/%d/%Y").strftime("%Y-%m-%d")
            milestone.save()
            system_message = 'Milestone date updated'
        else:
            system_message = 'Nothing to update:' + \
                target_date + ':' + complete_date

    milestones = Milestones.objects.filter(
        initiative_id=initiative_dao.get_intitiative_id(uuid)).values(
        'id',
        'initiative_id',
        'target_date',
        'complete_date',
        'milestone__short_desc')
    return render_to_response('initiative_milestone_dates.html', {
                              'system_message': system_message,
                              'milestones': milestones,
                              'uuid': uuid
                              }, RequestContext(request))


@login_required()
def initiative_payment(request):
    system_message = None
    if request.POST:

        profile_id = request.session['profile_id']
        uuid = request.POST['uuid']
        # Set your secret key: remember to change this to your live secret key in production
        # See your keys here https://manage.stripe.com/account
        stripe.api_key = settings.STRIPE_API_KEY

        # Get the credit card details submitted by the form
        token = request.POST['stripeToken']
        amount = settings.INITIATIVE_LAUNCH_FEE
        currency = 'usd'
        processor = 'stripe'
        # Create the charge on Stripe's servers - this will charge the user's
        # card
        try:
            # TODO find out what stripe.Charge.create() returns
            charge = stripe.Charge.create(
                amount=amount,  # amount in cents, again
                currency=currency,
                card=token,
                description=INITIATIVE_LAUNCH
            )
            initiative_id = initiative_dao.get_intitiative_id(uuid)

            payment = Payment_Receipt.objects.create(
                profile_id=profile_id,
                processor=processor,
                table_desc='initiative',
                table_key=initiative_id,
                ref_id=charge.id,
                short_desc=INITIATIVE_LAUNCH,
                amount=amount,
                currency_code=currency,
                transaction_date=datetime.now())

            initiative = Initiative.objects.get(pk=initiative_id)
            initiative.is_public = True,
            initiative.publish_date = datetime.now()
            initiative.save()
            system_message = 'Payment completed successfully! Your Initiative has been published!.'

        except stripe.CardError as e:
            # The card has been declined
            system_message = 'An error has occurred processing request.'

        return render_to_response('payment.html', {
                                  'system_message': system_message,
                                  }, context_instance=RequestContext(request))
    else:
        system_message = 'Invalid request.'
        return render_to_response('system.html', {
                                  'system_message': system_message,
                                  }, context_instance=RequestContext(request))
