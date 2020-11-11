from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post, Category, Tag

from .adminforms import PostAdminForm

from mysite.custom_site import custom_site

from mysite.base_admin import BaseOwnerAdmin

from django.contrib.admin.models import LogEntry


class PostInline(admin.TabularInline): #StackedInline 样式不同
	fields = ('title', 'des')
	extra = 1 #控制额外多个
	model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
	inlines = [PostInline, ]
	list_display = ('name', 'status', 'is_nav','post_count')
	fields = ('name', 'status', 'is_nav')

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		return super(CategoryAdmin, self).save_model(request, obj, form, change)
	def post_count(self, obj):
		return obj.post_set.count()

	post_count.short_description = '文章数量'



@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
	list_display = ('name', 'status',)
	fields = ('name', 'status')

	def save_model(self, request, obj, form, change):
		obj.owner = request.user
		return super(TagAdmin, self).save_model(request, obj, form, change)


'''class CategoryOwnerFilter(admin.SimpleListFilter):
	"""自定义过滤器只展示当前用户分类"""

	title = "分类过滤器"
	parameter_name = 'owner_category'

	def lookups(self, request, model_admin):
		return Category.objects.filter(owner=request.user).values_list('id', 'name')
		#return Category.objects.filter(status=Category.STATUS_NORMAL)

	def queryset(self, request, queryset):
		category_id = self.value()
		if category_id:
			return queryset.filter(category_id=category_id)
		return queryset'''


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
	form = PostAdminForm

	
	list_display = [
		'title', 'category', 'status', 'operator',]
	list_display_links = []

	#list_filter = [CategoryOwnerFilter, ]
	list_filter = ['category', ]
	search_fields = ['title', 'category__name']

	actions_on_top = True
	actions_on_bottom = True

	#编辑页面
	save_on_top = True

	exclude = ['owner']
	'''fields = (
		('category','title'),'desc','status','content', 'tag',)'''
	fieldsets = (
		('基础配置', {
			'description': '基础配置描述',
			'fields': (
				('title', 'category'),
				'status',
			),

			}),
			('内容', {
				'fields':(
					'des','content_html'
				),
			}),
			('额外信息', {
				'classes': ('wide',),
				'fields': ('tag',),
			})
	)
	#filter_horizontal = ('tag', )
	filter_vertical = ('tag', )
	def operator(self,obj):
		return format_html(
			'<a href="{}">编辑</a>',
			reverse('cus_admin:blog_post_change', args=(obj.id,))
			)
		operator.short_description = '操作'

	class Media:
		css = {
			'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/\
				bootstrap.min.css", ),
		}
		js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )

	'''def save_model(self, request, obj, form, change):
		obj.owner = request.user
		return super(PostAdmin,self).save_model(request, obj, form, change)

	def get_queryset(self, request):
		qs = super(PostAdmin, self).get_queryset(request)
		return qs.filter(owner = request.user)'''
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
	list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
	