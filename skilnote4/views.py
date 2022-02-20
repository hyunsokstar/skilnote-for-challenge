from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.views.generic import ListView, DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .forms import MyShortCutForm_input, SkilNoteForm , MyShortCutForm_image, MyShortCutForm_summer_note2
from accounts2.models import Profile
from .models import MyShortCutForSkilNote4, TypeForSkilNote4, CategoryForSkilNote4, CategoryNickForSkilNote4, CommentForShortCutForSkilNote4 , TempMyShortCutForSkilNote4, TempMyShortCutForBackEndForSkilNote4, CommentForShortCutForSkilNote4, RecommandationUserAboutSkilNote4, CommentForPageForSkilNote4, GuestBookForSkilNote4
from skilblog.models import SkilBlogTitle, SkilBlogContent
from django.http import HttpResponseRedirect
from datetime import datetime , timedelta
from django.utils import timezone
from django.urls import reverse_lazy
from . forms import CommentForm
from django.utils.datastructures import MultiValueDictKeyError


# 1122
def manualPage(request):
    return render(request, 'skilnote4/manual.html', {
	})

def intro_for_skilnote(request):
    return render(request, 'skilnote4/intro_page.html', {
	})


# 입력 모드
class MyShortCutListView2(LoginRequiredMixin,ListView):
    model = MyShortCutForSkilNote4

    def get_queryset(self):
        user = self.request.user
        print("self.request.user : ", self.request.user)
        selected_category_id = user.profile.selected_category_id
        qs = MyShortCutForSkilNote4.objects.filter(Q(author=user, category = selected_category_id)).order_by('created')
        return qs


    def get_template_names(self):
        if self.request.is_ajax():
            print("user list ajax 요청 확인")
            return ['skilnote4/myshortcut_list2.html']
        return ['skilnote4/myshortcut_list2.html']

        print("user : ", user)

        if self.request.user.is_anonymous:
            return MyShortCutForSkilNote4.objects.filter(author=self.request.user).order_by('created')
        else:
            selected_category_id = self.request.user.profile.selected_category_id
            return MyShortCutForSkilNote4.objects.filter(Q(author=user, category = selected_category_id)).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
        # 카테고리 각각의 정보를 저장하는 테이블 없으면 만든다.
        cn = CategoryNickForSkilNote4.objects.get_or_create(
            author=self.request.user,
        )
        category_id = self.request.user.profile.selected_category_id
        print("category_id :::::::::::::::::::::::::::::::::::" , category_id)
        context = super(MyShortCutListView2, self).get_context_data(**kwargs)
        # 스킬 노트 페이지 역할을 하는 카테고리 목록을 가져 온다.
        context['category_list'] = CategoryForSkilNote4.objects.all()
        # 카테고리 테이블은 id = 1 => ca1 id = 2 => ca2 이런식이므로 id로 ca1, ca2 객체를 생성 가능
        category = CategoryForSkilNote4.objects.get(id=category_id) # __str__ 설정으로 카테고리 객체 = 카테고리.name 이다
        context['category'] = category
        context['category_id'] = category_id
        # 카테고리 닉은 author = 현재 유저 이름이고 각각의 컬럼에 ca1, ca2, ca3, ca4 등의 카테고리 주제값이 들어있으므로 category.name로 검색해서 가져온다.
        context['category_nick'] = CategoryNickForSkilNote4.objects.values_list(category.name, flat=True).get(author=self.request.user)
        context['MyShortCutForm_summer_note2'] = MyShortCutForm_summer_note2

        return context


class MyShortcutListByCategory2(ListView):

    def get_template_names(self):
        if self.request.is_ajax():
            print("user list ajax 요청 확인")
            return ['skilnote4/myshortcut_list2.html']
        return ['skilnote4/myshortcut_list2.html']


    def get_queryset(self):
        slug = self.kwargs['slug']
        category = CategoryForSkilNote4.objects.get(slug=slug)
        pf = Profile.objects.filter(Q(user=self.request.user)).update(selected_category_id = category.id)
        print('category id update 성공')


        user = User.objects.get(Q(username = self.request.user))

        print('user : ' , user)

        return MyShortCutForSkilNote4.objects.filter(category=category, author=user).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
        user = User.objects.get(Q(username = self.request.user))

        context = super(type(self), self).get_context_data(**kwargs)
        context['posts_without_category'] = MyShortCutForSkilNote4.objects.filter(category=None,author=user).count()
        context['category_list'] = CategoryForSkilNote4.objects.all()
        context['posts_without_category'] = MyShortCutForSkilNote4.objects.filter(category=None, author=self.request.user).count()
        context['category_id'] = self.request.user.profile.selected_category_id
        context['MyShortCutForm_summer_note2'] = MyShortCutForm_summer_note2


        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = CategoryForSkilNote4.objects.get(slug=slug)
            context['category'] = category
            context['category_nick'] = CategoryNickForSkilNote4.objects.values_list(slug, flat=True).get(author=user)

        return context


def guest_book_list(request,guest_book_owner):
    if request.method == 'GET':
        print("geust_book_list 실행")
        owner = User.objects.get(username=guest_book_owner)

        object_list = GuestBookForSkilNote4.objects.filter(owner_for_guest_book=owner).order_by('created_at');
        print("object_list : ", object_list)

        return render(request, 'skilnote4/guest_book_list.html', {
            "object_list" : object_list,
        })
    else:
        return HttpResponse("Request method is not a GET")

def insert_temp_skill_note_for_textarea(request):
    print("insert_temp_skill_note_for_textarea 실행")
    ty = TypeForSkilNote4.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']

    skilnote4 = TempMyShortCutForSkilNote4.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content2 = ""
    )

    print("skilnote4 : ", skilnote4)

    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content2':skilnote4.content2,
    })

def delete_guest_book_list(request,id):
    user = request.user

    if request.method == "POST" and request.is_ajax():
        gb = GuestBookForSkilNote4.objects.filter(Q(id=id)).delete()
        print('GuestBookForSkilNote4 delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'comment 삭제 성공 ',
        })
    else:
        return redirect('/skilnote4/myshorcut/')

def insert_for_guest_book(request):
    print("insert_for_guest_book 실행")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    user = request.POST['page_user']
    text = request.POST['text']

    guest_book = GuestBookForSkilNote4.objects.create(
        owner_for_guest_book = request.user,
        author = request.user,
        content = text,
    )

    print("guest_book : ", guest_book)

    return JsonResponse({
        'message' : 'guest_book row 추가 성공',
        'guest_book_id' : guest_book.id,
        'guest_book_author' : guest_book.author.username,
        'guest_book_content' : guest_book.content,
        'guest_book_created_at' : guest_book.created_at,
    })



# delete_comment_for_skilpage
def delete_comment_for_skilpage(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        comment = CommentForPageForSkilNote4.objects.filter(Q(id=id)).delete()
        print('TempMyShortCutForBackEndForSkilNote4 delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'comment 삭제 성공',
        })
    else:
        return redirect('/todo')

def new_comment_for_skilpage(request, user_name, category_id):
    # user_name = request.GET.get('user_name')
    # category_id = request.GET.get('category_id')
    print("user_name : ", user_name)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user_name = user_name
            comment.category_id = category_id
            comment.save()
            return redirect('/skilnote4/myshortcut/'+user_name+"/"+category_id)
    else:
        return redirect('/skilnote4/myshortcut/'+user_name+"/"+category_id)

