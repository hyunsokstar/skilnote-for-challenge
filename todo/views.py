from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .forms import TodoForm, TodoAdminForm
from django.db.models import F

from django.db.models import Q

from . forms import CommentForm, CommentForm_TextArea

from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Todo, CommentForTodo, Category, TodoType, TeamInfo, TeamMember, Classification
from django.contrib.auth.models import User
from accounts2.models import Profile
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.urls import reverse

from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

from django.utils import timezone


# 1122 for todo

# 할일 미완료 목록 리스트 출력
class TodoList(LoginRequiredMixin,ListView):
    model = Todo
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Todo.objects.all().order_by('-created')
        else:
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodoList, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['category_list'] = Category.objects.all()
        context['todos_without_category'] = Todo.objects.filter(category=None).count()

        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()

        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        return context

# 할 일 완료 목록
class TodoCompleteListByMe(LoginRequiredMixin,ListView):
    model = Todo
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            # list_count = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False) )
            list_count = Todo.objects.filter(Q(author=self.request.user) & Q(completion="complete") )
            print("list_count  ", list_count)
            # qs = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False))
            qs = Todo.objects.filter(Q(author=self.request.user) & Q(completion="complete"))
            return qs

    def get_template_names(self):
        print("todo list complete 호출")
        return ['todo/todo_list_complete.html']

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # 미완료이면서 카테고리가 없는것
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()
        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()
        return context



def pass_task_to_selected_user(request):
    todo_arr = request.POST.getlist('todo_arr[]')
    selected_user = request.POST['selected_user']

    print('업무를 이전받을 id : ',selected_user)
    print('업데이트할 row  : ',todo_arr)

    author_for_update = User.objects.get(username=selected_user)
    Todo.objects.filter(Q(pk__in=todo_arr)).update(author = author_for_update)

    return JsonResponse({
        'message': selected_user+'에게 업무 이관 성공',
    })

def team_todo_list_by_check_user(request, team_name):
    print("team_name 22 : ", team_name)

    teamId = TeamInfo.objects.get(team_name = team_name).id
    team_leader_name = TeamInfo.objects.get(team_name = team_name).leader.username

    print("team_leader_name 22 : ", team_leader_name)

    team_member = TeamMember.objects.filter(team=teamId)
    classification_list = Classification.objects.all()
    team_name= team_name

    user_arr = request.POST.getlist('user_arr[]')
    print('user_arr : ', user_arr)

    team_todo_list = Todo.objects.filter(author__in=user_arr)

    return render(request, 'todo/team_todo_list_by_check_user.html', {
        "team_todo_list":team_todo_list,
    })

def team_todo_list(request, team_name):
    print("team_name : ", team_name)
    print("팀의 todo list를 출력 합니다.");

    teamId = TeamInfo.objects.get(team_name = team_name).id
    team_leader_name = TeamInfo.objects.get(team_name = team_name).leader.username

    # print("team_leader_name : ", team_leader_name)

    team_member = TeamMember.objects.filter(team=teamId)
    classification_list = Classification.objects.all()
    team_name= team_name

    member_array = []
    for member in team_member:
        # print(member.member.id) # nomad_coder, terecal
        member_array.append(member.member)

    team_todo_list = Todo.objects.filter(author__in=member_array)

    # print('team_todo_list : ' , team_todo_list)
    # print('team_member : ' , team_member)

    return render(request, 'todo/team_todo_list.html', {
        "team_todo_list":team_todo_list,
        "team_member_list":team_member,
        "classification_list":classification_list,
        "team_name":team_name,
        "team_leader_name": team_leader_name
    })


