from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class LikeGuestBookForskinote3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 누구에 대한 좋아요인가?
    author_id = models.CharField(max_length=40) # 누가 좋아요를 눌렀나?

class GuestBookForSkilNote3(models.Model):
    owner_for_guest_book = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True , editable = False)

class RecommandationUserAboutSkilNote3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")

class CategoryForSkilNote3(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
            return '/skilnote3/myshortcut/category/{}/'.format(self.slug)

class TypeForSkilNote3(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

class TempMyShortCutForSkilNote3(models.Model):
    title = models.CharField(max_length=120)
    content1 = models.CharField(max_length=180 , blank=True)
    content2 = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True , editable = False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryForSkilNote3, blank=True, null=True, on_delete=models.CASCADE)
    type= models.ForeignKey(TypeForSkilNote3, on_delete=models.CASCADE)

    def get_absolute_url(self,*args,**kwargs):
            return reverse('skilnote3:my_shortcut_list')

    def __str__(self):
        return self.title

class TempMyShortCutForBackEndForSkilNote3(models.Model):
    title = models.CharField(max_length=120)
    content1 = models.CharField(max_length=180 , blank=True)
    content2 = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True , editable = False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryForSkilNote3, blank=True, null=True, on_delete=models.CASCADE)
    type= models.ForeignKey(TypeForSkilNote3, on_delete=models.CASCADE)

    def get_absolute_url(self,*args,**kwargs):
            return reverse('skilnote3:my_shortcut_list')

    def __str__(self):
        return self.title


# skil note용 모델
class MyShortCutForSkilNote3(models.Model):
    title = models.CharField(max_length=120)
    filename= models.CharField(max_length=120, blank=True)
    content1 = models.CharField(max_length=180, blank=True)
    content2 = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryForSkilNote3, blank=True, null=True, on_delete=models.CASCADE)
    type= models.ForeignKey(TypeForSkilNote3, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='skilnote3/%y%m%d', blank=True)

    def get_absolute_url(self,*args,**kwargs):
            return reverse('skilnote3:my_shortcut_list')+'#shortcut_{}'.format(self.pk)

    def __str__(self):
        return self.title

class CommentForShortCutForSkilNote3(models.Model):
    shortcut= models.ForeignKey(MyShortCutForSkilNote3, on_delete=models.CASCADE)
    title= models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CommentForPageForSkilNote3(models.Model):
    author= models.CharField(max_length=40)
    content = models.TextField()
    user_name = models.CharField(max_length=40, blank=True)
    category_id = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']