class MyShortcutListByUser(ListView):
    model = MyShortCutForSkilNote4
    paginate_by = 20
    template_name = 'skilnote4/myshortcut_list_for_user.html'


    def get_queryset(self):
        user = self.kwargs['user']
        user = User.objects.get(username=user)


        category_id = self.kwargs['category_id']

        print("user : ", user)

        if self.request.user.is_anonymous:
            # return MyShortCutForSkilNote4.objects.filter(author=user).order_by('created')
            selected_category_id = category_id
            return MyShortCutForSkilNote4.objects.filter(Q(author=user, category = category_id)).order_by('created')
        else:
            selected_category_id = category_id
            return MyShortCutForSkilNote4.objects.filter(Q(author=user, category = category_id)).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
            user = self.kwargs['user']
            category_id = self.kwargs['category_id']
            user = User.objects.get(username=user)

            print("category_id : ", category_id)

            cn = CategoryNickForSkilNote4.objects.get_or_create(
                author=user,
            )

            context = super(MyShortcutListByUser, self).get_context_data(**kwargs)
            context['category_list'] = CategoryForSkilNote4.objects.all()

            # category = CategoryForSkilNote4.objects.get(id=user.profile.selected_category_id)
            category = CategoryForSkilNote4.objects.get(id=category_id)
            context['category'] = category
            context['category_num'] = category_id
            context['category_nick'] = CategoryNickForSkilNote4.objects.values_list(category.slug, flat=True).get(author=user)

            context['posts_without_category'] = MyShortCutForSkilNote4.objects.filter(category=None, author=user).count()
            context['page_user'] = user
            context['comment_list_for_page'] = CommentForPageForSkilNote4.objects.filter(user_name=user, category_id = category_id)
            context['star_count_for_user'] = RecommandationUserAboutSkilNote4.objects.filter(user=user.id).count
            context['comment_form'] = CommentForm()

            return context


def category_plus_1_for_current_user(request):
    # is this possible?
    # for x in range(i, 98)
    #     CategoryNickForSkilNote4.obejcts.filter(author=request.user).update("ca"+(x+1)=F('ca'+x))

    ca_num = request.POST['current_ca_num'] # 입력한 ca 번호
    print("ca_num : ", ca_num)
    print("ca_num type :",type(ca_num))

    # data2 = {'ca{}'.format(x+1): F('ca{}'.format(x)) for x in range(int(ca_num), 99)}
    data2 = {'ca{}'.format(x+1): F('ca{}'.format(x)) for x in range(int(ca_num), 120)}

    CategoryNickForSkilNote4.objects.filter(
        author=request.user
    ).update(**data2)

    # data1 = {'ca{}'.format(ca_num): "+1 실행 완료" }

    # CategoryNickForSkilNote4.objects.filter(
    #     author=request.user
    # ).update(**data1)

    skil_note = MyShortCutForSkilNote4.objects.filter(Q(author=request.user)).order_by("created")

    ca_delete=CategoryForSkilNote4.objects.get(name="ca120")
    MyShortCutForSkilNote4.objects.filter(Q(author=request.user) & Q(category=ca_delete)).delete()

    for sn in skil_note:
        # if(sn.category.id >= int(ca_num) and sn.category.id != 99):
        if(sn.category.id >= int(ca_num) and sn.category.id != 120):
            print("sn.category.id : ", sn.category.id)
            print("int(sn.category.id)+1 : ", int(sn.category.id)+1)
            ca = CategoryForSkilNote4.objects.get(id=int(sn.category.id)+1)
            MyShortCutForSkilNote4.objects.filter(id=sn.id).update(category=ca, created=F('created'))
        else:
            print("sn.category.id : ", sn.category.id)

    return JsonResponse({
        'message': "ca"+ca_num+"부터 ca120까지 +1 성공"
    })


def category_minus_1_for_current_user(request):
    # ca=CategoryForSkilNote4.objects.filter(id=category_num)
    ca_num = request.POST['current_ca_num'] # 입력한 ca 번호

    print("ca_num check : ", ca_num)
    print("ca_num type :",type(ca_num))

    data = {'ca{}'.format(x-1): F('ca{}'.format(x)) for x in range(120,int(ca_num)-1,-1)}
    CategoryNickForSkilNote4.objects.filter(
        author=request.user
    ).update(**data)

    skil_note = MyShortCutForSkilNote4.objects.filter(Q(author=request.user))

    if(int(ca_num)>1):
        ca_delete_num = int(ca_num)-1

    ca_delete=CategoryForSkilNote4.objects.get(id=ca_delete_num)
    MyShortCutForSkilNote4.objects.filter(Q(author=request.user) & Q(category=ca_delete)).delete()
    # MyShortCutForSkilNote4.obejcts.filter(Q(id=ca))

    for sn in skil_note:
        # print("sn.category.id : ", sn.category.id)
        if(sn.category.id >= int(ca_num) and sn.category.id != 1):
            # ca=CategoryForSkilNote4.objects.get(id=int(sn.category.id)+1)
            print("sn.category.id : ", sn.category.id)
            print("int(sn.category.id)-1 : ", int(sn.category.id)-1)
            ca = CategoryForSkilNote4.objects.get(id=int(sn.category.id)-1)
            MyShortCutForSkilNote4.objects.filter(id=sn.id).update(category=ca, image = F('image'))

    return JsonResponse({
        'message': "ca"+ca_num+"부터 ca120까지 -1 성공"
    })


def move_to_skil_blog(request):
    title = request.POST['title'] # 어떤 유저에 대해
    shortcut_ids = request.POST.getlist('shortcut_arr[]')

    sbt = SkilBlogTitle.objects.create(title=title, author=request.user)

    print("스킬 블로그 타이틀 id check ::::::::::::::::", sbt.id)
    print("스킬 블로그 타이틀 id check ::::::::::::::::", sbt.id)

    if shortcut_ids:
        skill_note_list = MyShortCutForSkilNote4.objects.filter(pk__in=shortcut_ids, author=request.user).order_by('created')
        print('skill_note_lists : ', skill_note_list)

    for p in skill_note_list:
        # print("p : ", p)
        profile = SkilBlogContent.objects.create(
            sbt = sbt,
			author = request.user,
			title = p.title,
            filename = p.filename,
			content1 = p.content1,
			content2 = p.content2,
			type_id = p.type_id,
            image = p.image
		)
    return JsonResponse({
        'message': "체크한 항목들을 스킬 블로그로 옮겼습니다."+title,
        'id':sbt.id
    })