# 확인 미완료 목록 개수
def add_todo_for_team_by_ajax(request):

    title = request.POST['title']
    leader_name = request.POST['team_leader_name']
    member_name = request.POST['select_for_team_member']
    dead_line_option = request.POST['dead_line_option']
    classification = request.POST['select_for_classification']

    print("leader_name : ", leader_name)
    print("classification  : ", classification)

    classification_obj = Classification.objects.get(name=classification)

    print("leader_name : " , leader_name),
    print("member_name : ", member_name)

    author = User.objects.get(username=member_name)
    director = User.objects.get(username=leader_name)

    dead_line=""

    if dead_line_option == "1h":
        print ("1h")
        dead_line = datetime.now() + timedelta(hours=1)
    elif (dead_line_option == "4h"):
        print ("4h")
        dead_line = datetime.now() + timedelta(hours=4)

    elif (dead_line_option == "8h"):
        print ("8h")
        dead_line = datetime.now() + timedelta(hours=8)

    elif (dead_line_option == "1d"):
        print ("1d")
        dead_line = datetime.now() + timedelta(hours=24)

    elif (dead_line_option == "1w"):
        print ("1w")
        dead_line = datetime.now() + timedelta(days=7)

    todo = Todo.objects.create(title=title, author=author, director = director, dead_line = dead_line, classification = classification_obj)

    print("todo(입력 결과) : " , todo)

    uncompletecount = Todo.objects.filter(author=author, elapsed_time__isnull=True).count()
    print("uncompletecount (current): " , uncompletecount)

    user_update = Profile.objects.filter(user=author).update(uncompletecount = uncompletecount)

    # user_update = Profile.objects.filter(user=author).update(uncompletecount = F('uncompletecount')+1)

    return HttpResponse(redirect('/todo/'))

    # return JsonResponse({
    #     "message":"입력 성공"
    #     # 'todoId' : todo.id,
    #     # 'classification':todo.classification.name,
    #     # 'director':todo.director,
    #     # 'title':todo.title,
    #     # 'remaining_time':todo.remaining_time,
    #     # 'dead_line':todo.dead_line,
    # })

def add_todo_by_ajax_by_teamleader(request):

    title = request.POST['title']
    leader_name = request.POST['team_leader_name']
    member_name = request.POST['team_member_name']
    dead_line_option = request.POST['dead_line_option']
    classification = request.POST['classification']

    print("classification  : ", classification)

    classification_obj = Classification.objects.get(name=classification)

    print("leader_name : " , leader_name),
    print("member_name : ", member_name)

    author = User.objects.get(username=member_name)
    director = User.objects.get(username=leader_name)

    dead_line=""

    if dead_line_option == "1h":
        print ("1h")
        dead_line = datetime.now() + timedelta(hours=1)
    elif (dead_line_option == "4h"):
        print ("4h")
        dead_line = datetime.now() + timedelta(hours=4)

    elif (dead_line_option == "8h"):
        print ("8h")
        dead_line = datetime.now() + timedelta(hours=8)

    elif (dead_line_option == "1d"):
        print ("1d")
        dead_line = datetime.now() + timedelta(hours=24)

    elif (dead_line_option == "1w"):
        print ("1w")
        dead_line = datetime.now() + timedelta(days=7)

    todo = Todo.objects.create(title=title, author=author, director = director, dead_line = dead_line, classification = classification_obj)

    print("todo(입력 결과) : " , todo)



    uncompletecount = Todo.objects.filter(author=author, elapsed_time__isnull=True).count()
    print("uncompletecount (current): " , uncompletecount)

    user_update = Profile.objects.filter(user=author).update(uncompletecount = uncompletecount)

    return HttpResponse(redirect('/todo/'))

    # return JsonResponse({
    #     "message":"입력 성공"
    #     # 'todoId' : todo.id,
    #     # 'classification':todo.classification.name,
    #     # 'director':todo.director,
    #     # 'title':todo.title,
    #     # 'remaining_time':todo.remaining_time,
    #     # 'dead_line':todo.dead_line,
    # })


