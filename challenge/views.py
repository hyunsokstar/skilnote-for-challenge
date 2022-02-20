from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.db.models import Q
from django.db.models import F
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse
from .models import StudentRecord, LecInfo, RecommandLecInfo, challenge_subject, LikeChallengeSubject
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LecInfoForm, challenge_subject_form
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.utils import timezone


# 1122
def delete_challenge_subject_by_id(request,id):
	user = request.user
	if request.method == "POST" and request.is_ajax():
		challenge = challenge_subject.objects.filter(Q(id=id)).delete()
		print("challenge_subject 삭제 성공 !!!!!!!!!!!!!!!!!!!", challenge)
		return JsonResponse({
			'message': 'challenge_subject 삭제 성공',
			})
	else:
		return redirect('/challenge')




class update_challenge_subject(UpdateView):
    model = challenge_subject
    form_class = challenge_subject_form

    def get_template_names(self):
        return ['challenge/challenge_subject_form.html']


# 챌린지 대주제(과목) 입력 뷰
class CreateChallengeSubjectView(LoginRequiredMixin,CreateView):
    model = challenge_subject
    form_class = challenge_subject_form

    def get_template_names(self):
        return ['challenge/challenge_subject_form.html']

    def form_valid(self, form):
        print("create challenge_subject(챌린지 과목) excute !!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        ms = form.save(commit=False)
        ms.leader = self.request.user
        ms.created = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('challenge:challenge_subject_list')


def like_or_unlike_for_challenge_subject(request):
    target_id = request.POST.get('target_id', False)
    my_id = request.POST.get('liker', False)

    print("target_id ", target_id)
    print("my_id ", my_id)

    target_challenge =  get_object_or_404(challenge_subject, id=target_id)
    me =  get_object_or_404(User, username=my_id)
    print("추천 받는 챌린지 : " , target_challenge)
    print("추천 하는 사람 : ", me)

    recommand_count = LikeChallengeSubject.objects.filter(Q(challenge=target_challenge) & Q(author=me)).count() # 내가 추천한거 있는지 확인
    print("recommand_count : ", recommand_count)

    if (recommand_count ==  0):
        rc = LikeChallengeSubject.objects.create(challenge=target_challenge , author=me) # 나의 추천 추가
        print('추천 ++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        recommand_count = LikeChallengeSubject.objects.filter(Q(challenge=target_challenge)).count() # 추천 받은 사람 점수 확인
        challenge = challenge_subject.objects.filter(Q(leader=target_challenge.leader)).update(like_count = recommand_count) # 추천 대상자 프로필 점수 반영

        return JsonResponse({
            'message': "추천 +1",
            "option":"plus",
            "recommand_count":recommand_count
        })

    else:
        LikeChallengeSubject.objects.filter(Q(challenge=target_challenge) & Q(author_id=me)).delete() # 내가 추천한거 삭제

        recommand_count = LikeChallengeSubject.objects.filter(Q(challenge=target_challenge)).count() # 추천 받은 사람 점수 확인
        print('추천 ---------------------------------------------------')
        challenge = challenge_subject.objects.filter(Q(leader=target_challenge.leader)).update(like_count = recommand_count)

        return JsonResponse({
            'message': "추천 -1 ",
            "option":"minus",
            "recommand_count":recommand_count
        })


class LecInfoDeleteView(DeleteView):
	model = LecInfo
	success_message = "challenge is removed"

	def get_success_url(self):
		challenge_title = self.object.challenge.title
		print("challenge_title : ", challenge_title)
		return reverse('challenge:lecinfo_list_for_challenge', kwargs={'challenge_title':challenge_title})

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(LecInfoDeleteView, self).delete(request, *args, **kwargs)

# 주제별 밑의 강의별 리스트

def lecinfo_list_for_challenge(request, challenge_title):
	print ("challenge subject 과목 관련 강의 리스트를 출력 합니다.")
	challenge = challenge_subject.objects.get (title=challenge_title)
	# lecinfo_list = LecInfo.objects.filter (challenge=challenge)
	lecinfo_list = challenge.lecinfo_set.all()
	print ('lecinfo_list : ', lecinfo_list)

	return render (request, 'challenge/lecinfo_list.html', {
		"lecinfo_list": lecinfo_list,
		"challenge_title": challenge_title,
        "challenge_leader": challenge.leader,
		"challenge_id":challenge.id,
		"challenge_image":challenge.image,
        "challenge_description":challenge.description
	})


# 주제별 리스트
class ChallengeSubjectList (LoginRequiredMixin, ListView):
	model = challenge_subject
	paginate_by = 10
	template_name = 'challenge/challenge_list.html'

	def get_queryset(self):
		return challenge_subject.objects.all().order_by('-like_count')


def challenge_list(request):
	return render (request, 'challenge/challenge_list.html', {
	})


def recommand_lecture(request, id):
	lecture = get_object_or_404 (LecInfo, pk=id)
	recommand_count = RecommandLecInfo.objects.filter (
		Q (author=request.user) & Q (lecinfo=lecture)).count ()
	print ("내가 강의 추천한 개수 : ", recommand_count)
	print ('id : ', id)

	id = str (id)

	if recommand_count < 1:
		lecinfo = RecommandLecInfo.objects.create (
			author=request.user, lecinfo=lecture)
		print ('추천을 추가')
	else:
		RecommandLecInfo.objects.filter (
			Q (author=request.user) & Q (lecinfo=lecture)).delete ()
		print ('추천을 삭제')

	return redirect ("/challenge/" + id)


# return reverse('challenge:lec_record_list', kwargs={'classification': id})


class CreatelecInfo (CreateView):
	model = LecInfo
	form_class = LecInfoForm
	success_message = "강의 정보 기록을 입력하였습니다."
	challenge_title = ""

	def get_template_names(self):
		return ['challenge/lecinfo_form.html']

	def form_valid(self, form):
		print ("CreateLecInfo 실행")
		fn = form.save (commit=False)
		fn.challenge = challenge_subject.objects.get(title=self.kwargs["challenge_title"])
		self.challenge_title = fn.challenge.title
		fn.manager = self.request.user
		return super ().form_valid (form)

	def get_context_data(self, **kwargs):
		ctx = super(CreatelecInfo, self).get_context_data(**kwargs)
		ctx['challenge_subject'] = self.kwargs["challenge_title"]
		return ctx

	def get_success_url(self):
		print("self.challenge_title : ", self.challenge_title)
		return reverse ('challenge:lecinfo_list_for_challenge', kwargs={'challenge_title':self.challenge_title})


class RecordUpdateView (UpdateView):
	model = StudentRecord
	fields = ['current_class']
	success_url = reverse_lazy ('challenge:lec_record_list')
	success_message = "record is modified"

	def get_success_url(self):
		classnum = self.kwargs['classification']
		return reverse ('challenge:lec_record_list', kwargs={'classification': classnum})


class LecInfoUpdateView (UpdateView):
	model = LecInfo
	fields = ['lec_name', 'manager', 'lec_url', 'git_url']

	def get_success_url(self):
		classnum = self.kwargs['classification']
		return reverse ('challenge:lec_record_list', kwargs={'classification': classnum})


class RecordDeleteView (DeleteView):
	model = StudentRecord
	success_message = "record is removed"

	def delete(self, request, *args, **kwargs):
		messages.success (self.request, self.success_message)
		return super (RecordDeleteView, self).delete (request, *args, **kwargs)

	def get_success_url(self):
		classnum = self.kwargs['classification']
		return reverse ('challenge:lec_record_list', kwargs={'classification': classnum})


# 강의 정보 및 참여자 정보
class ParticipantsListForLectureView (LoginRequiredMixin, ListView):
	model = StudentRecord
	paginate_by = 20
	ordering = ['-created']

	def get_queryset(self):
		print ("PostSearch 확인")
		classnum = self.kwargs['classification']
		object_list = StudentRecord.objects.filter (classification=classnum).order_by ('-created')
		print ("result : ", object_list)
		return object_list

	def get_context_data(self, *, object_list=None, **kwargs):
		classnum = self.kwargs['classification']
		lec_info = LecInfo.objects.get (id=classnum)
		context = super (ParticipantsListForLectureView, self).get_context_data (**kwargs)
		context['LecInfo'] = lec_info
		context['recommnad_count'] = RecommandLecInfo.objects.filter (
			lecinfo=lec_info).count ()

		return context


class LecInfoListView (LoginRequiredMixin, ListView):
	model = LecInfo
	paginate_by = 20


	def get_context_data(self, *, object_list=None, **kwargs):
		classnum = self.kwargs['challenge_title']
		return context


class CreateRecordView_11 (CreateView):
	model = StudentRecord
	fields = ['current_class', 'github_url']
	success_message = "강의 수강 기록을 입력하였습니다."

	def form_valid(self, form):
		classnum = self.kwargs['classification']

		print ("CreateRecordView 실행")
		fn = form.save (commit=False)
		fn.author = self.request.user

		lec = LecInfo.objects.get (id=classnum)
		fn.classification = lec

		return super ().form_valid (form)

	def get_success_url(self):
		classnum = self.kwargs['classification']
		return reverse ('challenge:lec_record_list', kwargs={'classification': classnum})
