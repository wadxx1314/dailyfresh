from django.shortcuts import render,redirect
import re
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.conf import settings
from user.models import User,Address
from goods.models import GoodsSKU
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
import time
from django.core.mail import send_mail
from django.http import HttpResponse
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate,login,logout
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection



#注册
def register(request):
    if request.method == 'GET':
        #显示注册页面
        return render(request,'register.html')
    else:
        #进行注册处理
        #接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        #进行数据的校验
        if not all([username,password,email,allow]):
            #数据不完整，返回注册首页
            return render(request,'register.html',{'errmag':'数据不完整'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request,'register.html',{'errmag':'邮箱不合法'})
        if allow !='on':
            return render(request,'register.html',{'errmag':'请同意协议'})

        #进行业务处理，完成用户注册
        user = User.objects.create_user(username,email,password)
        user.is_active = 0
        user.save()

        #返回应答跳转到首页
        return redirect(reverse('good:index'))

def register_handle(request):
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    # 进行数据的校验
    if not all([username, password, email, allow]):
        # 数据不完整，返回注册首页
        return render(request, 'register.html', {'errmag':'数据不完整'})
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmag':'邮箱不合法'})
    if allow != 'on':
        return render(request, 'register.html', {'errmag':'请同意协议'})

    # 进行业务处理，完成用户注册
    user = User.objects.create_user(username,email, password)
    user.is_active = 0
    user.save()

    # 返回应答跳转到首页
    return redirect(reverse('goods:index'))


#使用类注册邮箱

class RegisterView(View):
    '''注册'''
    #显示注册的页面
    def get(self,request):
        return render(request,'register.html')

    #进行注册处理
    def post(self,request):
        #接受用户注册的数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

    #进行数据检验
        if not all([username, password, email, allow]):
            return render(request, 'register.html', {'errmag':'数据不完整'})

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmag':'邮箱不合法'})

        if allow != 'on':
            return render(request, 'register.html', {'errmag':'请同意协议'})



    #校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request,'register.html',{'errmag':'用户名已经存在'})

    #进行业务处理：完成用户注册
        user = User.objects.create_user(username,email,password)
        user.is_active = 0
        user.save()

    #给用户注册邮箱发送激活邮件
    #激活链接中需要包含的用户身份信息/user/active/3

    #对用户的身份信息进行加密，生成激活的token
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()

        #使用celery发送邮件
        send_register_active_email.delay(email,username,token)

    #返回应答发送邮件
        return redirect(reverse('goods:index'))

#用户激活
class ActiveView(View):
    def get(self,request,token):
        #实例化密钥,获取对象
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
        #对用户的token进行解密
            info = serializer.loads(token)
        #获取激活用户的id
            user_id = info['confirm']
        #根据用户的id获取用户的信息
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
        #跳转到登陆页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
        #激活连接已经失效
            return HttpResponse('激活连接已经失效')

class LoginView(View):
    '''登陆'''
    def get(self,request):
        '''显示登陆页面'''
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request,'login.html',{'username':username,'checked':checked})
    def post(self,request):
        '''登陆校验'''
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        #数据校验
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'数据不完正'})
        #业务处理：登陆验证
        user = authenticate(username=username,password=password)
        print('user:',user)
        #用户名和密码正确
        if user is not None:
            #记住用户的登陆状态
            if user.is_active:
                login(request,user)
                #获取用户登陆后的url地址
                #如多获取不到next,默认跳转到首页
                next_url=request.GET.get('next',reverse('goods:index'))

                #跳转到登陆首页
                response=redirect(next_url)
                #判断是否需要记住用户名和密码
                remenber=request.POST.get('remember')
                if remenber =='on':
                    response.set_cookie('username',username)
                else:
                    response.delete_cookie('username')

                return response
            else:
                return render(request,'login.html',{'errmsg':'账户为激活'})

        else:
            print(username)
            print(password)
            return render(request,'login.html',{'errmsg':'用户名或密码错误'})
class logoutView(View):
    def get(self,request):
        #清楚session的信息
        logout(request)
        return redirect(reverse('goods:index'))




class UserInfoView(LoginRequiredMixin,View):
    '''用户中心信息页'''
    def get(self,request):
        #用户的个人信息
        user = request.user
        address = Address.objects.get_default_address(user=user)
        #用户历史浏览记录
        conn = get_redis_connection('default')
        list_key = 'history_%d'%user.id
        #从redis中获取用户浏览商品id的列表
        sku_ids = conn.lrange(list_key,0,4)
        #遍历查询用户商品信息，追加到goods_li列表中
        goods_li=[]
        for id in sku_ids:
            goods=GoodsSKU.objects.get(id=id)
            goods_li.append(goods)
        #模板上下文
        context = {'page':'user','address':address,'goods_li':goods_li}

        return render(request,'user_center_info.html',context)


class UserOrderView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'user_center_order.html',{'page':'order'})

class AddressView(LoginRequiredMixin,View):
    '''用户中心地址页'''
    def get(self,request):
        #显示地址
        #获取登陆用户对象
        user = request.user

        address = Address.objects.get_default_address(user=user)

        return render(request,'user_center_site.html',{'page':'address','address':address})

    def post(self,request):

        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        #数据的校验
        if not all([receiver,addr,phone]):
            return render(request,'user_center_site.html',{'errmsg':'数据不完整'})
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$',phone):
            return render(request, 'user_center_site.html', {'errmsg': '联系方式不正确'})

        #获取登陆用户的对象
        user = request.user

        address = Address.objects.get_default_address(user=user)
        print(receiver,phone)
        if address:
            is_default = False

        else:
            is_default = True
        #添加地址
        Address.objects.create(
                                user = user,
                                receiver = receiver,
                                addr = addr,
                                zip_code = zip_code,
                                phone = phone,
                                is_default = is_default)
        return redirect(reverse('user:address'))