def plus_recommand_for_skillnote_user(request):
    author_id = request.POST.get('author_id', False)
    my_id = request.POST.get('my_id', False)

    author =  get_object_or_404(User, pk=author_id)
    me =  get_object_or_404(User, pk=my_id)
    print("추천 받는 사람 : " , author)
    print("추천 하는 사람 : ", me)

    recommand_count = RecommandationUserAboutSkilNote4.objects.filter(Q(user=author) & Q(author_id=me)).count() # 내가 추천한거 있는지 확인
    print("recommand_count : ", recommand_count)

    if (recommand_count ==  0):
        rc = RecommandationUserAboutSkilNote4.objects.create(user=author , author_id=me) # 나의 추천 추가
        print('추천 ++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        recommand_count = RecommandationUserAboutSkilNote4.objects.filter(Q(user=author)).count() # 추천 받은 사람 점수 확인

        profile = Profile.objects.filter(Q(user=author_id)).update(skill_note_reputation = recommand_count) # 추천 대상자 프로필 점수 반영

        return JsonResponse({
            'message': "추천 +1",
            "option":"plus",
            "recommand_count":recommand_count
        })

    else:
        RecommandationUserAboutSkilNote4.objects.filter(Q(user=author) & Q(author_id=me)).delete() # 내가 추천한거 삭제

        recommand_count = RecommandationUserAboutSkilNote4.objects.filter(Q(user=author)).count() # 추천 받은 사람 점수 확인
        print('추천 ---------------------------------------------------')
        profile = Profile.objects.filter(Q(user=author_id)).update(skill_note_reputation = recommand_count)

        return JsonResponse({
            'message': "추천 -1 ",
            "option":"minus",
            "recommand_count":recommand_count
        })


def copy_to_me_from_user_id(request):

    author = request.POST['author']
    # 나의 노트 모두 지우기
    if( MyShortCutForSkilNote4.objects.filter(Q(author=request.user)).count() != 0):
        MyShortCutForSkilNote4.objects.filter(Q(author=request.user)).delete()
        CategoryNickForSkilNote4.objects.filter(Q(author=request.user)).delete()
        CommentForShortCutForSkilNote4.objects.filter(Q(author=request.user)).delete()

    user_id = User.objects.get(username=author).id
    print("user_id : " , user_id)

    skilnote4_list_for_copy = MyShortCutForSkilNote4.objects.filter(Q(author=user_id))
    print("skilnote4_list_for_copy : " , skilnote4_list_for_copy);
    MyShortCutForSkilNote4.objects.filter(Q(author=request.user)).delete()

    comment_skilnote4_list_for_copy = CommentForShortCutForSkilNote4.objects.filter(Q(author=user_id))


    for p in skilnote4_list_for_copy:
        myshortcut = MyShortCutForSkilNote4.objects.create(
            author = request.user,
            title = p.title,
            content1 = p.content1,
            content2 = p.content2,
            type_id = p.type_id,
            category = p.category,
            filename = p.filename,
            image=p.image,
            created = p.created,
        )
        # print("myshortcut : " , myshortcut.id)
        for comment in comment_skilnote4_list_for_copy:
            # print("comment.id : ", comment.id)
            # print("myshortcut.id : ", myshortcut.id )
            if comment.shortcut.id == p.id:
                print("댓글 생성 시도 확인")
                skilnote4 = MyShortCutForSkilNote4.objects.filter(id = comment.id)
                skilnote4_comment = CommentForShortCutForSkilNoteForSkilNote4.objects.create(
                    author = request.user,
                    title=comment.title,
                    shortcut = myshortcut,
                    content = comment.content,
                    created_at = comment.created_at,
                )

    list_for_copy2 = CategoryNickForSkilNote4.objects.filter(Q(author=user_id))
    print("list_for_copy2 : " , list_for_copy2);

    CategoryNickForSkilNote4.objects.filter(Q(author=request.user)).delete()

    for p in list_for_copy2:
        CN = CategoryNickForSkilNote4.objects.create(
            author = request.user,
            ca1 = p.ca1,
            ca2 = p.ca2,
            ca3 = p.ca3,
            ca4 = p.ca4,
            ca5 = p.ca5,
            ca6 = p.ca6,
            ca7 = p.ca7,
            ca8 = p.ca8,
            ca9 = p.ca9,
            ca10 = p.ca10,
            ca11 = p.ca11,
            ca12 = p.ca12,
            ca13 = p.ca13,
            ca14 = p.ca14,
            ca15 = p.ca15,
            ca16 = p.ca16,
            ca17 = p.ca17,
            ca18 = p.ca18,
            ca19 = p.ca19,
            ca20 = p.ca20,
            ca21 = p.ca21,
            ca22 = p.ca22,
            ca23 = p.ca23,
            ca24 = p.ca24,
            ca25 = p.ca25,
            ca26 = p.ca26,
            ca27 = p.ca27,
            ca28 = p.ca28,
            ca29 = p.ca29,
            ca30 = p.ca30,
            ca31 = p.ca31,
            ca32 = p.ca32,
            ca33 = p.ca33,
            ca34 = p.ca34,
            ca35 = p.ca35,
            ca36 = p.ca36,
            ca37 = p.ca37,
            ca38 = p.ca38,
            ca39 = p.ca39,
            ca40 = p.ca40,
            ca41 = p.ca41,
            ca42 = p.ca42,
            ca43 = p.ca43,
            ca44 = p.ca44,
            ca45 = p.ca45,
            ca46 = p.ca46,
            ca47 = p.ca47,
            ca48 = p.ca48,
            ca49 = p.ca49,
            ca50 = p.ca50,
            ca51 = p.ca51,
            ca52 = p.ca52,
            ca53 = p.ca53,
            ca54 = p.ca54,
            ca55 = p.ca55,
            ca56 = p.ca56,
            ca57 = p.ca57,
            ca58 = p.ca58,
            ca59 = p.ca59,
            ca60 = p.ca60,
            ca61 = p.ca61,
            ca62 = p.ca62,
            ca63 = p.ca63,
            ca64 = p.ca64,
            ca65 = p.ca65,
            ca66 = p.ca66,
            ca67 = p.ca67,
            ca68 = p.ca68,
            ca69 = p.ca69,
            ca70 = p.ca70,
            ca71 = p.ca71,
            ca72 = p.ca72,
            ca73 = p.ca73,
            ca74 = p.ca74,
            ca75 = p.ca75,
            ca76 = p.ca76,
            ca77 = p.ca77,
            ca78 = p.ca78,
            ca79 = p.ca79,
            ca80 = p.ca80,
            ca81 = p.ca81,
            ca82 = p.ca82,
            ca83 = p.ca83,
            ca84 = p.ca84,
            ca85 = p.ca85,
            ca86 = p.ca86,
            ca87 = p.ca87,
            ca88 = p.ca88,
            ca89 = p.ca89,
            ca90 = p.ca90,
            ca91 = p.ca91,
            ca92 = p.ca92,
            ca93 = p.ca93,
            ca94 = p.ca94,
            ca95 = p.ca95,
            ca96 = p.ca96,
            ca97 = p.ca97,
            ca98 = p.ca98,
            ca99 = p.ca99,
        )

    return JsonResponse({
        'message': author+'의 노트 전체를 나의 노트로 복사 했습니다',
    })

def edit_complete_skill_note_for_backend(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('TempMyShortCutForBackEndForSkilNote text를 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = TempMyShortCutForBackEndForSkilNote4.objects.filter(Q(id=id)).update(content2 = content2)
        print('backend update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def edit_complete_skill_note_for_front_end(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('shortcut을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = TempMyShortCutForSkilNote4.objects.filter(Q(id=id)).update(content2 = content2)
        print('frontend update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def edit_temp_skill_note_using_textarea_for_backend(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('TempMyShortCutForSkilNote 을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = TempMyShortCutForBackEndForSkilNote4.objects.filter(Q(id=id)).update(content2 = content2)
        print('TempMyShortCutForSkilNote update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def edit_temp_skill_note_using_input_for_backend(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST.get('content1','')

        print('TempMyShortCutForBackEndForSkilNote 을 ajax로 update input')
        print('id : ', id)
        print("content1 : ", content1)
        todo = TempMyShortCutForBackEndForSkilNote4.objects.filter(Q(id=id)).update(content1 = content1)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공 22',
        })
    else:
        return redirect('/todo')

def update_temp_skil_title_for_backend(request,id):
    user = request.user
    title = request.POST['title']

    if request.method == "POST" and request.is_ajax():
        todo = TempMyShortCutForBackEndForSkilNote4.objects.filter(Q(id=id)).update(title=title)
        print('TempMyShortCutForBackEndForSkilNote4 update 성공 id : ' , id);

        return JsonResponse({
            'message': 'shortcut 업데이트 성공',
            'title':title
        })
    else:
        return redirect('/todo')

def delete_temp_skill_note_for_backendarea(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = TempMyShortCutForBackEndForSkilNote4.objects.filter(Q(id=id)).delete()
        print('TempMyShortCutForBackEndForSkilNote4 delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 삭제 성공',
        })
    else:
        return redirect('/todo')

def insert_temp_skill_note_using_input_for_backend(request):
    print("create_new1_input 22 실행")
    ty = TypeForSkilNote4.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']

    skilnote4 = TempMyShortCutForBackEndForSkilNote4.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = ""
    )
    print("skilnote4 : ", skilnote4)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content':skilnote4.content1,
    })


def insert_temp_skill_note_using_textarea_for_backend(request):
    print("insert_temp_skill_note_for_textarea 실행")
    ty = TypeForSkilNote4.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']

    skilnote4 = TempMyShortCutForBackEndForSkilNote4.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content2 = ""
    )

    print("skilnote4 : ", skilnote4)

    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content2':skilnote4.content2,
    })