# uncomplte count +1 수정 확인
def add_todo_by_ajax(request):

    title = request.POST['title']
    dead_line_option = request.POST['dead_line_option']

    dead_line=""

    if dead_line_option == "1h":
        print ("1h")
        dead_line = datetime.now() + timedelta(hours=1)
    elif (dead_line_option == "4h"):
        print ("4h")
        dead_line = datetime.now() + timedelta(hours=4)

    elif (dead_line_option == "8h"):
        print ("8h")
        dead_line = datetime.now() + timedelta(hours=8)

    elif (dead_line_option == "1d"):
        print ("1d")
        dead_line = datetime.now() + timedelta(hours=24)

    elif (dead_line_option == "1w"):
        print ("1w")
        dead_line = datetime.now() + timedelta(days=7)

    todo = Todo.objects.create(title=title, author=request.user, director = request.user, dead_line = dead_line)

    print("todo(입력 결과) : " , todo)

    uncompletecount = Todo.objects.filter(author=request.user, elapsed_time__isnull=True).count()
    print("uncompletecount (current): " , uncompletecount)

    user_update = Profile.objects.filter(user=request.user.id).update(uncompletecount = uncompletecount)


    return HttpResponse(redirect('/todo/'))

    # return JsonResponse({
    #     "message":"입력 성공"
    #     # 'todoId' : todo.id,
    #     # 'classification':todo.classification.name,
    #     # 'director':todo.director,
    #     # 'title':todo.title,
    #     # 'remaining_time':todo.remaining_time,
    #     # 'dead_line':todo.dead_line,
    # })

def delete_team_memeber_info_by_memberId(request):
    print("팀 멤버 정보 삭제 by ajaz")
    if request.method == "POST" and request.is_ajax():
        team_memeber_id = request.POST['team_memeber_id']
        team_name = request.POST['team_name']
        team_member_name = request.POST['team_member_name']

        team_id = TeamInfo.objects.get(team_name = team_name).id



        TeamInfo.objects.filter(id=team_id).update(member_count = F('member_count')-1)


        print("team_memeber_id : ", team_memeber_id)
        print("team_name : ", team_name)
        print("team_member_name : ", team_member_name)

        dr = TeamMember.objects.filter(Q(id=team_memeber_id)).delete()
        messages.success(request, '{}팀에서 {} 회원이 탈퇴하셨습니다./'.format(team_name, team_member_name))


        return JsonResponse({
            'message': team_name+'팀에서 '+ team_name + '회원이 탈퇴 하였습니다.',
            'team_id': team_id
        })

def delete_team_member(request):
    print("팀 멤버 정보 삭제 22")
    if request.method == "POST" and request.is_ajax():
        option = ""
        team_memeber_id = request.POST['team_memeber_id']
        member = request.POST['member']
        team_id = request.POST['team_id']

        print("team_memeber_id : ", team_memeber_id)
        print("member : ", member)
        print("team_id : ", team_id)

        dr = TeamMember.objects.filter(Q(id=team_memeber_id)).delete()

        return JsonResponse({
            'message': '멤버 탈퇴 성공 : '+ member,
        })

def withdrawl_team(request):
    print("team_register view 실행")
    if request.method == "POST" and request.is_ajax():
        team_id = request.POST['team_id']
        user_id = request.POST['user_id']

        my_regi_count = TeamMember.objects.filter(Q(member=request.user)).count() # 회원 가입 여부 조사
        team_leader_ox = TeamInfo.objects.filter(Q(leader=request.user)).count()  # 팀장 여부 조사

        teaminfo_obj = TeamInfo.objects.get(id=team_id) # 팀 객체 생성
        team_name = teaminfo_obj.team_name # 팀 이름 얻어오기

        if team_leader_ox >=1:
            message= team_name , "팀의 팀장이므로 팀과 회원 정보 모두 삭제 합니다."
            ti = TeamInfo.objects.filter(Q(id=team_id)).delete()
            ti = TeamMember.objects.filter(Q(member=request.user)).delete()

        else:
            print("단순 멤버이므로 회원 탈퇴 하겠습니다")
            ti = TeamMember.objects.filter(Q(member=request.user)).delete()
            print("회원 탈퇴 성공 !!!!!!!!!!!!!!! ")

        team_member_count = TeamMember.objects.filter(team=team_id).count()
        print("이제", team_name, "의 회원 숫자는 ", team_member_count , '명이며 이를 TeamInfo 테이블에 업데이트 하겠습니다.')
        TeamInfo.objects.filter(id=team_id).update(member_count = team_member_count)
        print("가입한 회원 숫자 TeamInfo 테이블에 업데이트 성공 ################# ")
        message = team_name , "팀 탈퇴 성공. 회원수 : ", team_member_count

        return JsonResponse({
            'message': message,
        })


