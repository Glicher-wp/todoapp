from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.db.models import Count
from .models import PriorityCount, TagCount, TodoItem


@receiver(m2m_changed, sender=TodoItem.tags.through)
def task_tags_updated(sender, instance, action, model, **kwargs):
    if action != "post_add":
        return
    for tag in model.objects.all():
        count = tag.taggit_taggeditem_items.count()
        t = TagCount.objects.filter(tag_id=tag.id).first()
        if t is None:
            t = TagCount.objects.get_or_create(
            tag_slug=tag.slug,
            tag_name=tag.name,
            tag_id=tag.id,
            tag_count=count,
        )
            list(t)[0].save()
        else:
            t.tag_count = count

            t.save()


@receiver(post_save, sender=TodoItem)
def task_priority_update(sender, instance, **kwargs):
    count_high = sender.objects.filter(priority=1).count()
    count_medium = sender.objects.filter(priority=2).count()
    count_low = sender.objects.filter(priority=3).count()
    p = (PriorityCount(priority=1, priority_count=count_high), PriorityCount(priority=2, priority_count=count_medium),
         PriorityCount(priority=3, priority_count=count_low))
    for i in p:
        i.save()

