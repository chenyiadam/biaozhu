# biaozhu

在 $biaozhu$ 文件夹中，有 $configs$ 、 $images$ 、 $utils$ 三个文件夹，并且有 $biaozhu.py$ 、 $login.py$ 、 $recode\_1.py$ 、 $recode\_2.py$、 $注册器.py$  共5个 $Python$ 代码文件。

1. $configs$ 文件中，是用以自定义命名实体、关系的文件，你可以使用文本文件方式打开，并自定义命名实体类别、关系。（自定义实体、关系，除了 $configs$ 文件夹，  $biaozhu.py$  也需要修改）
2. $images$ 文件夹中，是一些图片文件，无需关心。
3. $utils$ 文件夹中，除了用作渲染颜色的 $Python$ 文件外，还存有一些 $HTML$ 、 $CSS$ 文件（即使你完全不了解它们也不影响你正常使用）。
4. $biaozhu.py$ 是主文件，你只需要运行它，就可以立即开始标注工作。
5. $login.py$ 是一个登录窗口，和 $biaozhu.py$ 分离，如果你对它不感兴趣，也可以将它删除，即不登陆直接开始标注工作。
6. 如果你希望尝试先登录，再标注的流程，那么你将用到 $注册器.py$ 。执行 $注册器.py$ ，会生成一个注册码，凭借注册码，可以在 $login.py$ 注册你的信息（本地模拟），程序会自动跳转到 $biaozhu.py$ 主文件。
7. 注意，$login.py$ 、  $注册器.py$   两个文件是非必要的，你可以直接运行 $biaozhu.py$ 开始你的工作。

详细教程：https://blog.csdn.net/AdamCY888/article/details/127613010