def team_register(request):
    print("team_register view 실행")
    if request.method == "POST" and request.is_ajax():
        option = ""
        team_id = request.POST['team_id']
        user_id = request.POST['user_id']

        my_regi_count = TeamMember.objects.filter(Q(member=request.user)).count() # 회원 가입 여부 조사
        team_leader_ox = TeamInfo.objects.filter(Q(leader=request.user)).count()  # 팀장 여부 조사

        teaminfo_obj = TeamInfo.objects.get(id=team_id) # 팀 객체 생성
        team_name = teaminfo_obj.team_name # 팀 이름 얻어오기

        if team_leader_ox >=1:
            message= team_name , "팀의 팀장이기 때문에 다른팀에 가입할수 없습니다."
            return JsonResponse({
                'message': message
            })
        elif my_regi_count >=1:
            message = team_name , "팀에 이미 가입했습니다."
            return JsonResponse({
                'message': message
            })
        else:
            print("팀에 가입하지도 않았고 팀장도 아니기 때문에 ", team_name , "팀에 가입합니다.")
            ti, is_created = TeamMember.objects.get_or_create(
                team=teaminfo_obj,
                member=request.user
            )
            print("회원 가입 성공 !!!!!!!!!!!!!!! ")
            team_member_count = TeamMember.objects.filter(team=team_id).count()
            print("이제", team_name, "의 회원 숫자는 ", team_member_count , '명이며 이를 TeamInfo 테이블에 업데이트 하겠습니다.')
            TeamInfo.objects.filter(id=team_id).update(member_count = team_member_count)
            print("가입한 회원 숫자 TeamInfo 테이블에 업데이트 성공 ################# ")
            message = team_name , "팀 가입 성공. 회원수 : ", team_member_count

            return JsonResponse({
                'message': message,
            })


class UncompleteTodoListByUserId_admin(ListView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        print("user_id : ", user_id)
        user = User.objects.get(username=user_id)
        print("user : " , user.id)

        return Todo.objects.filter(Q(elapsed_time__isnull=True) & Q(author=user.id)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.get(username=user_id)
        print("user_id : ", user_id)
        print("user : ", user)

        classification_list = Classification.objects.all()

        # 유저 이름
        context['user_name'] = self.kwargs['user_id']

        # 카테고리 정보
        context['category_list'] = Category.objects.all()
        # 미완료 개수
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=user) & Q(elapsed_time__isnull=True)).count()
        # 완료 개수
        context['todo_count_complete'] = Todo.objects.filter(Q(author=user) & Q(elapsed_time__isnull=False)).count()

        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        context['current_state_for_list'] = "미완료"

        context['team_leader_name']=self.kwargs['team_leader_name']
        context['classification_list'] = classification_list

        return context

    def get_template_names(self):
            return ['todo/uncomplete_todo_list_for_user_by_admin.html']

class CompleteTodoListByUserId_admin(ListView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(username=user_id)
        print("user : " , user.id)
        print("완료 목록 출력 ")

        return Todo.objects.filter(Q(elapsed_time__isnull=False) & Q(author=user.id)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        user_id = self.kwargs['user_id']
        user = User.objects.get(username=user_id)
        context = super(type(self), self).get_context_data(**kwargs)

        # 유저 이름
        context['user_name'] = self.kwargs['user_id']

        # 카테고리 정보
        context['category_list'] = Category.objects.all()

        # 미완료 개수
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=user) & Q(elapsed_time__isnull=True)).count()
        # 완료 개수
        context['todo_count_complete'] = Todo.objects.filter(Q(author=user) & Q(elapsed_time__isnull=False)).count()


        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()
        context['current_state_for_list'] = "완료"
        context['team_leader_name'] = self.kwargs['team_leader_name']
        return context

    def get_template_names(self):
            return ['todo/complete_todo_list_for_user_by_admin.html']


def delete_team_info(request,team_id):
    user = request.user
    if request.method == "GET" and request.is_ajax():
        # team_info_id = request.POST['team_info_id']
        team_info_id = team_id
        ti = TeamInfo.objects.filter(Q(id=team_info_id)).delete()
        print('delete_team_info 성공');
        return JsonResponse({
            'message': '댓글 삭제 성공',
        })
    else:
        return JsonResponse({
            'message': '댓글 삭제 실패',
        })

