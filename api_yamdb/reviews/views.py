from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import CommentsForm
from .models import Review, Comments, Titles


def review_detail(request, review_id):
    user = request.user
    review = get_object_or_404(Review, pk=review_id)
    author = review.author
    # review_count = Review.objects.filter(author=author).count()
    comments = Comments.objects.filter(review_id=review_id)
    form = CommentsForm(request.POST)
    context = {
        'review': review,
        'author': author,
        # 'post_count': post_count,
        'review_id': review_id,
        'user': user,
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/review_detail.html', context)

# тут надо много дорабатывать, возможно шаблоны и не нужны
@login_required
@csrf_exempt
def review_create(request):
    form = CommentsForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form = form.save(False)
        form.author = request.user
        form.save()
        return redirect('posts:profile', username=form.author)
    return render(
        request,
        'posts/create_post.html',
        {'form': form}
    )


@login_required
@csrf_exempt
def review_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.pk)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.pk)
    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'post': post, 'is_edit': is_edit}
    )