def temp_skill_list_for_backend1(request):
    print("***** BackEnd mini note 실행 확인 *******")
    user = request.user

    if (user==None):
        user = request.user

    object_list = TempMyShortCutForBackEndForSkilNote4.objects.filter(author=user)

    return render(request, 'skilnote4/TempMyShortCutForBackEnd_list.html', {
        'object_list': object_list,
        'page_user': user
    })

def temp_skill_list1(request):
    print("***** FrontEnd mini note 실행 확인 *******")
    user = request.user

    if (user==None):
        user = request.user

    print("user : ", user)
    object_list = TempMyShortCutForSkilNote4.objects.filter(author=user)

    return render(request, 'skilnote4/TempMyShortCut_list.html', {
        'object_list': object_list,
        'page_user': user
    })

def temp_skill_list_for_backend2(request,page_user):
    print("***** BackEnd mini note 실행 확인 *******")
    user = User.objects.get(username=page_user)

    if (user==None):
        user = request.user

    object_list = TempMyShortCutForBackEndForSkilNote4.objects.filter(author=user)

    return render(request, 'skilnote4/TempMyShortCutForBackEnd_list.html', {
        'object_list': object_list,
        'page_user': user
    })

def temp_skill_list2(request,page_user):
    print("***** FrontEnd mini note 실행 확인 *******")
    user = User.objects.get(username=page_user)

    if (user==None):
        user = request.user

    print("user : ", user)
    object_list = TempMyShortCutForSkilNote4.objects.filter(author=user)

    return render(request, 'skilnote4/TempMyShortCut_list.html', {
        'object_list': object_list,
        'page_user': user
    })


def insert_temp_skill_note_for_input(request):
    print("create_new1_input 실행 11")
    ty = TypeForSkilNote4.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']

    skilnote4 = TempMyShortCutForSkilNote4.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = ""
    )
    print("skilnote4 : ", skilnote4)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content':skilnote4.content1,
    })

def edit_temp_skill_note_for_input(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST.get('content1','')

        print('TempMyShortCutForSkilNote 을 ajax로 update input')
        print('id : ', id)
        print("content1 : ", content1)
        todo = TempMyShortCutForSkilNote4.objects.filter(Q(id=id)).update(content1 = content1)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def update_temp_skill_note_for_textarea(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('TempMyShortCutForSkilNote4 을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = TempMyShortCutForSkilNote4.objects.filter(Q(id=id)).update(content2 = content2)
        print('TempMyShortCutForSkilNote4 update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')




def delete_temp_memo_by_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = TempMyShortCutForSkilNote4.objects.filter(Q(id=id)).delete()
        print('TempMyShortCutForSkilNote4 delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 삭제 성공',
        })
    else:
        return redirect('/todo')

def update_temp_skil_title(request,id):
    user = request.user
    title = request.POST['title']

    if request.method == "POST" and request.is_ajax():
        todo = TempMyShortCutForSkilNote4.objects.filter(Q(id=id)).update(title=title)
        print('TempMyShortCutForSkilNote4 update 성공 id : ' , id);

        return JsonResponse({
            'message': 'shortcut 업데이트 성공',
            'title':title
        })
    else:
        return redirect('/todo')



def copyForCategorySubjectToMyCategory(request):
	author = request.POST['author']
	original_category = request.POST['original_category']
	destination_category = request.POST['destination_category']

	print("author : ", author)
	print("original_category : ", original_category)
	print("destination_category : ", destination_category)

	MyShortCutForSkilNote4.objects.filter(Q(author=request.user) & Q(category=destination_category)).delete()

	user_id = User.objects.get(username=author).id
	ca_id = CategoryForSkilNote4.objects.get(name=original_category)

	list_for_copy = MyShortCutForSkilNote4.objects.filter(Q(author=user_id) & Q(category = ca_id))

	category = CategoryForSkilNote4.objects.get(id=destination_category)

	for p in list_for_copy:
		profile = MyShortCutForSkilNote4.objects.create(
			author = request.user,
			title = p.title,
			content1 = p.content1,
			content2 = p.content2,
			type_id = p.type_id,
            created=p.created,
			category = category,
		)
	return JsonResponse({
		'message': author+'의 '+ original_category +'를 나의 ' +destination_category +'로 복사 했습니다',
	})


class search_skil_note_by_word(ListView):
    model = MyShortCutForSkilNote4
    paginate_by = 10
    template_name = 'book/MyShortCut_list_for_search.html'

    def get_queryset(self,request):
        # 검색할 유저(비로그인인 경우)
        try:
            page_user = self.request.POST['page_user']
        except MultiValueDictKeyError:
            page_user = False

        # 검색할 유저(로그인 유저일 경우 => 나 )
        if(request.user.is_authenticated):
            user = self.request.user
            search_word = self.request.POST['search_word']
            search_option = self.request.POST['search_option']
            print("search_word : ", search_word)
            print("search_option : ", search_option)

        # 로그인 유저에 대한 유저 객체 생성
        if(page_user):
            user = User.objects.get(username=page_user)
        else:
            user = User.objects.get(username=user)

        # 쿼리셋 객체 생성
        qs = MyShortCutForSkilNote4.objects.filter(Q(author = user)).filter(Q(title__icontains=search_word) | Q(content1__icontains=search_word) | Q(content2__icontains=search_word)).order_by('-category')
        return qs


class searchSkilNoteViewByIdAndWord(ListView):
    model = MyShortCutForSkilNote4
    paginate_by = 10
    template_name = 'skilnote4/MyShortCut_list_for_search.html'

    def get_queryset(self):
        if request.method == "POST" and request.is_ajax():
            search_user_id = request.user
            search_word = request.POST['search_word']
            search_option = request.POST['search_option']
            print("search_user_id : ", search_user_id)
            print("search_word : ", search_word)
            print("search_option : ", search_option)
            user = User.objects.get(username=search_user_id)
            qs = MyShortCutForSkilNote4.objects.filter(Q(author = user)).filter(Q(title__icontains=search_word) | Q(content1__icontains=search_word) | Q(content2__icontains=search_word)).order_by('-category')
            return qs
        else:
            qs = MyShortCutForSkilNote4.objects.filter(Q(author = user)).filter(Q(title__icontains=search_word) | Q(content1__icontains=search_word) | Q(content2__icontains=search_word)).order_by('-category')
            return qs


def delete_comment_for_my_shortcut(request, shortcut_comment_id):
    print('shortcut_comment_id : ' , shortcut_comment_id)
    co = CommentForShortCutForSkilNote4.objects.filter(id=shortcut_comment_id).delete()

    return JsonResponse({
        'message': '댓글 삭제 성공',
    })

def update_comment_for_my_shortcut(request, shortcut_comment_id):
    print('shortcut_comment_id : ' , shortcut_comment_id)
    co = CommentForShortCutForSkilNote4.objects.filter(id=shortcut_comment_id).update(
        title= request.POST['title'],
        content = request.POST['content']
    )

    return JsonResponse({
        'message': '댓글 수정 성공',
    })

def new_comment_for_my_shortcut(request, shortcut_id):
    print('shortcut_id : ' , shortcut_id)
    shortcut = MyShortCutForSkilNote4.objects.get(id=shortcut_id)
    co = CommentForShortCutForSkilNote4.objects.create(
        shortcut= shortcut,
        author = request.user,
        title="default title",
        content = "default content"
    )

    return JsonResponse({
        'message': shortcut.title+ '에 대해 comment 추가 성공 ',
        'comment_id':co.id,
        'comment_title':co.title,
        'comment_content':co.content,
    })

# def create_new4_textarea(request):
#     print("create_new4_textarea 실행")
#     ty = TypeForSkilNote4.objects.get(type_name="textarea")
#     category_id = request.user.profile.selected_category_id
#     ca = CategoryForSkilNote4.objects.get(id=category_id)
#     # title = request.POST['title']
#
#     skilnote41 = MyShortCutForSkilNote4.objects.create(
#         author = request.user,
#         title="title1",
#         type= ty,
#         category = ca,
#         content2 = ""
#     )
#     skilnote42 = MyShortCutForSkilNote4.objects.create(
#         author = request.user,
#         title="title2",
#         type= ty,
#         category = ca,
#         content2 = ""
#     )
#     skilnote43 = MyShortCutForSkilNote4.objects.create(
#         author = request.user,
#         title="title3",
#         type= ty,
#         category = ca,
#         content2 = ""
#     )
#     skilnote44 = MyShortCutForSkilNote4.objects.create(
#         author = request.user,
#         title="title4",
#         type= ty,
#         category = ca,
#         content2 = ""
#     )
#     skilnote45 = MyShortCutForSkilNote4.objects.create(
#         author = request.user,
#         title="title5",
#         type= ty,
#         category = ca,
#         content2 = ""
#     )
#
#     print("skilnote41 : ", skilnote41)
#
#     return JsonResponse({
#         'message': 'textarea 박스 추가 성공',
#         'shortcut_id':skilnote41.id,
#         'shortcut_title':skilnote41.title,
#         'shortcut_content2':skilnote41.content2,
#     })

# myshortcut_row, shorcut_id, shorcut_content
def create_new1_input(request):
    print("create_new1_input 실행 original")
    ty = TypeForSkilNote4.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']

    skilnote4 = MyShortCutForSkilNote4.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = "",
        created = datetime.now()
    )
    print("skilnote4 : ", skilnote4)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content':skilnote4.content1,
    })