# def register_for_team(request, team_id):
#     print("team_id : " , team_id)
#
#     team_name = TeamInfo.objects.get(id = team_id).team_name
#
#     Profile.objects.filter(Q(user=request.user.id)).update(team = team_id)
#     TeamInfo.objects.filter(id=team_id).update(member_count = F('member_count')+1)
#     member_count=TeamInfo.objects.get(id=team_id).member_count
#
#     messages.success(request, '{} 회원이 {}팀에 가입했습니다./'.format(request.user, team_name))
#     messages.success(request, '{}팀의 회원수가 {}명이 되었습니다./'.format(team_name, member_count))
#
#     return HttpResponseRedirect(reverse('todo:team_member_list' , kwargs={'team_info_id': team_id}))
#
# def unregister_for_team(request, team_id):
#     print("team_id : " , team_id)
#     team_name = TeamInfo.objects.get(id = team_id).team_name
#
#     Profile.objects.filter(Q(user=request.user.id)).update(team = "")
#     TeamInfo.objects.filter(id=team_id).update(member_count = F('member_count')-1)
#     member_count=TeamInfo.objects.get(id=team_id).member_count
#
#     messages.success(request, '{} 회원이 {}팀에서 탈퇴했습니다./'.format(request.user,team_name))
#     messages.success(request, '{}팀의 회원수가 {}명이 되었습니다./'.format(team_name, member_count))
#
#     return HttpResponseRedirect(reverse('todo:team_member_list' , kwargs={'team_info_id': team_id}))

class team_member_list_view(LoginRequiredMixin,ListView):
    model = TeamMember
    paginate_by = 40

    def get_queryset(self):
        team_info_id = self.kwargs['team_info_id']
        print("team_info_id : " , team_info_id)
        return TeamMember.objects.filter(team=team_info_id)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        team_info_id = self.kwargs['team_info_id']
        ti = TeamInfo.objects.get(id=team_info_id)

        print("ti : ", ti)
        context["team_id"] = ti.id
        context['team_name'] = ti.team_name
        context['team_leader_name'] = ti.leader.username
        context['team_member_count']= ti.member_count
        # context['my_team_name'] = request.user.profile.team

        return context

    def get_template_names(self):
        print("team member list page를 출력")
        return ['todo/teammember_list.html']


class TeamInfoCreateView(CreateView):
    model = TeamInfo
    fields = ['team_name','team_description']
    success_url = reverse_lazy('todo:TeamInfoListView')

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행")
        ti = form.save(commit=False)
        ti.leader = self.request.user

        return super().form_valid(form)


class TeamInfoListView(LoginRequiredMixin,ListView):
    model = TeamInfo
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        myteam=TeamMember.objects.filter(member=self.request.user)

        if myteam.exists():
            myteam=TeamMember.objects.get(member=self.request.user).team
            print("myteam : ", myteam)

        context['myteam']= myteam

        return context




def isnert_todo_popup_by_admin(request,user_name):
    print("isnert_todo_popup_by_admin 호출")
    print("user_name : ", user_name)

    return render(request, 'todo/insert_todo_by_admin.html', {
        'foo': 'bar',
    })

class TodoListByAdmin(LoginRequiredMixin,ListView):
    model = Todo
    paginate_by = 20

    def get_queryset(self):
        return Todo.objects.filter(Q(elapsed_time__isnull=False) & Q(author = self.request.user)).order_by('-created')

    def get_template_names(self):
        print("admin page를 출력")
        return ['todo/todo_list_by_admin.html']

