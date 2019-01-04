# 微信朋友圈爬取，将头像拼成特定形状
通过ichat库爬取朋友圈头像，将头像拼成一个‘猪’字。  
制作思路：  
从带猪字的图像的原点（0,0）开始遍历，图像模式为灰度，将小于255的像素点全部记录下来，计算占整个图片的多少，再根据需要拼接头像的多少计算出每个头像的大小。  
新建一张白色图片，按照小于255的点，粘贴头像图片。

我这里总共有255个头像，上述算出来拼好后只用了250个头像，这样计算的方式不是很精确。  

图片效果：

![](https://github.com/cqzan/addimg/blob/master/猪.jpg)
