from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from . forms import SignupForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from wm.models import RecommandationUserAboutSkillNote, AllowListForSkilNote
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordChangeView as AuthPasswordChangeView,
)



def login(request):
    return render(request, 'login.html', {})


def Logout(request):
    auth_logout(request)
    return redirect('/accounts/login')


def delete_for_liker_user_for_me(request):
    if request.method == "POST" and request.is_ajax():

        target_user_id = request.POST['target_user_id']
        author_id = request.POST['author_id']
        print("target_user_id : ", target_user_id)
        print("author_id : ", author_id)
        author_name = User.objects.get(id=author_id).username
        target_name = User.objects.get(id=target_user_id).username

        result1 = RecommandationUserAboutSkillNote.objects.filter(
            Q(user=target_user_id) & Q(author_id=author_id)).delete()
        print(author_name, "의 ", target_name, "에 대한 좋아요 삭제 Success!! ")

        message = '{}님의 {}에 대한 좋아요 삭제'.format(
            author_name, request.user.username)

        return JsonResponse({
            'message': message,
        })
    else:
        return redirect('/wm/myshorcut/')


def delete_for_my_favorite_user(request):
    if request.method == "POST" and request.is_ajax():

        target_user = request.POST['target_user']
        targetUser_id = User.objects.get(username=target_user).id
        print("targetUser_id : ", targetUser_id)
        result1 = RecommandationUserAboutSkillNote.objects.filter(
            Q(user=targetUser_id) & Q(author_id=request.user)).delete()
        print(request.user, "의", target_user, "에 대한 좋아요 삭제 Success!! ")

        message = '{}님의 {}에 대한 좋아요 삭제'.format(request.user, target_user)

        return JsonResponse({
            'message': message,
        })
    else:
        return redirect('/wm/myshorcut/')


def like_or_unlike(request):
    target_user = request.POST.get('target_user', False)
    my_id = request.POST.get('liker', False)

    print("target_user ", target_user)
    print("my_id ", my_id)

    target_user = get_object_or_404(User, username=target_user)
    me = get_object_or_404(User, username=my_id)
    print("추천 받는 사람 : ", target_user)
    print("추천 하는 사람 : ", me)

    recommand_count = RecommandationUserAboutSkillNote.objects.filter(
        Q(user=target_user) & Q(author_id=me)).count()  # 내가 추천한거 있는지 확인
    print("recommand_count : ", recommand_count)

    if (recommand_count == 0):
        rc = RecommandationUserAboutSkillNote.objects.create(
            user=target_user, author_id=me)  # 나의 추천 추가
        print('추천 ++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        recommand_count = RecommandationUserAboutSkillNote.objects.filter(
            Q(user=target_user)).count()  # 추천 받은 사람 점수 확인

        profile = Profile.objects.filter(Q(user=target_user)).update(
            skill_note_reputation=recommand_count)  # 추천 대상자 프로필 점수 반영

        return JsonResponse({
            'message': "추천 +1",
            "option": "plus",
            "recommand_count": recommand_count
        })

    else:
        RecommandationUserAboutSkillNote.objects.filter(
            Q(user=target_user) & Q(author_id=me)).delete()  # 내가 추천한거 삭제

        recommand_count = RecommandationUserAboutSkillNote.objects.filter(
            Q(user=target_user)).count()  # 추천 받은 사람 점수 확인
        print('추천 ---------------------------------------------------')
        profile = Profile.objects.filter(Q(user=target_user)).update(
            skill_note_reputation=recommand_count)

        return JsonResponse({
            'message': "추천 -1 ",
            "option": "minus",
            "recommand_count": recommand_count
        })


# 2244
def delete_login_user(request):
    if request.method == "POST" and request.is_ajax():
        allowlistupdate = AllowListForSkilNote.objects.filter(member=request.user.username).delete()
        print("allowlistupdate delete_login_user count: ", allowlistupdate)
        print("request.user.username : ", request.user.username)        
        
        userId = request.POST['userId']
        user_id_for_delete = User.objects.get(username=userId)
        print("userId : ", userId)
        result1 = RecommandationUserAboutSkillNote.objects.filter(
            Q(author_id=user_id_for_delete)).delete()
        result2 = User.objects.filter(Q(username=userId)).delete()
        print('회원 정보 삭제 (좋아요 목록 삭제 성공) ', result1)
        print('회원 정보 삭제 (회원 정보 삭제 성공) ', result2)

        return JsonResponse({
            'message': '좋아요 정보 유저 정보 삭제 성공 ',
        })
    else:
        return redirect('/wm/myshorcut/')


def user_profile_information_view(request, user):
    print("my_profile_information_view 실행")
    print("my_profile_information_view 실행 user : ", user)

    # profile_user = User.objects.filter(username=user)
    profile_user = User.objects.get(username=user)
    profile_user_id = profile_user.id
    print("profile_user : ", profile_user)
    print("profile_user_id : ", profile_user_id)

    user_favorite = []  # 유저가 좋아하는 사람 목록 담을 배열
    user_favorite_list = RecommandationUserAboutSkillNote.objects.filter(
        author_id=profile_user)  # 유저가 좋아하는 사람 목록 검색
    print("user_favorite_list : ", user_favorite_list)

    like_check = RecommandationUserAboutSkillNote.objects.filter(
        author_id=request.user, user=profile_user).count()  # 내가 유저 페이지 유저 좋아요 눌렀는지 확인
    print("like_check : ", like_check)

    if(like_check == 0):
        like_check = "noLike"
    else:
        like_check = "Like"

    for x in user_favorite_list:
        print("내가 추천한 user_id : ", x.user_id)
        user_favorite.append(x.user_id)

    my_favorite_user_list = User.objects.filter(
        id__in=user_favorite).order_by('-profile__skill_note_reputation')
    print("my_favorite_user_list : ", my_favorite_user_list)

    return render(request, 'accounts2/user_profile.html', {
        "profile_user": profile_user,
        "my_favorite_user_list": my_favorite_user_list,
        "like_check": like_check,
    })