class CompleteTodoListByUserId(ListView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        print("user_id : ", user_id)
        user = User.objects.get(username=user_id)
        print("user : " , user.id)

        return Todo.objects.filter(Q(elapsed_time__isnull=False) & Q(author=user.id)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        # 카테고리 정보
        context['category_list'] = Category.objects.all()
        # 미완료 개수
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료 개수
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료 개수
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()

        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        return context

    def get_template_names(self):
            return ['todo/todo_list_total.html']

class UncompleteTodoListByUserId(ListView):
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        print("user_id : ", user_id)
        user = User.objects.get(username=user_id)
        print("user : " , user.id)

        return Todo.objects.filter(Q(elapsed_time__isnull=True) & Q(author=user.id)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        # 카테고리 정보
        context['category_list'] = Category.objects.all()
        # 미완료 개수
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료 개수
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료 개수
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()

        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        return context

    def get_template_names(self):
            return ['todo/todo_list_total.html']

@login_required
def todo_delete_ajax(request):
    todo_ids = request.POST.getlist('todo_arr[]')
    if todo_ids:
        Todo.objects.filter(pk__in=todo_ids, author=request.user).delete()

    return redirect('/todo')

def todo_status_list(request):
    print("todo_status_list 실행")

    users = User.objects.all()

    return render(request, 'todo/todo_status_list.html', {
        'users': users,
    })

def FinisherList(request, id):
    fl = Finisher.objects.filter(Q(bestlec=id))
    print("fl : ", fl)
    print('해당 id에 대한 FinisherList')
    return render(request, 'bestlec/finisher_list.html', {
        'fl': fl,
        'fn_id':id
    })

def todo_new_admin(request,user_name,leader_name):
    if request.user.is_superuser:
        print("관리자는 입력할 수 있습니다.")
    else:
        messages.success(request,'관리자가 아니면 입력할 수 없습니다.')
        return redirect('/todo/category/_none')

    user = User.objects.get(username=user_name)
    print('user name ', user_name)

    if request.method=="POST":
        form = TodoAdminForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = user
            todo.director = request.user

            todo.save()

            uncompletecount = Todo.objects.filter(author=user, elapsed_time__isnull=True).count()
            print("uncompletecount (current): " , uncompletecount)

            user_update = Profile.objects.filter(user=user.id).update(uncompletecount = uncompletecount)

            return redirect('/todo/todolist/uncomplete/admin/'+user_name+'/'+leader_name)
            # http://127.0.0.1:8000/todo/todolist/uncomplete/admin/terecal/terecal
    else:
        form = TodoAdminForm()
    return render(request, 'todo/insert_todo_form_by_admin.html',{
        'user_name': user.username,
        'form':form
    })

class CommentUpdate(UpdateView):
    model = CommentForTodo
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment


class TodoListByComplete_total(LoginRequiredMixin,ListView):
    model = Todo
    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(elapsed_time__isnull=False))

    def get_template_names(self):
        return ['todo/todo_list_complete_total.html']
        # 카테고리 목록
    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # 미완료이면서 카테고리가 없는것
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()
        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()
        return context

def delete_comment_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = CommentForTodo.objects.filter(Q(id=id)).delete()
        print('delete 성공');
        return JsonResponse({
            'message': '댓글 삭제 성공',
        })
    else:
        return redirect('/myshortcut')


def update_comment_ajax_for_summernote(request,id):


    print("답변 수정 실행 view")

    user = request.user
    if request.method == "POST" and request.is_ajax():
        title = request.POST['title']
        file_name = request.POST['file_name']
        text = request.POST['text']

        print('id : ', id)
        print("title(view) : ", title)
        print("file_name : ", file_name)
        print("text : ", text)
        todo = CommentForTodo.objects.filter(Q(id=id)).update(title = title, file_name = file_name , text = text)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def update_comment_ajax_for_textarea(request,id):

    print("답변 수정 실행 view")

    user = request.user
    if request.method == "POST" and request.is_ajax():
        text = request.POST['text']

        print('id : ', id)
        print("text : ", text)
        todo = CommentForTodo.objects.filter(Q(id=id)).update(text = text)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def todo_help(request, id):
    todo = get_object_or_404(Todo, id=id)
    now_diff = todo.now_diff
    print("now_diff : ", now_diff)
    Todo.objects.filter(Q(id=id)).update(category = 2)
    print("핼프를 요청 id:",id)
    return redirect('/todo')

def todo_help_cancle(request, id):
    print("todo_help_cancle")
    todo = get_object_or_404(Todo, id=id)
    now_diff = todo.now_diff
    print("now_diff : ", now_diff)
    Todo.objects.filter(Q(id=id)).update(category = "")
    print("핼프를 요청 id:",id)
    return redirect('/todo')


class TodoUnCompleteListByMe(LoginRequiredMixin,ListView):
    model = Todo
    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True))

    def get_template_names(self):
        return ['todo/todo_list.html']
        # 카테고리 목록
    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        # 미완료이면서 카테고리가 없는것
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()
        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()
        return context