class CategoryNickForSkilNote3(models.Model):
    ca_subtitle = models.CharField(max_length=50, default="my category info")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ca1 = models.CharField(max_length=50, default="ca1")
    ca2 = models.CharField(max_length=50 , default="ca2")
    ca3 = models.CharField(max_length=50 , default="ca3")
    ca4 = models.CharField(max_length=50 , default="ca4")
    ca5 = models.CharField(max_length=50 , default="ca5")
    ca6 = models.CharField(max_length=50 , default="ca6")
    ca7 = models.CharField(max_length=50 , default="ca7")
    ca8 = models.CharField(max_length=50 , default="ca8")
    ca9 = models.CharField(max_length=50 , default="ca9")
    ca10 = models.CharField(max_length=50 , default="ca10")
    ca11 = models.CharField(max_length=50 , default="ca11")
    ca12 = models.CharField(max_length=50 , default="ca12")
    ca13 = models.CharField(max_length=50 , default="ca13")
    ca14 = models.CharField(max_length=50 , default="ca14")
    ca15 = models.CharField(max_length=50 , default="ca15")
    ca16 = models.CharField(max_length=50 , default="ca16")
    ca17 = models.CharField(max_length=50 , default="ca17")
    ca18 = models.CharField(max_length=50 , default="ca18")
    ca19 = models.CharField(max_length=50 , default="ca19")
    ca20 = models.CharField(max_length=50 , default="ca20")
    ca21 = models.CharField(max_length=50 , default="ca21")
    ca22 = models.CharField(max_length=50 , default="ca22")
    ca23 = models.CharField(max_length=50 , default="ca23")
    ca24 = models.CharField(max_length=50 , default="ca24")
    ca25 = models.CharField(max_length=50 , default="ca25")
    ca26 = models.CharField(max_length=50 , default="ca26")
    ca27 = models.CharField(max_length=50 , default="ca27")
    ca28 = models.CharField(max_length=50 , default="ca28")
    ca29 = models.CharField(max_length=50 , default="ca29")
    ca30 = models.CharField(max_length=50 , default="ca30")
    ca31 = models.CharField(max_length=50 , default="ca31")
    ca32 = models.CharField(max_length=50 , default="ca32")
    ca33 = models.CharField(max_length=50 , default="ca33")
    ca34 = models.CharField(max_length=50 , default="ca34")
    ca35 = models.CharField(max_length=50 , default="ca35")
    ca36 = models.CharField(max_length=50 , default="ca36")
    ca37 = models.CharField(max_length=50 , default="ca37")
    ca38 = models.CharField(max_length=50 , default="ca38")
    ca39 = models.CharField(max_length=50 , default="ca39")
    ca40 = models.CharField(max_length=50 , default="ca40")
    ca41 = models.CharField(max_length=50 , default="ca41")
    ca42 = models.CharField(max_length=50 , default="ca42")
    ca43 = models.CharField(max_length=50 , default="ca43")
    ca44 = models.CharField(max_length=50 , default="ca44")
    ca45 = models.CharField(max_length=50 , default="ca45")
    ca46 = models.CharField(max_length=50 , default="ca46")
    ca47 = models.CharField(max_length=50 , default="ca47")
    ca48 = models.CharField(max_length=50 , default="ca48")
    ca49 = models.CharField(max_length=50 , default="ca49")
    ca50 = models.CharField(max_length=50 , default="ca50")
    ca51 = models.CharField(max_length=50 , default="ca51")
    ca52 = models.CharField(max_length=50 , default="ca52")
    ca53 = models.CharField(max_length=50 , default="ca53")
    ca54 = models.CharField(max_length=50 , default="ca54")
    ca55 = models.CharField(max_length=50 , default="ca55")
    ca56 = models.CharField(max_length=50 , default="ca56")
    ca57 = models.CharField(max_length=50 , default="ca57")
    ca58 = models.CharField(max_length=50 , default="ca58")
    ca59 = models.CharField(max_length=50 , default="ca59")
    ca60 = models.CharField(max_length=50 , default="ca60")
    ca61 = models.CharField(max_length=50 , default="ca61")
    ca62 = models.CharField(max_length=50 , default="ca62")
    ca63 = models.CharField(max_length=50 , default="ca63")
    ca64 = models.CharField(max_length=50 , default="ca64")
    ca65 = models.CharField(max_length=50 , default="ca65")
    ca66 = models.CharField(max_length=50 , default="ca66")
    ca67 = models.CharField(max_length=50 , default="ca67")
    ca68 = models.CharField(max_length=50 , default="ca68")
    ca69 = models.CharField(max_length=50 , default="ca69")
    ca70 = models.CharField(max_length=50 , default="ca70")
    ca71 = models.CharField(max_length=50 , default="ca71")
    ca72 = models.CharField(max_length=50 , default="ca72")
    ca73 = models.CharField(max_length=50 , default="ca73")
    ca74 = models.CharField(max_length=50 , default="ca74")
    ca75 = models.CharField(max_length=50 , default="ca75")
    ca76 = models.CharField(max_length=50 , default="ca76")
    ca77 = models.CharField(max_length=50 , default="ca77")
    ca78 = models.CharField(max_length=50 , default="ca78")
    ca79 = models.CharField(max_length=50 , default="ca79")
    ca80 = models.CharField(max_length=50 , default="ca80")
    ca81 = models.CharField(max_length=50 , default="ca81")
    ca82 = models.CharField(max_length=50 , default="ca82")
    ca83 = models.CharField(max_length=50 , default="ca83")
    ca84 = models.CharField(max_length=50 , default="ca84")
    ca85 = models.CharField(max_length=50 , default="ca85")
    ca86 = models.CharField(max_length=50 , default="ca86")
    ca87 = models.CharField(max_length=50 , default="ca87")
    ca88 = models.CharField(max_length=50 , default="ca88")
    ca89 = models.CharField(max_length=50 , default="ca89")
    ca90 = models.CharField(max_length=50 , default="ca90")
    ca91 = models.CharField(max_length=50 , default="ca91")
    ca92 = models.CharField(max_length=50 , default="ca92")
    ca93 = models.CharField(max_length=50 , default="ca93")
    ca94 = models.CharField(max_length=50 , default="ca94")
    ca95 = models.CharField(max_length=50 , default="ca95")
    ca96 = models.CharField(max_length=50 , default="ca96")
    ca97 = models.CharField(max_length=50 , default="ca97")
    ca98 = models.CharField(max_length=50 , default="ca98")
    ca99 = models.CharField(max_length=50 , default="ca99")
    ca100 = models.CharField(max_length=50 , default="ca100")
    ca101 = models.CharField(max_length=50 , default="ca101")
    ca102 = models.CharField(max_length=50 , default="ca102")
    ca103 = models.CharField(max_length=50 , default="ca103")
    ca104 = models.CharField(max_length=50 , default="ca104")
    ca105 = models.CharField(max_length=50 , default="ca105")
    ca106 = models.CharField(max_length=50 , default="ca106")
    ca107 = models.CharField(max_length=50 , default="ca107")
    ca108 = models.CharField(max_length=50 , default="ca108")
    ca109 = models.CharField(max_length=50 , default="ca109")
    ca110 = models.CharField(max_length=50 , default="ca110")
    ca111 = models.CharField(max_length=50 , default="ca111")
    ca112 = models.CharField(max_length=50 , default="ca112")
    ca113 = models.CharField(max_length=50 , default="ca113")
    ca114 = models.CharField(max_length=50 , default="ca114")
    ca115 = models.CharField(max_length=50 , default="ca115")
    ca116 = models.CharField(max_length=50 , default="ca116")
    ca117 = models.CharField(max_length=50 , default="ca117")
    ca118 = models.CharField(max_length=50 , default="ca118")
    ca119 = models.CharField(max_length=50 , default="ca119")
    ca120 = models.CharField(max_length=50 , default="ca120")