def create_new1_input_between(request,current_article_id):

    current_article_id = current_article_id
    current_article = MyShortCutForSkilNote4.objects.get(id=current_article_id)
    print("current_article_time : " , current_article.created)

    smae_category_for_current_article=MyShortCutForSkilNote4.objects.filter(author= current_article.author, category = current_article.category).order_by("created")

    same_category_id_array = []

    for i,p in enumerate(smae_category_for_current_article):
        # print('i',i)
        if (p.created <= current_article.created):
            MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
        else:
            MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))


    print("create_new1_input 실행")
    ty = TypeForSkilNote4.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']

    skilnote4 = MyShortCutForSkilNote4.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        content1 = "",
        created=current_article.created+timedelta(seconds=1.5)
    )
    print("skilnote4 : ", skilnote4)
    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content':skilnote4.content1,
    })

def create_input_first(request):
    print("input box ajax 입력 box 실행 skil note2 !!!!")
    ty = TypeForSkilNote4.objects.get(type_name="input")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']

    current_first = MyShortCutForSkilNote4.objects.filter(Q(category=category_id) & Q(author=request.user)).order_by("created").first();
    if(current_first != None):
        print("current_first.id : ", current_first.title);
        skilnote4 = MyShortCutForSkilNote4.objects.create(
            author = request.user,
            title=title,
            type= ty,
            category = ca,
            content1 = "",
            created = current_first.created-timedelta(seconds=10)
        )
    else:
        skilnote4 = MyShortCutForSkilNote4.objects.create(
            author = request.user,
            title=title,
            type= ty,
            category = ca,
            content1 = "",
            created = timezone.now()
        )

    return JsonResponse({
        'message': '인풋 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content':skilnote4.content1,
    })


def create_textarea_first(request):
    print("create_new2_textarea_first")
    ty = TypeForSkilNote4.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']
    file_name_before = request.POST['file_name']
    file_name = file_name_before.replace("\\","/")

    current_first = MyShortCutForSkilNote4.objects.filter(Q(category=category_id) & Q(author=request.user)).order_by("created").first()
    if(current_first != None):
        skilnote4 = MyShortCutForSkilNote4.objects.create(
            author = request.user,
            title=title,
            filename=file_name,
            type= ty,
            category = ca,
            created = current_first.created-timedelta(seconds=10),
            content2 = ""
        )
    else:
        skilnote4 = MyShortCutForSkilNote4.objects.create(
            author = request.user,
            title=title,
            filename=file_name,
            type= ty,
            category = ca,
            created = timezone.now(),
            content2 = ""
        )

    print("skilnote4 : ", skilnote4)
    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content2':skilnote4.content2,
        # 'author':wm.author.username,
    })

# summer note 첫번째에 추가 하기 2244
def create_summernote_first(request):
    print("create_summer_note")
    ty = TypeForSkilNote4.objects.get(type_name="summer_note")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']
    file_name_before = request.POST['file_name']
    file_name = file_name_before.replace("\\","/")

    current_first = MyShortCutForSkilNote4.objects.filter(Q(category=category_id) & Q(author=request.user)).order_by("created").first();
    if(current_first != None):
        print("current_first.id : ", current_first.title);

        skilnote4 = MyShortCutForSkilNote4.objects.create(
            author = request.user,
            title=title,
            filename=file_name,
            type= ty,
            category = ca,
            created = current_first.created-timedelta(seconds=10),
            content2 = ""
        )
    else:
        skilnote4 = MyShortCutForSkilNote4.objects.create(
            author = request.user,
            title=title,
            filename=file_name,
            type= ty,
            category = ca,
            created = timezone.now(),
            content2 = ""
        )

    print("skilnote4 : ", skilnote4)
    return JsonResponse({
        'message': 'summer note 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content2':skilnote4.content2,
    })



def create_new2_textarea(request):
    print("create_new2_textarea 실행")
    ty = TypeForSkilNote4.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']
    # filename = request.POST['filename']
    file_name_before = request.POST['file_name']
    file_name = file_name_before.replace("\\","/")
    author = request.user.username

    print("author : ", author)

    skilnote4 = MyShortCutForSkilNote4.objects.create(
        author = request.user,
        title=title,
        filename=file_name,
        type= ty,
        category = ca,
        created = datetime.now(),
        content2 = ""
    )
    print("skilnote4 : ", skilnote4)
    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content2':skilnote4.content2,
        'file_name':skilnote4.filename,
        'author':author
    })

def create_new2_textarea_between(request,current_article_id):
    current_article_id = current_article_id
    current_article = MyShortCutForSkilNote4.objects.get(id=current_article_id)
    print("current_article_time : " , current_article.created)
    smae_category_for_current_article=MyShortCutForSkilNote4.objects.filter(author= current_article.author, category = current_article.category).order_by("created")
    same_category_id_array = []

    for i,p in enumerate(smae_category_for_current_article):
        # print('i',i)
        if (p.created <= current_article.created):
            MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
        else:
            MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))

    print("create_new2_textarea 실행")
    ty = TypeForSkilNote4.objects.get(type_name="textarea")
    category_id = request.user.profile.selected_category_id
    ca = CategoryForSkilNote4.objects.get(id=category_id)
    title = request.POST['title']

    skilnote4 = MyShortCutForSkilNote4.objects.create(
        author = request.user,
        title=title,
        type= ty,
        category = ca,
        created=current_article.created+timedelta(seconds=1.5),
        content2 = ""
    )
    print("skilnote4 : ", skilnote4)
    return JsonResponse({
        'message': 'textarea 박스 추가 성공',
        'shortcut_id':skilnote4.id,
        'shortcut_title':skilnote4.title,
        'shortcut_content2':skilnote4.content2,
    })

