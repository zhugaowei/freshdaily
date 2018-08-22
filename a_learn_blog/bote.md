html——name与value的使用

一、name使用
<form action="Handler2.ashx" method="post" enctype="application/x-www-form-urlencoded">
<p>客户名称: <input type="text" name="CustomerName" style="width: 300px" /></p>
<p>客户电话: <input type="text" name="CustomerTel" style="width: 300px" /></p>
<p><input type="submit" value="提交" /></p>
</form>
1、name的作用是用来让后台接受数据时使用的KEY值
2、同一个Form里不能有多个name属性相同的HTML标记，但如果一个网页中有多个Form，则不同的Form里可以有同个Name属性的标记。而ID是全局的，在一个HTML文档里不能有多个节点使用相同的ID，无论它处在哪个Form里。