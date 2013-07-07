from datetime import datetime

from django import template
from redis_metrics.models import R

register = template.Library()


@register.inclusion_tag("redis_metrics/_gauge.html")
def gauge(slug, maximum=9000, size=125):
    r = R()
    return {
        'slug': slug,
        'current_value': r.get_gauge(slug),
        'max_value': maximum,
        'size': size,
        'yellow': maximum - (maximum / 2),
        'red': maximum - (maximum / 4),
    }


@register.inclusion_tag("redis_metrics/_metric_list.html")
def metric_list():
    return {
        'metrics': R().metric_slugs_by_category(),
    }


@register.inclusion_tag("redis_metrics/_metric_detail.html")
def metric_detail(slug):
    return {
        'slug': slug,
        'metrics': R().get_metric(slug),
    }


@register.inclusion_tag("redis_metrics/_metric_history.html")
def metric_history(slug, granularity="daily", since=None):
    """Template Tag to display a metric's history.

    * ``slug`` -- the metric's unique slug
    * ``granularity`` -- the granularity: daily, weekly, monthly, yearly
    * ``since`` -- a date string of the form "YYYY-mm-dd";

    """
    try:
        since_date = datetime.strptime(since, "%Y-%m-%d")
    except (TypeError, ValueError):
        since_date = None

    metric_history = R().get_metric_history(
        slugs=slug,
        since=since_date,
        granularity=granularity
    )

    return {
        'slug': slug,
        'granularity': granularity,
        'metric_history': metric_history,
    }