def update_category_by_ajax(request):
    shortcut_ids = request.POST.getlist('shortcut_arr[]')
    category = request.POST['category']

    for i, sn in enumerate(shortcut_ids):
        MyShortCutForSkilNote4.objects.filter(id=sn, author=request.user).update(category=category, created = datetime.now()+timedelta(seconds=i),image=F('image'))

    return redirect('/skilnote4/myshortcut')

def delete_myshortcut_by_ajax(request):
    shortcut_ids = request.POST.getlist('shortcut_arr[]')
    if shortcut_ids:
        MyShortCutForSkilNote4.objects.filter(pk__in=shortcut_ids, author=request.user).delete()

    return redirect('/skilnote4/myshortcut')


def update_my_shortcut_subject(request):
    if request.method == "POST" and request.is_ajax():
        shortcut_subject = request.POST['shortcut_subject']

        print('update shortcut_subject : ',shortcut_subject)
        pf = Profile.objects.filter(user=request.user).update(subject_of_memo = shortcut_subject)

        print('shortcut_subject success : ' , shortcut_subject);

        return JsonResponse({
            'message': 'shortcut_subject update 성공 : ' +shortcut_subject
        })
    else:
        return redirect('/skilnote4/shortcut')


def favorite_user_list_for_skillnote(request):
    if request.method == 'GET':
        print("user_list_for_memo 실행")

        my_favorite = []
        ru = RecommandationUserAboutSkilNote4.objects.filter(author_id=request.user)

        for x in ru:
            print("내가 추천한 user_id : ",x.user_id)
            my_favorite.append(x.user_id)

        object_list = User.objects.filter(id__in=my_favorite).order_by('-profile__skill_note_reputation');

        print("object_list : ", object_list)


        return render(request, 'skilnote4/favorite_user_list_for_skilnote.html', {
            "object_list" : object_list,
        })
    else:
        return HttpResponse("Request method is not a GET")



class user_list_for_memo_view(ListView):
    paginate_by = 10
    # if 'q' in request.GET:
    #     query = request.GET.get('q')
    #     print("query : ", query)

    def get_template_names(self):
        if self.request.is_ajax():
            print("user list ajax 요청 확인")
            return ['skilnote4/_user_list_for_memo.html']
        return ['skilnote4/user_list_for_memo.html']

    def get_queryset(self):
        print("실행 확인 겟 쿼리셋")
        query = self.request.GET.get('q')
        print("query : ", query)

        if query != None:
            object_list = User.objects.all().filter(Q(username__contains=query)).order_by('-profile__skill_note_reputation');
            return object_list
        else:
            print("user list 출력 확인 ===========================================================")
            object_list = User.objects.all().filter(profile__public="yes").order_by('-profile__skill_note_reputation');
            print("result : ", object_list)
            return object_list


def update_shortcut_nick(request):
    if request.method == "POST" and request.is_ajax():
        ca_id = int(request.POST['ca_id'])
        field = request.POST['field']
        ca_nick_update = request.POST['ca_nick_update']

        print('update id : ',ca_id)
        print('update field  : ',field)
        print('update value : ',ca_nick_update)
        cn = CategoryNickForSkilNote4.objects.filter(id=ca_id).update(**{field: ca_nick_update})
        # .update(field = ca_nick_update)

        # print('update success : ' , update.id);

        return JsonResponse({
            'message': 'shortcut category nick name update 성공 ' +ca_nick_update,
        })
    else:
        return redirect('/skilnote4/shortcut')

def update_shortcut_nick2(request):
    if request.method == "POST" and request.is_ajax():
        ca_id = CategoryNickForSkilNote4.objects.get(author=request.user).id
        field = request.POST['field']
        ca_nick_update = request.POST['ca_nick_update']

        print('update id : ',ca_id)
        print('update field  : ',field)
        print('update value : ',ca_nick_update)

        cn = CategoryNickForSkilNote4.objects.filter(id=ca_id).update(**{field: ca_nick_update})
        # .update(field = ca_nick_update)

        # print('update success : ' , update.id);

        return JsonResponse({
            'message': 'shortcut category nick name update 성공 ' +ca_nick_update,
        })
    else:
        return redirect('/skilnote4/shortcut')


def CategoryNickListByUserId(request, user_name):
    if request.method == 'GET':
        print("user_name : ", user_name)
        user = User.objects.get(username=user_name)

        cn = CategoryNickForSkilNote4.objects.get_or_create(
            author=user,
        )
        print("cn : ", cn)

        cn_my = CategoryNickForSkilNote4.objects.get(author=user.id)
        print("cn_my : ", cn_my)

        return render(request, 'skilnote4/categorynick_list.html', {
            "category" : cn_my,
        })
    else:
        return HttpResponse("Request method is not a GET")


def CategoryNickListByUserId_for_user(request, user_name):
    if request.method == 'GET':
        print("user_name : ", user_name)
        user = User.objects.get(username=user_name)

        cn = CategoryNickForSkilNote4.objects.get_or_create(
            author=user,
        )
        print("cn : ", cn)

        cn_my = CategoryNickForSkilNote4.objects.get(author=user.id)
        print("cn_my : ", cn_my)

        return render(request, 'skilnote4/categorynick_list_for_user.html', {
            "category" : cn_my,
            "page_user": user_name
        })
    else:
        return HttpResponse("Request method is not a GET")


class update_skilnote_by_summernote(UpdateView):
    model = MyShortCutForSkilNote4
    form_class = SkilNoteForm

    def get_template_names(self):
        return ['skilnote4/myshortcut_summernote_form.html']

class modify_myshortcut_by_summer_note2(UpdateView):
    model = MyShortCutForSkilNote4
    form_class = SkilNoteForm

    def get_template_names(self):
        return ['skilnote4/myshortcut_summernote_form.html']


    def get_success_url(self):
        return reverse('skilnote4:my_shortcut_list2')


# 나의 shorcut id를 user list에서 클릭한 id로 교체
def update_shorcut_id_for_user(request, id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        user_id = request.POST['user_id']
        original_userId = id
        option=""
        original_user = ""

        print("id :", id)
        print("user_id : ", user_id)

        user_exist = User.objects.filter(username = user_id)
        original_user = user_id
        print("user_exist : ", user_exist)

        if user_exist:
            option = "메모장 유저를 " + user_id + "로 업데이트 하였습니다."
            todo = Profile.objects.filter(Q(user=request.user)).update(shortcut_user_id = user_id)
            print("메모장 유저를 {}로 교체 ".format(user_id))
        else:
            original_user = User.objects.get(id = original_userId).username
            print("original_user : ", original_user)
            option = user_id+ "유저가 없으므로 업데이트를 하지 않았습니다."
            print("유저를 업데이트 하지 않았습니다.")

        return JsonResponse({
            'message': option,
            'original_id': original_user
        })
    else:
        return redirect('/todo')

def update_shortcut1_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        content1 = request.POST.get('content1','')

        print('shortcut을 ajax로 update input')
        print('id : ', id)
        print("content1 : ", content1)
        todo = MyShortCutForSkilNote4.objects.filter(Q(id=id)).update(content1 = content1)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')

def update_shortcut2_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        print("content2 변수 넘어 왔다.")
        content2 = request.POST.get('content2','')
        # content2 = request.POST['content2']

        print('shortcut을 ajax로 update textarea')
        print('id : ', id)
        print("content2 : ", content2)
        todo = MyShortCutForSkilNote4.objects.filter(Q(id=id)).update(content2 = content2)
        print('update 성공');

        return JsonResponse({
            'message': '댓글 업데이트 성공',
        })
    else:
        return redirect('/todo')


def myfunc():
    print("myfunc 실행")


# 2244
class MyShortcutListByCategory(ListView):

    def get_template_names(self):
        return ['skilnote4/skil_note4_list.html']

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = CategoryForSkilNote4.objects.get(slug=slug)
        pf = Profile.objects.filter(Q(user=self.request.user)).update(selected_category_id = category.id)
        print('category id update 성공')

        user = User.objects.get(Q(username = self.request.user))

        print('user : ' , user)

        return MyShortCutForSkilNote4.objects.filter(category=category, author=user).order_by('created')

    def get_context_data(self, *, object_list=None, **kwargs):
        user = User.objects.get(Q(username = self.request.user))

        context = super(type(self), self).get_context_data(**kwargs)
        context['posts_without_category'] = MyShortCutForSkilNote4.objects.filter(category=None,author=user).count()
        context['category_list'] = CategoryForSkilNote4.objects.all()

        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = CategoryForSkilNote4.objects.get(slug=slug)
            context['category'] = category
            context['category_nick'] = CategoryNickForSkilNote4.objects.values_list(slug, flat=True).get(author=user)

        return context


def delete_shortcut_ajax(request,id):
    user = request.user
    if request.method == "POST" and request.is_ajax():
        todo = MyShortCutForSkilNote4.objects.filter(Q(id=id)).delete()
        print('MyShortCutForSkilNote4 delete 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 삭제 성공',
        })
    else:
        return redirect('/todo')