# 2244
def update_for_profile(request, id):
    print("업데이트 확인")
    
    user = request.user
    if request.method == "POST" and request.is_ajax():
        profile_user = request.POST.get('profile_user', '')
        profile_email = request.POST.get('profile_email', '')
        # profile_public = request.POST.get('profile_public','')
        profile_lecture_url = request.POST.get('profile_lecture_url', '')
        profile_github_original = request.POST.get(
            'profile_github_original', '')
        profile_github1 = request.POST.get('profile_github1', '')
        profile_github2 = request.POST.get('profile_github2', '')
        profile_github3 = request.POST.get('profile_github3', '')
        profile_github4 = request.POST.get('profile_github4', '')
        profile_id = request.POST.get('profile_id', '')
        update_for_profile = request.POST.get('update_for_profile', '')
        profile_first_category = request.POST.get('first_category', '')
        profile_last_category = request.POST.get('last_category', '')
        profile_public = request.POST.get('profile_public', '')
        
        print("profile_public : ", profile_public)
        print("profile_user : ", profile_user)

        print("update_for_profile (view) 실행")
        try:
            user_exists = User.objects.get(username=profile_user)
        except:
            user_exists = None
        print("user_exists : ", user_exists)
        if(user_exists != None and user_exists.username != request.user.username):
            return JsonResponse({
                'message': '업데이트 실패 , user 중복'
            })

        # 2244
        allowlistupdate = AllowListForSkilNote.objects.filter(member=request.user.username).update(member=profile_user)
        print("allowlistupdate update count : ", allowlistupdate)
        user = User.objects.filter(username=request.user.username).update(username=profile_user)
        
        
        print("user : ", user)
        profile = Profile.objects.filter(id=profile_id).update(
            email=profile_email,
            # public = profile_public,
            lecture_url=profile_lecture_url,
            github_original=profile_github_original,
            github1=profile_github1,
            github2=profile_github2,
            github3=profile_github3,
            github4=profile_github4,
            first_category=profile_first_category,
            last_category=profile_last_category,
            public=profile_public
        )
        print('update_for_profile Success !!!!!!!!!')
        return JsonResponse({
            'message': 'MyProfile Update Success',
        })
    else:
        return redirect('/todo')


class my_profile_information_view(LoginRequiredMixin, ListView):
    paginate_by = 10
    # if 'q' in request.GET:
    #     query = request.GET.get('q')
    #     print("query : ", query)

    def get_template_names(self):
        if self.request.is_ajax():
            print("user list ajax 요청 확인")
            return ['accounts2/my_profile.html']
        return ['accounts2/my_profile.html']

    def get_queryset(self):
        print("my_profile_information_view 실행")
        # object_list = User.objects.all().order_by('-profile__skill_note_reputation');
        object_list = User.objects.filter(username=self.request.user)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)

        my_favorite = []
        ru = RecommandationUserAboutSkillNote.objects.filter(
            author_id=self.request.user)

        for x in ru:
            print("내가 추천한 user_id : ", x.user_id)
            my_favorite.append(x.user_id)

        my_favorite_user_list = User.objects.filter(
            id__in=my_favorite).order_by('-profile__skill_note_reputation')
        print("my_favorite_user_list : ", my_favorite_user_list)

        context['my_favorite_user_list'] = my_favorite_user_list

        return context


class member_list_view(ListView):
    paginate_by = 20

    def get_template_names(self):
        if self.request.is_ajax():
            print("user list ajax 요청 확인")
            return ['wm/_user_list_for_memo.html']
        return ['wm/user_list_for_memo.html']

    def get_queryset(self):
        print("실행 확인 겟 쿼리셋")
        query = self.request.GET.get('q')
        print("query : ", query)

        if query != None:
            object_list = User.objects.all().filter(Q(username__contains=query))
            return object_list
        else:
            object_list = User.objects.all().order_by('-profile__skill_note_reputation')
            print("result : ", object_list)
            return object_list


member_list = member_list_view.as_view()


def logout(request):
    messages.success(request, '로그아웃되었습니다.')
    return logout_then_login(request)


def signup(request):
    print('회원 가입 뷰 실행 22')
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():    # 입력한 값이 있을 경우 True를 반환
            user = form.save()

            auth_login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
            redirect_url = request.GET.get("next", settings.LOGIN_REDIRECT_URL)

            return redirect(redirect_url)

    else:   # 입력한 값이 없을 경우
        form = SignupForm()
    return render(request, 'accounts2/signup_form.html', {
        'form': form,
    })


# Create your views here.
def profile(request):
    return render(request, 'accounts2/profile.html')
