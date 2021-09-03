# ustc-cas-mock

模仿 USTC CAS 的程序，用于开发校内网站应用阶段调试。

**请勿在生产环境部署！**

只测试了最常用的三个 CAS route：

```
/login
/serviceValidate（验证 CAS ticket）
/logout
```

没有测试过 proxy ticket。（因为我用不到，我也不知道怎么改）

## Why?

USTCCAS 比较特别的一点是，用户可以用不同的用户名登录：GID 可以，学号也可以，并且学号可以是自入学以来所有的学号。在开发时，很多同学都不会注意这件事情，这会导致一个人可以用多个不同的「身份」登录系统（并且在科大呆的时间越长，身份的数量就越多），往往是非预期的。

第二点特别的是，CAS 系统限制仅允许 ustc.edu.cn 域名的 service 使用，于是在本地开发的时候就特别难受，虽然可以用……「某些方式」绕过去，但是如果你真的拿到了一个学校域名，上线前又要大改配置，不太好受。

这个仓库代码使用了一个魔改版的 django-mama-cas，因为默认的 callback 没法方便插入特定的逻辑。

## 关于返回的属性

本仓库的逻辑是返回 CAS 能够返回的所有的信息，但是实际上，USTCCAS 在未申请权限的情况下只会返回最基本的信息：GID 和登录用的用户名，这一点需要特别注意。

此外，在 attributes 的处理上，USTCCAS 和 CAS 3.0 标准不完全一致：

USTCCAS 类似于下面这样:

```xml
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
<cas:authenticationSuccess>
<cas:user>登录用户名</cas:user>
<attributes>
<cas:gid>1234567</cas:gid>
</attributes>
</cas:authenticationSuccess>
</cas:serviceResponse>
```

而 CAS 3.0 类似于:

```xml
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
    <cas:authenticationSuccess>
        <cas:user>登录用户名</cas:user>
        <cas:attributes>
            <cas:gid>1234567</cas:gid>
        </cas:attributes>
    </cas:authenticationSuccess>
</cas:serviceResponse>
```

USTCCAS 的 attributes 是 `attributes` 而不是 `cas:attributes`。

此外：

- 有一些属性我也没有完全搞清楚，比如说 `xbm` 我就不知道是啥，反正这个值好像正常情况下应该返回 1。
- 关于人员在校状态码和人员分类码的信息，如果不适合公开，请联系我，我会立刻处理。

## 使用

首先配置虚拟环境，安装依赖，然后：

```
$ python manage.py migrate
$ python manage.py createsuperuser
```

然后可以使用创建的 superuser 登录 `/admin` 进行配置。需要注意，在添加用户后，还需要编辑用户，添加学号信息（学号值和顺序）。

当然，如果懒得配置，也可以在 cas 目录里直接：

```
$ curl -L https://github.com/taoky/ustc-cas-mock/releases/download/v0.1/test.sql | sqlite3 db.sqlite3
```

superuser 的 username/password 为 test/test。请注意在修改密码前确保服务仅本地可访问。