def update_shortcut_ajax(request,id):
    user = request.user
    title = request.POST['title']

    if request.method == "POST" and request.is_ajax():
        todo = MyShortCutForSkilNote4.objects.filter(Q(id=id)).update(title=title)
        print('MyShortCutForSkilNote4 update 성공 id : ' , id);
        return JsonResponse({
            'message': 'shortcut 업데이트 성공',
            'title':title
        })
    else:
        return redirect('/todo')

def update_skil_note_file_name(request,id):
    user = request.user
    # file_name = request.POST['file_name']
    file_name_before = request.POST['file_name']
    file_name = file_name_before.replace("\\","/")

    if request.method == "POST" and request.is_ajax():
        sn = MyShortCutForSkilNote4.objects.filter(Q(id=id)).update(filename=file_name)
        print('filename update 성공 id : ' , sn);
        return JsonResponse({
            'message': 'file_name 업데이트 성공',
            'file_name':file_name
        })
    else:
        return redirect('/todo')

# 2244
class SkilNoteListView(LoginRequiredMixin,ListView):
    model = MyShortCutForSkilNote4
    def get_template_names(self):
        return ['skilnote4/skil_note4_list.html']


    def get_queryset(self):
        user = self.request.user
        print("self.request.user : ", self.request.user)
        try:
            profile = Profile.objects.get(user=self.request.user)
            selected_category_id = profile.user.profile.selected_category_id
            print("selected_category_id ::::::::::::: " , selected_category_id)

            qs = MyShortCutForSkilNote4.objects.filter(Q(author=user, category = selected_category_id)).order_by('created')
            print("SkilNoteListView(qs) ::::::::::::::::" , qs)
        except:
            profile = Profile.objects.create(user=self.request.user)
            selected_category_id = self.request.user.profile.selected_category_id
            print("profile 생성 성공 ")
            qs = MyShortCutForSkilNote4.objects.filter(Q(author=user, category = selected_category_id)).order_by('created')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        cn = CategoryNickForSkilNote4.objects.get_or_create(
            author=self.request.user,
        )
        context = super(SkilNoteListView, self).get_context_data(**kwargs)
        category_list = CategoryForSkilNote4.objects.all()
        # print("category_list ::::::::" , category_list)

        if not category_list:
            for num in range(1,121):
                filed_name = "ca"+str(num)
                slug_name="ca"+str(num)
                CategoryForSkilNote4.objects.create(pk=num , name=filed_name, slug=slug_name, author=self.request.user)
                print("카테고리 row 생성 성공 ca",num)
                category_list = CategoryForSkilNote4.objects.all()
        else:
            print("카테고리가 이미 존재 ok!!!!!!!!")
            context['category_list'] = category_list
            category = CategoryForSkilNote4.objects.get(id=self.request.user.profile.selected_category_id)
            print("category ::", category)
            context['category'] = category
            context['category_nick'] = CategoryNickForSkilNote4.objects.values_list(category.name, flat=True).get(author=self.request.user)
        return context

class search_skil_note_for_me(LoginRequiredMixin,ListView):
    model = MyShortCutForSkilNote4
    paginate_by = 10

    def get_template_names(self):
        return ['skilnote4/search_skil_note_for_me.html']

    def get_queryset(self):
        if self.request.method == 'GET' and 'q' in self.request.GET:
            query = self.request.GET.get('q')
        else:
            query=""

        print("query ::::::::::::::: ", query)
        print('검색 결과를 출력합니다 유저는 {} 검색어는 {} 입니다 ################################################'.format(self.request.user, query))
        qs = MyShortCutForSkilNote4.objects.filter(Q(author=self.request.user) & (Q(title__contains=query) | Q(filename__contains=query) | Q(content1__contains=query) | Q(content2__contains=query))).order_by('created')
        print("qs : ", qs)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(search_skil_note_for_me, self).get_context_data(**kwargs)
        context['query'] =  self.request.GET.get('q')
        return context

class search_skilnote_by_file_name_for_me(LoginRequiredMixin,ListView):
    model = MyShortCutForSkilNote4
    paginate_by = 10

    def get_template_names(self):
        return ['skilnote4/search_skil_note_for_file_name_for_me.html']

    def get_queryset(self):
        if self.request.method == 'GET' and 'q' in self.request.GET:
            query = self.request.GET.get('q')
        else:
            query=""

        print("query ::::::::::::::: ", query)
        print('파일 검색 결과를 출력합니다 유저는 {} 검색어는 {} 입니다 ################################################'.format(self.request.user, query))
        qs = MyShortCutForSkilNote4.objects.filter(Q(author=self.request.user) & Q(filename__contains=query)).order_by('created')
        print("qs : ", qs)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(search_skilnote_by_file_name_for_me, self).get_context_data(**kwargs)
        context['query'] =  self.request.GET.get('q')
        return context

class search_skilnote_by_file_name_for_all(LoginRequiredMixin,ListView):
    model = MyShortCutForSkilNote4
    paginate_by = 10

    def get_template_names(self):
        return ['skilnote4/search_skil_note_for_file_name_for_all.html']

    def get_queryset(self):
        if self.request.method == 'GET' and 'q' in self.request.GET:
            query = self.request.GET.get('q')
        else:
            query=""

        print("query ::::::::::::::: ", query)
        print('파일 검색 결과를 출력합니다 유저는 all 검색어는 {} 입니다 ##'.format(self.request.user, query))
        qs = MyShortCutForSkilNote4.objects.filter(Q(filename__contains=query)).order_by('created')
        print("qs : ", qs)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(search_skilnote_by_file_name_for_all, self).get_context_data(**kwargs)
        context['query'] =  self.request.GET.get('q')
        return context


class search_skil_note_for_all(LoginRequiredMixin,ListView):
    model = MyShortCutForSkilNote4
    paginate_by = 10

    def get_template_names(self):
        return ['skilnote4/search_skil_note_for_all_user.html']

    def get_queryset(self):
        if self.request.method == 'GET' and 'q' in self.request.GET:
            query = self.request.GET.get('q')
        else:
            query=""

        print("query ::::::::::::::: ", query)
        print('검색 결과를 출력합니다 유저는 전체 검색어는 {} 입니다 ##'.format(query))
        qs = MyShortCutForSkilNote4.objects.filter(Q(title__contains=query) | Q(filename__contains=query) | Q(content1__contains=query) | Q(content2__contains=query)).order_by('created')
        print("qs : ", qs)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(search_skil_note_for_all , self).get_context_data(**kwargs)
        context['query'] =  self.request.GET.get('q')
        return context




