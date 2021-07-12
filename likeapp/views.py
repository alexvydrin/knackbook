from django.http import JsonResponse
from django.template.loader import render_to_string

from likeapp.models import LikeArticle
from mainapp.models import Article
from notificationapp.models import Notification


def likes(request, pk):
    """Постановка и снятие лайков"""
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
            'like_active': len(likes.filter(is_active=True, user=request.user.id))
        }

        if likes.filter(is_active=True, user=request.user.id, article=pk):
            article = Article.objects.filter(id=pk).first()
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
