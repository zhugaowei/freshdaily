一、下面来看看：filter查询：

1.__contains(包含)

shell命令下查询：Blog.objects.filter(title__contains ="django")------------------>返回一个queryset[]查询(查询集)只能输入一个值。加上一个"i"后不区别大小写【sql等数据库中】

2.__in （其中之一，可以传入一个列表，传多个值。）

Blog.objects.filter(id__in = [3,6,9])

3.__range(一个范围，使用元祖)：

> Blog.objects.filter(id__range =(30,45))



Diango模板中的forloop变量
{% for %} 标签在循环中设置了一个特殊的 forloop 模板变量。这个变量能提供一些当前循环进展的信息：

1. forloop.counter  ： forloop.counter总是一个表示当前循环的执行次数的整数计数器。这个计数器是从1开始的，所以在第一次循环时forloop.counter 将会被设置为1。例子如下：

{% for item in todo_list %}
<p>{{ forloop.counter }}: {{ item }}</p>
{% endfor %}

2.  forloop.counter0 ： forloop.counter0 类似于 forloop.counter ，但是它是从0计数的。第一次执行循环时这个变量会被设置为0。
3.  forloop.revcounter ： forloop.revcounter 是表示循环中剩余项的整型变量。在循环初次执行时 forloop.revcounter 将被设置为序列中项的总数。最后一次循环执行中，这个变量将被置1。 

4. forloop.revcounter0 ： forloop.revcounter 0类似于 forloop.revcounter ，但它以0做为结束索引。在第一次执行循环时，该变量会被置为序列的项的个数减1。在最后一迭代时，该变量为0。

5. forloop.first 是一个布尔值。在第一次执行循环时该变量为True，在下面的情形中这个变量是很有用的。
{% for object in objects %}
{% if forloop.first %}<li class="first">{% else %}<li>{% endif %}
{{ object }}
</li>
{% endfor %}

6. forloop.last 是一个布尔值；在最后一次执行循环时被置为True。一个常见的用法是在一系列的链接之间放置管道符（|）

{% for link in links %}{{ link }}{% if not forloop.last %} | {% endif %}{% endfor %}
显示如下：
Link1 | Link2 | Link3 | Link4

7. forloop.parentloop 是一个指向当前循环的上一级循环的 forloop 对象的引用（在嵌套循环的情况下）。例子在此：
{% for country in countries %}
<table>
{% for city in country.city_list %}
<tr>
<td>Country #{{ forloop.parentloop.counter }}</td>
<td>City #{{ forloop.counter }}</td>
<td>{{ city }}</td>
</tr>
{% endfor %}
</table>
{% endfor %}

注1.  forloop 变量仅仅能够在循环中使用，在模板解析器碰到 {% endfor %} 标签时， forloop 就不可访问了。

注2.  Context和forloop变量

  在一个{% for %} 块中，已存在的变量会被移除，以避免 forloop 变量被覆盖。Django会把这个变量移动到
forloop.parentloop 中。通常我们不用担心这个问题，但是一旦我们在模板中定义了 forloop 这个变量（当然我们反对这样做），在{% for %} 块中它会在forloop.parentloop 被重新命名。


pk字段同样也支持跨模型的查询，比如下面的三种写法，效果是一样的，都是表示查找所有Blog的ID为1的Entry集合：

>>> Entry.objects.filter(blog__id__exact=1) # 显示的使用__exact
>>> Entry.objects.filter(blog__id=1) # 隐含的使用__exact
>>> Entry.objects.filter(blog__pk=1) # __pk 相当于 __id__exact