class MyShortCutCreateView_input(LoginRequiredMixin,CreateView):
    model = MyShortCutForSkilNote4
    form_class = MyShortCutForm_input
    # fields = ['title','content1','category']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행11")
        ty = TypeForSkilNote4.objects.get(type_name="input")
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        category_id = self.request.user.profile.selected_category_id
        ca = CategoryForSkilNote4.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('skilnote4:my_shortcut_list')


class SkilNoteCreateView_image_through(LoginRequiredMixin,CreateView):
    model = MyShortCutForSkilNote4
    form_class = MyShortCutForm_image

    def form_valid(self, form):
        print("through 입력 확인")

        # current_category_id = self.request.user.profile.selected_category_id
        current_article_id = self.kwargs['current_article_id']
        current_article = MyShortCutForSkilNote4.objects.get(id=current_article_id)
        print("current_article_time : " , current_article.created)

        smae_category_for_current_article=MyShortCutForSkilNote4.objects.filter(author= current_article.author, category = current_article.category).order_by("created")

        same_category_id_array = []

        for i,p in enumerate(smae_category_for_current_article):
            # print('i',i)
            if (p.created <= current_article.created):
                MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
            else:
                MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))


        print("완료 명단 입력 뷰 실행2")
        ty = TypeForSkilNote4.objects.get(type_name="image")
        print("ty : ", ty)
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.created=current_article.created+timedelta(seconds=1.5)
        ms.type= ty
        category_id = self.request.user.profile.selected_category_id
        ca = CategoryForSkilNote4.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('skilnote4:my_shortcut_list')

class MyShortCutCreateView_image(LoginRequiredMixin,CreateView):
    model = MyShortCutForSkilNote4
    form_class = MyShortCutForm_image
    # fields = ['title','content1','category']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행2")
        ty = TypeForSkilNote4.objects.get(type_name="image")
        print("ty : ", ty)
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.created=timezone.now()
        ms.type= ty
        category_id = self.request.user.profile.selected_category_id
        ca = CategoryForSkilNote4.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('skilnote4:my_shortcut_list')


class MyShortCutCreateView_textarea(LoginRequiredMixin,CreateView):
    model = MyShortCutForSkilNote4
    fields = ['title','content2']

    def form_valid(self, form):
        print("완료 명단 입력 뷰 실행2")

        ty = TypeForSkilNote4.objects.get(type_name="textarea")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty

        category_id = self.request.user.profile.selected_category_id
        ca = CategoryForSkilNote4.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('skilnote4:my_shortcut_list')

class CreateSkilNoteBySummerNote(LoginRequiredMixin,CreateView):
    model = MyShortCutForSkilNote4
    form_class = SkilNoteForm

    def get_template_names(self):
        return ['skilnote4/myshortcut_summernote_form.html']

    def form_valid(self, form):
        print("create skil_note2 excute !!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        type_list = TypeForSkilNote4.objects.all()
        if not type_list:
            TypeForSkilNote4.objects.create(type_name="summer_note")
            TypeForSkilNote4.objects.create(type_name="textarea")
            TypeForSkilNote4.objects.create(type_name="input")
            TypeForSkilNote4.objects.create(type_name="image")
            print("타입 생성 성공 !!!!!!!!")

        ty = TypeForSkilNote4.objects.get(type_name="summer_note")
        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.type= ty
        ms.created = timezone.now()
        category_id = self.request.user.profile.selected_category_id
        ca = CategoryForSkilNote4.objects.get(id=category_id)
        ms.category = ca
        return super().form_valid(form)

    def get_success_url(self):
        category_id = self.request.user.profile.selected_category_id
        return reverse('skilnote4:my_shortcut_list')+'#shortcut_{}'.format(category_id)



class createSkilNoteForInsertMode(LoginRequiredMixin,CreateView):
    model = MyShortCutForSkilNote4
    form_class = SkilNoteForm

    def get_template_names(self):
        return ['skilnote4/myshortcut_summernote_form.html']

    def form_valid(self, form):
        print("summer note 입력 !!")
        type_list = TypeForSkilNote4.objects.all()
        if not type_list:
            TypeForSkilNote4.objects.create(type_name="summer_note")
            TypeForSkilNote4.objects.create(type_name="textarea")
            TypeForSkilNote4.objects.create(type_name="input")
            TypeForSkilNote4.objects.create(type_name="image")
            print("타입 생성 성공")
        else:
            print("타입이 이미 존재 ok!!!!!!!!")
        # ty = TypeForSkilNote4.objects.get(type_name="summer_note")
        ty = type_list.get(type_name="summer_note")
        ms = form.save(commit=False)
        ms.author = self.request.user

        ms.type= ty
        ms.created = timezone.now()

        category_id = self.request.user.profile.selected_category_id
        ca = CategoryForSkilNote4.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)

    def get_success_url(self):
        category_id = self.request.user.profile.selected_category_id
        return reverse('skilnote4:my_shortcut_list2')+'#shortcut_{}'.format(category_id)

class SkilNoteCreateView_summernote_through2(LoginRequiredMixin,CreateView):
    model = MyShortCutForSkilNote4
    form_class = SkilNoteForm

    def get_success_url(self):
        category_id = self.request.user.profile.selected_category_id
        return reverse('skilnote4:my_shortcut_list2')+'#shortcut_{}'.format(self.object.id)

    def get_template_names(self):
        return ['skilnote4/myshortcut_summernote_form.html']

    def form_valid(self, form):
        print("through 입력 확인 2222")

        # current_category_id = self.request.user.profile.selected_category_id
        current_article_id = self.kwargs['current_article_id']
        current_article = MyShortCutForSkilNote4.objects.get(id=current_article_id)
        print("current_article_time : " , current_article.created)

        smae_category_for_current_article=MyShortCutForSkilNote4.objects.filter(author= current_article.author, category = current_article.category).order_by("created")

        same_category_id_array = []

        for i,p in enumerate(smae_category_for_current_article):
            # print('i',i)
            if (p.created <= current_article.created):
                MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
            else:
                MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))


        print("same_category_id_array : ",same_category_id_array)

        ty = TypeForSkilNote4.objects.get(type_name="summer_note")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.created=current_article.created+timedelta(seconds=1.5)
        ms.type= ty

        category_id = self.request.user.profile.selected_category_id
        ca = CategoryForSkilNote4.objects.get(id=category_id)
        ms.category = ca

        return super().form_valid(form)


class SkilNoteCreateView_summernote_through(LoginRequiredMixin,CreateView):
    model = MyShortCutForSkilNote4
    form_class = SkilNoteForm

    def get_template_names(self):
        return ['skilnote4/myshortcut_summernote_form.html']

    def form_valid(self, form):
        print("through 입력 확인")

        # current_category_id = self.request.user.profile.selected_category_id
        current_article_id = self.kwargs['current_article_id']
        current_article = MyShortCutForSkilNote4.objects.get(id=current_article_id)
        print("current_article_time : " , current_article.created)

        smae_category_for_current_article=MyShortCutForSkilNote4.objects.filter(author= current_article.author, category = current_article.category).order_by("created")

        same_category_id_array = []

        for i,p in enumerate(smae_category_for_current_article):
            # print('i',i)
            if (p.created <= current_article.created):
                MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=0))
            else:
                MyShortCutForSkilNote4.objects.filter(id=p.id).update(created = F('created')+timedelta(seconds=i+1))


        print("same_category_id_array : ",same_category_id_array)
        ty = TypeForSkilNote4.objects.get(type_name="summer_note")

        ms = form.save(commit=False)
        ms.author = self.request.user
        ms.created=current_article.created+timedelta(seconds=1.5)
        ms.type= ty

        category_id = self.request.user.profile.selected_category_id
        ca = CategoryForSkilNote4.objects.get(id=category_id)
        ms.category = ca
        ms = form.save()

        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('skilnote4:my_shortcut_list')
