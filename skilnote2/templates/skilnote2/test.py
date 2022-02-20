url:



함수:
def CategoryNickListByUserId(request, user_name):
    if request.method == 'GET':
        print("user_name : ", user_name)
        user = User.objects.get(username=user_name)

        cn = CategoryNick.objects.get_or_create(
            author=user,
        )
        print("cn : ", cn)

        cn_my = CategoryNick.objects.get(author=user.id)
        print("cn_my : ", cn_my)

        return render(request, 'skilnote2/categorynick_list.html', {
            "category" : cn_my
        })
    else:
        return HttpResponse("Request method is not a GET")