class TodoListByCategory(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        print('slug : ', slug)

        if slug == '_none':
            category = None
            return Todo.objects.filter(Q(elapsed_time__isnull=True)).order_by('-created')
        else:
            # 카테고리가 없는 경우 전체 목록
            category = Category.objects.get(slug=slug)
            return Todo.objects.filter(Q(elapsed_time__isnull=True) & Q(category=category)).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        print('self.request.user : ', self.request.user)
        context = super(type(self), self).get_context_data(**kwargs)
        # 미완료이면서 카테고리가 있는것
        context['category_list'] = Category.objects.all()
        # 미완료이면서 카테고리가 없는것
        context['todos_without_category'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 미완료
        context['todo_count_uncomplete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=True)).count()
        # 완료
        context['todo_count_complete'] = Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time__isnull=False)).count()

        context['comment_form'] = CommentForm()
        context['total_todo_count_uncomplete'] = Todo.objects.filter(Q(elapsed_time__isnull=True)).count()
        context['total_todo_count_complete'] = Todo.objects.filter(Q(elapsed_time__isnull=False)).count()

        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category
        return context

    def get_template_names(self):
        return ['todo/todo_list_total.html']


def delete_comment(request, pk):
    comment = CommentForTodo.objects.get(pk=pk)
    todo = comment.todo

    if request.user == comment.author:
        comment.delete()
        return redirect('/todo')
    else:
        return redirect('/todo/')

class CommentUpdate(UpdateView):
    model = CommentForTodo
    form_class = CommentForm

    def get_object(self, queryset=None):
        comment = super(CommentUpdate, self).get_object()
        if comment.author != self.request.user:
            raise PermissionError('Comment 수정 권한이 없습니다.')
        return comment

def new_comment_by_summer_note(request, pk):
    print("댓글 입력 함수 기반뷰 실행")
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        ty = TodoType.objects.get(type_name="summer_note")


        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.todo = todo
            comment.author = request.user
            if comment.author == request.user:
                comment.user_type = 1
            else:
                comment.user_type = 2
            comment.type= ty
            comment.save()

            if request.is_ajax():
                return JsonResponse({
                    'author': comment.author.username,
                    'title': comment.title,
                    'file_name': comment.file_name,
                    'text':comment.text,
                    'created_at':comment.created_at,
                    'edit_id':comment.id,
                    'delete_id':comment.id
                })
            return redirect(comment.get_absolute_url())

        else:
            return JsonResponse(comment_form.errors,is_success=False)
    else:
        return redirect('/todo/')

def new_comment_text_area(request, pk):
    print("댓글 입력 함수 기반뷰 실행")
    todo = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        ty = TodoType.objects.get(type_name="text_area")

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.todo = todo
            comment.author = request.user

            if comment.author == request.user:
                comment.user_type = 1
            else:
                comment.user_type = 2

            comment.type= ty
            comment.save()

            if request.is_ajax():
                return JsonResponse({
                    'author': comment.author.username,
                    'title': comment.title,
                    'file_name': comment.file_name,
                    'text':comment.text,
                    'created_at':comment.created_at,
                    'edit_id':pk,
                    'delete_id':pk
                })
            return redirect(comment.get_absolute_url())

        else:
            print("에러 발생")
            # return JsonResponse(comment_form.errors,is_success=False)
    else:
        return redirect('/todo/')

# todo 상세 보기
class todoDetail(DetailView):
    model = Todo
    def get_template_names(self):
        if self.request.is_ajax():
            return ['todo/_todo_detail.html']
        return ['todo/todo_detail.html']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(todoDetail, self).get_context_data(**kwargs)
        context['comments_list_my'] = CommentForTodo.objects.filter(todo=self.object.pk, author=self.object.author)
        context['comments_list_commenter'] = CommentForTodo.objects.filter(Q(todo=self.object.pk) & ~Q(author=self.request.user))
        context['detail_id'] = self.object.pk
        context['comment_form'] = CommentForm()
        context['comment_form_text_area'] = CommentForm_TextArea()

        return context

class TodoList_by_card(ListView):
    model = Todo
    paginate_by = 2

    def get_template_names(self):
        return ['todo/todo_list_search.html']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all().order_by('-created')
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time !=None)).order_by('-created')

