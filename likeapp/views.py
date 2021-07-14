from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string

from authapp.models import User
from likeapp.models import LikeArticle, LikeUser
from mainapp.models import Article
from notificationapp.models import Notification


@login_required
def likes_article(request, pk):
    """Постановка и снятие лайков статьям"""
    if request.is_ajax():
        like = LikeArticle.objects.filter(article=pk,
                                          user=request.user.id).first()
        if like:
            if like.is_active:
                like.is_active = False
            else:
                like.is_active = True
        else:
            like = LikeArticle.objects.create(
                article=Article.objects.filter(id=pk).first(),
                user=request.user,
            )
        like.save()

        likes = LikeArticle.objects

        context = {
            'likes': len(likes.filter(is_active=True, article=pk)),
            'like_active': len(
                likes.filter(is_active=True, user=request.user.id))
        }

        if likes.filter(is_active=True, user=request.user.id, article=pk):
            article = Article.objects.filter(id=pk).first()
            if article.user != request.user:
                Notification.add_notification(
                    content='лайк статья',
                    user_to=article.user,
                    user_from=request.user,
                    article=article,
                    comment=None
                )

        result = render_to_string(
            'likeapp/like_article.html', context)

        return JsonResponse({'result': result})


@login_required
def likes_user(request, pk):
    """Постановка и снятие лайков пользователям"""
    if request.is_ajax():
        like = LikeUser.objects.filter(user_to=pk,
                                       user_from=request.user.id).first()

        if like:
            if like.is_active:
                like.is_active = False
            else:
                like.is_active = True
        else:
            like = LikeUser.objects.create(
                user_to=User.objects.filter(id=pk).first(),
                user_from=request.user,
            )
        like.save()

        likes = LikeUser.objects

        context = {
            'likes_user': len(likes.filter(is_active=True, user_to=pk)),
            'like_active_user': len(likes.filter(is_active=True, user_to=pk,
                                                 user_from=request.user.id))
        }

        result = render_to_string(
            'likeapp/like_user.html', context)

        return JsonResponse({'result': result})