class TodoSearch(ListView):
    def get_template_names(self):
        return ['todo/todo_list_search.html']
    # Q(elapsed_time = None)
    def get_queryset(self):
        print("실행 확인")
        q = self.kwargs['q']
        print("검색어 : ", q)
        # object_list = Todo.objects.filter(Q(title__contains=q) & Q(elapsed_time__isnull=False)).order_by('-created')
        object_list = Todo.objects.filter(Q(title__icontains=q)).order_by('-created')
        print("result : ", object_list)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TodoSearch, self).get_context_data(**kwargs)
        context['search_word'] = self.kwargs['q']
        return context

def todo_complete(request, id):
    if request.user.is_authenticated:
        todo = get_object_or_404(Todo, id=id)
        now_diff = todo.now_diff()
        print("now_diff : ", now_diff)
        Todo.objects.filter(Q(id=id)).update(elapsed_time = now_diff,category = None, completion = "complete" , updated = timezone.now())

        Profile.objects.filter(Q(user=request.user.id)).update(completecount = F('completecount')+1, uncompletecount = F('uncompletecount')-1)
        messages.success(request,'할일 : {} 를 완료 처리 하였습니다 ~!'.format(todo))

        print("todo 완료 업데이트 완료 ")

        return redirect('/todo')
    else:
        return redirect('accouts/login')

# class todo_delete_view(DeleteView):
#     model = Todo
#     success_url = reverse_lazy('todo:todo_list')
#     # success_message = "delete was complted"
# todo_delete = todo_delete_view.as_view()

def todo_delete(request, pk):
    # template = 'todo/todo_confirm_delete.html'
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()

    if todo.completion == "uncomplete":
        uncompletecount = Todo.objects.filter(author=request.user, elapsed_time__isnull=True).count()
        print("uncompletecount (current): " , uncompletecount)

        Profile.objects.filter(Q(user=request.user.id)).update(uncompletecount = uncompletecount)
    else:
        uncompletecount = Todo.objects.filter(author=request.user, elapsed_time__isnull=True).count()
        print("uncompletecount (current): " , uncompletecount)
        Profile.objects.filter(Q(user=request.user.id)).update(completecount = uncompletecount)

    print("todo" , todo , '를 삭제')
    return redirect('todo:todo_list')

    # AttributeError: '__proxy__' object has no attribute 'get'

def todo_new(request):
    if request.method=="POST":
        form = TodoForm(request.POST, request.FILES)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
            print('todo를 저장했습니다')

            uncompletecount = Todo.objects.filter(author=request.user, elapsed_time__isnull=True).count()
            print("uncompletecount (current): " , uncompletecount)

            Profile.objects.filter(Q(user=request.user.id)).update(uncompletecount = uncompletecount)
            print('uncompletecount를 +1')

            return redirect('/todo/')

    else:
        form = TodoForm()
    return render(request, 'todo/post_form.html',{
        'form':form
    })

def todo_edit(request, id):
    todo = get_object_or_404(Todo, id=id)

    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            post = form.save()
            return redirect('/todo')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/edit_form.html', {
        'form': form,
    })

class TodoListByComplete_by_card(ListView):
    model = Todo
    def get_queryset(self):
        # print(Todo.objects.all().count())
        # print(Todo.objects.filter(Q(author=self.request.user)).count())
        # print(Todo.objects.filter(Q(author=self.request.user) & Q(elapsed_time="")).count())
        if self.request.user.is_anonymous:
            print("익명 유저입니다")
            return Todo.objects.all()
        else:
            print("user : ", self.request.user)
            return Todo.objects.filter(Q(author=self.request.user) & ~Q(elapsed_time=""))

    def get_template_names(self):
        return ['todo/todo_list_complete_card.html']
